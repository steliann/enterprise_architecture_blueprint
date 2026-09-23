---
name: architecture-decision-record
description: Author, refresh, or quality-review Qlik/Talend enterprise-architecture Architecture Decision Records (ADRs) in the canonical Markdown-with-YAML-frontmatter format. Use this skill whenever the user mentions ADRs, decision records, capturing an architecture decision, turning a workshop/design review/project note into a decision record, allocating an ADR ID, superseding an existing ADR, checking an ADR against the Knowledge Fabric or against Knowledge Units, or reviewing/validating/scoring an ADR. Trigger even if the user just says "write this up as a decision record", "did we ever decide X?", "this ADR needs fixing", or pastes an existing ADR and asks for it to be normalized. Do NOT use this skill for authoring Knowledge Units (a KU captures reusable guidance; an ADR cites KUs but is not one — use knowledge-unit-architect for those), for plain Knowledge Fabric searches, or for implementation documentation that records no architecture choice.
---

# Architecture Decision Record

**Skill version: 3** — see Changelog at the end.

A Knowledge Unit captures reusable **guidance**. An ADR captures a specific **decision**: what was selected in one customer, program, product-platform, enterprise, or reference-architecture context, why, what was rejected, and when it must be reviewed. An ADR may cite KUs as evidence. It is never a KU, a project plan, a product tutorial, or a meeting summary.

## Step 1 — Pick the mode

| The user wants | Mode | Read |
|---|---|---|
| A new ADR from a discussion, workshop, KU, design doc, or project note | **Author** | `references/author.md` |
| An existing ADR normalized, corrected, extended, or superseded | **Refresh** | `references/refresh.md` |
| An ADR (or a folder of them) assessed, scored, or peer-reviewed | **Review** | `references/review.md` |

Read only the active mode's file. It will tell you when to pull in the shared files (`quality-rubric.md`, `naming-standard.md`, `ku-alignment.md`, `canonical-structure.md`). Don't read everything up front.

Two mode traps worth catching before you read anything:

- The user says "refresh" but supplies no existing text — that's Author.
- The user says "write an ADR" but the material records no choice between realistic alternatives — run the **is this even an ADR?** gate in `references/quality-rubric.md` first and say so. Implementation notes belong elsewhere.

If the mode is genuinely ambiguous, ask one question. Don't guess across a fork this large.

## Step 2 — The pipeline

Every mode runs the same five stages. The mode file defines what each stage means for that mode.

1. **Interrogate.** Gather what's missing. Batch questions with AskUserQuestion rather than dribbling them out one at a time. Never stall on cosmetic metadata — use `null`, flag it, move on.
2. **Cross-check.** Look up real KU and ADR IDs before citing any. Run the KU-alignment checks in `references/ku-alignment.md`. Never invent an ID.
3. **Draft.** Build on `assets/adr_template.md` and the section contract in `references/canonical-structure.md`. Never reproduce structure from memory.
4. **Assess.** Run `scripts/validate_adr.py`. Then score against `references/quality-rubric.md`. Run the script; don't eyeball it.
5. **Gate and deliver.** Apply the rubric gate. Then deliver the three artifacts below.

## Step 3 — Deliver

Three artifacts, always, in this order:

1. **The ADR file**, saved per `references/naming-standard.md` — `decision-records/<lowercase-id>-<short-kebab-title>.md`. Present it as a file; don't just print it inline.
2. **The quality report**, in the format fixed by `references/quality-rubric.md`, including validator output.
3. **A recommendation** — ship as-is, ship with follow-ups, needs review by a named person or expertise, or split into these ADRs.

Never deliver the file alone. A structurally valid ADR can still be a bad decision, and the report is where you say so.

## Invariants

These hold in every mode. They override any inference from the source material.

- **One decision per ADR.** The test is the supersession seam: if the selected option changed, would the whole ADR change? If no, it holds more than one decision. When unsure, split.
- **Append-only once Accepted.** An Accepted ADR is not rewritten in place. Material change means a successor ADR with a new ID and a two-way `supersedes` / `superseded_by` link. IDs are never reused, never renumbered to close gaps.
- **The decision must be explicit.** One paragraph starting "We will", and a Decision Outcome that names the selected option outright. A reader must never have to infer what was decided.
- **Options must be real.** At least two, no strawmen. Rejection needs an architecture reason, not a preference. Deferral needs the condition that would make the option viable.
- **Trade-offs are mandatory.** Every architecture decision gives something up. An ADR with only positive consequences is not finished.
- **Never overstate product capability.** An uncertain Qlik or Talend capability becomes an assumption, a constraint, an open question, or a review trigger — not a claim.
- **Honest metadata over impressive metadata.** Draft with `confidence: Low` and open questions beats Accepted with invented certainty. Record AI assistance in the frontmatter; it's provenance, not a weakness.
- **Escalate rather than fudge.** If you can't identify the selected option, can't tell KU from ADR, can't decide whether to split, or the open questions could change the selected option — say so in the recommendation and name it as needing architecture review.

## Format note

The canonical format uses an em dash in `# <ID> — <Title>` and `### Option N — <Name>`, and the validator matches on it. Use the em dash in those two constructs. Everywhere else, follow the user's prose preferences.

## Quoting rule

`title`, `decision_owner`, `decision_type`, `supersedes`, `superseded_by`, and every non-null item in `contributors`, `technology_scope.qlik`, `technology_scope.talend`, `technology_scope.third_party`, `related_patterns`, `related_adrs`, `impacted_architecture_views`, `related_assets`, and `tags` are always quoted in the YAML source — even a bare value with no punctuation. `scripts/validate_adr.py` checks this against the raw text and errors on any of them left unquoted.

## Changelog

**v3**

- Fixed a generation bug: several YAML frontmatter fields were coming out unquoted. `scripts/validate_adr.py` now checks the raw YAML text (not just the parsed values, which lose quoting once parsed) and errors if `title`, `decision_owner`, `decision_type`, `supersedes`, `superseded_by`, or any non-null item in `contributors`, `technology_scope.qlik/talend/third_party`, `related_patterns`, `related_adrs`, `impacted_architecture_views`, `related_assets`, or `tags` is left unquoted.
- Fixed the bundled example (`assets/example/decision-records/spx-adr-001-...md`), which had this exact bug — an unquoted `title` and four unquoted `tags` entries — and now validates clean under the new check.
- Updated `assets/adr_template.md` and `references/canonical-structure.md` to state the quoting rule explicitly, and fixed two unquoted example snippets in `references/naming-standard.md` (a `related_adrs` list and a `supersedes`/`superseded_by` pair) that modeled the wrong pattern.
- `ai_solutions_used` items were intentionally left out of this rule — they weren't in the reported list. Flag if that was an oversight and it should be added too.
