---
name: csp-objectives-from-architecture-review
description: Generate or refresh a Customer Success Plan Objectives Open Knowledge Format (OKF) package from an Architecture Blueprint Review OKF, preserving objective identity, recommendation traceability, business-outcome linkage, planning semantics, templates, and structural validation.
---

# CSP Objectives from Architecture Blueprint Review

Use this skill when the user wants to create, refresh, validate, or package **Customer Success Plan (CSP) Objectives OKF** from an **Architecture Blueprint Review OKF**.

The skill is architecture-detail agnostic. It must derive objectives from the supplied artifacts and must not embed customer- or product-specific conclusions that are not present in the inputs.

## Core outcome

Produce a package with this canonical structure:

```text
customer-success-plan-objectives/
├── index.md
├── customer-success-plan-objectives.md
├── knowledge-model/
│   ├── index.md
│   ├── knowledge-model.md
│   └── objective-guide.md
├── business-objectives/
│   ├── index.md
│   └── BO-*.md
└── technical-objectives/
    ├── index.md
    └── TO-*.md
```

Also produce a companion `validation-report.md`. When the user requests a downloadable package, zip the OKF folder and validation report together.

## Input contract

**Primary required input**
- Architecture Blueprint Review OKF, supplied as a directory or ZIP.

**Strongly recommended for refreshes**
- Previous CSP Objectives OKF. Use it to preserve immutable BO/TO identities, created dates, and still-valid business objectives.

**Required for a first complete CSP when business evidence is insufficient in the review**
- Architecture Blueprint OKF, or another authoritative source containing the business use cases needed to define the business-objective layer.

Do not fabricate business objectives merely to satisfy schema integrity. See `guides/input-contract.md`.

## Non-negotiable rules

1. **Architecture recommendations are authoritative for technical objectives.** Every active recommendation in the review must be represented by an active technical objective unless an explicit, evidenced consolidation is documented.
2. **Business use cases are authoritative for business objectives.** Do not derive a business objective solely from a technology recommendation if the business outcome is not evidenced.
3. **IDs are immutable.** Preserve an existing objective ID only when the intended outcome remains semantically equivalent. A material replacement gets a new ID.
4. **Recommendation numbers are not objective numbers.** Never remap a TO merely because a new recommendation happens to reuse an old `REC-nnn` identifier.
5. **Outcome, not implementation task.** Objectives describe measurable future conditions; implementation steps belong in rationale, milestones, or delivery plans.
6. **Separate architecture state from execution state.** `status`, `objective_state`, and `planning_state` have different meanings.
7. **Horizon is sequencing, not a committed date.** Inherit the review's horizon but do not turn it into a delivery commitment.
8. **No silent loss of coverage.** New, removed, superseded, or consolidated recommendations must be visible in the generation/validation report.
9. **Do not promote validation questions into objectives.** Review validation items are evidence gaps unless the review explicitly promotes them into recommendations.
10. **Validate before delivery.** Run the packaged validator and fix all structural errors before returning the final ZIP.

## Workflow

### 1. Inspect the source review

Run:

```bash
python scripts/inspect_review.py <review-okf-or-zip> --markdown review-inventory.md --json review-inventory.json
```

Read the integrated review report, recommendation register, and every recommendation artifact. Establish:
- review version;
- active recommendation IDs;
- title, horizon, impact, category, confidence and state;
- originating gaps;
- affected use cases/capabilities/products/flows/operations/ADRs;
- architecture advice, expected benefits, validation conditions and traceability.

Do not treat the recommendation title alone as sufficient evidence.

### 2. Determine generation mode

**Refresh mode — Review + prior CSP**
- Compare every prior technical objective to current recommendation semantics.
- Preserve the TO ID only when the objective outcome is still materially the same.
- Update wording, measures, traceability, horizon/impact/category and `last_updated_date` as required.
- Allocate new TO IDs above the highest historical TO number for materially new outcomes.
- Remove no historical meaning by reassigning an old ID to a different outcome.
- Retain business objectives whose underlying business outcomes/use cases remain current.

**First-generation mode — Review + sufficient business-use-case evidence**
- Create BOs from authoritative business use cases/outcomes.
- Create TOs from active recommendations.
- Map each TO to the BOs it materially enables.

**Review-only mode with insufficient business evidence**
- Generate the technical-objective mapping and a validation/generation report, but mark the complete CSP package as blocked rather than inventing BOs.
- Ask for the Blueprint OKF or a prior CSP only if a complete package cannot otherwise be grounded. If the user asked for best-effort output without clarification, deliver the grounded partial result and identify the missing evidence.

### 3. Build or refresh the business-objective layer

Follow `guides/mapping-guide.md` and `templates/business-objective.md`.

A business objective must:
- reference one or more primary business use cases;
- describe a customer/business outcome, not a platform implementation;
- carry business success measures that can be accepted by an accountable customer stakeholder;
- retain existing ID/created date when semantically unchanged in refresh mode.

### 4. Build or refresh the technical-objective layer

Default mapping is **one current architecture recommendation → one active technical objective**. Consolidate recommendations only when they genuinely define one inseparable measurable outcome and document the rationale.

For each TO:
- derive the objective from the recommendation's target architecture condition;
- inherit recommendation `horizon`, `impact`, and normally `category`;
- map to all materially enabled BOs, not every BO mechanically;
- convert recommendation acceptance/advice into **technical success measures**;
- preserve implementation choices as rationale/constraints rather than rewriting the TO as a task list;
- keep customer planning fields uncommitted unless the source artifacts contain agreed owners/baselines/targets/dates.

Use `templates/technical-objective.md`.

### 5. Regenerate portfolio and indexes

Generate:
- root `index.md`;
- `customer-success-plan-objectives.md` roll-up;
- `business-objectives/index.md`;
- `technical-objectives/index.md` grouped by horizon;
- the generic knowledge model and objective management guide from the templates/references in this skill.

The roll-up must make recommendation coverage and planning sequence visible.

### 6. Validate

Run:

```bash
python scripts/validate_csp.py <generated-csp-folder-or-zip> --review <review-okf-or-zip> --report validation-report.md
```

For refreshes, also run with the prior package:

```bash
python scripts/validate_csp.py <generated-csp> --review <review> --previous <previous-csp> --report validation-report.md
```

The shipping gate is **zero structural errors**. Warnings must either be resolved or explicitly explained in the final response.

See `guides/validation-guide.md` for the validation contract.

### 7. Package

After validation:

```bash
python scripts/package_csp.py <generated-csp-folder> --review <review-okf-or-zip> --out <output.zip>
```

Deliver the ZIP and summarize:
- BO count;
- TO count;
- recommendation coverage;
- Now/Next/Later distribution;
- preserved IDs vs newly allocated IDs;
- validation error/warning count.

## Authoring quality bar

The CSP is a customer-success planning artifact, not a copy of the architecture review. Rewrite architecture recommendations into durable outcomes that can later receive owners, baselines, targets, dates, milestones and acceptance evidence.

Prefer statements such as:
- “Establish controlled and measurable recovery behaviour for …”
- “Provide consumer-visible freshness and trust state for …”
- “Reduce peak-window acquisition work through managed incremental capture …”

Avoid task formulations such as:
- “Install X.”
- “Configure Y.”
- “Run a workshop.”

Implementation actions may appear in architecture rationale, dependencies, or future milestones, but they are not the objective itself.

## Package references

Read as needed:
- `guides/input-contract.md` — source requirements and operating modes.
- `guides/generation-guide.md` — detailed generation procedure.
- `guides/identity-and-refresh-rules.md` — immutable-ID and semantic equivalence rules.
- `guides/mapping-guide.md` — recommendation → TO → BO mapping.
- `guides/validation-guide.md` — structural and semantic validation.
- `schemas/csp-objective-schema.yaml` — machine-readable validation contract.
- `templates/` — canonical markdown templates.
- `examples/recommendation-to-objective.md` — architecture-agnostic worked example.
