# Decision Record Naming Standards

This document defines the naming and identification standards for Architecture Decision Records stored in the `decision-records/` folder.

Architecture Decision Records, also called ADRs or decision records, capture specific architecture decisions. They are different from Knowledge Units. A Knowledge Unit captures reusable guidance. A Decision Record captures a decision made for a specific customer, program, product platform, enterprise scope, or reference architecture context.

---

## Core principles

Decision Record names and IDs must follow these principles:

1. **Stable identity.** Once assigned, a Decision Record ID must not change.
2. **No reuse.** Never reuse an ID after a Decision Record is deprecated, superseded, deleted from the active set, or moved to an archive.
3. **Explicit decision scope.** The ID should make it clear whether the decision is generic or belongs to a specific customer, program, product platform, or architecture workstream.
4. **Readable file names.** File names should include both the ID and a short decision title.
5. **One decision per record.** Do not combine multiple independent decisions under one ID.
6. **Append-only lifecycle.** Accepted Decision Records should not be silently rewritten. Material changes should create a new Decision Record that supersedes the previous one.
7. **Repository traceability.** The ID in the YAML front matter, Markdown title, file name, and relationship fields must remain consistent.

---

## Standard ID formats

Use one of these two ID formats.

### Generic repository-level Decision Records

Use this format when the decision is not tied to a specific customer, program, or workstream.

```text
ADR-NNN
```

Examples:

```text
ADR-001
ADR-002
ADR-003
```

Use this format for:

* repository-level architecture decisions;
* reference architecture decisions;
* enterprise-wide decisions;
* internal architecture governance decisions;
* decisions that are intentionally not customer-scoped.

### Scoped Decision Records

Use this format when the decision belongs to a specific customer, program, product platform, architecture initiative, or workstream.

```text
SCOPE-ADR-NNN
```

Examples:

```text
SPX-ADR-001
SJP-ADR-004
QTC-ADR-002
CSE-ADR-005
```

Use this format for:

* customer-specific decisions;
* program-specific decisions;
* architecture initiative decisions;
* product-platform decisions;
* internal workstream decisions;
* decisions that need to be grouped by context.

---

## Scope prefix rules

The `SCOPE` prefix identifies the decision context.

Use **uppercase letters and digits only. No underscores, no lowercase letters, no other punctuation.** This is a hard rule, not a preference — the validation tooling enforces exactly this character set and will reject anything else. Prefer short prefixes.

Required pattern:

```text
[A-Z][A-Z0-9]{1,9}
```

Examples:

```text
SPX
SJP
QTC
CSE
DQF
REPL
GOV
```

The prefix should be:

* stable;
* short;
* recognizable to the architecture team;
* unique enough to avoid confusion;
* not dependent on a temporary project phase;
* not based on a person's name;
* not based on an implementation sprint or ticket number.

> **Revision note.** An earlier version of this rule said uppercase letters and numbers "unless a repository-specific convention already allows underscores." Drop that exception. The ADR schema and validation script both match IDs against `[A-Z][A-Z0-9]{1,9}` with no underscore variant, so an underscore-containing prefix is not actually usable regardless of local convention — it fails validation every time. If a prefix has already shipped with an underscore, treat it as a naming defect to correct at the next opportunity, not a supported pattern.

---

## Sequence number rules

Use a three-digit sequence number.

```text
001
002
003
```

Rules:

* Start at `001` for each scope.
* Increment by one for each new Decision Record in that scope.
* Do not reuse skipped numbers.
* Do not reuse numbers from deprecated or superseded records.
* Do not renumber existing Decision Records to close gaps.
* Do not use dates as sequence numbers.
* Do not use Jira ticket numbers as sequence numbers.

Examples:

```text
SPX-ADR-001
SPX-ADR-002
SPX-ADR-003
```

If `SPX-ADR-002` is superseded, the next Decision Record is still `SPX-ADR-003`, not a reuse of `SPX-ADR-002`.

**When the corpus can't be checked** (offline, no repository access, tooling unavailable), write the sequence portion as `XXX` — e.g. `SPX-ADR-XXX` — rather than guessing a number. A guessed number that collides with a real one is a worse failure than a visible placeholder. Flag the placeholder wherever the record is reviewed, and allocate the real number before the record is committed or accepted.

---

## File naming convention

Decision Record files must be stored in:

```text
decision-records/
```

Use lowercase file names.

Recommended file name format:

```text
<adr-id-lowercase>-<short-kebab-case-title>.md
```

Examples:

```text
decision-records/spx-adr-001-use-qlik-cloud-catalog-for-initial-profiling.md
decision-records/sjp-adr-004-use-talend-studio-for-advanced-duplicate-matching.md
decision-records/qtc-adr-002-use-dynamic-engine-for-containerized-execution.md
decision-records/adr-001-use-standard-adr-metadata-model.md
```

File name rules:

* Use lowercase.
* Use hyphens between words.
* Include the full ADR ID at the start of the file name.
* Keep the title portion short but recognizable.
* Do not use spaces.
* Do not use underscores.
* Do not include status in the file name.
* Do not include dates in the file name unless the date is part of the decision context.
* Do not rename files after publication unless correcting a clear naming error and preserving links.

---

## YAML ID convention

The YAML `id` field must match the Decision Record ID exactly.

Example:

```yaml
id: SPX-ADR-001
```

The Markdown H1 must also include the same ID.

Example:

```markdown
# SPX-ADR-001 — Use Qlik Cloud Catalog for Initial Profiling
```

The file name should use the lowercase version of the same ID.

Example:

```text
spx-adr-001-use-qlik-cloud-catalog-for-initial-profiling.md
```

These three values must stay aligned:

| Location    | Example                                                        |
| ----------- | --------------------------------------------------------------- |
| YAML `id`   | `SPX-ADR-001`                                                  |
| Markdown H1 | `# SPX-ADR-001 — Use Qlik Cloud Catalog for Initial Profiling` |
| File name   | `spx-adr-001-use-qlik-cloud-catalog-for-initial-profiling.md`  |

---

## Title naming rules

The ADR title must name the decision, not just the topic.

Use action-oriented titles.

Good examples:

```text
Use Qlik Cloud Catalog for Initial Profiling and Trust Score Baseline
Use Snowflake as the Operational Data Quality Store
Use Talend Studio for Advanced Duplicate Matching and Survivorship
Use OIDC with Okta for Qlik Cloud SSO
Use Dynamic Engine for Containerized Talend Workload Execution
```

Weak examples:

```text
Data Quality
Snowflake
Duplicate Matching
SSO
Dynamic Engine
```

Avoid titles that are:

* generic;
* phrased as questions;
* phrased as meeting notes;
* phrased as implementation tasks;
* too broad for one decision;
* customer-specific when the decision is intended to be reusable.

Preferred title pattern:

```text
Use [selected product / pattern / approach] for [architecture role / decision purpose]
```

Alternative valid patterns:

```text
Adopt [standard / pattern] for [scope]
Retain [existing approach] for [reason]
Replace [current approach] with [target approach]
Defer [decision] until [condition]
Standardize on [technology / operating model] for [scope]
```

---

## ID and title examples

### Customer-scoped ADR

```yaml
id: SPX-ADR-002
title: Use Qlik Cloud Catalog and Data Quality for Initial Profiling and Trust Score Baseline
```

File name:

```text
decision-records/spx-adr-002-use-qlik-cloud-catalog-and-data-quality-for-initial-profiling.md
```

### Program-scoped ADR

```yaml
id: QTC-ADR-001
title: Use Data Movement Gateway for Qlik Cloud Data Integration Runtime Connectivity
```

File name:

```text
decision-records/qtc-adr-001-use-data-movement-gateway-for-runtime-connectivity.md
```

### Generic repository-level ADR

```yaml
id: ADR-001
title: Use Canonical Metadata and Markdown Structure for Architecture Decision Records
```

File name:

```text
decision-records/adr-001-use-canonical-metadata-and-markdown-structure.md
```

---

## Relationship naming rules

When referencing Decision Records from other Decision Records, use the ADR ID exactly.

Example:

```yaml
related_adrs:
  - SPX-ADR-001
  - SPX-ADR-003
```

When referencing Decision Records from Knowledge Units, use the same ID exactly.

Example:

```yaml
originating_adrs:
  - SPX-ADR-002
```

When referencing KUs from Decision Records, include the KU ID, title, and relative path when possible.

Example:

```yaml
related_patterns:
  - "QDQ-001 — Data Quality Profiling Baseline (../knowledge-units/qdq-001-data-quality-profiling-baseline.md)"
```

Do not invent IDs. Do not reference records that do not exist unless the relationship is explicitly marked as an open question.

---

## Supersession naming rules

When a Decision Record is replaced, do not edit the original decision in place if it has already been accepted.

Create a new Decision Record with a new ID.

Example:

Original ADR:

```yaml
id: SPX-ADR-002
status: Superseded
superseded_by: SPX-ADR-006
```

Replacement ADR:

```yaml
id: SPX-ADR-006
status: Accepted
supersedes: SPX-ADR-002
superseded_by: null
```

Rules:

* The replacement ADR gets a new ID.
* The superseded ADR keeps its original ID.
* The superseded ADR status changes to `Superseded`.
* The superseded ADR points to the replacement using `superseded_by`.
* The replacement ADR points back using `supersedes`.
* Do not reuse the old ID.
* Do not create partial supersession such as "replaces section 3 only." If only part of an ADR is replaced, the original ADR was probably too broad and should be split or superseded by multiple narrower ADRs.

---

## Status and naming interaction

Do not encode status in the ID or file name.

Correct:

```text
spx-adr-002-use-qlik-cloud-catalog-for-initial-profiling.md
```

Incorrect:

```text
spx-adr-002-proposed-use-qlik-cloud-catalog.md
spx-adr-002-accepted-use-qlik-cloud-catalog.md
spx-adr-002-final-use-qlik-cloud-catalog.md
```

Status belongs only in YAML:

```yaml
status: Proposed
```

This prevents file churn when the status changes.

---

## Date and naming interaction

Do not encode dates in the ID or file name unless the date is materially part of the decision context.

Correct:

```text
spx-adr-002-use-qlik-cloud-catalog-for-initial-profiling.md
```

Usually incorrect:

```text
2026-05-26-spx-adr-002-use-qlik-cloud-catalog.md
spx-adr-002-2026-05-26-use-qlik-cloud-catalog.md
```

The decision date belongs in YAML:

```yaml
date: 2026-05-26
```

Use dates in file names only when the repository intentionally organizes records chronologically. If chronological sorting is needed, rely on metadata or repository views rather than file name dates.

---

## Scope prefix registry

Maintain a small prefix registry to avoid collisions.

Suggested location:

```text
decision-records/_registry.md
```

Recommended registry format:

```markdown
# Decision Record Scope Registry

| Prefix | Scope | Owner | Description |
|---|---|---|---|
| ADR | Repository-level | Architecture Governance | Generic repository-level architecture decisions |
| SPX | Customer | [Owner] | SPX customer architecture decisions |
| SJP | Customer | [Owner] | SJP customer architecture decisions |
| QTC | Program | [Owner] | Qlik Talend Cloud architecture decisions |
| CSE | Program | [Owner] | Customer Success Engineering architecture decisions |
```

Before creating a new scoped ADR:

1. Check whether the prefix already exists.
2. Check the highest used sequence number for that prefix.
3. Allocate the next number — or use the `XXX` placeholder above if the registry can't be reached right now.
4. Add the new ADR to the registry if the repository tracks individual records there.
5. Do not create a new prefix when an existing prefix already covers the scope.

---

## Recommended registry entry for each ADR

A registry may also track individual ADRs.

Suggested format:

```markdown
| ADR ID | Title | Status | Owner | File |
|---|---|---|---|---|
| SPX-ADR-002 | Use Qlik Cloud Catalog and Data Quality for Initial Profiling and Trust Score Baseline | Proposed | Andrew Younge | [link](spx-adr-002-use-qlik-cloud-catalog-and-data-quality-for-initial-profiling.md) |
```

This is optional, but useful when the number of ADRs grows.

---

## Naming validation checklist

Before committing a new Decision Record, verify:

* The file is stored under `decision-records/`.
* The ID follows `ADR-NNN` or `SCOPE-ADR-NNN`, using letters and digits only — no underscores.
* The sequence number has three digits, or is the `XXX` placeholder pending allocation.
* The ID has not been used before.
* The YAML `id` matches the Markdown H1.
* The file name starts with the lowercase ADR ID.
* The file name uses kebab case.
* The title names a decision, not a topic.
* The status is not encoded in the file name.
* The date is not encoded in the file name unless intentionally required.
* The `supersedes` and `superseded_by` fields reference real ADR IDs.
* Related KUs and ADRs use real IDs and relative links where appropriate.

---

## Quick examples

Good:

```text
decision-records/spx-adr-002-use-qlik-cloud-catalog-for-initial-profiling.md
```

Good:

```text
decision-records/sjp-adr-004-use-talend-studio-for-advanced-duplicate-matching.md
```

Good:

```text
decision-records/adr-001-use-canonical-adr-structure.md
```

Avoid:

```text
decision-records/data-quality.md
```

Avoid:

```text
decision-records/final-adr.md
```

Avoid:

```text
decision-records/spx-decision-new.md
```

Avoid:

```text
decision-records/2026-05-26-use-catalog.md
```

Avoid:

```text
decision-records/spx-adr-2-catalog.md
```

The last example is invalid because the sequence number must use three digits: `SPX-ADR-002`.

---

## Changelog

**Revision 2**

* Removed the clause permitting underscores in scope prefixes "when a repository-specific convention allows it." The ID regex enforced by the schema and validation script never accepts underscores, so the exception described a case that tooling would always reject. The rule is now unconditional: letters and digits only.
* Added explicit guidance on the `XXX` sequence placeholder for use when the registry can't be checked, matching the behavior the validation script already accepts (with a warning) so authors have one documented, tooling-compatible way to defer ID allocation instead of guessing a number.
* Updated the naming validation checklist to mention the `XXX` placeholder path.
