# Markdown Architecture Blueprint Report Guide

## Role of the Markdown report

The Markdown report is the canonical customer-facing architecture baseline.
It is the source for Word and PowerPoint and should therefore contain the
complete narrative needed to understand the solution at architecture level.

It is not a dump of the OKF and it is not a gap analysis.

## Level of detail

Use three levels deliberately:

### Level 1 — business and architecture narrative

Always include. Explain what the architecture enables and why the main
structures and decisions matter.

### Level 2 — architecture mechanics needed to understand a decision

Include selectively. Examples: staging-to-warehouse-to-product flow, a public
serving boundary, reconciliation separate from ingestion, or workload-specific
runtime capacity.

### Level 3 — implementation and evidence detail

Keep in the OKF unless it is necessary to explain an architecture concern.
Examples: exact schedules, configuration parameters, individual tables, detailed
restart steps, evidence references and low-level mapping detail.

## How to consolidate the OKF

Do not mechanically list every entity.

- Use cases -> retain all material business outcomes, but write at outcome level.
- Required capabilities -> normally surface through other sections rather than as a list.
- Data flows -> consolidate into principal integration patterns.
- Data products -> retain material products/product families.
- Quality controls -> consolidate into trust/control themes.
- Operational capabilities -> consolidate into operating domains.
- ADRs -> retain the choices that materially shape architecture or transition.
- Sources/technologies -> include only those needed to explain the landscape.
- Evidence/confidence metadata -> keep in the OKF, not the customer narrative.

## Section openings after the Executive Summary

Each major section should begin with 2–4 cohesive paragraphs that naturally
cover:

- what the architectural area is;
- why it matters;
- how the customer benefits;
- any material concern supported by evidence;
- any future direction or active transition.

Do not turn these into a repetitive five-label checklist.

## Direct narrative

Avoid:

> This chapter describes the integration landscape.

Prefer:

> Information reaches the analytical environment through several ingestion
> patterns and is consolidated through shared processing layers before being
> delivered to purpose-specific products.

Avoid:

> This section presents the architecture overview.

Prefer:

> The architecture should be considered as a whole, from source domains through
> integration and processing to the shared analytical foundation and the
> specialised products built around it.

## Concerns and future direction

A baseline may contain important concerns, but only when the source supports
them.

Use these distinctions:

- **Confirmed issue:** source material establishes an actual problem.
- **Material dependency:** failure would have significant consequence, but no failure is asserted.
- **Transition concern:** temporary complexity may become permanent without clear exit criteria.
- **Validation point:** current understanding is incomplete.
- **Future direction:** a target or evolution is already known.

Do not collapse these into "gaps".

## Points to Validate

Keep the customer list short. A question belongs here when a different answer
could materially change the later assessment.

Typical domains:

- ownership and service expectations;
- sensitive/public data boundaries;
- transition exit criteria;
- source precedence during migration;
- retention/immutability;
- batch windows and operational ownership;
- target-state assumptions.

## Versioning

Update:

- YAML `artifact.report_version`;
- `dates.last_updated`;
- YAML `change_log`;
- Appendix B.

Keep `artifact.schema_version` unchanged unless the template/structure changes.

## Quality checks

Before downstream generation:

- YAML frontmatter parses;
- required sections exist and are ordered;
- current report version exists in the change log;
- no meta-document section openings;
- no unsupported findings;
- terminology is consistent;
- validation points are not written as defects.
