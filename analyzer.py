import asyncio
import json

from anthropic import AsyncAnthropic

from parser import SlideData
from principles import PRINCIPLES_TEXT

client = AsyncAnthropic()

_SYSTEM_PROMPT = [
    {
        "type": "text",
        "text": f"""You are an experienced instructional designer reviewing slides for a colleague. \
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
- TEMPORAL CONTIGUITY: Do NOT flag normal slide presentations. A presenter advancing slides while speaking already achieves temporal contiguity. Only flag if the entire narration is explicitly separated from all visuals as a large successive block.
- PRE-TRAINING: Do NOT flag for expert audiences. Only flag when (1) novice audience, AND (2) complex technical multi-component content, AND (3) no vocabulary introduction or component overview exists anywhere in the deck.
- MODALITY: Do NOT flag slides for having text on them. Do NOT flag slides for lacking audio narration — most slide decks have no audio. Only flag if there is an animation/video where dense captions replace narration in a fast-paced system-controlled lesson for native speakers with familiar vocabulary.
- SEVERITY: Only use "high" severity when a violation is clear, well-supported by Mayer's research, and would meaningfully hurt learning. Use "medium" or "low" when borderline or when boundary conditions might apply.

Respond ONLY with valid JSON — no prose, no markdown fences.""",
        "cache_control": {"type": "ephemeral"},
    }
]

_USER_TEMPLATE = """\
Slide metadata:
{metadata}

Analyze this slide against all 8 Mayer principles. Return ONLY valid JSON:
{{
  "violations": [
    {{
      "principle": "Coherence|Signaling|Spatial Contiguity|Multimedia|Redundancy|Temporal Contiguity|Pre-Training|Modality",
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
    "Multimedia":           ("high",   "d=1.35 across 13 studies"),
    "Coherence":            ("high",   "d=0.86 across 19 studies"),
    "Spatial Contiguity":   ("high",   "d=0.82 across 9 studies"),
    "Temporal Contiguity":  ("high",   "d=1.31 across 8 studies, large-block successive only"),
    "Modality":             ("high",   "d=1.00 across 19 studies, fast-paced system-controlled only"),
    "Pre-Training":         ("medium", "d=0.78 across 10 studies, novice learners + complex material"),
    "Redundancy":           ("medium", "d=0.72, applies to fast-paced narrated presentations"),
    "Signaling":            ("medium", "d=0.70 across 16 studies"),
}


def _enrich_violations(violations: list[dict]) -> list[dict]:
    """Add confidence and evidence fields to each violation based on principle."""
    enriched = []
    for v in violations:
        principle = v.get("principle", "")
        level, evidence = _PRINCIPLE_CONFIDENCE.get(principle, ("medium", ""))
        enriched.append({**v, "confidence": level, "evidence": evidence})
    return enriched


async def _analyze_slide_async(slide: SlideData, png_b64: str) -> dict:
    if slide.slide_type() in ("title/transition", "section/transition"):
        return {"violations": [], "passes": ["Coherence", "Signaling", "Spatial Contiguity", "Multimedia", "Redundancy", "Temporal Contiguity", "Pre-Training", "Modality"]}

    prompt = _USER_TEMPLATE.format(
        metadata=slide.to_prompt_text(),
    )
    response = await client.messages.create(
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
    text = response.content[0].text.strip()
    # Extract the outermost JSON object, discarding any prose the model appended.
    start = text.find("{")
    end = text.rfind("}") + 1
    result = json.loads(text[start:end])
    result["violations"] = _enrich_violations(result.get("violations", []))
    return result


async def _analyze_slide_with_delay(slide: SlideData, png: str, delay: float) -> dict:
    await asyncio.sleep(delay)
    return await _analyze_slide_async(slide, png)


async def analyze_deck(slides: list[SlideData], pngs: list[str]) -> list[dict]:
    # Stagger requests to avoid input token rate limits — the principles system
    # prompt is large (~8k tokens) and sending all slides simultaneously pushes
    # over the 50k input tokens/min limit for larger decks.
    return await asyncio.gather(*[
        _analyze_slide_with_delay(slide, png, i * 1.5)
        for i, (slide, png) in enumerate(zip(slides, pngs))
    ])
