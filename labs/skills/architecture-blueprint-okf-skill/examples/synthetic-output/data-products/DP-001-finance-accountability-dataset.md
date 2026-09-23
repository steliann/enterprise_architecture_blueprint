---
type: "data-product"
artifact_type: "Data Product"
schema_version: 1
id: "DP-001"
title: "Finance Accountability Dataset"
status: "Confirmed"
confidence: "High"
supports_use_cases:
  - "UC-001"
provides_required_capabilities:
  - "RC-001"
produced_or_updated_by:
  - "DF-001"
assured_by_quality_controls:
  - "QC-001"
operated_by_capabilities:
  - "OC-001"
shaped_by_adrs:
  - "ADR-001"
created_on: "2026-08-01"
last_updated: "2026-08-01"
---

# DP-001 — Finance Accountability Dataset

## Product Purpose

Provide a governed monthly representation of payment actuals, approved commitments, and reconciliation exceptions.

## Consumers

- [CON-001 — Finance Analysts](../consumers.md#con-001--finance-analysts)
- [CON-002 — Audit and Assurance](../consumers.md#con-002--audit-and-assurance)

## Information Provided

- Payment actuals
- Approved commitments
- Matching status
- Coverage and exception measures

## Delivery Form

Governed relational analytical dataset with approved reporting outputs.

## Business Use Cases Supported

- [UC-001 — Financial Accountability](../business-use-cases/UC-001-financial-accountability.md)

## Required Capabilities Provided

- [RC-001 — Reconciled Financial Representation](../required-capabilities/RC-001-reconciled-financial-representation.md)

## Data Flows

- [DF-001 — Finance Actuals Integration](../data-flows/DF-001-finance-actuals-integration.md)

## Quality Controls

- [QC-001 — Payment and Commitment Reconciliation](../quality-controls/QC-001-payment-and-commitment-reconciliation.md)

## Operational Capabilities

- [OC-001 — Scheduled Build Monitoring and Recovery](../operational-capabilities/OC-001-scheduled-build-monitoring-and-recovery.md)

## Architecture Decisions

- [ADR-001 — Use Managed Relational Storage](../architecture-decision-records/ADR-001-use-managed-relational-storage.md)

## Open Questions and Gaps

| Open question or gap | Why it matters |
| --- | --- |
| Confirm product owner and service target. | Required for accountable operation. |
