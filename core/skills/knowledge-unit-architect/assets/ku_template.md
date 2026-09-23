---
# ---- Identity ----
id: MCA-001                       # ADL-NNN per references/naming-standard.md: Architecture
                                   # area + Deployment scope + highest TOGAF Layer, then a
                                   # sequence number scoped to that exact 3-letter prefix.
                                   # MCA = Data Movement (M) + Cloud (C) + Application (A).
                                   # Never derive the ID from a product name. Never reused.
yaml_version: 4                   # schema version this record follows
title: Replicate CDC Task Design for SAP HANA to Snowflake
status: Proposed                  # Draft | Proposed | Approved | Deprecated | Superseded
tier: 1                           # 1 = Reusable As-Is | 2 = Contextually Reusable | 3 = Field-Expert Annotation Only
confidence: High                  # High | Medium | Low

# ---- Classification ----
source_basis:                     # where this pattern came from
  - Field Experience              # Field Experience | Customer ADRs | Product Documentation | Architecture Review
togaf_layers:                     # Business | Data | Application | Technology | Security
  - Business                      # (Security may appear here even though it is never the
  - Data                          #  ID's 3rd letter, which is limited to B/A/D/T)
  - Application
  - Technology
well_architected_pillars:         # AWS Well-Architected pillars
  - Reliability
  - Performance Efficiency

# ---- Qlik products in scope ----
qlik_products:
  - product: Qlik Replicate
    versions: ">= 2024.5"
  - product: Qlik Sense
    versions: "Not version-specific"

# ---- Customer environment ----
external_technologies:
  sources:
    - name: SAP HANA
      versions: ">= 2.0 SP05"
  targets:
    - name: Snowflake
      versions: any
  ecosystem:                      # adjacent tooling the pattern touches; null if none
    - Control-M
    - Microsoft Entra ID
deployment:
  environment: cloud              # on-premises | cloud | hybrid
  cloud_vendor: AWS               # AWS | Azure | GCP | null if on-premises
  containerized: true             # true | false
  container_platforms:            # null if not containerized
    - K8s
    - containerd

# ---- AI assistance used to produce this pattern ----
used_ai_to_solve_it: true
ai_solutions_used:                # null if none
  - Qlik Answers
  - Claude

# ---- Ownership and review ----
owner: "[Name / Role]"            # single person accountable for keeping this record current
contributors:                     # experts consulted who contributed to the pattern
  - "[Name / Role]"
peer_reviewers:                   # reviewed this record at least once before it reaches Approved
  - "[Name / Role]"
created: 2026-05-15
last_reviewed: 2026-05-15
review_by: 2026-11-15             # tie to the next relevant Qlik release where possible

# ---- Relationships ----
# Lifecycle: the supersession chain (append-only; never edit a record in place)
supersedes:                       # record this one replaces; null if original
superseded_by:                    # record that replaces this one; null if current
# Other knowledge units
related:                          # peer KUs worth reading alongside this one
  - REPL-001
  - QDA-012
alternatives:                     # KUs that solve the same problem a different way; null if none
  - REPL-020
migration_path:                   # ordered KUs describing how to move to or from this pattern; null if none
  - QTC-099
  - QTC-100
# Provenance and assets
originating_adrs:                 # customer ADRs this pattern was distilled from; null if none
  - ADR-000
related_assets:                   # non-KU assets: blueprint, checklist, playbook, diagram, assessment
  - "[Asset name or link]"

# ---- References ----
qlik_help_links:
  - https://help.qlik.com/...
qlik_community_links:
  - https://community.qlik.com/...

# ---- Tags ----
tags:
  - sap
  - hana
  - cdc
  - snowflake
  - financial-services
---

<!--
CANONICAL STRUCTURE (v4 body)
Eleven H2 sections below, in this exact order. Six are REQUIRED for every KU regardless
of tier: Context, Guidance, TOGAF Impact, Well-Architected Impact, Consequences,
Anti-Patterns. Five are OPTIONAL and may be omitted entirely when they don't add
anything: Boundaries, Customer-Ecosystem Notes, Field Qualification Questions (Tier 3),
Implementation Guidance, Operationalization Guidance. "Optional" is not the same as
"Tier 3 only" — a Tier 1 KU can validly omit Boundaries if Context already makes the
scope obvious. An empty optional section is fine; a padded one is not. Use ### only
where shown. Do not add extra top-level sections unless explicitly requested.

HOW COMPLETENESS VARIES BY TIER
  Tier 1 (Reusable As-Is): complete the full record, including whichever optional
    sections genuinely apply. This is the codified "of course" answer.
  Tier 2 (Contextually Reusable): same, and in Guidance list the valid variants with the
    decision criteria for choosing each.
  Tier 3 (Field-Expert Annotation Only): the answer is situational. Context and Field
    Qualification Questions (Tier 3) carry the record and should not be omitted. The
    other optional sections, and even Guidance/Consequences, may be light or marked
    "N/A — Tier 3" rather than filled in with padding.
-->

## Context
[3 to 5 paragraphs. P1: the recurring architecture problem or operating-model challenge —
specific enough that another CSE recognizes the situation. P2: what this pattern provides
and where it fits architecturally. P3: the purpose and the architectural outcome it enables.
P4 (if useful): what usually happens without this guidance. Do not start with
implementation details, and avoid restating the product manual.]

## Boundaries [optional]
[One short paragraph — or a short bullet list if that reads more clearly — saying where
this guidance applies and where it does not: applicable Qlik products, source/target
platforms, prerequisites, and the situations where someone should use a different KU
instead (name its ID where one exists). Skip this section entirely if Context already
makes the scope obvious.]

## Guidance
Use **[main product/capability/pattern]** as [the architecture role of the pattern].

[5 to 8 paragraphs total. Cover: the core architectural recommendation; how the pattern is
positioned; what it should not be confused with; the governance or operating-model
discipline required; connections to upstream/downstream KUs; the expected architecture
outcome. Specific, opinionated, actionable — include configuration excerpts where relevant.
Tier 2: list the valid variants with the decision criterion for choosing each. Bold only
the main product, capability, or key concept. This is reusable guidance at the KU layer; it
becomes a customer Decision when an EA instantiates it into an ADR.]

## TOGAF Impact
[A few sentences per layer — you are noting where the pattern touches each layer, not
writing an architecture chapter. If this section runs long, the KU is probably carrying
more than one decision (see the supersession-seam test).]

### Business
[Business, ownership, decision, governance, or operating-model impact.]

### Data
[Data architecture, metadata, quality, lineage, result-model, or lifecycle impact.]

### Application
[Application/component impact, product interactions, integration and orchestration
responsibilities.]

### Technology
[Platform, runtime, connectivity, security, performance, storage, or operational
infrastructure impact.]

### Security
<!-- Optional subsection: include only if togaf_layers lists Security and it cuts
across the other four layers beyond what's already covered above. Delete this
subsection entirely (heading and all) if not applicable. -->
[Where security materially cuts across the pattern beyond what's already covered above.]

## Well-Architected Impact
[One ### subsection per pillar listed in well_architected_pillars, in the same order.
Allowed headings: Reliability, Operational Excellence, Security, Performance Efficiency,
Cost Optimization, Sustainability. Each subsection: one concise paragraph with the positive
impact AND the main trade-off, design consideration, or operational responsibility.]

### [Pillar]
[...]

## Consequences
[What this approach makes possible; what it gives up in exchange; what to watch out for;
what breaks if the pattern is ignored. Keep the pillar-by-pillar trade-off analysis in
Well-Architected Impact above — here, describe the practical, real-world outcomes. A
short list or a few paragraphs both work; do not force a positive/negative split if the
consequences read better woven together.]

## Anti-Patterns
[One or two specific traps someone has actually fallen into — this is often the most
valuable section of the KU. Name each with specifics: "customer enables logical
replication on a transactional source database with no read replica" is good;
"performance issues" is not. Never invent one — if there's no real trap yet, leave this
section as a marked gap rather than padding it. A KU with a genuinely wide failure
surface can list more than two, structured as below, but don't manufacture entries to
hit a count.]

### Anti-pattern 1 — [name]
Do not [behavior to avoid]. [Why it creates architectural, operational, governance,
quality, security, performance, or adoption risk.]

**Preferred approach**

- [preferred behavior]
- [preferred behavior]

## Customer-Ecosystem Notes [optional]
[Only if the pattern interacts with the wider customer stack: the vendor lens
(SAP-specific, Snowflake-specific, Databricks-specific gotchas), source/target-specific
considerations, and integration handshakes with adjacent Qlik products. KUs listed in
`related` can be expanded on here. Leave this section out entirely if not applicable.]

## Field Qualification Questions (Tier 3) [optional]
[The situational questions a CSE or EA should ask the customer before applying this
pattern — the judgment calls the library cannot answer, captured so the next person asks
the same questions you would. Example: "Has the customer mandated a specific cloud
region for SOC 2 reasons?" For a Tier 3 KU this is the main section and must be thorough;
for Tier 1/2 it's where you park the questions that still need a human — omit if there
are none.]

## Implementation Guidance [optional]
[Enough practical direction to avoid the common mistakes when applying the pattern —
order of operations, settings that interact, validation steps. Not a full implementation
manual; if help.qlik.com covers the step-by-step, link it in `qlik_help_links` instead.
Omit if the Guidance section already covers this.]

Recommended implementation sequence:

1. [Numbered steps, as many as genuinely needed. Start with validation of scope,
   ownership, prerequisites, and dependencies; then design, configuration,
   implementation, validation, rollout, and scale-out.]

## Operationalization Guidance [optional]
[What must be in place after the pattern is applied so it can run and be supported in
production: monitoring, alerting, ownership, runbooks, escalation paths — the difference
between a pattern that works in the engagement and one that survives it. Omit if there's
nothing beyond standard operations.]

Operational requirements:

1. [Numbered requirements, as many as genuinely needed — ownership, cadence, monitoring
   or review, lifecycle management, access/security where relevant, change control,
   escalation, periodic reassessment of the guidance.]
