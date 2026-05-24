# Slide Analyzer

### A PM Case Study on Building Trust in AI Feedback

A side project I built solo over May 2026. This case study covers the product decisions, not the engineering. The full technical architecture is in a companion document.

---

## What This Case Study Is, and What It Isn't

This was a solo project. No design partners, no user interviews, no pilot cohort. The product decisions described below were made without users. Instead, I treated Mayer's research as a proxy for what users would value, and treated every false-positive class I caught in testing as a stand-in for a support ticket I would otherwise have received.

That's not as good as real users. The case study is about what PM judgment looks like under those constraints, and where I'd invest first with a budget.

---

## The Problem I Picked

If you've built a slide deck for teaching, you know the feeling: you finish it, sense something's off, and can't tell what. The fixes are easy if someone tells you what's wrong. They're hard if you have to diagnose your own work.

There are three options for that diagnosis today. Generic AI design feedback (Copilot, Designer, several startups) optimizes for visual polish: alignment, color, font consistency. It says nothing about whether the deck will actually teach. Human expert review costs $200+ per deck and takes days; it's right for high-stakes content but impractical for the 90% of decks that don't justify it. Self-review with no framework is what most educators do, which produces decks built on instinct.

The gap is research-grounded feedback at AI economics. Mayer's *Multimedia Learning* (3rd ed.) is the canonical reference: nine principles, each with a measured effect size on transfer learning, replicated across hundreds of studies. Nobody had built tooling against it.

Things I don't know about this problem: how often educators actually want this feedback versus how often I assume they do; whether instructional designers (who know Mayer) or generalist teachers (who don't) are the better wedge; what either would pay. Those are the first questions I'd answer with a budget.

## The Insight That Made This Worth Building

The product insight isn't that AI can analyze slides. That's table stakes. The insight is about trust.

Generic AI feedback fails because it's unfalsifiable. When Copilot says "this slide has too much text," the user can't evaluate whether the claim is true. There's no standard being applied. The advice is confident-sounding noise, and educators have learned to ignore it.

Mayer's principles flip that. Every claim is traceable to specific studies with specific effect sizes. "Your slide has bullet points that compete with on-screen narration" is unfalsifiable. "Your slide has on-screen narration alongside bullet points, which violates Mayer's Modality principle (d=1.00 across 19 studies)" is a claim a user can verify, push back on, or trust.

That's the only durable wedge against much-better-funded incumbents. If they ship Mayer-grounded analysis tomorrow, the product loses. As of build date, none of them had.

## The Wedge: What I Built First and What I Deliberately Didn't

The minimum loop that tests the insight: upload deck, automated analysis, HTML report with deck-level score, per-slide findings, severity, confidence, and research-grounded rationale. One-shot artifact, no integrations.

What I deliberately didn't build:

- **PowerPoint plugin or inline annotations.** Almost certainly the right long-term UX (findings should appear on the slide a user is editing). Building it first would mean shipping a Microsoft Office integration before knowing whether the analysis was useful. Wrong order.
- **Team and collaboration features.** A solo upload tells me whether one user finds value. Team workflows risk building features for a usage pattern that doesn't yet exist.
- **Content generation.** "Fix this slide for me" is the obvious next step. I shipped critique-only because critique is falsifiable. If the analysis is wrong, the user can tell. If a generated fix is wrong, they may not notice for years.
- **Comparison across versions.** Storing results would create a habit loop ("I improved from 67 to 84"). But the first question isn't whether users come back. It's whether they trust the first report at all.

Every feature not built was a hypothesis not yet worth testing.

## The Hard Product Decisions

Five decisions where the alternative was tempting and wrong.

### Scoring: effect-size weighted, not a simple rubric

**Decision:** Overall deck score is a 0-100 number weighted by Cohen's d values from Mayer's meta-analyses. A Multimedia violation (d=1.35) costs more than a Signaling violation (d=0.70).

**Alternative considered:** A letter grade or 1-5 rubric. Easier to read.

**Why I rejected it:** A simpler score would be more legible but less correct. The pitch is research-grounded feedback. A score that flattens effect sizes contradicts the pitch. The rebuttal ("users won't care about Cohen's d") is probably true for some users. The product can show a letter grade derived from the underlying number, but the number underneath has to be right.

### Confidence claims are derived from literature, not from the model

**Decision:** Each finding shows `high` or `medium` confidence based on the principle's effect size and breadth of evidence. The mapping is deterministic. Claude does not self-rate.

**Alternative considered:** Ask the model to rate its own confidence per finding. Easier to implement, more granular.

**Why I rejected it:** Self-rated AI confidence is poorly calibrated and drifts across model versions. If a user ever caught the model claiming high confidence on a wrong finding, the trust I'd spent months building would collapse. Literature-derived confidence is auditable, stable, and traceable to citations. If a user disagrees with a confidence level, they can argue with Mayer rather than with the product. This is the single most defensive decision in the design, and the one I'd be most reluctant to revisit.

### Filter low-severity findings before showing them

**Decision:** Low-severity violations are computed and stored but not rendered.

**Alternative considered:** Show everything; let users decide what matters.

**Why I rejected it:** The reports the product replaces fail because of noise, not missing signal. Every additional finding costs user attention. A user who sees 12 findings and skims misses the 3 important ones; a user who sees 3 reads all of them. Verbose mode is a one-line change if anyone asks for it. Defaulting to verbose and dialing back would compromise initial trust.

### Per-slide API calls instead of whole-deck

**Decision:** Each slide gets its own API call, with that slide's PNG as the image input.

**Alternative considered:** Send the whole deck (or batches) in one call. Cheaper, faster.

**Why I rejected it:** A deck-level call produces findings attributed to the wrong slide, or generalized across slides, or both. Per-slide matches the user's mental model: they fix slides, not decks. Parallelism (via async) reclaimed most of the latency cost. The cost penalty was real but acceptable until v0.4, when prompt caching closed most of it.

### Haiku, not Sonnet

**Decision:** `claude-haiku-4-5` for the analysis calls.

**Alternative considered:** `claude-sonnet-4-6`. Smarter, more expensive, slower.

**Why Haiku won:** Once the prompt is properly calibrated, Mayer principle checking is structured pattern recognition against a rule set with extensive examples. It's not open-ended reasoning. Haiku handles it well in testing. Unit economics matter: if cost-per-deck is the difference between "free trial" and "paid product," Haiku makes a free tier viable. The model string is a one-line revert if a class of edge cases ever requires Sonnet.

---

## The Central Story: Calibrated Trust

The most important thing I learned: what to flag is a product decision, not a research decision. Mayer's literature tells you which patterns hurt learning. It doesn't tell you which to surface to a user. Those are different questions, and confusing them is the failure mode of every research-grounded tool I've seen.

The calibration arc went through three phases.

### Phase 1: Headline numbers only (overflagging)

The first version of the system prompt described each principle at summary level: "people learn better when extraneous material is excluded." The model applied this literally and flagged everything. A logo in the corner: Coherence violation. A bullet list: Multimedia violation. Any text on a slide: Redundancy violation.

If this had shipped, users would have abandoned the product within minutes. The fix was reading the underlying chapters.

### Phase 2: Boundary conditions added (overcaution)

After reading the chapters, I added the full boundary conditions to the prompt. This fixed the false positives but introduced a new problem: the model hedged every finding. Reports became unreadable. Every claim ended with "however, this may not apply if your audience is expert and the pacing is learner-controlled and..."

The model had absorbed the research's caution but not its decisiveness. For a user, this was worse than overflagging. Overflagging is wrong but actionable; overcaution gives no signal.

### Phase 3: Calibrated decisiveness

The breakthrough was rewriting the calibration rules in the voice of a senior instructional designer giving peer feedback, not a researcher describing study conditions. The reframe: Mayer's boundary conditions are specific. They apply only when explicit conditions are present. If the slide deck doesn't show those conditions, the boundary doesn't apply. Default to flagging the violation; back off only with positive evidence that the boundary holds.

That single shift, from "only flag when sure" to "flag unless you have evidence not to," is what made the analyzer useful.

Concrete example: the Redundancy principle. The headline d=0.72 looks moderate and reliable. Reading chapter 8 shows the effect only replicates in 5 of 12 studies, and only when text and narration are identical, simultaneous, fast and system-controlled, and the audience is native speakers. A standard slide deck satisfies none of those. The calibration rule became absolute: do not flag text on slides unless there is explicit evidence of simultaneous fast-paced audio narration. No hedging.

The same pattern repeated across all nine principles. Each had a class of false positives the literature explicitly ruled out. Each required a rule strict enough to prevent the model from generating that class.

**The PM takeaway.** Trust in an AI product comes from what it doesn't flag, not from what it does. Every false positive in a user's first session lowers credibility for every real finding after it. The cost is asymmetric: a missed real issue can be caught later. Destroyed trust often can't.

---

## How I Validated Without Real Users

**Fixture suite as synthetic user complaints.** I built 13 fixture tests for patterns Mayer's research says should and shouldn't flag: a definition slide, an expert-audience technical diagram, a bullet list, a section heading, an image with a caption. Each false positive in the fixture suite became a stand-in for the support ticket I would have received from a real user. Baseline: 12/13 passing. After calibration: 13/13.

This is not as good as 13 real users telling me about 13 different false positives. It's structured, repeatable, and tractable to iterate against. The closest analog is a regression suite for a product whose primary failure mode is unwanted output.

**E2E across deck archetypes.** Five fixture decks representing real educator archetypes (lecture-heavy, diagram-heavy, sparse, mixed-media, unusual formatting) tested at the pipeline level. 30 parametrized assertions per deck. Caught real issues, including a stream-exhaustion bug on PPTX uploads that would have produced a 500 on every PowerPoint user's first attempt.

**What this didn't tell me.** Whether the report format matches how users want to consume findings. Whether the severity-by-color scan pattern matches their workflow. Whether the score is a meaningful number to them or theater. Whether they'd pay. Whether they'd come back. Whether they'd recommend it. Those are what real users would tell me, and what I'd buy first with a budget.

---

## Outcomes

The v0.4 performance work brought the product into the range where iterative use is plausible:

- Latency: 7.5 seconds for a 7-slide deck (down from several minutes).
- Cost per deck: order-of-magnitude reduction from the v0.1 baseline.
- Quality: 13/13 on the fixture suite. 0 crashes across 30 E2E tests.
- Coverage: 9 of Mayer's major principles, calibrated independently per principle.

These are prerequisite outcomes, not product outcomes. They're necessary for the product to work, not sufficient evidence that it does. Real product outcomes would be activation rate, retention from first to second use, decks improved between v1 and v2 reviews, willingness to pay. I don't have any of those.

---

## What I Got Wrong

**I built before talking to users.** I should have done 8 to 10 instructional designer interviews before writing a line of code. I didn't, because the engineering felt tractable and the discovery felt squishy. That's a PM failure mode: choosing the work you find concrete over the work that matters. With a budget, the first two weeks would be interviews, not commits.

**I chose the output format before validating the workflow.** The HTML report assumes users want a standalone document. They probably want findings on their slides as they edit. The right v0.1 might have been a Chrome extension on Google Slides, not a one-shot uploader. I don't know, because I didn't ask.

**I optimized cost before having evidence users would pay.** Premature optimization, in the PM sense. Unit economics matter eventually. They don't matter before a product-market fit signal exists.

**I picked Mayer because it's rigorous, not because users asked for it.** Educators may want simpler, less academic feedback. The product I built is calibrated to be defensible to a learning scientist. The product the market may want is calibrated to be useful to a tired teacher at 9pm on a Sunday. Those might be different products.

**The expansion to 9 principles was builder-driven.** I expanded because I wanted the product to be complete against Mayer's framework. A user-driven version would have asked whether users were hitting the limits of the 5-principle version. I didn't know, because I didn't have users.

---

## Product Roadmap

Ordered by user impact, with the bet each item makes.

### Now: validate the trust hypothesis with real users

- **15 instructional designer interviews.** Not to gather requirements. To test whether the report is actually trusted. Specific hypothesis: the effect-size citation per finding produces a different reaction than generic AI feedback. If yes, the wedge is real. If no, rethink the product.
- **Activation funnel instrumentation.** What percent of uploaders open the report? What percent click into individual findings? Where do they drop off?
- **One paid pilot with a corporate L&D team.** L&D has the highest willingness to pay. A pilot here tests pricing, not just usage.

### Next: move from report to workflow

- **Inline annotations in PowerPoint and Google Slides.** The HTML report is wrong as a long-term unit of delivery. Findings should appear on the slide a user is editing, in the tool they're editing it in. Biggest UX bet on the roadmap.
- **Re-analysis on edit.** Each upload is currently a fresh deck. Users should see findings update in near-real-time as they make fixes.

### Later: build the habit loop

- **Deck version comparison.** "You went from 67 to 84 between v1 and v2. Here are the 3 violations you fixed and the 1 you introduced."
- **Audience-specific calibration.** A toggle for expert vs. novice audiences. The current analyzer assumes a novice audience; the expertise reversal effect on Multimedia and Pre-Training means expert audiences need different calibration.
- **Slide-level health scores.** Sort the worst slides first. Lets users triage decks they don't have time to fix entirely.

### Maybe never: generation

The obvious next product is "fix this slide for me." I'm leaving it for last because generation introduces a class of failure (silently wrong fixes a user won't catch) that critique-only avoids. Critique is falsifiable. Generation partially isn't. I'd want a lot more user trust in the critique before adding generation on top of it.

---

## Closing

This was built solo without users. The product decisions were deliberate even when the data wasn't. The first money I'd spend on this would go to user research.
