---
name: adr-ku-alignment-report
description: Create or refresh an internal ADR–KU Alignment Report for one customer account from Accepted/Proposed ADRs, current Knowledge Units, and current customer/account context. Use the full ADR knowledge available, classify ADRs as Direct/Adjacent/Contextual during analysis, keep contextual ADRs out of alignment metrics, revalidate KU currency, distinguish Declared from Observed Alignment, and present the result using the canonical ACME/Northstar report pattern.
---

# ADR–KU Alignment Report Skill

## Purpose

Use this skill to create or refresh the canonical internal artifact:

`adr-ku-alignment-report.md`

for a single customer account.

The report is a focused account-level review of the customer’s **architecture decision and governance posture**. It is not a full Architecture Blueprint and must not claim architecture completeness or overall architecture maturity.

The skill combines three evidence pillars:

1. **ADRs** — what the customer decided, why, and under what constraints/conditions.
2. **KUs** — what current reusable Qlik/Talend architecture knowledge says now, including technology changes reflected through KU updates/supersession.
3. **Customer/account context** — what is happening around the decision now: objectives, adoption, incidents, blockers, staffing, governance, milestones, customer feedback, and engagement notes.

The purpose is to determine **what remains sound, what needs attention, what requires validation or discovery, and what conversation/action should come next**.

## Authority hierarchy

Use the package sources with two complementary forms of authority:

1. `references/purpose-and-operating-model.md` — **normative methodology and analysis semantics**.
2. `references/concept-overview.md` — framing, value proposition, and boundaries.
3. `examples/acme/adr-ku-alignment-report.md` and `examples/northstar/adr-ku-alignment-report.md` — **canonical presentation patterns**.
4. `templates/adr-ku-alignment-report.md` — generalized implementation of the canonical presentation pattern.

The Operating Model determines **what must be analyzed and what conclusions are legitimate**. The ACME and Northstar examples determine **how the canonical report is presented** unless a case-specific finding requires a small additional subsection.

Do not add visible fields, columns, or sections merely because they are useful internally during analysis. In particular, Direct / Adjacent / Contextual relevance is an analysis classification and is surfaced only when it materially improves understanding of a reported finding or dependency.

## Canonical presentation rule

Generated reports should follow the ACME/Northstar pattern:

- YAML front matter;
- report title and, where relevant, example/classification notice;
- `Purpose and boundary`;
- exactly eleven numbered top-level sections:
  1. Account Context
  2. Decision Portfolio Inventory
  3. KU Currency and Alignment Summary
  4. Material Findings
  5. Architecture Whitespace / Discovery Flags
  6. Risk and Governance Rollup
  7. Customer-Success Opportunity Signals
  8. Trajectory
  9. Prioritized CSE / EA Engagement Agenda
  10. Executive Rollup
  11. Customer-Shareable Derivative Guidance

The structure is intentionally compact. Evidence traceability may be carried by Material Findings rather than repeated in every summary table.

## When to use

Use when the user asks to create or refresh an ADR–KU Alignment Report, review an ADR portfolio against KUs, identify decision/governance findings from ADRs + KUs + account context, or produce the canonical internal source for downstream customer-facing and CSE/EA artifacts.

Do not use this skill as a substitute for a full Architecture Blueprint analysis.

## Inputs

Consume as much relevant account knowledge as is available.

Expected inputs include customer/account identity, ADR corpus, KU corpus or resolvable KU references, current customer/account context, and assessment date. Previous reports, engagement notes, account objectives, adoption/entitlement information, incidents, delivery milestones, and workshop outcomes are useful where available.

If data is missing, do not invent it. Mark uncertainty explicitly and create discovery questions where appropriate.

## Core workflow

### 1. Ingest the full ADR knowledge available

Read all ADR knowledge needed to understand the account, including decisions that are not about Qlik/Talend.

Only Accepted and Proposed ADRs can enter the current decision assessment. Draft, Superseded, and Deprecated ADRs are excluded from current metrics, though historical ADRs may be consulted for rationale/evolution.

### 2. Classify ADR relevance internally before alignment

Classify each Accepted/Proposed ADR considered as:

- **Direct** — Qlik/Talend technology or a pattern for which Qlik has clear advisory ownership. Full ADR–KU assessment.
- **Adjacent** — primarily third-party/edge technology, but materially constrains, integrates with, or changes Qlik/Talend architecture. Assess only the Qlik-relevant boundary/implication.
- **Contextual** — useful to understand the customer architecture, standards, dependencies, or rationale, but Qlik/Talend guidance is not materially applicable. Use as supporting knowledge only.

Rules:

- Contextual ADRs do not enter alignment distributions or ADR–KU portfolio metrics.
- Contextual ADRs are never `No KU Coverage`.
- Contextual ADRs normally stay out of the visible Decision Portfolio Inventory.
- Surface a contextual ADR only when it materially explains another reported finding/dependency, and do so in Account Context, the relevant Material Finding, or a brief dependency note rather than creating a mandatory standalone inventory.
- Adjacent ADRs enter metrics only when a genuine Qlik/Talend-relevant assessment was made.

### 3. Revalidate KU currency

For every cited/relevant KU, check existence, lifecycle status, supersession/successor, confidence/maturity where available, and continued applicability.

Technology changes on the Qlik side should normally enter the assessment through KU evolution.

If a KU is superseded, use successor guidance where possible, flag the ADR reference for governance review, and do not silently edit the ADR. Add a focused subsection under Section 3 only when there is an actual KU-currency issue, as demonstrated by Northstar.

### 4. Assess customer/account context

Treat customer context as a first-class evidence pillar. Distinguish confirmed fact, credible observation, and working hypothesis when reliability materially affects a conclusion.

Context changes interpretation and priority; it does not replace architecture evidence.

In the report, prefer the compact ACME/Northstar narrative style. Do not force reliability labels onto every bullet when the facts are clear; qualify only the material uncertain observations.

### 5. Compare Declared and Observed Alignment

Declared Alignment is the outcome recorded in the ADR. Observed Alignment is the current CSE/EA assessment based on:

`ADR evidence + current KU guidance + current customer context`

Typical outcomes are Aligned, Conditionally Aligned, Misaligned, Requires Governance Exception, and No KU Coverage.

Show both values in Section 3. Explain material differences in Section 4. Observed Alignment is advisory and never silently rewrites the ADR.

### 6. Generate material findings

Use the applicable finding type:

- Decision revisit
- Governance follow-up
- Execution follow-up
- Proposed-decision review
- KU coverage gap
- KU reference currency
- Architecture whitespace / discovery flag

Follow the canonical compact finding pattern:

- heading with ADR ID and decision title;
- Status;
- Declared / Observed;
- KU where applicable;
- concise evidence-backed explanation;
- Finding type;
- Risk where supported;
- Priority;
- Recommended conversation where useful.

Do **not** add mandatory visible `Relevance`, `Assessment scope`, or `Shareability` fields to every finding. Those may be stated only when materially useful.

### 7. Derive risks carefully

Allowed risk categories are Architecture, Governance, Delivery, Operational, Adoption, Relationship, and Renewal.

Relationship/Renewal risk require explicit supporting account context. Never infer them automatically from a technical finding.

Present Section 6 as the compact narrative rollup used by the canonical examples. A table is optional only if the case is too complex for concise bullets.

### 8. Derive opportunities from validated customer need

Use the three canonical subsections:

- Adoption / value realization
- Expertise / engagement
- Capability / expansion

The customer problem comes first. Do not create product pitches from whitespace or technical findings alone.

### 9. Analyze the portfolio, not only individual ADRs

Look for dependencies, recurring exceptions/root causes, stale temporary decisions, repeated execution issues, domain concentration, Proposed ADRs revealing operating-model patterns, changes in KU use, and customer context repeatedly shaping architecture choices.

Trajectory describes **architecture decision/governance maturity**, not overall architecture maturity.

### 10. Produce the engagement agenda

Use the canonical compact table:

`Priority | Conversation | Why now | Intended outcome | Type`

The supporting ADR/KU/context evidence should already be traceable through the corresponding Material Findings. Do not duplicate evidence columns or participant columns unless a specific use case requires them.

Recommend a conversation/validation step, not a new customer architecture decision made on the customer’s behalf.

### 11. Classify content for sharing

The canonical report is internal. Section 11 states what to retain and what to remove/reframe for a customer-facing derivative.

### 12. Validate and save

Create/refresh `adr-ku-alignment-report.md` using the template and run:

`python scripts/validate_report.py <path-to-report>`

Do not mark the report Approved unless it has actually been internally reviewed/approved.

## Create vs refresh behavior

### Create

Use the template and generate a new `report_id`.

### Refresh during Draft/Proposed review

If the evidence snapshot is materially the same and the assessment is simply being refined, preserve `report_id`, increment `version`, and update `last_updated`.

### New assessment snapshot

If ADRs, KUs, or customer context have materially changed, normally create a new `report_id` and use lineage to supersede the previous approved assessment.

## Presentation guardrails

- Treat ACME and Northstar as canonical exemplars of report density and structure.
- Do not expand the visible report simply to expose internal analysis mechanics.
- Accepted and Proposed ADRs must remain visibly distinct.
- Proposed ADRs must never be counted as governing architecture.
- Contextual ADRs must never pollute alignment counts or appear as No KU Coverage.
- Whitespace is a discovery prompt, not a confirmed gap.
- Keep the report bounded to architecture decision/governance posture.
- Preserve the customer-facing derivative guidance as the final section.
