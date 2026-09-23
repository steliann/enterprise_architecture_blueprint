---
artifact_type: Architecture Coverage View
document_type: Coverage Category Report
category_id: <category-id>
category: <Category>
blueprint: <Blueprint name>
blueprint_version: <version>
review_date: YYYY-MM-DD
coverage_model_version: <model-version>
coverage_model_hash: <model-hash>
coverage_dimensions:
  required_field_completeness: <0|0.25|0.5|0.75|1|null>
  relationship_integrity: <0|0.25|0.5|0.75|1|null>
  ownership_and_accountability: <0|0.25|0.5|0.75|1|null>
  lifecycle_state_clarity: <0|0.25|0.5|0.75|1|null>
  end_to_end_traceability: <0|0.25|0.5|0.75|1|null>
  authority_and_interface_contracts: <0|0.25|0.5|0.75|1|null>
  control_thresholds_and_acceptance: <0|0.25|0.5|0.75|1|null>
  operations_monitoring_recovery: <0|0.25|0.5|0.75|1|null>
  security_retention_access: <0|0.25|0.5|0.75|1|null>
  decision_currency_and_rationale: <0|0.25|0.5|0.75|1|null>
category_score: <0-100>
coverage: <level>
status: current
confidence: <high|medium|low|not_assessed>
validation: not_applicable
---

# <Category> - Detailed Coverage Findings

**Category score:** **<score>/100**  
**Coverage:** **<level>**  
**Coverage model:** `<model-hash>`  
**Overall calculated impact:** <impact>  
**First global priority:** <rank>

## Category statistics

| Measure | Result |
|---|---:|
| Findings | <n> |
| High-impact findings | <n> |
| Medium-impact findings | <n> |
| Low-impact findings | <n> |
| Records | <n> |
| Record-level open items | <n> |

## Category assessment

<Explain what is strong, what limits review confidence, and which conclusions must remain conditional.>

## Scoring evidence

Use the resolved coverage rubric. Disabled dimensions must be shown as `Disabled`; enabled but genuinely non-applicable dimensions as `N/A`. The raw score is retained in frontmatter so weight-only recalculation is deterministic.

| Dimension | Enabled | Base weight | Applicability | Raw score 0-1 | Effective category weight | Contribution | Rationale |
|---|---|---:|---|---:|---:|---:|---|
| Required field completeness | <Yes/No> | <weight> | <Yes/N/A> | <value> | <percent> | <points> | <rationale> |
| Relationship integrity | <Yes/No> | <weight> | <Yes/N/A> | <value> | <percent> | <points> | <rationale> |
| Ownership and accountability | <Yes/No> | <weight> | <Yes/N/A> | <value> | <percent> | <points> | <rationale> |
| Lifecycle state clarity | <Yes/No> | <weight> | <Yes/N/A> | <value> | <percent> | <points> | <rationale> |
| End-to-end traceability | <Yes/No> | <weight> | <Yes/N/A> | <value> | <percent> | <points> | <rationale> |
| Authority and interface contracts | <Yes/No> | <weight> | <Yes/N/A> | <value> | <percent> | <points> | <rationale> |
| Control thresholds and acceptance | <Yes/No> | <weight> | <Yes/N/A> | <value> | <percent> | <points> | <rationale> |
| Operations, monitoring and recovery | <Yes/No> | <weight> | <Yes/N/A> | <value> | <percent> | <points> | <rationale> |
| Security, retention and access | <Yes/No> | <weight> | <Yes/N/A> | <value> | <percent> | <points> | <rationale> |
| Decision currency and rationale | <Yes/No> | <weight> | <Yes/N/A> | <value> | <percent> | <points> | <rationale> |

## Ranked findings

### 1. <Finding title>

**Global priority:** <rank>  
**Calculated impact:** <impact>  
**Affected:** <IDs/files>

<Finding statement>

**Override impact:** _Not set_  
**Reviewer comment:** _Required when an override is entered_

## Detailed record findings

### <ID> - <Title>

**Status:** <...>  
**Confidence:** <...>

**Unresolved items**
- <item>

## Category conclusion

<State what the score means for review confidence, not architecture quality.>
