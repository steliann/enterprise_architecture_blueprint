# KU Quality Rubric and Delivery Gate

Score every KU against all four groups below. The rubric exists because the library fails
in a specific way: a KU that no customer ADR ever cites is dead weight. Every criterion
traces back to "will a peer reuse this on a real engagement?"

Scoring: each criterion is **Pass / Weak / Fail**. Record one line of evidence per
criterion (quote or point to the KU text — never score on vibes).

## Group A — The five marks of a good KU (all required)

| # | Criterion | Pass looks like | Fail looks like |
|---|---|---|---|
| A1 | **Recurring decision** | Answers a question a CSE/EA will face again; you can state that question in one sentence | A fact, a single config detail, a one-off fix |
| A2 | **Opinionated** | Takes a position; Tier 2 lists variants *with the criterion for choosing each*; Tier 3's position is the question list | "It depends" with no signals; a neutral survey of options |
| A3 | **Do AND don't** | Anti-Patterns (required, never omitted) names 1–2 specific traps someone actually fell into ("enabled logical replication on a transactional source with no read replica") — more than a couple is fine if the failure surface is genuinely that wide, but don't manufacture entries to hit a count | Empty, generic ("performance issues"), or restates the Guidance negated |
| A4 | **Recognizable Context** | A peer reads Context and says "I have seen that" — 3–6 sentences, situational, specific | Too general (any customer, any product) or too narrow (one customer's quirks) |
| A5 | **Not the manual** | Captures trade-offs and situational judgment; manual content is linked, not restated | Paraphrases help.qlik.com |

## Group B — Sizing (all required)

- **B1 Supersession seam.** If a future release changes component X, would only part of
  this KU need updating? If yes → split. Other too-big signals: more than one "what to do"
  in Guidance; sections at different tiers; different natural owners; ≥3 "depending on
  whether" clauses; two adjacent ADRs would cite different halves. When unsure, split —
  two short linked KUs beat one big one under the append-only model.
- **B2 Not too small.** Apply three tests together: (1) *re-askable question* — can you
  name the out-loud question it answers? (2) *independent citation* — could a customer ADR
  cite it alone? (3) *guidance vs. setting* — is it a position, not just a value? Fail any
  one → fold into the parent KU's Guidance. **Exception:** a self-contained configuration
  recipe that is looked up repeatedly (e.g. "QDA Cloud SSO with Entra ID") stays its own KU.
- **B3 Right-sized for the canon.** The actual bar is behavioral: a peer should read the
  KU in about three minutes and then be able to apply it. Ten minutes to get through it
  is too big (usually a B1 failure in disguise); finishing in thirty seconds and asking
  "but what would I actually do?" is too small or too general. As a rough proxy, that's
  roughly 250-2,200 body words — a proxy only; judge by the read-it-and-apply-it test,
  not the count.

## Group C — Tier fit (required)

| Tier | Shape check |
|---|---|
| 1 — Reusable As-Is | One right answer, stated tightly. Full record completed. Strong Anti-Patterns. If you find variants creeping in, it's Tier 2. |
| 2 — Contextually Reusable | Variants + decision criteria in Guidance. More than 3–4 variants → two decisions hiding in one KU → split. Full record completed. |
| 3 — Field-Expert Annotation Only | The question, not the answer. Context + Field Qualification Questions thorough; everything else may be light or N/A. If the KU answers the question confidently, it's mis-tiered — likely Tier 2. |

## Group D — Record integrity (required; mostly automated)

Run `scripts/validate_ku.py` — it checks frontmatter fields, enums, dates, required
sections, bundle-path conformance, and size heuristics. On top of the validator, judge:

- **D1 Canonical sections carry weight.** Six required sections (Context, Guidance,
  TOGAF Impact, Well-Architected Impact, Consequences, Anti-Patterns) present in order;
  the five optional sections (Boundaries, Customer-Ecosystem Notes, Field Qualification
  Questions (Tier 3), Implementation Guidance, Operationalization Guidance) present only
  where they add something — omitting one entirely is a legitimate choice, not a gap. The
  validator enforces the shape; you judge the substance. Per-section content bar:
  - *Context*: establishes the architectural need first, not implementation detail.
  - *Boundaries* (if included): says where the guidance applies and doesn't — capability
    limits, ownership/maturity assumptions, sequencing, and pointers to the KU to use
    instead. Fine to omit if Context already makes the scope obvious.
  - *Guidance*: opens "Use **X** as …"; a clear recommendation, not marketing or tutorial.
  - *TOGAF / WA Impact*: each subsection concise, with the trade-off, and consistent with
    the YAML layers/pillars. A trailing TOGAF `### Security` subsection is fine only if
    `togaf_layers` lists Security and it genuinely cuts across the other four.
  - *Consequences*: negatives are real trade-offs, not generic warnings and not the
    positives restated in reverse. Free-form prose or bullets both work — no mandated
    positive/negative subsection split.
  - *Anti-Patterns*: required, never omitted; each names the risk and, ideally, gives a
    Preferred approach; topic-specific, not padded to a target count.
  - *Field Qualification Questions (Tier 3)* (if included): answerable in the field and
    tied to the Boundaries; the de facto main section for Tier 3, and should not be
    omitted there.
  - *Implementation Guidance* (if included): ordered; starts with scope/ownership/
    prerequisite validation, not tooling.
  - *Operationalization Guidance* (if included): covers ownership, cadence, lifecycle,
    change control, escalation, reassessment — how the pattern is *sustained*, not a
    deployment checklist.
  (Tier 3: light or "N/A — Tier 3" is fine for anything but Context and Field
  Qualification Questions (Tier 3); padded sections fail regardless of tier.)
- **D2 Honest provenance.** `source_basis` matches the actual origin; `originating_adrs`
  listed where the pattern came from engagements; `used_ai_to_solve_it` answered honestly;
  `confidence` defensible given the evidence.
- **D3 Environment precision.** `qlik_products` versions, `external_technologies`
  source/target versions, and `deployment` are specific enough that the next reader can
  tell whether their environment matches.
- **D4 Relationships correct.** `related` = read alongside; `alternatives` = same problem,
  different way (two KUs solving the same problem are alternatives, NOT duplicates — don't
  delete one); `migration_path` = ordered; supersession chain only via successor records.
- **D5 Review wiring.** `review_by` tied to product release cadence where possible;
  `owner` named; `peer_reviewers` named if status is Approved (Approved without a named
  peer reviewer is an automatic Fail).
- **D6 Naming standard.** ID matches `ADL-NNN` per `references/naming-standard.md`
  (validator enforces the letter sets); the file lives at
  `knowledge-units/<ID>/knowledge-unit.md` with the directory named for the ID, never the
  title. A KU still on the retired flat `<ID>-<title>.md` convention is a Fail for a new
  draft, and a Minor finding (with a migration recommendation) for an existing KU under
  review.

## The gate

- **PASS** — every criterion Pass, validator clean (warnings acceptable if explained in
  the quality report). Deliver.
- **FAIL** — any criterion Fail, or validator errors. Return to interrogation with
  questions targeted at the failing criteria only; revise; re-score. Maximum two revision
  rounds — after that, deliver with `status: Draft`, honest `confidence`, and the gap list.
  Do not loop forever and do not silently lower the bar.
- A **Weak** is not a Fail, but ≥3 Weaks in Group A = treat as Fail (the KU is mediocre
  everywhere, which is its own failure).

## Quality report format

```
## Quality Report — <KU id>: <title>
Gate: PASS | FAIL (round N) | DELIVERED AS DRAFT
Validator: clean | N warnings | N errors (summarize)
Fabric check: done — <findings> | unavailable — skipped

| Criterion | Score | Evidence |
|---|---|---|
| A1 Recurring decision | Pass | "..." |
...

Gaps / follow-ups: ...
Recommendation: ship as-is | ship with follow-ups | needs peer review by <who/what expertise> | split into: <titles>
```
