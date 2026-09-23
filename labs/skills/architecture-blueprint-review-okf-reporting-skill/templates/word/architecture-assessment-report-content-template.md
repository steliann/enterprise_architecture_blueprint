# <Customer> - Architecture Gaps and Recommendations

**Status:** <Draft for validation / Final>  
**Version:** <version>  
**Date:** <date>  
**Prepared by:** <team/role>

# About this architecture assessment

This report assesses the fitness of **<Customer>** architecture against the outcomes represented in the reviewed Architecture Blueprint and the current/target conditions recorded in the Architecture Blueprint Review.

The assessment considers the current architecture, operating model, known transitions and required capabilities. It distinguishes incomplete information from evidenced architecture mismatches and presents each material finding together with its corresponding response.

The assessment is intended as a structured basis for architecture discussion and planning, not as an audit or compliance verdict unless explicitly scoped otherwise.

## How to read this document

Each detailed assessment is presented vertically. The **Architecture finding** explains the expected/current condition, mismatch and impact. The **Recommendation** follows immediately with the target direction, response path, benefits and validation/acceptance points.

## Scope

- <scope item>

## Evidence rule

A finding is recorded as a gap only when the expected architecture condition is sufficiently clear, the current condition is sufficiently evidenced, and a material mismatch can be stated. Unknown or undocumented information remains a coverage finding or Validation Item.

# Executive assessment

<3-5 paragraphs summarizing the architecture position, dominant themes and review confidence.>

## Portfolio KPIs

| KPI | Value | Interpretation |
|---|---:|---|
| Candidate + Active gaps | <n> | <meaning> |
| High/Critical priority | <n> | <meaning> |
| Validation items | <n> | Not counted as gaps |
| Recommendations | <n> | <mapping statement> |

## Priority discussion areas

- **<Theme>.** <Short direction>

# Assessment approach and classification

The review starts from the validated architecture baseline and asks whether the current or intended implementation is fit for the outcomes represented in the Blueprint.

## How findings are promoted

| Classification | Meaning | Treatment |
|---|---|---|
| Coverage finding | Information is incomplete, weakly traced or inconsistent. | Retain as review-confidence evidence. |
| Validation item | A potentially material concern exists, but the current condition is not sufficiently evidenced. | Validate before gap classification. |
| Candidate gap | Evidence is sufficient to state a material mismatch, but customer/design confirmation remains. | Discuss and validate; recommendation can be prepared conditionally. |
| Active gap | The material mismatch is confirmed. | Govern remediation, priority and architecture change. |

## How recommendations are categorized

| Response class | Architecture ownership | Typical use |
|---|---|---|
| Current capability | Primary response can be implemented using capabilities already available. | Optimisation, control closure, operational hardening. |
| Strategic / expanded capability | A strategic capability provides a materially different managed path. | Target-state simplification or platform evolution. |
| Adjacent technology / domain | The primary decision sits outside the reviewed platform, which may still enable part of the solution. | Platform, security, governance or business-domain decisions. |
| Hybrid | Response spans more than one of the above. | Cross-domain target architecture. |

## Benefit model

| Benefit | Architecture value |
|---|---|
| Reliability & Risk | Resilience, recoverability, integrity, security/compliance and risk reduction. |
| Operational Efficiency | Reduced manual work, maintenance, troubleshooting and operational complexity. |
| Performance & Scalability | Improved throughput, latency, concurrency, elasticity and workload predictability. |
| Agility & Time to Value | Easier change, onboarding, automation and reuse. |
| Governance & Architectural Sustainability | Better ownership, standardisation, traceability, lifecycle management and lower technical debt. |

## Coverage constraints that affect interpretation

- Overall review-confidence score: <score/level>.
- <important limitation>

# Findings and recommendations at a glance

| Architecture finding | Priority | State | Response path | Horizon |
|---|---|---|---|---|
| <Gap title> | High | Candidate | Hybrid | Next |

## Validation items - deliberately not gaps

| Observation | Required validation |
|---|---|
| <VAL title> | <evidence> |

# Detailed architecture findings and recommended responses

> Repeat the following block once for every in-scope gap.

## <Gap title>

**CATEGORY:** <lens/category>

| PRIORITY | CONFIDENCE | RESPONSE | HORIZON |
|---|---|---|---|
| <High> | <High> | <Response class> | <Now/Next/Later> |

### Architecture finding

#### Expected architecture condition

<Expected condition>

#### Architecture context / current condition

<Current evidence and context>

#### Architecture gap

<Precise mismatch>

#### Impact if not addressed

- <impact>

### Recommendation

#### Recommended architectural direction

<Target condition/direction>

#### Current capability path

<If applicable>

#### Strategic / expanded path

<If applicable>

#### Adjacent-domain responsibilities

<If applicable>

#### Expected benefits

- **<Benefit class>** - <benefit>

#### Acceptance / validation

- <measure or validation question>

#### Traceability

<GAP, REC and Blueprint IDs>

# Cross-gap architecture themes

## <Theme>

<Synthesize recurring pressure or design principle across several gaps.>

# Validation items and evidence to capture

## <VAL title>

<Why it is not a gap and what evidence is needed.>

# Aggregated architecture conclusions

The detailed assessment records gaps independently. The following conclusions synthesize several findings and are **not additional gap records**.

| Aggregated finding | Target direction |
|---|---|
| <Finding> | <Direction> |

## <Aggregated conclusion title>

### Architecture conclusion

<Executive synthesis>

### Recommended architectural direction

<Target direction backed by several detailed recommendations.>

# Assessment disposition

<State the next validation/decision/governance step.>

## Decision point

A Candidate Gap becomes Active only after the current condition and materiality are confirmed. Recommendation acceptance should drive the corresponding ADR, Blueprint and delivery-plan changes.

# Document status

| Item | Value |
|---|---|
| Version | <version> |
| Date | <date> |
| Status | <status> |
| Source baseline | <Blueprint name/version> |
| Source review | <Review name/version> |
