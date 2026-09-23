# Worked Example — Recommendation to Technical Objective

This example is deliberately generic and contains no customer-specific architecture.

## Source recommendation

**REC-042 — Replace customer-managed runtime switching with workload-adaptive managed capacity**

Evidence:
- workload demand differs materially between processing windows;
- the customer maintains custom infrastructure-switching logic;
- the target platform can provide managed elastic/runtime capacity;
- acceptance requires workload compatibility, recovery behaviour and retirement criteria for the custom mechanism.

## Weak CSP conversion

> **TO — Implement managed runtime.** Install the managed runtime and migrate all jobs.

Why weak:
- it is a task;
- it assumes implementation completion equals success;
- it does not state the service/capacity condition that matters.

## Strong CSP conversion

> **Objective:** Provide workload-adaptive runtime capacity that satisfies distinct processing windows without customer-owned infrastructure switching, while preserving required workload compatibility and recovery behaviour.

Possible technical success measures:
- representative workloads execute successfully on the target managed runtime;
- capacity adapts to agreed workload windows without the legacy switching mechanism;
- interruption/restart behaviour is validated;
- retirement criteria for the customer-owned switching mechanism are met;
- operational evidence confirms the target service condition.

This TO would inherit the source recommendation horizon/impact and map only to business objectives that materially depend on the affected processing capability.
