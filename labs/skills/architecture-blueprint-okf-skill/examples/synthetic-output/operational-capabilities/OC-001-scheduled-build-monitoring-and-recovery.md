---
type: "operational-capability"
artifact_type: "Operational Capability"
schema_version: 1
id: "OC-001"
title: "Scheduled Build Monitoring and Recovery"
status: "Confirmed"
confidence: "High"
operates_or_supports:
  - "DF-001"
  - "DP-001"
architecture_decisions:
  - "ADR-001"
created_on: "2026-08-01"
last_updated: "2026-08-01"
---

# OC-001 — Scheduled Build Monitoring and Recovery

## Capability Statement

Schedule, observe, stop, retry, and recover the finance product build without exposing a partial result.

## Operational Behaviours

- Run source acquisition and product build on an approved schedule.
- Monitor step completion and data-control results.
- Preserve the last successful product on failure.
- Retry recoverable failures and escalate unresolved incidents.

## Operates or Supports

- [DF-001 — Finance Actuals Integration](../data-flows/DF-001-finance-actuals-integration.md)
- [DP-001 — Finance Accountability Dataset](../data-products/DP-001-finance-accountability-dataset.md)

## Architecture Decisions

- [ADR-001 — Use Managed Relational Storage](../architecture-decision-records/ADR-001-use-managed-relational-storage.md)

## Open Questions and Gaps

| Open question or gap | Why it matters |
| --- | --- |
| Define recovery target and support hours. | Required to assess operational fitness. |
