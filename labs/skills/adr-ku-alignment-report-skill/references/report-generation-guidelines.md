# Report Generation Guidelines

## Preferred sequence

1. Establish assessment scope and evidence cutoff.
2. Ingest the full ADR corpus and relevant history.
3. Filter current assessment statuses to Accepted + Proposed.
4. Classify each current ADR internally as Direct / Adjacent / Contextual.
5. Resolve/revalidate current KUs for Direct/Adjacent ADRs.
6. Gather current customer/account context and qualify reliability where material.
7. Compare Declared vs Observed Alignment.
8. Identify finding types and priorities.
9. Analyze dependencies and portfolio trajectory, using Contextual ADRs only when they materially explain the story.
10. Derive risks and opportunities conservatively.
11. Build the prioritized engagement agenda.
12. Draft the Executive Rollup.
13. Add customer-shareable guidance.
14. Validate the report against the canonical ACME/Northstar presentation pattern.

## Presentation authority

The ACME and Northstar examples are canonical for visible report structure, information density, and summary-table shape.

The Operating Model remains authoritative for analysis semantics. Internal reasoning classifications do not need to become visible report columns unless they materially help the reader.

In particular:

- Direct / Adjacent / Contextual is required during analysis but not a mandatory visible column.
- Contextual ADRs normally remain outside the Decision Portfolio Inventory.
- The engagement agenda uses the compact five-column canonical table; detailed evidence is traceable through Material Findings rather than repeated.
- Risk and Governance Rollup is normally concise narrative bullets rather than a mandatory evidence table.
- Material Findings use the compact ACME/Northstar field set; additional fields are optional, not mandatory.

## Evidence rules

### ADR evidence

Use ADR text as the source for the customer’s documented decision, rationale, constraints, and declared alignment.

### KU evidence

Use current KU state, not stale snapshots. Product/technology evolution on the Qlik side should normally enter through KU changes.

### Customer context

Context is required to test whether assumptions/conditions still hold and whether a finding matters now.

Do not overstate reliability. Confirmed facts may be stated directly; credible observations should be qualified when material; working hypotheses should become validation questions rather than conclusions.

## ADR relevance rules

### Direct

Full assessment and metrics.

### Adjacent

Assess only the Qlik/Talend boundary. Include in metrics only when an actual alignment assessment is meaningful.

### Contextual

Use in reasoning/dependency analysis only. Do not assign No KU Coverage, count it in alignment metrics, or create a standalone visible alignment entry unless a genuine Qlik/Talend-relevant assessment exists.

## Writing guidance

- Be concise but evidence-rich.
- Separate architecture conclusion from customer-success interpretation.
- Prefer “validate/revisit/confirm” over prescriptive solution language.
- Do not prescribe a replacement design before customer requirements and constraints are validated.
- Make the Executive Rollup useful to an account team without turning it into a health score.
