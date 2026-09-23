# Validation Guide

## Blueprint validator

Checks required package anchors, frontmatter parseability, duplicate IDs and dangling ID references.

```bash
python scripts/validate_blueprint_okf.py blueprint.zip
```

## Review OKF validator

Checks package structure, metadata enums, unique IDs, gap/recommendation links, register counts, validation-item separation, required headings and optional Blueprint traceability.

```bash
python scripts/validate_review_okf.py review.zip --blueprint blueprint.zip
```

## Word validator

Checks required section headings, presence of every in-scope gap title, key report labels, unresolved placeholders and optional consistency against a Review manifest.

```bash
python scripts/validate_report_docx.py report.docx --review review.zip
```

## Slide validator

Checks title/methodology/portfolio/next-step slides, gap-title coverage, one-gap-per-slide default, duplicate/missing gap slides and unresolved placeholders.

```bash
python scripts/validate_review_slides.py review.pptx --review review.zip
```

## All-assets gate

```bash
python scripts/validate_all.py --blueprint blueprint.zip --review review.zip --docx report.docx --pptx review.pptx
```

A validator warning does not automatically block delivery, but every warning must be understood. Structural errors block delivery.

## Coverage rubric validation

When a custom rubric is used, validate it with `scripts/validate_coverage_rubric.py` and pass it to `validate_review_okf.py --coverage-config ...`. Category totals must reproduce from `coverage_dimensions`; the combined total must equal the arithmetic mean of category scores; model hashes should match the resolved rubric.
