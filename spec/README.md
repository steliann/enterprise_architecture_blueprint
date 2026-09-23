# Architecture AI Skill Specification

Each installable skill is one folder containing a `SKILL.md`. Supporting material belongs beneath that folder.

## Required frontmatter

```yaml
---
name: lowercase-hyphenated-name
description: >-
  Clear activation description including when the agent should use the skill.
license: Proprietary
metadata:
  author: Architecture AI
  version: 0.1.0
  tags:
    - architecture
allowed-tools: read
---
```

Required fields: `name`, `description`, `license`, `metadata.author`, `metadata.version`. Folder name and `name` must match. `metadata.version` must be semantic version `x.y.z`.

## Recommended sections

1. Purpose
2. When to use
3. Inputs
4. Outputs
5. Workflow
6. Human-in-the-loop gates
7. Validation rules
8. Failure / incomplete-information behavior
9. References and templates

## Skill package structure

```text
skill-name/
├── SKILL.md
├── references/
├── assets/
├── scripts/
└── tests/
    ├── activation-cases.yaml
    └── validation-cases.yaml
```

Only `SKILL.md` is mandatory; the remaining folders are used when the capability needs them.
