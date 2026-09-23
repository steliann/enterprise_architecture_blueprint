# Input Contract

## Required source

The Architecture Blueprint Review OKF is the authoritative source for the current technical improvement portfolio. The skill expects, at minimum:

```text
architecture-blueprint-review/
├── architecture-blueprint-review.md
└── recommendations/
    ├── index.md
    └── REC-*.md
```

A richer review may also contain gaps, coverage findings and validation items. Use them as context, but technical objectives are sourced from the active recommendation set.

## Optional prior CSP

A previous CSP Objectives OKF is the preferred identity ledger during refresh. It is authoritative for historical objective IDs and `created_date` values, but not for whether an old objective is still active.

Use the prior CSP to answer:
- Does the same objective already exist under a stable BO/TO ID?
- Has the objective materially changed?
- Which IDs are already consumed historically?
- Which business objectives remain valid?

Never recycle a retired/superseded ID for a new meaning.

## Optional Blueprint OKF

Use the Blueprint when:
- creating the business-objective layer for the first time;
- a business use case changed materially;
- the review refers only to IDs and does not contain enough business context to define an outcome safely.

## Evidence sufficiency rule

A complete CSP package requires both:
1. an evidence-backed business-objective layer; and
2. a complete technical-objective layer covering the current recommendations.

If the review contains no usable business-use-case evidence and no prior CSP/Blueprint is provided, do **not** invent BOs. Produce a technical mapping/partial draft plus a validation report that states why complete schema validation is blocked.
