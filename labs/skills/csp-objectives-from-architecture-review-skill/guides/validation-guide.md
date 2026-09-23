# Validation Guide

## Structural gate

A deliverable passes only with **zero errors** from `scripts/validate_csp.py`.

The validator checks:

### Package structure
- required root files and folders;
- business/technical indexes;
- knowledge-model files.

### Frontmatter
- required keys by artifact type;
- ID format and uniqueness;
- list-valued relationship fields;
- allowed governance/planning states;
- valid ISO dates;
- schema version.

### Referential integrity
- TO `business_objectives` resolve to active BO IDs;
- TO `source_recommendations` resolve to current review recommendations;
- BO primary use cases are non-empty;
- optional Blueprint validation resolves BO use-case IDs when Blueprint is supplied.

### Recommendation coverage
- every current recommendation is covered by at least one active TO;
- no active TO references a recommendation absent from the current review;
- a recommendation mapped more than once is reported;
- a TO with multiple recommendations is reported unless intentionally consolidated.

### Metadata alignment
For one-recommendation TOs:
- horizon must match the recommendation;
- impact must match when both are present;
- category mismatch is a warning because taxonomy normalization can be legitimate.

### Required content sections
BOs:
- Objective
- Primary Business Use Cases
- Business Success Measures
- Customer Success Plan Fields
- Acceptance

TOs:
- Objective
- Business Objectives
- Source Recommendations
- Architecture Rationale
- Technical Success Measures
- Customer Success Plan Fields
- Acceptance

### Refresh identity checks
When `--previous` is supplied:
- reused IDs are compared semantically using normalized Objective text and primary relationships;
- suspicious ID reuse is warned;
- new IDs below/equal to the prior historical maximum are warned;
- created dates changing on reused IDs are warned.

The validator cannot prove semantic equivalence perfectly. Treat identity warnings as mandatory human/agent review items.

## Warning policy

Warnings do not automatically block packaging, but the generating agent must either:
- resolve them; or
- state why they are acceptable.

For customer-facing production, prefer zero warnings.
