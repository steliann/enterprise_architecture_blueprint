---
# ---- Identity ----
id:                               # ADR-NNN or SCOPE-ADR-NNN — unique, never reused. Use SCOPE-ADR-XXX if the sequence number can't be allocated yet.
yaml_version: 1                   # schema version this record follows — do not change
title:                            # name the decision specifically, not the topic
status: Draft                     # Draft | Proposed | Accepted | Deprecated | Superseded
date:                             # YYYY-MM-DD — date the decision was recorded or made
review_by:                        # YYYY-MM-DD — tied to a real cycle or milestone; null if not applicable

# ---- Ownership ----
decision_owner:                   # single person or role accountable for the decision — not necessarily the author
contributors:                     # people who contributed to the decision, options, or review; null if none
  - ""

# ---- Classification ----
decision_type: "Architecture"     # keep as Architecture
architecture_domain:              # Data | Application | Integration | Security | Platform | Operations | Governance | Other — dominant domain only
decision_scope:                   # Customer | Product Platform | Program | Enterprise | Reference Architecture
decision_level:                   # Strategic | Tactical | Operational
confidence:                       # High | Medium | Low — Low is legitimate for Draft/Proposed, not for Accepted

# ---- Technology scope ----
# Only what is materially involved in the decision. Not an inventory of the whole estate.
technology_scope:
  qlik:                           # Qlik products directly involved in the decision; null if none
    - ""
  talend:                         # Talend products directly involved in the decision; null if none
    - ""
  third_party:                    # external technologies directly involved; null if none
    - ""

# ---- Relationships ----
# Real IDs only. Never invent one. If unverified, use null and log it under Open Questions.
related_patterns:                 # supporting KUs or reusable patterns; use real IDs/links only, null if none
  - ""
related_adrs:                     # peer ADRs worth reading alongside this one; real IDs only, null if none
  - ""
impacted_architecture_views:      # e.g. Governance View | Data Flow View | Operational View | Security View | Platform Deployment View; null if none
  - ""
related_assets:                   # diagrams, playbooks, workshop notes, assessments, design documents; null if none
  - ""

# Lifecycle: the supersession chain
supersedes:                       # ADR this one replaces; null if original
superseded_by:                    # ADR that replaces this one; null if current — required when status is Superseded

# ---- AI assistance ----
used_ai_to_prepare:               # true | false — answer honestly, this is provenance, not a weakness
ai_solutions_used:                # list if used_ai_to_prepare is true; must be null if used_ai_to_prepare is false
  - ""

# ---- Tags ----
tags:                              # lowercase, hyphenated, meaningful search terms
  - ""
---

<!--
YAML RULES THAT ACTUALLY BREAK FILES

  Use "-" for every list bullet, never "*". A leading "*" is a YAML alias marker, not a
  bullet, and the file will fail to parse.
  Keep qlik / talend / third_party indented two spaces under technology_scope. If they are
  flush-left with technology_scope itself, they become separate top-level keys instead of
  its children, and technology_scope parses as empty.
  Use null for a field with nothing to say. Delete the placeholder "" entries you do not fill,
  or replace the whole list with null.
  Quote any string value containing a colon, slash, bracket, or other punctuation.

HOW COMPLETENESS VARIES BY STATUS

  Draft:
    Use when the decision is still being shaped. It may contain open questions,
    incomplete option analysis, unresolved ownership, or unvalidated assumptions.

  Proposed:
    Use when the decision is clear and ready for architecture review, but not yet accepted.

  Accepted:
    Use only after the decision has been approved for the stated scope. The decision should be
    explicit, the selected option clear, trade-offs documented, and review triggers defined.
    Append-only from here — a material change creates a successor ADR, not an edit.

  Superseded:
    Use when another ADR replaces this one. The superseded_by field must point to the replacement ADR.

  Deprecated:
    Use when the decision is no longer recommended or no longer applicable, but has not been
    directly replaced by another ADR.

REQUIRED SECTIONS FOR EVERY ADR (no exceptions by status)
  Context, Decision, Decision Drivers, Options Considered, Decision Outcome,
  Architecture Impact, Consequences, Implementation Implications,
  Operational Implications, Risks and Mitigations, Review Triggers, Open Questions.

  Implementation Implications and Operational Implications are required, not optional, even
  though early drafts of this template labeled them otherwise. A decision with no implementation
  or operational footprint at all is probably not architecturally significant enough to be an ADR —
  see the "how small is too small" tests in the authoring guide.

OPTIONAL SECTION
  Knowledge Unit Alignment — include only when a KU materially supports, constrains, or
  contradicts this decision. Place it immediately after Decision Outcome. An empty section
  is worse than no section — delete it entirely if it doesn't apply.

An ADR records one specific architecture decision. It is not a Knowledge Unit, a project
note, an implementation guide, a product tutorial, a meeting summary, or sales positioning.
-->

# <ID> — <Title>

## Context

<!-- 2 to 4 paragraphs.

Describe the architecture situation, business or technical problem, customer/program context,
and why a decision is required. Start with the need for the decision, not the selected product
or an implementation detail. Explain what is at stake: governance, data flow, platform direction,
operating model, security, cost, delivery, scalability, supportability, or customer constraints.

A peer should finish this section understanding why leaving the direction ambiguous would create
architecture, delivery, operational, governance, or adoption risk. -->

## Decision

<!-- One paragraph. The first sentence must start with "We will".

State the selected architectural direction explicitly enough that another architect knows what
was chosen, what was excluded, and what architecture role the selection plays.

This is the decision, not the rationale. Do not survey the options here — that belongs in
Options Considered — and do not repeat Context. Rationale belongs in Decision Outcome. -->

## Decision Drivers

<!-- 5 to 8 bullets explaining why the decision was required.

Use specific business, architecture, operational, governance, security, delivery, cost,
lifecycle, platform, or adoption drivers. "Better performance" is not a driver unless you
name the architectural constraint that made performance decisive. -->

-

## Options Considered

<!-- At least two realistic options, no strawmen. The selected option must be one of them.
Rejection needs an architecture reason, not a preference. Deferral names the condition that
would make the option viable later. Duplicate the block below per option. -->

### Option 1 — [option name]

<!-- 1 to 2 paragraphs describing the option. -->

**Benefits**

-

**Limitations**

-

**Fit assessment**

<!-- Selected, rejected, deferred, or conditionally acceptable — and why. -->

### Option 2 — [option name]

<!-- 1 to 2 paragraphs describing the option. This must be a realistic alternative, not a strawman. -->

**Benefits**

-

**Limitations**

-

**Fit assessment**

<!-- Selected, rejected, deferred, or conditionally acceptable — and why. -->

<!-- Add a further "### Option 3 — [option name]" block, in the same shape, only if a third
realistic option genuinely exists. Remove this comment and any unused option block —
don't leave an empty Option 3 scaffold behind. -->

## Decision Outcome

Selected option: Option <N> — [selected option name].

<!-- 1 to 3 paragraphs on why this option best satisfies the decision drivers, plus the
conditions, assumptions, dependencies, and sequencing requirements that must hold for the
decision to remain valid. -->

## Knowledge Unit Alignment

<!-- OPTIONAL SECTION. Delete it entirely unless a KU materially supports, constrains, or
contradicts this decision. An empty section is worse than no section.

Before linking a KU, check: does the ADR fit the KU boundaries, does it follow the KU
guidance, does it avoid the KU's anti-patterns, and do the ADR's consequences reflect the
KU's trade-offs? An undisclosed contradiction with a KU is the worst governance failure an
ADR can commit. -->

### Supporting Knowledge Units

<!-- KU ID, title, and relative path, and what specifically it supports. -->

* [KU-ID — KU title](../knowledge-units/example-ku.md):

### Conditional Support and Constraints

<!-- Which KU, which condition or constraint, and where in this ADR it is handled
(Decision Outcome, Implementation Implications, Operational Implications, Risks, Review
Triggers, or Open Questions). -->

* [KU-ID — KU title](../knowledge-units/example-ku.md):

### Contradictions or Exceptions

<!-- Which KU, what the contradiction is, and whether this context justifies it as an
exception, whether the ADR should be revised, or whether the KU needs review. -->

* [KU-ID — KU title](../knowledge-units/example-ku.md):

### Alignment Outcome

<!-- One of: aligned | conditionally aligned | misaligned | requires a governance exception. -->

## Architecture Impact

<!-- One concise paragraph each. You are saying where the decision lands, not writing an
architecture chapter. -->

### Business

<!-- Ownership, process, adoption, funding, stakeholder, governance, or operating-model impact. -->

### Data

<!-- Data flow, metadata, quality, lineage, governance, retention, ownership, lifecycle. -->

### Application

<!-- Applications, Qlik/Talend components, integration points, APIs, orchestration,
deployment model, dependency boundaries, component responsibilities. -->

### Technology

<!-- Runtime, infrastructure, network, identity, security, connectivity, scalability,
resilience, observability, storage, platform operations. -->

## Consequences

<!-- Consequences are not only benefits. Every architecture decision creates trade-offs. -->

### Positive Consequences

<!-- 5 to 8 bullets. Be concrete. "Improved governance" is weak. -->

-

### Negative Consequences / Trade-offs

<!-- 5 to 8 bullets. Real trade-offs this decision creates — complexity, cost, ownership
burden, product dependency, sequencing risk, operational effort, performance limitation,
governance burden, migration constraint, future lock-in — not generic cautions about change.
An ADR with only positive consequences is not finished. -->

-

## Implementation Implications

<!-- 6 to 10 bullets. REQUIRED. Architecture-oriented: prerequisites, sequencing, ownership,
configuration boundaries, integration dependencies, testing, migration, rollout, change
control, validation activities. Not a product tutorial and not a task list. -->

-

## Operational Implications

<!-- 5 to 8 bullets. REQUIRED. What must be sustained after go-live: support ownership,
monitoring, alerting, lifecycle management, access control, incident handling, documentation,
runbooks, escalation, auditability, review cadence. -->

-

## Risks and Mitigations

<!-- 4 to 8 bullets, in exactly this form, specific to this decision:
- Risk: [risk]. Mitigation: [mitigation].
Avoid generic project risks unless they affect the architecture decision. -->

- Risk: . Mitigation: .

## Review Triggers

Review this ADR if:

<!-- 5 to 8 bullets. Concrete, observable conditions: a product capability shipping or being
withdrawn, a customer platform change, a new non-functional requirement, a security policy
change, a cost model change, an operating model change, a related KU being superseded, a new
enterprise standard. "If requirements change" is not a review trigger. -->

-

## Open Questions

<!-- 3 to 8 bullets of genuinely unresolved material points that affect implementation,
governance, operations, capability validation, or future review — or exactly:
No open questions at the time of this ADR.

Do not use this section to hide an unclear decision. If an open question could change the
selected option, keep the ADR in Draft or Proposed until it's resolved. -->

-
