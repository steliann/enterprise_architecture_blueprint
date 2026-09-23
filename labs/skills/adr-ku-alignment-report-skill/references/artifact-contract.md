# Artifact Contract

## Canonical artifact

### `adr-ku-alignment-report.md`

- Audience: internal CSE/EA and account team.
- Authority: source of truth for this evidence snapshot.
- Contains: ADR/KU assessment + relevant customer context + internal risk/opportunity interpretation + engagement agenda.
- Lifecycle: draft → proposed → approved → superseded.


## Presentation contract

The ACME and Northstar internal reports are the canonical presentation patterns for `adr-ku-alignment-report.md`. The Operating Model governs analysis semantics; the examples govern visible structure and information density. Internal analysis classifications such as Direct / Adjacent / Contextual need not be exposed unless they materially improve understanding.

## Derived artifacts

Derived outputs must be generated from the canonical report and must not perform an independent assessment.

### Customer-facing architecture decision review

Purpose: share validated decision/governance/execution findings with the customer.

Rules:

- remove internal commercial/account-health framing;
- remove sensitive notes and unvalidated hypotheses;
- use collaborative language (“validate together”, “review”, “confirm”);
- retain traceability to ADR/KU evidence;
- contextual ADRs appear only if they help the customer understand a dependency/constraint.

### Customer workshop content / presentation

Purpose: facilitate validation and decision discussion.

Recommended content:

- project context;
- what was reviewed;
- portfolio view;
- what remains strong;
- what should be validated together;
- governance/execution follow-ups;
- discovery questions;
- workshop flow;
- agreed outcomes.

### CSE/EA preparation plan

Purpose: turn report findings into continuing internal account work.

Use exactly seven top-level phases:

1. Prepare
2. Validate
3. Workshop
4. Govern
5. Execute
6. Discover
7. Refresh

Account-specific actions are subtasks under those phases.

Every ADR/KU reference should link to the governed artifact when a URL is available.
