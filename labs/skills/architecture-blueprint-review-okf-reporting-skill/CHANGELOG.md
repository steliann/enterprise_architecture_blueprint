# Changelog

## 1.1.0 - 2026-09-07

- Made the coverage rubric externally configurable while preserving `config/defaults.yaml` as the immutable skill default.
- Added the portable `coverage-rubric.yaml` contract used by Architecture Blueprint Workbench v1.8.0.
- Added enabled/disabled coverage dimensions and relative-weight normalization.
- Added `coverage_dimensions`, `coverage_model_version`, and `coverage_model_hash` to coverage category templates for reproducible scoring.
- Added `review-model/coverage-rubric.yaml` to generated Review OKFs so each review carries the exact scoring model used.
- Added deterministic weight-only recalculation when raw category dimension scores are present.
- Added `validate_coverage_rubric.py`, `recalculate_coverage.py`, and rubric consistency checks in the Review OKF validator.
- Added an example coverage-rubric override.

## 1.0.0 - 2026-09-07

- Initial architecture-agnostic Architecture Blueprint Review skill.
- Supports Blueprint -> Review OKF, Review OKF -> Word report, Review OKF -> slides, and full end-to-end generation.
- Adds generic Review OKF templates for coverage, gaps, Validation Items, recommendations, registers, knowledge model and integrated review.
- Adds Qlik-style Word and PowerPoint design seeds derived from the supplied customer-facing examples without customer-specific architecture content.
- Adds deterministic validators for Blueprint OKF, Review OKF, Word report, slides, and cross-asset delivery gates.
- Adds reproducible coverage scoring guidance and explicit Unknown-is-not-a-gap promotion rules.
