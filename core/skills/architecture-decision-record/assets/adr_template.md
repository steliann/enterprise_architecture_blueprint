---
# ---- Identity ----
id:                               # ADR-NNN or SCOPE-ADR-NNN. Unique, never reused, never renumbered. Not quoted.
yaml_version: 1                   # schema version this record follows - do not change. Not quoted.
title: ""                          # name the decision, not the topic: "Use X for Y" - always quoted
status: Draft                     # Draft | Proposed | Accepted | Superseded | Deprecated. Not quoted.
date:                             # YYYY-MM-DD - when the decision was recorded or made. Not quoted.
review_by:                        # YYYY-MM-DD, tied to a real cycle or milestone; null if not applicable. Not quoted.

# ---- Ownership ----
decision_owner: ""                 # person or role accountable for the decision - always quoted
contributors:                     # people who contributed to the decision, options, or review; null if none
  - ""                            # each entry always quoted

# ---- Classification ----
decision_type: "Architecture"     # always "Architecture" - always quoted
architecture_domain:              # Data | Application | Integration | Security | Platform | Operations | Governance | Other - dominant domain only. Not quoted.
decision_scope:                   # Customer | Product Platform | Program | Enterprise | Reference Architecture. Not quoted.
decision_level:                   # Strategic | Tactical | Operational. Not quoted.
confidence:                       # High | Medium | Low - Low is legitimate for Draft/Proposed, never for Accepted. Not quoted.

# ---- Technology scope ----
# Only what is materially involved in the decision. Not an inventory of the estate.
# Every product/technology entry below is always quoted, even a bare name with no punctuation.
technology_scope:
  qlik:                           # Qlik products directly involved; null if none
    - ""
  talend:                         # Talend products directly involved; null if none
    - ""
  third_party:                    # external technologies directly involved; null if none
    - ""

# ---- Relationships ----
# Real IDs only. Never invent one. If unverified, use null and log it under Open Questions.
# Every entry below, and both supersedes/superseded_by, is always quoted.
related_patterns:                 # supporting KUs: "ID - Title (../knowledge-units/file.md)"; null if none
  - ""
related_adrs:                     # peer ADRs worth reading alongside this one; null if none
  - ""
impacted_architecture_views:      # Governance View | Data Flow View | Operational View | Security View | Platform Deployment View | ...
  - ""
related_assets:                   # diagrams, playbooks, design docs, workshop outputs, assessments; null if none
  - ""
supersedes: null                  # ADR this one replaces; null if original. Quoted when set, e.g. "SPX-ADR-002".
superseded_by: null               # ADR that replaces this one; null if current. Required when status is Superseded. Quoted when set.

# ---- AI assistance ----
used_ai_to_prepare:               # true | false - answer honestly, this is provenance
ai_solutions_used:                # list if used_ai_to_prepare is true; null if false
  - ""

# ---- Tags ----
tags:                             # lowercase, hyphenated, meaningful search terms - each entry always quoted
  - ""
---

<!--
YAML RULES THAT ACTUALLY BREAK FILES

  Use "-" for list bullets, never "*". A leading "*" is a YAML alias and the file will not parse.
  Keep qlik / talend / third_party indented under technology_scope, or they become top-level keys.
  Use null for empty fields. Delete the placeholder "" entries you do not fill.
  Quote any string containing a colon, slash, bracket, or other punctuation.

  ALWAYS QUOTE these fields, even when the value has no punctuation that would force it:
  title, decision_owner, decision_type, supersedes, superseded_by, and every non-null
  entry in contributors, technology_scope.qlik, technology_scope.talend,
  technology_scope.third_party, related_patterns, related_adrs,
  impacted_architecture_views, related_assets, and tags. validate_adr.py checks this
  against the raw YAML text and errors if any of them is unquoted.

COMPLETENESS BY STATUS

  Draft       Still being shaped. May carry open questions, incomplete option analysis,
              unresolved ownership, unvalidated assumptions.
  Proposed    Decision is clear and ready for architecture review, not yet approved.
  Accepted    Approved for the stated scope. Decision explicit, selected option clear,
              trade-offs documented, review triggers defined. Append-only from here.
  Superseded  Replaced by another ADR. superseded_by must point to the replacement.
  Deprecated  No longer recommended or applicable, with no direct replacement.

REQUIRED SECTIONS
  Context, Decision, Decision Drivers, Options Considered, Decision Outcome,
  Architecture Impact, Consequences, Implementation Implications,
  Operational Implications, Risks and Mitigations, Review Triggers, Open Questions.

OPTIONAL SECTION
  Knowledge Unit Alignment - include only when KUs materially support, constrain,
  or contradict the decision. Goes immediately after Decision Outcome.

An ADR records one specific architecture decision. It is not a Knowledge Unit, a project
note, an implementation guide, a product tutorial, a meeting summary, or sales positioning.
-->

# <ID> — <Title>

## Context

<!-- 2 to 4 paragraphs.

P1: the architecture situation, the business or technical problem, the customer or program
context, and why a decision is required.
P2: the architecture scope - systems, products, data flows, operating model, governance concern.
P3 (optional): the risk of not deciding, or of leaving the direction ambiguous.

Do not open with the selected product or an implementation detail. Establish the need first.
A peer should finish this section understanding why ambiguity here creates real risk. -->

## Decision

<!-- One paragraph. The first sentence must start with "We will".

State the selected direction explicitly enough that another architect knows what was chosen,
what was excluded, and what architecture role the selection plays.

This is the decision, not the rationale. Rationale goes in Decision Outcome. Do not survey
the options here and do not repeat Context. -->

## Decision Drivers

<!-- 5 to 8 bullets explaining why the decision was required.

Business, architecture, operational, governance, security, cost, delivery, lifecycle,
platform, or adoption drivers. "Better performance" is not a driver unless you name the
architectural constraint that made performance decisive. -->

-

## Options Considered

<!-- At least two realistic options, no strawmen. The selected option must be one of them.
Rejection needs an architecture reason, not a preference. Deferral names the condition that
would make the option viable later. Duplicate the block below per option. -->

### Option 1 — <name>

<!-- 1 to 2 paragraphs describing the option. -->

**Benefits**

-

**Limitations**

-

**Fit assessment**

<!-- Selected, rejected, deferred, or conditionally acceptable - and why. -->

### Option 2 — <name>

<!-- 1 to 2 paragraphs describing the option. -->

**Benefits**

-

**Limitations**

-

**Fit assessment**

<!-- Selected, rejected, deferred, or conditionally acceptable - and why. -->

## Decision Outcome

Selected option: Option <N> — <name>.

<!-- 1 to 3 paragraphs on why this option best satisfies the decision drivers, plus the
conditions, assumptions, dependencies, and sequencing requirements that must hold for the
decision to remain valid. -->

## Knowledge Unit Alignment

<!-- OPTIONAL SECTION. Delete it entirely unless a KU materially supports, constrains, or
contradicts this decision. An empty section is worse than no section.

An undisclosed contradiction with a KU is the worst governance failure an ADR can commit. -->

### Supporting Knowledge Units

<!-- KU ID and title, and what specifically it supports. -->

### Conditional Support and Constraints

<!-- Which KU, which condition or constraint, and where in this ADR it is handled. -->

### Contradictions or Exceptions

<!-- Which KU, what the contradiction is, and whether this context justifies it. -->

### Alignment Outcome

<!-- One of: aligned | conditionally aligned | misaligned | requires a governance exception. -->

## Architecture Impact

<!-- One concise paragraph each. You are saying where the decision lands, not writing an
architecture chapter. -->

### Business

<!-- Ownership, process, adoption, funding, stakeholder impact. -->

### Data

<!-- Data flow, metadata, quality, lineage, governance, retention, ownership, lifecycle. -->

### Application

<!-- Applications, Qlik/Talend components, integration points, APIs, orchestration,
deployment model, dependency boundaries. -->

### Technology

<!-- Runtime, infrastructure, network, identity, security, connectivity, scalability,
resilience, observability, platform operations. -->

## Consequences

### Positive Consequences

<!-- 5 to 8 bullets. Be concrete. "Improved governance" is weak. -->

-

### Negative Consequences / Trade-offs

<!-- 5 to 8 bullets. Real trade-offs this decision creates, not generic cautions about
change. An ADR with only positive consequences is not finished. -->

-

## Implementation Implications

<!-- 6 to 10 bullets. REQUIRED. Architecture-oriented: prerequisites, sequencing, ownership,
configuration boundaries, integration dependencies, testing, migration, rollout, change
control. Not a product tutorial and not a task list. -->

-

## Operational Implications

<!-- 5 to 8 bullets. REQUIRED. What must be sustained after go-live: support ownership,
monitoring, alerting, lifecycle management, access control, incident handling, documentation,
auditability, review cadence. -->

-

## Risks and Mitigations

<!-- 4 to 8 bullets, in exactly this form, specific to this decision:
- Risk: <risk>. Mitigation: <mitigation>. -->

- Risk: . Mitigation: .

## Review Triggers

Review this ADR if:

<!-- 5 to 8 bullets. Concrete, observable conditions: a product capability shipping or being
withdrawn, a customer platform change, a new non-functional requirement, a security policy
change, a cost model change, an operating model change, a strategic technology change.
"If requirements change" is not a review trigger. -->

-

## Open Questions

<!-- 3 to 8 bullets of genuinely unresolved material points, or exactly:
No open questions at the time of this ADR.

Do not use this section to hide an unclear decision. If an open question could change the
selected option, the ADR is not ready for Accepted. -->

-
