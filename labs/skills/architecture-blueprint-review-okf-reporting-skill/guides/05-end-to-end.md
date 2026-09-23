# End-to-End Generation

## Full pipeline

1. Unpack and validate the Blueprint.
2. Create Review OKF from the frozen Blueprint snapshot.
3. Validate the Review OKF against the Blueprint.
4. Extract a Review manifest with `scripts/extract_review_manifest.py`.
5. Generate the Word report from the validated Review.
6. Validate + render + visually inspect the Word report.
7. Generate the slide deck from the validated Review; when the Blueprint is available, use combined discussion mode.
8. Validate + render + visually inspect the slide deck.
9. Run `scripts/validate_all.py` as the final cross-asset gate.
10. Deliver only the requested final artifacts.

## Naming convention

Recommended names:

- `<customer>-architecture-blueprint-review-okf-v<version>.zip`
- `<customer>-architecture-assessment-and-recommendations-v<version>.docx`
- `<customer>-architecture-blueprint-and-review-customer-discussion-v<version>.pptx`

## Consistency rule

The Review OKF is the single source for all counts, gap titles, states, priorities and recommendation mappings. If a downstream asset disagrees, fix the downstream asset unless the user explicitly requests a Review refresh.

## Coverage rubric input

If a portable coverage rubric is supplied, validate it first and use it consistently during the Review OKF stage. Do not apply new weights only to the combined score; every category score must use the same resolved rubric and carry the same model hash.
