# Word Architecture Blueprint Report Guide

> **Routing note:** This guide is for the descriptive Architecture Blueprint baseline.
> For a customer-facing Architecture Assessment with gaps and recommendations, use
> `guidance/assessment-word-report-guide.md`.


## Purpose

The Word document is the polished customer-shareable expression of the validated
Markdown baseline. It should be easier to read than the Markdown and normally
shorter.

Do not perform a literal Markdown-to-Word conversion.

## Source of truth

Use the validated Markdown report as the canonical narrative.

If the Word document would materially change a conclusion or introduce new
architecture content, update the Markdown first.

## Recommended content

Normally include:

1. Cover
2. Purpose and Scope
3. Executive Architecture Summary
4. Business Outcomes
5. Architecture Overview
6. Data and Integration Landscape
7. Data Products and Consumption
8. Principal Architecture Choices
9. Data Quality, Trust and Governance
10. Operations and Resilience
11. Architecture Evolution and Current Transitions
12. Points to Validate
13. Architecture Baseline Conclusion

Appendix inventories are optional and are usually excluded unless traceability
is useful to the customer.

## Curation

The Word report should preserve the richer narrative at the start of every
major section after the Executive Summary.

Then use only the most useful supporting structures:

- a concise architecture-at-a-glance table;
- one simplified architecture view;
- business outcome table;
- principal product table;
- architecture choice table;
- trust/governance table;
- operations table;
- transition table;
- validation table.

Do not reproduce every detailed sub-section and table from the Markdown when
the same point is already clear in prose.

## Tone

Use customer-facing architecture language.

- factual;
- explanatory;
- collaborative;
- descriptive before evaluative;
- explicit about transitions;
- careful about unvalidated concerns.

Avoid internal OKF terminology unless it is useful for traceability.

## Architecture concerns

If a serious concern is supported by the baseline, state it proportionally.
Otherwise use language such as:

- "This is an area for validation."
- "The dependency is architecturally significant."
- "The current mechanism may be revisited independently of the requirement."
- "No critical failure has been established from the information reviewed."

Do not add a gap-analysis chapter unless explicitly requested.

## Visual composition

Follow `styles/word-style.md`.

Prefer:

- generous whitespace;
- short paragraphs;
- strong green section headings;
- concise tables;
- light green or light teal callout boxes;
- a small number of meaningful diagrams.

Avoid dense pages and tables that require very small text.

## Document metadata

Record:

- customer;
- report title;
- source Markdown report version;
- status;
- date;
- confidentiality classification when applicable.

Do not display YAML frontmatter.

## QA

Before delivery:

1. render the DOCX to page images;
2. inspect every page at 100%;
3. correct overflow, broken tables, header/footer issues, awkward page breaks and
   unreadable text;
4. re-render after each layout-sensitive change.
