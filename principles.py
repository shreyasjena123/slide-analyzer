# Grounded in Mayer, R.E. (2020). Multimedia Learning (3rd ed.).
# Chapters: 5 (Multimedia), 6 (Coherence), 7 (Signaling), 8 (Redundancy), 9 (Spatial Contiguity),
#           10 (Temporal Contiguity), 12 (Pre-Training), 13 (Modality).
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

=== TEMPORAL CONTIGUITY PRINCIPLE (d=1.31, Ch. 10) ===
Mayer's definition: "People learn better when corresponding words and pictures are presented simultaneously rather than successively."

Effect size context: d=1.31 across 8 studies (Mayer & Anderson 1991, 1992; Mayer & Sims 1994; Mayer et al. 1999) — all with college students, all computer-based narrated animations on mechanical/scientific processes (pumps, brakes, lightning, lungs), all measuring transfer tests. The violation being studied was presenting the ENTIRE narration THEN the ENTIRE animation as separate large blocks (140 seconds apart), not brief alternation.

WHAT IS A VIOLATION:
- A deck explicitly structured so that all spoken audio narration runs as a separate segment BEFORE or AFTER all corresponding slides are shown — meaning learners must hold an entire narration in working memory while waiting for the visuals (or vice versa). This is the "large successive block" pattern Mayer studied.
- An instructional video or animation where audio commentary describes one phase of a process while the screen shows a completely different phase — systematic misalignment throughout the lesson.

WHAT IS NOT A VIOLATION — these are the specific conditions where the effect disappears:
- SHORT ALTERNATING SEGMENTS: When successive presentation alternates in short segments (8–10 seconds of narration then 8–10 seconds of matching animation), the effect essentially disappears — median d<0.20 in three experiments (Mayer et al. 1999; Moreno & Mayer 1999). Any reasonable slide-by-slide presentation where each slide's narration and visuals are reasonably close in time does NOT violate this principle.
- LEARNER-CONTROLLED PACING: Michas & Berry (2000): learner-paced successive presentation showed d=0.09 (negligible). When learners control pace — as in any standard self-paced or presenter-advanced slide deck — they can re-examine material and the temporal contiguity effect is minimal or absent.
- STANDARD SLIDE PRESENTATIONS: A presenter advancing slides one by one while speaking about each slide IS presenting words and pictures in close temporal proximity. This is NOT successive large-block presentation. Do not flag a normal slide deck for temporal contiguity.
- NOTE: Mayer's studies required the boundary to be COMPLETE separation of ALL words from ALL pictures across the entire lesson. Slides shown in sequence where each slide has narration delivered while that slide is visible already achieve temporal contiguity.

Analyzer calibration: This principle is extremely difficult to violate in a standard slide deck, because individual slides with corresponding narration already achieve temporal contiguity. Flag ONLY when there is explicit structural evidence that a full audio track is presented completely before OR after all the visual slides — the "separate audio file, then slides" or "slides first, audio commentary later" pattern. A normal presented deck does not violate this principle.

=== PRE-TRAINING PRINCIPLE (d=0.78, Ch. 12) ===
Mayer's definition: "People learn more deeply from a multimedia message when they know the names and characteristics of the main concepts."

Effect size context: d=0.78 across 10 studies (Mayer et al. 2002a x3; Mayer et al. 2002b x2; Gegner et al. 2009 x2; Fiorella & Mayer 2012; Pilegard & Mayer 2016, 2018) — all involved complex multi-component systems (hydraulic brakes, tire pump, geology simulation, electrical circuits, adventure games) where learners were novices unfamiliar with component terminology. Pre-training provided names, locations, and states of each key part BEFORE the main lesson.

WHAT IS A VIOLATION:
- A complex technical lesson that immediately launches into a multi-step causal explanation of how a system works, using component names (pistons, valves, cylinders, neural pathways, molecular bonds) that the target novice audience is unlikely to know, with no prior introduction to what each component is and what states it can be in.
- A deck on a complex mechanism that skips any orientation to the key parts — going straight to "here's how the system functions" before establishing "here's what each part is."
- The violation is: NEW TERMS + COMPLEX CAUSAL EXPLANATION + FAST PACE + NOVICE AUDIENCE, all at once, with no prior component familiarization anywhere in the deck.

WHAT IS NOT A VIOLATION — these are the specific conditions where the effect disappears:
- HIGH PRIOR KNOWLEDGE / EXPERTISE: Clark et al. (2005) and Pollock et al. (2002): pre-training helped low-experience learners with large effect sizes (d=1.84, d=1.22) but showed NO benefit for high-experience learners. Expert audiences already have component models in long-term memory. Do not flag a lesson for an expert audience that skips component introduction.
- PRE-TRAINING IS PRESENT: Any slide deck that begins with a vocabulary slide, a "key terms" section, a labelled diagram tour, or a components overview IS implementing pre-training. These patterns satisfy the principle — do not flag them.
- SIMPLE MATERIAL: Pre-training manages "essential overload" — the condition where learning component meanings AND the causal explanation simultaneously exceeds capacity. If the material is simple or uses familiar vocabulary, there is no essential overload and pre-training is unnecessary.
- SLOW-PACED OR LEARNER-CONTROLLED LESSONS: The principle is most urgent when pace is fast. Mayer notes the need to manage essential processing is "most urgent when essential processing threatens to overload working memory." In a learner-paced deck where terms can be absorbed at the learner's own speed, the need for dedicated pre-training is reduced.
- GLOSSARY IN MARGIN / CLICKABLE DEFINITIONS: Plass et al. (1998, 2003): giving learners access to definitions or pictures of terms on demand helped comprehension for some learners. Just-in-time definition access achieves similar goals. Do not flag a deck that provides definitions inline or as annotations.
- TETRIS RESULT: Pilegard & Mayer (2018) found pre-training on Tetris piece names showed negligible benefit (d=0.22) because Tetris itself was not an effective learning activity. The principle requires a meaningful complex lesson to benefit from.

Analyzer calibration: Flag ONLY when (1) the deck targets novice learners, AND (2) the material is genuinely complex with multi-component mechanisms using technical vocabulary, AND (3) there is no vocabulary introduction, labelled component overview, or key terms section anywhere in the deck. Do not flag for expert audiences, simple material, decks that include inline definitions, or learner-paced lessons where learners can absorb terminology at their own pace. The question is: would a novice be overwhelmed by simultaneously learning what the components are AND how they interact, with no prior orientation?

=== MODALITY PRINCIPLE (d=1.00, Ch. 13) ===
Mayer's definition: "People learn more deeply from pictures and spoken words than from pictures and printed words."

Effect size context: d=1.00 across 19 studies — but 17 of these foundational studies used fast-paced, system-controlled narrated animations (lightning, brakes, pumps, electric motors, environmental science games) with familiar vocabulary and college students as native-language speakers. The final two studies pinpointed boundary conditions: learner-paced GIS slideshow (d=0.16, negligible) and second-language learners (d=−0.83, REVERSED). Ginns (2005) meta-analysis of 39 comparisons: overall d=0.72, strongest for system-paced dynamic graphics and transfer tests. Reinwein (2012): strongest for system-paced rather than student-paced lessons. Tabbers et al. (2004): for learner-controlled slow-paced lessons with technical jargon, effect REVERSED (d=−0.47).

WHAT IS A VIOLATION:
- An animation or fast-paced instructional video where the explanation of a complex causal process is delivered ONLY as dense full-sentence captions at the bottom of the screen simultaneously with the animation — overloading the visual channel by requiring learners to read AND watch the animation at the same time, with no audio narration available. This is the specific "captioned animation" pattern Mayer studied.
- A narrated screen recording or video where the speaker's words are duplicated as a full verbatim transcript on screen (graphics + printed text instead of graphics + narration), for a fast-paced system-controlled lesson with familiar vocabulary and native speakers.

WHAT IS NOT A VIOLATION — these are the specific conditions where the effect disappears or reverses:
- LEARNER-PACED / SELF-PACED DECKS: Mayer, Wells, Parong & Howarth (2019): learner-paced GIS slideshow showed d=0.16 (negligible). Tabbers et al. (2004): learner-paced lesson with technical jargon REVERSED (d=−0.47). When learners control pace, they have time to read and view graphics without visual channel overload. A standard self-paced slide deck with on-screen text does NOT violate the modality principle — learners can read at their own pace.
- SECOND-LANGUAGE LEARNERS: Lee & Mayer (2018): L2 learners performed BETTER with printed text than narration (d=−0.83 favoring text). Spoken text is transient — L2 learners need to re-read. Do not flag on-screen text for multilingual or international audiences.
- TECHNICAL / UNFAMILIAR VOCABULARY: When words are technical jargon or unfamiliar, the transient nature of spoken audio becomes a disadvantage — learners cannot re-hear missed terms. Mayer explicitly names this as a boundary condition where printed text may be preferred. Do not flag text-heavy slides about specialized technical content where vocabulary familiarity cannot be assumed.
- STATIC GRAPHICS (not animations): The modality effect is driven by the competition between reading printed text and simultaneously watching a dynamic animation. Static images or simple diagrams create far less visual channel demand. Reinwein (2012): effect stronger for dynamic than static graphics.
- SIMPLE MATERIAL / ISOLATED FACTS: Tindall-Ford et al. (1997) and Leahy et al. (2003): the modality effect applies to building mental models, NOT to memorizing isolated elements. A simple factual slide with a static image and a short caption does not create visual channel overload.
- LONG VERBAL SEGMENTS: Leahy & Sweller (2011); Wong et al. (2012): strong NEGATIVE modality effects when verbal segments were long. Very long spoken narration becomes a disadvantage — the transient nature of audio means learners cannot re-hear missed content. For complex dense narration, printed text may actually be preferred.
- TEXT-ONLY SLIDES: A slide with only text (no animation or complex graphic) has no visual channel split-attention problem in the first place. There is nothing to split attention between.
- HEARING IMPAIRMENTS / ACCESSIBILITY: For learners with hearing difficulties, printed text is necessary and not a modality violation.

Analyzer calibration: This principle is about the specific situation where a FAST-PACED, SYSTEM-CONTROLLED animation forces learners to simultaneously read dense caption text AND watch the animation, creating visual channel overload. In a standard self-paced slide deck, learners advance slides at their own pace — visual channel overload is not present, and the modality principle does not apply. Do NOT flag slides for having text on them. Do NOT flag slides for not having audio narration — most slide decks have no audio and that is normal. Only flag if there is clear evidence of (1) an animation or fast-paced video, AND (2) full-sentence dense captions are the only word delivery, AND (3) the pace is system-controlled, AND (4) the audience is native speakers with familiar vocabulary. For any self-paced slide deck, the modality principle simply does not apply.
"""
