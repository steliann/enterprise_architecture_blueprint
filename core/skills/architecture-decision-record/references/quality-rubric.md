# ADR quality rubric

Score every criterion **Pass / Weak / Fail** with one line of evidence — a quote or a section reference. Never score on vibes. A criterion with no evidence line isn't scored.

## Gate 0 — Is this an ADR at all?

Before scoring, three tests. Failing any one means the artifact isn't an ADR.

| # | Test | Pass looks like | Fail looks like |
|---|---|---|---|
| 0.1 | Real choice | Two or more paths were genuinely available | Only one path was ever possible — it's an implementation note |
| 0.2 | Future audit | Someone will ask "why this way?" in six months | Nobody will ever ask; it's configuration documentation |
| 0.3 | Named alternative | At least one realistic alternative exists | No alternative can be named, and no reason is given for that |

A narrow decision can still be a valid ADR — "Use OIDC with Okta for Qlik Cloud SSO" qualifies if identity options existed and the choice carries security and operational consequences. A setting with no architecture consequence does not: "set timeout to 60 seconds" is an ADR only if it encodes a deliberate resilience or platform-limit decision.

## Group A — Decision quality

All five required. These are the criteria that separate a decision record from documentation.

| # | Criterion | Pass looks like | Fail looks like |
|---|---|---|---|
| A1 | One clear decision | A reader points at one sentence and says "that's what we decided" | The reader has to assemble the decision from the narrative |
| A2 | The need is established | Context makes the decision unavoidable | Context reads like background; nothing forces a choice |
| A3 | Realistic options compared | Alternatives a competent architect would have considered, each with real limitations | Strawmen, or only the chosen option documented |
| A4 | Selected option explicit | Decision Outcome names it outright | The selection is implied by tone or ordering |
| A5 | Trade-offs captured | Negative consequences a reasonable person would push back on | All-positive consequences, or generic cautions about change |
| A6 | Operationally credible | States what must be owned, monitored, governed, and reviewed after go-live | Stops at "configure the product" |
| A7 | Reviewable later | Review triggers a future architect can observe happening | No triggers, or triggers phrased as "if requirements change" |

## Group B — Sizing

| # | Criterion | Pass looks like | Fail looks like |
|---|---|---|---|
| B1 | Supersession seam | If the selected option changed, essentially the whole ADR would change | Parts of the ADR would survive unchanged — it holds multiple decisions |
| B2 | Not too small | Narrow but architecturally consequential | Records a setting with no architecture consequence |
| B3 | Three-minute read | A peer understands decision, alternatives, trade-offs, and review conditions in three to five minutes | Fifteen minutes (multiple decisions) or thirty seconds with "but why?" left over (too thin) |

**Too-big signals** for B1 — any two of these means split:

- the Decision paragraph contains "and" between two independent choices;
- Options Considered compares answers to different questions;
- different owners would approve different parts;
- one part is strategic and another operational;
- one part is product selection and another runtime topology;
- one part could be superseded without touching the rest;
- different KUs support different parts;
- the review triggers apply to only one section.

When unsure, split. Two short linked ADRs govern better than one that hides choices.

## Group C — Record integrity

Mostly automated — `scripts/validate_adr.py` covers the mechanical half. Score the judgment half.

| # | Criterion | Pass looks like | Fail looks like |
|---|---|---|---|
| C1 | Sections substantive | Every required section carries real content at the target density | Sections present but padded to satisfy the validator |
| C2 | Honest provenance | `status`, `confidence`, `used_ai_to_prepare` all truthful | `Accepted` on an unreviewed draft; AI assistance unrecorded |
| C3 | Capability precision | Product claims are validated, or marked as assumption / constraint / open question | Unvalidated Qlik or Talend capability asserted as fact |
| C4 | Relationships correct | Cited IDs exist and resolve; supersession is two-way | Invented IDs, dangling references, one-way supersession |
| C5 | Scope honest | `decision_scope` matches how reusable the decision actually is | A customer-specific decision presented as reusable guidance |
| C6 | KU alignment disclosed | Support, constraint, and contradiction all stated per `ku-alignment.md` | A contradiction left unmentioned |
| C7 | Naming compliant | ID, H1, and filename aligned per `naming-standard.md`; title names a decision | Status or date in the filename; title names a topic |

## Red flags

Fast pre-scoring sweep. Two or more true means the ADR needs revision before approval.

- Decision section doesn't start with "We will".
- More than one primary decision.
- Selected option not explicitly stated.
- Options weak, unrealistic, or strawmen.
- Consequences entirely positive.
- Trade-offs generic.
- Reads like a product tutorial.
- Reads like a project plan.
- Duplicates a KU instead of citing it.
- Contradicts a KU without explaining the exception.
- No review triggers.
- Open questions that could invalidate the selected option.
- Claims unvalidated product capabilities.
- `status: Accepted` without a governance path having been followed.

## The gate

- **PASS** — every criterion Pass, validator clean (warnings acceptable if explained in the report). Deliver.
- **FAIL** — any criterion Fail, or validator errors. Return to interrogation with questions targeted at the failing criteria only; revise; re-score. Maximum two revision rounds — after that, deliver with `status: Draft`, honest `confidence`, and the gap list. Do not loop forever and do not silently lower the bar.
- A **Weak** is not a Fail, but three or more Weaks in Group A counts as a Fail: the ADR is mediocre everywhere, which is its own failure.
- Gate 0 failure is not a FAIL to be revised. It means this content isn't an ADR. Say so and name where it belongs.

## Report format

```
## Quality Report — <ADR id>: <title>
Gate: PASS | FAIL (round N) | DELIVERED AS DRAFT | NOT AN ADR
Validator: clean | N warnings | N errors (summarize)
Fabric check: done — <findings> | unavailable — skipped
Operation: author | normalize | extend | supersede | deprecate | review

| Criterion | Score | Evidence |
|---|---|---|
| A1 One clear decision | Pass | "We will use ..." |
...

Gaps / follow-ups: ...
Recommendation: ship as-is | ship with follow-ups | needs review by <who / what expertise> | split into: <titles> | not an ADR — belongs in <where>
```

For refresh, add a **What changed** list. For review, add the findings table from `review.md`.

## Escalate to the architecture workstream when

Don't sit on these — an unclear decision in the repository gets reused incorrectly.

- The selected option can't be identified.
- You can't tell whether the content is a KU or an ADR.
- You can't decide whether to split.
- You can't tell whether the ADR contradicts a KU or is a valid exception.
- An existing KU may be outdated.
- The decision owner is unidentifiable.
- Open questions could change the selected option.
- The decision has strategic impact beyond its stated scope.
- The decision depends on uncertain product capability.
- A customer-specific decision looks like it should become reusable guidance.
