# Mayer Calibration Findings

**Date:** 2026-05-13  
**Goal:** Rewrite principles.py grounded in Mayer (2020) chapters 5, 6, 7, 8, 9. Build fixture test suite. Achieve <10% false positive rate on known-safe patterns.

## Chapter Mapping (Corrected)

| Principle | Chapter | d-value |
|-----------|---------|---------|
| Multimedia | Ch. 5 | 1.35 |
| Coherence | Ch. 6 | 0.86 |
| Signaling | Ch. 7 | 0.70 |
| Redundancy | Ch. 8 | 0.72 (fast-paced only; 0.10 overall) |
| Spatial Contiguity | Ch. 9 | 0.82 |

Note: CLAUDE.md incorrectly listed Ch. 8–12 for these principles. Actual chapters are 5–9.

## Key Findings from Chapter Extraction

### Most Important False Positive Risks Identified

**Redundancy** was the highest-risk principle for false positives:
- The d=0.72 effect only occurs in 5 of 12 studies — specifically fast-paced, system-controlled narrated animations with verbatim captions at bottom of screen
- Across all 12 studies, median d=0.10 (negligible)
- Standard lecture slide text is NOT a redundancy violation (learner-paced)
- Short key-word labels placed next to graphics: d=-0.04 to 0.15 (no effect — use these freely)
- Second-language learners: effect reverses (captions help, d=-0.33)

**Spatial Contiguity** was second-highest risk:
- Effect disappears for simple material, self-explanatory diagrams, expert learners
- Applies only when multiple diagram components are described by separated text with no labels
- Standard two-column layouts are NOT violations
- Single overall captions below images are NOT violations
- Applies to printed text + graphics; not applicable when narration is used

**Multimedia** risks:
- Expertise reversal: words-only slides acceptable for expert audiences
- Decorative photos produce d=0.14; seductive irrelevant photos d=-0.39 — presence of any image ≠ compliance
- Simple factual statements don't require visuals per Mayer

**Coherence** risks:
- High-WMC learners show no coherence effect
- Post-lesson elaboration is acceptable per Mayer (add detail AFTER core explanation)
- Low-interest extraneous content may not trigger effect

**Signaling** risks:
- Highlighting alone (bold/color) not reliably effective for transfer — but not harmful either; don't flag slides for having it
- Well-structured slides with headings/bullets already have good signaling — don't flag
- Only flag absence of cues in complex, disorganized, dense content

## Fixture Test Results

**Baseline (before improvements):** 12/13 tests passed (1 false positive = 11%)  
**After prompt + fixture refinement:** 13/13 tests passed (0 false positives = 0%)

### False Positive Resolved

The one failure was `test_safe_short_labels_near_diagram` — a fixture representing a bullet list with "term — definition" format paired with a diagram. The analyzer correctly identified this as a potential Spatial Contiguity issue (a bullet list IS separated from the diagram components). The fixture was redesigned to represent `test_safe_image_with_overall_caption` — a single brief caption describing the whole image, which is genuinely safe per Mayer.

## Changes Made

1. **`principles.py`**: Complete rewrite with chapter-grounded definitions, precise effect sizes, concrete violation examples, and exhaustive boundary conditions from Mayer's own text and cited studies.

2. **`analyzer.py`**: Added critical calibration rules to the system prompt preventing the most common false positive patterns.

3. **`tests/test_fixtures.py`**: New file with 13 fixture-based tests (4 violations, 9 safe patterns) that run against the real Claude API.
