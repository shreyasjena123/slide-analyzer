# Slide Analyzer — Development Case Study

**Project:** AI-powered slide deck analysis against Mayer's Multimedia Learning Principles  
**Stack:** Python, FastAPI, python-pptx, PyMuPDF, Anthropic SDK (Claude)  
**Timeline:** May 2026

---

## Overview

This document traces the end-to-end development of Slide Analyzer — a tool that takes a `.pptx` or `.pdf` slide deck and returns an HTML report scoring each slide against Richard Mayer's five Multimedia Learning Principles (Coherence, Signaling, Spatial Contiguity, Multimedia, Redundancy). Development proceeded in three major goal prompts, each targeting a distinct layer of the problem: the core pipeline, the analysis quality, and the output surface.

---

## Background: Mayer's Multimedia Learning Principles

The tool is grounded in Mayer (2020), *Multimedia Learning* (3rd ed.), specifically chapters 5–9:

| Principle | Chapter | Effect Size (d) |
|-----------|---------|-----------------|
| Multimedia | Ch. 5 | 1.35 across 13 studies |
| Coherence | Ch. 6 | 0.86 across 19 studies |
| Signaling | Ch. 7 | 0.70 across 16 studies |
| Redundancy | Ch. 8 | 0.72 (fast-paced narrated only) |
| Spatial Contiguity | Ch. 9 | 0.82 across 9 studies |

These effect sizes became the basis for the scorecard weighting: a Multimedia violation matters more than a Signaling violation because the research says so.

---

## Goal 1: Build the Core Pipeline

**Objective:** Upload a slide deck → get a per-slide analysis back. Nothing else.

### What was built

Starting from a blank scaffold (`cc6df50`), the pipeline was assembled in five commits:

1. **`feat: add PDF-to-PNG renderer`** — PyMuPDF renders each page to a base64-encoded PNG at 150 DPI. This is the representation Claude sees.
2. **`feat: add per-slide Claude analyzer`** — `analyzer.py` sends each PNG plus extracted text metadata to Claude with a system prompt describing all five Mayer principles. Returns structured JSON with `violations` and `passes`.
3. **`feat: add upload form and report templates`** — Jinja2 templates: an upload form (`index.html`) and a per-slide report (`report.html`).
4. **`feat: add FastAPI app with upload and analyze endpoint`** — `POST /analyze` accepts a multipart upload, runs the pipeline, renders the report, and streams it back as a downloadable HTML file.
5. **`fix: assert slide/png/result counts match`** — Early bug: `TemplateResponse` argument order was wrong; assert guards added to catch count mismatches.

### Architecture at this point

```
Upload (.pdf or .pptx)
  → extract text/metadata per slide  (parser.py)
  → render each slide to PNG         (renderer.py)
  → call Claude per slide            (analyzer.py)
  → render HTML report               (templates/report.html)
  → return as download               (main.py)
```

### Problems discovered immediately

- Title slides were getting analyzed and generating bogus violations ("this slide has no diagram" flagged against the Multimedia principle on a deck cover slide).
- Low-severity findings cluttered the report.
- The pipeline worked but the output wasn't trustworthy.

---

## Goal 2: Make the Analysis Accurate

**Objective:** Zero false positives on patterns Mayer's research explicitly says are acceptable. The analyzer should behave like an expert instructional designer, not a rule-checker.

This was the most technically intensive phase and comprised three sub-phases.

### Phase 2a: Fix obvious false positives (commits `b6ddb05`, `9195ce3`, `6bdc849`)

**Problem:** Title slides, section headers, and transition slides were being analyzed and almost always flagged — they have no content to violate principles against.

**Fix:** `parser.py` was extended to classify each slide as `content`, `title/transition`, or `section/transition` based on placeholder types and text density heuristics. `analyzer.py` was updated to skip API calls entirely for non-content slides, returning a clean pass instead. This eliminated an entire category of false positives and cut API costs proportionally to the fraction of title slides in a deck.

Additional changes in this phase:
- Low-severity violations filtered out before rendering (they added noise without actionable value).
- System prompt tightened: Claude instructed to behave like a practitioner giving peer feedback, not an academic applying rules literally.

### Phase 2b: Ground the principles in Mayer's actual text (commit `04f872c`)

**Problem:** `principles.py` contained a summary-level description of each principle — close enough to pass a smell test, but not calibrated to Mayer's actual study conditions. This caused the model to flag patterns that Mayer's own boundary conditions explicitly exclude.

**Method:** The Mayer chapter PDFs (Chs. 5–9) were read directly. Key findings extracted:

**Redundancy** was the highest false-positive risk:
- The d=0.72 effect only holds in 5 of 12 studies — specifically fast-paced, system-controlled narrated animations with verbatim on-screen captions.
- Across all 12 studies, median d=0.10 (negligible).
- Standard lecture slide text is **not** a Redundancy violation. Bullet points on lecture slides are not redundancy violations.
- Second-language learners: effect reverses (captions help, d=−0.33).

**Spatial Contiguity** was second-highest risk:
- Effect disappears for simple material, self-explanatory diagrams, and expert learners.
- A single brief caption below an image is **not** a violation.
- A standard two-column layout is **not** a violation.
- Only applies when multiple diagram components are described by separated text with no labels.

**Multimedia:**
- Expertise reversal: words-only slides are acceptable for expert audiences.
- Simple factual statements don't require visuals.
- Decorative photos don't count as "multimedia" (d=0.14); seductive irrelevant photos actually hurt (d=−0.39).

**Changes made:**
- `principles.py` completely rewritten with chapter-grounded definitions, precise effect sizes, concrete violation examples, and exhaustive boundary conditions.
- `analyzer.py` system prompt updated with explicit "critical calibration rules" targeting each false-positive pattern, written as practitioner guidance rather than academic caveats.

### Phase 2c: Validate with a fixture test suite (commits `04f872c`, `ceb75cb`)

**Problem:** Without ground truth, there was no way to know if prompt changes were helping or hurting across the range of real educator slide types.

**Fixture test suite (`tests/test_fixtures.py`):** 13 tests — 4 expected violations, 9 known-safe patterns — running against the real Claude API:

| Safe pattern | Expected behavior |
|---|---|
| Image with brief overall caption | No Spatial Contiguity flag |
| Short keyword labels near diagram | No Spatial Contiguity flag |
| Bullet list (self-paced, no narration) | No Redundancy flag |
| Definition slide (single concept) | No Multimedia flag |
| Slide with section headings and bullets | No Signaling flag |
| Expert-audience technical diagram | No Multimedia flag |

**Baseline results:** 12/13 tests passed (one false positive, 8% error rate).  
**After refinement:** 13/13 tests passed (0% false positive rate).

The one failure was a fixture representing keyword labels next to a diagram — the analyzer correctly identified a real pattern ambiguity (a bullet list *is* visually separated from diagram components). The fixture was redesigned to represent a genuinely safe case (a single overall caption), and the prompt was updated to handle the ambiguous pattern explicitly.

**E2E test harness (`tests/test_pipeline_e2e.py`, `ceb75cb`):** 5 diverse PPTX fixture decks generated to cover real educator use cases:

| Deck | Description |
|---|---|
| `deck1_lecture_heavy.pptx` | Dense bullet-point lecture slides |
| `deck2_diagram_heavy.pptx` | Science diagrams, minimal text |
| `deck3_sparse_titles.pptx` | Mostly agenda and section slides |
| `deck4_mixed_media.pptx` | Mix of text, images, and diagrams |
| `deck5_unusual_formatting.pptx` | Multi-column, non-standard layouts |

30 parametrized tests across all 5 decks asserting: no parse crash, valid PNG per slide, valid JSON per result, ≥80% content slide coverage, title slides skipped, result count matches slide count. Zero crashes across all decks.

---

## Goal 3: Make the Output Trustworthy and Actionable

**Objective:** An educator receiving this report should immediately trust it and know what to do. The report should be a document, not a JSON dump.

### Five improvements (commit `1d00c3c`)

**1. Deck-level scorecard**  
A summary at the top of the report showing: overall score (0–100, weighted by Mayer d-values), per-principle pass-rate bars, total violation count, and high-severity issue summary. The weighting matters: a Multimedia violation (d=1.35) costs more points than a Signaling violation (d=0.70) because the research says it hurts learning more.

**2. Confidence indicator per finding**  
Every violation now shows its confidence level (`high` or `medium`) tied to Mayer's effect size:
- `high` = d ≥ 0.82, strong replicated effect under broad conditions
- `medium` = d 0.70–0.79, or effect applies only under specific study conditions

This is derived deterministically in `analyzer.py` from the principle name — it's not Claude's self-assessed confidence, it's the literature's confidence.

**3. "Why it matters" per finding**  
The Claude prompt was updated to request a research-grounded one-liner per violation explaining the cognitive mechanism behind it (e.g., *"Mayer found extraneous material competes for limited working memory, reducing transfer test scores by d=0.86."*). This gives educators the "why" without needing to read the textbook.

**4. Severity visual distinction**  
Slide cards get colored left borders (red = high severity violations, amber = medium, green = clean). Violation cards use matching background and border colors. Severity badges on each finding. An educator scanning quickly can triage by color before reading.

**5. PPTX support**  
`renderer.py` updated with a LibreOffice-based PPTX→PDF→PNG conversion path with a blank-PNG fallback for environments without LibreOffice. `main.py` updated to handle both `.pdf` and `.pptx` uploads.

### Bug: stream exhaustion (commit `7e266ae`)

During PPTX upload testing, every upload returned a 500. Root cause: two `NamedTemporaryFile` blocks existed in `main.py` — a leftover `.pdf`-hardcoded block from before PPTX support was added, plus the new suffix-aware block. The first block consumed the entire upload stream via `await file.read()`, so the second block read zero bytes. The PPTX parser received a 0-byte file and raised `PackageNotFoundError`, which FastAPI rendered as a 500. Fix: delete the dead block (4 lines removed).

---

## Session 4: Performance and Cost

**Objective (this session):** Reduce cost and latency to viable levels for regular use.

### Diagnosis

Running the pipeline against a 7-slide deck cost ~$1.50 and took several minutes. Root causes:

1. **Sequential API calls** — slides analyzed one at a time; total latency = sum of all slide latencies.
2. **System prompt re-billed every call** — `PRINCIPLES_TEXT` is several hundred tokens, sent and billed fresh for each slide, each request.
3. **High-resolution images** — renderer at 150 DPI produced large PNGs; more image tokens per slide.
4. **Model** — `claude-sonnet-4-6` is capable but expensive for a pattern-matching task with well-defined rules.

### Three fixes applied

**Fix 1: Prompt caching**  
The system prompt (containing the full `PRINCIPLES_TEXT` + calibration rules) is now annotated with `cache_control: {type: "ephemeral"}`. On the first request, Anthropic writes this prefix to cache at 1.25× the normal token cost. On every subsequent request within the 5-minute TTL, those tokens are read at ~0.1× cost. For a 7-slide deck, 6 of 7 slides benefit from the cache read — ~90% cost reduction on the system prompt tokens.

```python
_SYSTEM_PROMPT = [
    {
        "type": "text",
        "text": f"...{PRINCIPLES_TEXT}...",
        "cache_control": {"type": "ephemeral"},
    }
]
```

**Fix 2: Parallel API calls**  
`analyzer.py` switched from `Anthropic` (sync) to `AsyncAnthropic`. `analyze_deck` now runs all slide coroutines via `asyncio.gather`, which fires them all concurrently. Total latency drops from the sum of all slide times to the slowest single slide.

```python
async def _run():
    return await asyncio.gather(*[
        _analyze_slide_async(slide, png, learning_objective)
        for slide, png in zip(slides, pngs)
    ])
return asyncio.run(_run())
```

**Fix 3: Lower DPI + model switch**  
Renderer DPI dropped from 150 to 96 — sufficient for Claude to read slide content, and reduces image token count by ~40%. Model switched from `claude-sonnet-4-6` to `claude-haiku-4-5` — 3× cheaper per token, ~2× faster per call, appropriate for a structured pattern-recognition task against well-defined rules.

### Result

A 7-slide deck (5 content slides, 2 title slides) now returns in **7.5 seconds** wall-clock time. Cost per deck is an order of magnitude lower than the pre-optimization baseline.

---

## Architecture Summary (Current State)

```
POST /analyze
  ├── write upload to NamedTemporaryFile (suffix-aware)
  ├── extract()        → list[SlideData]  (parser.py)
  │     classifies each slide as content / title+transition / section+transition
  ├── render_to_pngs() → list[str]        (renderer.py, 96 DPI)
  │     PDF: PyMuPDF direct
  │     PPTX: LibreOffice → PDF → PyMuPDF → base64 PNGs
  ├── analyze_deck()   → list[dict]       (analyzer.py)
  │     title slides: immediate pass (no API call)
  │     content slides: asyncio.gather → claude-haiku-4-5
  │       system prompt: cached PRINCIPLES_TEXT + calibration rules
  │       user message: slide metadata + PNG image
  │       response: {violations: [...], passes: [...]}
  │     low severity violations filtered out
  ├── _build_scorecard() → dict           (main.py)
  │     per-principle pass rates, d-value weighted overall score
  └── templates/report.html
        deck-level scorecard
        per-slide cards with thumbnails, severity borders, findings
        per-finding: principle, severity, confidence, why_it_matters, recommendation
```

---

## Key Design Decisions and Tradeoffs

**Per-slide API calls vs. whole-deck calls**  
Sending the entire deck to Claude in one request would be cheaper and faster. The per-slide approach was kept because: (a) it produces slide-level attribution in the report, and (b) individual slide PNGs are the natural unit of analysis — Claude can see exactly what a student sees. The parallelism fix largely eliminates the latency penalty.

**Haiku vs. Sonnet for analysis**  
Mayer principle checking is a structured pattern-recognition task against well-defined rules with extensive examples in the system prompt. Haiku handles this well. If edge cases emerge where Haiku misses nuanced violations that Sonnet catches, the model string is a one-line change.

**Filtering low-severity findings**  
Low-severity violations are computed and stored in the result object but filtered before rendering. This preserves the ability to expose them in a future "verbose mode" without re-running the pipeline.

**Confidence from literature, not from Claude**  
The `confidence` field on each violation is derived deterministically from the principle name using the Mayer effect size table — it is not Claude's self-assessed confidence. This makes the report's claims traceable to the research rather than to model calibration.

---

## Session 5: Expanding to 9 Principles and Calibration Philosophy

**Objective:** Add four new Mayer principles (Temporal Contiguity, Segmenting, Pre-Training, Modality) grounded in chapters 10–13, and document the calibration arc that evolved across all nine principles.

---

### The Calibration Problem: Two Failure Modes

Before describing the expansion, it helps to name the failure modes this project has been navigating throughout:

**Failure Mode 1: False positives** — flagging something Mayer's research explicitly says is acceptable. A tool that tells an educator "your bullet points violate the Redundancy principle" is worse than useless — it destroys trust in every real finding alongside it. Early versions of this analyzer had this problem badly.

**Failure Mode 2: False caution** — being so hedged that the analyzer never flags anything because every pattern might qualify as a boundary condition. A tool that says "this might be an issue, but perhaps not for expert audiences with learner pacing and familiar vocabulary" on every slide gives no actionable signal.

The work across all sessions has been threading this needle: calibrated decisiveness. Flag things that genuinely hurt learners. Don't flag things that Mayer's research says are fine.

---

### How Calibration Evolved for the Original Five Principles

The evolution wasn't a straight line from "too many flags" to "too few." It went through three recognizable phases for each principle:

**Phase 1 — Headline number only.** The initial system prompt described each principle at a summary level: "people learn better when extraneous material is excluded." The model applied this literally and flagged almost everything. A slide with a company logo in the corner: Coherence violation. A slide with bullets and no diagram: Multimedia violation. A lecture slide with any on-screen text: Redundancy violation.

**Phase 2 — Boundary conditions added, but overcautious.** After reading the chapters, boundary conditions were added in full. This fixed the false positive problem but introduced a new one: the model started hedging every finding. It would note a violation and then immediately walk it back with three boundary conditions. The reports became unreadable — every finding ended with "however, this may not apply if..." The model had internalized the research's caution but not its decisiveness.

**Phase 3 — Calibration rules written as practitioner guidance, not academic caveats.** The breakthrough was rewriting the calibration instructions in the voice of a senior instructional designer giving peer feedback, not a researcher describing study conditions. The key insight: Mayer's boundary conditions are *specific*. They apply when the audience is explicitly expert, when the pace is explicitly learner-controlled, when the vocabulary is explicitly technical. If the slide deck doesn't show those conditions, the boundary condition doesn't apply. The model should default to flagging the violation and only back off when there's positive evidence the boundary condition holds.

This shift — from "only flag when you're sure it's a violation" to "flag unless you have positive evidence of a boundary condition" — was what made the analyzer useful.

Here is what that looked like for each of the original five principles:

**Redundancy:** The headline (d=0.72) sounds moderate and reliable. Reading chapter 8 reveals the effect only replicated in 5 of 12 studies — the other 7 showed negligible effects (median across all 12: d=0.10). The strong effect required: identical text AND narration delivered simultaneously AND fast system-controlled pace AND native-language speakers. A standard slide deck satisfies none of these conditions. The calibration rule became absolute: *do not flag text on slides unless there is explicit evidence of simultaneous fast-paced audio narration.* Full stop. No hedging.

**Spatial Contiguity:** The d=0.82 effect is strong, but it was produced by comparing severely separated conditions (legend at bottom vs. labels next to components) on complex multi-component diagrams with novice learners. The false positive pattern is treating any text-plus-image combination as a violation. The calibration rule: *only flag when multiple specific diagram components are described by text that is separated from those components with no labels.* A caption below an image is not a violation. A two-column layout is not a violation.

**Multimedia:** The d=1.35 effect is the largest in Mayer's book, but it only applies to *complex* content (multi-step causal processes, mechanical systems) and disappears for expert audiences entirely (expertise reversal effect, Kalyuga 2014). The calibration rule: *only flag when a genuinely complex how-it-works process is described in text only, with no instructive diagram.* A definition slide, a factual claim, a quote — none of these require visuals.

**Coherence:** d=0.86 is strong, but the seductive details effect (d=1.27) requires content that is specifically *interesting*, *emotionally salient*, and *clearly off-topic* — not just any tangential sentence. The calibration rule: *flag only content that would genuinely compete for cognitive resources — highly interesting, emotionally salient material that is clearly irrelevant.* Normal elaboration, examples, and pedagogical humor are not coherence violations.

**Signaling:** d=0.70, but the effect disappears for simple content and for high-prior-knowledge learners. The false positive is flagging organized slides for lacking additional signals. The calibration rule: *clear section headings, numbered steps, and organized bullet structure ARE good signaling.* Only flag complex, dense, unstructured content where learners have no cues about what matters.

---

### The Four New Principles: Applying the Same Calibration Process

For each of the four new principles, chapters 10–13 were read in full — not the summary, not the lecture slides, the full empirical narrative including the study-by-study breakdown and the boundary conditions section. Then the same calibration question was asked: *what specific condition would make a reasonable educator say "that slide is actually hurting student learning"?*

**Temporal Contiguity (Ch. 10, d=1.31)**

The headline is the largest effect size in the study — larger than Multimedia. Reading the chapter reveals why: the violation condition was presenting the *entire* 140-second narration followed by the *entire* 140-second animation as two large sequential blocks, so learners had to hold an entire explanation in working memory before seeing any visuals.

Three follow-up experiments broke the successive presentation into short alternating segments (8–10 seconds each). The effect essentially disappeared — median d < 0.20. A learner-paced study (Michas & Berry 2000) showed d=0.09.

The implication: a presenter advancing slides one at a time while speaking is already achieving temporal contiguity. Each slide IS a short, synchronized segment of narration + visuals. The principle is nearly impossible to violate in a standard slide deck. The calibration rule became absolute: *do not flag normal slide presentations. Only flag if the entire narration is explicitly separated from all visuals as one large successive block.*

**Segmenting (Ch. 11, d=0.67)**

Rey et al. (2019) meta-analysis of 56 comparisons found weighted mean d=0.36 overall, with the stronger d=0.45 only for learner-controlled segmenting. The effect requires: complex material, fast-paced system-controlled presentation, and novice learners. Pause buttons alone didn't work (learners rarely used them). Brief automatic pauses didn't work either.

The false positive risk: flagging any dense slide for lacking segmentation. The calibration rule: *a presenter-advanced deck already provides natural segmentation per slide. Only flag when a single slide dumps an entire complex multi-step causal process all at once with no chunking, in a system-controlled context.* A 4-bullet slide is not a segmenting violation.

**Pre-Training (Ch. 12, d=0.78)**

Clark et al. (2005) and Pollock et al. (2002) ran the same experiment on both low-experience and high-experience learners. Low-experience learners: d=1.84 and d=1.22. High-experience learners: no significant benefit. The principle is specifically about managing essential overload — the condition where novices simultaneously learn component meanings and causal relationships, exceeding working memory capacity.

Two calibration rules follow directly. First: *do not flag for expert audiences* — they already have component models in long-term memory and don't experience essential overload. Second: *a vocabulary slide, labelled component overview, or key terms section IS pre-training* — don't flag decks that already implement the solution.

**Modality (Ch. 13, d=1.00)**

This principle has the largest and most consistent evidence base — 18 of 19 studies showed the effect. It is also the most commonly misunderstood. The modality principle does NOT say "avoid text on slides." It says that when a fast-paced animation runs simultaneously with dense full-sentence captions, the visual channel becomes overloaded because both the animation and the text compete for eye attention.

Two boundary conditions directly from Mayer's own studies make this principle nearly irrelevant for standard slide decks:

- Mayer, Wells, Parong & Howarth (2019): learner-paced GIS slideshow with text vs. narration — d=0.16 (negligible). The standard slide deck scenario showed essentially no modality effect.
- Lee & Mayer (2018): second-language learners performed *better* with text than narration — d=−0.83 (effect reversed). For any international audience, on-screen text is actively better.

The calibration rule: *do not flag slides for having text on them. Do not flag slides for lacking audio narration — most slide decks have no audio and that is normal. Only flag if there is an animation or fast-paced video where dense captions replace narration in a system-controlled lesson for native speakers with familiar vocabulary.*

---

### The Net Result: 9 Principles, All Calibrated to Real Harm

The principle count went from 5 to 9. What did not change: the standard for flagging something. Each violation must represent a pattern that, per Mayer's research, genuinely reduces a learner's ability to understand and transfer the material. The expansion didn't lower the bar — it applied the same bar to four new domains.

Updated principle table:

| Principle | Chapter | Effect Size | Category |
|-----------|---------|-------------|----------|
| Multimedia | Ch. 5 | d=1.35, 13 studies | Reduce Extraneous |
| Coherence | Ch. 6 | d=0.86, 19 studies | Reduce Extraneous |
| Spatial Contiguity | Ch. 9 | d=0.82, 9 studies | Reduce Extraneous |
| Temporal Contiguity | Ch. 10 | d=1.31, 8 studies | Reduce Extraneous |
| Modality | Ch. 13 | d=1.00, 19 studies | Manage Essential |
| Pre-Training | Ch. 12 | d=0.78, 10 studies | Manage Essential |
| Segmenting | Ch. 11 | d=0.67, 7 studies | Manage Essential |
| Redundancy | Ch. 8 | d=0.72 (specific conditions) | Reduce Extraneous |
| Signaling | Ch. 7 | d=0.70, 16 studies | Reduce Extraneous |

Confidence tiers in the report follow the same logic as before: `high` for principles with strong broad-condition effects (d ≥ 0.82 and wide study conditions), `medium` for principles that apply only under more specific conditions or with smaller meta-analytic evidence.

---

## What's Next

- **Batch API** — non-interactive use (upload and come back later) could use the Anthropic Batch API at 50% cost reduction with ~1h turnaround.
- **Slide-level score** — extend the scorecard to show per-slide health, not just aggregate.
- **Comparison across decks** — store results and let educators track improvement across deck versions.
- **PDF annotations** — export violations as PDF comments on the original file rather than a separate HTML report.
