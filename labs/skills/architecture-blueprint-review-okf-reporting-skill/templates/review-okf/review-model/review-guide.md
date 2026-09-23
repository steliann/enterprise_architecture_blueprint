---
id: ABR-GDE-001
artifact_type: Architecture Blueprint Review Guide
document_type: Method Guide
title: Architecture Blueprint Review Model Guide
model_version: '1.0'
last_updated_date: YYYY-MM-DD
status: current
confidence: high
validation: not_applicable
---

# Architecture Blueprint Review Model Guide

## Purpose

The review answers three questions:

1. Can the available Blueprint be trusted enough for review? - Coverage.
2. What material architecture conditions require resolution? - Gaps.
3. What should change and how will success be verified? - Recommendations.

## End-to-end process

1. Establish and validate the Blueprint baseline.
2. Assess coverage by category.
3. Separate missing knowledge from architecture problems.
4. Create/validate Candidate or Active Gaps.
5. Prioritize the gap register.
6. Form recommendations from gaps, not from features.
7. Build the integrated review.
8. Validate with customer/architecture owners.
9. Govern accepted recommendations through ADRs and initiatives.
10. Validate outcomes before closing gaps.
11. Refresh the Review after material Blueprint/architecture change.

## Gap promotion rule

A missing field is a coverage observation. A potentially material unknown current-state control is a Validation Item. Evidence of a material mismatch supports a Candidate Gap. Customer/design confirmation supports an Active Gap.

## Recommendation rule

State the target condition first. Then distinguish current capabilities, strategic/expanded capabilities and adjacent-domain responsibilities only where they materially affect the path. Do not imply an upgrade or new technology is required when the current architecture can close the gap.

## Customer validation rule

Validation should correct the Blueprint first where possible. Refresh the Review from the corrected Blueprint rather than maintaining two competing current-state descriptions.

## Coverage rubric configuration

The default rubric remains in the skill's `config/defaults.yaml`. If an external `coverage-rubric.yaml` is supplied, merge only the enabled flags and weights for known dimensions. Copy the resolved rubric into the Review OKF under `review-model/coverage-rubric.yaml` and stamp its model hash on all coverage reports.

Weight-only changes do not require evidence reinterpretation when every category retains complete `coverage_dimensions`; recalculate totals from those raw values. Legacy reviews without raw dimension scores require a full coverage rescore.
