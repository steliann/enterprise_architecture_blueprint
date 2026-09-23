# Customer-Facing Architecture Assessment Word Guide

## Purpose

The Word assessment is the polished customer-facing expression of the validated
Architecture Assessment / Review OKF.

It is an architecture guidance document for architects and technical leads. It
must be technically useful without becoming an implementation runbook or a
commercial product proposal.

## Source of truth

Use the validated Assessment / Review OKF as the authoritative assessment source.
Use the Architecture Blueprint to verify context and readable names.

If Word would introduce a new gap, change priority, alter a recommendation or
reclassify a finding, update the Assessment OKF first.

## Customer-facing framing

The opening should make clear that:

- the assessment evaluates fitness against required architecture outcomes;
- it considers the current Qlik/Talend estate and potential future capabilities
  without assuming that any single product is the answer;
- it evaluates architecture mechanics such as movement, transformation,
  persistence, analytical serving, trust and operations;
- recommendations are architecture-first;
- guidance explains what adjustment would mean for the technical team but does
  not replace detailed design/delivery engineering;
- Candidate findings remain subject to customer validation.

Avoid direct references to internal OKF mechanics in the narrative unless needed
for document-status traceability.

## Recommended report structure

1. Cover
2. About this architecture assessment
3. Scope and evidence rule
4. Executive assessment
5. Priority discussion areas
6. Assessment approach and classification
7. Optional "How the assessment has evolved" summary for later editions
8. Findings / design topics and recommendations at a glance
9. Detailed architecture findings, validation/design topics and recommended responses
10. Cross-gap architecture themes
11. Cross-gap operational themes, when material
12. Aggregated architecture conclusions
13. Assessment disposition
14. Document status

## Executive assessment

The executive section should state:

- what is already strong/reusable;
- what architectural pressures are material;
- what the most important decisions are;
- what is not yet established;
- concise architecture-direction statements for the high-priority findings.

Do not make the executive section a list of Qlik capabilities.

For major recommendations, the reader should be able to extract a one-sentence
"gist", such as:

> Define persistence by lifecycle and data class rather than assuming a permanent
> relational layer at every stage.

or

> Move appropriate set-based warehouse transformation into the analytical
> platform and retain Talend primarily for orchestration where that is the more
> efficient pattern.

## Detailed finding block

### Assessment classification and architecture evidence

Start each detailed topic by making the classification visible: **Candidate/Active
Gap** or **Validation/Design Topic**.

Then use:

- **Architecture evidence / current condition** — concise, evidence-supported current state, including the
  architectural purpose of an existing mechanism when known.
- **Architecture gap** — solution-independent material mismatch **only when the
  evidence supports a gap**.
- **Impact if not addressed** — architecture/operational consequences for actual
  gaps.

For validation/design topics, do not invent an impact statement merely to make
the section look like a gap. Explain instead what decision remains open.

### Recommendation

Use this order:

#### Recommended direction

State the target architecture principle first.

#### Practical implications

Explain what changes for the current estate/team. Normally 2–4 substantive
paragraphs for major findings and less for secondary findings.

This may identify affected job classes, data layers, dataset types, runtime
patterns, quality/control workflows or lifecycle practices. It should indicate
what representative proof/assessment would be sensible without listing every
implementation step.

#### Options and trade-offs / key considerations

Capture credible options and the important decision factors. Use bullets or a
compact table when they improve exact comparison. Preserve the purpose of current
mechanisms where evidence shows why they exist.

#### Validation and acceptance

State the high-level evidence that would justify the architecture decision. This
can include representative workload comparison, correctness/reconciliation,
failure/recovery behaviour, service visibility, consumer acceptance or total
operational/cost evidence.

Do not write a detailed test script. Product deployment by itself is not
acceptance.

#### Optional finding-specific guidance

Use only when the finding benefits from it, for example:

- **Indicative persistence guidance** — transient, persistent staging, curated,
  static/reference, snapshot, exchange patterns;
- **Platform options to keep open during assessment** — current platform, cloud
  analytical platform, object/open storage, hybrid;
- **Transformation-placement categories** — Talend processing, pushdown/native,
  transient, managed target-platform transformation.

Do not force the same optional table into every finding.

#### Qlik/Talend role

Explain product fit after the architecture direction. It is acceptable to say
that the primary decision belongs to AWS, Snowflake, Databricks, security,
information governance or another domain, with Qlik/Talend acting as an enabler.

Do not use entitlement/licence labels as headings in the customer report.

#### Expected benefits

Use the standard benefit model where relevant:

- Reliability & Risk
- Operational Efficiency
- Performance & Scalability
- Agility & Time to Value
- Governance & Architectural Sustainability

Benefits must follow from the architecture change, not from generic product
claims.

## Persistence and static/reference data

When material to the customer architecture, explicitly discuss:

- source/raw landing;
- transient processing state;
- persistent staging/reconciliation;
- curated/warehouse persistence;
- presentation/marts;
- static/reference/master data;
- historical snapshots/retained extracts;
- exchange/research/TRE datasets;
- advanced analytics/ML/LLM access patterns.

Do not treat this as a "which database" question. Explain why in-memory,
temporary/transient database structures, relational persistence, object storage
/ Parquet/open formats and analytical platforms fit different lifecycle roles.

For static/reference datasets, address versioning/effective dating, historical
reproducibility, retention and authoritative ownership when the source supports
those concerns.

## Platform fitness

Do not conclude "replace Aurora/current database with Snowflake/Databricks/etc."
without the workload/persistence reasoning.

The report should normally state that:

- some current platform roles may remain valid;
- analytical-platform choice follows from workload and persistence needs;
- representative workloads should be assessed/proved before broad migration;
- migration can be staged/coexistent and reconciled;
- Qlik/Talend can provide integration, orchestration, replication/CDC or managed
  transformation where appropriate after the platform direction is selected.

## Guidance versus implementation

The report should indicate:

- what pattern should change;
- what the team would need to review/adjust;
- the main options and decision factors;
- the likely progressive adoption shape.

It should not define:

- detailed configurations;
- exact component values;
- sizing;
- code changes;
- job-by-job migration steps;
- production cutover runbooks.

Mention the detailed-design/delivery boundary in the opening or disposition; do
not repeat disclaimers in every recommendation.

## Commercial-tone controls

Avoid:

- leading with QTC product features;
- "expanded entitlement" headings;
- "QTC-led roadmap";
- implying that retaining the current architecture is a failure to adopt Qlik;
- product-feature inventories embedded in every recommendation.

Prefer:

- architecture principle;
- practical implications;
- measured fitness;
- coexistence and controlled migration;
- preserve/optimise/change/retire distinctions;
- Qlik/Talend implementation fit after the architecture case.

## Cross-gap themes and aggregated conclusions

Cross-gap themes synthesize recurring pressure; they do not add new findings.

Aggregated conclusions should be architecture statements first. A final section
may then explain how Qlik/Talend supports those target properties across the
portfolio.

## Document status and traceability

Show at least:

- report version/date/status;
- source Blueprint version;
- source Assessment / Review OKF version.

The customer report can omit internal GAP/REC IDs from narrative headings when a
cleaner customer style is preferred, but retain sufficient internal mapping in
source metadata or a traceability section to prove one-to-one derivation.

## Visual composition

Follow `styles/word-style.md`.

Keep the existing visual language:

- strong green section headings;
- concise metadata bands;
- readable tables;
- generous whitespace;
- clear finding/recommendation hierarchy;
- limited callouts used for genuine emphasis.

Do not squeeze detailed technical tables onto pages at unreadable font sizes.

## DOCX QA gate

Before delivery:

1. render the DOCX to PNG pages using the canonical DOCX renderer;
2. inspect every page at 100% zoom;
3. correct clipping, overflow, broken tables, headers/footers and bad page breaks;
4. re-render after every layout-sensitive correction;
5. deliver only the final DOCX unless another format is explicitly requested.

## How the assessment has evolved

For a later edition of a report already shared with the customer, normally add a
short section explaining how the assessment changed. A compact two-column table
works well:

| Earlier discussion area | Refinement in this edition |
|---|---|
| <Area> | <Why evidence changed the classification, scope or recommendation> |

Use this to show continuity without defending outdated conclusions. It is valid
for an earlier gap to become a validation/design topic. Explain that the lower
gap count reflects more precise classification when that is the case.

## Evidence and decision roadmap

Where useful for a technical-lead audience, close with a compact roadmap of the
architecture decisions/evidence to obtain next. Keep it as guidance: decide what
to measure/validate and in what logical order, not a project plan with task-level
steps.
