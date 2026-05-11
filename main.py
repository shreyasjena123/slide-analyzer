import os
import tempfile

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from analyzer import analyze_deck
from parser import extract
from renderer import render_pdf_to_pngs

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    learning_objective: str = Form(...),
):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        slides = extract(tmp_path)
        pngs = render_pdf_to_pngs(tmp_path)
        results = analyze_deck(slides, pngs, learning_objective)
    finally:
        os.unlink(tmp_path)

    slide_data = [
        {"slide": slide, "png": png, "result": result}
        for slide, png, result in zip(slides, pngs, results)
    ]
    total_violations = sum(len(d["result"]["violations"]) for d in slide_data)

    html = templates.get_template("report.html").render(
        deck_name=file.filename,
        learning_objective=learning_objective,
        slide_data=slide_data,
        total_violations=total_violations,
    )

    return Response(
        content=html,
        media_type="text/html",
        headers={"Content-Disposition": 'attachment; filename="report.html"'},
    )
