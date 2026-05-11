# Slide Analyzer — Design Spec
Date: 2026-05-10

## Goal

Analyze PDF slide decks against Mayer's 5 Multimedia Learning Principles and return a self-contained HTML report with per-slide violations, findings, and recommendations.

Demo deadline: 7 days (to Professor Mayer himself).

## Scope

- **In:** PDF uploads only (PPTX excluded from MVP — user exports to PDF first)
- **In:** User-provided learning objective
- **In:** Per-slide analysis via Claude (one API call per slide)
- **In:** Downloadable self-contained HTML report
- **Out:** PPTX rendering, streaming UI, authentication, database, multi-user

## File Structure

```
slide-analyzer/
├── main.py            # FastAPI app — upload form + /analyze endpoint
├── renderer.py        # PDF pages → PNG via PyMuPDF at 150 DPI
├── analyzer.py        # Per-slide Claude API call, returns structured violations
├── parser.py          # Already done — extracts SlideData from PDF
├── principles.py      # Already done — loads Mayer chapter text
├── templates/
│   ├── index.html     # Upload form + learning objective field
│   └── report.html    # Jinja2 report template
└── static/
    └── style.css      # Report styling
```

## Data Flow

1. User submits PDF + learning objective via `POST /analyze`
2. `parser.py` extracts `SlideData` list (text, positions, image count, notes)
3. `renderer.py` renders each PDF page to PNG at 150 DPI using PyMuPDF
4. `analyzer.py` loops slides sequentially:
   - Sends PNG (as base64) + `SlideData.to_prompt_text()` + learning objective to Claude
   - Parses JSON response into violations list
5. Jinja2 renders `report.html` with all violations + base64 thumbnails
6. HTML file returned as download response

## Rendering

PDF → PNG via `fitz.Page.get_pixmap(matrix=fitz.Matrix(150/72, 150/72))`. No external dependencies. Same `fitz` import already used in `parser.py`.

## Claude API

**Model:** `claude-sonnet-4-6`
**Max tokens:** 1024 per slide
**System prompt:** Mayer principles text (from `principles.py`) + instruction to return JSON only

**Per-slide user message structure:**
```
Learning objective: <user input>

Slide metadata:
<SlideData.to_prompt_text()>

Analyze this slide against all 5 Mayer principles. Return ONLY valid JSON:
{
  "violations": [
    {
      "principle": "Coherence|Signaling|Spatial Contiguity|Multimedia|Redundancy",
      "severity": "high|medium|low",
      "finding": "one sentence describing the issue",
      "recommendation": "one sentence fix"
    }
  ],
  "passes": ["principle names that are satisfied"]
}
```

Image attached as base64 PNG in the message content block.

## Report Format

Single self-contained HTML file (inline CSS, thumbnails as base64 data URIs).

Structure:
- Header: deck name, learning objective, total violation count
- One section per slide:
  - Slide thumbnail (base64 PNG)
  - Violations list: severity badge + finding + recommendation
  - Passes list: principles with no violations

## Principles Reference

| Principle | Effect Size | What to flag |
|---|---|---|
| Coherence | d=0.86 | Extraneous images, decorative elements, irrelevant text |
| Signaling | d=0.70 | Missing headings, no emphasis on key terms, no visual cues |
| Spatial Contiguity | d=0.82 | Text and corresponding graphics on opposite sides |
| Multimedia | d=1.35 | Concept explained only in words with no visual support |
| Redundancy | d=0.72 | Identical content in slide text AND speaker notes |

## Dependencies

All already in `requirements.txt`. No new dependencies needed — PyMuPDF handles both parsing and rendering.

## Known Constraints

- Synchronous endpoint: large decks (30+ slides) will have a long HTTP timeout. Acceptable for demo.
- `principles.py` chapter paths are hardcoded to local filesystem — must be present at runtime.
- PDF-only: user must export PPTX to PDF before uploading.
