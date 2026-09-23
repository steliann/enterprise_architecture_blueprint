# Architecture Blueprint Review Skill v1.1.0

Architecture-agnostic skill for generating and validating:

1. Architecture Blueprint Review OKF from an Architecture Blueprint OKF.
2. Customer-facing Word architecture assessment from the Review OKF.
3. Architecture review slides from the Review OKF.
4. All three outputs end-to-end from a Blueprint OKF.

## Coverage rubric

The skill keeps its immutable default scoring model in `config/defaults.yaml` under `coverage_rubric`.

A user may supply a portable `coverage-rubric.yaml`, including one exported by Architecture Blueprint Workbench v1.8.0. The skill merges only known dimension enabled flags and weights over its defaults. It never edits `config/defaults.yaml`.

Generated category reports preserve raw dimension scores in `coverage_dimensions`, and the Review OKF stores the resolved rubric in `review-model/coverage-rubric.yaml`. This supports deterministic weight-only recalculation.

Useful commands:

```bash
python scripts/validate_coverage_rubric.py /path/to/coverage-rubric.yaml
python scripts/recalculate_coverage.py /path/to/architecture-blueprint-review --coverage-config /path/to/coverage-rubric.yaml --write
```

A legacy Review OKF without `coverage_dimensions` cannot be safely reweighted; perform a full coverage rescore from the Blueprint.

See `SKILL.md` and `guides/` for the complete operating model.
