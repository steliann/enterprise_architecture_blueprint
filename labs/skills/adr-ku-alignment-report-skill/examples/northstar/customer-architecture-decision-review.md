# Customer Architecture Decision Review — Northstar Components Group

> Synthetic customer-facing derivative of the Northstar internal ADR–KU Alignment Report.

## Project Context

Northstar is modernizing a mixed Talend on-prem and Qlik Talend Cloud integration estate with Snowflake as the primary analytical platform. The technology direction is increasingly clear; the review therefore concentrates on whether transitional technical and operating-model decisions are becoming permanent by default.

## Portfolio Overview

The main discussion themes are runtime resilience, retirement of temporary migration patterns, the Proposed production-approval model, and whether service-data freshness requirements have changed.

## Decision Review Highlights

### NS-ADR-003 — Remote Engine for SAP transition
The current runtime placement remains a transitional choice, but the resilience condition associated with the decision needs to be validated and evidenced. The customer discussion should determine whether the workload remains intentionally transitional and whether the agreed recovery/failover model is now complete.

### NS-ADR-006 — Central production approval
This decision is still Proposed. The workshop should use that status to validate whether the required controls can be preserved without creating a structural delivery bottleneck before the decision becomes governing architecture.

### NS-ADR-007 — Nightly service analytics
The ADR’s original KU reference has been superseded, but the successor guidance preserves the same principle: cadence should follow consumer freshness needs. The current question is therefore whether the business requirement has changed from next-day to intraday availability.

## Follow-up

Agree the disposition of overdue transition ADRs, the design work still required for Proposed decisions, and the operational/discovery actions needed before the next report refresh.
