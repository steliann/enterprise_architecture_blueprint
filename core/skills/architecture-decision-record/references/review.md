# Review mode — assess an existing ADR

You are the peer reviewer, not the author. Assess and recommend. Do not rewrite the ADR unless the user asks you to switch to Refresh mode.

## Stage 1 — Read cold

Read the ADR once as a reader who has three minutes and wasn't in the room. Capture your first-read reactions **before** you touch the rubric:

- Could you state the decision in one sentence after one pass?
- Did you have to infer the selected option?
- Did anything read as a product tutorial, a project plan, or a meeting summary?
- Did you finish knowing what would make this decision wrong later?
- Did you believe the trade-offs, or were they decoration?

Write these down first. A second reading is too informed to be useful for this, and the three-minute-reader test is the one thing a validator can't check.

Then ask the reader-fit questions you can't answer from the text: is the decision owner right, is the status defensible, is the scope claim accurate.

## Stage 2 — Cross-check

Read `ku-alignment.md`. In review mode you're checking the ADR's citations rather than choosing them:

- Do the cited KU and ADR IDs exist?
- Does the ADR fit the boundaries of the KUs it cites?
- Does it trip any anti-pattern in those KUs?
- Does it contradict a KU without saying so? This is a Blocker.
- Is a KU cited as supporting when it's really only conditionally supporting? Also a finding.

## Stage 3 — Three lenses

Assess along all three. They catch different failures.

**Quality** — is this a good decision record? Score against `quality-rubric.md`.

**Consistency** — does it agree with itself and with the corpus? ID matches the H1 matches the filename. `status` matches the completeness. `confidence` matches the open questions. Relationships resolve. Terminology is used correctly: "decision" for the selected direction, "option" for alternatives, "consequence" for impact, "trade-off" for cost, "review trigger" for a revisit condition.

**Validity** — is the architecture sound? Are claimed Qlik/Talend capabilities real? Are the rejected options rejected for architecture reasons or for preference? Is the sizing right? Where you lack the product knowledge to judge, write "unverified — needs SME confirmation on <specific claim>", never "wrong". Naming what you can't verify is more useful than guessing.

## Stage 4 — Findings

Every finding carries four parts:

- **Severity** — Blocker / Major / Minor;
- **Location** — the section, and the line or quote;
- **What and why** — what's wrong and what it costs the reader;
- **Fix** — concrete, not "consider improving".

Severity calibration:

**Blocker** — the ADR can't be approved as-is. No explicit decision. Selected option unstated. Contains multiple independent decisions. Contradicts a KU without disclosure. Claims an unvalidated product capability as fact. `status: Accepted` with open questions that could change the selected option. Validator errors.

**Major** — approvable only after revision. Strawman options. All-positive consequences. Generic trade-offs. No review triggers, or review triggers no one could observe. Drivers that state preference rather than requirement. Missing required section. `status: Accepted` with `confidence: Low`. Broken supersession chain.

**Minor** — should be fixed, doesn't block. Terminology drift. Filename or ID casing. Weak title that names a topic instead of a decision. Missing tags. Formatting inconsistency. Overlong Context.

## Stage 5 — Deliver

Run `python3 scripts/validate_adr.py <path>.md` and include the output. Then the report per `quality-rubric.md`, plus the findings table:

```
| Severity | Location | Finding | Fix |
|---|---|---|---|
| Blocker | ## Decision | ... | ... |
```

End with the recommendation: approve, approve with minor fixes, revise and re-review, split into these ADRs, or needs SME verification on these specific claims.

## Batch review

Reviewing a folder of ADRs, run the validator across all of them first — one call, many paths — and let that triage which need close reading. Then review each individually, and close with one summary table:

```
| ADR ID | Gate | Top finding | Action |
|---|---|---|---|
```

For a batch, also check the corpus-level things a single-file review can't see:

- ID collisions, and IDs referenced but missing;
- duplicate or reused sequence numbers;
- broken supersession chains — a `superseded_by` pointing at a nonexistent ADR, or a one-way link where the replacement doesn't declare `supersedes`;
- two ADRs deciding the same question in different directions with no relationship between them;
- an ADR still `Accepted` whose `review_by` date has passed;
- scope prefixes not in the registry, or a new prefix created where an existing one already covered the scope.

These corpus defects matter more than individual polish. A library with colliding IDs and dangling references can't be trusted as an audit trail, no matter how well each record reads.
