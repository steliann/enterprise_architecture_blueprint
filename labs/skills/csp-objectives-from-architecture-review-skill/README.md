# CSP Objectives from Architecture Review Skill

This package is a reusable ChatGPT/OpenAI-style skill for generating and validating Customer Success Plan Objectives OKF from Architecture Blueprint Review OKF.

Start with `SKILL.md`.

Useful commands:

```bash
python scripts/inspect_review.py review.zip --markdown review-inventory.md --json review-inventory.json
python scripts/validate_csp.py csp.zip --review review.zip --report validation-report.md
python scripts/package_csp.py customer-success-plan-objectives --review review.zip --out csp-objectives-okf.zip
```
