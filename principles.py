# Distilled from Mayer, R.E. (2020). Multimedia Learning (3rd ed.), Chapters 5–9.
# ~1,500 tokens vs. 73,000 for raw chapter text — same signal, far less noise.

PRINCIPLES_TEXT = """
=== MULTIMEDIA PRINCIPLE (d=1.35) ===
Definition: People learn better from words AND pictures than from words alone.

What it requires on a slide:
- Any concept being explained should have a corresponding visual (diagram, illustration, chart, graph, or photo that directly depicts the process or relationship).
- The visual must be RELEVANT and COORDINATED with the words — not decorative.

Violation patterns to flag:
- A slide that explains a process, system, or relationship using only text paragraphs or bullet points with no supporting graphic.
- A slide where the only image is a stock photo, logo, or decorative element unrelated to the concept.

Boundary conditions: Applies most strongly to low-knowledge learners and complex processes. A slide with a single factual statement (e.g., a definition) may not need an image.

=== COHERENCE PRINCIPLE (d=0.86) ===
Definition: People learn better when extraneous material is EXCLUDED rather than included.

Three forms of coherence violation:
1. Interesting but irrelevant words/pictures — e.g., a decorative stock photo of students in a library on a slide about cell biology; statistics or anecdotes that are interesting but don't serve the learning objective.
2. Unneeded verbal elaboration — wordy sentences, tangential details, or lengthy explanations that go beyond what the learner needs to understand the core concept.
3. Background music or decorative visual noise — anything that consumes cognitive resources without contributing to the learning goal.

Violation patterns to flag:
- Decorative images (clip art, stock photos) that don't illustrate the concept.
- Slides with dense blocks of text containing details irrelevant to the stated learning objective.
- Logos, borders, or animations used as decoration.

Key insight: Extraneous material competes for working memory resources. Even "interesting" additions hurt learning if they don't serve the goal.

=== SIGNALING PRINCIPLE (d=0.70) ===
Definition: People learn better when cues are added that highlight the organization and essential elements of the material.

Two forms of signaling:
1. Verbal signaling — outlines/preview statements naming key sections, headings for each section, pointer words ("first... second... as a result..."), graphic organizers (flow charts, matrices, hierarchies that spatially arrange key terms).
2. Visual signaling — arrows or pointers directing attention to specific parts of a graphic; color changes coordinated with narration; emphasis on the relevant component at the moment it is discussed.

What works (research-backed):
- Outlines, headings, pointer words
- Graphic organizers (flow charts, matrices)
- Specific pointing gestures to diagram parts
- Color change coordinated with verbal emphasis

What does NOT work as signaling:
- Highlighting key words in red/bold alone (without other cues)
- General gestures toward a diagram rather than specific parts

Violation patterns to flag:
- Key terms introduced without any visual or textual emphasis.
- A diagram with no labels, arrows, or callouts directing attention to what matters.
- No headings or structural cues on a content-dense slide.
- A multi-step process with no numbering, flow arrows, or sequence indicators.

=== REDUNDANCY PRINCIPLE (d=0.72) ===
Definition: People learn better from graphics + narration than from graphics + narration + printed text that repeats the narration verbatim.

Core idea: When identical information appears in both spoken narration AND as full on-screen text simultaneously, the visual channel is overloaded — learners must split attention between reading and listening to the same words.

What IS redundant (flag it):
- Speaker notes that contain the full sentences read aloud on the slide — identical content in two modalities simultaneously.
- Full-sentence captions that repeat verbatim what a narration track says.
- On-screen paragraphs that duplicate what the presenter will speak word-for-word.

What is NOT redundant (do not flag):
- Brief labels or short callouts on a diagram (a few words, not sentences).
- On-screen text when there is NO narration (text-only presentation is fine).
- Providing words in a second language or for unfamiliar technical terms.

Boundary condition: The redundancy effect is strongest for fast-paced narrated animation. For self-paced text-only slides (no narration), this principle does not apply.

=== SPATIAL CONTIGUITY PRINCIPLE (d=0.82) ===
Definition: People learn better when corresponding words and pictures are placed NEAR each other on the page or screen, rather than far apart.

What it requires:
- Text that describes or labels a graphic should appear immediately adjacent to the part of the graphic it describes — not in a legend at the bottom, not on a separate slide, not across the slide from the image.
- Labels should be integrated INTO or directly beside the diagram component they describe.

Violation patterns to flag:
- Text explanation on the left half of the slide, corresponding diagram on the right half with no integration (average centers more than 40% of slide width apart is a strong signal).
- A numbered diagram with a legend or key at the bottom of the slide listing what each number means.
- Text on one slide and the corresponding illustration on the next slide.
- Captions placed at the bottom of the slide for a graphic at the top.

Boundary conditions: Applies most strongly when (a) the material is complex, (b) the diagram cannot be understood without words, and (c) the learner is unfamiliar with the content.
"""
