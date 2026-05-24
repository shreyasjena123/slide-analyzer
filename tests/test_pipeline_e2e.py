"""
End-to-end pipeline tests against 5 diverse fixture PPTX decks.

Tests are designed to be CI-runnable without an ANTHROPIC_API_KEY by using
mock mode (MOCK_PIPELINE=1). With a real key, they run against the live API.

Assertions per deck:
  1. parse:   no crash, returns list[SlideData]
  2. render:  produces one PNG (b64 string) per slide
  3. analyze: no crash, valid JSON structure per slide
  4. coverage: ≥ 80% of non-title slides have a valid analysis result
"""
from __future__ import annotations

import base64
import json
import os
import struct
import zlib
from pathlib import Path
from typing import List
from unittest.mock import MagicMock, patch

import pytest

from parser import SlideData, extract
from analyzer import analyze_deck

FIXTURES = Path(__file__).parent / "fixtures" / "decks"

DECKS = [
    (
        FIXTURES / "deck1_lecture_heavy.pptx",
        "Understand cell biology: membrane structure, transport, organelles, mitosis, enzyme activity.",
    ),
    (
        FIXTURES / "deck2_diagram_heavy.pptx",
        "Understand how photosynthesis converts light energy into chemical energy.",
    ),
    (
        FIXTURES / "deck3_sparse_titles.pptx",
        "Understand Mendelian genetics and patterns of inheritance.",
    ),
    (
        FIXTURES / "deck4_mixed_media.pptx",
        "Understand the evidence and mechanisms of climate change.",
    ),
    (
        FIXTURES / "deck5_unusual_formatting.pptx",
        "Understand data types, probability distributions, and hypothesis testing.",
    ),
]

MOCK_PIPELINE = os.environ.get("MOCK_PIPELINE", "0") == "1"
HAS_API_KEY = bool(os.environ.get("ANTHROPIC_API_KEY"))

VALID_PRINCIPLES = {
    "Coherence", "Signaling", "Spatial Contiguity", "Multimedia", "Redundancy",
    "Temporal Contiguity", "Pre-Training", "Modality",
}
VALID_SEVERITIES = {"high", "medium", "low"}

MOCK_RESULT = {
    "violations": [
        {
            "principle": "Multimedia",
            "severity": "medium",
            "finding": "Concept described in text without a supporting diagram.",
            "recommendation": "Add an instructive diagram.",
        }
    ],
    "passes": ["Coherence", "Signaling", "Spatial Contiguity", "Redundancy"],
}


def _blank_png_b64() -> str:
    """Minimal valid 1×1 PNG encoded as base64."""
    header = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
    ihdr_chunk = b"IHDR" + ihdr
    crc = zlib.crc32(ihdr_chunk) & 0xFFFFFFFF
    ihdr_full = struct.pack(">I", 13) + ihdr_chunk + struct.pack(">I", crc)
    raw = b"\x00" + bytes([100, 149, 200])
    compressed = zlib.compress(raw)
    idat_chunk = b"IDAT" + compressed
    crc2 = zlib.crc32(idat_chunk) & 0xFFFFFFFF
    idat_full = struct.pack(">I", len(compressed)) + idat_chunk + struct.pack(">I", crc2)
    iend_chunk = b"IEND"
    crc3 = zlib.crc32(iend_chunk) & 0xFFFFFFFF
    iend_full = struct.pack(">I", 0) + iend_chunk + struct.pack(">I", crc3)
    return base64.b64encode(header + ihdr_full + idat_full + iend_full).decode()


BLANK_PNG = _blank_png_b64()


def _mock_message(result: dict) -> MagicMock:
    msg = MagicMock()
    msg.content = [MagicMock(text=json.dumps(result))]
    return msg


def _run_pipeline(deck_path: Path, objective: str) -> tuple[List[SlideData], List[dict]]:
    """Parse → render (placeholder PNGs) → analyze. Returns (slides, results)."""
    slides = extract(str(deck_path))
    pngs = [BLANK_PNG] * len(slides)
    if MOCK_PIPELINE or not HAS_API_KEY:
        with patch("analyzer.client.messages.create", return_value=_mock_message(MOCK_RESULT)):
            results = analyze_deck(slides, pngs)
    else:
        results = analyze_deck(slides, pngs)
    return slides, results


def _assert_valid_result(result: dict, slide_num: int, deck_name: str) -> None:
    assert isinstance(result, dict), (
        f"{deck_name} slide {slide_num}: result is not a dict — got {type(result)}"
    )
    assert "violations" in result, (
        f"{deck_name} slide {slide_num}: missing 'violations' key — got {list(result.keys())}"
    )
    assert "passes" in result, (
        f"{deck_name} slide {slide_num}: missing 'passes' key — got {list(result.keys())}"
    )
    assert isinstance(result["violations"], list), (
        f"{deck_name} slide {slide_num}: 'violations' is not a list"
    )
    assert isinstance(result["passes"], list), (
        f"{deck_name} slide {slide_num}: 'passes' is not a list"
    )
    for v in result["violations"]:
        assert isinstance(v, dict), f"{deck_name} slide {slide_num}: violation is not a dict"
        assert "principle" in v, f"{deck_name} slide {slide_num}: violation missing 'principle'"
        assert "severity" in v, f"{deck_name} slide {slide_num}: violation missing 'severity'"
        assert "finding" in v, f"{deck_name} slide {slide_num}: violation missing 'finding'"
        assert "recommendation" in v, f"{deck_name} slide {slide_num}: violation missing 'recommendation'"
        assert v["principle"] in VALID_PRINCIPLES, (
            f"{deck_name} slide {slide_num}: unknown principle {v['principle']!r}"
        )
        assert v["severity"] in VALID_SEVERITIES, (
            f"{deck_name} slide {slide_num}: unknown severity {v['severity']!r}"
        )
    for p in result["passes"]:
        assert p in VALID_PRINCIPLES, (
            f"{deck_name} slide {slide_num}: unknown principle in passes: {p!r}"
        )


def _assert_coverage(slides: List[SlideData], results: List[dict], deck_name: str) -> None:
    n_content = sum(1 for s in slides if s.slide_type() == "content")
    if n_content == 0:
        return  # all-title deck — coverage check not applicable
    n_valid = sum(
        1
        for s, r in zip(slides, results)
        if s.slide_type() == "content"
        and isinstance(r, dict)
        and "violations" in r
        and "passes" in r
    )
    coverage = n_valid / n_content
    assert coverage >= 0.80, (
        f"{deck_name}: coverage {coverage:.0%} < 80% ({n_valid}/{n_content} content slides analyzed)"
    )


# ── parametrized tests ───────────────────────────────────────────────────────

@pytest.mark.parametrize("deck_path,objective", DECKS, ids=[d[0].stem for d in DECKS])
def test_parse_no_crash(deck_path, objective):
    """Parser must not crash and must return a non-empty list of SlideData."""
    slides = extract(str(deck_path))
    assert isinstance(slides, list)
    assert len(slides) > 0, f"{deck_path.name}: parsed 0 slides"
    for s in slides:
        assert isinstance(s, SlideData), f"Expected SlideData, got {type(s)}"
        assert isinstance(s.num, int)
        assert isinstance(s.body_text, str)
        assert isinstance(s.image_count, int)
        assert s.image_count >= 0


@pytest.mark.parametrize("deck_path,objective", DECKS, ids=[d[0].stem for d in DECKS])
def test_render_produces_one_png_per_slide(deck_path, objective):
    """One valid base64-encoded PNG per slide."""
    slides = extract(str(deck_path))
    pngs = [BLANK_PNG] * len(slides)
    assert len(pngs) == len(slides), "PNG count must match slide count"
    for i, png in enumerate(pngs):
        assert isinstance(png, str), f"Slide {i+1}: PNG is not a string"
        raw = base64.b64decode(png)
        assert raw[:4] == b"\x89PNG", f"Slide {i+1}: not a valid PNG header"


@pytest.mark.parametrize("deck_path,objective", DECKS, ids=[d[0].stem for d in DECKS])
def test_analyze_no_crash_valid_json(deck_path, objective):
    """Analyzer must not crash and must return valid JSON structure for every slide."""
    slides, results = _run_pipeline(deck_path, objective)
    assert len(results) == len(slides), (
        f"{deck_path.name}: result count {len(results)} != slide count {len(slides)}"
    )
    for s, r in zip(slides, results):
        _assert_valid_result(r, s.num, deck_path.name)


@pytest.mark.parametrize("deck_path,objective", DECKS, ids=[d[0].stem for d in DECKS])
def test_coverage_at_least_80_percent(deck_path, objective):
    """At least 80% of non-title slides must have a valid analysis result."""
    slides, results = _run_pipeline(deck_path, objective)
    _assert_coverage(slides, results, deck_path.name)


@pytest.mark.parametrize("deck_path,objective", DECKS, ids=[d[0].stem for d in DECKS])
def test_title_slides_skipped(deck_path, objective):
    """Title and transition slides must return empty violations list (not analyzed)."""
    slides, results = _run_pipeline(deck_path, objective)
    for s, r in zip(slides, results):
        if s.slide_type() in ("title/transition", "section/transition"):
            assert r.get("violations") == [], (
                f"{deck_path.name} slide {s.num} ({s.slide_type()!r}): "
                f"expected no violations but got {r.get('violations')}"
            )


@pytest.mark.parametrize("deck_path,objective", DECKS, ids=[d[0].stem for d in DECKS])
def test_result_count_matches_slide_count(deck_path, objective):
    """Result list length must equal slide list length."""
    slides, results = _run_pipeline(deck_path, objective)
    assert len(results) == len(slides)
