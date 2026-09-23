# Mode: Refresh ("preserve-then-normalize")

Rewrite an existing KU into the canonical structure while preserving its architectural
intent. This is a preservation and normalization task — not greenfield drafting (build
modes) and not assessment-only (review mode). Typical triggers: a KU written before the
canon existed, a validator failure list, "bring this KU up to standard".

**Append-only guard first.** Refresh-in-place is allowed only for `Draft` or `Proposed`
records. If the KU is `Approved`, a refresh that changes meaning must become a successor
record (`supersedes`/`superseded_by`); a refresh that only fixes structure/YAML without
changing the recommendation may be applied in place, but say so explicitly and recommend
the owner re-review. Keep the same KU ID and bundle directory unless the user asks
otherwise — per `references/naming-standard.md` the ID/directory are permanent regardless
of content changes. If the KU currently lives under the deprecated flat-filename
convention (`<ID>-<title>.md`, no bundle directory), migrating it to
`knowledge-units/<ID>/knowledge-unit.md` is itself an in-place-safe structural fix — do it
and say so in the change log, even if nothing else changes.

## Stage 1 — Interrogate (the diff, then the author)

1. Run `scripts/validate_ku.py` on the existing file — the error list is the work list.
2. Diff the KU against the canonical template: which sections are missing, mis-ordered,
   merged, or non-canonical? Which YAML fields are absent, placeholder, or invalid?
3. Ask the author only what the existing text cannot answer: missing metadata (owner,
   versions, deployment, provenance, dates), conflicts between the old text and current
   product reality, and any updated intent. If old content and new input conflict, prefer
   the newer input; preserve original content only where it remains compatible.

## Stage 2 — Fabric cross-check

Lightweight unless scope changed: confirm the KU's decision is not now duplicated,
contradicted, or superseded-in-fact (checks 1 and 3 in `knowledge-fabric.md`). A refresh
that discovers version drift becomes a supersession, not a rewrite — switch to the
build-from-scratch drafting rules for the successor.

## Stage 3 — Draft (normalize)

- Rewrite into the canonical ten-section body on `assets/ku_template.md`; fix YAML against
  the schema-conformant frontmatter. Never invent fields or extra H2 sections.
- Preserve: architecture rationale, boundaries, relationships, ADR references, assets,
  references, tags, known risks. Remove duplication. Normalize headings and terminology
  ("Knowledge Unit" = the artifact; "pattern" = the approach; "guidance" = the direction).
- Convert implementation-only notes into reusable architecture guidance; strengthen vague
  content into clear positions where the original intent supports it.
- Downgrade unsupported or uncertain claims to a Boundary, Consequence, Field
  Qualification Question, or validation point — never assert, never silently delete.
- Missing facts the author can't supply: `null` / "[TBD]" + a gap-list entry. Do not
  invent anti-patterns, reviewers, versions, or links to fill canonical sections.

## Stages 4–5 — Assess, gate, deliver

Per SKILL.md and `quality-rubric.md`. Delivery extras for this mode:

- A **change log**: what was restructured, what was preserved verbatim-in-substance, what
  was downgraded to boundary/question, what was dropped (and why).
- Validator before/after summary.
- If the KU was Approved: the in-place vs successor decision, stated explicitly.
