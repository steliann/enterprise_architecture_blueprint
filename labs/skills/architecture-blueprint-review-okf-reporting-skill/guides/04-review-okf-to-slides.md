# Review OKF -> Review Slides

## Modes

### Review-only mode

Use when only the Review OKF is available:

1. Title
2. Assessment methodology/evidence rule
3. Gap/validation/recommendation portfolio
4. Priority architecture themes
5. One slide per gap
6. Validation items
7. Aggregated target direction / conclusions
8. Validation and next steps

### Combined blueprint + review discussion mode

Use when the Blueprint is also available. Prepend compact baseline slides similar to the supplied customer-discussion example:

1. shared baseline objective;
2. architecture footprint/KPIs;
3. business outcomes and architecture emphasis;
4. high-level architecture/core product or service view;
5. principal integration/data-service patterns;
6. trust/control model;
7. operations model;
8. active transitions/evolution.

Then continue with the review-only sequence.

## One gap per slide

By default, every Candidate or Active Gap in scope receives its own slide. Do not combine multiple gaps into one detailed slide merely to shorten the deck.

Each gap slide contains:

- gap title;
- state, priority, confidence, response class;
- current condition;
- architecture gap;
- impact if not addressed;
- recommendation target direction;
- 3-5 implementation/architecture actions;
- expected benefit line;
- customer validation question(s).

The slide should be traceable to one `GAP-NNN`. The recommendation side can summarize one or multiple linked `REC-NNN` artifacts.

## Portfolio and priority slides

All counts and ranks come from the Review OKF. The priority slide should highlight the first 3-5 gaps/themes, not invent a separate prioritization model.

## Validation items

Keep Validation Items visually separate from gaps and state that they require evidence before negative architecture conclusions are made.

## Style

Use `templates/slides/architecture-blueprint-review-template.pptx` as the design seed and `templates/slides/slide-style-guide.md` for typography/layout.

## Validation and visual QA

```bash
python scripts/validate_review_slides.py review.pptx --review <review.zip-or-directory>
```

For an intentionally shortened executive deck, add `--allow-subset` and provide a slide-selection note in the deck or accompanying output.

Render the PPTX to PDF/images and inspect every slide for overflow, overlap, unreadable text and inconsistent alignment.
