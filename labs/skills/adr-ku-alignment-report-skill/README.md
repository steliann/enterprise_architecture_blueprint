# ADR–KU Alignment Report Skill v1.1.0

This package operationalizes the ADR–KU Alignment Report initiative.

## Canonical artifact

`adr-ku-alignment-report.md`

The canonical report is internal and is the source for downstream customer-facing and CSE/EA artifacts.

## Authority model

- `references/purpose-and-operating-model.md` is authoritative for **methodology and analysis semantics**.
- ACME and Northstar `adr-ku-alignment-report.md` examples are authoritative for the **canonical presentation pattern**.
- `templates/adr-ku-alignment-report.md` generalizes that pattern.

This distinction intentionally keeps analysis rigor (including Direct / Adjacent / Contextual classification) without forcing internal mechanics into the visible report.

## Package contents

- `SKILL.md` — skill instructions and execution workflow.
- `templates/adr-ku-alignment-report.md` — canonical report template.
- `references/concept-overview.md` — initiative framing and value proposition.
- `references/purpose-and-operating-model.md` — authoritative methodology.
- `references/report-generation-guidelines.md` — authoring and presentation rules.
- `examples/acme/*` and `examples/northstar/*` — canonical presentation exemplars and derivatives.
- `scripts/new_report.py` — create a report skeleton from the template.
- `scripts/validate_report.py` — validate front matter and canonical report structure.

## Typical usage

```bash
python scripts/new_report.py \
  --account "Customer Name" \
  --owner "CSE / EA Name" \
  --program "Program / domain scope" \
  --output ./adr-ku-alignment-report.md
```

Validate:

```bash
python scripts/validate_report.py ./adr-ku-alignment-report.md
```

The scripts require Python 3.10+ and PyYAML.
