# Input Routing and Output Selection

## 1. Blueprint OKF supplied

The Blueprint can generate the Review OKF. If the user asks for the complete review package, continue to Word and slides only after the Review OKF validates.

Expected Blueprint indicators include a top-level `index.md`, a knowledge model, a high-level architecture file and model folders/inventories such as use cases, capabilities, data products, flows, controls, operational capabilities and ADRs. The exact architecture content is not prescribed.

## 2. Review OKF supplied

Do not re-run gap discovery unless the user asks to refresh the review. Treat the Review OKF as authoritative and generate the Word report/slides from it.

## 3. Review + Blueprint supplied

Use the Blueprint to verify Review traceability and to generate optional baseline slides. Do not silently replace existing review conclusions merely because a different interpretation seems possible; flag refresh candidates and follow the user's intent.

## 4. Downstream asset supplied

When the user asks to validate or refresh a Word report/PPTX, require or locate the Review OKF first. Downstream assets cannot be validated semantically without the review authority.


## Optional coverage rubric override

A supplied `coverage-rubric.yaml` is a scoring configuration, not architecture evidence. Merge only its `coverage_rubric` section over `config/defaults.yaml`. Preserve the skill defaults unchanged. The same override must be used consistently for every coverage category and for the combined score.
