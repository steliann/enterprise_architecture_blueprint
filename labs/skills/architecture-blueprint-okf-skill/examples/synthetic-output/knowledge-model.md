---
type: "knowledge-model"
artifact_type: "Architecture Blueprint"
schema_version: 1
document_type: "Knowledge Model"
customer: "Example Research Council"
solution: "Funding Data Service"
status: "Working"
last_updated: "2026-08-01"
---

# Example Research Council — Funding Data Service Knowledge Model

## Purpose

Define the concepts and relationships used by the synthetic blueprint.

## Conceptual Model

```text
CON-001 and CON-002 participate in UC-001 and consume DP-001.
UC-001 requires RC-001.
SRC-001 and SRC-002 feed DF-001.
DF-001 updates DP-001.
QC-001 assures DF-001 and DP-001.
OC-001 operates DF-001 and DP-001.
TECH-001 and TECH-002 realize the implementation.
ADR-001 shapes DP-001, DF-001, and OC-001.
```

## Concepts

| Concept | Identifier | Example |
| --- | --- | --- |
| Consumer | CON-NNN | CON-001 Finance Analysts |
| Source | SRC-NNN | SRC-001 Grant Platform |
| Technology | TECH-NNN | TECH-001 Managed Relational Database |
| Business Use Case | UC-NNN | UC-001 Financial Accountability |
| Required Capability | RC-NNN | RC-001 Reconciled Financial Representation |
| Data Product | DP-NNN | DP-001 Finance Accountability Dataset |
| Data Flow | DF-NNN | DF-001 Finance Actuals Integration |
| Quality Control | QC-NNN | QC-001 Payment and Commitment Reconciliation |
| Operational Capability | OC-NNN | OC-001 Scheduled Build Monitoring and Recovery |
| Architecture Decision Record | ADR-NNN | ADR-001 Use Managed Relational Storage |

## Relationship Semantics

The standard skill relationships apply without customer-specific extensions.

## Evidence, Status, and Confidence

The public records state conclusions and open questions. Detailed provenance is maintained under `.okf`.

## Identifier and File Rules

Identifiers are stable and filenames begin with the identifier followed by a lowercase hyphenated title.

## Modelling Rules

Business outcomes are modelled before implementation. Data quality remains under Quality Controls, operations remain under Operational Capabilities, and only real external systems are Sources.

## Folder Structure

The package uses the canonical top-level documents and seven record collections defined by template set 1.0.0.

## Template and Schema Governance

The package is locked to Architecture Blueprint OKF 0.2 and template set 1.0.0.
