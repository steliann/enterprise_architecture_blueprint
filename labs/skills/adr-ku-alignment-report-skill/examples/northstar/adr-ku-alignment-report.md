---
schema_version: "1.0"
report_id: "NORTHSTAR-ADRKU-2026-001"
report_type: "adr-ku-alignment"
title: "ADR–KU Alignment Report — Northstar Components Group"
status: "proposed"
version: "0.3"
classification: "internal"
customer_shareable_derivative: true
synthetic: true

account:
  name: "Northstar Components Group"
  account_id: "SYNTH-NORTHSTAR"

ownership:
  owner: "CSE / Enterprise Architect"
  reviewer: "Account Architecture Review Group"

dates:
  created_on: "2026-08-20"
  last_updated: "2026-08-31"
  assessment_as_of: "2026-08-31"
  review_by: "2026-09-30"

scope:
  included_adr_statuses:
    - accepted
    - proposed
  excluded_adr_statuses:
    - draft
    - superseded
    - deprecated
  program: "Data integration modernization and Qlik Talend Cloud adoption"

evidence_snapshot:
  accepted_adrs: 6
  proposed_adrs: 2
  kus_checked_as_of: "2026-08-31"
  account_context_as_of: "2026-08-31"

lineage:
  supersedes: null
  superseded_by: null
---

# ADR–KU Alignment Report — Northstar Components Group

> **Synthetic example.** All customer, ADR, KU, and account information is fictional. This example demonstrates a representative CSE / EA working report, including a superseded KU reference.

## Purpose and boundary

This report reviews Northstar's **Accepted and Proposed ADRs** for its data integration modernization and Qlik Talend Cloud adoption program, their related Knowledge Units, and relevant account context.

It is not a complete assessment of Northstar's architecture.

**Accepted ADRs** are treated as governing decisions. **Proposed ADRs** are assessed and flagged, but are not counted as governing architecture.

The report distinguishes:

- **Declared Alignment** — recorded in the ADR;
- **Observed Alignment** — current CSE / EA assessment.

Observed Alignment does not modify the ADR.

## 1. Account Context 🟢 headline / 🔒 account-note detail

**Account:** Northstar Components Group — industrial manufacturing and aftermarket services.

**Program:** Modernization of a Talend-based integration estate, with Qlik Talend Cloud used for selected workloads and Snowflake as the main analytical platform.

**Current program state:** The first production Qlik Talend Cloud workload is live. The customer remains cautious about moving SAP-related workloads because of operational-control requirements and continues to operate a mixed Talend on-prem / Qlik Talend Cloud model.

**Relevant internal notes:**

- **2026-05-12:** First production Qlik Talend Cloud Salesforce-to-Snowflake workload is successful; customer remains cautious about SAP workload movement because of operational-control requirements.
- **2026-06-04:** PS review found uneven Remote Engine workload distribution and no automated failover for one critical SAP extraction chain.
- **2026-07-09:** Customer reported that production changes often wait on a small central integration team.
- **2026-07-22:** Service operations asked whether order and parts data could be available intraday rather than next day.
- **2026-08-05:** Customer wants to simplify the mixed Talend on-prem / Qlik Talend Cloud operating model; no formal expansion discussion exists.

These notes affect prioritization and discovery but are not architecture evidence by themselves.

## 2. Decision Portfolio Inventory 🟢

### Governing portfolio — Accepted ADRs

| ID | Decision | Review By | Owner |
|---|---|---|---|
| NS-ADR-001 | Snowflake as primary analytical platform | 2027-02-14 | J. Belham |
| NS-ADR-002 | Qlik Talend Cloud for new SaaS-to-cloud workloads | 2026-12-18 | J. Belham |
| NS-ADR-003 | Retain Talend Remote Engine for SAP extraction during transition | **2026-07-03 overdue** | J. Belham |
| NS-ADR-004 | Use log-based CDC for operational replication | 2027-09-11 | J. Belham |
| NS-ADR-005 | Direct SQL Server-to-Snowflake copy for transition migrations | **2026-04-06 overdue** | J. Belham |
| NS-ADR-007 | Nightly batch as default for service analytics | 2026-11-27 | J. Belham |

### Pending decisions — Proposed ADRs

| ID | Decision | Domain | Review By | Owner |
|---|---|---|---|
| **NS-ADR-006 — PROPOSED** | Central platform team approves all production changes | 2026-10-19 | J. Belham |
| **NS-ADR-008 — PROPOSED** | DQ rules owned by domains, execution centralized | 2026-12-16 | J. Belham |

The Proposed ADRs are assessed below but are not counted as governing architecture.

## 3. KU Currency and Alignment Summary 🔒 full detail / 🟢 agreed findings

All cited KUs were checked on **2026-08-31**.

| ADR | ADR status | Cited KU | Current KU state | Declared Alignment | Observed Alignment |
|---|---|---|---|---|---|
| ADR-001 | Accepted | QTC-DAT-001 | Approved / current | Aligned | Aligned |
| ADR-002 | Accepted | QTC-PLT-004 | Approved / current | Aligned | Aligned |
| ADR-003 | Accepted | TAL-RUN-009 | Approved / current | Conditionally Aligned | Requires Governance Exception |
| ADR-004 | Accepted | QR-CDC-003 | Approved / current | Aligned | Conditionally Aligned |
| ADR-005 | Accepted | MIG-DAT-006 | Approved / current | Misaligned | Misaligned |
| **ADR-006** | **Proposed** | GOV-OPS-012 | Approved / current | Requires Governance Exception | Requires Governance Exception |
| ADR-007 | Accepted | INT-CAD-014 | **Superseded by INT-CAD-019** | Conditionally Aligned | Conditionally Aligned |
| **ADR-008** | **Proposed** | — | No KU cited | No KU Coverage | No KU Coverage |

### Governing Accepted portfolio

- **2 Aligned**
- **2 Conditionally Aligned**
- **1 Misaligned**
- **1 Requires Governance Exception**

### Proposed portfolio

- **1 Requires Governance Exception**
- **1 No KU Coverage**

This separation prevents pending decisions from being presented as part of the accepted architecture posture.

### KU reference currency — ADR-007

The ADR still cites `INT-CAD-014`, which has been superseded by `INT-CAD-019 — Consumer Freshness and Processing Cadence`.

The successor KU retains the principle that processing cadence should be derived from consumer freshness requirements. The current evidence therefore does not justify changing ADR-007's Observed Alignment solely because the KU reference changed.

However:

- the ADR reference should be refreshed through normal ADR governance;
- recent account notes suggest the underlying service-data freshness requirement may itself have changed.

**Finding type:** KU reference currency + Decision revisit candidate

The report does not edit the ADR automatically.

## 4. Material Findings

### NS-ADR-003 — Remote Engine for SAP transition
**Status:** Accepted  
**Declared / Observed:** Conditionally Aligned / **Requires Governance Exception**  
**KU:** `TAL-RUN-009` — current and Approved

The ADR allows a single execution path during transition only while critical workloads have a documented recovery mechanism and tested failover.

Current evidence indicates that one critical SAP extraction chain lacks automated failover. The review date is overdue.

**Finding type:** Governance follow-up + Execution follow-up  
**Risk:** Operational / Governance  
**Priority:** High

**Recommended conversation:** Confirm whether the workload remains intentionally transitional and whether resilience should be implemented immediately or the runtime-placement decision revisited.

### NS-ADR-005 — Direct migration copy
**Status:** Accepted  
**Declared / Observed:** Misaligned / Misaligned  
**KU:** `MIG-DAT-006` — current and Approved

The ADR deliberately allows direct database copy for one-time migration work. Account notes indicate that the pattern is now being proposed for recurring data movement because it is faster to deliver.

The original decision may still have been reasonable, but its use is expanding beyond its stated scope.

**Finding type:** Decision revisit + Governance follow-up  
**Risk:** Architecture / Governance  
**Priority:** High

**Recommended conversation:** Reconfirm the boundary between one-time migration mechanisms and recurring production integration. Do not prescribe a replacement design until the recurring workload requirements are understood.

### NS-ADR-004 — CDC monitoring
**Status:** Accepted  
**Declared / Observed:** Aligned / **Conditionally Aligned**  
**KU:** `QR-CDC-003` — current and Approved

The CDC architecture remains sound, but the KU expects consistent monitoring across capture delay, apply delay, and recovery state. Current account evidence indicates that monitoring practices differ between teams.

**Finding type:** Execution follow-up  
**Risk:** Operational  
**Priority:** Medium

**Recommended conversation:** Validate a common minimum monitoring standard before CDC adoption expands to additional domains.

### NS-ADR-006 — Central production approval
**Status:** **Proposed**  
**Declared / Observed:** Requires Governance Exception / Requires Governance Exception  
**KU:** `GOV-OPS-012` — current and Approved

The proposed decision centralizes all production approvals in a small platform team. This is a deliberate exception to the KU's federated-delivery-with-central-guardrails model.

Account evidence already shows delivery friction around the same central team.

Because the ADR is Proposed, this is an opportunity to challenge the operating model **before it becomes governing architecture**.

**Finding type:** Proposed-decision review  
**Risk:** Delivery / Adoption  
**Priority:** High

**Recommended conversation:** Determine whether Northstar can retain its required controls while reducing dependency on the central team.

### NS-ADR-007 — Nightly batch for service analytics
**Status:** Accepted  
**Declared / Observed:** Conditionally Aligned / Conditionally Aligned  
**Current KU:** `INT-CAD-019` successor guidance

The original requirement was next-business-day availability. Service operations now asks for intraday availability.

The new account note does not by itself make the ADR misaligned. It is sufficient to trigger validation of the underlying requirement.

**Finding type:** Decision revisit candidate + KU reference currency  
**Risk:** Adoption, if the changed requirement is confirmed  
**Priority:** Medium

**Recommended conversation:** Confirm whether intraday availability is now a formal requirement. Only then determine whether the cadence decision should change.

### NS-ADR-008 — Federated DQ ownership
**Status:** **Proposed**  
**Declared / Observed:** No KU Coverage / No KU Coverage

No current KU directly addresses the proposed split between domain rule ownership, centralized execution, and exception accountability.

**Finding type:** KU coverage gap + Proposed-decision review  
**Priority:** Medium

The report does not create a new KU automatically. The decision deserves additional validation before acceptance; KU-library governance may separately consider whether reusable guidance is missing.

## 5. Architecture Whitespace / Discovery Flags 🔒

These are **not confirmed architecture gaps**.

### Enterprise lineage and impact analysis

Relevant guidance exists, but the supplied portfolio contains no ADR for lineage ownership or impact analysis across SAP, Salesforce, Snowflake, Talend, Qlik Talend Cloud, and CDC.

**Discovery question:** Is the decision documented elsewhere, or is the topic genuinely undecided?

### Runtime observability standard

Multiple ADRs depend on monitoring, but the supplied portfolio contains no ADR defining a common minimum observability standard across Remote Engine, Qlik Talend Cloud, and CDC workloads.

**Discovery question:** Does an operational standard exist outside the ADR portfolio?

## 6. Risk and Governance Rollup 🔒

- **Operational / Governance:** ADR-003 is overdue and a required resilience condition is not currently met.
- **Architecture / Governance:** ADR-005 is overdue and a time-bound migration pattern is expanding beyond its original scope.
- **Delivery / Adoption:** Proposed ADR-006 may institutionalize a bottleneck already visible in account notes.
- **Operational:** ADR-004 depends on monitoring controls that are not yet consistently implemented.
- **Adoption:** ADR-007 may no longer satisfy the consumer freshness requirement, but that requirement still needs validation.
- **Proposed-decision quality:** ADR-008 has no current KU coverage and should receive additional review before acceptance.
- **KU reference currency:** ADR-007 cites superseded guidance and its reference should be refreshed through normal ADR governance.

There is insufficient evidence to classify Northstar as a Relationship or Renewal Risk.

## 7. Customer-Success Opportunity Signals 🔒

### Adoption / value realization

- Use the runtime-placement and resilience review to identify which workloads can safely use capabilities Northstar already owns.
- Standardize monitoring as CDC expands so that increased adoption does not create inconsistent operational controls.
- Use the ADR review process to retire or refresh transition patterns rather than allowing them to become defaults.

### Expertise / engagement

- Run a CSE / EA operating-model workshop on guardrails, delegated delivery, and production controls before Proposed ADR-006 is accepted.
- Facilitate the review of ADR-003 and ADR-005 as a combined transition-governance discussion.
- Help the customer distinguish whether ADR-007 is an architecture problem or a changed business requirement.

### Capability / expansion

- If intraday service data becomes a confirmed requirement and current capabilities or entitlements are insufficient, assess whether additional Qlik capability is relevant.
- Lineage / impact analysis is a discovery topic first; additional capability should only follow validation of the customer's need.

## 8. Trajectory 🔒

The portfolio shows three broad phases.

**Initial modernization direction.** ADR-001 and ADR-002 establish a coherent target direction: Snowflake for analytics and Qlik Talend Cloud for new cloud-oriented workloads.

**Transition pragmatism.** ADR-003 and ADR-005 introduce temporary exceptions intended to preserve delivery speed during modernization. Both are now overdue for review, and each is beginning to behave like a persistent operating pattern. ADR-004 introduces a stronger CDC pattern, but its operational monitoring is not yet consistently implemented.

**Operating-model pressure.** More recent decisions and account context point increasingly toward organizational constraints rather than platform selection. Proposed ADR-006 centralizes approvals in the same small team associated with delivery friction. ADR-007 may also be reaching the limits of the freshness requirement it was originally designed to satisfy.

The portfolio therefore does not show a simple "better" or "worse" trend.

A more useful interpretation is:

> **Northstar's target technology direction is becoming clearer, while retirement of transitional decisions and the production operating model are becoming the main constraints on architecture decision quality and delivery.**

This is an assessment of **architecture decision / governance maturity**, not overall architecture maturity.

## 9. Prioritized CSE / EA Engagement Agenda 🔒

| Priority | Conversation | Why now | Intended customer outcome | Type |
|---|---|---|---|---|
| 1 | Review ADR-003 and ADR-005 transition decisions | Both are overdue; transition patterns are becoming persistent | Confirm retirement, refresh, or the need for a new decision | Decision revisit / Governance / Execution |
| 2 | Challenge Proposed ADR-006 operating model | Decision is not yet governing; current friction is already visible | Preserve required controls without institutionalizing a bottleneck | Proposed-decision review / Adoption |
| 3 | Validate service freshness and refresh ADR-007 KU reference | KU is superseded and the business requirement may have changed | Confirm the requirement, then determine whether the ADR needs revision | Discovery / Decision revisit / KU currency |
| 4 | Standardize monitoring around ADR-004 | Expansion of CDC depends on consistent operational controls | Agree a common minimum monitoring standard | Execution |
| 5 | Review Proposed ADR-008 and whitespace areas | No KU coverage; lineage and observability decisions are not present in the supplied portfolio | Improve pending decision quality and determine whether missing decisions exist elsewhere | Governance / Discovery |

## 10. Executive Rollup 🟢

**8 ADRs are in scope: 6 Accepted and 2 Proposed.** The Accepted governing portfolio contains **2 Aligned, 2 Conditionally Aligned, 1 Misaligned, and 1 Requires Governance Exception** decision. The Proposed portfolio contains **1 Requires Governance Exception and 1 No KU Coverage** decision.

All cited KUs were checked on **31 August 2026**. One Accepted ADR references a superseded KU; successor guidance was used for the current assessment and the ADR reference should be refreshed through normal governance. Two Accepted ADR reviews are overdue.

Overall, Northstar's platform direction remains coherent, but transitional choices and centralized operating controls are becoming persistent constraints. The most useful next actions are to review the overdue transition decisions, challenge the proposed central-approval model before acceptance, validate whether service-data freshness requirements have changed, and establish consistent operational monitoring.

The current evidence supports proactive architecture, governance, adoption, and advisory conversations but does not by itself indicate a Relationship or Renewal Risk.

## 11. Customer-Shareable Derivative Guidance 🔒

**Retain:**

- program scope;
- Accepted / Proposed distinction;
- current KU-state findings;
- factual overdue reviews;
- architecture and execution findings;
- constructive discovery questions;
- agreed next-step architecture conversations.

**Remove or reframe:**

- internal account notes;
- adoption / expansion framing;
- hypotheses about team capacity;
- account risk classifications;
- internal prioritization rationale.

A customer derivative should read as an **architecture decision review and discussion agenda**, not an account-health or commercial document.
