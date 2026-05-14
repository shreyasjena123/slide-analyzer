import json

from anthropic import Anthropic

from parser import SlideData
from principles import PRINCIPLES_TEXT

client = Anthropic()

_SYSTEM_PROMPT = f"""You are an experienced instructional designer reviewing slides for a colleague. \
You know Mayer's Multimedia Learning Principles deeply — use the research below as your guide.

{PRINCIPLES_TEXT}

When reviewing, think like a practitioner giving real feedback, not an academic applying rules literally. \
Only flag something you would genuinely bring up in a feedback session — things where you'd say \
"this is actually hurting student learning." If a reasonable educator would look at it and say \
"that's fine, that's normal," don't flag it. When in doubt, leave it out.

Critical calibration rules to prevent false positives:
- SPATIAL CONTIGUITY: Only flag when a complex diagram has MULTIPLE SPECIFIC COMPONENTS described by text that is SEPARATED from those components with no labels connecting them. A single brief caption below an image describing the overall image is NOT a violation. A standard two-column layout is NOT a violation. Only flag when learners must visually search back and forth between a component legend and an unlabeled diagram.
- REDUNDANCY: Do NOT flag text on slides unless there is explicit evidence of simultaneous fast-paced audio narration. Text on a self-paced slide is not redundancy. Bullet points on lecture slides are not redundancy violations.
- MULTIMEDIA: Do NOT flag slides with simple definitions, factual statements, or single-concept claims. Only flag when a genuinely complex multi-step process or mechanism is described entirely in text with NO instructive diagram.
- SIGNALING: Do NOT flag slides that already have clear section headings, numbered steps, or organized bullet structure. These ARE good signaling. Only flag complex, dense, unstructured content where learners have no cues about what matters.
- SEVERITY: Only use "high" severity when a violation is clear, well-supported by Mayer's research, and would meaningfully hurt learning. Use "medium" or "low" when borderline or when boundary conditions might apply.

Respond ONLY with valid JSON — no prose, no markdown fences."""

_USER_TEMPLATE = """\
Deck context (use this to understand what the instructor is trying to teach, not to judge each slide against it individually): {objective}

Slide metadata:
{metadata}

Analyze this slide against all 5 Mayer principles. Return ONLY valid JSON:
{{
  "violations": [
    {{
      "principle": "Coherence|Signaling|Spatial Contiguity|Multimedia|Redundancy",
      "severity": "high|medium|low",
      "finding": "one sentence describing the specific issue on this slide",
      "recommendation": "one sentence fix",
      "why_it_matters": "one sentence grounded in Mayer's research — cite the specific cognitive mechanism or study finding that explains why this hurts learning (e.g. 'Mayer found extraneous material competes for limited working memory, reducing transfer test scores by d=0.86.')"
    }}
  ],
  "passes": ["principle names with no violations"]
}}"""


# Confidence levels grounded in Mayer's effect sizes and study conditions.
# High = strong, replicated effect under broad conditions (d ≥ 0.82).
# Medium = moderate effect or applies only under specific conditions (d 0.70–0.79).
_PRINCIPLE_CONFIDENCE = {
    "Multimedia":         ("high",   "d=1.35 across 13 studies"),
    "Coherence":          ("high",   "d=0.86 across 19 studies"),
    "Spatial Contiguity": ("high",   "d=0.82 across 9 studies"),
    "Redundancy":         ("medium", "d=0.72, applies to fast-paced narrated presentations"),
    "Signaling":          ("medium", "d=0.70 across 16 studies"),
}


def _enrich_violations(violations: list[dict]) -> list[dict]:
    """Add confidence and evidence fields to each violation based on principle."""
    enriched = []
    for v in violations:
        principle = v.get("principle", "")
        level, evidence = _PRINCIPLE_CONFIDENCE.get(principle, ("medium", ""))
        enriched.append({**v, "confidence": level, "evidence": evidence})
    return enriched


def analyze_slide(slide: SlideData, png_b64: str, learning_objective: str) -> dict:
    if slide.slide_type() in ("title/transition", "section/transition"):
        return {"violations": [], "passes": ["Coherence", "Signaling", "Spatial Contiguity", "Multimedia", "Redundancy"]}

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
    result = json.loads(text)
    result["violations"] = _enrich_violations(result.get("violations", []))
    return result


def analyze_deck(slides: list[SlideData], pngs: list[str], learning_objective: str) -> list[dict]:
    return [analyze_slide(slide, png, learning_objective) for slide, png in zip(slides, pngs)]
