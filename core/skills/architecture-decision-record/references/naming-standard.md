# ADR naming and identity standard

## Principles

1. **Stable identity.** Once assigned, an ID never changes.
2. **No reuse.** Never reuse an ID after an ADR is deprecated, superseded, deleted, or archived.
3. **Explicit scope.** The ID makes clear whether the decision is generic or belongs to a specific customer, program, platform, or workstream.
4. **One decision per record.** Never combine independent decisions under one ID.
5. **Append-only lifecycle.** Accepted ADRs aren't silently rewritten. Material change creates a successor.
6. **Traceability.** The YAML `id`, the Markdown H1, the filename, and every relationship field stay consistent.

## ID formats

**Generic, repository-level** — `ADR-NNN`

For repository-level, reference-architecture, enterprise-wide, and internal governance decisions that are intentionally not customer-scoped. Examples: `ADR-001`, `ADR-002`.

**Scoped** — `SCOPE-ADR-NNN`

For customer, program, architecture-initiative, product-platform, and internal-workstream decisions. Examples: `SPX-ADR-001`, `SJP-ADR-004`, `QTC-ADR-002`, `CSE-ADR-005`.

### Scope prefix

Pattern `[A-Z][A-Z0-9]{1,9}`. Uppercase letters and digits only. Keep it short.

The prefix must be stable, recognizable to the architecture team, and unique enough to avoid confusion. It must not derive from a temporary project phase, a person's name, a sprint, or a ticket number.

Observed prefixes: `ADR` (repository-level), `SPX`, `SJP`, `QTC`, `CSE`, `DQF`, `REPL`, `GOV`. Don't create a new prefix when an existing one already covers the scope.

### Sequence number

Three digits, starting at `001`, incrementing by one per new ADR **within each scope**.

- Don't reuse skipped numbers.
- Don't reuse numbers from deprecated or superseded records.
- Don't renumber existing ADRs to close gaps.
- Don't use dates or ticket numbers as sequence numbers.

If `SPX-ADR-002` is superseded, the next new record is `SPX-ADR-003`. `002` is retired.

## Filename

Stored in `decision-records/`, lowercase, hyphen-separated:

```
decision-records/<adr-id-lowercase>-<short-kebab-case-title>.md
```

```
decision-records/spx-adr-001-use-qlik-cloud-catalog-for-initial-profiling.md
decision-records/sjp-adr-004-use-talend-studio-for-advanced-duplicate-matching.md
decision-records/qtc-adr-002-use-dynamic-engine-for-containerized-execution.md
decision-records/adr-001-use-standard-adr-metadata-model.md
```

Rules: lowercase; hyphens not underscores; no spaces; full ADR ID at the start; title portion short but recognizable. **No status in the filename** — status changes would churn the file. **No date in the filename** unless the date is materially part of the decision context. Don't rename after publication except to correct a clear naming error, and then preserve links.

## The three-way alignment

| Location | Example |
|---|---|
| YAML `id` | `SPX-ADR-001` |
| Markdown H1 | `# SPX-ADR-001 — Use Qlik Cloud Catalog for Initial Profiling` |
| Filename | `spx-adr-001-use-qlik-cloud-catalog-for-initial-profiling.md` |

The validator checks all three.

## Titles

The title names the **decision**, not the topic. Preferred pattern:

```
Use [selected product / pattern / approach] for [architecture role / decision purpose]
```

Also valid: `Adopt [standard] for [scope]`, `Retain [existing approach] for [reason]`, `Replace [current] with [target]`, `Defer [decision] until [condition]`, `Standardize on [technology / operating model] for [scope]`.

Good:

```
Use Qlik Cloud Catalog for Initial Profiling and Trust Score Baseline
Use Snowflake as the Operational Data Quality Store
Use OIDC with Okta for Qlik Cloud SSO
Use Dynamic Engine for Containerized Talend Workload Execution
```

Weak — these name topics, not decisions:

```
Data Quality
Snowflake
SSO
Dynamic Engine
```

Avoid titles that are generic, phrased as questions, phrased as meeting notes, phrased as implementation tasks, too broad for one decision, or customer-specific when the decision is meant to be reusable.

## Relationship references

ADR-to-ADR — the ID exactly:

```yaml
related_adrs:
  - "SPX-ADR-001"
  - "SPX-ADR-003"
```

ADR-to-KU — ID, title, and relative path where available:

```yaml
related_patterns:
  - "QDQ-001 — Data Quality Profiling Baseline (../knowledge-units/qdq-001-data-quality-profiling-baseline.md)"
```

KU-to-ADR uses `originating_adrs` on the KU side, closing the loop. When an ADR draws materially on a KU, the KU's `originating_adrs` should eventually list it — flag that as a follow-up rather than editing someone else's KU.

**Never invent IDs.** Never reference a record that doesn't exist unless the relationship is explicitly marked as an open question.

## Supersession

Original:

```yaml
id: SPX-ADR-002
status: Superseded
superseded_by: "SPX-ADR-006"
```

Replacement:

```yaml
id: SPX-ADR-006
status: Accepted
supersedes: "SPX-ADR-002"
superseded_by: null
```

The replacement gets a new ID. The superseded record keeps its own. Links go both ways. No partial supersession — if only part of an ADR is being replaced, the original was too broad and should be split or superseded by several narrower records.

## Status and date live in YAML only

```yaml
status: Proposed
date: 2026-05-26
```

Never in the ID or filename. Wrong:

```
spx-adr-002-proposed-use-qlik-cloud-catalog.md
spx-adr-002-accepted-use-qlik-cloud-catalog.md
2026-05-26-spx-adr-002-use-qlik-cloud-catalog.md
```

## Scope prefix registry

Maintained at `decision-records/_registry.md`:

```markdown
# Decision Record Scope Registry

| Prefix | Scope | Owner | Description |
|---|---|---|---|
| ADR | Repository-level | Architecture Governance | Generic repository-level architecture decisions |
| SPX | Customer | [Owner] | SPX customer architecture decisions |
| QTC | Program | [Owner] | Qlik Talend Cloud architecture decisions |
| CSE | Program | [Owner] | Customer Success Engineering architecture decisions |
```

Before creating a scoped ADR: check whether the prefix exists, find the highest used sequence number for it, take the next one, and add the record to the registry if the repository tracks individual records. Optional per-ADR registry rows:

```markdown
| ADR ID | Title | Status | Owner | File |
|---|---|---|---|---|
```

## Pre-commit checklist

- File is under `decision-records/`.
- ID matches `ADR-NNN` or `SCOPE-ADR-NNN`, three-digit sequence.
- The ID has never been used before.
- YAML `id`, Markdown H1, and filename all agree.
- Filename is lowercase kebab-case, starting with the ID.
- Title names a decision, not a topic.
- No status or date encoded in the filename.
- `supersedes` and `superseded_by` reference real ADRs.
- Related KUs and ADRs use real IDs, with relative links where appropriate.
