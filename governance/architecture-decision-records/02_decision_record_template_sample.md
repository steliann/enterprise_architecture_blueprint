---
# ---- Identity ----
id: SPX-ADR-001                   # ADR-NNN or SCOPE-ADR-NNN — unique and never reused
yaml_version: 1                   # schema version this record follows
title: Use Qlik Cloud Catalog for Initial Data Quality Profiling
status: Proposed                  # Draft | Proposed | Accepted | Deprecated | Superseded
date: 2026-05-26                  # date the decision was recorded or made
review_by: 2026-11-26              # next planned review date; null if not applicable

# ---- Ownership ----
decision_owner: "Andrew Younge — Enterprise Architect"   # single person or role accountable for the decision
contributors:                     # people who contributed to the decision, options, or review
  - "SPX Data Platform Lead"
  - "SPX Data Governance Manager"

# ---- Classification ----
decision_type: "Architecture"
architecture_domain: Data         # Data | Application | Integration | Security | Platform | Operations | Governance | Other
decision_scope: Customer          # Customer | Product Platform | Program | Enterprise | Reference Architecture
decision_level: Tactical          # Strategic | Tactical | Operational
confidence: High                  # High | Medium | Low

# ---- Technology scope ----
technology_scope:
  qlik:                           # Qlik products directly involved in the decision
    - "Qlik Cloud Catalog"
    - "Qlik Cloud Data Quality"
  talend:                         # Talend products directly involved in the decision; null if none
    - "Talend Studio"
  third_party:                    # external technologies directly involved; null if none
    - "Microsoft SQL Server"

# ---- Relationships ----
related_patterns:                 # supporting Knowledge Units or reusable patterns; null if none
  - "QDQ-001 — Data Quality Profiling Baseline (../knowledge-units/qdq-001-data-quality-profiling-baseline.md)"
related_adrs:                     # peer ADRs worth reading alongside this one; null if none
  - SPX-ADR-002
impacted_architecture_views:      # architecture views affected by this decision
  - "Governance View"
  - "Data Flow View"
  - "Operational View"
related_assets:                   # diagrams, playbooks, designs, workshop outputs, or assessments; null if none
  - "SPX Data Quality Discovery Workshop, 2026-05-14"
supersedes: null                  # ADR this one replaces; null if original
superseded_by: null               # ADR that replaces this one; null if current

# ---- AI assistance ----
used_ai_to_prepare: true          # true if AI helped prepare, review, or refine the ADR
ai_solutions_used:                # null if used_ai_to_prepare is false
  - "GitHub Copilot"

# ---- Tags ----
tags:
  - data-quality
  - profiling
  - catalog
  - trust-score
---

<!--
This file is a worked SAMPLE, not a blank starting point. Copy 03_decision_record_template_blank.md
to start a new ADR — copying this file risks carrying over SPX-specific content by accident.

HOW COMPLETENESS VARIES BY STATUS

  Draft:      Decision still being shaped. May contain open questions, incomplete option
              analysis, or unresolved ownership.
  Proposed:   Decision is clear and ready for architecture review, but not yet accepted.
  Accepted:   Approved for the stated scope. Decision explicit, selected option clear,
              trade-offs documented, review triggers defined.
  Superseded: Replaced by another ADR. superseded_by must point to the replacement.
  Deprecated: No longer recommended or applicable, with no direct replacement.

Required sections for every ADR, regardless of status:
Context, Decision, Decision Drivers, Options Considered, Decision Outcome, Architecture Impact,
Consequences, Implementation Implications, Operational Implications, Risks and Mitigations,
Review Triggers, Open Questions.

Optional section:
Knowledge Unit Alignment — add this only when existing KUs materially support, constrain,
or contradict the ADR.
-->

# SPX-ADR-001 — Use Qlik Cloud Catalog for Initial Data Quality Profiling

## Context

SPX is migrating eleven operational reporting domains onto Qlik Cloud, and no shared data quality baseline currently exists across them — each domain judges its own data acceptable or not, with no common measure. The stewardship function SPX plans to stand up later this year needs one defensible baseline to prioritize against, not eleven disagreeing domain-level assessments.

The decision covers where initial profiling happens for datasets landing in Qlik Cloud during migration, and where the resulting quality baseline is recorded as authoritative. It does not cover operational remediation of quality issues once found — that is a separate decision. SPX already runs Talend Studio for integration work, which makes it a genuine candidate for profiling as well, not just a default choice.

Leaving this ambiguous has a real cost: without one baseline, remediation priority becomes a negotiation between domain owners, and the incoming stewardship function inherits a backlog it cannot defend with numbers anyone agrees on.

## Decision

We will use Qlik Cloud Catalog together with Qlik Cloud Data Quality to profile datasets migrated into Qlik Cloud and to hold the authoritative initial quality baseline for each one. This catalog-held baseline becomes the single reference point for remediation prioritization. Talend Studio profiling and any application-level quality checks are explicitly excluded from the authoritative-baseline role, though they may continue to inform domain-level work.

## Decision Drivers

- The incoming stewardship function needs one defensible baseline, not eleven domain-owned assessments that disagree with each other.
- Remediation sequencing across all migrated datasets must be justifiable to the programme board using a uniform measure, not per-domain judgment.
- The baseline must exist before remediation starts, or the programme has no before-state to measure improvement against.
- Governance and stewardship users are business-side, not developer-side, so the baseline needs to live in a metadata surface they can reach without an integration toolchain.
- The migration timeline leaves no room for a bespoke profiling build.
- SPX's existing Talend Studio footprint makes the profiling-tool choice a real decision, not a default, and the boundary with remediation tooling needs to be explicit.

## Options Considered

### Option 1 — Qlik Cloud Catalog and Qlik Cloud Data Quality as the baseline

Profile datasets as they land in Qlik Cloud, using Qlik Cloud Data Quality to generate quality measures and Qlik Cloud Catalog to hold the resulting baseline and metadata alongside the dataset itself. Governance and stewardship users work directly from the catalog.

**Benefits**

- No new tooling introduced; the baseline lives where lineage and ownership metadata already sit.
- Business-side users can read the baseline without needing integration-team access.
- Profiling follows migration automatically, with no separate scheduled workstream.

**Limitations**

- Forgoes cross-dataset and cross-system profiling rules that Talend Studio could express.
- Creates a dependency on the Qlik Cloud Data Quality roadmap for any assessment need that emerges later.

**Fit assessment**

Selected. It puts the baseline directly in the metadata surface stewardship will use, without requiring a bespoke build inside the migration window.

### Option 2 — Talend Studio profiling jobs feeding a shared quality baseline table

Build dedicated Talend Studio jobs to profile each migrated dataset and write results to a shared control table that Catalog or another tool then surfaces.

**Benefits**

- Full control over profiling rules, including cross-dataset and cross-system checks Qlik Cloud Data Quality cannot express today.
- Reuses the integration team's existing Talend skill set.

**Limitations**

- Requires building and maintaining a new profiling job set inside an already-tight migration timeline.
- Separates the baseline from the catalog's lineage and ownership metadata unless a further integration step is built, adding a second surface stewardship users must learn.

**Fit assessment**

Rejected for the initial baseline. The build cost and the split from catalog metadata outweigh the extra profiling depth SPX doesn't yet have a stated need for; revisit if a cross-dataset rule becomes a real requirement.

## Decision Outcome

Selected option: Option 1 — Qlik Cloud Catalog and Qlik Cloud Data Quality as the baseline.

This option gives the stewardship function one baseline, visible in the same place as lineage and ownership, without asking the migration programme to fund a bespoke profiling build. It assumes Trust Score comparability holds across SPX's mixed dataset population — verified by sampling before the baseline is published to the programme board — and that Talend Studio profiling remains available as a separate, later decision if a profiling depth requirement emerges that Qlik Cloud Data Quality can't meet.

## Knowledge Unit Alignment

### Supporting Knowledge Units

* [QDQ-001 — Data Quality Profiling Baseline](../knowledge-units/qdq-001-data-quality-profiling-baseline.md): recommends catalog-held profiling as the default starting pattern for a customer with no existing shared baseline, which matches SPX's situation.

### Conditional Support and Constraints

* [QDQ-001 — Data Quality Profiling Baseline](../knowledge-units/qdq-001-data-quality-profiling-baseline.md): the KU's guidance is conditional on baseline comparability being verified across the customer's actual dataset population before publication — reflected here in Decision Outcome and in Risks and Mitigations.

### Contradictions or Exceptions

No contradiction identified.

### Alignment Outcome

Conditionally aligned. The decision follows QDQ-001's default pattern, conditional on the comparability check described in Decision Outcome.

## Architecture Impact

### Business

Quality prioritization moves from domain-level negotiation to one programme-level reference point. Domain owners lose the ability to set their own thresholds for prioritization and will need a short briefing on how to read the baseline before remediation sequencing starts.

### Data

Every migrated dataset gains a quality baseline held in the catalog alongside its lineage and ownership metadata. The baseline is a point-in-time measure and needs a defined refresh cadence once migration completes, or it will silently go stale.

### Application

Profiling becomes a step in the existing per-domain migration runbook rather than a new standalone application. Talend Studio's integration workload is untouched by this decision.

### Technology

No new runtime or infrastructure is introduced; profiling runs inside Qlik Cloud against datasets already landed there. Profiling load coincides with migration load on the same tenant, which needs capacity monitoring it doesn't currently have.

## Consequences

### Positive Consequences

- Establishes one governed quality baseline before any remediation work begins, giving the programme a measurable before-state.
- Replaces eleven domain-specific, incomparable assessments with one measure the programme board can act on.
- Keeps quality, lineage, and ownership readable from the same metadata surface.
- Lets the stewardship function start with a defensible backlog instead of spending its first quarter building one.
- Delivers inside the migration timeline with no bespoke build.

### Negative Consequences / Trade-offs

- Forgoes cross-dataset and cross-system profiling rules that Talend Studio could express, so some quality dimensions go unassessed at baseline.
- Ties SPX's assessment capability to the Qlik Cloud Data Quality roadmap, with no in-house fallback in place.
- Removes domain owners' local control over prioritization thresholds, which is likely to create friction when remediation sequencing starts.
- Adds a transitional period where application-level quality checks and the catalog baseline can disagree, and precedence has to be communicated.
- Makes baseline currency an ongoing operational obligation — a stale baseline that's still trusted is worse than no baseline.

## Implementation Implications

- Add profiling as a gate in each domain's migration runbook, executed on dataset arrival and before remediation touches the dataset.
- Sample-verify Trust Score comparability across a representative spread of datasets before publishing the baseline to the programme board.
- Document precedence between the catalog baseline and existing application-level quality checks, and communicate it to all eleven domain owners.
- Provision stewardship users' Qlik Cloud space access ahead of the function standing up, not at the point they first need it.
- Put tenant capacity monitoring in place before bulk profiling begins, since profiling and migration load coincide.
- Define a per-domain baseline refresh cadence tied to change rate rather than a single fixed schedule.

## Operational Implications

- Assign an interim owner for baseline currency until the stewardship function takes it over.
- Alert on profiling failures — a silently unprofiled dataset drops out of prioritization without anyone noticing.
- Monitor tenant capacity during profiling windows against the migration schedule.
- Route any change to stewardship's catalog access through change control, since access loss silently disables the governance function.
- Set a documented cadence and named approver for baseline publication to the programme board.

## Risks and Mitigations

- Risk: Trust Score comparability doesn't hold across SPX's mixed dataset population, undermining prioritization built on it. Mitigation: sample-verify comparability before publishing the baseline, and treat a negative result as a review trigger.
- Risk: domain owners reject prioritization based on a composite measure they didn't produce. Mitigation: brief owners on Trust Score interpretation before prioritization begins.
- Risk: the baseline goes stale after migration and is still trusted. Mitigation: define a per-domain refresh cadence and alert on profiling failure.
- Risk: profiling load contends with migration load and slows migration itself. Mitigation: put tenant capacity monitoring in place before bulk profiling, with a defined throttling action.

## Review Triggers

Review this ADR if:

- Trust Score comparability sample verification fails across SPX's dataset population.
- Qlik Cloud Data Quality gains or loses capability that changes the depth trade-off against Talend Studio.
- The stewardship function states a baseline requirement the catalog-held approach can't meet.
- An assessment requirement emerges that needs cross-dataset or cross-system rules with no platform-native path.
- Tenant capacity contention during profiling forces a migration schedule change.
- QDQ-001 is revised or superseded in a way that changes its baseline-location guidance.

## Open Questions

- What refresh cadence applies per domain after migration completes, and who approves it?
- Who holds baseline currency between migration start and the stewardship function standing up?
- What is the exception path for a dataset that fails to profile — excluded from prioritization, or flagged into it?
