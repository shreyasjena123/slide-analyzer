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
