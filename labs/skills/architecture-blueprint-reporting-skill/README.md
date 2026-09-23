# Architecture Blueprint Customer Reporting Skill

This package supports both customer-facing Architecture Blueprint baselines and
Architecture Assessment reporting.

## Supported output families

### Blueprint baseline

- Markdown baseline from Architecture Blueprint OKF;
- Word baseline from validated Markdown;
- PowerPoint workshop deck from validated Markdown;
- baseline structure validation.

### Architecture assessment

- Architecture Assessment / Review OKF from a sufficiently mature Blueprint;
- refresh of an existing Assessment / Review OKF from a newer Blueprint and new
  customer evidence;
- customer-facing Word assessment derived from the validated Assessment OKF;
- assessment structure/editorial validation.

The assessment workflow is deliberately **architecture-first**. Findings are
solution-independent. Recommendations state target direction, practical
implications and key considerations before mapping the direction to Qlik/Talend
or adjacent technologies.

## Package contents

- `SKILL.md` — main operating instructions and workflow router.
- `templates/architecture-blueprint-report-template.md` — baseline Markdown template.
- `templates/architecture-assessment-okf-template.md` — canonical assessment/review template for greenfield use.
- `guidance/markdown-report-guide.md` — baseline content/editorial guidance.
- `guidance/word-report-guide.md` — baseline Word guidance.
- `guidance/powerpoint-workshop-guide.md` — baseline workshop presentation guidance.
- `guidance/assessment-okf-guide.md` — assessment reasoning, record and refresh guidance.
- `guidance/assessment-word-report-guide.md` — customer-facing assessment Word guidance.
- `styles/style-tokens.yaml` — reusable visual design tokens.
- `styles/word-style.md` — Word layout and styling rules.
- `styles/powerpoint-style.md` — PowerPoint layout and styling rules.
- `schemas/report-structure.yaml` — baseline structure definition.
- `schemas/assessment-okf-structure.yaml` — canonical assessment structure definition.
- `scripts/validate_report.py` — baseline validator.
- `scripts/validate_assessment.py` — assessment validator for the canonical Markdown structure.
- `requirements.txt` — validator dependency.
- `manifest.txt` — package file list.

## Key assessment principles added in v2

- Unknown is not a gap.
- A product feature or licence opportunity is not a gap.
- The customer-facing report must not be organised around entitlement classes.
- Major recommendations explain what the adjustment means for the technical team
  without becoming an implementation runbook.
- Data placement/persistence is assessed independently from database-product
  selection when relevant.
- Static/reference data, historical snapshots and exchange/research datasets are
  treated as explicit architecture classes when material.
- Analytical-platform recommendations keep retention, migration and hybrid
  options open until workload fitness is demonstrated.
- Existing DQ, governance, lineage, business rules and orchestration are preserved
  when they remain fit.
- Qlik/Talend fit is explained after the architecture direction.
- Word is derived from the authoritative Assessment / Review OKF and cannot
  silently introduce new findings or recommendations.

The original example documents used to establish the visual design language are
not included. The reusable style system is represented by the style guides and
tokens in this package.
