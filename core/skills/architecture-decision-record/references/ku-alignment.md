# Knowledge Unit alignment and Fabric lookup

An ADR uses KUs as architecture evidence. It must not cite them blindly, and it must not hide a conflict with one.

## Finding real KUs

`related_patterns`, `related_adrs`, `supersedes`, and `superseded_by` take **real IDs only**. To get them, query the Knowledge Fabric connector (named something like "Knowledge Fabric (VPN Required)"; it exposes `list_available_indexes`, `search_documents_simple`, `search_documents_with_filters`, `get_available_filters`).

Call `list_available_indexes` first as a cheap probe — it confirms the connector is reachable and shows you what's actually indexed. Tool and index names drift, so adapt to what the probe returns rather than assuming.

Keep it read-only and cheap: a few targeted queries on the decision's subject and products. Never publish to the Fabric from this skill.

**If the Fabric is unavailable** (VPN off, connector not configured): say so once, don't retry in a loop, and proceed. Ask the user for KU IDs if they have them. Leave unverifiable relationship fields `null` and record the intended relationship as an open question. Note "fabric unavailable — skipped" in the quality report, and state that the alignment checks are required before the ADR can move to Accepted.

## The four checks

Run all four before writing any citation.

**1. Boundary fit.** Does the customer or program context sit inside the KU's stated Boundaries? A KU scoped to single-tenant deployments doesn't support a multi-tenant decision, however relevant its guidance sounds.

**2. Guidance fit.** Does the decision follow the KU's guidance, or diverge from it? Divergence isn't automatically wrong, but it must be disclosed.

**3. Anti-pattern check.** Does the decision trip any anti-pattern the KU names? If it does, that's either an explicit, justified exception or a reason to revisit the decision. It is never something to leave unsaid.

**4. Trade-off consistency.** Do the ADR's consequences reflect the trade-offs the KU already documents? A KU that warns about an operational cost, paired with an ADR whose consequences are silent about it, means the ADR is incomplete.

## Classify the relationship

Each relevant KU gets exactly one classification, and each has a different obligation.

### Supported

The decision follows the guidance and fits the boundaries. Add the KU to `related_patterns`. No extra section needed.

### Conditionally supported

The KU supports the decision only while certain conditions hold. Add it to `related_patterns` **and** put the condition somewhere it will be acted on — Decision Outcome, Implementation Implications, Operational Implications, Risks and Mitigations, Review Triggers, or Open Questions. A condition recorded only in metadata will be missed.

### Constrained

The KU narrows how the decision must be implemented or governed. Cite it and make the constraint explicit in the body. Don't bury a constraint in a frontmatter list.

### Contradicted

The decision goes against the KU. Do not present the KU as a supporting pattern.

Add the optional `## Knowledge Unit Alignment` section immediately after Decision Outcome and state which of these it is:

- a deliberate, justified exception for this context;
- a sign the decision should be revised;
- a sign the KU is outdated and needs review;
- a conflict that architecture governance must resolve.

An undisclosed contradiction is the worst governance failure an ADR can commit, and it's a **Blocker** in review mode. Its whole value is in being visible.

## The Knowledge Unit Alignment section

Include it when any KU materially supports, constrains, or contradicts the decision. Omit it entirely when no KU is materially involved — an empty section is worse than no section.

Structure:

```markdown
## Knowledge Unit Alignment

### Supporting Knowledge Units

<KU ID and title, and what specifically it supports.>

### Conditional Support and Constraints

<Which KU, which condition or constraint, and where in this ADR it is handled.>

### Contradictions or Exceptions

<Which KU, what the contradiction is, and why this context justifies it — or that it doesn't.>

### Alignment Outcome

<One of: aligned / conditionally aligned / misaligned / requires a governance exception.>
```

The validator checks that `### Alignment Outcome` exists and that its text states one of those four outcomes.

When a contradiction is recorded, the validator also expects KU alignment to surface in Risks and Mitigations, Review Triggers, and Open Questions. That isn't box-ticking — a contradiction creates a real risk, a real review condition, and usually an unresolved governance question.

## Don't duplicate the KU

The commonest citation failure isn't a wrong link, it's an ADR that reproduces a KU's guidance instead of pointing at it. If the ADR explains a pattern at length, cut it and cite the KU. The ADR's job is what was decided **here** and why — the reusable part already lives somewhere else.

If no KU exists for guidance the ADR needed, note it as a follow-up: this is a candidate KU. That's how the library grows.
