# Architecture Assessment / Review OKF Guide

## Purpose

The Assessment / Review OKF is the authoritative structured record of the
architecture fitness assessment. It sits downstream of the Architecture
Blueprint and upstream of the customer-facing Word assessment.

It must be detailed enough to preserve evidence, classification, reasoning and
traceability without forcing all internal detail into the customer document.

## Source precedence

When refreshing an assessment:

1. refresh the Blueprint first if new evidence changes current-state facts;
2. use the refreshed Blueprint as the primary architecture baseline;
3. use customer transcripts/telemetry/documents as supporting assessment evidence;
4. preserve conflicts or uncertainty rather than silently selecting a convenient
   interpretation.

If a customer validation session proves that an earlier gap was based on an
incorrect understanding, reclassify/supersede/withdraw it in the OKF. Do not keep
it active merely to preserve report numbering or narrative continuity.

## Required assessment distinctions

Keep four classes separate:

### Coverage finding

Information is incomplete, weakly traced or inconsistent. It may affect
assessment confidence but is not itself a defect.

### Validation item / design topic

The question matters, but the evidence does not establish a defect or preferred
implementation. Record exactly what evidence would permit gap classification or
a design decision. It may still carry a conditional recommendation and option
comparison.

### Candidate gap

Expected condition, current condition and material mismatch are sufficiently
evidenced to state a gap, but customer/design confirmation remains.

### Active gap

The mismatch has been confirmed and should drive governed remediation or a
formal architecture decision.

## Gap record requirements

Each GAP should contain or expose:

- ID and title;
- assessment lens/category;
- state;
- confidence;
- priority;
- horizon;
- expected architecture condition;
- architecture context/current condition;
- material gap statement;
- impact if not addressed;
- linked recommendation;
- high-level validation/acceptance evidence;
- traceability to Blueprint elements/evidence;
- customer validation status/questions where useful.

The gap statement must be solution-independent. Do not write "customer does not
use QTC CDC" as a gap. Write the architectural mismatch, for example that source
acquisition and transformation are unnecessarily concentrated in one peak
window when eligible sources can be decoupled.

## Recommendation record requirements

Each recommendation should contain or expose:

- ID/title and linked GAP(s);
- recommended architectural direction;
- practical implications for the current architecture/team;
- options and trade-offs / key considerations;
- validation and acceptance criteria at architecture level;
- Qlik/Talend role;
- adjacent platform/domain role where relevant;
- expected benefits;
- horizon/priority alignment;
- acceptance/validation information when appropriate;
- traceability.

### Recommended direction

State what architecture property should change. Do not name a product unless the
product is already an accepted architectural constraint/decision.

### Practical implications

Explain the types of assets and practices affected: jobs, layers, datasets,
persistence, orchestration, runtime profiles, quality workflows, lifecycle
controls, etc.

This should answer "what would this mean for the team?" without becoming a
step-by-step implementation procedure.

### Options and trade-offs / key considerations

Record credible alternatives and the decision factors that materially affect the
outcome. Prefer a small number of consequential factors over a generic checklist.
Explicitly preserve the architectural purpose of existing mechanisms when that
purpose is supported by evidence.

### Validation and acceptance

State what evidence would justify selecting the option: representative workload
comparison, failure/recovery observation, correctness/reconciliation result,
consumer validation, service visibility or cost/operational evidence as relevant.
Keep this at architecture guidance level; do not write a delivery test script.

### Qlik/Talend role

Map the architectural direction to current Talend, QTC or other Qlik capabilities
only after the direction is established. It is valid for the primary decision to
sit in an adjacent platform/domain.

Entitlement/licence information can be metadata, but must not determine gap
classification or architecture recommendation.

## Data-placement and persistence finding pattern

When the current design implicitly uses the same persistence mechanism at every
stage, consider a dedicated architecture finding rather than hiding the issue
inside the warehouse-platform finding.

The expected condition is normally that persistence/processing is selected
intentionally by lifecycle role and data characteristics.

The review should distinguish, where evidenced:

- transient intermediate state;
- persistent/replayable staging;
- curated analytical state;
- presentation/mart state;
- static/reference/master data;
- historical snapshots/retained history;
- exchange or research packages;
- ML/LLM/advanced-analytics datasets.

Do not assert that Parquet/object storage or a database is universally better.
Use restartability, auditability, versioning, change frequency, query/concurrency,
retention, schema evolution, portability, security and cost/operations as the
main decision dimensions.

## Transformation-placement finding pattern

Where source and target layers are co-located, determine whether the architecture
has an explicit rule for processing location.

The recommendation should distinguish:

- Talend/component-driven processing;
- set-based database/target-native processing;
- transient temporary processing;
- managed target-platform transformations.

The durable output should be an engineering/architecture principle, not simply a
list of jobs to rewrite.

## Platform-fitness finding pattern

A platform-fitness gap is the absence of a validated target-state decision or a
material mismatch between workload needs and platform characteristics — not the
mere fact that a newer platform exists.

The recommendation should keep open:

- retain current platform for all/some roles;
- move selected workloads;
- adopt a new analytical platform;
- use object/open storage for specific classes;
- hybrid architecture.

Evaluate after persistence and workload classes are understood.

## Existing investment rule

Explicitly identify what remains valid and should be preserved. Do not recommend
rebuilding governance, DQ, lineage, business rules or orchestration merely to
move them under a newer product.

## Technical depth rule

For major findings include enough content that a technical lead can see:

- what pattern changes;
- which assets are affected;
- what type of proof/assessment would be sensible;
- the principal decision factors;
- the likely progressive adoption shape.

Stop before detailed solution design, sizing, configuration, runbooks or
component-by-component implementation.

## Cross-gap themes

Create a cross-gap theme only when it synthesizes multiple independent findings.
Do not use themes to introduce new gaps.

Useful theme types include:

- intentional data placement and processing;
- reducing peak-window concentration;
- preserving governance investment;
- making transition/retirement criteria explicit;
- separating business-control decisions from technical enforcement.

## Aggregated conclusions

Aggregated conclusions are executive synthesis, not additional GAP records.
They should state architecture properties or decisions, for example:

- establish an intentional data-placement and processing model;
- decouple workload growth from the critical batch window;
- make the analytical-platform decision through measured fitness;
- extend trust/control without replacing established governance.

Only after these are stated should the assessment summarize how Qlik/Talend can
support them.

## Customer feedback handling

When a validation session provides new evidence:

- current-state fact changed -> update Blueprint first, then assessment;
- concern proven not to exist -> withdraw/reclassify GAP;
- concern remains but evidence weak -> VAL item;
- mismatch confirmed -> Candidate may become Active;
- recommendation remains useful but scope changes -> update REC and traceability;
- new material architectural question -> add GAP/VAL only when the evidence rule
  is met.

Always update change history.

## Later-edition refinement

When refreshing a report already shared with a customer, preserve enough of the
original discussion sequence that the new edition reads as an evolution. Add an
explicit refinement/evolution summary when changes are material.

For each earlier discussion area, the refreshed Assessment OKF may record that it:

- remains a Candidate/Active Gap;
- is narrowed or made conditional;
- becomes a Validation/Design Topic because evidence does not prove a defect;
- is withdrawn because the current-state understanding was wrong;
- is split because new evidence shows distinct architecture questions.

Do not infer that a lower gap count means the architecture improved. It may mean
the assessment became more precise.
