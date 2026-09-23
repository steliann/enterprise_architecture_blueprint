# Authoring Architecture Decision Records: A Companion Guide

A quick reference to keep open when you write an ADR. Pairs with the ADR template, ADR schema, ADR validation script, and Copilot ADR prompts in this repository. It answers the questions that come up the first few times you try to turn architecture discussion into a proper decision record.

**A note on vocabulary.** A Knowledge Unit captures reusable **guidance**. An Architecture Decision Record captures a specific **decision**. Guidance says what pattern should normally be used. A decision says what was selected in a specific customer, program, product, platform, or enterprise context. An ADR may cite one or more KUs, but it is not itself a KU.

When you read "guidance," think "what the architecture library recommends."
When you read "decision," think "what was selected here, why it was selected, what alternatives were rejected, and when the decision must be reviewed."

---

## What makes an ADR good

A good ADR meets all seven of these. If any one is missing, the ADR is not ready for governance.

1. **It records one clear architecture decision.** Not a discussion. Not a recommendation. Not an implementation plan. A reader should be able to point to one sentence and say, "this is what we decided."

2. **It explains why the decision was needed.** The Context section should make the decision necessary. If the context does not show why a choice had to be made, the ADR will read like documentation rather than a decision record.

3. **It compares realistic options.** The ADR must show what alternatives were considered and why they were accepted, rejected, deferred, or made conditional. A weak ADR only documents the chosen option. A strong ADR explains why the other options were not selected.

4. **It makes the selected option explicit.** The Decision Outcome section must state the selected option clearly. The reader should not need to infer it from the narrative.

5. **It captures consequences and trade-offs.** Every architecture decision buys something and gives something up. If the ADR only contains benefits, it is not ready.

6. **It is operationally credible.** The decision must describe what has to be owned, monitored, governed, reviewed, or supported after implementation. Architecture does not end when the product is configured.

7. **It is reviewable later.** The Review Triggers section should tell a future architect exactly when the decision may no longer be valid.

---

## How much information is enough

A target shape, section by section. The order matches the ADR template.

* **Context.** Two to four paragraphs. Explain the customer, program, product, platform, or enterprise situation. Describe the architecture problem and why a decision is required. Do not start with the chosen product or implementation detail.

* **Decision.** One clear paragraph. The first sentence starts with "We will". This is the actual decision, not the rationale and not the option comparison.

* **Decision Drivers.** Five to eight bullets. These are the reasons the decision exists: business drivers, technical constraints, governance needs, operational needs, security needs, delivery constraints, cost pressure, lifecycle concerns, or platform strategy.

* **Options Considered.** At least two realistic options. Each option gets benefits, limitations, and a fit assessment. The rejected options must not be strawman options. They should be options a reasonable architect might have considered.

* **Decision Outcome.** One to three paragraphs. State the selected option and explain why it best satisfies the decision drivers. Include assumptions, dependencies, sequencing requirements, or conditions that must remain true.

* **Knowledge Unit Alignment.** Optional, but required when KUs materially support, constrain, or contradict the ADR. If the ADR is aligned with existing KUs, link them. If it goes against a KU, be explicit and explain whether this is an exception, a reason to revise the ADR, or a reason to review the KU.

* **Architecture Impact.** Required. Use Business, Data, Application, and Technology as the structure. Keep each subsection short. You are explaining where the decision lands, not writing a full architecture chapter.

* **Consequences.** Required. Split into positive consequences and negative consequences / trade-offs. Be concrete. "Improved governance" is weak. "Creates one governed quality baseline visible through the catalog before operational remediation is built" is stronger.

* **Implementation Implications.** Required — six to ten bullets. These are architecture-oriented implementation implications: prerequisites, sequencing, ownership, integration dependencies, testing, rollout, migration, and change control. Not a low-level tutorial.

* **Operational Implications.** Required — five to eight bullets. Explain what must be sustained: monitoring, support ownership, alerting, access control, lifecycle management, incident handling, documentation, review cadence.

  > These two sections are required on every ADR, at every status, not optional extras. If a decision genuinely has nothing to say under either one, that is usually a sign the decision is too small to be an ADR at all — see "How small is too small" below — rather than a reason to skip the section.

* **Risks and Mitigations.** Four to eight bullets. Use the form `Risk: ... Mitigation: ...`. Risks should be specific to the decision.

* **Review Triggers.** Five to eight bullets. These are the conditions that may invalidate or materially change the decision: product changes, strategy changes, security policy changes, scale changes, cost model changes, operating model changes, or new enterprise standards.

* **Open Questions.** Use this when something material is unresolved. Do not use open questions to hide an unclear decision. If the open question could change the selected option, the ADR is probably not ready for approval.

**Rule of thumb on total size.** A peer should be able to read an ADR in three to five minutes and understand the decision, the alternatives, the trade-offs, and the review conditions. If they need fifteen minutes, the ADR is probably carrying multiple decisions. If they finish in thirty seconds and still ask "why did we choose this?", it is too thin.

---

## How big is too big

The clearest test: **the decision seam**.

Ask yourself one question: if the selected option changed, would the whole ADR need to change?

If no, the ADR probably contains more than one decision.

An ADR should record one primary decision. It may mention related implementation implications, but it should not bundle independent decisions into the same artifact.

Signs that an ADR is too big:

* The Decision section contains "and" between two independent choices.
* The Options Considered section compares different questions at the same time.
* Different owners would approve different parts of the decision.
* One part is strategic and another part is operational.
* One part is about product selection and another is about runtime topology.
* One part could be superseded without changing the rest.
* Different KUs would support different parts of the ADR.
* The review triggers apply to only one section of the ADR.

When you are unsure, split. Two short ADRs with clear relationships are easier to govern than one large ADR that hides multiple choices.

Example:

* Good single decision: "Use Snowflake as the operational data quality store."
* Separate decision: "Use Talend Studio to persist failed-row details into Snowflake."
* Separate decision: "Expose quality outcomes through Qlik Sense dashboards."
* Separate decision: "Use Qlik Cloud Catalog Trust Score as the initial quality baseline."

These decisions are related, but each can be reviewed, superseded, or challenged independently.

---

## How small is too small

This is the harder question. Use three tests together.

**Test 1: The real choice test.** Was there a meaningful choice to make? If there was only one possible path, you may have an implementation note, not an ADR.

**Test 2: The future audit test.** Would someone six months from now ask "why did we do it this way?" If yes, an ADR is useful. If no, the content may belong in implementation documentation.

**Test 3: The alternative test.** Can you name at least one realistic alternative? If no, the decision may be too small or not really a decision.

A small ADR is valid when the decision is narrow but important. For example, "Use OIDC with Okta for Qlik Cloud SSO" can be a valid ADR if the customer had multiple identity integration options and the choice has security, governance, and operational consequences.

A small ADR is weak when it records a setting without an architecture consequence. For example, "Set timeout to 60 seconds" is usually not an ADR unless it reflects a deliberate architecture decision around resilience, user experience, or platform limits.

---

## Should you start from a KU, an architecture discussion, or an existing project note?

Three useful approaches. Pick the one that matches the material you have.

### Starting from a Knowledge Unit

Use this when the decision applies existing reusable guidance to a specific context.

Start with the KU Guidance and Boundaries. Then ask:

* Does the customer or program context fit the KU boundaries?
* Is the ADR following the KU guidance directly?
* Is the ADR only conditionally aligned?
* Does the ADR violate an anti-pattern?
* Are there constraints from the KU that must become ADR risks, assumptions, or review triggers?

This is the cleanest path when the architecture library already contains relevant guidance.

### Starting from an architecture discussion

Use this when the decision came from a workshop, design review, customer meeting, or internal architecture conversation.

Start by extracting:

* the problem that required a decision;
* the options discussed;
* the selected option;
* the reason for selection;
* the known trade-offs;
* who owns the decision;
* what would cause the decision to be revisited.

Do not copy the meeting notes into the ADR. Convert the discussion into decision language.

### Starting from an existing project note

Use this when the material is buried in implementation documentation, a slide deck, a design document, or a delivery plan.

Start by finding the decision seam. Then separate:

* decision content;
* implementation implications;
* operational implications;
* project tasks;
* product tutorial steps;
* background information.

Only the decision content belongs in the ADR. Low-level implementation tasks belong elsewhere.

---

## Status guidance in one line each

The status tells the reader how much governance weight the ADR carries.

* **Draft.** Work in progress. The decision may still change. Use this while the ADR is being shaped.
* **Proposed.** Ready for review. The decision is clear, but not yet approved or accepted.
* **Accepted.** The decision is approved for the stated scope. Future changes should create a successor ADR or explicitly update the decision through governance.
* **Superseded.** Replaced by another ADR. The `superseded_by` field must point to the replacement.
* **Deprecated.** No longer recommended or no longer applicable, but not directly replaced by a successor ADR.

Use Draft for incomplete work. Use Proposed when the ADR is ready for architecture review. Use Accepted only when the decision has been approved through the relevant governance path.

---

## Filling in the metadata

Most metadata fields are descriptive, but these require judgment.

* **`id`.** Stable identifier. Use `ADR-001` for generic repository-level ADRs or a scoped format such as `SPX-ADR-002` when the ADR belongs to a customer, program, or workstream. Do not reuse IDs. If you can't check the registry for the next free sequence number right now, write the scoped prefix with `XXX` in place of the number (e.g. `SPX-ADR-XXX`) and flag it as an open question rather than guessing — a guessed number that collides with a real one is worse than a visible placeholder. Allocate the real number before the ADR is committed or accepted. Never put anything other than uppercase letters and digits in the prefix — see the naming standard.

* **`yaml_version`.** Leave it at the schema version the ADR template ships with. For the current ADR metadata model, use `yaml_version: 1`.

* **`title`.** Name the decision, not the topic. "Use Qlik Cloud Catalog for Initial Profiling" is better than "Data Quality Profiling."

* **`status`.** Use Draft, Proposed, Accepted, Superseded, or Deprecated. Do not mark an ADR Accepted until the decision has been reviewed and approved through the right governance path. `confidence: Low` is never valid alongside `status: Accepted`.

* **`date`.** The date the decision was recorded or made. Use ISO format.

* **`review_by`.** The next planned review date. Choose a date that makes sense for the decision: product release cycle, customer milestone, contract phase, platform migration, or architecture review cadence. Leave it null only when no review horizon applies — for a Proposed or Accepted ADR with no review date at all, expect a validator warning, since an undated review horizon is usually an oversight.

* **`decision_owner`.** The accountable owner of the decision. This is not always the author. Use a named person or role when possible. A bracketed placeholder such as `[Name / Role]` is not an acceptable final value — if the owner is genuinely not yet assigned, say so in words (for example, "Integration Architecture Lead — not yet assigned") and record it as an open question, rather than leaving a fill-in-the-blank token in the field.

* **`contributors`.** People who contributed materially to the decision, option assessment, constraints, or review.

* **`architecture_domain`.** The primary domain affected: Data, Application, Integration, Security, Platform, Operations, Governance, or Other. Choose the dominant domain, not every domain touched.

* **`decision_scope`.** The boundary of the decision: Customer, Product Platform, Program, Enterprise, or Reference Architecture. This prevents a customer-specific ADR from being mistaken for reusable guidance.

* **`decision_level`.** Strategic, Tactical, or Operational. A strategic ADR changes direction. A tactical ADR selects a pattern for a known use case. An operational ADR records a supportable operating choice.

* **`confidence`.** High, Medium, or Low. Low confidence is allowed for Draft or Proposed ADRs. Low confidence is not appropriate for Accepted ADRs.

* **`technology_scope`.** List only products and technologies materially involved in the decision. Do not list every technology in the customer environment. In YAML, `qlik`, `talend`, and `third_party` must be indented as children of `technology_scope` — if they sit flush-left with `technology_scope` itself, they parse as unrelated top-level fields instead, and the record fails validation.

* **`related_patterns`.** Link supporting KUs here. Use the KU ID, title, and relative path when available.

* **`related_adrs`.** Link other ADRs that should be read alongside this one. Do not use this for a dependency that should actually be a supersession relationship.

* **`impacted_architecture_views`.** List the architecture views affected by the decision: Governance View, Data Flow View, Operational View, Security View, Platform Deployment View, or other repository-specific views.

* **`related_assets`.** Link diagrams, design documents, playbooks, workshops, templates, or assessments that provide additional context.

* **`supersedes` and `superseded_by`.** Use these for lifecycle replacement. If this ADR replaces another ADR, set `supersedes`. If this ADR is replaced, set `superseded_by`.

* **`used_ai_to_prepare` and `ai_solutions_used`.** Record honestly whether AI helped prepare, review, or refine the ADR. This is provenance, not a weakness. The two fields travel together: if `used_ai_to_prepare` is `true`, `ai_solutions_used` must list at least one tool — it can't be left null. If `used_ai_to_prepare` is `false`, `ai_solutions_used` must be `null`, not an empty or leftover list.

* **`tags`.** Use lowercase hyphenated search terms. Prefer meaningful tags such as `data-quality`, `trust-score`, `snowflake`, `cdc`, `governance`, `matching`, `stewardship`, or `operational-store`.

---

## YAML mechanics that break the file, not just the style

These are parsing failures, not preferences. Get them wrong and the ADR either fails to load or loads with the wrong structure silently.

* **Use `-` for every list bullet in YAML front matter, never `*`.** A leading `*` at the start of a line is a YAML alias reference, not a bullet — the file will fail to parse, and the error will point somewhere unhelpful several lines later.
* **Indent `qlik`, `talend`, and `third_party` under `technology_scope`.** If they're flush-left with `technology_scope:` itself, they become sibling top-level keys, `technology_scope` parses as empty, and no validator error will make the cause obvious unless you're checking for it specifically.
* **Keep sibling keys at the same indentation.** A key indented two spaces more than its neighbors reads as a continuation of whatever came before it, not a new field.
* **Quote any string containing a colon, slash, bracket, or other YAML-significant punctuation.**

If in doubt, parse the front matter with a YAML library before trusting it by eye — a file that "looks right" in an editor can still parse into the wrong shape.

---

## Linking ADRs to Knowledge Units

ADRs should use KUs as architecture evidence, but they should not blindly cite them.

Before linking a KU, check four things:

1. **Does the ADR fit the KU boundaries?**
2. **Does the ADR follow the KU guidance?**
3. **Does the ADR avoid the KU anti-patterns?**
4. **Do the ADR consequences reflect the KU trade-offs?**

Use these classifications.

### Supported

The KU supports the ADR when the ADR follows the KU guidance and fits the KU boundaries.

In this case, add the KU to `related_patterns`.

### Conditionally supported

The KU supports the ADR only if certain conditions hold.

In this case, add the KU to `related_patterns`, but also add the condition to Decision Outcome, Implementation Implications, Operational Implications, Risks, Review Triggers, or Open Questions.

### Constrained

The KU narrows how the ADR should be implemented or governed.

In this case, link the KU and make the constraint explicit. Do not hide constraints in metadata.

### Contradicted

The ADR goes against the KU.

In this case, do not present the KU as a supporting pattern. Add a `## Knowledge Unit Alignment` section after Decision Outcome and explain the contradiction. State whether the ADR is an exception, whether the ADR should be revised, whether the KU is outdated, or whether governance needs to resolve the conflict.

---

## Common objections, answered

Short and direct. Use these when you meet resistance, including from yourself.

* **"This is obvious."** Maybe now. In six months someone will ask why the other option was not chosen. Obvious decisions still need a record when they have architecture consequences.

* **"We already have this in a slide deck."** A slide deck explains or sells the direction. An ADR records the decision, the options, the trade-offs, and the review triggers. Link the deck as a related asset.

* **"We do not know everything yet."** That is normal. Record assumptions and open questions. If the unknowns could change the selected option, keep the ADR in Draft or Proposed.

* **"This is just implementation detail."** Then it may not be an ADR. Ask whether there was a real architecture choice, a meaningful alternative, or future audit value. If not, move it to implementation documentation.

* **"There are no alternatives."** Usually there are. "Do nothing," "use the existing platform," "build custom," "use Qlik-native capability," "use third-party capability," and "defer the decision" are often valid options. If none are realistic, explain why.

* **"The decision may change."** That is why the ADR has Review Triggers, Supersedes, and Superseded By. Architecture records are allowed to evolve. Silent changes are the risk.

* **"This contradicts a KU."** Then the ADR needs an explicit exception or the KU needs review. Do not hide the contradiction. Governance value comes from making the conflict visible.

* **"AI helped write this."** Record it in the metadata. The decision still needs human ownership and architecture review.

---

## Ready-to-write checklist

Before you open the ADR template, you should be able to answer yes to all seven.

* I can state the decision in one sentence starting with "We will".
* I can explain why the decision is needed.
* I can name at least two realistic options.
* I can explain why the selected option is preferred.
* I can name at least one real trade-off.
* I know who owns the decision.
* I know what would cause the decision to be reviewed.

If you cannot say yes to these, do not force the ADR to Accepted. Write it as Draft or Proposed, capture the open questions, and ask for architecture review.

---

## Red flags during review

Watch for these during peer review or Copilot validation.

* The Decision section does not start with "We will".
* The ADR contains more than one primary decision.
* The selected option is not explicitly stated.
* The options are weak or unrealistic.
* The rejected options are strawmen.
* The consequences are all positive.
* The trade-offs are generic.
* The ADR reads like a product tutorial.
* The ADR reads like a project plan.
* The ADR duplicates a KU instead of citing it.
* The ADR contradicts a KU but does not explain the exception.
* The ADR has no review triggers.
* The ADR has open questions that could invalidate the selected option.
* The ADR claims product capabilities that have not been validated.
* `status: Accepted` is set without a governance path having actually been followed.

If two or more of these are true, the ADR needs revision before approval.

---

## Tooling: repository support for ADRs

This repository supports ADR authoring through four tooling layers.

1. **ADR template or snippet.** Use this to create a new Markdown ADR with YAML front matter and the required sections. Start from the blank template, not from a filled-in sample — copying a sample risks carrying over its example content by accident.

2. **ADR JSON schema.** Use this to validate the YAML metadata model, including ID format, lifecycle status, technology scope, relationships, AI provenance, and supersession rules.

3. **ADR validation script.** Use this to validate the Markdown file, front matter, required sections, subsection structure, decision quality rules, lifecycle consistency, and basic KU alignment rules. Run it before treating any draft as reviewable — a file that "looks right" in an editor can still fail validation on YAML nesting or bullet syntax alone.

4. **Copilot prompts.** Use the create, refresh, validate, and KU-alignment prompts to produce consistent ADRs from VS Code.

The tools help with structure and consistency. They do not replace architecture judgment. A valid ADR can still be a poor decision. A good peer review checks both.

---

## When to ask the workstream for help

Use the workstream or architecture review channel when any of these are true.

* You cannot identify the selected option.
* You cannot decide whether the content is a KU or an ADR.
* You cannot decide whether one ADR should be split into several ADRs.
* You cannot decide whether the ADR contradicts a KU or represents a valid exception.
* You cannot decide whether an existing KU is outdated.
* You cannot identify the decision owner.
* The open questions could change the selected option.
* The ADR has strategic impact beyond the stated scope.
* The decision depends on uncertain product capability.
* The customer-specific decision may need to become reusable guidance later.

Do not wait until the weekly session for these. The longer an unclear decision sits in the repository, the more likely it is to be reused incorrectly.

---

## Changelog

**Revision 2**

* Marked Implementation Implications and Operational Implications as required, not optional, and added a note explaining why a decision with nothing to say under either section is usually too small to be an ADR. This resolves a contradiction in the blank template, which had labeled the same two sections "(OPTIONAL)" in their headers while this guide's own size guidance always treated them as required.
* Added a new "YAML mechanics that break the file, not just the style" section, covering the `-` vs `*` bullet issue and the `technology_scope` indentation issue found in both the sample and blank templates in the field. These are hard parsing failures, not style preferences, and are now called out on their own rather than left implicit.
* Tightened the `id` guidance to describe the `XXX` placeholder convention for when the registry can't be checked, matching what the validation script already accepts.
* Tightened the `decision_owner` guidance to rule out bracketed placeholder text such as `[Name / Role]` as a final value, since the validation script treats it as an unfilled placeholder and rejects it.
* Made the `used_ai_to_prepare` / `ai_solutions_used` pairing rule explicit (each field's allowed value depends on the other), since the validation script enforces this strictly and the previous wording only implied it.
* Added a reminder in the tooling section to start new ADRs from the blank template, not by copying a filled-in sample.
