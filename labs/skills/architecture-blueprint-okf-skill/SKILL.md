---
name: architecture-blueprint-okf
description: Generate, refresh, validate, migrate, and package a maintainable Architecture Blueprint OKF from interview transcripts, notes, diagrams, and shared customer documents.
version: 1.0.0
---

# Architecture Blueprint OKF Skill

## Purpose

Use this skill when an EA or CSE needs to turn unstructured customer evidence into a maintained Architecture Blueprint Open Knowledge Format (OKF) package.

The skill supports two operating modes:

1. **Create** — establish a new blueprint from transcripts, notes, diagrams, spreadsheets, presentations, and other shared material.
2. **Refresh** — merge new evidence into an existing blueprint without losing stable identifiers, validated content, explicit uncertainty, or record history.

The skill also validates the package against independently maintained templates and schemas. Template changes are versioned and can be applied without rewriting the core skill instructions.

## Required output

Produce the complete blueprint package, not isolated documents:

```text
architecture-blueprint/
├── index.md
├── high-level-architecture.md
├── knowledge-model.md
├── consumers.md
├── sources.md
├── technologies.md
├── business-use-cases/
│   ├── index.md
│   └── UC-NNN-<slug>.md
├── required-capabilities/
│   ├── index.md
│   └── RC-NNN-<slug>.md
├── data-products/
│   ├── index.md
│   └── DP-NNN-<slug>.md
├── data-flows/
│   ├── index.md
│   └── DF-NNN-<slug>.md
├── quality-controls/
│   ├── index.md
│   └── QC-NNN-<slug>.md
├── operational-capabilities/
│   ├── index.md
│   └── OC-NNN-<slug>.md
├── architecture-decision-records/
│   ├── index.md
│   └── ADR-NNN-<slug>.md
├── reports/
│   ├── change-summary.md
│   ├── open-questions.md
│   └── validation-report.md
└── .okf/
    ├── manifest.yaml
    ├── template-lock.yaml
    ├── id-registry.yaml
    ├── evidence-ledger.jsonl
    ├── claim-map.yaml
    └── validation-report.json
```

Do not copy raw customer evidence into the package unless explicitly requested. Store evidence provenance, hashes, locations, timestamps, pages, slides, or sections in `.okf/evidence-ledger.jsonl` and map claims to records in `.okf/claim-map.yaml`.

## Core modelling chain

```text
Consumer
    participates in Business Use Case
    consumes Data Product

Business Use Case
    requires Required Capability

Source
    feeds Data Flow

Data Flow
    produces or updates Data Product

Quality Control
    assures Data Flow or Data Product

Operational Capability
    operates or supports Data Flow or Data Product

Technology
    realizes or constrains implementation

Architecture Decision Record
    shapes Data Product, Data Flow, Quality Control,
    Operational Capability, Source boundary, or Technology choice
```

## Mandatory operating principles

### Evidence before architecture

Read all available material before finalizing the model. Build an evidence inventory first. Distinguish:

- direct customer statements;
- descriptions of current implementation;
- stated future direction;
- interviewer hypotheses or questions;
- model inference;
- external research.

Never convert an interviewer suggestion into a confirmed customer fact.

### No invented certainty

Do not invent owners, service levels, thresholds, RTO/RPO, retention, volumes, approvals, authoritative-source status, decision rationale, or target dates. Record unresolved points as open questions.

### Business outcomes before implementation

Identify Business Use Cases from consumer outcomes, decisions, accountabilities, or obligations. A system, feed, report, database, data-quality process, or technical activity is not automatically a use case.

Data quality belongs in Quality Controls. Operational support belongs in Operational Capabilities. A temporary operational workaround may be a candidate or transitional use case only when it directly supports a real business action.

### Stable identity

Identifiers are permanent. Titles and filenames may change, but IDs do not. Never reuse retired IDs. During refresh:

- update the existing record when the concept is the same;
- split a record only when evidence proves separate outcomes or architectural boundaries;
- merge records only with an explicit redirect or supersession entry;
- deprecate rather than silently delete;
- keep the ID registry current.

### Bidirectional traceability

Maintain relationships in both directions where the templates define an inverse relationship. Update all affected files when a relationship changes.

### Separate current, transitional, and target state

Do not collapse coexistence or migration into one state. Mark records and statements as current, transitional, target, candidate, deprecated, or superseded as applicable.

### Retrospective ADR discipline

When documenting an existing decision after implementation:

- record the implemented choice as confirmed;
- distinguish observed benefits from original rationale;
- state when original alternatives, approver, or date are unknown;
- do not retrofit a persuasive rationale;
- record negative consequences and review questions.

## Workflow

### Phase 1 — Discover inputs

Identify:

- the existing blueprint, if any;
- all new evidence files;
- customer and solution names;
- evidence dates or session sequence;
- the selected template set and version;
- whether the task is create, refresh, validate, migrate, or a combination.

Use the latest complete blueprint as the refresh baseline. Do not merge unrelated historical packages simply because their filenames are newer.

### Phase 2 — Index evidence

Create or refresh `.okf/evidence-ledger.jsonl`.

Each evidence entry should include:

```yaml
id: EVD-NNNN
source_file: <path or source name>
source_type: transcript | note | document | slide | spreadsheet | diagram | external-research
session_or_date: <value when known>
location: <timestamp, page, slide, sheet/cell, section, or paragraph>
content_hash: <sha256>
summary: <short evidence description>
```

For long transcripts, use timestamp-bounded evidence units. For documents, use page or section references. Keep excerpts short and only when needed to disambiguate the claim.

### Phase 3 — Extract atomic claims

Build `.okf/claim-map.yaml` before drafting records. Each claim should identify:

- claim ID;
- subject or candidate concept;
- claim text;
- state: current, transitional, target, historical, or unknown;
- support: confirmed, inferred, disputed, or superseded;
- confidence: High, Medium, or Low;
- evidence IDs;
- affected record IDs when resolved.

Resolve contradictions explicitly. Prefer the most direct and most recent evidence only when it describes the same time horizon. Preserve valid historical facts.

### Phase 4 — Resolve entities and boundaries

Normalize aliases, acronyms, renamed systems, and overlapping personas. Apply these boundaries:

- **Consumer** — a person, team, organisation, public audience, or system that uses information or participates in the outcome.
- **Source** — a real system or provider outside the principal solution boundary that originates or externally curates data.
- **Technology** — a named product, service, engine, platform, or material technical pattern selected to realize or constrain the solution.
- **Data Product** — a managed information offering for defined consumers and purposes; not merely a table or database.
- **Data Flow** — a logical end-to-end movement and transformation path; not every job or stage.
- **Quality Control** — a preventive, detective, or corrective trust mechanism.
- **Operational Capability** — a repeatable ability to run, observe, recover, secure, scale, deploy, or retire the solution.
- **ADR** — a material architecture choice with consequences and alternatives.

Exclude transit buckets, staging schemas, temporary files, queues, and intermediate tables from the Source inventory. They may appear in Data Flows or Technologies.

### Phase 5 — Model in dependency order

Create or refresh records in this order:

1. Consumers
2. Business Use Cases
3. Required Capabilities
4. Sources
5. Data Products
6. Data Flows
7. Quality Controls
8. Operational Capabilities
9. Technologies
10. Architecture Decision Records
11. High-Level Architecture
12. Knowledge Model
13. Collection indexes and root index

This order prevents technology-led modelling and makes relationship validation easier.

### Phase 6 — Author from templates

Load `templates/template-registry.yaml`. Use the registered Jinja templates and JSON schemas. Do not reproduce section structures from memory.

Template rules:

- keep YAML front matter parseable;
- include both `type` and `artifact_type`;
- use `okf_version: "0.2"` at package level;
- use stable IDs and lowercase hyphenated filenames;
- use unnumbered headings;
- do not add standalone evidence sections to public blueprint documents;
- place provenance in `.okf/`;
- retain open questions in each relevant record;
- use relative Markdown links;
- keep the High-Level Architecture concise and narrative; the Solution Summary must not exceed three paragraphs.

### Phase 7 — Refresh safely

When new evidence arrives:

1. Copy the existing blueprint to a working output location.
2. Index only the new or changed evidence, preserving existing evidence IDs.
3. Extract new claims and compare them with existing claims and records.
4. Classify each proposed change as:
   - confirm;
   - enrich;
   - correct;
   - supersede;
   - split;
   - merge;
   - deprecate;
   - add;
   - unresolved conflict.
5. Apply changes to records and inverse links.
6. Update dates only on materially changed files.
7. Update indexes, counts, the High-Level Architecture, and the Knowledge Model only where affected.
8. Write `reports/change-summary.md` with before/after rationale and evidence IDs.
9. Keep unresolved contradictions in `reports/open-questions.md`.
10. Validate before packaging.

Preserve manually curated content unless new evidence clearly supersedes it. Do not replace precise text with generic summaries during refresh.

### Phase 8 — Validate

Run deterministic validation:

```bash
python -m architecture_blueprint_okf.cli validate <blueprint-path> --strict
```

The package must pass:

- required file and folder checks;
- YAML syntax and schema checks;
- template heading presence and order;
- stable ID and filename checks;
- duplicate ID detection;
- internal Markdown link validation;
- referenced-ID existence checks;
- inverse-relationship checks;
- inventory record-ID checks for `CON`, `SRC`, and `TECH`;
- collection index coverage;
- template-lock compatibility;
- placeholder detection;
- ZIP integrity after packaging.

Semantic checks should additionally confirm:

- every use case states a clear purpose and primary business question;
- use cases are distinct by outcome, consumer, decision, or obligation;
- every required capability is implementation-independent;
- every Data Product has consumers and a managed purpose;
- Data Flows have real source and target boundaries;
- Quality Controls state failure actions;
- Operational Capabilities describe repeatable operating behaviour;
- ADRs contain consequences and do not invent rationale;
- sources are outside the main solution boundary;
- technologies are named implementation choices, not generic terms;
- unknowns remain explicit.

### Phase 9 — Package

Generate both the folder and a ZIP archive:

```bash
python -m architecture_blueprint_okf.cli package <blueprint-path> --output <archive.zip>
```

Always provide:

- the complete ZIP;
- the root `index.md`;
- the validation report;
- the change summary for refresh operations.

## Template maintenance

Templates are maintained independently under `templates/`, with metadata in `templates/template-registry.yaml` and field constraints in `schemas/`.

When understanding of the blueprint changes:

1. edit the relevant template;
2. edit the corresponding JSON schema;
3. update required headings or relationship rules in the registry;
4. increment that document's `schema_version`;
5. increment `template_set_version` when the package contract changes;
6. add a migration note under `templates/migrations/`;
7. run the test suite;
8. run `template-lock` on newly generated packages.

Do not change templates without changing the registry and tests. Do not make the validator depend on hard-coded headings when the registry can define them.

For an existing blueprint using an older template set:

```bash
python -m architecture_blueprint_okf.cli migrate <blueprint-path> --dry-run
python -m architecture_blueprint_okf.cli migrate <blueprint-path> --apply
```

Automatic migration is conservative: it adds missing required sections and metadata but does not delete or reinterpret customer content. Semantic migration remains an LLM task and must be summarized in the change report.

## Quality gate

A blueprint is ready for delivery only when:

- all requested core documents exist;
- every record validates structurally;
- all internal links resolve;
- all referenced IDs exist;
- inverse relationships are consistent or explicitly waived;
- no raw template placeholders remain;
- record counts match indexes;
- the template lock matches the selected template set;
- the package archive passes integrity validation;
- the open-question report contains every material unknown or conflict;
- the change summary accurately describes refresh changes.

If the package cannot pass, deliver the partial package only with a clear validation report identifying each failure. Never claim successful validation without running it.
