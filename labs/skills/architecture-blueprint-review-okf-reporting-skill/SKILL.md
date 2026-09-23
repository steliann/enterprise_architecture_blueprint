---
name: architecture-blueprint-review
version: 1.1.0
description: Produce and validate an architecture blueprint review OKF, a customer-facing Word architecture assessment report, and review slides from an Architecture Blueprint OKF. Supports staged or end-to-end generation and remains architecture- and vendor-agnostic.
---

# Architecture Blueprint Review Skill

## Purpose

Use this skill to convert an **Architecture Blueprint OKF** into a governed architecture review and then render that review into two customer-facing assets:

1. **Architecture Blueprint Review OKF** - authoritative review knowledge containing coverage, architecture gaps, validation items, recommendations, traceability and the integrated review conclusion.
2. **Architecture Assessment Word report** - readable customer document derived from the Review OKF.
3. **Architecture Review slide deck** - workshop/customer-discussion presentation derived from the Review OKF, optionally prefixed with blueprint-baseline slides when the Blueprint OKF is also available.

The skill is deliberately **architecture-agnostic**. Never assume a customer, technology, vendor, product, data platform, cloud, licence, operating model or target architecture unless it is evidenced by the supplied Blueprint/Review or explicitly provided by the user.

## Input routing

Determine the requested pipeline from the files supplied and the user's explicit request.

| Input available | Valid outputs |
|---|---|
| Blueprint OKF | Review OKF; or Review OKF + Word report + slides |
| Review OKF | Word report; slides; or both |
| Blueprint OKF + Review OKF | Refresh/validate Review OKF, then Word/slides as requested |
| Word report / slides + Review OKF | Validate or refresh the downstream asset against the Review OKF |

Default behavior when the user provides **only a Blueprint OKF** and asks generally for an architecture review is to run the full pipeline: **Blueprint -> Review OKF -> Word -> Slides**. If the user explicitly requests only one stage, produce only that stage and its validation report.

## Authority and derivation rules

- The **Blueprint OKF** is authoritative for current architecture knowledge.
- The **Review OKF** is authoritative for review conclusions, gap states, validation items, recommendations, priorities and downstream counts.
- The **Word report and slides are renderings of the Review OKF**. They must not introduce new gaps or materially change recommendations.
- If customer validation changes a fact, update the Blueprint first where possible, then refresh the Review.
- Never use downstream prose as evidence to overwrite the Blueprint without explicit user direction.

## Core review principle

**Unknown is not automatically a gap.**

Promote an item only when all three are sufficiently supported:

1. the expected architecture outcome or condition is clear;
2. the current condition is sufficiently evidenced;
3. a material mismatch can be stated.

If the current condition is not established, keep the issue as a **coverage finding** or **Validation Item**. Use a **Candidate Gap** when evidence supports a material mismatch but customer/design confirmation is still required. Use an **Active Gap** only when the mismatch is confirmed.

## Required workflow

### A. Blueprint -> Review OKF

Read `guides/02-blueprint-to-review-okf.md` and the templates in `templates/review-okf/`.

1. Validate the Blueprint structure with `scripts/validate_blueprint_okf.py`.
2. Declare the reviewed Blueprint name/version/date/scope.
3. Build the coverage assessment across all in-scope categories.
4. Separate coverage limitations, Validation Items, Candidate Gaps and Active Gaps.
5. Create one file per gap and one file per validation item.
6. Create one recommendation per gap unless a clearly documented systemic recommendation intentionally addresses multiple gaps.
7. Preserve traceability to Blueprint IDs and ADRs.
8. Build gap/recommendation registers and the integrated review report.
9. Validate with `scripts/validate_review_okf.py`.
10. Package the review as a ZIP with one top-level `architecture-blueprint-review/` directory.

### B. Review OKF -> Word report

Read `guides/03-review-okf-to-word-report.md`.

1. Use the Review OKF as the only source of review conclusions.
2. Build the report using `templates/word/architecture-assessment-report-template.docx` and the content mapping in `templates/word/architecture-assessment-report-content-template.md`.
3. Include all in-scope gaps, validation items and recommendations represented in the Review OKF.
4. Keep aggregated architecture conclusions explicitly separate from the gap count.
5. Validate structure and Review-to-report consistency with `scripts/validate_report_docx.py`.
6. Render the DOCX to page images and inspect every page before delivery.

### C. Review OKF -> Slides

Read `guides/04-review-okf-to-slides.md`.

1. Use `templates/slides/architecture-blueprint-review-template.pptx` as the design seed.
2. If the Blueprint is available, use the **combined discussion** mode: baseline slides + methodology + review portfolio + one slide per gap + validation/conclusions/next steps.
3. If only the Review OKF is available, use **review-only** mode: methodology + portfolio + priorities + one slide per gap + validation/conclusions/next steps.
4. Use **one gap per slide** for every in-scope gap unless the user explicitly requests a shorter executive subset.
5. Keep each slide traceable to exactly one `GAP-NNN` and its recommendation(s).
6. Validate with `scripts/validate_review_slides.py`.
7. Render to PDF/images and visually inspect every slide before delivery.

### D. End-to-end

Read `guides/05-end-to-end.md`. Generate and validate in strict order:

`Blueprint OKF -> Review OKF -> Review manifest -> Word report -> Slides`

Do not build the Word report or slides from provisional notes before the Review OKF passes validation.

## Review lenses

Use these lenses to search for material architecture mismatches. They are perspectives, not automatic gap generators:

- requirements fitness;
- technology fitness;
- integration and data movement;
- data management and product design;
- data quality, governance and trust;
- operational fitness, observability and recovery;
- security/access/retention where represented by the Blueprint;
- architecture consistency and decision fitness;
- lifecycle, transition and evolution.

## Coverage model

Use the reproducible scoring rubric in `guides/02-blueprint-to-review-okf.md` and `config/defaults.yaml`. `config/defaults.yaml` is the immutable skill default and must remain inside the skill package.

If the user supplies a portable `coverage-rubric.yaml` (for example one exported by the Architecture Blueprint Workbench), treat it as an **override of only `coverage_rubric`**. Do not overwrite or modify `config/defaults.yaml`. Resolve the external enabled/disabled flags and weights against the skill defaults before scoring. Validate an override with:

```bash
python scripts/validate_coverage_rubric.py /path/to/coverage-rubric.yaml
```

Every generated coverage category must retain the raw 0/0.25/0.5/0.75/1 dimension scores in `coverage_dimensions` frontmatter, including `null` for N/A. Every category and the combined coverage report must record `coverage_model_hash` and `coverage_model_version`. This allows a later weight-only recalculation without changing the underlying evidence assessment.

The coverage score measures **review confidence/readiness**, not architecture quality and not percentage documentation complete. Disabled dimensions are excluded. Enabled but non-applicable dimensions are excluded per category. The remaining enabled/applicable weights are renormalized for each category. The overall score is the arithmetic mean of the in-scope category scores.

When the user supplies a new rubric for an existing Review OKF:

- if all category reports contain complete `coverage_dimensions`, recalculate scores from those retained raw dimension scores;
- if the review predates v1.1 and lacks raw dimension scores, do not infer them from the old total score: rerun the coverage assessment from the Blueprint evidence;
- changing only enabled flags or weights does **not** change coverage findings, gaps, or recommendations unless the user asks for a full review refresh.

## Gap writing standard

Each gap must include:

- assessment position/state/confidence/priority;
- expected architecture condition;
- current architecture condition and evidence basis;
- precise architecture gap statement;
- impact if not addressed;
- affected Blueprint elements and ADRs;
- customer/design validation questions;
- linked recommendation(s).

A gap statement must be **solution-independent**. Do not put a preferred product or implementation into the problem statement.

## Recommendation writing standard

Each recommendation must include:

- originating gap(s);
- target architecture condition/direction;
- current capability path where relevant;
- strategic/expanded capability path where relevant;
- adjacent technology/domain responsibilities where relevant;
- preferred path and rationale;
- delivery sequence;
- risks/trade-offs;
- expected benefits;
- observable acceptance measures;
- required ADR and Blueprint changes;
- customer validation/decision points.

A product feature is never a recommendation by itself. Start from the gap and explain why the capability improves the architecture.

## Benefit model

Use one or more of these benefit classes consistently:

- Reliability & Risk
- Operational Efficiency
- Performance & Scalability
- Agility & Time to Value
- Governance & Architectural Sustainability

## Aggregated architecture conclusions

After the detailed gaps, synthesize 2-4 broader target-state directions when several findings converge. These are **aggregated findings**, not extra `GAP-NNN` records. Never include them in the gap count.

## Refresh rules

When refreshing an existing review:

- preserve stable IDs;
- add/retire/supersede rather than renumbering existing gaps or recommendations;
- recalculate coverage and counts;
- preserve state history in frontmatter/change logs where present;
- update downstream Word/slides only after the Review OKF is refreshed and validated.

## Validation gate

Before delivery, run the relevant validators. A final asset must have no structural errors. Warnings may remain only when they represent deliberate review limitations and are described to the user.

Use `scripts/validate_all.py` when producing more than one output.
