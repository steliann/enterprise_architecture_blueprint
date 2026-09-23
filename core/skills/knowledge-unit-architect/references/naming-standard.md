# KU Identifier and Bundle Naming Standard

Source of truth: the team's "Knowledge Unit Bundle and Naming Standard." Read this file
whenever you allocate a new KU ID or deliver a KU file — both build modes and refresh
need it; review mode needs it for the consistency check.

## The identifier: `ADL-NNN`

Three letters, each with a fixed meaning by position, then a three-digit sequence number
**scoped to that exact three-letter prefix** (MCA-001 and MHA-001 are independent
sequences).

**Position 1 — primary architecture area** (pick the single best fit; other areas the KU
touches go in metadata/tags, not the ID):

| Code | Area |
|---|---|
| A | Data Analytics |
| M | Data Movement |
| T | Data Transformation |
| Q | Data Quality |
| I | Artificial Intelligence |
| G | Data Governance |
| O | Operations/DevOps |

**Position 2 — deployment scope:**

| Code | Deployment |
|---|---|
| M | Client-managed |
| C | Cloud |
| H | Hybrid — use only when the hybrid *interaction* is material to the guidance, not just because components live in different places |
| A | All — use only when the guidance is genuinely deployment-independent, not merely adaptable |

**Position 3 — highest materially affected TOGAF layer**, precedence
`Business > Application > Data > Technology`:

| Code | Layer |
|---|---|
| B | Business |
| A | Application |
| D | Data |
| T | Technology |

Judge by architectural impact, not by which technology is named. A messaging-based
integration pattern between applications is still Application-layer even though it
involves messaging tech. This third letter is a fixed four-way choice (B/A/D/T) — it is
narrower than the `togaf_layers` metadata field, which may also include `Security`
(see `assets/ku_template.md`); `Security` is never used as the ID's third letter.

## Allocating a new ID

1. Pick the architecture area, deployment scope, and highest TOGAF layer per the tables
   above — this gives the three-letter prefix (e.g. `MCA`).
2. Find the next free sequence number **for that exact prefix** (check the KU corpus /
   Knowledge Fabric per `knowledge-fabric.md`). Sequences are independent per prefix:
   `MCA-001`, `MCA-002`, `MHA-001`, `QCD-001` are all valid and unrelated.
3. If the corpus isn't reachable, leave a placeholder like `MCA-XXX` with a note — a
   colliding ID is worse than a placeholder.

Do not derive the ID from the product name (a prior version of this skill used
product-based prefixes like `REPL-003` — that convention is retired; do not reuse it).

## Bundle path (fixed, not a suggestion)

```
knowledge-units/<KU-ID>/knowledge-unit.md
```

- The KU identifier is the bundle **directory** name — never the KU title.
- The file inside the bundle is always literally named `knowledge-unit.md`.
- The title lives in the YAML `title` field and the H1 heading only — never in the path.

Correct: `knowledge-units/MCA-001/knowledge-unit.md`
Wrong: `knowledge-units/MCA-001-efficient-data-ingestion/knowledge-unit.md`
Wrong: `knowledge-units/MCA-001/efficient-data-ingestion.md`
Wrong (deprecated flat convention): `MCA-001-efficient-data-ingestion.md`

This keeps the path stable even when the title is edited later.

## Immutability

- The ID and its bundle directory are permanent once assigned. Never rename the directory
  when the title changes, wording is refreshed, assets are added, or the KU is deprecated
  or superseded.
- IDs are never reused, including after deprecation/supersession/withdrawal/archival. If
  `MCA-004` is deprecated, the next KU in that prefix is `MCA-005`, not a reissued
  `MCA-004`.

## Asset naming

Assets that accompany a KU live alongside it (e.g. `knowledge-units/MCA-001/assets/...`)
and use clear, descriptive kebab-case filenames that communicate purpose independent of
visual content — `reference-architecture.svg`, `data-flow-example.png`,
`deployment-topology.drawio`. Avoid generic names (`image1.png`, `diagram-final.svg`,
`new-diagram-v2.png`).

## What changed from the flat-filename convention

Earlier tooling (and an earlier version of this skill) delivered KUs as a single file
named `<ID>-<short-title>.md` with no bundle directory. That convention is superseded by
the bundle-path standard above. When refreshing or reviewing an older KU stored under the
flat convention, recommend migrating it into the bundle path — same ID, same content,
new location — and note the migration in the delivery/change log; do not silently move
files without saying so.
