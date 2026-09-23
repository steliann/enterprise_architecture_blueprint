# v2 → v3 changelog

Corrections applied after cross-checking v2 against the team's authoritative source
docs (`01_knowledge_unit_authoring_guide.md`, `02_..._template_sample.md`,
`03_..._template_blank.md`, `04_file_naming_standard-2.md`).

## Naming and file location (the critical fix)
- **ID scheme replaced.** v2 used product-prefix IDs (`REPL-003`). v3 uses the
  standard's `ADL-NNN` scheme — architecture area + deployment scope + highest TOGAF
  layer, sequence scoped per exact prefix. New: `references/naming-standard.md`.
- **Delivery path replaced.** v2 delivered a flat file `<ID>-<title>.md`. v3 delivers
  the fixed bundle path `knowledge-units/<ID>/knowledge-unit.md`; the ID is never
  paired with the title in a path.
- `scripts/validate_ku.py`: `ID_RE` now enforces the actual letter sets per position
  (previously accepted any 2-10 char alphanumeric prefix); a new bundle-path check
  (single-file and corpus-level) verifies the directory name equals the ID and the
  filename is literally `knowledge-unit.md`; old-style IDs/filenames are recognized
  and flagged with a migration message rather than silently accepted.
- `--corpus` now uses `rglob` instead of `glob` so it finds KUs nested in bundle
  directories, not just flat files in one folder.
- All four mode reference files, `SKILL.md`, and `knowledge-fabric.md` updated to
  reference the naming standard when allocating IDs or delivering files.

## Section structure corrected to match the guide
- **Added the missing `Customer-Ecosystem Notes [optional]` section** — present in
  both source templates, absent from v2's canon entirely.
- **Required/optional inverted back to the source.** v2 treated all ten sections as
  required (Tier 3 exempted only three). v3 has six always-required sections (Context,
  Guidance, TOGAF Impact, Well-Architected Impact, Consequences, Anti-Patterns) and
  five genuinely optional ones (Boundaries, Customer-Ecosystem Notes, Field
  Qualification Questions (Tier 3), Implementation Guidance, Operationalization
  Guidance) that may be omitted entirely at any tier, not just marked "N/A" at Tier 3.
- **Heading names corrected** to match the source templates exactly:
  `Operationalization Guidance` (was `Operationalization`), `Field Qualification
  Questions (Tier 3)` (was `Field Qualification Questions`). Old names accepted as
  aliases with a warning.
- **`togaf_layers` enum fixed** — added `Security`, which both source templates allow
  and v2's validator rejected. (The ID's third letter remains B/A/D/T only — `Security`
  is metadata-only, per the naming standard.) `TOGAF Impact` body may now carry an
  optional trailing `### Security` subsection.

## Structural rules loosened to match the guide (previously invented, not sourced)
- **Boundaries**: one short paragraph (or a short list), not a mandatory two-part
  "applies when / does not apply when" bulleted split.
- **Consequences**: free-form prose or bullets; the "Positive consequences /
  Negative consequences" subsection split is no longer enforced.
- **Anti-Patterns**: guide says "one or two specific traps"; v2 required 4-6. v3
  requires at least one (the section itself stays required) and only warns if the
  count runs well past two, rather than failing KUs with fewer.
- **Size heuristic**: v2's 1,600-2,800 word target wasn't sourced from the guide,
  which actually specifies a *behavioral* test ("read in about three minutes and then
  apply it"). v3 approximates that as ~250-2,200 words and says so explicitly, rather
  than presenting an invented range as a firm target.

## Also corrected while in here
- `references/knowledge-fabric.md`'s observed-index list was two months stale (missing
  `call_transcripts`); updated and dated, with a privacy-hygiene note extending the
  case_information rule to it (sales/account data, not architecture guidance).

## Not changed
- Frontmatter fields, enums (status/tier/confidence/source_basis/pillars), AI-assistance
  fields, relationship-field semantics, and the append-only/supersession model were
  already consistent with the source docs and are unchanged.
