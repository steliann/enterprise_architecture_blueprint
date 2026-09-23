---
name: knowledge-unit-architect
description: Build, draft, carve, or quality-review Qlik CSE/EA Knowledge Units (KUs) for the Enterprise Customer Success field-pattern library. Use this skill whenever the user mentions knowledge units, KUs, the field-pattern library, capturing a field pattern, turning a document/wiki page/transcript/reference architecture into reusable architectural guidance, checking a draft pattern against the Knowledge Fabric, reviewing/validating/scoring a KU against best practices, or refreshing/normalizing an existing KU into the canonical structure. Trigger even if the user just says "write this up as a KU", "is this KU any good?", or "help me capture this pattern" — do not wait for the exact phrase "knowledge unit". Do NOT use this skill for authoring customer-specific ADRs or other customer deliverables (an ADR cites KUs but is not one), for plain Knowledge Fabric searches, or for general documentation that is not a KU.
---

# Knowledge Unit Architect

Produce high-quality Knowledge Units (KUs) — ADR-style records of reusable Qlik field
architectural guidance — and review existing ones. A KU is *guidance for a recurring
decision*: opinionated, field-proven, append-only, status-tracked. It is not product
documentation and not a customer deliverable.

This skill uses progressive disclosure. Read ONLY the reference file for the active mode,
plus the shared files listed under each mode. Do not read everything up front.

## Step 1 — Pick the mode

| User intent | Mode | Read |
|---|---|---|
| Has an existing document (wiki page, reference architecture, customer doc, transcript) to convert | **Build from document** | `references/build-from-document.md` |
| Wants to capture a pattern from their head; no source document | **Build from scratch** | `references/build-from-scratch.md` |
| Has one or more existing KUs to assess for quality, consistency, validity | **Review** | `references/review.md` |
| Has an existing KU to rewrite/normalize into the canonical structure, preserving its intent | **Refresh** | `references/refresh.md` |

If the intent is ambiguous, ask one question to settle it before reading anything.

Every mode also uses, at the stage where its reference file says so:

- `references/quality-rubric.md` — the scored rubric and the delivery gate
- `references/knowledge-fabric.md` — how to discover and use the Knowledge Fabric MCP connector
- `references/naming-standard.md` — the KU identifier scheme (area+deployment+layer) and the fixed bundle-path convention; read this whenever you allocate a new ID or deliver a file, in every mode
- `assets/ku_template.md` — the v4 KU template: schema-conformant frontmatter + the canonical eleven-section body, six required and five optional (copy it; never invent frontmatter fields or extra H2 sections)
- `scripts/validate_ku.py` — deterministic schema/structure validation, including canonical section order, subsection formats, and bundle-path conformance (run it; don't eyeball). Pass multiple files or `--corpus <dir>` to also get library-level checks: duplicate IDs, bundle-path↔id match, dangling relationships, supersession reciprocity. When the user's KU library folder is reachable, always run the corpus check, not just the single file.

## Step 2 — Run the five-stage pipeline

All three modes follow the same pipeline. The mode reference file defines what each stage
means for that mode.

1. **Interrogate** — gather what the KU needs from the source (document, author's head, or
   the KU under review). Ask in batches, not one long interview. Use the AskUserQuestion
   tool where available.
2. **Cross-check the Knowledge Fabric** — search for duplicates, overlaps, alternatives,
   and contradictions before drafting (see `references/knowledge-fabric.md`). Never skip
   silently: if the connector is unavailable, record that in the quality report.
3. **Draft** — produce the KU(s) on the v4 template. One decision per KU.
4. **Assess** — run `scripts/validate_ku.py` on each draft, then score it against
   `references/quality-rubric.md`.
5. **Gate and deliver** — the rubric defines a hard gate. If a KU fails, return to stage 1
   with *targeted* follow-up questions (only the failing criteria), revise, re-assess.
   After two failed rounds, stop iterating: deliver the KU with `status: Draft`, the honest
   `confidence` value, and an explicit gap list — the library's own rule is "ship the
   pattern marked for what it is, rather than not shipping it."

## Step 3 — Deliver

Every delivery includes, for each KU:

1. The KU file itself, delivered at its bundle path per `references/naming-standard.md`:
   `knowledge-units/<KU-ID>/knowledge-unit.md` (e.g.
   `knowledge-units/MCA-001/knowledge-unit.md`). The ID goes in the directory name only —
   never the title. If the user's library visibly and consistently uses a different,
   documented convention, match the library and say so explicitly; otherwise this is the
   standard, not a default to deviate from.
2. A **quality report**: rubric scores with one-line evidence each, validator output,
   Knowledge Fabric findings (or "fabric unavailable — checks skipped"), and open gaps
3. A **recommendation**: ship as-is / ship with named follow-ups / needs a peer reviewer
   for X / split into N KUs (with proposed titles)

## Invariants (apply in every mode, every stage)

- **One decision per KU.** The supersession-seam test decides splits: if a future product
  release would invalidate only part of the KU, that part is its own KU.
- **Append-only.** Never edit a published KU in place. Changes to an Approved KU mean a
  successor KU wired up via `supersedes`/`superseded_by`.
- **Opinionated.** "It depends" is not guidance. "It depends on these signals, and here is
  what to do in each case" is (Tier 2). For Tier 3, the opinion is the list of questions.
- **Don't repeat the product manual.** If help.qlik.com explains it, link it in
  `qlik_help_links` and capture only the judgment the manual lacks.
- **Honest metadata beats impressive metadata.** Low confidence, Proposed status, and
  `source_basis: Product Documentation` are all legitimate. A reader weighs a pattern from
  three engagements differently from one from the manual — never inflate.
- **Never fabricate field experience**, customer evidence, anti-patterns, versions, or
  links. If the author can't supply it, leave it null/absent and list it as a gap.
- **Downgrade, don't assert.** If a product capability claim is uncertain, do not state it
  as fact and do not silently drop it: express it as a Boundary, a Consequence, a Field
  Qualification Question, or a validation step — and flag it for SME verification.
- **Canonical structure is fixed.** Eleven H2 sections in exact order — six required
  (Context, Guidance, TOGAF Impact, Well-Architected Impact, Consequences, Anti-Patterns)
  and five optional (Boundaries, Customer-Ecosystem Notes, Field Qualification Questions
  (Tier 3), Implementation Guidance, Operationalization Guidance) — see the template. An
  optional section may be omitted entirely when it doesn't add anything ("an empty
  optional section is fine; a padded one is not"); it is not gated on Tier. For Tier 3,
  Field Qualification Questions (Tier 3) becomes the de facto main section and should not
  be omitted. No extra top-level sections unless the user asks.
- **ID and bundle path are fixed by standard, not invented per-KU.** Allocate IDs and
  deliver files exactly per `references/naming-standard.md` — the three-letter prefix
  encodes architecture area + deployment scope + TOGAF layer, and the file always lands
  at `knowledge-units/<ID>/knowledge-unit.md`. Never derive an ID from a product name and
  never put the title in the path.
