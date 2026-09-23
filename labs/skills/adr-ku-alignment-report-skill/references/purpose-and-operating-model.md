# ADR–KU Alignment Report — Purpose and Operating Model

## 1. Purpose

The **ADR–KU Alignment Report** is a focused account-level architecture assessment used by the CSE / Enterprise Architect to review a customer’s current and proposed architecture decisions as a portfolio rather than as isolated records.

Architecture Decision Records capture **what the customer decided, why the decision was made, the constraints and trade-offs that shaped it, and the conditions under which it remains valid**. Knowledge Units provide **current reusable architecture knowledge** — patterns, boundaries, guardrails, anti-patterns, operational expectations, and field-proven decision guidance. Customer and account context adds the third perspective: **what has changed around those decisions since they were made**.

That context matters because an architecture decision is rarely wrong simply because time has passed. More often, the environment around it changes: a migration constraint disappears, a temporary exception becomes permanent, a safeguard is never implemented, a business requirement becomes more demanding, adoption stalls, a customer raises a new concern, an incident exposes a weakness, or the organization no longer has the capacity assumed by the original design.

The report combines these three evidence sources:

**customer decisions + current reusable guidance + current customer context**

The analysis should use the **full ADR knowledge available for the account** so that relevant dependencies, constraints, and architecture context are not lost. However, not every ADR belongs in the visible ADR–KU assessment. Some ADRs are useful only because they explain the customer environment around Qlik/Talend decisions.

The report therefore separates **knowledge considered** from **findings presented**. It should use contextual ADRs when they help explain or qualify an in-scope decision, but it should not force those ADRs into KU alignment, risk counts, or detailed report sections when Qlik/Talend guidance is not materially relevant.

The combined evidence is used to determine:

**which decisions remain sound, which deserve governance or execution follow-up, which may need to be reconsidered, what requires further discovery, and what customer conversation or action should come next.**

The report is intentionally narrower than a full Architecture Blueprint assessment. It does not attempt to reconstruct or score the complete customer architecture. Its subject is the **architecture decision portfolio and the customer context in which those decisions now operate**.

---

## 2. Objectives

The report serves two complementary purposes that must remain explicit and distinguishable.

### 2.1 Improve architecture decision quality and governance

The report should help keep the customer’s decision portfolio **current, intentional, and governed**.

It should identify:

- decisions that remain supported by current Knowledge Unit guidance;
- decisions whose original conditions, assumptions, or constraints may no longer hold;
- temporary exceptions that have become stale or persistent;
- overdue reviews or incomplete governance actions;
- decisions that remain architecturally sound but have unmet implementation or operational safeguards;
- Proposed ADRs that deserve challenge or clarification before becoming governing architecture;
- ADRs for which no suitable current KU exists;
- ADR references to KUs that have since been superseded;
- relevant architecture topics that appear absent from the supplied ADR portfolio and therefore require discovery.

The report does **not** replace customer architecture governance. It surfaces evidence and recommends review. Changes to the decision remain the responsibility of the ADR owner and the customer’s normal governance process.

### 2.2 Turn architecture evidence into customer-success action

The report should help the CSE / Enterprise Architect and account team decide **where attention is most useful and why**.

It should connect architecture findings with current customer context to identify:

- architecture, governance, delivery, operational, and adoption risks;
- customer concerns or changing requirements that should trigger architecture validation;
- situations where capabilities already owned could create more value;
- situations where Qlik expertise could help the customer progress;
- situations where an additional capability may be relevant after the customer need is validated;
- the architecture conversations that should be prioritized;
- the customer and Qlik stakeholders who should participate;
- the follow-through required after the customer discussion.

The report is therefore not only an assessment. It is a **decision-support instrument for ongoing customer engagement**.

---

## 3. Value Created

### 3.1 Value for the customer

The report gives the customer a structured way to revisit architecture decisions without reopening the entire architecture.

It can help the customer:

- preserve the reasoning behind important decisions;
- verify that decisions still match current needs and constraints;
- close stale exceptions and overdue reviews;
- distinguish a design problem from an execution problem;
- identify where a decision should be clarified before implementation;
- apply current field-proven guidance without treating that guidance as a substitute for customer context;
- maintain institutional memory when people, priorities, or programs change;
- focus architecture discussions on the decisions that matter now.

The customer-facing value is **better decision governance and more relevant architecture conversations**, not an architecture score.

### 3.2 Value for the CSE / Enterprise Architect

The report provides a repeatable method to convert a collection of ADRs, KUs, and engagement knowledge into a prioritized account architecture view.

It helps the CSE / EA:

- understand the customer’s architecture decision posture quickly;
- identify where customer context changes the meaning or priority of a decision;
- apply KUs in a disciplined, evidence-based way;
- distinguish decision, governance, execution, and discovery work;
- prepare targeted customer workshops;
- build an internal preparation and follow-through plan;
- identify where other Qlik roles or expertise may be useful;
- maintain continuity across successive customer engagements.

### 3.3 Value for the account team

The report gives the wider account team a technically grounded explanation of:

- what matters in the customer architecture decision portfolio;
- why it matters now;
- what is confirmed versus still a hypothesis;
- where risk exists and at what level;
- what customer need may justify an adoption, expertise, or capability conversation;
- what action should happen next.

This creates a common evidence base across CSE, EA, CSM, AE, SA, PS, Support, and other account participants without turning the architecture review into a commercial assessment.

---

## 4. Operating Principles

The following principles govern every ADR–KU Alignment Report.

### 4.1 The customer problem comes before the product opportunity

The report begins with customer decisions, customer outcomes, and customer context.

A product or commercial opportunity may emerge from the analysis, but only after a customer need has been identified and validated.

### 4.2 Customer context is a first-class evidence source

Customer and account context is not decorative background.

It is required to understand whether:

- an ADR assumption still holds;
- a temporary constraint has disappeared;
- an operational safeguard is actually working;
- a business requirement has changed;
- a delivery or staffing constraint is shaping architecture;
- an architecture finding is affecting adoption or customer outcomes;
- a technical issue is material enough to become an account risk.

Context does not replace ADR or KU evidence. It performs a different role: **it tells the report whether the decision is still operating in the environment for which it was made.**

### 4.3 Architecture evidence and contextual evidence must remain distinguishable

The report must show what supports a conclusion.

For example:

- ADR + KU evidence can support an architecture-alignment finding;
- account context can show that a condition has changed;
- customer notes can trigger a discovery question;
- relationship or renewal risk requires account evidence beyond the technical finding.

The report must not convert an unvalidated account observation into an architecture fact.

### 4.4 Accepted and Proposed ADRs are treated differently

Only **Accepted** and **Proposed** ADRs are in scope.

- **Accepted ADRs** represent governing architecture decisions.
- **Proposed ADRs** are assessed and clearly flagged, but are not treated as governing architecture.

Draft, Superseded, and Deprecated ADRs are excluded from the current portfolio assessment.

Historical records may be consulted only when needed to understand the rationale or evolution of an in-scope decision.

### 4.5 ADR knowledge is broader than the visible alignment portfolio

The report builder should consider the complete ADR knowledge available for the account, because decisions outside the Qlik/Talend technology scope may still explain important customer constraints, dependencies, or target-state choices.

Every Accepted or Proposed ADR considered by the analysis should therefore be classified by relevance:

- **Direct** — the ADR concerns Qlik/Talend technology or an architecture pattern for which Qlik has clear advisory ownership. It receives full ADR–KU assessment.
- **Adjacent** — the ADR primarily concerns another technology or architecture domain but materially constrains, integrates with, or changes the use of Qlik/Talend technology. The report assesses only the Qlik-relevant boundary, dependency, or implication.
- **Contextual** — the ADR is useful for understanding the customer architecture or the rationale behind another decision, but Qlik/Talend guidance is not materially applicable. It is used as context only.

Contextual ADRs must **not** be classified as `No KU Coverage`. They are outside the intended KU alignment scope.

Contextual ADRs should also not be included in alignment distributions, risk counts, or detailed finding sections unless they materially explain another reported finding. Where useful, they may be referenced briefly in Account Context, dependency analysis, or the rationale for a finding.

This allows the analysis to use the **entire decision knowledge available** without polluting the report with decisions that Qlik is not positioned to assess.

### 4.6 The report starts from the ADR but does not stop there

The ADR’s own relationships, rationale, conditions, and Declared Alignment are the starting point.

The report does not reconstruct the decision from first principles unless the evidence requires it. It revalidates the related KUs and tests whether the decision’s surrounding conditions still appear true.

### 4.7 KUs must be current

Every cited KU must be checked at report-generation time.

The report must verify:

- existence;
- lifecycle status;
- supersession / successor;
- current confidence or maturity where available;
- continued applicability of the relevant guidance.

If the KU has been superseded, successor guidance is used where possible and the ADR reference is flagged for governance review. The report does not silently edit the ADR.

### 4.8 Observed Alignment is advisory

The report may conclude that the current evidence suggests a different alignment from the one recorded in the ADR.

That **Observed Alignment** is an evidence-backed CSE / EA assessment. It is not an automatic ADR update.

The report must show both values and explain any difference.

### 4.9 Absence is not proof

- No ADR found does not automatically mean an architecture gap.
- No KU found does not automatically mean a poor decision.
- No evidence of a control does not automatically mean the control does not exist.

The appropriate response is discovery, not overstatement.

### 4.10 The report is time-bounded

The report represents a particular **evidence snapshot**.

ADRs change. KUs change. Customer objectives, adoption, staffing, incidents, milestones, and requirements change.

A report can therefore be valid and approved for its assessment date while still becoming obsolete later.

---

## 5. Evidence Model

The report uses three primary evidence pillars.

### 5.1 Architecture Decision Records — customer-specific decision evidence

ADRs provide the customer-specific architecture record.

Relevant fields may include:

- ADR status;
- decision and rationale;
- architecture domain, scope, and level;
- owner;
- decision date and review date;
- constraints and assumptions;
- options considered;
- consequences;
- operational implications;
- related ADRs;
- related KUs;
- Declared Alignment;
- governance exceptions;
- conditions and revisit triggers;
- open questions.

The ADR answers:

> **What did the customer decide, why, and under what conditions?**

The analysis should ingest all available ADR knowledge needed to understand the account, then apply the **Direct / Adjacent / Contextual** relevance classification before deciding how an ADR appears in the report.

- Direct ADRs become normal ADR–KU assessment subjects.
- Adjacent ADRs contribute only the part that materially affects the Qlik/Talend architecture.
- Contextual ADRs remain available as supporting knowledge but are normally omitted from the visible decision portfolio.

### 5.2 Knowledge Units — reusable architecture guidance

KUs provide current reusable knowledge that can support, constrain, or challenge the decision.

Relevant content may include:

- recommended patterns;
- applicability boundaries;
- qualification criteria;
- guardrails;
- anti-patterns;
- conditions;
- trade-offs;
- operational expectations;
- implementation considerations;
- confidence / maturity;
- validation history.

The KU answers:

> **What does current reusable architecture knowledge tell us about this type of decision?**

### 5.3 Customer and account context — current situational evidence

Customer context may come from structured account information and engagement evidence, including:

- current customer objectives and initiatives;
- program and migration status;
- product and capability adoption;
- customer concerns and stated priorities;
- incidents and recurring operational issues;
- implementation blockers;
- staffing or organizational constraints;
- governance or ownership challenges;
- delivery progress;
- milestones and commitments;
- customer workshop outcomes;
- CSE / CSM / SA / PS engagement notes;
- relationship signals;
- renewal context where relevant.

Customer context answers:

> **What has changed around the decision, and why does the decision matter now?**

Context should be assessed for reliability. The report should distinguish, where material, between:

- confirmed customer facts;
- credible account observations;
- working hypotheses requiring customer validation.

This distinction is particularly important when context changes the priority of a finding or supports Relationship / Renewal risk classification.

---

## 6. Analysis Model

### 6.1 Declared Alignment

Declared Alignment is the outcome recorded in the ADR.

Typical outcomes are:

- **Aligned**
- **Conditionally Aligned**
- **Misaligned**
- **Requires Governance Exception**
- **No KU Coverage**

Declared Alignment remains part of the customer’s ADR record.

### 6.2 Observed Alignment

Observed Alignment is the report’s current assessment based on:

**ADR evidence + current KU guidance + current customer context**

Observed Alignment asks whether the decision still appears to operate within the conditions represented by its Declared Alignment.

Examples:

- an ADR may remain Aligned because its design and assumptions still hold;
- a Conditionally Aligned decision may require review because the condition is no longer true;
- a temporary Governance Exception may have reached its end condition;
- a decision may remain sound while an agreed safeguard has not been executed;
- the KU may have been superseded while successor guidance continues to support the decision;
- a new customer requirement may make a previously reasonable decision worth revisiting.

When Observed Alignment differs from Declared Alignment, the report must:

1. show both values;
2. identify the evidence that caused the difference;
3. state what should be validated or reviewed;
4. leave the ADR unchanged.

---

## 7. Finding Types

Not every finding means that the architecture decision is wrong.

The report must distinguish the action required.

### 7.1 Decision revisit

The decision itself may need reconsideration because an assumption, constraint, requirement, or trade-off may no longer hold.

### 7.2 Governance follow-up

The decision may remain valid, but its governance is incomplete.

Examples include:

- overdue review;
- stale exception;
- unresolved ownership;
- missing closure;
- unaddressed open question.

### 7.3 Execution follow-up

The decision remains sound, but an agreed safeguard, test, operational practice, or implementation commitment has not been completed.

### 7.4 Proposed-decision review

A Proposed ADR contains material questions or exceptions that should be addressed before the decision becomes governing architecture.

### 7.5 KU coverage gap

A **Direct or materially Adjacent** ADR is within Qlik's legitimate architecture advisory scope, but no suitable current KU supports the decision.

This means additional validation may be appropriate. It does not mean the ADR is wrong, and the report does not automatically create a new KU.

A **Contextual ADR must never be classified as No KU Coverage** simply because no Qlik/Talend KU applies.

### 7.6 KU reference currency

The ADR cites guidance that is no longer current.

Successor guidance should be used where possible, and the ADR reference should be reviewed through normal governance.

### 7.7 Architecture whitespace / discovery flag

The customer context and known footprint suggest that an architecture topic may be relevant, but no ADR is present in the supplied portfolio.

This is a discovery prompt:

> **Is the decision documented elsewhere, genuinely undecided, or not relevant?**

It is not a confirmed architecture gap.

---

## 8. Risk Model

Architecture findings may create customer-success risks, but the report must classify risk carefully.

Risk categories are:

- **Architecture Risk** — a decision may not satisfy the required architecture qualities or future need.
- **Governance Risk** — decision ownership, review, exception, or accountability is inadequate.
- **Delivery Risk** — current constraints may prevent an intended outcome from being delivered.
- **Operational Risk** — resilience, performance, monitoring, security, recoverability, or operational controls may be inadequate.
- **Adoption Risk** — architecture or operating conditions may prevent successful use or expansion of the platform.
- **Relationship Risk** — the condition is credibly affecting customer confidence or the working relationship.
- **Renewal Risk** — there is credible account evidence that the condition may materially affect customer retention.

The first five may often be supported by architecture and contextual evidence together.

**Relationship and Renewal Risk require explicit supporting account context.** They must never be inferred automatically from a technical finding.

---

## 9. Opportunity Model

Opportunities must begin with a customer problem, desired outcome, or validated constraint.

The report may identify three types.

### 9.1 Adoption / value-realization opportunity

The customer already owns relevant capability but could use it more effectively or apply it to an additional validated need.

### 9.2 Expertise / engagement opportunity

The customer may benefit from additional CSE, EA, SA, PS, Support, enablement, or other Qlik expertise.

This does not automatically imply a paid engagement.

### 9.3 Capability / expansion opportunity

A validated customer need may require or materially benefit from capability the customer does not currently use or own.

The report should explain:

1. the customer problem;
2. the architecture or operational need;
3. why current capability may be insufficient;
4. what additional capability could contribute.

Commercial interpretation is a downstream account-team decision.

---

## 10. Portfolio-Level Analysis

The report is valuable because it looks beyond individual ADRs.

Where supported by the evidence, it should identify:

- dependencies between Direct, Adjacent, and Contextual ADRs;
- contextual customer decisions that materially explain or constrain a reported Qlik/Talend decision;
- common constraints affecting multiple decisions;
- recurring exceptions;
- repeated execution failures;
- concentration of issues in one architecture domain;
- temporary decisions becoming permanent;
- Proposed ADRs revealing an emerging operating-model pattern;
- customer context repeatedly influencing architecture choices;
- areas where adoption or delivery pressure is shaping design;
- changes in KU usage and governance quality over time.

### 10.1 Trajectory

Trajectory describes how the **architecture decision / governance practice** appears to be evolving.

It may show, for example:

- stronger use of KUs over time;
- improved closure of exceptions;
- increasing dependence on temporary workarounds;
- migration pressure being replaced by staffing pressure;
- better decision quality but weaker execution;
- greater architectural coherence but a weaker operating model.

Trajectory is not a score of the customer’s overall architecture maturity.

---

## 11. Required Report Outcomes

The report is not complete when it merely classifies ADRs.

It must produce actionable outcomes.

### 11.1 Portfolio understanding

The reader should understand:

- what Accepted **Direct and materially Adjacent** decisions currently govern the Qlik/Talend-relevant architecture;
- what Proposed Direct or materially Adjacent decisions are pending;
- how current KUs relate to them;
- which contextual customer decisions materially influence the interpretation of those decisions, without expanding the visible portfolio unnecessarily;
- what customer context materially changes their interpretation;
- where the strongest findings are.

### 11.2 Prioritized architecture conversations

The report should identify a small set of conversations worth having with the customer.

For each conversation, it should state:

- what should be discussed;
- why now;
- supporting ADR evidence;
- supporting KU evidence;
- supporting customer-context evidence;
- finding type;
- intended customer outcome;
- relevant customer and Qlik participants.

### 11.3 CSE / EA follow-through

The report should support an internal CSE / EA action cycle:

**Prepare → Validate → Workshop → Govern → Execute → Discover → Refresh**

The report itself does not need to contain the full action plan, but it must provide enough traceable evidence to generate that plan.

### 11.4 Customer-facing derivative

The report should support generation of a customer-facing architecture decision review.

The customer version should retain:

- validated decision and KU findings;
- factual governance and execution observations;
- constructive discovery questions;
- decision-review topics;
- agreed follow-up actions.

It should remove or reframe:

- internal commercial interpretation;
- relationship or renewal assessment;
- sensitive account notes;
- unvalidated hypotheses;
- internal ownership and account strategy.

---

## 12. Required Report Information — Flexible Presentation

The Operating Model defines **required information**, not a mandatory section order or presentation format.

Every report must contain:

- YAML report metadata and lifecycle;
- report purpose, scope, and evidence boundary;
- account / customer context relevant to the analysis;
- Accepted and Proposed **Direct / materially Adjacent** ADR inventory with status clearly visible;
- contextual ADR references only where they materially improve understanding of a reported decision, dependency, or finding;
- current KU-state validation;
- Declared and Observed Alignment;
- material findings and finding type;
- evidence supporting material conclusions;
- risk rollup where supported;
- opportunity rollup where supported;
- KU coverage gaps;
- KU currency findings;
- architecture whitespace / discovery flags where supported;
- portfolio / trajectory analysis where supported;
- prioritized customer conversations / CSE–EA engagement agenda;
- executive summary / rollup;
- customer-shareable derivative guidance.

Accepted and Proposed ADRs may be shown together for usability, but metrics and narrative must not present Proposed decisions as governing architecture.

Alignment distributions and other ADR–KU portfolio metrics must exclude **Contextual ADRs**. Adjacent ADRs should be included only where a genuine Qlik/Talend-relevant assessment has been made.

---

## 13. Report Lifecycle

Every ADR–KU Alignment Report is a governed, time-bounded artifact.

### 13.1 Lifecycle states

- **draft** — generated or being prepared; not yet reviewed.
- **proposed** — submitted for internal review as the candidate current assessment.
- **approved** — accepted internally as the current report for the stated evidence snapshot.
- **superseded** — replaced by a newer approved report and retained for history.

Approval means:

> **This report is accepted as the current assessment for this scope and evidence snapshot.**

It does not mean that the findings remain permanently current.

### 13.2 Minimum YAML front matter

```yaml
---
schema_version: "1.0"
report_id: "<ACCOUNT>-ADRKU-YYYY-NNN"
report_type: "adr-ku-alignment"
title: "ADR–KU Alignment Report — <Account>"
status: "draft" # draft | proposed | approved | superseded
version: "0.1"
classification: "internal"
customer_shareable_derivative: true

account:
  name: "<Account name>"
  account_id: "<optional internal account identifier>"

ownership:
  owner: "<CSE / EA>"
  reviewer: "<optional reviewer>"

dates:
  created_on: "YYYY-MM-DD"
  last_updated: "YYYY-MM-DD"
  assessment_as_of: "YYYY-MM-DD"
  review_by: "YYYY-MM-DD"

scope:
  included_adr_statuses:
    - accepted
    - proposed
  excluded_adr_statuses:
    - draft
    - superseded
    - deprecated
  program: "<optional program / domain scope>"

evidence_snapshot:
  accepted_adrs_assessed: 0
  proposed_adrs_assessed: 0
  contextual_adrs_considered: 0
  kus_checked_as_of: "YYYY-MM-DD"
  account_context_as_of: "YYYY-MM-DD"

lineage:
  supersedes: null
  superseded_by: null
---
```

### 13.3 Header rules

- `report_id` identifies one assessment instance.
- `version` changes while the same Draft / Proposed assessment is being refined.
- a materially new assessment with a new evidence snapshot should normally create a new `report_id`;
- the new approved report supersedes the previous approved report;
- `assessment_as_of` identifies the evidence cutoff;
- `kus_checked_as_of` records KU currency;
- `account_context_as_of` records the latest customer-context evidence intentionally considered;
- `accepted_adrs_assessed` and `proposed_adrs_assessed` count only ADRs that actually enter the Direct / materially Adjacent assessment portfolio;
- `contextual_adrs_considered` records that broader decision knowledge was used without treating those ADRs as KU-alignment subjects;
- the canonical report is `internal`;
- a customer-facing derivative should trace back to the approved internal report.

---

## 14. Internal and Customer-Facing Use

The canonical ADR–KU Alignment Report is internal because it combines architecture evidence with account context and customer-success interpretation.

Content should be classified according to how it may be used.

### Customer-shareable

Examples:

- ADR inventory and status;
- current KU guidance;
- validated alignment observations;
- overdue decision reviews;
- unmet execution commitments;
- decision-revisit questions;
- architecture discovery questions;
- agreed architecture actions.

### Internal

Examples:

- commercial interpretation;
- adoption opportunity classification;
- Relationship / Renewal risk assessment;
- sensitive customer or account-team notes;
- hypotheses that still require customer validation;
- internal account strategy;
- Qlik ownership and resourcing decisions.

Customer-facing material should be **derived from the approved internal report**, not maintained as an independent assessment.

---

## 15. Boundaries

The ADR–KU Alignment Report is not a full Architecture Blueprint review.

It does not systematically assess:

- all customer business objectives and use cases;
- all data products;
- all data flows;
- the complete technology landscape;
- every data-quality control;
- all operational capabilities;
- overall architecture completeness;
- overall requirements fitness;
- overall technology fitness.

Therefore:

- the report may use architecture decisions that do not appear in the visible ADR–KU portfolio when they are useful contextual knowledge;
- an ADR outside Qlik/Talend advisory scope should not be forced into KU alignment merely because it is known;
- absence of an ADR is not proof of an architecture gap;
- the report cannot claim the architecture is complete;
- the report cannot claim overall architecture maturity;
- a finding should not be generalized beyond the evidence in scope.

Where broader analysis is required, report findings can become inputs to an Architecture Blueprint or deeper architecture review.

---

## 16. Quality Criteria

A high-quality ADR–KU Alignment Report should be:

### Evidence-based
Every material conclusion can be traced to ADRs, KUs, customer context, or an explicit combination of them.

### Current
KUs and account context are intentionally refreshed for the assessment date.

### Bounded
The report is clear about what it can and cannot conclude.

### Actionable
Findings lead to specific validation, governance, execution, discovery, or customer-conversation actions.

### Customer-problem-led
Opportunities and recommendations start from a validated customer need.

### Governance-safe
The report never silently changes an ADR or substitutes itself for the customer’s decision process.

### Useful over time
The report can be refreshed and compared with earlier assessments to show decision / governance trajectory.

---

## 17. Core Principle

The ADR–KU Alignment Report exists because architecture decisions cannot be judged only by how they looked when they were written.

A decision must be understood in relation to:

**what the customer decided, what other customer decisions constrain or explain it, what current reusable knowledge says, and what is happening in the customer environment now.**

The analysis should use all relevant account knowledge, but the report should present only the subset that materially improves the Qlik/Talend architecture assessment.

The report turns those three perspectives into a focused portfolio view that helps the CSE / Enterprise Architect and the customer decide:

**what remains sound, what needs attention, what should be validated, and what should happen next.**
