---
schema_version: "1.0"
report_id: "ACME-ADRKU-2026-001"
report_type: "adr-ku-alignment"
title: "ADR–KU Alignment Report — ACME Industrial Supply Co."
status: "proposed"
version: "0.2"
classification: "internal"
customer_shareable_derivative: true
synthetic: true

account:
  name: "ACME Industrial Supply Co."
  account_id: "SYNTH-ACME"

ownership:
  owner: "Priya Natarajan, CSE"
  reviewer: "Enterprise Architecture Review Group"

dates:
  created_on: "2026-08-15"
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
  program: "Cloud data warehouse migration — Teradata to Snowflake on Azure"

evidence_snapshot:
  accepted_adrs: 8
  proposed_adrs: 1
  kus_checked_as_of: "2026-08-31"
  account_context_as_of: "2026-08-31"

lineage:
  supersedes: null
  superseded_by: null
---

# ADR–KU Alignment Report — ACME Industrial Supply Co.

> **Synthetic example.** All customer details, ADRs, KUs, names, and account notes are fictional. The example is designed to stress-test the Operating Model.

## Purpose and boundary

This report reviews ACME's **Accepted and Proposed ADRs** for the warehouse migration program, their related Knowledge Units, and relevant account context.

It is not a complete assessment of ACME's architecture.

**Accepted ADRs** are treated as governing decisions. **Proposed ADRs** are assessed and flagged, but are not counted as governing architecture.

The report distinguishes:

- **Declared Alignment** — recorded in the ADR;
- **Observed Alignment** — current CSE / EA assessment.

Observed Alignment does not modify the ADR.

## 1. Account Context 🟢 headline / 🔒 account-note detail

**Account:** ACME Industrial Supply Co. — industrial components manufacturing and distribution, with approximately 40 plants and distribution centers across North America and the EU.

**Program:** Retiring an on-prem Teradata EDW in favor of Snowflake on Azure, with Qlik Talend Cloud for integration / quality and Qlik Cloud Analytics for consumption.

**Current program state:** Finance and Sales have substantially cut over. Manufacturing / IoT remains mid-migration.

**Relevant internal notes:**

- **2026-02-03:** Internal audit identified a near-miss involving analyst access sprawl in the warehouse. No breach occurred.
- **2026-07-14:** The architecture function is concentrated in one architect covering governance and delivery. An exploratory discussion about plant-level data quality has occurred, but no formal opportunity exists.

These notes affect prioritization but are not architecture evidence by themselves.

## 2. Decision Portfolio Inventory 🟢

### Governing portfolio — Accepted ADRs

| ID | Decision | Review By | Owner |
|---|---|---|---|---|
| ACME-ADR-001 | Snowflake on Azure as the enterprise cloud data warehouse | 2027-01-20 | M. Feld |
| ACME-ADR-002 | Nightly batch ELT as default for Finance / Sales | 2026-09-10 | E. Kovac |
| ACME-ADR-003 | Single shared staging schema across all domains | **2026-04-02 overdue** | M. Feld |
| ACME-ADR-004 | Temporary direct analyst write access to production schemas | **2026-05-18 overdue** | S. Ramirez |
| ACME-ADR-005 | Tokenization of B2B contact PII | 2027-06-30 | S. Ramirez |
| ACME-ADR-007 | Cross-region DR strategy | 2026-11-12 | M. Feld |
| ACME-ADR-008 | Customer dimension master-data source of truth | 2027-01-22 | E. Kovac |
| ACME-ADR-009 | Route plant IoT telemetry through nightly batch | 2026-10-08 | E. Kovac |

### Pending decision — Proposed ADR

| ID | Decision | Review By | Owner |
|---|---|---|---|---|
| **ACME-ADR-006 — PROPOSED** | Data-quality rule ownership and exception-handling model | 2026-11-05 | E. Kovac |

The Proposed ADR is assessed below but is not counted as governing architecture.

## 3. KU Currency and Alignment Summary 🔒 full detail / 🟢 agreed findings

All cited KUs were checked on **2026-08-31**.

| ADR | ADR status | Cited KU | Current KU state | Declared Alignment | Observed Alignment |
|---|---|---|---|---|---|
| ADR-001 | Accepted | DWH-CLD-PLT-001 | Approved / current / High confidence | Aligned | Aligned |
| ADR-002 | Accepted | ETL-CLD-APP-014 | Approved / current / Medium confidence | Conditionally Aligned | Conditionally Aligned |
| ADR-003 | Accepted | GOV-CLD-DAT-009 | Approved / current / High confidence | Misaligned | Misaligned |
| ADR-004 | Accepted | SEC-CLD-GOV-005 | Approved / current / High confidence | Requires Governance Exception | Requires Governance Exception |
| ADR-005 | Accepted | SEC-CLD-DAT-011 | Approved / current / High confidence | Aligned | Aligned |
| **ADR-006** | **Proposed** | — | No KU cited | No KU Coverage | No KU Coverage |
| ADR-007 | Accepted | OPS-CLD-TEC-018 | Approved / current / Medium confidence | Conditionally Aligned | Conditionally Aligned |
| ADR-008 | Accepted | MDM-CLD-DAT-007 | Approved / current / High confidence | Aligned | Aligned |
| ADR-009 | Accepted | INT-CLD-APP-021 | Approved / current / High confidence | Requires Governance Exception | Requires Governance Exception |

### Governing Accepted portfolio

- **3 Aligned**
- **2 Conditionally Aligned**
- **1 Misaligned**
- **2 Requires Governance Exception**

### Proposed portfolio

- **1 No KU Coverage**

This separation prevents a pending decision from being presented as part of the accepted architecture posture.

## 4. Material Findings

### ACME-ADR-003 — Shared staging schema
**Status:** Accepted  
**Declared / Observed:** Misaligned / Misaligned  
**KU:** `GOV-CLD-DAT-009` — Current and Approved

The KU recommends domain-isolated staging to limit blast radius and enable domain-level access control. ACME deliberately chose a single schema under migration-time pressure.

A malformed Manufacturing / IoT load has since affected a Finance refresh through shared-schema locking, matching a failure mode described by the KU. The ADR's review is overdue.

**Finding type:** Decision revisit + Governance follow-up  
**Risk:** Architecture / Governance  
**Priority:** High

**Recommended conversation:** Validate whether the migration constraint that justified the exception still applies. Do not prescribe a replacement design until the current domain and operational requirements are confirmed.

### ACME-ADR-004 — Temporary direct analyst write access
**Status:** Accepted  
**Declared / Observed:** Requires Governance Exception / Requires Governance Exception  
**KU:** `SEC-CLD-GOV-005` — Current and Approved

The ADR explicitly accepted a KU anti-pattern as a temporary exception, with an end condition: retire direct writes once the reconciliation pipeline is live.

Account evidence suggests that pipeline may already be live, while the access remains. The ADR review is overdue, and the internal audit near-miss increases the priority.

**Finding type:** Decision revisit + Governance follow-up  
**Risk:** Governance / Security / Operational  
**Priority:** Critical

**Recommended conversation:** Confirm whether the stated end condition has been met and either close the exception or create a new explicit decision.

### ACME-ADR-002 — Nightly batch for Finance / Sales
**Status:** Accepted  
**Declared / Observed:** Conditionally Aligned / Conditionally Aligned  
**KU:** `ETL-CLD-APP-014` — Current and Approved

The KU supports nightly cadence when downstream freshness is at least 12 hours. Finance month-end requires eight hours and is currently covered by a manual micro-batch.

The architecture decision does not automatically need to change. The immediate concern is that the condition is being satisfied through a manual workaround.

**Finding type:** Execution follow-up  
**Risk:** Delivery / Operational  
**Priority:** Medium

### ACME-ADR-007 — Disaster recovery
**Status:** Accepted  
**Declared / Observed:** Conditionally Aligned / Conditionally Aligned  
**KU:** `OPS-CLD-TEC-018` — Current and Approved

The ADR's 4-hour RPO / 8-hour RTO is compatible with KU guidance only when quarterly failover testing occurs. The first test has been deferred twice.

The decision remains sound; the execution condition is unmet.

**Finding type:** Execution follow-up  
**Risk:** Operational  
**Priority:** High

### ACME-ADR-009 — IoT telemetry through nightly batch
**Status:** Accepted  
**Declared / Observed:** Requires Governance Exception / Requires Governance Exception  
**KU:** `INT-CLD-APP-021` — Current and Approved

The source already lands in Kafka, but ACME routes telemetry through nightly processing because the manufacturing domain is not staffed for a streaming path.

Plant managers have asked for same-shift OEE information, making the current latency an active business issue.

**Finding type:** Decision revisit candidate  
**Risk:** Architecture / Adoption  
**Priority:** High

**Recommended conversation:** Validate the business freshness requirement and whether the staffing constraint remains. Streaming is a possible design direction, not a conclusion of this report.

### ACME-ADR-006 — DQ ownership and exception handling
**Status:** **Proposed**  
**Declared / Observed:** No KU Coverage / No KU Coverage

The proposed decision assigns rule ownership to business domains while routing exceptions to a centralized queue. No current KU directly addresses this ownership / exception model.

More than 40 exceptions have reportedly remained unresolved for over 30 days.

**Finding type:** KU coverage gap + Proposed-decision review  
**Priority:** Medium

The report should not generate a new KU automatically. The decision deserves additional validation before acceptance, and KU-library governance may separately consider whether a reusable pattern is missing.

## 5. Architecture Whitespace / Discovery Flags 🔒

These are **not confirmed architecture gaps**.

### Data catalog and lineage
Relevant KU guidance exists, and ACME has a heterogeneous footprint across SAP, CRM, e-commerce, Kafka / IoT, and plant systems, but no ADR in the supplied portfolio addresses lineage or catalog ownership.

**Discovery question:** Is the decision documented elsewhere, or is this genuinely undecided?

### Data retention and archival
ACME has a PII-tokenization decision but no ADR in the supplied portfolio defining retention and archival boundaries.

**Discovery question:** Is retention governed elsewhere, particularly for EU data?

## 6. Risk and Governance Rollup 🔒

- **Critical governance / security:** ADR-004 may have outlived its own end condition and is tied to an internal audit near-miss.
- **Architecture / governance:** ADR-003 is overdue and a warned failure mode has already occurred.
- **Operational:** ADR-007 remains unverified because DR testing has not occurred.
- **Operational / delivery:** ADR-002 relies on a manual safeguard.
- **Architecture / adoption:** ADR-009 may no longer support the manufacturing decision-making requirement.
- **Proposed-decision quality:** ADR-006 has no current KU coverage and unresolved ownership consequences.

There is not enough evidence to classify the account as a Relationship or Renewal Risk.

## 7. Customer-Success Opportunity Signals 🔒

### Adoption / value realization
- Use current Qlik Talend Cloud capabilities more effectively for plant-level data-quality and manufacturing workflows if discovery confirms the problem.
- Improve DQ exception operations before adding technology.
- Use the ADR governance process to close stale exceptions and time-bound decisions.

### Expertise / engagement
- CSE / EA architecture review for ADR-003, ADR-004, and ADR-009.
- Advisory support to separate decision issues from execution commitments.
- Operating-model support for the Proposed DQ ownership decision.

### Capability / expansion
- Plant-level data quality may become an expansion topic if the customer confirms the need and current entitlement is insufficient.
- Catalog / lineage is a discovery topic first; additional capability should be discussed only after the customer problem is validated.

## 8. Trajectory 🔒

The earliest accepted decisions show a sound platform foundation but also two migration-pressure exceptions: the shared staging design and temporary direct-write access.

The middle period shows stronger alignment around security, DR, and MDM.

The most recent accepted decision, ADR-009, introduces a new exception driven by staffing rather than migration deadline.

The portfolio therefore suggests that **decision governance improved after the initial cutover, but capacity constraints are now creating a different class of exception**.

This is evidence about **architecture decision / governance maturity**, not overall architecture maturity.

## 9. Prioritized CSE / EA Engagement Agenda 🔒

| Priority | Conversation | Why now | Intended outcome | Type |
|---|---|---|---|---|
| 1 | Close or refresh ADR-004 direct-write exception | Overdue; end condition may be met; audit near-miss | Confirm closure or create a new explicit decision | Decision / governance |
| 2 | Revisit ADR-003 shared staging | Overdue; original constraint changed; failure mode occurred | Confirm whether a new architecture decision is required | Decision revisit |
| 3 | Qualify ADR-009 manufacturing latency | Same-shift OEE need conflicts with current batch path | Confirm requirement and current constraint | Architecture / adoption discovery |
| 4 | Execute ADR-007 and ADR-002 safeguards | DR test missing; Finance safeguard manual | Close execution gaps without unnecessarily reopening sound decisions | Execution |
| 5 | Review Proposed ADR-006 and whitespace areas | Pending decision has no KU; lineage / retention not found | Improve decision quality and identify missing discovery | Governance / discovery |

## 10. Executive Rollup 🟢

**9 ADRs are in scope: 8 Accepted and 1 Proposed.** The Accepted governing portfolio contains **3 Aligned, 2 Conditionally Aligned, 1 Misaligned, and 2 Requires Governance Exception** decisions. The single Proposed ADR has **No KU Coverage** and should be reviewed before acceptance.

All cited KUs were checked as current on **31 August 2026**. Two Accepted ADR reviews are overdue, and both relate to high-consequence findings. The strongest immediate actions are to close the direct-write exception, revisit the shared staging decision, execute already-agreed resilience safeguards, and validate whether manufacturing data freshness requirements have changed.

Overall, ACME has a sound platform foundation but shows weak retirement governance for time-bound exceptions and a newer pattern of decisions being shaped by capacity constraints. The current evidence supports proactive architecture, adoption, and advisory conversations but does not by itself indicate a relationship or renewal risk.

## 11. Customer-Shareable Derivative Guidance 🔒

**Retain:**
- program scope;
- Accepted / Proposed ADR inventory;
- validated KU status and alignment findings;
- factual overdue reviews;
- agreed execution gaps;
- discovery questions;
- architecture conversation topics.

**Remove or reframe:**
- account-health / renewal interpretation;
- commercial opportunity framing;
- internal audit or staffing detail unless customer-approved for use;
- unvalidated root-cause hypotheses;
- internal prioritization based on account strategy.

The customer derivative should read as an **architecture decision review and discussion agenda**, not an account assessment.
