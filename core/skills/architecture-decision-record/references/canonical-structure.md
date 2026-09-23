# Canonical ADR structure

Authoritative section contract. `assets/adr_template.md` is the skeleton to build on; this file says what goes in each part and how much. `scripts/validate_adr.py` enforces the mechanical half.

## Frontmatter

YAML between `---` delimiters, in this exact field order and grouping. See `assets/adr_template.md` for the copy-ready version with inline guidance.

Field groups: Identity (`id`, `yaml_version`, `title`, `status`, `date`, `review_by`) · Ownership (`decision_owner`, `contributors`) · Classification (`decision_type`, `architecture_domain`, `decision_scope`, `decision_level`, `confidence`) · Technology scope (`technology_scope` with nested `qlik`, `talend`, `third_party`) · Relationships (`related_patterns`, `related_adrs`, `impacted_architecture_views`, `related_assets`, `supersedes`, `superseded_by`) · AI assistance (`used_ai_to_prepare`, `ai_solutions_used`) · Tags (`tags`).

### Enums

- `status`: Draft | Proposed | Accepted | Superseded | Deprecated
- `architecture_domain`: Data | Application | Integration | Security | Platform | Operations | Governance | Other — the **dominant** domain, not every domain touched
- `decision_scope`: Customer | Product Platform | Program | Enterprise | Reference Architecture
- `decision_level`: Strategic | Tactical | Operational
- `confidence`: High | Medium | Low
- `decision_type`: always `Architecture`
- `yaml_version`: always `1`

### YAML rules

- `null` for empty fields, never an empty string and never a placeholder left in.
- List fields use `-` bullets, correctly indented. **Never `*`** — YAML reads a leading `*` as an alias and the file won't parse.
- `technology_scope` nests two levels. Its three sub-keys must be indented under it, or they flatten into top-level keys and validation fails.
- Quote strings containing punctuation, slashes, brackets, or colons.
- **Always quote these, whether or not the value contains punctuation** — this is house style, not a parsing requirement, and `validate_adr.py` checks it against the raw text: `title`, `decision_owner`, `decision_type`, `supersedes`, `superseded_by`, and every non-null item in `contributors`, `technology_scope.qlik`, `technology_scope.talend`, `technology_scope.third_party`, `related_patterns`, `related_adrs`, `impacted_architecture_views`, `related_assets`, and `tags`.
- ISO dates. `review_by` must be later than `date`, or `null`.
- `used_ai_to_prepare: false` requires `ai_solutions_used: null`. `true` requires a non-empty list.
- `status: Superseded` requires `superseded_by`. Otherwise `superseded_by` is normally `null`.
- `status: Accepted` must not carry `confidence: Low`.
- No field may reference the ADR's own `id`.

### Judgment fields

- `review_by` — tie it to something real: a product release cycle, customer milestone, contract phase, platform migration, or the architecture review cadence. An arbitrary date is worse than `null`.
- `decision_owner` — the accountable owner, not necessarily the author.
- `confidence` — Low is legitimate for Draft and Proposed. It is not legitimate for Accepted.
- `technology_scope` — only what's materially involved in the decision. Not an inventory of the customer's estate.
- `impacted_architecture_views` — Governance View, Data Flow View, Operational View, Security View, Platform Deployment View, or repository-specific ones.
- `tags` — lowercase, hyphenated, meaningful: `data-quality`, `trust-score`, `snowflake`, `cdc`, `governance`, `matching`, `stewardship`, `operational-store`.

## Body

H1 then `##` sections in exactly this order. `###` for subsections. No extra top-level sections unless the user asks.

```
# <ID> — <Title>
## Context
## Decision
## Decision Drivers
## Options Considered
## Decision Outcome
## Knowledge Unit Alignment          (optional — see ku-alignment.md)
## Architecture Impact
## Consequences
## Implementation Implications
## Operational Implications
## Risks and Mitigations
## Review Triggers
## Open Questions
```

### Context — 2 to 4 paragraphs

Paragraph 1: the architecture situation, the business or technical problem, the customer or program context, and why a decision is required.

Paragraph 2: the architecture scope — systems, products, data flows, operating model, governance concern.

Paragraph 3, if useful: the risk of not deciding, or of leaving the direction ambiguous.

Do not open with the selected product or an implementation detail. Establish the need first. A peer should finish this section understanding why ambiguity here would create architecture, delivery, operational, governance, or adoption risk.

### Decision — one paragraph

First sentence starts with **"We will"**. Validator-enforced.

State the selected direction explicitly enough that another architect knows what was chosen, what was excluded, and what architecture role the selection plays. This section is the decision, not the rationale — rationale belongs in Decision Outcome. Don't survey the options here and don't repeat Context.

### Decision Drivers — 5 to 8 bullets

Why the decision was *required*. Business, architecture, operational, governance, security, cost, delivery, lifecycle, platform, or adoption drivers.

"Better performance" is not a driver. "Profiling must complete inside the overnight window or the stewardship queue starts a day behind" is.

### Options Considered — at least 2

One `###` subsection per option, headed exactly `### Option N — <name>`.

1 to 2 paragraphs describing the option, then:

```
**Benefits**

- ...

**Limitations**

- ...

**Fit assessment**

<Selected, rejected, deferred, or conditionally acceptable — and why.>
```

The selected option must be one of them. No strawmen. Rejection needs an architecture reason, not a preference. Deferral names the condition that would make the option viable later.

### Decision Outcome — 1 to 3 paragraphs

Opens with: `Selected option: Option N — <name>.` Validator-enforced.

Then why it best satisfies the drivers, plus the conditions, assumptions, dependencies, and sequencing requirements that must hold for the decision to remain valid.

### Architecture Impact — four required subsections

`### Business` — ownership, process, adoption, funding, stakeholder impact.

`### Data` — data flow, metadata, quality, lineage, governance, retention, ownership, lifecycle.

`### Application` — applications, Qlik/Talend components, integration points, APIs, orchestration, deployment model, dependency boundaries.

`### Technology` — runtime, infrastructure, network, identity, security, connectivity, scalability, resilience, observability, platform operations.

One concise paragraph each. You're saying where the decision lands, not writing an architecture chapter.

### Consequences — two required subsections

`### Positive Consequences` — 5 to 8 bullets.

`### Negative Consequences / Trade-offs` — 5 to 8 bullets. Exact heading, including the slash.

Be concrete. "Improved governance" is weak. "Creates one governed quality baseline visible through the catalog before operational remediation is built" is a consequence. The negatives must be real trade-offs this decision creates, not generic cautions.

### Implementation Implications — 6 to 10 bullets

**Required**, despite what older templates say. Architecture-oriented: prerequisites, sequencing, ownership, configuration boundaries, integration dependencies, testing, migration, rollout, change control. Not a product tutorial and not a task list.

### Operational Implications — 5 to 8 bullets

**Required.** What must be sustained after go-live: support ownership, monitoring, alerting, lifecycle management, access control, incident handling, documentation, auditability, review cadence.

### Risks and Mitigations — 4 to 8 bullets

Exact form, validator-enforced:

```
- Risk: <risk>. Mitigation: <mitigation>.
```

Specific to this decision.

### Review Triggers — 5 to 8 bullets

Opens with `Review this ADR if:` then the bullets.

Concrete, observable conditions: a product capability shipping or being withdrawn, a customer platform change, a new non-functional requirement, a security policy change, a cost model change, an operating model change, a strategic technology change. "If requirements change" is not a review trigger.

### Open Questions — 3 to 8 bullets, or the fixed sentence

If none: `No open questions at the time of this ADR.`

Open questions record genuinely unresolved material points. They are not a place to hide an unclear decision. If an open question could change the selected option, the ADR isn't ready for Accepted — keep it Draft or Proposed and say so.

## Total size

A peer reads the whole thing in three to five minutes and comes away with the decision, the alternatives, the trade-offs, and the review conditions. Fifteen minutes means it's carrying multiple decisions. Thirty seconds and they still ask "why this one?" means it's too thin.
