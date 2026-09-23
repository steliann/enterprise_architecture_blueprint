# Mapping Guide

## Relationship model

```text
Business Objective 1 ──primary_business_use_cases──> 1..* Business Use Case
Technical Objective 1 ──source_recommendations─────> 1..* Architecture Recommendation
Technical Objective 1 ──business_objectives────────> 1..* Business Objective
```

Relationship fields are always YAML lists.

## Recommendation → Technical Objective

Default to one active recommendation per TO because it gives clean CSP traceability and closure semantics.

A recommendation may map to an existing TO when the objective outcome is semantically equivalent. The TO wording should not be copied mechanically from the recommendation title.

### Consolidation exception

Multiple recommendations may map to one TO only when:
- they are inseparable parts of one measurable capability outcome;
- they share the same acceptance authority and closure evidence;
- separate TOs would duplicate the same success measures;
- the consolidation rationale is documented.

The validator reports non-one-to-one mapping as a warning unless strict mode is requested.

## Technical Objective → Business Objective

Map a TO only to BOs whose outcomes materially depend on that technical condition.

Evidence sources, strongest first:
1. recommendation `affected_elements.use_cases`;
2. originating gap/use-case relationships;
3. affected data products/capabilities that are already traced to BO primary use cases;
4. explicit review narrative linking the recommendation to business consumers/outcomes;
5. prior CSP mapping that remains semantically valid.

Do not map every enterprise/platform objective to every BO merely because the capability is shared.

## Business Objective → Business Use Case

A BO must be anchored to one or more authoritative use cases. A technical recommendation is not a substitute for business-use-case evidence.

## Recommendation metadata inheritance

For a one-recommendation TO:
- `horizon` should equal recommendation horizon;
- `impact` should equal recommendation impact;
- `category` should normally equal recommendation category;
- TO confidence may inherit recommendation confidence unless stronger/weaker evidence is explicitly justified.

## Review validation items

`VAL-*` items describe uncertainty/evidence needs and do not automatically become CSP objectives. They can appear as dependencies or validation prerequisites for a TO only when relevant.
