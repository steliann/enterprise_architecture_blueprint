---
type: "architecture-decision-record"
artifact_type: "Architecture Decision Record"
schema_version: 1
id: "ADR-001"
title: "Use Managed Relational Storage"
status: "Accepted"
confidence: "Medium"
decision_kind: "Retrospective"
decision_date: null
affected_artifacts:
  - "DP-001"
  - "DF-001"
  - "OC-001"
created_on: "2026-08-01"
last_updated: "2026-08-01"
---

# ADR-001 — Use Managed Relational Storage

## Status

Accepted — Retrospective

## Context

The solution needs a governed relational representation of commitments, payment actuals, matching results, and historical corrections.

## Decision

Use a cloud-managed relational database as the principal analytical storage platform.

## Rationale

The implementation is confirmed. Managed operation and relational query support are observable benefits, but the original comparison, approver, and selection criteria were not documented in the evidence.

## Alternatives Considered or Not Documented

- Self-managed relational database
- Cloud analytical warehouse
- Lakehouse storage and query pattern
- Original alternatives were not documented.

## Consequences

### Positive

- Relational integrity and familiar query access.
- Managed backup and availability features.

### Negative and Trade-Offs

- Platform-specific scaling and cost characteristics.
- Potential coupling of transformation design to the database engine.

## Affected Blueprint Records

- [DP-001 — Finance Accountability Dataset](../data-products/DP-001-finance-accountability-dataset.md)
- [DF-001 — Finance Actuals Integration](../data-flows/DF-001-finance-actuals-integration.md)
- [OC-001 — Scheduled Build Monitoring and Recovery](../operational-capabilities/OC-001-scheduled-build-monitoring-and-recovery.md)
- [TECH-001 — Managed Relational Database](../technologies.md#tech-001--managed-relational-database)

## Open Items

| Open item | Why it matters |
| --- | --- |
| Recover the original decision criteria and approver. | Required to validate whether the decision remains appropriate. |
