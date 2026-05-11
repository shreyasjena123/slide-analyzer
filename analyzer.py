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
    text = response.content[0].text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(text)


def analyze_deck(slides: list[SlideData], pngs: list[str], learning_objective: str) -> list[dict]:
    return [analyze_slide(slide, png, learning_objective) for slide, png in zip(slides, pngs)]
