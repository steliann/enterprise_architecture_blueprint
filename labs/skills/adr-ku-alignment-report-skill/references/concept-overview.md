# ADR–KU Alignment Report — Concept Overview

*For peer and leadership discussion*

## The initiative

Architecture decisions are usually created and reviewed one at a time. That gives us a record of individual choices, but it does not give the CSE / Enterprise Architect an account-level view of whether those decisions still make sense together, whether the reasons behind them still hold, or where attention is needed next.

The **ADR–KU Alignment Report** introduces that portfolio view.

For one customer at a time, it brings together the architecture decisions we know about, the current reusable architecture knowledge available to us, and the customer context collected through the engagement. The result is a focused view of the customer’s **architecture decision and governance posture** and a prioritized basis for the next architecture conversations.

It is deliberately narrower than an Architecture Blueprint. It does not attempt to describe or assess the customer’s complete architecture.

---

## Why this is needed

An ADR captures a decision at a point in time.

That decision may have been entirely reasonable when it was made, but the environment around it can change:

- a migration constraint disappears;
- a temporary exception remains in place longer than intended;
- a product capability or recommended pattern evolves;
- a safeguard is never implemented;
- a business requirement becomes more demanding;
- adoption exposes a new operational problem;
- a customer changes priorities;
- staffing or ownership changes;
- a new incident makes an old trade-off more important.

Looking only at the ADR does not tell us whether any of those things happened.

Looking only at current product knowledge does not tell us why the customer made the decision.

Looking only at account notes does not tell us whether the architecture decision itself is still sound.

The report becomes useful by bringing all three perspectives together.

---

## The knowledge it uses

The assessment is built from three complementary sources.

### Customer architecture decisions

ADRs tell us **what the customer decided, why it was decided, and what assumptions, constraints, trade-offs, or exceptions shaped that decision**.

The analysis can use the full ADR knowledge available for the account, including decisions that are outside Qlik/Talend technology when they help explain the customer architecture, dependencies, or constraints.

Not every known ADR needs to appear in the visible report. Decisions that are only contextual should inform the analysis without being forced into Qlik/Talend alignment or cluttering the report.

### Current reusable architecture knowledge

Knowledge Units tell us **what Qlik currently knows about the relevant architecture problem**.

They capture reusable patterns, product behaviour, boundaries, guardrails, trade-offs, anti-patterns, and operational expectations.

They also provide the mechanism through which changes on the Qlik side enter the assessment. When technology capabilities, limitations, or recommended patterns change, the relevant KU should evolve with them. The report therefore compares the customer decision with **current** KU guidance, not only with the guidance that existed when the ADR was written.

### Current customer context

Account and engagement information tells us **what is happening around the decision now**.

This can include customer objectives, program status, adoption, implementation progress, incidents, blockers, staffing, ownership, operational concerns, customer feedback, upcoming milestones, and other information collected by the CSE, CSM, SA, PS, or wider account team.

This context is essential because it helps us understand whether the assumptions behind a decision still hold and why a finding matters now.

It informs interpretation and priority; it does not replace architecture evidence.

---

## What the report should achieve

The report has two connected objectives.

First, it should help keep the customer’s architecture decisions **current, intentional, and governed**. It should make it easier to see which decisions remain well supported, which conditions or exceptions deserve review, where execution has not caught up with the decision, and where a pending decision deserves more challenge before it becomes part of the governing architecture.

Second, it should turn those findings into **useful customer-success action**. The CSE / Enterprise Architect should be able to use the report to determine which conversations matter most, what should be validated with the customer, where follow-through is required, and where a customer problem may justify additional adoption, expertise, or capability discussion.

The report is therefore not just an assessment of architecture decisions. It is a way to make architecture engagement **more focused, evidence-based, and continuous**.

---

## Value created

### For the customer

The report gives the customer a structured second look at important decisions without reopening the entire architecture.

It can help them:

- verify that decisions still reflect current requirements and constraints;
- close stale exceptions and overdue governance actions;
- distinguish a design decision from an implementation or operational problem;
- preserve the reasoning behind decisions as people and programs change;
- identify where a decision should be clarified before implementation;
- use current Qlik architecture knowledge in the context of their own environment;
- focus architecture discussions on the areas that matter now.

The customer-facing value is **better architecture decision governance and more relevant architecture conversations**, not a score of the customer architecture.

### For the CSE / Enterprise Architect

The report creates a repeatable way to turn distributed account knowledge into a prioritized architecture view.

It helps the CSE / EA:

- understand the decision portfolio faster;
- connect ADRs with current KUs and customer reality;
- decide what needs validation, governance, execution, or discovery;
- prepare focused customer workshops;
- create a follow-through plan that continues after the workshop;
- identify when other Qlik expertise should be involved;
- maintain continuity as the account evolves.

### For the account team

The report gives the wider account team a common technical basis for understanding:

- what matters in the customer’s decision portfolio;
- why it matters now;
- what is confirmed and what still needs validation;
- where architecture conditions may affect delivery or adoption;
- where a customer need may lead to a value-realization, expertise, or capability conversation;
- what should happen next.

This makes customer-success and commercial discussions better grounded in the customer’s own architecture reality.

---

## What it produces

The internal report should provide a concise portfolio view and make the important findings traceable back to the evidence.

Its practical outputs are:

- a view of the relevant current and proposed decisions;
- an understanding of how current reusable guidance relates to those decisions;
- the customer context that materially changes their interpretation or priority;
- the decisions or conditions that deserve attention;
- architecture topics that require further discovery;
- portfolio-level patterns and trajectory where the evidence supports them;
- a prioritized set of customer architecture conversations;
- enough evidence to generate a CSE / EA preparation and follow-through plan;
- a basis for a customer-facing architecture decision review.

The canonical report is internal. Customer-facing reports and workshop material are derived from it after removing internal account, commercial, and unvalidated contextual information.

---

## What this is not

The ADR–KU Alignment Report is not:

- a complete Architecture Blueprint;
- a score of overall architecture maturity;
- a customer health score;
- a product recommendation engine;
- an automatic way to rewrite customer ADRs;
- a mechanism for forcing every customer decision into Qlik/Talend guidance;
- a substitute for customer discovery or architecture governance.

The report can use broad account knowledge, but its conclusions must remain limited to what the available ADRs, current KUs, and customer context can support.

---

## How it fits into the initiative

The initiative has three complementary artifacts.

### Concept Overview

This document explains the **problem, proposed practice, expected value, and boundaries**. It is the entry point for peer and leadership discussion and can later be reused for onboarding.

### Purpose and Operating Model

The Operating Model is the **authoritative methodology**. It defines scope, evidence rules, ADR relevance, KU currency, alignment treatment, finding types, risks, opportunities, report lifecycle, and required outcomes.

If there is ever a difference between this Concept Overview and the Operating Model, the Operating Model takes precedence.

### Reference Examples

The synthetic ACME and Northstar reports show **what the methodology looks like when applied to realistic account information**.

They allow reviewers to judge whether the report produces useful, credible architecture conversations rather than only agreeing with the concept in the abstract.

Together, the package answers three questions:

> **Is this a useful practice?**

> **Do we agree with the methodology that governs it?**

> **Does the methodology produce the kind of account insight we want?**

---

## Feedback we need

The Concept Overview is intended to support discussion around the initiative rather than detailed methodology review.

The most useful feedback is:

- Does this solve a real problem in how we currently manage customer architecture decisions?
- Is the value to the customer, CSE / EA, and account team clear?
- Are ADRs, KUs, and customer context the right evidence combination?
- Is the boundary with a full Architecture Blueprint clear enough?
- Does the resulting report create the right kind of customer conversation?
- Is there any important consumer or outcome missing before we pilot the approach?

Detailed questions about classifications, lifecycle, evidence rules, or report mechanics belong in the **Purpose and Operating Model**.
