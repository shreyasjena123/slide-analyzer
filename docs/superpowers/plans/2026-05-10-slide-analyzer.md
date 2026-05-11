# Slide Analyzer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a FastAPI app that accepts a PDF slide deck + learning objective, analyzes each slide against Mayer's 5 Multimedia Learning Principles via Claude (multimodal), and returns a self-contained HTML report.

**Architecture:** Upload endpoint saves PDF to temp file → `parser.py` extracts `SlideData` → `renderer.py` renders pages to PNG → `analyzer.py` calls Claude once per slide with image + metadata → Jinja2 renders self-contained HTML report → returned as file download.

**Tech Stack:** Python, FastAPI, PyMuPDF (fitz), Anthropic SDK (claude-sonnet-4-6), Jinja2, pytest

---

## File Map

| File | Status | Responsibility |
|---|---|---|
| `parser.py` | Done | Extract `SlideData` from PDF |
| `principles.py` | Done | Load Mayer chapter text |
| `renderer.py` | Create | PDF pages → base64 PNG list |
| `analyzer.py` | Create | Per-slide Claude API call → violations dict |
| `main.py` | Create | FastAPI app — upload form + /analyze endpoint |
| `templates/index.html` | Create | Upload form with learning objective field |
| `templates/report.html` | Create | Jinja2 report with inline CSS |
| `static/style.css` | Create | Upload form styling |
| `tests/test_renderer.py` | Create | Unit tests for renderer |
| `tests/test_analyzer.py` | Create | Unit tests for analyzer (mocked Claude) |
| `tests/test_main.py` | Create | Integration test for /analyze endpoint |

---

## Task 1: renderer.py — PDF pages → base64 PNGs

**Files:**
- Create: `renderer.py`
- Create: `tests/test_renderer.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_renderer.py
import base64
import os
import tempfile

import fitz


def _make_test_pdf(path: str, pages: int = 2) -> None:
    doc = fitz.open()
    for i in range(pages):
        page = doc.new_page()
        page.insert_text((72, 72), f"Test slide {i + 1}")
    doc.save(path)


def test_render_returns_one_png_per_page():
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        tmp = f.name
    _make_test_pdf(tmp, pages=3)
    try:
        from renderer import render_pdf_to_pngs
        pngs = render_pdf_to_pngs(tmp)
        assert len(pngs) == 3
    finally:
        os.unlink(tmp)


def test_render_returns_valid_base64_png():
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        tmp = f.name
    _make_test_pdf(tmp, pages=1)
    try:
        from renderer import render_pdf_to_pngs
        pngs = render_pdf_to_pngs(tmp)
        decoded = base64.b64decode(pngs[0])
        assert decoded[:8] == b'\x89PNG\r\n\x1a\n'  # PNG magic bytes
    finally:
        os.unlink(tmp)
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
cd /Users/shreyasjena/slide-analyzer && python -m pytest tests/test_renderer.py -v
```

Expected: `ModuleNotFoundError: No module named 'renderer'`

- [ ] **Step 3: Implement renderer.py**

```python
# renderer.py
import base64
import fitz


def render_pdf_to_pngs(path: str, dpi: int = 150) -> list[str]:
    """Render each PDF page to a base64-encoded PNG string."""
    doc = fitz.open(path)
    matrix = fitz.Matrix(dpi / 72, dpi / 72)
    return [
        base64.b64encode(page.get_pixmap(matrix=matrix).tobytes("png")).decode()
        for page in doc
    ]
```

- [ ] **Step 4: Run tests to confirm they pass**

```bash
cd /Users/shreyasjena/slide-analyzer && python -m pytest tests/test_renderer.py -v
```

Expected: `2 passed`

- [ ] **Step 5: Commit**

```bash
cd /Users/shreyasjena/slide-analyzer && git add renderer.py tests/test_renderer.py && git commit -m "feat: add PDF-to-PNG renderer"
```

---

## Task 2: analyzer.py — per-slide Claude API call

**Files:**
- Create: `analyzer.py`
- Create: `tests/test_analyzer.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_analyzer.py
import json
from unittest.mock import MagicMock, patch

from parser import SlideData


def _make_slide(num: int = 1) -> SlideData:
    return SlideData(
        num=num,
        title="Test Slide",
        body_text="Some body text",
        notes="",
        image_count=0,
        image_positions=[],
        text_box_positions=[],
        slide_width=960.0,
        slide_height=540.0,
    )


MOCK_RESPONSE_JSON = {
    "violations": [
        {
            "principle": "Multimedia",
            "severity": "high",
            "finding": "Concept explained in text only with no supporting image.",
            "recommendation": "Add a diagram illustrating the process.",
        }
    ],
    "passes": ["Coherence", "Signaling", "Spatial Contiguity", "Redundancy"],
}


def _mock_claude_message(response_dict: dict) -> MagicMock:
    msg = MagicMock()
    msg.content = [MagicMock(text=json.dumps(response_dict))]
    return msg


def test_analyze_slide_returns_violations_and_passes():
    with patch("analyzer.client.messages.create", return_value=_mock_claude_message(MOCK_RESPONSE_JSON)):
        from analyzer import analyze_slide
        result = analyze_slide(_make_slide(), "fake_b64_png", "Understand ATP production")

    assert result["violations"][0]["principle"] == "Multimedia"
    assert result["violations"][0]["severity"] == "high"
    assert "Coherence" in result["passes"]


def test_analyze_deck_calls_claude_once_per_slide():
    with patch("analyzer.client.messages.create", return_value=_mock_claude_message(MOCK_RESPONSE_JSON)) as mock_create:
        from analyzer import analyze_deck
        results = analyze_deck(
            [_make_slide(1), _make_slide(2)],
            ["fake_b64_1", "fake_b64_2"],
            "Understand ATP production",
        )

    assert len(results) == 2
    assert mock_create.call_count == 2


def test_analyze_slide_passes_image_as_base64_block():
    with patch("analyzer.client.messages.create", return_value=_mock_claude_message(MOCK_RESPONSE_JSON)) as mock_create:
        from analyzer import analyze_slide
        analyze_slide(_make_slide(), "abc123png", "Learn something")

    call_args = mock_create.call_args
    content = call_args.kwargs["messages"][0]["content"]
    image_block = next(b for b in content if b.get("type") == "image")
    assert image_block["source"]["data"] == "abc123png"
    assert image_block["source"]["media_type"] == "image/png"
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
cd /Users/shreyasjena/slide-analyzer && python -m pytest tests/test_analyzer.py -v
```

Expected: `ModuleNotFoundError: No module named 'analyzer'`

- [ ] **Step 3: Implement analyzer.py**

```python
# analyzer.py
import json

from anthropic import Anthropic

from parser import SlideData
from principles import PRINCIPLES_TEXT

client = Anthropic()

_SYSTEM_PROMPT = f"""You are an expert in Mayer's Multimedia Learning Principles. \
Use the research below to evaluate slides.

{PRINCIPLES_TEXT}

Respond ONLY with valid JSON — no prose, no markdown fences."""

_USER_TEMPLATE = """\
Learning objective: {objective}

Slide metadata:
{metadata}

Analyze this slide against all 5 Mayer principles. Return ONLY valid JSON:
{{
  "violations": [
    {{
      "principle": "Coherence|Signaling|Spatial Contiguity|Multimedia|Redundancy",
      "severity": "high|medium|low",
      "finding": "one sentence describing the issue",
      "recommendation": "one sentence fix"
    }}
  ],
  "passes": ["principle names with no violations"]
}}"""


def analyze_slide(slide: SlideData, png_b64: str, learning_objective: str) -> dict:
    prompt = _USER_TEMPLATE.format(
        objective=learning_objective,
        metadata=slide.to_prompt_text(),
    )
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": png_b64,
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    )
    return json.loads(response.content[0].text)


def analyze_deck(slides: list[SlideData], pngs: list[str], learning_objective: str) -> list[dict]:
    return [analyze_slide(slide, png, learning_objective) for slide, png in zip(slides, pngs)]
```

- [ ] **Step 4: Run tests to confirm they pass**

```bash
cd /Users/shreyasjena/slide-analyzer && python -m pytest tests/test_analyzer.py -v
```

Expected: `3 passed`

- [ ] **Step 5: Commit**

```bash
cd /Users/shreyasjena/slide-analyzer && git add analyzer.py tests/test_analyzer.py && git commit -m "feat: add per-slide Claude analyzer"
```

---

## Task 3: Templates and static CSS

**Files:**
- Create: `templates/index.html`
- Create: `templates/report.html`
- Create: `static/style.css`

No tests for static HTML/CSS — verified visually after Task 4.

- [ ] **Step 1: Create templates/index.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide Analyzer</title>
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>
  <main class="upload-form">
    <h1>Slide Analyzer</h1>
    <p>Analyze your PDF slides against Mayer's Multimedia Learning Principles.</p>
    <form action="/analyze" method="post" enctype="multipart/form-data">
      <label>
        PDF Slide Deck
        <input type="file" name="file" accept=".pdf" required>
      </label>
      <label>
        Learning Objective
        <input
          type="text"
          name="learning_objective"
          placeholder="e.g. Students will understand how ATP is produced in mitochondria"
          required
        >
      </label>
      <button type="submit">Analyze Slides</button>
    </form>
  </main>
</body>
</html>
```

- [ ] **Step 2: Create static/style.css**

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: system-ui, -apple-system, sans-serif;
  background: #f5f5f5;
  color: #1a1a1a;
  line-height: 1.5;
}

.upload-form {
  max-width: 560px;
  margin: 6rem auto;
  background: #fff;
  padding: 2.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}

h1 { font-size: 1.5rem; margin-bottom: 0.5rem; }
p { color: #555; margin-bottom: 1.5rem; }

label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

input[type="file"],
input[type="text"] {
  display: block;
  width: 100%;
  margin-top: 0.375rem;
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 0.9375rem;
  font-weight: 400;
}

button {
  margin-top: 0.5rem;
  width: 100%;
  padding: 0.625rem;
  background: #2563eb;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
}

button:hover { background: #1d4ed8; }
```

- [ ] **Step 3: Create templates/report.html**

Note: report is downloaded as a file, so CSS must be inline (no `/static/` link).

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Slide Analysis Report</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: system-ui, -apple-system, sans-serif; background: #f5f5f5; color: #1a1a1a; line-height: 1.5; padding: 2rem; }
    .header { max-width: 900px; margin: 0 auto 2rem; background: #fff; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.07); }
    .header h1 { font-size: 1.75rem; margin-bottom: 0.75rem; }
    .header p { color: #555; margin-bottom: 0.25rem; }
    .summary-badge { display: inline-block; margin-top: 0.75rem; padding: 0.25rem 0.75rem; background: #fee2e2; color: #991b1b; border-radius: 999px; font-weight: 700; font-size: 0.875rem; }
    .summary-badge.clean { background: #dcfce7; color: #166534; }
    .slide { max-width: 900px; margin: 0 auto 2rem; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.07); overflow: hidden; }
    .slide-header { padding: 1rem 1.5rem; border-bottom: 1px solid #e5e7eb; font-weight: 700; font-size: 1rem; }
    .slide-body { display: flex; gap: 1.5rem; padding: 1.5rem; }
    .slide-thumb { flex-shrink: 0; width: 280px; }
    .slide-thumb img { width: 100%; border: 1px solid #e5e7eb; border-radius: 4px; }
    .slide-findings { flex: 1; }
    .violation { margin-bottom: 1rem; padding: 0.75rem 1rem; border-left: 4px solid #f59e0b; background: #fffbeb; border-radius: 0 4px 4px 0; }
    .violation.high { border-color: #ef4444; background: #fef2f2; }
    .violation.low { border-color: #3b82f6; background: #eff6ff; }
    .badge { display: inline-block; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.375rem; }
    .violation p { font-size: 0.9rem; margin-top: 0.25rem; }
    .pass { font-size: 0.875rem; color: #166534; padding: 0.2rem 0; }
    .passes-header { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: #6b7280; margin-top: 1rem; margin-bottom: 0.25rem; }
  </style>
</head>
<body>
  <div class="header">
    <h1>Slide Analysis Report</h1>
    <p><strong>Deck:</strong> {{ deck_name }}</p>
    <p><strong>Learning objective:</strong> {{ learning_objective }}</p>
    <span class="summary-badge {% if total_violations == 0 %}clean{% endif %}">
      {% if total_violations == 0 %}No violations found{% else %}{{ total_violations }} violation{{ 's' if total_violations != 1 else '' }} found{% endif %}
    </span>
  </div>

  {% for item in slide_data %}
  <div class="slide">
    <div class="slide-header">
      Slide {{ item.slide.num }}{% if item.slide.title %}: {{ item.slide.title }}{% endif %}
    </div>
    <div class="slide-body">
      <div class="slide-thumb">
        <img src="data:image/png;base64,{{ item.png }}" alt="Slide {{ item.slide.num }}">
      </div>
      <div class="slide-findings">
        {% if item.result.violations %}
          {% for v in item.result.violations %}
          <div class="violation {{ v.severity }}">
            <span class="badge">⚠ {{ v.principle }} &middot; {{ v.severity }} priority</span>
            <p><strong>Finding:</strong> {{ v.finding }}</p>
            <p><strong>Fix:</strong> {{ v.recommendation }}</p>
          </div>
          {% endfor %}
        {% endif %}

        {% if item.result.passes %}
        <div class="passes-header">Passes</div>
        {% for p in item.result.passes %}
        <div class="pass">✓ {{ p }}</div>
        {% endfor %}
        {% endif %}

        {% if not item.result.violations and not item.result.passes %}
        <p style="color:#6b7280;font-size:0.9rem;">No analysis data for this slide.</p>
        {% endif %}
      </div>
    </div>
  </div>
  {% endfor %}
</body>
</html>
```

- [ ] **Step 4: Commit**

```bash
cd /Users/shreyasjena/slide-analyzer && git add templates/ static/ && git commit -m "feat: add upload form and report templates"
```

---

## Task 4: main.py — FastAPI app

**Files:**
- Create: `main.py`
- Create: `tests/test_main.py`

- [ ] **Step 1: Write failing test**

```python
# tests/test_main.py
import json
import os
import tempfile
from unittest.mock import MagicMock, patch

import fitz
from fastapi.testclient import TestClient


def _make_pdf_bytes(pages: int = 2) -> bytes:
    doc = fitz.open()
    for i in range(pages):
        page = doc.new_page()
        page.insert_text((72, 72), f"Slide {i + 1}")
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        doc.save(f.name)
        path = f.name
    with open(path, "rb") as f:
        data = f.read()
    os.unlink(path)
    return data


MOCK_RESULT = {
    "violations": [
        {
            "principle": "Multimedia",
            "severity": "high",
            "finding": "No image present.",
            "recommendation": "Add a diagram.",
        }
    ],
    "passes": ["Coherence", "Signaling", "Spatial Contiguity", "Redundancy"],
}


def _mock_msg(d: dict) -> MagicMock:
    m = MagicMock()
    m.content = [MagicMock(text=json.dumps(d))]
    return m


def test_index_returns_upload_form():
    from main import app
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "application/pdf" in response.text


def test_analyze_returns_html_download():
    from main import app
    client = TestClient(app)
    pdf_bytes = _make_pdf_bytes(pages=1)

    with patch("analyzer.client.messages.create", return_value=_mock_msg(MOCK_RESULT)):
        response = client.post(
            "/analyze",
            data={"learning_objective": "Understand photosynthesis"},
            files={"file": ("deck.pdf", pdf_bytes, "application/pdf")},
        )

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "attachment" in response.headers["content-disposition"]
    assert "Understand photosynthesis" in response.text
    assert "Multimedia" in response.text


def test_analyze_embeds_slide_thumbnail():
    from main import app
    client = TestClient(app)
    pdf_bytes = _make_pdf_bytes(pages=1)

    with patch("analyzer.client.messages.create", return_value=_mock_msg(MOCK_RESULT)):
        response = client.post(
            "/analyze",
            data={"learning_objective": "Learn something"},
            files={"file": ("deck.pdf", pdf_bytes, "application/pdf")},
        )

    assert "data:image/png;base64," in response.text
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
cd /Users/shreyasjena/slide-analyzer && python -m pytest tests/test_main.py -v
```

Expected: `ModuleNotFoundError: No module named 'main'`

- [ ] **Step 3: Implement main.py**

```python
# main.py
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
        headers={"Content-Disposition": f'attachment; filename="report.html"'},
    )
```

- [ ] **Step 4: Add pytest to requirements.txt**

Open `requirements.txt` and add at the end:
```
pytest
pytest-anyio
httpx
```

- [ ] **Step 5: Install new deps**

```bash
cd /Users/shreyasjena/slide-analyzer && pip install pytest httpx
```

Expected: installs without error.

- [ ] **Step 6: Run all tests**

```bash
cd /Users/shreyasjena/slide-analyzer && python -m pytest tests/ -v
```

Expected: `8 passed` (2 renderer + 3 analyzer + 3 main)

- [ ] **Step 7: Commit**

```bash
cd /Users/shreyasjena/slide-analyzer && git add main.py requirements.txt tests/test_main.py && git commit -m "feat: add FastAPI app with upload and analyze endpoint"
```

---

## Task 5: Smoke test — run the app against a real PDF

This is manual verification, not automated. Required before the demo.

- [ ] **Step 1: Set ANTHROPIC_API_KEY**

```bash
export ANTHROPIC_API_KEY=your_key_here
```

- [ ] **Step 2: Start the server**

```bash
cd /Users/shreyasjena/slide-analyzer && uvicorn main:app --reload
```

Expected: `Uvicorn running on http://127.0.0.1:8000`

- [ ] **Step 3: Open the upload form**

Navigate to `http://127.0.0.1:8000` in a browser. Verify the upload form appears.

- [ ] **Step 4: Upload a real PDF**

Use any PDF slide deck you have. Enter a realistic learning objective. Click Analyze.

Expected: browser downloads `report.html` after 10–60 seconds (depending on slide count).

- [ ] **Step 5: Open the downloaded report**

Open `report.html` in a browser. Verify:
- Header shows deck name, learning objective, violation count
- Each slide has a thumbnail (PNG embedded)
- Violations show principle, severity badge, finding, recommendation
- Passing principles show checkmarks

- [ ] **Step 6: Commit if any fixes were needed**

```bash
cd /Users/shreyasjena/slide-analyzer && git add -p && git commit -m "fix: smoke test corrections"
```

---

## Init git if needed

If the project isn't yet a git repo:

```bash
cd /Users/shreyasjena/slide-analyzer && git init && git add . && git commit -m "feat: initial slide analyzer scaffold"
```
