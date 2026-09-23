# Generation Guide

## A. Establish the current recommendation portfolio

1. Read `architecture-blueprint-review.md` for declared review version and recommendation count.
2. Read `recommendations/index.md` to establish the intended active order and sequencing.
3. Read every `REC-*.md` file.
4. Ignore validation items unless they have been promoted to a recommendation.
5. Flag discrepancies between declared counts, index membership and physical files.

Capture for every recommendation:
- ID and title;
- state/status;
- horizon;
- impact;
- category;
- confidence;
- originating gap(s);
- affected elements;
- recommendation basis and architecture context;
- target architecture advice;
- expected benefits;
- customer validation prerequisites;
- traceability.

## B. Refresh or establish business objectives

### Refresh path

Retain an existing BO when all are true:
- its intended business outcome remains valid;
- its primary business use case(s) remain the same in meaning;
- changes are editorial, clarifying, or measure refinements rather than a new outcome.

Create a new BO when:
- a new material business outcome appears;
- the underlying use case is materially split/merged/replaced;
- acceptance semantics materially change.

Do not renumber existing BOs to make the sequence contiguous.

### First-generation path

Group use cases only when they express one durable business outcome. Prefer one BO per primary use case unless the source evidence clearly calls for consolidation.

Business success measures must be observable outcomes. If numeric thresholds are unknown, state the measurable condition and leave the quantitative threshold to be agreed.

## C. Convert recommendations into technical objectives

For each current recommendation answer:

1. **What future technical condition must be true?** This becomes the Objective.
2. **Why does it matter architecturally?** Summarize as Architecture Rationale.
3. **How will we know the condition is achieved?** Convert acceptance criteria, prerequisites and expected architecture behaviour into Technical Success Measures.
4. **Which business outcomes does it materially enable?** Populate `business_objectives`.
5. **What sequencing signal applies?** Inherit horizon.
6. **How material is it?** Inherit impact.
7. **What domain does it belong to?** Normally inherit category; normalize only when the CSP taxonomy requires it and record the rationale.

### Objective formulation

Good TOs are technology-aware when technology is integral to the recommendation, but they still describe a capability/outcome rather than an activity.

Good:
> Provide workload-adaptive runtime capacity that can satisfy distinct processing windows without customer-owned infrastructure switching.

Weak:
> Migrate to Dynamic Engine.

The second is an action. The first is the enduring outcome; migration can be one route to it.

## D. Translate recommendation acceptance into success measures

Technical measures should cover the material architecture assertions. Typical dimensions include:
- capability availability;
- reliability/recovery;
- performance/capacity;
- governance/traceability;
- lifecycle/retirement controls;
- reconciliation/completeness;
- compatibility/prerequisite validation;
- consumer-visible service state;
- operational evidence.

Do not invent numeric values. Preserve “to be measured/agreed” where the source does not provide a threshold.

## E. Preserve planning neutrality

Default fields for a newly proposed objective:
- `objective_state: proposed`
- `planning_state: not_planned`
- owner: To be agreed
- baseline: To be measured/established
- target date: To be agreed
- acceptance evidence: To be defined before execution

Do not convert architecture priority into a committed customer delivery date.

## F. Generate companion reporting

The portfolio document must provide:
- purpose and relationship model;
- BO roll-up;
- TO roll-up with recommendation IDs and horizons;
- refresh disposition when prior CSP exists;
- planning interpretation;
- required enrichment before commitment.

The validation report must provide:
- source review version;
- BO/TO counts;
- recommendation coverage;
- horizon distribution;
- preserved/new/superseded IDs when previous CSP is supplied;
- errors and warnings.
