# Mode: Review

Assess one or more existing KUs for **quality** (against the rubric), **consistency**
(against the template, and against each other when reviewing a batch), and **validity**
(against the Knowledge Fabric and current product reality). The reviewer's output supports
the peer-review step that moves a KU from Proposed to Approved — so be specific enough that
the author can act on every finding without coming back to ask what you meant.

Review is assessment, not rewriting. Do not silently fix the KU. Findings + concrete
recommendations; offer to apply fixes only after presenting them — and remember the
append-only rule: an Approved KU is never edited in place, so fixes to an Approved KU must
be framed as a successor record.

## Stage 1 — Interrogate (the KU, then the author)

Read the KU(s) cold, as the target reader: a CSE/EA on a live engagement with three
minutes. Capture first-read reactions — "would I recognize this situation?", "do I know
what to do now?", "what would I still have to ask a colleague?" These reactions are Group A
evidence; collect them before detailed criterion-by-criterion work, because a second
reading is too informed to notice them.

Then ask the author/requester only what the review needs: is this pre-peer-review or an
audit of older content? Is there authority to propose supersessions? For batch reviews:
any known overlaps to focus on?

## Stage 2 — The three review lenses

**Quality.** Score the full rubric (`quality-rubric.md`) with evidence per criterion.
Apply tier-appropriate expectations — do not fail a Tier 3 KU for a light Guidance section;
do fail a Tier 1 KU for variants creeping in.

**Consistency.**
- Run `scripts/validate_ku.py` for schema/structure conformance — on the whole library
  (`--corpus <dir>` or all files at once) when reviewing more than one KU, so duplicate
  IDs, bundle-path/id mismatches, dangling relationships, and broken supersession
  reciprocity are caught mechanically.
- Check the file location itself against `references/naming-standard.md`: is the KU at
  `knowledge-units/<ID>/knowledge-unit.md`, with the ID (not the title) as the directory
  name? Flag anything still on the deprecated flat-filename convention as a Minor finding
  with "migrate to bundle path" as the fix (see `refresh.md`).
- Check internal coherence: does the title match the Guidance? Does the tier match the
  shape? Do tags/togaf_layers/pillars match the content? Does Consequences contradict
  Guidance?
- Batch reviews additionally: same decision covered twice (run the overlap triage in
  `knowledge-fabric.md` check 1 — duplicate vs. version-drift supersession vs. legitimate
  alternative), inconsistent terminology for the same
  concept, relationship asymmetries (A relates to B but not vice versa), broken
  supersession chains, ID collisions.

**Validity.**
- Fabric checks 1–3 from `knowledge-fabric.md`: is this KU now duplicated, contradicted, or
  superseded-in-fact by newer fabric content?
- Staleness: `review_by` in the past? Product versions in scope now EOL or several releases
  old? Links dead? Flag for review/supersession rather than guessing at corrections.
- Truth check within your means: verify product claims against help.qlik.com links given;
  where you cannot verify a field claim, say "unverified — needs SME", never "wrong".

## Stage 3 — "Draft" = the findings

For each KU, the quality report (format in `quality-rubric.md`) plus a findings list, each
finding: **severity** (Blocker: would mislead a reader or fails the gate / Major: weakens
reuse / Minor: polish), **location**, **what and why**, **concrete fix**.

## Stage 4 — Assess

Self-check the review: every Blocker/Major tied to a rubric criterion or validator error?
Every fix actionable as written? Tier expectations applied?

## Stage 5 — Gate and deliver

The gate here applies to the *verdict*, not to rewriting:

- **PASS** → "ready for peer review / re-approval", with Minors listed.
- **FAIL** → the targeted list of what must change, plus the recommendation: fix-in-place
  (only if status is Draft/Proposed), supersede (Approved KUs), split (B1 failures, with
  proposed titles), fold (B2 failures, with target KU), deprecate (duplicated/obsolete),
  or **refresh** (structurally non-canonical but sound in substance → `references/refresh.md`).

Batch reviews end with a one-table summary: KU id → gate result → top finding →
recommended action.
