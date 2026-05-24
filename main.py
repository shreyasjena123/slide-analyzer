import os
import tempfile
from collections import defaultdict

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from analyzer import analyze_deck
from parser import extract
from renderer import render_to_pngs

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
):
    suffix = os.path.splitext(file.filename)[1].lower()
    tmp_suffix = suffix if suffix in (".pdf", ".pptx") else ".pdf"
    with tempfile.NamedTemporaryFile(suffix=tmp_suffix, delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        slides = extract(tmp_path)
        pngs = render_to_pngs(tmp_path)
        results = await analyze_deck(slides, pngs)
        assert len(slides) == len(pngs) == len(results)
    finally:
        os.unlink(tmp_path)

    slide_data = []
    for slide, png, result in zip(slides, pngs, results):
        result["violations"] = [v for v in result["violations"] if v.get("severity") != "low"]
        slide_data.append({"slide": slide, "png": png, "result": result})

    total_violations = sum(len(d["result"]["violations"]) for d in slide_data)
    scorecard = _build_scorecard(slide_data)

    html = templates.get_template("report.html").render(
        deck_name=file.filename,
        slide_data=slide_data,
        total_violations=total_violations,
        scorecard=scorecard,
    )

    return Response(
        content=html,
        media_type="text/html",
        headers={"Content-Disposition": 'attachment; filename="report.html"'},
    )


_ALL_PRINCIPLES = [
    "Multimedia", "Coherence", "Spatial Contiguity", "Temporal Contiguity",
    "Modality", "Pre-Training", "Redundancy", "Signaling",
]
_PRINCIPLE_D = {
    "Multimedia":          1.35,
    "Temporal Contiguity": 1.31,
    "Modality":            1.00,
    "Coherence":           0.86,
    "Spatial Contiguity":  0.82,
    "Pre-Training":        0.78,
    "Redundancy":          0.72,
    "Signaling":           0.70,
}


def _build_scorecard(slide_data: list[dict]) -> dict:
    """Compute per-principle violation counts and an overall health score."""
    violation_counts = defaultdict(int)
    content_slides = [d for d in slide_data if d["slide"].slide_type() == "content"]
    n_content = len(content_slides)

    for d in content_slides:
        for v in d["result"].get("violations", []):
            violation_counts[v["principle"]] += 1

    principles = []
    total_weighted = 0.0
    max_weighted = 0.0
    for p in _ALL_PRINCIPLES:
        count = violation_counts[p]
        d_val = _PRINCIPLE_D[p]
        # pass rate: fraction of content slides that passed this principle
        pass_rate = 1.0 - (count / n_content) if n_content > 0 else 1.0
        pass_rate = max(0.0, min(1.0, pass_rate))
        principles.append({
            "name": p,
            "violations": count,
            "pass_rate": pass_rate,
            "d_value": d_val,
        })
        total_weighted += pass_rate * d_val
        max_weighted += d_val

    overall = round((total_weighted / max_weighted) * 100) if max_weighted > 0 else 100
    high_violations = sum(
        1 for d in content_slides
        for v in d["result"].get("violations", [])
        if v.get("severity") == "high"
    )
    return {
        "principles": principles,
        "overall_score": overall,
        "n_content_slides": n_content,
        "high_violations": high_violations,
    }
