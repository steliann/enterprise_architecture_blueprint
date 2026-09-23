# Customer Architecture Decision Review — ACME Industrial Supply Co.

> Synthetic customer-facing derivative of the ACME internal ADR–KU Alignment Report.

## Project Context

ACME is progressing a Teradata-to-Snowflake modernization on Azure, with Finance and Sales substantially cut over and Manufacturing/IoT still transitioning. This review focuses on the architecture decisions supporting that program and on whether the assumptions and safeguards behind those decisions still reflect the current phase of the migration.

## Portfolio Overview

The governing decision portfolio remains broadly coherent. The strongest follow-up topics are not a wholesale redesign of the platform, but a small number of older exceptions and conditional decisions that now deserve validation or execution closure.

## Decision Review Highlights

### ACME-ADR-003 — Shared staging schema
The original decision accepted a shared staging schema under migration-time pressure. Current guidance favors stronger domain isolation where blast radius and domain-level access control matter. The review should validate whether the original migration constraint still applies now that major domains have cut over.

### ACME-ADR-004 — Temporary direct analyst write access
The decision was explicitly temporary and included an end condition. The useful customer discussion is whether that end condition has now been met and whether the exception can close through the normal architecture-governance process.

### ACME-ADR-009 — IoT telemetry through nightly batch
The decision was shaped by staffing constraints, while current manufacturing stakeholders appear to need fresher OEE information. The workshop should first confirm the real freshness requirement and whether the original resource constraint still holds before considering any new ingestion design.

## Follow-up

Agree which ADRs need owner-led review, which safeguards need execution evidence, and which whitespace topics require separate discovery rather than immediate design change.
