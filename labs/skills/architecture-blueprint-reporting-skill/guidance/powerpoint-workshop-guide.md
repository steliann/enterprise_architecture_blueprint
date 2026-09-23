# PowerPoint Architecture Blueprint Workshop Guide

## Purpose

The PowerPoint is used during a customer call to understand and validate the
architecture baseline.

It is not a compressed copy of the Word report.

Unless the user explicitly asks for assessment content, the deck should not
contain gap analysis or recommendations.

## Typical size

Aim for 8–12 slides.

## Default storyline

Adapt to the customer, but a strong baseline workshop sequence is:

1. **Title**
2. **What we want to confirm today**
   - scope;
   - information basis;
   - baseline-not-assessment framing.
3. **Architecture footprint at a glance**
   - blueprint KPIs such as number of use cases, products, flows, quality
     controls, operational capabilities and architecture decisions.
4. **Business outcomes shape different architecture needs**
5. **The architecture should be considered as a whole**
   - simplified source -> integration -> shared core -> specialised products/consumption.
6. **Data and integration patterns**
   - only the principal patterns and the controls that materially distinguish them.
7. **Data products and consumption boundaries**
8. **Trust, data quality and governance**
9. **Operations and resilience**
   - include material orchestration/capacity/service-window dependencies.
10. **Architecture transitions and future directions**
11. **Points to confirm**
   - only if useful; otherwise combine with the final slide.
12. **Confirming the architecture baseline**
   - what needs to be validated after the call.

Reduce or combine slides when the architecture is simpler.

## Discussion orientation

Slides should help conversation.

Use concise prompts such as:

- **Discuss / validate**
- "Is this the right boundary?"
- "Is this still the intended direction?"
- "What is the agreed service expectation?"
- "Are these the remaining transition dependencies?"
- "Who owns this operating decision?"

Do not ask the customer to validate low-level detail that is not important to
the architecture.

## What to omit

By default omit:

- full entity inventories;
- detailed ADR text;
- exact technical configuration;
- exhaustive open-question lists;
- evidence metadata;
- gap scoring;
- recommendations;
- target-state proposals not already present in the baseline.

## Slide writing

Use action titles rather than labels where possible.

Examples:

- "DataBank is the shared analytical centre of gravity"
- "Different outcomes require different consumption boundaries"
- "Trust is established across the full data lifecycle"
- "Runtime capacity is part of the operating model"
- "Several current structures are deliberately transitional"

Keep each slide to one primary message.

## KPI slide

When the blueprint provides reliable counts, include a footprint slide early in
the deck.

Good KPIs include:

- business use cases;
- required capabilities;
- data products;
- principal data flows;
- quality controls;
- operational capabilities;
- architecture decisions.

These are **architecture scope KPIs**, not health scores. Do not imply that a
larger or smaller count is inherently good or bad.

## Visual design

Follow `styles/powerpoint-style.md`.

Use diagrams, architectural bands, product/group cards and transition timelines
instead of text-heavy bullet slides when possible.

## Closing slide

When the meeting is only about understanding the solution, close with
confirmation of the baseline, not with "recommendations" or "what should change".

The gap analysis can be introduced later as a separate activity.

## QA

Render the deck and inspect all slides before delivery.

Check:

- no clipped or overflowing text;
- consistent spacing;
- readable font size;
- diagrams align cleanly;
- discussion prompts are visible but not dominant;
- slide sequence tells a coherent story;
- no assessment language has slipped into a baseline-only deck.
