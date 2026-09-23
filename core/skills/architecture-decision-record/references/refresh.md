# Refresh mode — existing ADR

An ADR already exists. Something about it needs to change. Before touching anything, work out which of four operations this actually is — they have very different rules.

## Stage 0 — Classify the operation

| The change is | Operation | Rule |
|---|---|---|
| Structure, formatting, invalid YAML, missing sections, weak wording — decision unchanged | **Normalize** | Edit in place. Same ID. |
| New information strengthens or clarifies the existing decision — decision unchanged | **Extend** | Edit in place if `status` is Draft or Proposed. Same ID. |
| The selected option changes, or the decision's scope materially changes | **Supersede** | New ADR, new ID, two-way link. Never edit in place. |
| The decision no longer applies and nothing replaces it | **Deprecate** | Set `status: Deprecated`, leave `superseded_by: null`, add a note in Decision Outcome saying why. |

The governing rule: **an Accepted ADR is append-only.** If `status: Accepted` and the decision itself is changing, this is a supersession regardless of how small the change looks. Silently rewriting an accepted decision destroys the audit trail the ADR exists to provide.

If you're unsure whether the decision changed or was merely clarified, ask. Getting this wrong is worse than one extra question.

### Supersession mechanics

Read `naming-standard.md`, then:

- Replacement ADR gets a **new** ID from the next free sequence number in that scope. The old number is retired permanently.
- Superseded ADR keeps its ID, `status: Superseded`, `superseded_by: <new-id>`.
- Replacement ADR carries `supersedes: <old-id>`, `superseded_by: null`.
- No partial supersession. "Replaces section 3 only" means the original ADR was too broad — split it, or supersede it with several narrower ADRs.
- If the ADR you'd be superseding belongs to someone else, produce the recommendation and tell that owner. Don't enact it unilaterally.

Deliver **both** files when superseding: the edited original and the new replacement.

## Stage 1 — Interrogate

Read the existing ADR first, cold, and note what's actually wrong before asking anything. Then ask only about the gaps you can't resolve from the text.

Preserve unless you have a reason to change:

- the ADR ID;
- the selected option;
- relationships — `related_patterns`, `related_adrs`, `impacted_architecture_views`, `related_assets`;
- tags;
- decision owner and contributors;
- the original `date` (the decision date doesn't move because you reformatted it).

**Never silently change the selected option.** If the existing ADR is ambiguous about what was selected, infer the most likely option, state the inference explicitly in Open Questions, and flag it in the quality report. Do not resolve the ambiguity by picking one and moving on.

## Stage 2 — Cross-check

Read `ku-alignment.md`. Refresh-specific concerns:

- Verify every cited ID still exists and still resolves. Stale citations are common in older records.
- Re-run the alignment checks — a KU published after this ADR may now support, constrain, or contradict it. A new contradiction is a review trigger, and it needs the `## Knowledge Unit Alignment` section added.
- Check whether a citation drifted: same ID, but the KU's guidance changed underneath it.

## Stage 3 — Rewrite

Read `canonical-structure.md`. Then, in order:

1. Fix invalid YAML. The common defects in the existing corpus: `*` used as a list bullet (YAML reads it as an alias and the file won't parse at all), lost indentation under `technology_scope` so `qlik`/`talend`/`third_party` flatten to top-level keys, and a missing `review_by`.
2. Migrate the metadata shape. Canonical `technology_scope` has three keys — `qlik`, `talend`, `third_party` — each a list or `null`. Older records using a two-key shape get `talend` added.
3. Normalize headings to canonical order and level. `Implementation Implications` and `Operational Implications` are **required**, not optional — some older templates mark them optional and are wrong.
4. Remove duplication. Refreshed ADRs often repeat Context inside Decision Outcome, or restate drivers as consequences.
5. Convert implementation-only notes into decision language, or move them out and say where they went.
6. Strengthen the weak sections. In practice this is almost always: decision drivers that state preferences rather than requirements, options with no real limitations, consequences that are entirely positive, and absent or generic review triggers.
7. Update `date` only if the decision itself was re-made. Set `review_by` to something defensible — tie it to a product release cycle, customer milestone, contract phase, or the architecture review cadence rather than picking an arbitrary six months.

## Stage 4 — Assess

```
python3 scripts/validate_adr.py <path-to-adr>.md
```

Run it on the original **before** you edit as well. The before/after comparison is the most useful thing in the quality report for a refresh, and it shows the user what was actually broken.

Then score against `quality-rubric.md` and apply the gate.

## Stage 5 — Deliver

File(s), quality report, recommendation. The refresh report should include a short **what changed** list — structural fixes, metadata migrations, content strengthening, and anything you deliberately left alone. If you inferred an ambiguous selected option, put that at the top of the report, not buried in Open Questions.
