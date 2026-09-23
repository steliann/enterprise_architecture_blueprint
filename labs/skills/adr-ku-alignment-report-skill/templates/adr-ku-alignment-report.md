---
schema_version: "1.0"
report_id: "<ACCOUNT>-ADRKU-YYYY-NNN"
report_type: "adr-ku-alignment"
title: "ADR–KU Alignment Report — <Account>"
status: "draft"
version: "0.1"
classification: "internal"
customer_shareable_derivative: true

account:
  name: "<Account name>"
  account_id: "<optional internal account identifier>"

ownership:
  owner: "<CSE / EA>"
  reviewer: "<optional reviewer>"

dates:
  created_on: "YYYY-MM-DD"
  last_updated: "YYYY-MM-DD"
  assessment_as_of: "YYYY-MM-DD"
  review_by: "YYYY-MM-DD"

scope:
  included_adr_statuses:
    - accepted
    - proposed
  excluded_adr_statuses:
    - draft
    - superseded
    - deprecated
  program: "<optional program / domain scope>"

evidence_snapshot:
  accepted_adrs: 0
  proposed_adrs: 0
  kus_checked_as_of: "YYYY-MM-DD"
  account_context_as_of: "YYYY-MM-DD"

lineage:
  supersedes: null
  superseded_by: null
---

# ADR–KU Alignment Report — <Account>

## Purpose and boundary

This report reviews <Account>'s **Accepted and Proposed ADRs** for <program/scope>, their related Knowledge Units, and relevant account context.

It is not a complete assessment of <Account>'s architecture.

**Accepted ADRs** are treated as governing decisions. **Proposed ADRs** are assessed and flagged, but are not counted as governing architecture.

The report distinguishes:

- **Declared Alignment** — recorded in the ADR;
- **Observed Alignment** — current CSE / EA assessment.

Observed Alignment does not modify the ADR.

## 1. Account Context 🟢 headline / 🔒 account-note detail

**Account:** <brief account context>

**Program:** <program / domain>

**Current program state:** <current state>

**Relevant internal notes:**

- <date>: <relevant customer/account context>

These notes affect prioritization and discovery but are not architecture evidence by themselves.

## 2. Decision Portfolio Inventory 🟢

### Governing portfolio — Accepted ADRs

| ID | Decision | Review By | Owner |
|---|---|---|---|
| <ADR-ID> | <decision> | <date> | <owner> |

### Pending decisions — Proposed ADRs

| ID | Decision | Review By | Owner |
|---|---|---|---|
| **<ADR-ID> — PROPOSED** | <decision> | <date> | <owner> |

The Proposed ADRs are assessed below but are not counted as governing architecture.

## 3. KU Currency and Alignment Summary 🔒 full detail / 🟢 agreed findings

All cited KUs were checked on **<date>**.

| ADR | ADR status | Cited KU | Current KU state | Declared Alignment | Observed Alignment |
|---|---|---|---|---|---|
| <ADR-ID> | Accepted | <KU-ID> | Approved / current | Aligned | Aligned |
| **<ADR-ID>** | **Proposed** | — | No KU cited | No KU Coverage | No KU Coverage |

### Governing Accepted portfolio

- **<n> Aligned**
- **<n> Conditionally Aligned**
- **<n> Misaligned**
- **<n> Requires Governance Exception**

### Proposed portfolio

- **<n> <alignment>**

This separation prevents pending decisions from being presented as part of the accepted architecture posture.

<!-- Add a focused KU-reference-currency subsection here only when a cited KU is superseded or otherwise materially stale. -->

## 4. Material Findings

### <ADR-ID> — <Decision title>
**Status:** Accepted / Proposed  
**Declared / Observed:** <declared> / <observed>  
**KU:** `<KU-ID>` — <current state>

<Concise evidence-backed interpretation of the ADR, current KU guidance, and material customer context.>

**Finding type:** <type>  
**Risk:** <category, if supported>  
**Priority:** Critical / High / Medium / Low

**Recommended conversation:** <what should be validated or discussed and why now>

## 5. Architecture Whitespace / Discovery Flags 🔒

These are **not confirmed architecture gaps**.

### <Topic>

<Why the topic may be relevant based on known architecture/context.>

**Discovery question:** <what needs to be confirmed?>

## 6. Risk and Governance Rollup 🔒

- **<Risk/category>:** <concise evidence-supported rollup>.

If there is insufficient evidence for Relationship or Renewal Risk, say so explicitly rather than inferring it from technical findings.

## 7. Customer-Success Opportunity Signals 🔒

### Adoption / value realization

- <validated customer problem → opportunity to use owned capability more effectively>

### Expertise / engagement

- <validated customer problem → useful CSE / EA / SA / PS / Support / enablement involvement>

### Capability / expansion

- <validated customer need → possible additional capability; discovery first>

## 8. Trajectory 🔒

<Describe evidence-supported phases/patterns across the decision portfolio.>

Conclude about **architecture decision / governance maturity**, not overall architecture maturity.

## 9. Prioritized CSE / EA Engagement Agenda 🔒

| Priority | Conversation | Why now | Intended outcome | Type |
|---|---|---|---|---|
| 1 | <topic> | <trigger> | <customer outcome> | <finding/action type> |

## 10. Executive Rollup 🟢

<1–3 concise paragraphs covering Accepted vs Proposed portfolio, alignment distribution, KU currency, strongest findings, trajectory, and most useful next actions.>

## 11. Customer-Shareable Derivative Guidance 🔒

**Retain:**

- program scope;
- Accepted / Proposed distinction;
- validated KU status and alignment findings;
- factual governance and execution observations;
- constructive discovery questions;
- architecture conversation topics.

**Remove or reframe:**

- internal account notes;
- commercial or expansion interpretation;
- Relationship / Renewal assessment;
- unvalidated hypotheses;
- internal account strategy and prioritization rationale.

A customer derivative should read as an **architecture decision review and discussion agenda**, not an account-health or commercial document.
