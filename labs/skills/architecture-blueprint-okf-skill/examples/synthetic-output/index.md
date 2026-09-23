---
type: "architecture-blueprint"
artifact_type: "Architecture Blueprint"
okf_version: "0.2"
schema_version: 1
document_type: "Package Index"
template_set: "architecture-blueprint"
template_set_version: "1.0.0"
customer: "Example Research Council"
solution: "Funding Data Service"
status: "Working"
last_updated: "2026-08-01"
---

# Example Research Council — Funding Data Service Architecture Blueprint

## Purpose

This package is the maintained architecture blueprint for Funding Data Service. It connects consumer outcomes and business use cases to required capabilities, managed information products, data movement, trust controls, operating capabilities, technologies, and architecture decisions.

## Start Here

- [High-Level Architecture](high-level-architecture.md)
- [Knowledge Model](knowledge-model.md)
- [Consumers](consumers.md)
- [Sources](sources.md)
- [Technologies](technologies.md)

## Package Inventory

| Record type | Count |
| --- | ---: |
| Business Use Cases | 1 |
| Required Capabilities | 1 |
| Data Products | 1 |
| Data Flows | 1 |
| Quality Controls | 1 |
| Operational Capabilities | 1 |
| Architecture Decision Records | 1 |
| Consumers | 2 |
| Sources | 2 |
| Technologies | 2 |

## Modelling Status

The package distinguishes confirmed, candidate, transitional, target, deprecated, and superseded elements. Unknown ownership, thresholds, service levels, recovery objectives, dates, and rationale remain explicit open questions.

## Folder Structure

```text
architecture-blueprint/
├── index.md
├── high-level-architecture.md
├── knowledge-model.md
├── consumers.md
├── sources.md
├── technologies.md
├── business-use-cases/
├── required-capabilities/
├── data-products/
├── data-flows/
├── quality-controls/
├── operational-capabilities/
└── architecture-decision-records/
```

## Primary Architecture Chain

```text
Consumer → Business Use Case → Required Capability
Source → Data Flow → Data Product → Consumer
Quality Control assures delivery
Operational Capability operates delivery
Technology realizes or constrains implementation
ADR explains architecture-shaping choices
```

## Scope and Maintenance Notes

This blueprint is a maintained architecture understanding, not a low-level design or assessment report. New evidence is merged using stable IDs, explicit change history, and template validation.
