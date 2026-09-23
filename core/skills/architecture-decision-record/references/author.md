# Author mode — new ADR

You have source material and no existing ADR. Turn the material into one decision record.

## Stage 0 — Is this even an ADR?

Run this before gathering anything else. Three tests from the authoring guide, all must pass:

1. **The real choice test.** Was there a meaningful choice? If only one path was ever possible, this is an implementation note.
2. **The future audit test.** Would someone in six months ask "why did we do it this way?" If no, it belongs in implementation documentation.
3. **The alternative test.** Can you name at least one realistic alternative? "Do nothing", "use the existing platform", "build custom", "use the Qlik-native capability", "use a third-party capability", and "defer the decision" are usually available. If none are realistic, explain why in one line — and if you can't, this isn't an ADR.

Also run the **sizing gate** from `quality-rubric.md` (criterion B1). If the material carries two or more independent decisions, say so now and propose the split before drafting. Two short linked ADRs govern better than one that hides choices.

If the material fails these tests, tell the user plainly, name where the content should live instead, and stop. Don't produce a hollow ADR to be agreeable.

## Stage 1 — Interrogate

The source material determines your opening line of questioning. Pick the matching start.

### Starting from a Knowledge Unit

The decision applies existing reusable guidance to a specific context. Open the KU's Guidance and Boundaries, then ask:

- Does this customer or program context fit inside the KU's stated boundaries?
- Is the ADR following the KU guidance directly, or only conditionally?
- Does anything here trip a KU anti-pattern?
- Which KU constraints have to become ADR assumptions, risks, or review triggers?

This is the cleanest path. The KU has already done the option analysis; your job is to record which way this context went and what's context-specific about it.

### Starting from an architecture discussion

Workshop, design review, customer call, internal debate. Extract, in this order:

- the problem that forced a decision;
- the options actually discussed;
- which one was selected;
- the stated reason;
- the trade-offs anyone named out loud;
- who owns the decision;
- what anyone said would make them revisit it.

Do not transcribe the discussion. Convert it into decision language. Hedging in a meeting ("we're leaning towards...") becomes either a decision with `status: Proposed` or an open question — never a vague Decision paragraph.

### Starting from an existing project note

Slide deck, design document, delivery plan, implementation doc. Find the decision seam first, then sort the content into buckets:

- decision content → the ADR;
- implementation implications → the ADR's Implementation Implications, condensed to what teams must account for;
- operational implications → the ADR's Operational Implications;
- project tasks, tutorial steps, background → **not** the ADR. Say where they should go.

The failure mode here is a decision record that reads like a product tutorial. Watch for it.

### What to gather in all cases

Ask in one or two batched rounds, not fifteen separate questions. Critical fields — block on these: the decision itself, at least two realistic options, the selected option, the decision owner, the scope (customer / program / product platform / enterprise / reference architecture).

Everything else can start as `null` or a flagged placeholder: ID (see below), title, status, dates, contributors, technology scope, relationships, tags. Flag placeholders in the quality report rather than stalling the draft.

### ID allocation

Read `naming-standard.md`. Allocate from the real corpus: find the existing prefixes and the highest used sequence number for the relevant scope, then take the next number. If you can't reach the corpus, write `<PREFIX>-ADR-XXX` and flag it — a colliding ID is worse than a visible placeholder. Never renumber to fill a gap. Never reuse a superseded number.

## Stage 2 — Cross-check

Read `ku-alignment.md` and run all four checks. Two hard rules:

- `related_patterns`, `related_adrs`, `supersedes`, `superseded_by` get real IDs only. If you couldn't verify one, leave the field `null` and note the intended relationship as an open question.
- If a KU materially supports, constrains, or contradicts the decision, add the optional `## Knowledge Unit Alignment` section. A contradiction that isn't stated is the single worst governance failure an ADR can commit.

## Stage 3 — Draft

Read `canonical-structure.md` and build on `assets/adr_template.md`. Section order and headings are exact — the validator enforces them.

Content discipline while drafting:

- Context establishes the need before any product is named. If paragraph one names the selected product, rewrite it.
- The Decision paragraph is the decision, not the rationale. Rationale lives in Decision Outcome.
- Decision drivers explain why a decision was *required*. "Better performance" is not a driver unless you say which architectural constraint made performance decisive.
- Consequences are concrete. "Improved governance" is weak; "creates one governed quality baseline visible in the catalog before operational remediation exists" is a consequence.
- Negative consequences are the trade-offs this decision creates, not generic cautions about change.
- Risks use the exact form `Risk: <risk>. Mitigation: <mitigation>.` and are specific to this decision.
- Review triggers are conditions a future architect can actually observe: a product capability shipping, a platform migration, a new NFR, a security policy change, a cost model change, an operating model change.

Target length: a peer reads it in three to five minutes. Fifteen minutes means multiple decisions. Thirty seconds with "but why this one?" left over means it's too thin.

## Stage 4 — Assess

```
python3 scripts/validate_adr.py <path-to-adr>.md
```

Add `--schema assets/architecture-decision-record.schema.json` when you want full metadata-model validation, and `--json` when you want to parse the result. Exit 0 clean, 1 warnings, 2 errors.

Fix every error. Then score against `quality-rubric.md` and apply the gate.

## Stage 5 — Deliver

Per SKILL.md Step 3: file, quality report, recommendation. Save to `decision-records/<lowercase-id>-<short-kebab-title>.md`.

If the gate failed twice, ship as `status: Draft` with honest `confidence` and the gap list. Don't loop forever and don't quietly lower the bar to make the gate pass.
