---
artifact_type: Customer Success Plan Objective Knowledge Model
schema_version: 2
title: Customer Success Plan Objective Knowledge Model
status: current
confidence: high
validation: not_applicable
last_updated_date: '{{YYYY-MM-DD}}'
---

# Customer Success Plan Objective Knowledge Model

## Concepts

### Business Use Case

A source artifact in the architecture blueprint that describes the business purpose, consumers, decisions, required information and service expectations.

### Business Objective

A Customer Success Plan outcome connected to one or more primary business use cases. It expresses the business condition the customer intends to achieve and the measures by which that outcome will be accepted.

### Technical Objective

A measurable architecture outcome connected to one or more architecture recommendations and one or more business objectives.

### Architecture Recommendation

A source artifact in the architecture blueprint review that describes a target improvement, delivery path and architecture acceptance measures.

### Milestone

A future Customer Success Plan planning artifact that records a verifiable intermediate result, owner and date contributing to a technical or business objective. Milestones are intentionally not created in this OKF unless delivery ownership and dates have been agreed.

## Authoritative Relationships

```text
Business Objective 1 ──primary_business_use_cases──> 1..* Business Use Case
Technical Objective 1 ──source_recommendations─────> 1..* Architecture Recommendation
Technical Objective 1 ──business_objectives────────> 1..* Business Objective
Technical Objective 1 ──delivered through──────────> 0..* Milestone
```

## State Model

- `status`: architecture position (`target` or `transitional`).
- `objective_state`: governance maturity (`draft`, `proposed`, `approved`, `achieved`, `withdrawn`, `superseded`).
- `planning_state`: CSP execution (`not_planned`, `planned`, `in_progress`, `at_risk`, `blocked`, `completed`, `cancelled`).

## Integrity Rules

1. Every business objective references at least one valid `primary_business_use_cases` ID.
2. Every technical objective references at least one valid `source_recommendations` ID.
3. Every technical objective references at least one valid `business_objectives` ID.
4. Relationship fields are ID lists.
5. Business success measures describe customer outcomes; technical success measures describe architecture outcomes.
6. Implementation completion alone does not make an objective achieved; acceptance evidence is required.
7. IDs are immutable. Material replacement creates a new objective.
8. IDs, not file paths, are authoritative for relationships.
9. Horizon is sequencing and is not a committed date.
10. Owners, baselines, targets, dates and acceptance evidence must be completed before an objective becomes an approved CSP commitment.
