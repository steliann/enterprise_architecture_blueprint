---
type: "business-use-case"
artifact_type: "Business Use Case"
schema_version: 1
id: "UC-001"
title: "Financial Accountability"
status: "Confirmed"
confidence: "High"
business_area: "Finance and assurance"
purpose_summary: "Establish a reconciled view of actual payments and approved commitments."
business_question: "How much was paid against approved commitments, and can the result be defended?"
related_required_capabilities:
  - "RC-001"
related_data_products:
  - "DP-001"
known_consumers:
  - "CON-001"
  - "CON-002"
created_on: "2026-08-01"
last_updated: "2026-08-01"
---

# UC-001 — Financial Accountability

## Purpose

Provide Finance and assurance stakeholders with a reconciled and traceable view of payment actuals linked to approved commitments.

## Primary Business Question

> How much was paid against approved commitments, and can the result be defended?

## Scope and Boundary

**Includes:**

- Payment actuals, approved commitments, matching exceptions, and coverage evidence.

**Excludes:**

- Broad portfolio analysis, public publication, and the operation of data-quality processes as a business outcome.

## Consumers

- [CON-001 — Finance Analysts](../consumers.md#con-001--finance-analysts)
- [CON-002 — Audit and Assurance](../consumers.md#con-002--audit-and-assurance)

## Decisions and Actions Supported

- Reconcile money paid to approved commitments.
- Investigate unmatched or incomplete records.
- Approve a defensible month-end result.

## Required Information

- Payment actuals
- Approved commitments
- Recipient and period
- Matching and coverage exceptions

## Timing and Service Expectations

Monthly availability is required. Real-time processing is not required. The exact month-end cut-off remains open.

## Required Capabilities

- [RC-001 — Reconciled Financial Representation](../required-capabilities/RC-001-reconciled-financial-representation.md)

## Supporting Data Products

- [DP-001 — Finance Accountability Dataset](../data-products/DP-001-finance-accountability-dataset.md)

## Open Questions and Gaps

| Open question or gap | Why it matters |
| --- | --- |
| Define month-end cut-off and approval. | Determines when the result is complete and defensible. |

## Current Assessment

**Status:** Confirmed  
**Confidence:** High

The use case is distinct because success is measured by financial completeness and reconciliation rather than general analytical breadth.
