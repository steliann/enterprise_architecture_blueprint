---
type: "consumer-inventory"
artifact_type: "Architecture Blueprint"
schema_version: 1
document_type: "Consumer Inventory"
customer: "Example Research Council"
solution: "Funding Data Service"
status: "Working"
last_updated: "2026-08-01"
record_pattern: "CON-NNN"
---

# Example Research Council — Funding Data Service Consumers

## Purpose

Define the consumer groups that participate in business outcomes or consume managed information.

## Boundary Rules

Consumers are people, teams, organisations, public audiences, or systems using the information. Technology components are excluded.

## Consumer Classification

| Classification | Meaning |
| --- | --- |
| Analytical | Uses information for analysis and decisions. |
| Governance and assurance | Assures completeness and accountability. |

## Consumer Overview

| ID | Consumer | Classification | Primary need | Main access pattern |
| --- | --- | --- | --- | --- |
| CON-001 | Finance Analysts | Analytical | Reconcile payments and commitments | Governed analytical dataset |
| CON-002 | Audit and Assurance | Governance and assurance | Verify coverage and traceability | Approved reports and extracts |

## Detailed Consumer Definitions

### CON-001 — Finance Analysts

**Definition.** Finance specialists responsible for monthly spend analysis.

**Purpose and decisions.** Reconcile payment actuals to approved commitments and investigate exceptions.

**Information needs.** Payment, commitment, recipient, period, and reconciliation status.

**Access pattern.** Governed analytical dataset and approved reports.

**Related records.** [UC-001](business-use-cases/UC-001-financial-accountability.md) and [DP-001](data-products/DP-001-finance-accountability-dataset.md).

**Open points.** Confirm accountable product owner and month-end sign-off role.

### CON-002 — Audit and Assurance

**Definition.** Internal or external stakeholders who need defensible evidence of financial completeness.

**Purpose and decisions.** Determine whether reported spend is complete, traceable, and appropriately reconciled.

**Information needs.** Coverage measures, exceptions, lineage, and restatement history.

**Access pattern.** Approved reports and controlled extracts.

**Related records.** [UC-001](business-use-cases/UC-001-financial-accountability.md) and [DP-001](data-products/DP-001-finance-accountability-dataset.md).

**Open points.** Confirm formal acceptance criteria.

## Consumer-to-Use-Case Matrix

| Consumer | Related use cases |
| --- | --- |
| CON-001 | UC-001 |
| CON-002 | UC-001 |

## Cross-Consumer Architecture Implications

The product must support analytical exploration while preserving a stable, traceable result for assurance.

## Open Questions

- Who formally approves month-end completeness?

## Maintenance Rules

Assign stable CON identifiers and preserve separate consumer groups when their decisions or access controls differ.
