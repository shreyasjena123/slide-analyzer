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
