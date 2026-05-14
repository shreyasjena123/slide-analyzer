import base64
import struct
import zlib

import fitz


def render_pdf_to_pngs(path: str, dpi: int = 150) -> list[str]:
    """Render each PDF page to a base64-encoded PNG string."""
    doc = fitz.open(path)
    matrix = fitz.Matrix(dpi / 72, dpi / 72)
    return [
        base64.b64encode(page.get_pixmap(matrix=matrix).tobytes("png")).decode()
        for page in doc
    ]


def render_pptx_to_pngs(path: str, dpi: int = 150) -> list[str]:
    """Render each PPTX slide to a base64-encoded PNG by converting via an in-memory PDF."""
    import subprocess, tempfile, os, sys

    # Try LibreOffice headless conversion (most reliable)
    for soffice in ("soffice", "libreoffice", "/Applications/LibreOffice.app/Contents/MacOS/soffice"):
        try:
            with tempfile.TemporaryDirectory() as tmp:
                result = subprocess.run(
                    [soffice, "--headless", "--convert-to", "pdf", "--outdir", tmp, path],
                    capture_output=True, timeout=60,
                )
                pdf_name = os.path.splitext(os.path.basename(path))[0] + ".pdf"
                pdf_path = os.path.join(tmp, pdf_name)
                if result.returncode == 0 and os.path.exists(pdf_path):
                    return render_pdf_to_pngs(pdf_path, dpi=dpi)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue

    # Fallback: return blank placeholder PNGs (one per slide)
    from pptx import Presentation
    prs = Presentation(path)
    n = len(prs.slides)
    return [_blank_png_b64() for _ in range(n)]


def _blank_png_b64() -> str:
    """Minimal valid 1×1 grey PNG encoded as base64."""
    header = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
    ihdr_chunk = b"IHDR" + ihdr
    crc = zlib.crc32(ihdr_chunk) & 0xFFFFFFFF
    ihdr_full = struct.pack(">I", 13) + ihdr_chunk + struct.pack(">I", crc)
    raw = b"\x00" + bytes([180, 180, 180])
    compressed = zlib.compress(raw)
    idat_chunk = b"IDAT" + compressed
    crc2 = zlib.crc32(idat_chunk) & 0xFFFFFFFF
    idat_full = struct.pack(">I", len(compressed)) + idat_chunk + struct.pack(">I", crc2)
    iend_chunk = b"IEND"
    crc3 = zlib.crc32(iend_chunk) & 0xFFFFFFFF
    iend_full = struct.pack(">I", 0) + iend_chunk + struct.pack(">I", crc3)
    return base64.b64encode(header + ihdr_full + idat_full + iend_full).decode()


def render_to_pngs(path: str, dpi: int = 150) -> list[str]:
    """Dispatch to the right renderer based on file extension."""
    from pathlib import Path
    suffix = Path(path).suffix.lower()
    if suffix == ".pdf":
        return render_pdf_to_pngs(path, dpi=dpi)
    elif suffix == ".pptx":
        return render_pptx_to_pngs(path, dpi=dpi)
    else:
        raise ValueError(f"Unsupported file type for rendering: {suffix}")
