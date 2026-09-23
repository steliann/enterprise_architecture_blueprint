---
type: "source-inventory"
artifact_type: "Architecture Blueprint"
schema_version: 1
document_type: "Source Inventory"
customer: "Example Research Council"
solution: "Funding Data Service"
status: "Working"
last_updated: "2026-08-01"
record_pattern: "SRC-NNN"
---

# Example Research Council — Funding Data Service Sources

## Purpose

Define the real external systems that originate grant commitments and payment actuals.

## Boundary Rules

Only systems outside the Funding Data Service are sources. Queues, files, staging schemas, and warehouse layers are excluded.

## Source Classification

| Classification | Meaning |
| --- | --- |
| Operational system | Originates awards and commitments. |
| Finance system | Originates payment actuals. |

## Source Overview

| ID | Source | Classification | Information supplied | Lifecycle |
| --- | --- | --- | --- | --- |
| SRC-001 | Grant Platform | Operational system | Awards and commitments | Current |
| SRC-002 | Finance Platform | Finance system | Payment actuals | Current |

## Detailed Source Definitions

### SRC-001 — Grant Platform

**Definition.** Operational funding system used to approve awards and commitments.

**Information supplied.** Award identifiers, approved values, recipients, and commitment dates.

**Authoritative role.** Authoritative for approved commitments in this example.

**Interface and cadence.** Nightly managed extract.

**Lifecycle.** Current.

**Related records.** [DF-001](data-flows/DF-001-finance-actuals-integration.md) and [DP-001](data-products/DP-001-finance-accountability-dataset.md).

**Open points.** Confirm schema-change notification process.

### SRC-002 — Finance Platform

**Definition.** Enterprise finance platform that records money paid.

**Information supplied.** Payment actuals, posting dates, recipients, and ledger references.

**Authoritative role.** Authoritative for payment actuals in this example.

**Interface and cadence.** Daily API extraction with monthly reconciliation use.

**Lifecycle.** Current.

**Related records.** [DF-001](data-flows/DF-001-finance-actuals-integration.md) and [DP-001](data-products/DP-001-finance-accountability-dataset.md).

**Open points.** Confirm correction and restatement contract.

## Source-to-Data-Flow Matrix

| Source | Data flows |
| --- | --- |
| SRC-001 | DF-001 |
| SRC-002 | DF-001 |

## Source-to-Data-Product Summary

| Source | Products informed |
| --- | --- |
| SRC-001 | DP-001 |
| SRC-002 | DP-001 |

## Cross-Source Architecture Implications

Commitment and payment records require stable matching keys and explicit reconciliation exceptions.

## Open Questions

- How are unmatched legacy payments handled?

## Maintenance Rules

Assign stable SRC identifiers and exclude transport or internal processing components.
