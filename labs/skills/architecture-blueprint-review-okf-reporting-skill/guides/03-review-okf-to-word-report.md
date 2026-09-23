# Review OKF -> Word Architecture Assessment Report

## Authority

The Review OKF is the source of truth for the report. The report may summarize and restructure the review, but it must not create new `GAP-NNN` items, silently change gap state/priority, or materially alter recommendation direction.

## Required report structure

1. Cover
2. About this architecture assessment
3. Table of contents
4. Executive assessment
5. Assessment approach and classification
6. Findings and recommendations at a glance
7. Detailed architecture findings and recommended responses
8. Cross-gap architecture themes
9. Validation items and evidence to capture
10. Aggregated architecture conclusions
11. Assessment disposition
12. Document status

Use `templates/word/architecture-assessment-report-content-template.md` for the content contract and `architecture-assessment-report-template.docx` for styling.

## Detailed gap presentation

Present every in-scope gap vertically:

- gap title/category;
- Priority / Confidence / Response / Horizon strip;
- **Architecture finding**
  - expected condition;
  - current context/evidence;
  - architecture gap;
  - impact if not addressed;
- **Recommendation**
  - target direction;
  - current capability path if relevant;
  - strategic/expanded path if relevant;
  - expected benefits;
  - acceptance/validation questions;
  - traceability.

The report can use customer-friendly labels instead of raw YAML field names, but values must remain consistent with the Review OKF.

## Executive roll-up

Counts must be calculated from the Review OKF and reused everywhere. Do not manually type conflicting counts in narrative, KPI blocks and tables.

Recommended KPIs:

- Candidate + Active gaps in scope;
- High/Critical priority gaps;
- Validation Items;
- Recommendations.

## Assessment method

Explain the evidence rule and promotion model. Include a classification table distinguishing Coverage Finding, Validation Item, Candidate Gap and Active Gap.

## Aggregated conclusions

Use 2-4 conclusions only when supported by multiple detailed findings. State explicitly that they are aggregated findings and are not additional gap records.

## Style and QA

Follow `templates/word/word-style-guide.md`.

After generation:

```bash
python scripts/validate_report_docx.py report.docx --review <review.zip-or-directory>
```

Then render the DOCX and visually inspect every page. Fix clipping, page-break, table and heading issues before delivery.
