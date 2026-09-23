# Contributing

1. Create or change skills under `labs/skills/` first.
2. Keep the skill folder name identical to `name` in `SKILL.md`.
3. Add activation and validation cases under `tests/`.
4. Run `npm run validate` locally.
5. Open a pull request and obtain architecture-practice review.
6. Promote a skill to `core/skills/` only when its contract, outputs and tests are stable.

## Versioning

Use semantic versioning in `metadata.version`. Increment the skill version whenever behavior, inputs, outputs, or required tooling changes.
