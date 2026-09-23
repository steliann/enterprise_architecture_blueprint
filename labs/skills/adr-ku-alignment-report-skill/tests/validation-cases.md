# Validation Cases

The validator covers structural and canonical-presentation rules; semantic review must also apply these cases.

## Must pass structurally

1. Canonical ACME report as provided.
2. Canonical Northstar report as provided.
3. A generated report using the eleven canonical sections.
4. Evidence snapshot using `accepted_adrs` / `proposed_adrs`.
5. Evidence snapshot using the newer aliases `accepted_adrs_assessed` / `proposed_adrs_assessed`.

## Must pass semantically

1. Accepted Direct ADR + current KU → normal alignment assessment.
2. Proposed Direct ADR → assessed, clearly pending, separate from governing metrics.
3. Adjacent third-party ADR → assess only Qlik-relevant boundary, without requiring a visible Relevance column.
4. Contextual customer ADR → may inform another finding but is not in alignment metrics or No KU Coverage.
5. Superseded KU → successor guidance used; ADR reference flagged; ADR unchanged.
6. Sound ADR + missing failover test → Execution follow-up, not necessarily Decision revisit.
7. No suitable KU for Direct ADR → KU coverage gap; do not automatically create a KU.
8. Missing ADR in relevant domain → Architecture whitespace / discovery flag, not architecture gap.

## Canonical presentation expectations

1. Section 3 uses the compact six-column KU alignment table from ACME/Northstar.
2. Section 9 uses `Priority | Conversation | Why now | Intended outcome | Type`.
3. Risk rollup may be narrative bullets.
4. Findings do not require visible Relevance / Assessment scope / Shareability fields.
5. Contextual ADRs are surfaced only when they materially help explain a finding; no mandatory contextual inventory is required.
