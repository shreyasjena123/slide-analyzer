# Slide Analyzer — Product Case Study

**Product:** An AI-powered slide deck reviewer that scores each slide against Richard Mayer's Multimedia Learning Principles and returns an actionable HTML report.
**Built for:** Educators, instructional designers, and corporate L&D teams reviewing their own decks before delivery.
**Timeline:** May 2026

---

## The Product

Slide Analyzer takes a `.pptx` or `.pdf` upload and returns a report scoring each slide against nine cognitive-science principles for effective instructional design. The output gives the user three things they didn't have before: a deck-level score, per-slide findings with severity and confidence, and a research-grounded "why this matters" for every flagged issue.

The competitive frame: generic AI design feedback (Copilot, Designer) optimizes for visual polish. Human expert reviews cost $200+ per deck and take days. Self-review with no framework — what most educators do today — produces decks built on instinct rather than evidence. Slide Analyzer occupies the gap: research-grounded feedback, in minutes, for the cost of a few API calls.

## Why This Exists

The underlying insight is a trust problem. AI tools that critique slide decks today rely on opaque heuristics — "your slide has too much text" without an answer to *says who, and by how much*. Educators ignore that feedback because they can't tell good critique from confident-sounding noise.

Mayer's *Multimedia Learning* (3rd ed., 2020) is the credible standard. Each principle has a measured effect size on transfer learning (Cohen's d), replicated across dozens of studies. A tool that grounds every finding in that literature — with the effect size visible to the user — is a fundamentally different kind of feedback than generic AI critique. That's the product wedge.

| Principle | Chapter | Effect Size (d) | Category |
|-----------|---------|-----------------|----------|
| Multimedia | Ch. 5 | 1.35 | Reduce Extraneous |
| Coherence | Ch. 6 | 0.86 | Reduce Extraneous |
| Signaling | Ch. 7 | 0.70 | Reduce Extraneous |
| Redundancy | Ch. 8 | 0.72 (conditional) | Reduce Extraneous |
| Spatial Contiguity | Ch. 9 | 0.82 | Reduce Extraneous |
| Temporal Contiguity | Ch. 10 | 1.31 | Reduce Extraneous |
| Segmenting | Ch. 11 | 0.67 | Manage Essential |
| Pre-Training | Ch. 12 | 0.78 | Manage Essential |
| Modality | Ch. 13 | 1.00 | Manage Essential |

---

## v0.1 — Prove the Loop Works

**Goal:** Validate that the core mechanic (upload → per-slide AI analysis → readable report) was technically feasible before investing in calibration or output quality.

**What shipped:** Five-component pipeline — PDF/PPTX parser, page-to-PNG renderer (PyMuPDF at 150 DPI), per-slide Claude analyzer, Jinja2 report templates, FastAPI upload endpoint. End-to-end working in ~5 commits.

**What I learned:** The pipeline worked. The output didn't. Title slides got analyzed and generated nonsense ("this slide has no diagram" against a cover page). Low-severity findings cluttered the report. The mechanic was right; the product wasn't trustworthy yet. That diagnosis became the v0.2 brief.

## v0.2 — Earn the User's Trust

**Goal:** Zero false positives on patterns Mayer's research explicitly says are acceptable. The product cannot tell users "your bullet points are wrong" when Mayer's own work says they aren't — that single false flag destroys credibility for every real finding around it.

This was the most important product phase. It happened in three sub-phases.

**Phase 2a — Eliminate the obvious noise.** The parser was extended to classify each slide as `content`, `title/transition`, or `section/transition` based on placeholder types and text density. Non-content slides skip the AI call entirely and return a clean pass. This cut API costs proportionally to the title-slide fraction of a deck — typically 15-25%. Low-severity violations were filtered before rendering: they added cognitive load to the user without changing any decision they'd make.

**Phase 2b — Ground the analysis in primary sources.** The principle definitions were rewritten directly from Mayer's chapters, not summaries. This exposed how brittle the original definitions were:

- **Redundancy** turned out to apply only in 5 of 12 studies — specifically fast-paced, system-controlled narrated animations with verbatim captions, for native speakers. Median across all 12 studies: d=0.10. Standard lecture slides are not a redundancy violation. The original prompt was flagging them anyway. For second-language learners the effect reverses (d=-0.33).
- **Spatial Contiguity** disappears for simple material, self-explanatory diagrams, and expert audiences. A caption below an image is not a violation. The original prompt flagged them anyway.
- **Multimedia** is subject to expertise reversal — words-only slides are acceptable for expert audiences. Decorative photos don't help (d=0.14); seductive irrelevant photos actively hurt (d=-0.39). The original prompt didn't distinguish.

Each of these was a class of false positive that would have shipped to users and destroyed trust. The fix was rewriting the system prompt with explicit calibration rules — written as practitioner peer feedback, not academic caveats.

**Phase 2c — Validate against fixtures before users.** 13 fixture tests (4 expected violations + 9 known-safe patterns) ran against the real API. Baseline: 12/13 (one false positive, 8% error rate). After refinement: 13/13. An additional 30 parametrized E2E tests across 5 diverse decks (lecture-heavy, diagram-heavy, sparse, mixed, unusual formatting) verified zero crashes and ≥80% content-slide coverage. This was the product's quality bar before any user would touch it.

## v0.3 — Make the Output Usable

**Goal:** An educator opening this report should immediately trust it and know what to do next.

**What shipped:**

- **Deck-level scorecard.** A summary at the top: overall score 0-100, per-principle pass rates, total violations, high-severity issues. The score is weighted by Cohen's d — a Multimedia violation (d=1.35) costs more than a Signaling violation (d=0.70). This is a small detail with a large effect: the score answers "how bad is my deck" before the user reads a single finding.
- **Confidence per finding, derived from literature.** Every violation shows `high` or `medium` confidence tied to Mayer's effect size — not Claude's self-assessment. This was a deliberate trust decision. Self-rated AI confidence is unreliable; effect sizes are public, citable, and don't drift over time. The confidence claim becomes traceable to research rather than to model calibration.
- **"Why it matters" per finding.** A one-line research-grounded explanation per violation, naming the cognitive mechanism and the effect size. Educators get the *why* without needing to open the textbook.
- **Severity as color.** Slide cards get colored left borders (red/amber/green). An educator scanning the report can triage by color before reading any text. This sounds like a visual nicety; it's actually a workflow decision — most users will not read findings sequentially. They will scan for problems.
- **PPTX support.** LibreOffice-based PPTX→PDF→PNG path so PowerPoint users don't have to export first.

## v0.4 — Make It Viable for Regular Use

**Goal:** Bring cost and latency to a level that supports iterative review — i.e., a user fixes a finding, re-uploads, and checks again.

**Diagnosis.** A 7-slide deck cost ~$1.50 and ran for several minutes. Three causes: sequential API calls, the system prompt being re-billed every call, high-resolution images, and an overpowered model for the task.

**Fixes:**

| Change | Mechanism | Product effect |
|---|---|---|
| Prompt caching | `cache_control: ephemeral` on the system prompt; 6 of 7 slides hit the cache | ~90% cost reduction on system prompt tokens |
| Parallel API calls | `AsyncAnthropic` + `asyncio.gather` across slides | Total latency drops to slowest single slide |
| Lower DPI (150 → 96) | Renderer change | ~40% fewer image tokens; Claude still reads slides correctly |
| Haiku 4.5 over Sonnet 4.6 | Model swap | 3× cheaper, ~2× faster; task is well-defined pattern matching |

**Outcome.** A 7-slide deck now returns in 7.5 seconds, at roughly an order of magnitude lower cost. The product is now viable for the iterative review workflow — fix, re-upload, re-check — that the v0.3 design assumes users want.

## v0.5 — Expand Coverage

**Goal:** Add four new Mayer principles (Temporal Contiguity, Segmenting, Pre-Training, Modality) to cover all nine of the major principles in *Multimedia Learning* — without lowering the bar on false positives.

The temptation in any feature expansion is to ship more findings to make the product look more thorough. That would have been a regression. The bar — "flag only patterns that genuinely reduce learner outcomes per Mayer's research" — applied to four new domains required reading chapters 10-13 in full and writing calibration rules just as strict as the originals.

The non-obvious findings:

- **Temporal Contiguity** (d=1.31, the largest effect in the book) has a boundary condition that makes it nearly irrelevant for slide decks. The violation requires the entire narration to be separated from the entire animation as two large blocks. A presenter advancing slides while speaking already achieves temporal contiguity. Rule: do not flag normal slide presentations.
- **Modality** (d=1.00) is widely misunderstood as "avoid text on slides." It's not. The principle applies to fast-paced narrated animations with dense captions. For learner-paced slideshows: d=0.16 (negligible). For second-language learners: d=-0.83 (effect reverses, text helps). Rule: do not flag slides for having text.
- **Pre-Training** (d=0.78) doesn't apply to expert audiences. It also doesn't apply to decks that already include a vocabulary or key-terms slide — those *are* pre-training.
- **Segmenting** (d=0.67) is satisfied by presenter-advanced slides. A 4-bullet slide is not a segmenting violation.

Each new principle could have produced a class of false positives equivalent to what v0.2 fixed. The calibration discipline applied earlier is what made this expansion safe.

---

## Product Decisions, Summarized

The decisions worth foregrounding for a hiring manager:

**Per-slide API calls over whole-deck calls.** Cheaper and faster to send the whole deck at once. I chose per-slide because slide-level attribution is the natural unit of the user's task ("which slide do I fix") and because individual slide PNGs are what students actually see. Parallelism reclaimed most of the latency cost.

**Effect-size weighted scoring over a simple 1-5 rubric.** A simpler score would be easier to read but would hide the fact that some violations matter much more than others. The weighting makes the score *correct* in proportion to research evidence, not just *legible*.

**Confidence from literature, not from the model.** Self-rated AI confidence drifts; effect sizes don't. This was a trust decision, not a technical one.

**Filter low-severity findings.** Computed but not displayed. The product favors signal over completeness. Verbose mode is a one-line change if user feedback demands it.

**Haiku over Sonnet.** Structured pattern recognition against well-defined rules with examples in the prompt. Haiku handles this well. The model string is a one-line revert if accuracy ever regresses.

---

## What's Next

Ordered by what would most change the user's experience:

1. **Inline PowerPoint annotations.** The current HTML report is a separate artifact from the deck. Educators want findings *on the slides they're editing*. This is the biggest UX gap.
2. **Slide-level health score.** Extend the scorecard to per-slide, so users can sort and prioritize the worst slides.
3. **Comparison across deck versions.** Store results so a user can see "I fixed 4 of 7 violations between v1 and v2." This creates a habit loop the current product doesn't.
4. **Batch API integration.** 50% cost reduction for non-interactive use (overnight review of a course catalog). Enables institutional pricing.
5. **Audience-specific calibration.** Currently the analyzer assumes a typical novice audience. An expertise toggle would change which principles apply (expertise reversal effect on Multimedia, Pre-Training).
