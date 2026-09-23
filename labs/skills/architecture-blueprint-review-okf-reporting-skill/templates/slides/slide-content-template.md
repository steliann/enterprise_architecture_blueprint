# Architecture Blueprint & Review Slide Content Template

## Title

**<Customer> Architecture Blueprint & Review**  
Current-state baseline, architecture findings and recommendations  
Architecture Review & Recommendations  
<Authoring team>  
<Month Year>

## Optional baseline sequence (when Blueprint is available)

1. **A shared architecture baseline for solution understanding** - baseline/validation/shared-understanding framing and discussion objective.
2. **Architecture footprint at a glance** - counts of use cases, capabilities, data products, flows, controls, operations and ADRs. State that these are scope/coverage indicators, not architecture quality scores.
3. **Business outcomes drive different architecture needs** - 5-7 outcomes and the architecture emphasis each creates.
4. **<Core product/service> is the centre of the architecture** - source domains -> integration/processing -> core product/service -> specialized products/consumers.
5. **Integration combines shared processing with domain-specific controls** - 4-6 principal patterns.
6. **Trust is built through layered controls** - 4-5 trust layers.
7. **Operations are part of the architecture** - orchestration, runtime/capacity, monitoring, recovery, trust services.
8. **The current state includes deliberate transitions** - transition/current position/direction table.

## Review methodology

### Architecture assessment starts from the baseline

1. Baseline evidence
2. Expected outcome
3. Material mismatch
4. Response path

**UNKNOWN != GAP** - incomplete or undocumented information remains a coverage finding or Validation Item.

## Portfolio

### Gaps, validation items and recommendations stay separate

- `<n>` Candidate/Active gaps
- `<n>` Validation Items
- `<n>` High/Critical priority recommendations
- `<n>` Recommendations total

## Priorities

### <3-5> findings shape the first review priorities

For each: short label + one-line architecture consequence.

## Detailed gap slide - repeat once per gap

### <Gap title>

**<STATE>**  **PRIO. <PRIORITY>**  **CONF. <CONFIDENCE>**  **<RESPONSE CLASS>**

**ARCHITECTURE FINDING**

**Current condition**  
<2-3 short lines>

**Architecture gap**  
<2-3 short lines>

**Impact if not addressed**  
- <1-2 bullets>

**RECOMMENDATION**

**<Action-oriented recommendation headline>**

<Simple 2-4 step architecture flow or target-state visual>

- <3-5 implementation/architecture actions>

**EXPECTED BENEFIT**  
<3 concise benefits separated by bullets/dots>

**VALIDATE**  
<1-2 customer/design questions>

## Validation items

Keep them visually separate from gaps. State why each requires evidence before classification.

## Aggregated target direction

Show 2-4 aggregated conclusions and how they combine into one coherent target direction. State that these are syntheses, not new gap records.

## Closing

### Validate the findings and agree the target sequence

1. Confirm evidence
2. Select first moves
3. Resolve major target-state decisions
4. Confirm governance/ownership
5. Close Validation Items

**Desired workshop outcome:** validated gap set, agreed first priorities, and clear owners for decisions/evidence.
