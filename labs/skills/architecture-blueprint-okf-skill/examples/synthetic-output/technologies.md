---
type: "technology-inventory"
artifact_type: "Architecture Blueprint"
schema_version: 1
document_type: "Technology Inventory"
customer: "Example Research Council"
solution: "Funding Data Service"
status: "Working"
last_updated: "2026-08-01"
record_pattern: "TECH-NNN"
---

# Example Research Council — Funding Data Service Technologies

## Purpose

Define named technologies that materially realize or constrain the example solution.

## Boundary Rules

Include identifiable platforms and material implementation choices. Exclude sources, products, generic protocols, and intermediate stages.

## Technology Classification

| Classification | Meaning |
| --- | --- |
| Data storage platform | Stores governed analytical data. |
| Data integration platform | Acquires and transforms source data. |

## Technology Overview

| ID | Technology | Classification | Deployment context | Lifecycle |
| --- | --- | --- | --- | --- |
| TECH-001 | Managed Relational Database | Data storage platform | Cloud-managed warehouse | Current |
| TECH-002 | Managed Integration Service | Data integration platform | Scheduled source ingestion | Current |

## Detailed Technology Definitions

### TECH-001 — Managed Relational Database

**Definition.** Cloud-managed relational database selected for the analytical warehouse.

**Classification.** Data storage platform.

**Architectural role.** Stores curated commitment, payment, and reconciliation data.

**Deployment context.** Managed cloud service; exact engine and topology are intentionally synthetic.

**Lifecycle.** Current.

**Related records.** [ADR-001](architecture-decision-records/ADR-001-use-managed-relational-storage.md) and [DP-001](data-products/DP-001-finance-accountability-dataset.md).

**Key open points.** Confirm capacity, recovery, upgrade, and ownership policies.

### TECH-002 — Managed Integration Service

**Definition.** Scheduled integration platform used to acquire and transform source data.

**Classification.** Data integration platform.

**Architectural role.** Implements [DF-001](data-flows/DF-001-finance-actuals-integration.md).

**Deployment context.** Managed runtime with scheduled daily execution.

**Lifecycle.** Current.

**Related records.** [DF-001](data-flows/DF-001-finance-actuals-integration.md) and [OC-001](operational-capabilities/OC-001-scheduled-build-monitoring-and-recovery.md).

**Key open points.** Confirm promotion and runtime support model.

## Maintenance Rules

Assign stable TECH identifiers and record coexistence, replacement, or retirement explicitly.
