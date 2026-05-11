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
