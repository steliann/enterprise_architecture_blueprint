---
type: "data-flow"
artifact_type: "Data Flow"
schema_version: 1
id: "DF-001"
title: "Finance Actuals Integration"
status: "Confirmed"
confidence: "High"
source: "SRC-001 and SRC-002"
target: "DP-001"
frequency: "Daily ingestion; monthly assurance use"
produces_or_updates:
  - "DP-001"
quality_controls:
  - "QC-001"
operational_capabilities:
  - "OC-001"
architecture_decisions:
  - "ADR-001"
created_on: "2026-08-01"
last_updated: "2026-08-01"
---

# DF-001 — Finance Actuals Integration

## Purpose

Combine approved commitments and payment actuals to update the Finance Accountability Dataset.

## Source and Target

| Boundary | Value |
| --- | --- |
| Source | [SRC-001](../sources.md#src-001--grant-platform) and [SRC-002](../sources.md#src-002--finance-platform) |
| Target | [DP-001](../data-products/DP-001-finance-accountability-dataset.md) |
| Frequency | Daily ingestion; monthly assurance use |

## Flow Steps

1. Acquire approved commitments from the Grant Platform.
2. Acquire payment actuals from the Finance Platform.
3. Standardise identifiers and periods.
4. Match payments to commitments.
5. Validate reconciliation and publish the successful result.

## Data Products Produced or Updated

- [DP-001 — Finance Accountability Dataset](../data-products/DP-001-finance-accountability-dataset.md)

## Quality Controls

- [QC-001 — Payment and Commitment Reconciliation](../quality-controls/QC-001-payment-and-commitment-reconciliation.md)

## Operational Capabilities

- [OC-001 — Scheduled Build Monitoring and Recovery](../operational-capabilities/OC-001-scheduled-build-monitoring-and-recovery.md)

## Architecture Decisions

- [ADR-001 — Use Managed Relational Storage](../architecture-decision-records/ADR-001-use-managed-relational-storage.md)

## Risks and Open Questions

| Risk or open question | Why it matters |
| --- | --- |
| Source identifiers may not match consistently. | Unmatched records reduce financial completeness. |
