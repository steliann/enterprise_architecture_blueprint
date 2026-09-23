# Architecture Blueprint OKF Skill

A reusable skill and deterministic toolset for converting architecture-review evidence into a maintained Architecture Blueprint OKF.

## What is included

- `SKILL.md` — agent operating instructions.
- `templates/` — editable Markdown/Jinja templates and a versioned registry.
- `schemas/` — JSON Schemas for YAML front matter.
- `src/architecture_blueprint_okf/` — validation, initialization, evidence indexing, migration, and packaging utilities.
- `prompts/` — focused reasoning checklists used by the skill.
- `references/` — modelling, refresh, evidence, and template-maintenance guidance.
- `examples/` — synthetic evidence and a complete example OKF.
- `tests/` — validator and template tests.

## Install

```bash
./scripts/setup.sh
```

The setup script creates a local virtual environment that reuses installed Python packages, so it also works in restricted or offline environments. Optional package installation remains available through `pyproject.toml`.

## Commands

```bash
blueprint-okf validate-templates
blueprint-okf init --customer "Example Organisation" --solution "Funding Data Service" --output ./architecture-blueprint
blueprint-okf new-record ./architecture-blueprint --type business-use-case --title "Funding Portfolio Insight"
blueprint-okf index-evidence ./evidence --blueprint ./architecture-blueprint
blueprint-okf refresh-indexes ./architecture-blueprint
blueprint-okf validate ./architecture-blueprint --strict
blueprint-okf migrate ./architecture-blueprint --dry-run
blueprint-okf package ./architecture-blueprint --output ./architecture-blueprint.zip
```

The Python tools enforce the package contract. Interpretation and semantic authoring remain the responsibility of the model following `SKILL.md`.
