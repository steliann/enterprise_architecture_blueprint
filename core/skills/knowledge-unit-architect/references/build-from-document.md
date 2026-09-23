# Mode: Build from Document ("big-then-carve")

Convert an existing artifact — reference architecture, wiki page, customer document,
meeting transcript, runbook — into one or more KUs. The method is **big-then-carve**: treat
the document as one oversized draft, find the supersession seams, and carve candidate KUs
along them. Expect some candidates to fold back into siblings; that is normal.

The hard part of this mode is not writing — it's that documents contain *facts and
descriptions*, while KUs contain *decisions and judgment*. Most of the interrogation exists
to recover the judgment the document left out.

## Stage 1 — Interrogate

**1a. Read and map the document.** Produce a decision inventory: every place the document
takes (or implies) a position — a default, a recommendation, a "we chose X", a warning.
Each inventory entry gets: the candidate decision in one sentence, the re-askable question
it answers, and a guessed tier. Ignore pure description (product features, definitions) —
that content links to the manual, it doesn't become KUs.

**1b. Carve.** Group inventory entries along supersession seams (quality-rubric.md Group B):
things replaced together stay together. Present the proposed carving to the user as a short
list — "this document yields N candidate KUs: …, plus these sections I propose to drop
because they restate documentation" — and get agreement before drafting. Carving is the
highest-judgment step; don't do it silently.

**1c. Recover what the document doesn't say.** For each agreed candidate, ask the author
(batched, via AskUserQuestion where available) only what the document can't answer:

- Provenance: which engagement(s) did this come from? Any originating ADRs? Honest
  `source_basis` and `confidence`?
- Anti-patterns: what did a customer actually do wrong here? (Documents rarely record this;
  it's often the most valuable thing the interview adds.)
- Trade-offs: what does this pattern give up? What breaks if ignored?
- Tier confirmation, owner, environment specifics (versions, cloud vendor, containerized)
  if absent from the document.

Don't interrogate for what the document already states — extract it. A question the
document answers is a wasted question.

## Stage 2 — Fabric cross-check

Run all four checks in `knowledge-fabric.md` for each candidate. Carving output often
overlaps existing KUs — expect to drop or re-scope candidates here.

## Stage 3 — Draft

One file per surviving candidate, on `assets/ku_template.md` — all ten canonical sections,
exact order, prescribed subsection formats. Rules specific to this mode:

- Quote the document's substance, but rewrite description into guidance: every Guidance
  sentence should describe something the reader can *do*.
- Material that is true but not decision-bearing → `qlik_help_links` /
  `related_assets` / dropped, not padded into sections.
- The source document itself goes in `related_assets`.
- If the author couldn't supply an anti-pattern, leave a marked gap — do not invent one.

## Stages 4–5 — Assess, gate, deliver

Per SKILL.md and `quality-rubric.md`. Mode-specific delivery extras:

- A **carving map**: which document sections became which KU, which were dropped and why,
  which folded into existing fabric KUs.
- Candidates that failed B2 (too small) are listed as folded, with where they went.
- Each surviving candidate gets an ID allocated per `references/naming-standard.md`
  (architecture area + deployment scope + highest TOGAF layer, next free sequence for
  that prefix) and is delivered at its bundle path, not as a flat file.
