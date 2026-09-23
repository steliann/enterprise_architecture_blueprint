# Blueprint OKF -> Architecture Blueprint Review OKF

## Objective

Produce a governed review package that separates **coverage**, **architecture gaps**, **validation items** and **recommendations** while preserving direct traceability to the reviewed Blueprint snapshot.

## Stage 1 - Establish the review baseline

Record the Blueprint name, version, snapshot date, review date, declared scope and any exclusions. Do not mix evidence from different Blueprint versions without explicitly refreshing the review baseline.

Run:

```bash
python scripts/validate_blueprint_okf.py <blueprint.zip-or-directory>
```

Structural validation is a prerequisite, not proof that the architecture is complete.

## Stage 2 - Coverage assessment

Evaluate each in-scope coverage category against the following criteria. The default rubric is stored in `config/defaults.yaml`. If a `coverage-rubric.yaml` is supplied, resolve its enabled flags and weights against those defaults and use the resolved rubric for the entire review:

| Criterion | Weight | Question |
|---|---:|---|
| Required field completeness | 15 | Are the fields required by the Blueprint's own model populated sufficiently for review? |
| Relationship integrity | 15 | Are references valid and are key forward relationships present? |
| Ownership and accountability | 10 | Are decision/service/control owners known where architecture conclusions depend on them? |
| Lifecycle state clarity | 10 | Are current, target, transitional, deprecated and retirement states distinguishable? |
| End-to-end traceability | 10 | Can business need be traced through required capability to realization, trust and operations? |
| Authority and interface contracts | 10 | Are source authority, overlap, cutover and interface assumptions explicit where material? |
| Control thresholds and acceptance | 10 | Are measurable thresholds, exception paths and acceptance criteria represented? |
| Operations, monitoring and recovery | 10 | Are service expectations, monitoring, failure handling and recovery sufficiently known? |
| Security, retention and access | 5 | Are material access, retention and disclosure constraints represented? |
| Decision currency and rationale | 5 | Do ADRs explain material choices and is current fitness/relevance visible? |

### Scoring and rubric persistence

For each criterion assign a raw value from 0 to 1, or `null` when genuinely N/A:

- `1.00` - strong enough for reliable conclusions;
- `0.75` - mostly established, with bounded open items;
- `0.50` - mixed; high-level conclusions possible but detailed claims conditional;
- `0.25` - weak; substantial validation required;
- `0.00` - absent or contradictory for the category.

Disabled rubric dimensions are excluded globally. Mark genuinely non-applicable enabled dimensions as N/A and renormalize the remaining enabled/applicable weights for that category. Round each category to the nearest integer. Overall score = arithmetic mean of the in-scope category scores.

Persist the raw per-dimension values in each category report frontmatter under `coverage_dimensions`. Persist `coverage_model_hash` and `coverage_model_version` in every category and in the combined coverage report. Also copy the resolved rubric to `review-model/coverage-rubric.yaml` so the Review OKF carries the exact scoring model used.

A subsequent change to enabled flags or weights can therefore recalculate the category totals without reinterpreting evidence. If an older Review OKF does not contain `coverage_dimensions`, perform a full coverage rescore from the Blueprint rather than reverse-engineering raw scores from the previous total.

Coverage levels:

- 85-100 High
- 70-84 Moderate-High
- 50-69 Moderate
- 30-49 Low-Moderate
- 0-29 Low

The score is a **review-confidence index**. Never describe it as architecture quality or documentation percentage.

## Stage 3 - Coverage findings

For every material coverage limitation record:

- category;
- finding statement;
- calculated impact;
- affected elements;
- global priority;
- reviewer override and mandatory comment if an override is used.

Impact guidance:

- Critical - prevents a reliable conclusion over a material architecture outcome or can conceal a severe control/security/regulatory failure.
- High - materially constrains an important gap/decision/critical flow or service conclusion.
- Medium - limits precision but does not prevent the main architecture assessment.
- Low - localized or mainly editorial/structural weakness.

## Stage 4 - Promotion test

Apply the decision test to every potential gap:

1. Is the expected architecture condition clear?
2. Is the current condition sufficiently established?
3. Is the mismatch material?
4. Is the gap statement independent of a preferred solution?
5. Can affected elements and consequences be identified?

Disposition:

- no expected condition -> refine the criterion;
- current condition unknown -> coverage finding or Validation Item;
- likely material mismatch with evidence but confirmation pending -> Candidate Gap;
- confirmed material mismatch -> Active Gap;
- no material consequence -> Blueprint open item, not a gap.

## Stage 5 - Gap creation

Use `templates/review-okf/gaps/gap-template.md`. Preserve one stable `GAP-NNN` through its lifecycle.

Each gap contains:

- assessment position;
- expected architecture condition;
- current architecture condition/evidence;
- gap statement;
- impact if not addressed;
- affected Blueprint elements;
- related ADRs/capabilities;
- validation questions;
- recommendation links.

Do not create a product-shaped gap such as "Customer does not use Product X." State the architecture condition that is unfit or missing.

## Stage 6 - Validation items

Use `templates/review-okf/gaps/validation/validation-item-template.md` when a potentially material issue exists but the current control/condition is not sufficiently evidenced.

Validation Items are not included in gap counts.

## Stage 7 - Recommendations

Use `templates/review-okf/recommendations/recommendation-template.md`.

The recommendation should establish the target condition, then explain implementation paths. If current/strategic entitlements or adjacent technologies are relevant, preserve the distinction but do not force it when the architecture is not product-specific.

Every recommendation must define observable acceptance measures and identify required ADR/Blueprint changes.

## Stage 8 - Integrated review

Build:

- coverage combined view + category reports;
- gap register;
- validation register;
- recommendation register;
- `architecture-blueprint-review.md` executive/integrated review;
- `index.md` package entry point;
- review model/guide.

Synthesize cross-gap themes and 2-4 aggregated architecture conclusions only where multiple gaps support a common target direction. These are not new gap records.

## Stage 9 - Validation and packaging

Run:

```bash
python scripts/validate_review_okf.py <review-directory-or-zip> --blueprint <blueprint-directory-or-zip>
```

Then ZIP the single top-level `architecture-blueprint-review/` directory.
