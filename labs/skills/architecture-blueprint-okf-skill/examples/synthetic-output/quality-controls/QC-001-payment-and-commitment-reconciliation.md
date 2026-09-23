---
type: "quality-control"
artifact_type: "Quality Control"
schema_version: 1
id: "QC-001"
title: "Payment and Commitment Reconciliation"
status: "Confirmed"
confidence: "High"
control_type: "Mixed"
applies_to:
  - "DF-001"
  - "DP-001"
created_on: "2026-08-01"
last_updated: "2026-08-01"
---

# QC-001 — Payment and Commitment Reconciliation

## Control Objective

Prevent an incomplete or internally inconsistent finance product from replacing the last successful result.

## Control Type

Mixed preventive and detective control.

## Control Method

Check duplicate identifiers, unmatched payments, missing commitments, and overall coverage before product publication.

## Failure or Exception Action

Stop publication, preserve the last successful product, alert operations, and create an exception for investigation.

## Applies To

- [DF-001 — Finance Actuals Integration](../data-flows/DF-001-finance-actuals-integration.md)
- [DP-001 — Finance Accountability Dataset](../data-products/DP-001-finance-accountability-dataset.md)

## Open Questions and Gaps

| Open question or gap | Why it matters |
| --- | --- |
| Confirm accepted exception and coverage thresholds. | Determines pass or fail behaviour. |
