# Changelog

## 2.0.0

Expanded the skill from blueprint-baseline reporting to a combined blueprint and
architecture-assessment reporting workflow.

- Added first-class Architecture Assessment / Review OKF generation and refresh.
- Added architecture-first recommendation rules: recommended direction ->
  practical implications -> key considerations -> Qlik/Talend role -> benefits.
- Removed entitlement/product classification as the required customer-facing
  narrative structure; entitlement remains optional internal metadata.
- Added explicit technical-lead guidance depth: enough to understand what the
  team must review/adjust, without becoming a delivery/PS runbook.
- Added data-placement/persistence assessment guidance across source, staging,
  curated, presentation and consumption layers.
- Added explicit handling for static/reference/master data, historical snapshots,
  retained extracts, exchange/TRE datasets and advanced-analytics data.
- Added transformation-placement and analytical-platform fitness guidance.
- Added rules to preserve existing governance, DQ, lineage, business rules and
  orchestration when still fit.
- Added customer-validation handling for correcting, reclassifying, superseding
  or withdrawing earlier findings.
- Added canonical Assessment OKF template, schema and validator.
- Added dedicated customer-facing Architecture Assessment Word guide.
- Added DOCX render-and-inspect QA requirement for assessment Word delivery.

## 1.0.0

Initial skill package.

- Canonical versioned Markdown architecture-baseline template.
- Markdown validation workflow and validator script.
- Blueprint-to-Markdown generation guidance.
- Markdown-to-Word curation guidance.
- Markdown-to-PowerPoint workshop guidance.
- Reusable Word and PowerPoint style systems derived from the approved visual
  language without including the original example documents.
- Supports Markdown-only or full three-deliverable workflows.
