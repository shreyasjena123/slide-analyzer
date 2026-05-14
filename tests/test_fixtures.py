"""
Fixture-based tests for the slide analyzer.

Each fixture represents either a clear violation or a known-safe pattern.
The analyzer is called with real Claude API calls (not mocked) to measure
actual false positive rates.

Safe fixtures — patterns Mayer explicitly says are NOT violations:
  - Text-only slide for simple content
  - Text-only slide with expert audience marker
  - Standard two-column layout (text left, image right)
  - Short key-word labels near diagram components
  - Title/agenda slide
  - Slide with relevant photo of subject matter
  - Learner-paced deck text (no redundancy)
  - Slide with section heading, bullets, numbered steps (good signaling)
  - Additional detail in speaker notes only

Violation fixtures — patterns Mayer explicitly identifies as violations:
  - Complex multi-step process in text only, no diagram
  - Decorative stock photo with no instructional illustration
  - Interesting but irrelevant seductive detail paragraph
  - Complex diagram with numbered legend at bottom (spatial contiguity)
  - Multi-step process as disconnected bullets with no flow/arrows (signaling)
"""

from __future__ import annotations

import os
from typing import Optional, List, Tuple
import pytest
from parser import SlideData
from analyzer import analyze_slide

# Skip if ANTHROPIC_API_KEY not available (CI without key)
pytestmark = pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set",
)

LEARNING_OBJECTIVE = "Understand how photosynthesis converts light energy into chemical energy stored in glucose."

# Minimal 1x1 transparent PNG in base64 — used as placeholder image
# A real deck would pass a rendered PNG; for fixture tests we pass a blank.
BLANK_PNG_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk"
    "YPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
)


def _slide(
    title: str = "",
    body_text: str = "",
    notes: str = "",
    image_count: int = 0,
    image_positions: Optional[List[Tuple]] = None,
    text_box_positions: Optional[List[Tuple]] = None,
    num: int = 1,
) -> SlideData:
    return SlideData(
        num=num,
        title=title,
        body_text=body_text,
        notes=notes,
        image_count=image_count,
        image_positions=image_positions or [],
        text_box_positions=text_box_positions or [(0.0, 0.1, 0.9, 0.9)],
        slide_width=960.0,
        slide_height=540.0,
    )


def _has_violation(result: dict, principle: str) -> bool:
    return any(v["principle"] == principle for v in result.get("violations", []))


def _high_severity_violations(result: dict) -> list[dict]:
    return [v for v in result.get("violations", []) if v.get("severity") == "high"]


# =============================================================================
# VIOLATION FIXTURES — analyzer SHOULD flag these
# =============================================================================

def test_multimedia_violation_complex_process_text_only():
    """Complex multi-step causal process described in text only with no diagram."""
    slide = _slide(
        title="How Photosynthesis Works",
        body_text=(
            "Light energy strikes chlorophyll molecules in the thylakoid membrane. "
            "This excites electrons, which travel through the electron transport chain. "
            "As electrons move, they pump protons across the membrane, creating a gradient. "
            "ATP synthase uses this gradient to produce ATP. "
            "Meanwhile, water molecules are split, releasing oxygen as a byproduct. "
            "In the Calvin cycle, CO2 is fixed using the ATP and NADPH produced."
        ),
        image_count=0,
    )
    result = analyze_slide(slide, BLANK_PNG_B64, LEARNING_OBJECTIVE)
    assert _has_violation(result, "Multimedia"), (
        f"Expected Multimedia violation for complex process in text only. Got: {result}"
    )


def test_coherence_violation_seductive_detail():
    """Interesting but irrelevant paragraph inserted into a content slide."""
    slide = _slide(
        title="Photosynthesis and Energy",
        body_text=(
            "Plants convert light into glucose through photosynthesis.\n\n"
            "Fun fact: Did you know that on average, a bolt of lightning contains "
            "enough energy to toast 100,000 slices of bread? Lightning strikes the "
            "earth about 100 times per second. Each year approximately 2,000 people "
            "are killed by lightning worldwide — making it one of nature's deadliest phenomena."
        ),
        image_count=0,
    )
    result = analyze_slide(slide, BLANK_PNG_B64, LEARNING_OBJECTIVE)
    assert _has_violation(result, "Coherence"), (
        f"Expected Coherence violation for irrelevant seductive detail. Got: {result}"
    )


def test_spatial_contiguity_violation_numbered_legend():
    """Complex diagram described with numbered legend at bottom — classic split-attention."""
    slide = _slide(
        title="Chloroplast Structure",
        body_text=(
            "Figure 1: Chloroplast cross-section\n\n"
            "Legend:\n"
            "1. Outer membrane\n"
            "2. Inner membrane\n"
            "3. Thylakoid membrane\n"
            "4. Granum (stack of thylakoids)\n"
            "5. Stroma\n"
            "6. Lumen\n\n"
            "See diagram above for component locations. "
            "Each numbered component plays a distinct role in light and dark reactions."
        ),
        image_count=1,
        image_positions=[(0.05, 0.1, 0.95, 0.6)],
        text_box_positions=[(0.05, 0.65, 0.95, 0.95)],
    )
    result = analyze_slide(slide, BLANK_PNG_B64, LEARNING_OBJECTIVE)
    assert _has_violation(result, "Spatial Contiguity"), (
        f"Expected Spatial Contiguity violation for numbered legend at bottom. Got: {result}"
    )


def test_signaling_violation_complex_process_no_structure():
    """Multi-step causal chain presented as a flat prose block with no sequence cues."""
    slide = _slide(
        title="The Calvin Cycle",
        body_text=(
            "Carbon dioxide enters the cycle and combines with RuBP catalyzed by RuBisCO. "
            "The resulting compound is unstable and splits into two 3-PGA molecules. "
            "ATP and NADPH reduce 3-PGA to G3P. "
            "Some G3P exits the cycle to form glucose. "
            "The remaining G3P is used to regenerate RuBP using ATP. "
            "RuBP is ready to accept another CO2 molecule and the cycle repeats."
        ),
        image_count=0,
    )
    result = analyze_slide(slide, BLANK_PNG_B64, LEARNING_OBJECTIVE)
    # Either Signaling (no flow cues) or Multimedia (no diagram) should fire — both are valid
    flagged_signaling = _has_violation(result, "Signaling")
    flagged_multimedia = _has_violation(result, "Multimedia")
    assert flagged_signaling or flagged_multimedia, (
        f"Expected Signaling or Multimedia violation for flat prose multi-step process. Got: {result}"
    )


# =============================================================================
# SAFE FIXTURES — analyzer should NOT flag these (known-safe per Mayer)
# =============================================================================

def test_safe_title_slide():
    """Title/agenda slide — intentionally sparse, explicitly safe per Mayer."""
    slide = _slide(
        title="Photosynthesis",
        body_text="BIO 201 — Unit 3\nDr. Sarah Chen",
        image_count=0,
    )
    result = analyze_slide(slide, BLANK_PNG_B64, LEARNING_OBJECTIVE)
    high = _high_severity_violations(result)
    assert len(high) == 0, (
        f"Title slide should have no high-severity violations. Got: {result}"
    )


def test_safe_agenda_slide():
    """Agenda/outline slide — good signaling per Mayer, not a coherence violation."""
    slide = _slide(
        title="Today's Agenda",
        body_text=(
            "1. Review: cell structure\n"
            "2. Light reactions\n"
            "3. Calvin cycle\n"
            "4. Factors affecting photosynthesis\n"
            "5. Summary and Q&A"
        ),
        image_count=0,
    )
    result = analyze_slide(slide, BLANK_PNG_B64, LEARNING_OBJECTIVE)
    high = _high_severity_violations(result)
    assert len(high) == 0, (
        f"Agenda slide should have no high-severity violations. Got: {result}"
    )


def test_safe_standard_two_column_layout():
    """Text on left, diagram on right — normal slide layout, NOT a spatial contiguity violation."""
    slide = _slide(
        title="Light Reactions Overview",
        body_text=(
            "Key steps:\n"
            "• Light strikes photosystem II\n"
            "• Water is split, O2 released\n"
            "• Electrons enter transport chain\n"
            "• ATP is produced via chemiosmosis\n"
            "• Photosystem I re-energizes electrons\n"
            "• NADPH is produced"
        ),
        image_count=1,
        image_positions=[(0.55, 0.1, 0.95, 0.9)],
        text_box_positions=[(0.05, 0.1, 0.5, 0.9)],
    )
    result = analyze_slide(slide, BLANK_PNG_B64, LEARNING_OBJECTIVE)
    assert not _has_violation(result, "Spatial Contiguity"), (
        f"Standard two-column layout should NOT be flagged for Spatial Contiguity. Got: {result}"
    )


def test_safe_image_with_overall_caption():
    """A single image with a brief overall caption below — not a spatial contiguity violation
    because the caption describes the image as a whole, not individual unlabeled components."""
    slide = _slide(
        title="Chloroplast Structure",
        body_text="Figure 1: Cross-section of a plant chloroplast showing thylakoid membranes.",
        image_count=1,
        image_positions=[(0.1, 0.1, 0.9, 0.75)],
        text_box_positions=[(0.05, 0.78, 0.95, 0.92)],
    )
    result = analyze_slide(slide, BLANK_PNG_B64, LEARNING_OBJECTIVE)
    assert not _has_violation(result, "Spatial Contiguity"), (
        f"Single image with brief overall caption should NOT be a Spatial Contiguity violation. Got: {result}"
    )
    assert not _has_violation(result, "Redundancy"), (
        f"Brief figure caption should NOT be flagged as redundancy. Got: {result}"
    )


def test_safe_relevant_subject_photo():
    """A photo of the actual subject (e.g., a leaf) — not a multimedia violation."""
    slide = _slide(
        title="Leaves: Nature's Solar Panels",
        body_text="The leaf is the primary organ of photosynthesis in most plants.",
        image_count=1,
        image_positions=[(0.4, 0.2, 0.95, 0.85)],
        text_box_positions=[(0.05, 0.1, 0.95, 0.25), (0.05, 0.25, 0.4, 0.85)],
        notes="Show the cross-section photo of a leaf. Students can see the mesophyll layers.",
    )
    result = analyze_slide(slide, BLANK_PNG_B64, LEARNING_OBJECTIVE)
    assert not _has_violation(result, "Multimedia"), (
        f"Slide with relevant subject photo should NOT be flagged for Multimedia. Got: {result}"
    )


def test_safe_slide_with_clear_structure():
    """Well-structured slide with heading, numbered steps, pointer words — good signaling."""
    slide = _slide(
        title="Three Stages of Photosynthesis",
        body_text=(
            "Stage 1: Light Absorption\n"
            "Chlorophyll captures photons from sunlight.\n\n"
            "Stage 2: Energy Conversion\n"
            "Excited electrons flow through the electron transport chain, producing ATP and NADPH.\n\n"
            "Stage 3: Carbon Fixation\n"
            "ATP and NADPH power the Calvin cycle to fix CO2 into glucose."
        ),
        image_count=0,
    )
    result = analyze_slide(slide, BLANK_PNG_B64, LEARNING_OBJECTIVE)
    assert not _has_violation(result, "Signaling"), (
        f"Well-structured slide with numbered stages should NOT be flagged for Signaling. Got: {result}"
    )


def test_safe_text_slide_no_audio_no_redundancy():
    """Self-paced text slide with no narration — redundancy principle does not apply."""
    slide = _slide(
        title="Key Terms: Photosynthesis",
        body_text=(
            "Chlorophyll: the green pigment that absorbs light energy\n"
            "Thylakoid: membrane-bound compartment where light reactions occur\n"
            "Stroma: fluid-filled space where the Calvin cycle takes place\n"
            "ATP: adenosine triphosphate, the energy currency of the cell\n"
            "NADPH: electron carrier produced during light reactions"
        ),
        image_count=0,
    )
    result = analyze_slide(slide, BLANK_PNG_B64, LEARNING_OBJECTIVE)
    assert not _has_violation(result, "Redundancy"), (
        f"Text-only self-paced slide should NOT be flagged for Redundancy. Got: {result}"
    )


def test_safe_simple_definition_slide():
    """Simple single-concept definition — multimedia principle applies to complex content only."""
    slide = _slide(
        title="What is Photosynthesis?",
        body_text="Photosynthesis is the process by which plants use sunlight, water, and CO2 to produce glucose and oxygen.",
        image_count=0,
    )
    result = analyze_slide(slide, BLANK_PNG_B64, LEARNING_OBJECTIVE)
    # A simple one-sentence definition is not a multimedia violation per Mayer
    high = _high_severity_violations(result)
    assert len(high) == 0, (
        f"Simple definition slide should have no high-severity violations. Got: {result}"
    )


def test_safe_post_lesson_elaboration():
    """Additional detail presented after the core explanation — coherence exception per Mayer."""
    slide = _slide(
        title="Going Deeper: C4 and CAM Photosynthesis",
        body_text=(
            "Now that you understand the standard C3 pathway, here are two important variants:\n\n"
            "C4 plants (corn, sugarcane): pre-fix CO2 in mesophyll cells to concentrate it "
            "near RuBisCO in bundle sheath cells, reducing photorespiration.\n\n"
            "CAM plants (cacti, succulents): open stomata at night to collect CO2, "
            "storing it as organic acids released during the day."
        ),
        image_count=0,
        notes="This slide comes AFTER students have mastered the basic Calvin cycle.",
    )
    result = analyze_slide(slide, BLANK_PNG_B64, LEARNING_OBJECTIVE)
    assert not _has_violation(result, "Coherence"), (
        f"Post-lesson elaboration slide should NOT be flagged for Coherence. Got: {result}"
    )
