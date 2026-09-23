---
# ---- Identity ----
id: REPL-003                      # PRODUCT-NNN, unique and never reused
yaml_version: 4                   # schema version this record follows
title: Replicate CDC Task Design for SAP HANA to Snowflake
status: Proposed                  # Draft | Proposed | Approved | Deprecated | Superseded
tier: 1                           # 1 = Reusable As-Is | 2 = Contextually Reusable | 3 = Field-Expert Annotation Only
confidence: High                  # High | Medium | Low

# ---- Classification ----
source_basis:                     # where this pattern came from
  - Field Experience              # Field Experience | Customer ADRs | Product Documentation | Architecture Review
togaf_layers:
  - Business
  - Data
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
HOW COMPLETENESS VARIES BY TIER
  Tier 1 (Reusable As-Is): complete the full record. This is the codified "of course" answer.
  Tier 2 (Contextually Reusable): complete the full record, and in Guidance list the valid
    variants with the decision criteria for choosing each.
  Tier 3 (Field-Expert Annotation Only): the answer is situational. Capture Context and the
    Field Qualification Questions section thoroughly. The rest may be light or marked N/A.
Required sections for every record: Context, Guidance, TOGAF Impact, Well-Architected Impact,
Consequences, Anti-Patterns. All other sections are optional.
-->

## Context
[The customer problem this addresses. 3 to 6 sentences. Specific enough that another CSE
recognizes the situation when they encounter it. Avoid restating the product manual.]

## Boundaries [optional]
[Define when this guidance applies and when it does not. Include: applicable Qlik products,
applicable source and target platforms, prerequisites, and situations where this guidance
should not be used.]

## Guidance
[The pattern. What to do. Include configuration excerpts where relevant. Specific, opinionated,
actionable. For Tier 2 records, list the valid variants with the decision criteria for each.
This is reusable guidance at the KU layer. It becomes a customer Decision when an EA
instantiates it into an ADR.]

## TOGAF Impact
[Describe how the guidance affects the architecture across the business, data, application, and
technology layers. Use the TOGAF layers as the structure.]

## Well-Architected Impact
[Map the guidance to the AWS Well-Architected pillars. Explain why this is good architecture,
not only how it works technically. For each relevant pillar, describe the positive impact and
the trade-off.]

## Consequences
[What works as a result. What this enables. What it trades off (map the trade-offs to the
Well-Architected pillars where possible). What to watch for. What breaks if you ignore the
pattern.]

## Anti-Patterns
[What NOT to do, and why. Often the most valuable section. Include the common-mistake version
of this pattern that you have seen customers fall into.]

## Customer-Ecosystem Notes [optional]
[How this pattern interacts with the wider customer environment. The vendor lens.
Source-specific and target-specific gotchas (for example SAP-specific or Snowflake-specific
considerations), and integration handshakes with adjacent Qlik products. Records listed in
'related' can be expanded on here.]

## Field Qualification Questions (Tier 3) [optional]
[Questions a CSE or EA should ask the customer before applying this pattern. These are the
situational judgment calls the library cannot answer; it can only capture the question so the
next CSE knows what to think about. Example: "Has the customer mandated a specific cloud region
for SOC 2 compliance reasons?" or "Is the customer's data team comfortable owning the Replicate
task themselves, or do they need managed-service options?"]

## Implementation Guidance [optional]
[Practical guidance for applying the pattern. Not a full implementation manual, but enough
direction to avoid common mistakes.]

## Operationalization Guidance [optional]
[What must be operationalized after the pattern is applied, so the guidance can actually be run
and supported in production.]