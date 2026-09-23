---
name: architecture-blueprint-customer-reporting
version: "2.0.0"
description: >
  Create customer-facing Architecture Blueprint baseline reports and architecture
  assessments from an Architecture Blueprint OKF. Supports a structured
  Architecture Assessment/Review OKF as the authoritative assessment source and
  polished customer-facing Word reports derived from it, while preserving the
  original blueprint-baseline reporting workflow.
---

# Architecture Blueprint Customer Reporting

## Purpose

Use this skill for two related but deliberately separate workflows:

1. **Blueprint reporting** — turn an Architecture Blueprint OKF into a concise,
   customer-facing architecture baseline for validation.
2. **Architecture assessment** — assess a sufficiently mature Architecture
   Blueprint, create or refresh an Architecture Assessment / Review OKF, and
   produce a customer-facing Word assessment from that authoritative review.

Do not blur the two artifacts. The Blueprint describes the architecture as
understood. The Assessment evaluates fitness and records findings,
recommendations and validation items.

## Supported workflows

### Blueprint baseline

- Blueprint OKF -> Markdown baseline
- Blueprint OKF -> Markdown + Word + PowerPoint baseline pack
- Existing baseline Markdown -> validate -> Word and/or PowerPoint
- Existing baseline Markdown -> structure validation only

### Architecture assessment

- Blueprint OKF -> Architecture Assessment / Review OKF only
- Blueprint OKF -> Assessment OKF + customer-facing Word assessment
- Existing Assessment / Review OKF -> refresh from a newer Blueprint and/or
  customer evidence -> Word assessment
- Existing Assessment / Review OKF -> Word assessment only
- Existing Assessment / Review OKF -> structural/content validation only

If an existing Assessment / Review OKF is supplied, **preserve its structure,
record IDs and decision history** unless the user explicitly asks to migrate to a
new structure. The templates in this skill are canonical guidance for greenfield
assessment artifacts, not a reason to rewrite a valid existing OKF.

## Source grounding

Use only information supported by the engagement source set unless the user
explicitly requests external research.

Typical sources:

- Architecture Blueprint / OKF records;
- customer interviews, workshop transcripts and validation sessions;
- telemetry or operational evidence supplied for the review;
- customer-shared documentation;
- product/technology documentation already supplied for the engagement;
- external/public research only when explicitly requested.

Preserve source terminology. Do not silently repair, reconcile or replace
customer-specific facts using generic architecture knowledge.

If customer feedback invalidates an earlier assumption, update the Blueprint or
Assessment accordingly. Do not keep an obsolete finding merely because it
appeared in an earlier report. Preserve decision history through versioning,
status/supersession or changelog entries where appropriate.

# Part A — Blueprint Baseline Reporting

The customer baseline is an **architecture baseline, not an assessment**.

It should establish:

- business outcomes and use cases;
- architecture structure and principal flows;
- data products and consumers;
- architecture-shaping decisions;
- data quality, trust and governance;
- operations and resilience;
- current transitions;
- a limited set of material validation points.

Unknown is not a defect. Do not convert open questions into gaps.

For baseline generation use:

- `templates/architecture-blueprint-report-template.md`
- `guidance/markdown-report-guide.md`
- `guidance/word-report-guide.md`
- `guidance/powerpoint-workshop-guide.md`
- `schemas/report-structure.yaml`
- `scripts/validate_report.py`

The existing baseline editorial and validation rules remain unchanged.

# Part B — Architecture Assessment / Review

## Assessment premise

The assessment starts from the architecture outcomes the customer needs and asks
whether the current or intended implementation is fit for those outcomes.

A gap exists only when all three can be stated with evidence:

1. **Expected architecture condition** — the required outcome, control, property
   or target behaviour.
2. **Current architecture condition** — what the architecture currently does or
   intends to do, supported by evidence.
3. **Material mismatch** — why the current condition does not sufficiently meet
   the expected condition.

A missing feature, undocumented detail, unanswered discovery question,
commercial opportunity or availability of a newer product is **not** a gap by
itself.

Use these states consistently:

- **Coverage finding** — information is incomplete, weakly traced or inconsistent.
- **Validation item / design topic** — the question matters, but current evidence
  does not establish a defect or preferred implementation. It can still carry a
  conditional recommendation or option comparison.
- **Candidate gap** — evidence supports a material mismatch; customer/design
  confirmation remains.
- **Active gap** — the material mismatch is confirmed.

Unknown is not automatically a gap.

A customer-relevant architecture topic may remain in the assessment even when it
is not a gap. In that case label it clearly as a **validation/design topic** and
provide a conditional comparison or guidance. Do not promote it to Candidate only
to keep the report structure symmetrical.

When a later report edition refines an earlier assessment, preserve the
recognisable discussion sequence where useful, but explicitly show how the
interpretation changed. A lower Candidate-gap count after deeper discovery is a
valid outcome and should be explained as improved classification, not hidden.

## Architecture-first recommendation rule

Every recommendation must be **architecture-first and product-second**.

The core order is:

1. **Recommended direction** — state the target architecture principle or
   condition without assuming a specific product.
2. **Practical implications** — explain what the change would mean for the
   current jobs, datasets, layers, runtime, controls or engineering practice.
3. **Options and trade-offs / key considerations** — explain credible
   alternatives, material trade-offs and the evidence that should guide the
   decision.
4. **Validation and acceptance** — state the evidence that would justify the
   decision at architecture level; use representative tests/observations, not a
   delivery runbook.
5. **Qlik/Talend role** — only then explain how current Talend, QTC or another
   Qlik capability can implement or enable the selected direction.
6. **Expected benefits** — connect the direction to measurable architecture
   value without unsupported product-value claims.

Do not organise the customer narrative around `Current Entitlement`, `Expanded
Entitlement`, licence tier or product availability. Entitlement/response-path
metadata may remain in the Assessment OKF for internal traceability, but it must
not become the reasoning structure of the report.

Avoid language such as:

- "QTC-led target-state roadmap";
- "impact if the QTC opportunity is not evaluated";
- "expanded entitlement" as a recommendation heading;
- "replace with <product>" before architectural fitness is established.

Prefer:

- "target-state architecture roadmap";
- "risk of retaining the current pattern";
- "Qlik/Talend role";
- "platform options to keep open during assessment";
- "recommended architectural direction".

## Guidance depth for a technical-lead audience

The assessment is guidance, not a delivery runbook.

For major findings, provide enough technical depth that the technical lead can
understand **what the team would need to review or adjust**, without specifying
every implementation step.

Normally include:

- which workload/data/service patterns are affected;
- what engineering principle would change;
- the main categories of technical option;
- why an existing mechanism may have been introduced and which purpose must be
  preserved (for example replay evidence, shared checkpoint, isolation boundary
  or last-good publication);
- what should be compared or proven on representative cases;
- the decision considerations and trade-offs;
- high-level validation/acceptance evidence for the chosen option;
- the likely adoption shape (for example prove on representative workloads,
  apply progressively, coexist/reconcile, then retire superseded mechanisms).

Do **not** turn the assessment into:

- detailed component configuration;
- sizing instructions;
- exact migration waves;
- code or job-by-job implementation instructions;
- production cutover runbooks;
- a substitute for detailed design or PS/delivery engineering.

A useful test is: the technical lead should understand the intended adjustment
and the engineering conversation it creates, but should still need detailed
design before implementation.

## Data placement, persistence and processing guidance

When the blueprint shows multiple data lifecycle stages or the customer asks
whether every ETL stage should be a database layer, the assessment must evaluate
**data placement and persistence as an architecture decision in its own right**.
Do not reduce the question to one database product versus another.

Assess, when relevant:

- source/raw landing;
- transient working/intermediate state;
- persistent staging/reconciliation boundaries;
- curated/core analytical data;
- presentation/data-mart structures;
- consumer-facing access patterns;
- static/reference/master data;
- historical snapshots and retained source history;
- exchange/export/TRE/research datasets;
- data used for heavy analytics, ML/LLM or experimentation.

Keep the following mechanism classes open until requirements justify one:

- in-memory processing;
- temporary/transient database structures;
- persisted relational staging;
- analytical warehouse/lakehouse structures;
- object storage and open formats such as Parquet;
- materialized structures/views where justified;
- hybrid patterns.

For each class, the decision should be driven by characteristics such as
restart/replay requirements, audit/reconciliation needs, frequency of change,
versioning/effective dating, historical reproducibility, data volume,
concurrency, shared consumption, latency, schema evolution, retention, security,
portability and operational ownership.

Static/reference data must not be treated as an afterthought when it is material
to the architecture. HESA-like datasets, RDM/reference domains, geographic
reference data, retained finance extracts, formal snapshots and exchange
packages may require different persistence/lifecycle rules from transactional or
frequently changing analytical data.

## Transformation placement guidance

When transformations occur between co-located or same-platform layers, assess
whether Talend should remain the data-processing path or primarily orchestrate
processing executed by the data platform.

Distinguish at least:

- component/procedural/external processing that should remain in Talend;
- relational/set-based processing suitable for database or target-native
  execution;
- temporary/transient processing that does not require a permanent layer;
- managed analytical-platform transformation where a target platform is chosen.

The recommendation should establish a repeatable **transformation-placement
principle**, not merely suggest converting selected jobs.

## Platform-fitness guidance

Do not start with a predetermined replacement product.

For analytical-platform findings:

1. establish the data-placement/persistence principles first;
2. identify the workload classes that actually require analytical database
   capabilities;
3. compare retaining the current platform, moving selected workloads, or using a
   hybrid/open-storage model;
4. evaluate target technologies against workload, operations, governance,
   security, cost and ecosystem requirements;
5. describe Qlik/Talend as the integration/migration/operating layer only after
   the architecture direction is clear.

A current platform can remain appropriate for some roles even if it is not the
best target for every workload.

## Preserve useful existing investments

Recommendations should distinguish:

- what should be preserved;
- what should be optimised in the current estate;
- what should progressively change;
- what can be retired only after coexistence/reconciliation criteria are met.

Existing governance, quality, lineage, business rules, orchestration semantics,
operating knowledge and validated controls should not be recreated merely to
increase product adoption.

## Major recommendation clarity

For each high-priority or structurally important finding, the executive section
should contain a short architecture-direction statement — normally one sentence
that answers "what should UKRI/customer do differently?" without product
marketing.

Examples of the style:

- Move set-based warehouse transformations toward execution in the analytical
  platform and retain integration tooling primarily for orchestration where that
  is the more efficient pattern.
- Define persistence by data lifecycle and data class rather than assuming a
  permanent relational layer at every processing stage.
- Decide the long-term analytical platform through measured fitness rather than
  retaining or replacing the current platform by inertia.

## Assessment OKF as source of truth

The Architecture Assessment / Review OKF is authoritative for the assessment.
The Word report is derived from it.

The Assessment OKF should retain:

- review scope and lenses;
- evidence/coverage position;
- coverage findings where needed;
- validation items;
- candidate/active gaps;
- recommendations;
- priorities, confidence and horizon;
- response/technology-fit metadata when useful;
- benefits;
- traceability to Blueprint elements and evidence;
- cross-gap themes and aggregated conclusions when they are used in the report;
- version/change history.

Each detailed Word assessment topic must map to one authoritative GAP or VAL /
design-topic record. Each Word recommendation must map to an authoritative
recommendation record or recommendation section in the Assessment OKF. Word must
not invent additional gaps, design topics, recommendations or priorities.

Customer validation can cause a gap to be:

- confirmed/activated;
- downgraded to a validation item;
- corrected;
- superseded/withdrawn when the original condition was misunderstood.

Record that change in the Assessment OKF before regenerating Word.

For assessment generation use:

- `templates/architecture-assessment-okf-template.md`
- `guidance/assessment-okf-guide.md`
- `guidance/assessment-word-report-guide.md`
- `schemas/assessment-okf-structure.yaml`
- `scripts/validate_assessment.py`
- `styles/word-style.md`

## Assessment -> Word workflow

1. Inspect the complete Blueprint and the current Assessment / Review OKF if one
   exists.
2. Apply new customer evidence to the Blueprint first when it changes factual
   current-state architecture.
3. Refresh the Assessment OKF from the updated Blueprint/evidence.
4. Reclassify or remove findings invalidated by better evidence; do not preserve
   them for report continuity.
5. Validate the Assessment OKF.
6. Generate the Word report from the validated Assessment OKF using
   `guidance/assessment-word-report-guide.md`.
7. Render the DOCX to page images and inspect **every page at 100%**. Fix layout
   defects and re-render until clean.

## Word report narrative contract

The customer-facing assessment normally contains:

1. About this architecture assessment
2. Scope and evidence rule
3. Executive assessment and priority discussion areas
4. Assessment approach and classification
5. Optional "How the assessment has evolved" summary for later editions
6. Findings/design topics and recommendations at a glance
7. Detailed architecture findings, validation/design topics and recommended responses
8. Cross-gap architecture themes
9. Cross-gap operational themes when material
10. Aggregated architecture conclusions
11. Assessment disposition
12. Document status

The detailed assessment block should normally contain:

- assessment classification: Candidate/Active Gap or Validation/Design Topic
- architecture evidence / current condition
- architecture gap **only when a material mismatch is evidenced**
- impact if not addressed, for actual gaps
- recommended direction or conditional recommendation
- practical implications
- options and trade-offs / key considerations
- validation and acceptance
- optional finding-specific guidance/table when materially useful
- Qlik/Talend role
- expected benefits
- review references / traceability where appropriate

A design topic can therefore have a recommendation without being described as a
defect. Product adoption alone never counts as acceptance evidence.

Do not mechanically force an optional subsection into every finding. Use it only
when it improves the technical guidance.

## Customer-facing tone

The report can be produced by Qlik and still be an architecture assessment.

Use neutral, evidence-led language. The reader should be able to distinguish:

- architecture need;
- technical direction;
- implementation options;
- Qlik/Talend fit.

Avoid making product adoption the justification for the finding.

## Versioning

### Baseline report

- `artifact.schema_version` — template/schema version
- `artifact.report_version` — customer report version

### Assessment OKF

Maintain assessment artifact version, source Blueprint version and change history.
When customer feedback changes factual architecture first, the assessment should
reference the refreshed Blueprint version.

The Word assessment should show both the source Blueprint version and source
Assessment / Review version in document status or metadata.

## Output naming

Recommended names:

- `<customer>-architecture-blueprint-report-v<version>.md`
- `<customer>-architecture-blueprint-v<version>.docx`
- `<customer>-architecture-blueprint-workshop-v<version>.pptx`
- `<customer>-architecture-blueprint-review-okf-v<version>.zip` or `.md`
- `<customer>-architecture-assessment-v<version>.docx`

Use a filesystem-safe customer name.

## Quality bar

A strong assessment should:

- be traceable to the Blueprint and customer evidence;
- separate unknowns from material mismatches;
- state findings in solution-independent architecture language;
- provide enough practical guidance for a technical lead to understand the
  adjustment without becoming an implementation runbook;
- treat data placement/persistence and static/reference data explicitly when
  material;
- keep analytical-platform options open until fitness is assessed;
- preserve useful current investments and controls;
- explain Qlik/Talend fit after the architecture direction;
- provide concise executive direction for the most important findings;
- remain internally consistent between the Assessment OKF and Word report;
- render cleanly and professionally in Word.
