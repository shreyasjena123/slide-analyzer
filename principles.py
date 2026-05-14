# Grounded in Mayer, R.E. (2020). Multimedia Learning (3rd ed.).
# Chapters: 5 (Multimedia), 6 (Coherence), 7 (Signaling), 8 (Redundancy), 9 (Spatial Contiguity).
# Boundary conditions extracted directly from Mayer's own text and cited studies.

PRINCIPLES_TEXT = """
=== MULTIMEDIA PRINCIPLE (d=1.35, Ch. 5) ===
Mayer's definition: "People learn better from words and pictures than from words alone."

Effect size context: d=1.35 across 13 studies — but only for complex scientific/mechanical explanations (brakes, pumps, lightning, generators) with low-prior-knowledge college students. Effect applies to transfer tests (problem-solving), not rote recall.

WHAT IS A VIOLATION:
- A complex how-it-works process (multi-step mechanism, causal chain, biological process) explained with text only and no diagram, chart, or instructive illustration depicting the process.
- An image present but purely decorative — stock photo of a thinking person, generic background, company logo — that does not depict the concept being taught. Decorative photos produce d=0.14; seductive irrelevant photos produce d=-0.39 (hurt learning).
- An abstract, unlabeled illustration that learners cannot connect to the text (Schmeck et al., 2014: d=0.05 — no benefit from unconnected graphics).

WHAT IS NOT A VIOLATION — these are the specific conditions where the effect disappears:
- EXPERTISE: High prior knowledge learners showed no multimedia effect (Mayer & Gallini, 1990). For expert audiences, words-only slides are acceptable — they mentally generate the visual model from long-term memory. This is the expertise reversal effect (Kalyuga, 2014).
- SIMPLE CONTENT: Mayer states "The multimedia principle applies more strongly to complex explanations." A simple factual definition or single-claim statement may not benefit from a visual.
- TOO MANY GRAPHICS: Excessive graphic organizers (3+ per paragraph) yielded d=-0.03 (Stull & Mayer, 2007). More images does not mean better compliance.
- NON-CONCURRENT PRESENTATION: When animation and narration are shown sequentially rather than simultaneously, the effect is substantially reduced (Moreno & Mayer, 2002a). Concurrent pairing is required for full effect.
- REPRESENTATIONAL PHOTOS: A photo of the actual subject (historical figure, biological specimen, equipment) that IS the content is not a multimedia violation. Only the absence of instructive/organizational graphics matters.
- Title and agenda slides are intentionally sparse — these are not violations.

Analyzer calibration: The question is whether a complex process that would benefit from a visual has none, not whether every slide has an image. Do not flag a slide for lacking images if the content is simple, the audience is likely expert, or a photo of the subject is already present.

=== COHERENCE PRINCIPLE (d=0.86, Ch. 6) ===
Mayer's definition: "People learn better when extraneous material is excluded rather than included."

Three sub-versions from Mayer's own text:
1. Remove "seductive details" — interesting but irrelevant stories, photos, statistics (d=1.27 across 9 studies)
2. Remove unneeded elaboration and technical detail (d=0.70 across 8 studies)
3. Remove background music or decorative audio (d=0.95 across 2 studies)

Effect size context: d=0.86 overall. Studies used system-paced narrated animations and paper booklets with low-prior-knowledge college students, measuring transfer tests.

WHAT IS A VIOLATION:
- Seductive details: interesting but irrelevant text passages or photos inserted to "spice up" the lesson. Mayer's examples: a story about a football player struck by lightning inserted into a lightning lesson; statistics about lightning fatalities; 8–10 second video clips of lightning storms unrelated to the causal process being taught; inserted facts about sex, death, or injury.
- Unneeded elaboration: a 550-word passage when key-word captions already convey all steps; quantitative measurements/formulas inserted into a qualitative explanation; explanations of tangential related systems appended to the core lesson.
- Background music that plays continuously behind a narrated lesson, even "gentle" instrumental music (Moreno & Mayer, 2000: d=0.67–1.23).

WHAT IS NOT A VIOLATION — these are the specific conditions where the effect disappears:
- EXPERTISE: Low-WMC and low-prior-knowledge learners are most affected. High-WMC learners show no coherence effect (Sanchez & Wiley, 2006: d=0.97 for low WMC, no effect for high WMC). High-knowledge learners may benefit from the details that would hurt novices (expertise reversal, Kalyuga, 2014). Do not flag additional detail in lessons for expert audiences.
- PACING CONTROL: Rey (2012) meta-analysis found coherence effect is stronger for system-paced than learner-paced presentations. When learners control pace, they self-regulate attention and extraneous material is less damaging.
- ELABORATION AFTER THE CORE: Mayer explicitly states needed elaboration should be presented AFTER the learner has built a coherent model of the core content — detail at the end is not a violation. "After a concise multimedia presentation helps the learner understand the major steps in the process of lightning, additional material can be presented to elaborate on each step."
- LOW-INTEREST EXTRANEOUS CONTENT: Doolittle & Altstaedter (2009): added sounds and animations that "may not have been sufficiently distracting" yielded d=0.06 (null). The principle is calibrated to "particularly interesting" extraneous material, not neutral content.
- LOW COGNITIVE LOAD CONDITIONS: Park et al. (2011): under low cognitive load, seductive details slightly helped (d=-0.34, non-significant). When a lesson uses best-practice low-load design, extra content is less damaging.
- MUSIC AS CONTENT: Background music is not a coherence violation if music IS the essential content (e.g., a music history or music theory lesson where the music being analyzed is playing).
- Normal slide formatting: headers, footers, slide numbers, institutional logos in corners. These are not extraneous material.
- Brief examples or analogies that help learners connect new material to prior knowledge. Generative elaboration that builds understanding is not extraneous.
- Intentional humor that an instructor uses knowingly for pedagogical rapport — do not flag humor as a coherence violation.

Analyzer calibration: Flag only content that would genuinely compete for cognitive resources with the lesson's core message — highly interesting, emotionally salient, attention-grabbing material that is clearly off-topic. Do not flag mildly tangential content, post-lesson elaboration, or standard slide formatting.

=== SIGNALING PRINCIPLE (d=0.70, Ch. 7) ===
Mayer's definition: "People learn better when cues are added that highlight the organization of the essential material."

Two types of signals Mayer identifies:
1. Verbal: preview/outline sentence naming main sections, headings keyed to the outline, pointer words ("first," "second," "as a result," "most importantly")
2. Visual: arrows or labels pointing to SPECIFIC components being discussed; color changes that simultaneously highlight a specific graphic element while it is being narrated; specific pointing gestures by an onscreen agent

Effect size context: d=0.70 combined (d=0.51 for verbal signals in multimedia lessons; d=0.75 for verbal signals in words-only text; d=0.71 for visual signaling). Studies used narrated animations and illustrated text with college and high school students.

WHAT IS A VIOLATION:
- A complex multi-component diagram with no labels, arrows, or callouts identifying what each component is or does — learner must infer structure without guidance.
- A multi-step causal process presented as prose or disconnected bullets with no flow arrows, numbering, or sequence indicators.
- A complex chart or graph with no title, no axis labels, no annotation directing attention to the key finding.
- Content that has all elements presented with equal visual weight — no cue indicating what is most important.

WHAT IS NOT A VIOLATION — these are specific cases where the signaling effect disappears or is not supported:
- HIGHLIGHTING ALONE is insufficient: Red-colored or bolded text alone does not reliably improve transfer (Xie et al., 2019: d=0.05 for vocal stress only; d=0.02 for color alone). Mayer's conclusion: "There is insufficient evidence to recommend using highlighting when the goal is to improve transfer performance." A slide with bold or colored terms is NOT thereby violating the signaling principle — it just may not produce the full signaling benefit.
- GENERAL (NON-SPECIFIC) POINTING: An onscreen agent gesturing vaguely toward a diagram without indicating specific elements is ineffective (Fiorella & Mayer, 2016b: d=0.10; Li et al., 2019: d=-0.08). But absence of an onscreen pointing agent is not a violation — most slides have no such agent.
- SIMPLE CONTENT: Jeung, Chandler & Sweller (1997) found visual signaling effective for complex displays but NOT for simple displays. Do not flag a simple two-point slide for lacking structural cues.
- HIGH PRIOR KNOWLEDGE LEARNERS: Meyer et al. (1980) and Naumann et al. (2007) found signaling beneficial for low-skill readers but not for high-skill readers, who compensate by adjusting their own reading strategies. Richter et al. (2016): signaling helps low-prior-knowledge learners but not high-prior-knowledge learners.
- OVERUSE OF SIGNALS: Too many graphic organizers (3+ per paragraph) yielded d=-0.03 (Stull & Mayer, 2007). A slide already has structure through headers, bullets, and visual hierarchy — additional signals on a simple organized slide are not needed and not a violation.
- Clear section headings, numbered steps, and organized bullet structure ARE good signaling — do not flag these as problems.
- Arrows and flow diagrams are valid visual signals (Table 7.3 in Mayer) — do not flag them as clutter.
- Outline/preview statements at the start of a section are the core mechanism of the principle — do not flag these as redundant text.

Analyzer calibration: The principle is violated by ABSENCE of organizational cues in COMPLEX material where learners have low prior knowledge. Do not flag slides for lacking signals if the content is simple, the structure is already clear through headers and bullet hierarchy, or the audience is expert. Violations-by-commission are limited to: non-specific pointing gestures and overuse of signals to the point of visual confusion.

=== REDUNDANCY PRINCIPLE (d=0.72, Ch. 8) ===
Mayer's definition: "People learn better from graphics and narration than from graphics, narration, and printed text" — specifically when the printed text is IDENTICAL to the narration and the lesson is FAST-PACED.

CRITICAL SCOPE LIMITATION: The strong d=0.72 effect was produced in ONLY 5 of 12 studies — specifically fast-paced, system-controlled narrated animations with full identical captions at the bottom of the screen for native-language college students. Across all 12 studies, the median effect size is d=0.10 (negligible). Mayer's exact language: "the redundancy effect is strongest when learners do not have control over the pace of presentation."

WHAT IS A VIOLATION:
- Full, verbatim identical captions displayed at the bottom of the screen simultaneously with fast-paced narration in a system-controlled animation — the learner must visually scan between the animation and the caption, overloading the visual channel.
- Reading every bullet point verbatim, slide after slide, in a fast-paced instructor-controlled presentation (the "reading from slides" pattern).

WHAT IS NOT A VIOLATION — these are the specific conditions where the effect disappears or reverses:
- LEARNER-CONTROLLED PACING: When learners control the pace (slideshow they advance themselves, interactive simulation), the effect is negligible or absent (Mayer et al., 2018: d=-0.08, -0.09; Schuler et al., 2013: null; Makransky et al., 2019: d=0.05). Standard lecture slide decks — where the presenter or learner controls pacing — fall into this category. Do NOT flag text on lecture slides as redundancy violations.
- SHORT KEY-WORD LABELS PLACED NEAR GRAPHICS: When text is shortened to a few key words AND placed next to the corresponding graphic element (not at the bottom as a long caption), the redundancy effect disappears entirely (Mayer & Johnson, 2008: d=-0.04 to 0.15). Short labels integrated with diagrams are the CORRECT design pattern.
- SECOND-LANGUAGE LEARNERS: The effect reverses for learners studying in their second language — captions help (Lee & Mayer, 2018: d=-0.33 favoring captions). Providing onscreen text for L2 learners reduces extraneous processing.
- UNFAMILIAR OR TECHNICAL VOCABULARY: When spoken words are technical or unfamiliar, redundant text gives learners time to process word meaning. Named boundary condition by Mayer.
- REWORDED (NOT IDENTICAL) TEXT: Yue et al. (2013) found that shortened and reworded onscreen text HELPED transfer. Mayer's definition of "redundant" requires text to be IDENTICAL to narration — reworded summaries or shorter paraphrases are NOT what this principle addresses.
- NO GRAPHICS PRESENT + SHORT SEGMENTS: When there are no graphics and verbal segments are short, text+narration together (verbal redundancy) HELPS learning — Moreno & Mayer (2002a); Adesope & Nesbit (2012). This is not a violation.
- RETENTION GOALS: Mayer explicitly notes redundant text may help "when the goal is verbatim memory for the words rather than transfer test performance."
- Text on slides where NO audio narration is being delivered — the principle requires audio narration to be present simultaneously. A self-paced text-based deck has no redundancy issue.

Analyzer calibration: ONLY flag redundancy when there is strong evidence that: (1) identical text and narration will be delivered simultaneously, AND (2) the pace is fast and system-controlled, AND (3) the audience is native-language learners with sufficient prior knowledge. For standard slide decks without audio, for learner-paced presentations, for short key-word labels near graphics, or for second-language audiences — do not flag redundancy.

=== SPATIAL CONTIGUITY PRINCIPLE (d=0.82, Ch. 9) ===
Mayer's definition: "People learn better when corresponding words and pictures are presented near rather than far from each other on the page or screen."

Mayer's own examples: (1) a car braking system diagram with components numbered 1–6 and a separate numbered legend at the bottom vs. text placed directly next to each component; (2) a text passage on one page and all illustrations on the next page vs. each paragraph placed beside its illustration.

Effect size context: d=0.82 across 9 studies (all college students, all complex scientific content, ALL measuring transfer tests). Effect is weaker on retention tests (g=0.39 vs g=0.65 for transfer, Schroeder & Cenkci, 2018). Studies compared severely separated conditions (different pages, bottom-of-screen captions) to tightly integrated conditions.

WHAT IS A VIOLATION:
- A numbered diagram (components labeled 1, 2, 3…) with a separate numbered legend at the bottom — forces visual search between diagram and legend.
- A lengthy text explanation on one side and the diagram it describes on the other, with no integration — especially when text describes specific components that have no labels pointing to them.
- A full paragraph of prose below or above a complex diagram with multiple unlabeled components.
- Captions placed far from the graphic element they describe that explain specific labeled components.

WHAT IS NOT A VIOLATION — these are the specific conditions where the effect disappears:
- SIMPLE MATERIAL: "Strong spatial contiguity effect for complex material but not for simple material" (Schroeder & Cenkci, 2018; Chandler & Sweller, 1991, 1996). When material is simple, learners have spare cognitive capacity to handle the visual search cost. A simple diagram with a brief caption below is not a meaningful violation.
- SELF-EXPLANATORY GRAPHICS: "If words are not needed for understanding a graphic, then it is not effective to place words near to rather than far from the corresponding parts of the graphic" (Ayres & Sweller, 2014). A self-sufficient diagram, photograph, or icon does not require spatial integration with text.
- HIGH PRIOR KNOWLEDGE / EXPERTISE REVERSAL: "The spatial contiguity principle is most applicable when the learner is not familiar with the material." Mayer et al. (1995, Expt. 2): integrated > separated for low-knowledge learners but NOT for high-knowledge learners (Kalyuga, Chandler, & Sweller, 1998; Yeung, Jin, & Sweller, 1998). Expert audiences generate their own verbal commentary from long-term memory.
- NARRATED SLIDES: "The spatial contiguity principle comes into play in situations where printed text is called for." When words are delivered as spoken narration (audio), the spatial contiguity principle does NOT govern text placement — the temporal contiguity and modality principles apply instead. Do not flag text placement on a narrated slide using this principle.
- STANDARD TWO-COLUMN LAYOUT: Text on the left and a diagram on the right is normal slide design. This is NOT a spatial contiguity violation unless the text specifically describes labeled components of the diagram that have no labels pointing to them.
- NUMBERED LEGEND WITH CORRESPONDENCE CUES: A numbered legend is a lesser violation — Johnson & Mayer (2012, Expt. 3) found it still produced a benefit for full integration (d=0.35), but meaningfully smaller than severe separation. Not all separation is equally harmful.
- SHORT LABELS NEAR COMPONENTS: Mayer's own integrated designs use short labels embedded in or next to diagram components. This IS the correct pattern — proximity of short labels is the solution, not a problem.
- RETENTION-FOCUSED MATERIAL: Effect is substantially weaker for retention (g=0.39) than transfer (g=0.65). A slide designed for recall rather than deep understanding is less affected.

Analyzer calibration: Flag only when: (1) complex material, AND (2) text describes specific components of a diagram, AND (3) corresponding elements have no labels or spatial connection, AND (4) the audience is likely low-prior-knowledge. Do not flag standard two-column layouts, simple graphics with captions, self-explanatory diagrams, narrated slides, or slides for expert audiences.
"""
