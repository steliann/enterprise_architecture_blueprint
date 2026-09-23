---
# ---- Identity ----
id: SPX-ADR-001
yaml_version: 1
title: "Use Qlik Cloud Catalog and Data Quality for Initial Profiling and Trust Score Baseline"
status: Proposed
date: 2026-05-26
review_by: 2026-11-26

# ---- Ownership ----
decision_owner: "Andrew Younge / Enterprise Architect"
contributors:
  - "Data Platform Lead, SPX"
  - "Data Governance Manager, SPX"
  - "Qlik Customer Success Engineer"

# ---- Classification ----
decision_type: "Architecture"
architecture_domain: Data
decision_scope: Customer
decision_level: Tactical
confidence: High

# ---- Technology scope ----
technology_scope:
  qlik:
    - "Qlik Cloud Catalog"
    - "Qlik Cloud Data Quality"
  talend:
    - "Talend Studio"
  third_party:
    - "Microsoft SQL Server"
    - "Snowflake"

# ---- Relationships ----
related_patterns:
  - "QDQ-001 — DQ Baseline Assessment and Trust Score (../knowledge-units/qdq-001-dq-baseline-assessment-and-trust-score.md)"
related_adrs: null
impacted_architecture_views:
  - "Governance View"
  - "Data Flow View"
  - "Operational View"
related_assets:
  - "SPX Data Quality Discovery Workshop, 2026-05-14"
supersedes: null
superseded_by: null

# ---- AI assistance ----
used_ai_to_prepare: true
ai_solutions_used:
  - "Claude"

# ---- Tags ----
tags:
  - "data-quality"
  - "profiling"
  - "catalog"
  - "trust-score"
---

# SPX-ADR-001 — Use Qlik Cloud Catalog and Data Quality for Initial Profiling and Trust Score Baseline

## Context

SPX is consolidating eleven operational reporting domains onto Qlik Cloud over the next three quarters, and the migration has surfaced a governance gap that predates it. Data quality at SPX is currently assessed inside individual reporting applications, so the same customer master attribute can be judged acceptable in one domain and unusable in another, with no shared record of which assessment is authoritative. The programme cannot sequence remediation work without an agreed baseline, and the stewardship function that SPX plans to stand up in Q3 has nothing to steward until one exists.

The decision covers where the initial profiling of migrated datasets happens and where the resulting quality baseline is recorded. In scope are the roughly 340 datasets landing in Qlik Cloud from SQL Server and Snowflake during migration, the metadata surface that governance and stewardship users will work from, and the boundary between assessment and remediation. Operational remediation itself, including failed-row persistence and survivorship logic, is a separate decision and is not settled here. SPX has Talend Studio in place for existing integration work, which makes it a genuine candidate for profiling as well as remediation.

Leaving this ambiguous carries a specific cost rather than a general one. Without a single baseline, remediation priority becomes a negotiation between domain owners, each armed with their own numbers, and the stewardship team inherits a backlog it cannot defend. Establishing the baseline after remediation has started is worse still: there is then no measurable before-state, and the programme loses the ability to show whether its quality investment worked.

## Decision

We will use Qlik Cloud Catalog together with Qlik Cloud Data Quality to profile all datasets migrated into Qlik Cloud and to hold the authoritative initial quality baseline and Trust Score for each one. The catalog-held baseline is the single reference point for remediation prioritisation and for stewardship reporting during the migration programme. Talend Studio profiling is explicitly excluded from the baseline role, and dataset-level or application-level quality assessments are excluded from being treated as authoritative, though they may continue to inform domain-level work.

## Decision Drivers

- The stewardship function starting in Q3 needs one defensible baseline it can prioritise against, not eleven domain-owned assessments that disagree.
- Remediation sequencing across 340 datasets must be justifiable to the programme board, which requires a comparable quality measure applied uniformly rather than per-domain judgement.
- Baseline measurement has to be in place before remediation begins, or the programme loses its before-state and cannot evidence improvement.
- Governance and stewardship users at SPX are business-side rather than developer-side, so the baseline has to be visible in a metadata surface they can reach without an integration toolchain.
- Migration timelines allow no room for a bespoke profiling build; profiling must follow dataset arrival in Qlik Cloud automatically rather than as a scheduled parallel workstream.
- SPX's existing Talend Studio footprint makes tool choice a real decision rather than a default, and the boundary between assessment and remediation tooling needs to be stated before both teams start work.
- Quality outcomes must carry lineage back to the source system to survive audit, which rules out any assessment held outside the platform's metadata model.

## Options Considered

### Option 1 — Qlik Cloud Catalog and Qlik Cloud Data Quality as the baseline

Profile datasets in place as they land in Qlik Cloud, using Qlik Cloud Data Quality to generate dataset-level quality measures and Qlik Cloud Catalog to hold the resulting Trust Score, profile statistics, and metadata alongside the dataset itself. Governance and stewardship users work directly from the catalog, and the baseline lives in the same metadata surface as the lineage and ownership information it needs to be read against.

Remediation remains a separate concern. This option decides only where assessment happens and where its output is authoritative, leaving the operational remediation path to be settled independently.

**Benefits**

- Baseline and dataset share one metadata surface, so quality, lineage, and ownership are read together rather than reconciled.
- Business-side governance and stewardship users reach the baseline without needing access to an integration toolchain.
- Profiling follows dataset arrival in the platform, so coverage tracks migration progress without a parallel scheduling workstream.
- Trust Score gives the programme board one comparable measure across all 340 datasets.
- No bespoke build, so the baseline is available inside the migration timeline.

**Limitations**

- Profiling depth is bounded by what the platform capability offers; complex cross-dataset rules are not expressible here.
- Creates a dependency on Qlik Cloud capability roadmap for any future assessment requirement.
- The baseline is only as current as the last profiling run, so freshness needs active monitoring rather than being implicit.
- Trust Score is a composite measure, and domain owners will need help interpreting it before they accept prioritisation based on it.

**Fit assessment**

Selected. It is the only option that puts the baseline in the metadata surface the stewardship function will actually use, and the only one deliverable inside the migration timeline without a parallel build. Its profiling-depth limitation is acceptable because the baseline's purpose is comparable triage across many datasets, not deep rule evaluation on a few.

### Option 2 — Talend Studio profiling into a governed quality store

Use Talend Studio's profiling capability against the source systems and migrated datasets, persisting profile results and quality measures into a governed store in Snowflake. Governance and stewardship users consume the baseline through a reporting layer built over that store.

SPX already runs Talend Studio for integration work, so the skills and licensing exist. The profiling capability is materially deeper than dataset-level scoring, and cross-dataset and cross-system rules are expressible.

**Benefits**

- Deeper profiling, including cross-dataset and cross-system rules the platform-native option cannot express.
- Reuses existing SPX Talend Studio skills and licensing.
- Quality results held in Snowflake are queryable by any downstream consumer, not only Qlik.
- The same tooling would later serve operational remediation, keeping assessment and remediation in one technology.

**Limitations**

- Requires building and owning a quality store, a reporting layer, and a scheduling regime before any baseline exists, which does not fit the migration timeline.
- Separates the quality baseline from the catalog metadata, so lineage and ownership must be joined manually to be read alongside quality.
- Puts the baseline behind a developer toolchain and a custom reporting layer, which the business-side stewardship function cannot self-serve.
- Adds a second orchestration surface to operate and monitor during migration, when platform operations capacity is already committed.

**Fit assessment**

Rejected, on architecture grounds rather than capability. Its profiling depth is genuinely superior, but the baseline's architectural role here is a shared, self-service reference point for triage, and this option places it behind a build and a toolchain that the intended users cannot reach. The depth advantage would matter for rule-based remediation, which is a different decision.

### Option 3 — Defer the baseline until the stewardship function is operating

Migrate datasets without establishing a quality baseline, and decide the profiling approach in Q3 once the stewardship function exists and can state its own requirements. Domain owners continue to assess quality within their applications in the interim.

**Benefits**

- Requirements would be stated by the team that will use the baseline, rather than inferred ahead of it.
- No tooling commitment before the stewardship operating model is settled.
- Removes a workstream from an already committed migration schedule.

**Limitations**

- Destroys the before-state: remediation would begin without a measurable baseline, so improvement cannot be evidenced.
- Leaves prioritisation as a negotiation between domain owners with incompatible numbers for the whole of migration.
- The stewardship function starts with an undefended backlog, which is the situation this decision exists to prevent.
- Retrofitting a baseline across 340 already-migrated datasets costs more than profiling them on arrival.

**Fit assessment**

Rejected. Deferral is the option that most damages the programme's ability to evidence its own outcome, and the interim state it preserves is precisely the problem being solved. The requirements argument does not hold either: the baseline's consumers are known well enough to proceed, and the catalog-held approach can be extended once stewardship states more specific needs.

## Decision Outcome

Selected option: Option 1 — Qlik Cloud Catalog and Qlik Cloud Data Quality as the baseline.

Option 1 satisfies the drivers that constrain this decision most tightly. It puts the baseline in the metadata surface where lineage and ownership already live, which is what makes it defensible in audit and readable by business-side stewardship users without an intermediary. It is also the only option that delivers baseline coverage in step with migration rather than after it, which preserves the before-state the programme needs to evidence improvement. The profiling-depth advantage of Option 2 is real, but it applies to rule-based remediation rather than to comparable triage across a large dataset population, so it does not bear on this decision's architectural role.

The decision holds only while three conditions remain true. First, that assessment and remediation stay architecturally separable, so choosing platform-native assessment does not constrain the remediation tooling decision still to be made. Second, that Trust Score remains a comparable measure across datasets of differing shape, which SPX should sample-verify on a representative set before the baseline is published to the programme board. Third, that profiling can be triggered on dataset arrival rather than only on a fixed schedule, since coverage tracking migration progress is a stated driver rather than a convenience.

Sequencing matters here. The baseline must be established on each dataset before any remediation touches it, which means profiling has to be part of the migration runbook for each domain rather than a follow-on activity.

## Knowledge Unit Alignment

### Supporting Knowledge Units

QDQ-001 — DQ Baseline Assessment and Trust Score supports the decision directly. It holds that the initial quality baseline should sit in the platform metadata surface alongside lineage and ownership, and that assessment tooling should be chosen separately from remediation tooling. Both positions are the substance of this decision.

### Conditional Support and Constraints

QDQ-001's guidance is scoped to populations where datasets are broadly comparable in shape. SPX's 340 datasets span operational reporting extracts and dimensional structures, which sits at the edge of that boundary. The condition is handled in Decision Outcome as a sample-verification requirement on Trust Score comparability, and in Implementation Implications as a gate before the baseline is published to the programme board.

### Contradictions or Exceptions

No contradiction. The decision follows QDQ-001's guidance and stays inside its stated boundaries, subject to the comparability condition above.

### Alignment Outcome

Conditionally aligned. The decision follows QDQ-001 and fits its boundaries, conditional on Trust Score comparability holding across the mixed dataset population, which is verified before publication rather than assumed.

## Architecture Impact

### Business

Quality prioritisation moves from domain-owned negotiation to one programme-level reference point, which changes how remediation scope is agreed and who can challenge it. Domain owners lose the ability to set their own quality thresholds for prioritisation purposes, and will need briefing on Trust Score interpretation before they are asked to accept sequencing based on it. The stewardship function due in Q3 inherits a defensible backlog rather than building one, but also inherits ownership of baseline currency.

### Data

Every migrated dataset gains profile statistics and a Trust Score held in the catalog alongside its lineage and ownership metadata, making quality readable in the same place as provenance. The baseline is a point-in-time measure and becomes stale as data changes, so refresh cadence becomes a data-lifecycle concern rather than a one-off migration activity. Source-system quality assessments in SQL Server and Snowflake are not migrated and are superseded for prioritisation purposes.

### Application

Profiling becomes a step in the per-domain migration runbook rather than a separate application, so no new component is introduced but the runbook gains a gate. Existing quality logic inside individual Qlik applications continues to run and is not authoritative, which creates a period where two numbers exist for the same attribute and the precedence has to be stated. The Talend Studio estate is untouched by this decision, keeping the remediation tooling choice genuinely open.

### Technology

No new runtime or infrastructure is introduced, since profiling executes within Qlik Cloud against datasets already landed there. Profiling load coincides with migration load on the same tenant, so tenant capacity during migration windows needs monitoring that it does not currently have. Access to the baseline follows existing Qlik Cloud identity and space permissions, which means stewardship users' space access has to be provisioned before the baseline is useful to them.

## Consequences

### Positive Consequences

- Creates one governed quality baseline visible through the catalog before any operational remediation is built, so improvement is measurable against a defensible before-state.
- Gives the programme board a single comparable measure across all 340 datasets, replacing eleven domain-specific assessments that could not be reconciled.
- Quality, lineage, and ownership are read from one metadata surface, so audit questions about provenance and quality are answered together.
- The Q3 stewardship function starts with a prioritised backlog it can defend rather than spending its first quarter building one.
- Baseline coverage tracks migration progress automatically, so coverage gaps surface as migration gaps rather than as a separate reporting exercise.
- Keeps the remediation tooling decision open, so the deeper Talend Studio profiling capability remains available where it actually applies.
- No bespoke build, so the baseline is delivered inside the migration timeline without drawing on committed platform operations capacity.

### Negative Consequences / Trade-offs

- Forgoes the cross-dataset and cross-system profiling rules Talend Studio could express, which means some quality dimensions will not be assessed at baseline at all.
- Creates a dependency on the Qlik Cloud Data Quality capability roadmap for any assessment requirement that emerges later, with no in-house fallback established.
- Domain owners lose local control over prioritisation thresholds, which is a governance gain but a real reduction in their autonomy and a likely source of friction in Q3.
- Introduces a period during which application-level quality logic and the catalog baseline both exist and disagree, requiring precedence to be stated and communicated.
- Baseline currency becomes an ongoing operational obligation; a stale Trust Score is worse than no Trust Score because it is trusted.
- Profiling load lands on the same tenant during migration windows, adding contention to a period already at capacity.
- Trust Score is composite and needs interpretation, so the baseline is less immediately legible to domain owners than the single-dimension measures they use today.

## Implementation Implications

- Profiling must be added as a gate in each domain's migration runbook, executed on dataset arrival and before any remediation touches the dataset.
- Trust Score comparability must be sample-verified across a representative spread of operational extracts and dimensional structures before the baseline is published to the programme board.
- Precedence between the catalog baseline and existing application-level quality logic has to be stated in writing and communicated to all eleven domain owners before prioritisation begins.
- Stewardship users' Qlik Cloud space access must be provisioned ahead of the Q3 function starting, not at the point they need it.
- Tenant capacity monitoring during migration windows needs to be in place before bulk profiling begins, since profiling and migration load coincide.
- Baseline refresh cadence must be defined per dataset domain, tied to change rate rather than applied uniformly.
- Trust Score interpretation guidance for domain owners should be produced before they are asked to accept prioritisation decisions based on it.
- The boundary with remediation must stay explicit in programme documentation, so this decision is not read as having settled the remediation tooling question.
- Datasets that fail to profile need a defined exception path rather than silently absent baselines, since an unprofiled dataset is invisible to prioritisation.
- Coverage reporting should show profiled versus migrated dataset counts per domain, so baseline gaps surface during migration rather than after it.

## Operational Implications

- Baseline currency is owned by the stewardship function from Q3, with an interim owner named in the programme for the period before it stands up.
- Profiling failures need alerting, since a silently unprofiled dataset drops out of prioritisation without anyone noticing.
- Trust Score drift on previously baselined datasets should be monitored, as drift is itself a quality signal and not only a refresh trigger.
- Tenant capacity during profiling windows needs monitoring against the migration schedule, with a defined action if contention affects migration throughput.
- Space and permission changes affecting stewardship access to the catalog must go through change control, since access loss silently disables the governance function.
- Baseline publication to the programme board needs a documented cadence and a named approver, so the numbers reaching the board are attributable.
- The decision's review date should align to the Q3 stewardship stand-up, when the function can state whether the baseline is serving it.

## Risks and Mitigations

- Risk: Trust Score proves not comparable across the mixed dataset population, undermining prioritisation built on it. Mitigation: sample-verify comparability across representative dataset shapes before publishing the baseline, and treat a negative result as a review trigger rather than a tuning exercise.
- Risk: domain owners reject prioritisation based on a composite measure they did not produce and do not interpret. Mitigation: produce interpretation guidance and brief owners before prioritisation begins, and record objections as programme risk rather than resolving them informally.
- Risk: the baseline goes stale after migration and is trusted anyway, producing worse decisions than no baseline. Mitigation: define per-domain refresh cadence tied to change rate, alert on profiling failure, and monitor Trust Score drift.
- Risk: excluded profiling depth turns out to be needed for a quality dimension the programme cares about. Mitigation: keep the remediation tooling decision open, and treat an unaddressable assessment requirement as a review trigger for this decision.
- Risk: profiling load contends with migration load and slows the migration itself. Mitigation: put tenant capacity monitoring in place before bulk profiling, with a defined throttling action.
- Risk: the decision is read as having settled remediation tooling, foreclosing that choice by accident. Mitigation: state the boundary explicitly in programme documentation and in this ADR's scope.

## Review Triggers

Review this ADR if:

- Trust Score comparability sample verification fails across the mixed dataset population.
- Qlik Cloud Data Quality gains or loses profiling capability that changes the depth trade-off against Talend Studio.
- The Q3 stewardship function states baseline requirements the catalog-held approach cannot meet.
- An assessment requirement emerges that needs cross-dataset or cross-system rules, and no platform-native path exists for it.
- SPX's remediation tooling decision selects an approach that makes co-located assessment materially cheaper or more coherent.
- Tenant capacity contention during profiling forces migration schedule changes.
- Dataset population grows materially beyond the 340 in scope, or shifts in shape such that comparability no longer holds.
- QDQ-001 is revised or superseded in a way that changes its guidance on baseline location or on separating assessment from remediation tooling.

## Open Questions

- What refresh cadence applies per domain after migration completes, and who approves it?
- Which interim owner holds baseline currency between migration start and the Q3 stewardship stand-up?
- How is precedence between the catalog baseline and existing application-level quality logic communicated to domain owners, and by whom?
- What is the exception path for datasets that cannot be profiled, and are they excluded from prioritisation or flagged into it?
- Does the programme board require Trust Score reported per domain as well as per dataset, and does that need a view that does not exist yet?
