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
