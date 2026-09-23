---
# ---- Identity ----
id:                               # PRODUCT-NNN, unique and never reused (check the registry/fabric for the next free number)
yaml_version: 4                   # schema version this record follows — do not change
title:                            # name the source, target, or scenario specifically (not "best practices for X")
status: Draft                     # Draft | Proposed | Approved | Deprecated | Superseded
tier:                             # 1 = Reusable As-Is | 2 = Contextually Reusable | 3 = Field-Expert Annotation Only
confidence:                       # High | Medium | Low — Low is legitimate; be honest

# ---- Classification ----
source_basis:                     # Field Experience | Customer ADRs | Product Documentation | Architecture Review
  -
togaf_layers:                     # Business | Data | Application | Technology | Security
  -
well_architected_pillars:         # Operational Excellence | Security | Reliability | Performance Efficiency | Cost Optimization | Sustainability
  -

# ---- Qlik products in scope ----
qlik_products:
  - product:
    versions:                     # e.g. ">= 2024.5" or "Not version-specific"

# ---- Customer environment ----
external_technologies:
  sources:
    - name:
      versions:
  targets:
    - name:
      versions:
  ecosystem:                      # adjacent tooling the pattern touches; null if none
deployment:
  environment:                    # on-premises | cloud | hybrid
  cloud_vendor:                   # AWS | Azure | GCP | null if on-premises
  containerized:                  # true | false
  container_platforms:            # null if not containerized

# ---- AI assistance used to produce this pattern ----
used_ai_to_solve_it:              # true | false — answer honestly
ai_solutions_used:                # null if none

# ---- Ownership and review ----
owner:                            # single person accountable for keeping this record current
contributors:
  -
peer_reviewers:                   # required before status can reach Approved
  -
created:                          # YYYY-MM-DD
last_reviewed:                    # YYYY-MM-DD
review_by:                        # YYYY-MM-DD — tie to the next relevant Qlik release where possible

# ---- Relationships ----
# Lifecycle: the supersession chain (append-only; never edit a published record in place)
supersedes:                       # record this one replaces; null if original
superseded_by:                    # record that replaces this one; null if current
# Other knowledge units
related:                          # peer KUs worth reading alongside this one; real IDs only
alternatives:                     # KUs that solve the same problem a different way; null if none
migration_path:                   # ordered KUs for moving to/from this pattern; null if none
# Provenance and assets
originating_adrs:                 # customer ADRs this pattern was distilled from; null if none
related_assets:                   # non-KU assets: blueprint, checklist, playbook, diagram

# ---- References ----
qlik_help_links:
  -
qlik_community_links:
  -

# ---- Tags ----
tags:
  -
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

<!-- The customer problem this addresses, in 3 to 6 sentences. Write it so another CSE/EA
reads it and says "yes, I have seen that" — describe the situation, what the customer is
trying to achieve, and what goes wrong without this pattern. Specific enough to be
recognizable in the field, general enough that it isn't one customer's quirks. Do not
restate the product manual here. -->



## Boundaries [optional]

<!-- One short paragraph: where this guidance applies and where it does not. Name the
applicable Qlik products, source/target platforms, prerequisites, and the situations where
someone should NOT use this pattern. Skip this section entirely if Context already makes
the scope obvious — an empty optional section is fine; a padded one is not. -->



## Guidance

<!-- The pattern: what to do. Every sentence should describe something the reader can DO.
Be specific, opinionated, and actionable — include configuration excerpts where relevant.
"It depends" is not guidance; "it depends on these signals, and here is what to do in each
case" is. Tier 1: one right answer, stated tightly. Tier 2: list the valid variants AND
the decision criterion for choosing each (more than 3-4 variants means two decisions are
hiding in one KU — split it). Settings/values that support the position belong here, not
in their own KU. This becomes a customer Decision when an EA cites it in an ADR. -->



## TOGAF Impact

<!-- A few sentences on how the guidance lands across the four layers: Business, Data,
Application, Technology (plus Security where it cuts across). Use the layers as the
structure. You are noting where the pattern touches each layer, not writing an
architecture chapter — if this section runs long, the KU is probably carrying more than
one decision. -->



## Well-Architected Impact

<!-- Map the guidance to the AWS Well-Architected pillars (Operational Excellence,
Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability). For
each pillar that matters, say what the pattern IMPROVES and what it COSTS — this is where
you explain why it is good architecture, not just how it works. Skip pillars that aren't
relevant. -->



## Consequences

<!-- The practical results of applying the pattern: what it makes possible, what it gives
up in exchange, what to watch out for, and what breaks if the pattern is ignored. Keep the
pillar-by-pillar trade-off analysis in Well-Architected Impact above; here, describe the
real-world outcomes. -->



## Anti-Patterns

<!-- One or two specific traps someone has ACTUALLY fallen into, named with specifics:
"customer enables logical replication on a transactional source database with no read
replica" is good; "performance issues" is not. Often the most valuable section of the KU.
Do not invent one — if you don't have a real trap, leave a marked gap. -->



## Customer-Ecosystem Notes [optional]

<!-- Only if the pattern interacts with the wider customer stack: the vendor lens
(SAP-specific, Snowflake-specific, Databricks-specific gotchas), source/target-specific
considerations, and integration handshakes with adjacent Qlik products. KUs listed in
'related' can be expanded on here. Leave empty if not applicable. -->



## Field Qualification Questions (Tier 3) [optional]

<!-- The situational questions a CSE or EA should ask the customer BEFORE applying this
pattern — the judgment calls the library cannot answer, captured so the next person asks
the same questions you would. Example: "Has the customer mandated a specific cloud region
for SOC 2 reasons?" For a Tier 3 KU this is the main section and must be thorough. For
Tier 1/2 it is where you park the questions that still need a human. -->



## Implementation Guidance [optional]

<!-- Enough practical direction to avoid the common mistakes when applying the pattern —
order of operations, settings that interact, validation steps. Not a full implementation
manual; if help.qlik.com covers the step-by-step, link it in qlik_help_links instead. -->



## Operationalization Guidance [optional]

<!-- What must be in place AFTER the pattern is applied so it can run and be supported in
production: monitoring, alerting, ownership, runbooks, escalation paths. The difference
between a pattern that works in the engagement and one that survives it. -->

