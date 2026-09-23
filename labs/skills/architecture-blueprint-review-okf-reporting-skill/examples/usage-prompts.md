# Example Usage Prompts

## Full pipeline from a Blueprint OKF

> Using the attached Architecture Blueprint OKF, create the complete architecture review package: Review OKF, customer-facing Word assessment report, and customer-discussion review slides. Validate every asset before delivery.

Expected pipeline:

`Blueprint OKF -> Review OKF -> Word report -> Slides`

## Review OKF only

> Review the attached Architecture Blueprint OKF and produce the Architecture Blueprint Review OKF only. Keep incomplete evidence as coverage findings or Validation Items rather than inferring gaps.

## Word report from Review OKF

> Using the attached Architecture Blueprint Review OKF, create the customer-facing architecture assessment and recommendations Word report. Do not change the gap set or recommendation direction.

## Slides from Review OKF

> Using the attached Architecture Blueprint Review OKF, create the customer-discussion review deck. Include one detailed slide for every in-scope Candidate or Active Gap.

## Combined discussion deck

> Using the attached Blueprint OKF and Review OKF, create a combined Blueprint & Review customer-discussion deck: compact baseline slides first, then methodology, review portfolio, priorities, one slide per gap, validation items, target direction, and next steps.

## Validate existing assets

> Validate the attached Review OKF, Word assessment report, and review slides for structural integrity, traceability, count consistency, and Review-to-downstream alignment. Report errors and warnings without changing content.

## Use a Workbench coverage rubric

> Generate the Architecture Blueprint Review OKF from this Blueprint. Use the attached `coverage-rubric.yaml` exported from the Architecture Blueprint Workbench instead of the skill default coverage weights. Preserve the raw dimension scores and scoring-model hash in the Review OKF.

## Recalculate coverage with new weights

> Recalculate only the coverage scores in this Review OKF using the attached `coverage-rubric.yaml`. Preserve the existing coverage evidence/findings, gaps and recommendations unless the recalculated score exposes a consistency problem. If the Review lacks raw `coverage_dimensions`, tell me a full coverage rescore is required.
