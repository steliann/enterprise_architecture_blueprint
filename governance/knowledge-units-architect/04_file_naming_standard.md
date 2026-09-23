# Knowledge Unit Bundle and Naming Standard

## 1. Purpose

This standard defines how Knowledge Units (KUs) are identified, named, stored, and organized.

The KU identifier is designed to provide a compact classification based on:

* the primary architecture area addressed by the KU;
* the deployment scope to which the KU applies;
* the highest materially affected TOGAF architecture layer;
* a unique sequence number.

KU identifiers and bundle directories are permanent once assigned.

---

## 2. KU Identifier

The KU identifier uses the following structure:

```text
ADL-NNN
```

Where:

* `A`: primary architecture area.
* `D`: deployment scope.
* `L`: highest materially affected TOGAF layer.
* `NNN`: non-zero three-digit sequence for the exact prefix.

Example:

```text
MCA-001
```

This represents:

* `M` — Data Movement;
* `C` — Cloud;
* `A` — Application layer;
* `001` — first KU assigned to the `MCA` prefix.

Sequence numbers are allocated independently for each exact three-letter prefix.

For example:

```text
MCA-001
MCA-002
MHA-001
QCD-001
```

`MCA`, `MHA`, and `QCD` each maintain their own sequence.

---

## 3. First Letter — Architecture Area

The first letter identifies the **primary architecture area** addressed by the Knowledge Unit.

| Code | Architecture Area       |
| ---- | ----------------------- |
| A    | Data Analytics          |
| M    | Data Movement           |
| T    | Data Transformation     |
| Q    | Data Quality            |
| I    | Artificial Intelligence |
| G    | Data Governance         |
| O    | Operations/DevOps       |

The selected area should represent the primary subject of the KU.

A KU may relate to several architecture areas, but only one area is encoded in the identifier.

Where several areas are involved, select the area that best represents the main architectural concern, capability, pattern, or guidance described by the KU.

Related areas may be represented separately in KU metadata where required.

### Examples

```text
MCA-001
```

Primary architecture area:

```text
Data Movement
```

```text
QAD-003
```

Primary architecture area:

```text
Data Quality
```

```text
IAT-002
```

Primary architecture area:

```text
Artificial Intelligence
```

---

## 4. Second Letter — Deployment Scope

The second letter identifies the deployment context to which the KU applies.

| Code | Deployment     |
| ---- | -------------- |
| M    | Client-managed |
| C    | Cloud          |
| H    | Hybrid         |
| A    | All            |

### Client-managed — `M`

Use when the KU applies specifically to environments operated or managed by the customer.

Examples may include:

* customer-managed runtime infrastructure;
* on-premises deployments;
* customer-managed virtual machines;
* customer-managed Kubernetes environments;
* locally operated platform components.

### Cloud — `C`

Use when the KU applies specifically to a cloud-managed or SaaS deployment.

### Hybrid — `H`

Use when the KU specifically addresses interaction between cloud and client-managed environments.

Use `H` when the hybrid nature of the architecture is material to the guidance, rather than simply because components happen to exist in different locations.

### All — `A`

Use when the guidance is materially applicable across deployment models and is not dependent on one particular deployment context.

Do not use `A` merely because a KU could potentially be adapted to multiple environments. Use it when the architectural guidance itself is genuinely deployment-independent.

---

## 5. Third Letter — TOGAF Architecture Layer

The third letter identifies the **highest materially affected TOGAF architecture layer**.

| Code | Layer       |
| ---- | ----------- |
| B    | Business    |
| A    | Application |
| D    | Data        |
| T    | Technology  |

When a KU materially affects more than one layer, use the following precedence:

```text
Business > Application > Data > Technology
```

The identifier should represent the highest architecture layer that is materially affected by the guidance.

The classification is based on the architectural impact of the KU, not simply on the technology mentioned in the document.

### Business — `B`

Use when the KU materially affects business capabilities, operating models, responsibilities, business processes, policies, or business-level outcomes.

### Application — `A`

Use when the KU materially affects application or service behavior, system interactions, integration responsibilities, application architecture, or solution-level capabilities.

### Data — `D`

Use when the KU primarily concerns data structures, datasets, data lifecycle, information models, data management, data quality, metadata, or governance of data.

### Technology — `T`

Use when the KU primarily concerns infrastructure, runtime platforms, deployment technologies, networking, compute, storage, or other technology-layer concerns without materially changing a higher architecture layer.

### Precedence examples

A KU describing how applications should exchange data through an asynchronous integration pattern may involve messaging technology, but its material architectural impact is at the Application layer.

It would therefore use:

```text
A
```

as the third letter.

A KU describing storage configuration for a runtime engine, with no material impact on application or data architecture, would use:

```text
T
```

A KU defining ownership and governance responsibilities for enterprise reference data may involve data structures and applications, but if the guidance materially affects organizational responsibilities and governance processes, it would use:

```text
B
```

---

## 6. Bundle Path

Every Knowledge Unit is stored as a stable bundle using the KU identifier.

The standard path is:

```text
knowledge-units/<KU-ID>/knowledge-unit.md
```

Example:

```text
knowledge-units/MCA-001/knowledge-unit.md
```

The KU identifier is used as the bundle directory name.

The KU title must not be included in the directory or filename.

For example, a KU titled:

```text
Efficient Data Ingestion Using Incremental Processing
```

with identifier:

```text
MCA-001
```

is stored as:

```text
knowledge-units/MCA-001/knowledge-unit.md
```

and not as:

```text
knowledge-units/MCA-001-efficient-data-ingestion/knowledge-unit.md
```

or:

```text
knowledge-units/MCA-001/efficient-data-ingestion.md
```

The title belongs in:

* the YAML metadata;
* the H1 heading of the Knowledge Unit.

This keeps the bundle path stable even when the KU title changes.

---

## 7. Bundle Stability

The KU bundle directory is permanent.

Once assigned:

```text
knowledge-units/MCA-001/
```

must remain associated with that KU for its entire lifecycle.

The directory must not be renamed when:

* the KU title changes;
* wording is improved;
* guidance is refreshed;
* supporting assets are added;
* the KU is deprecated;
* the KU is superseded.

KU identifiers and bundle directories are immutable.

---

## 8. Asset Naming

Assets use clear, descriptive kebab-case filenames.

Examples:

```text
assets/reference-architecture.svg
assets/data-flow-example.png
assets/deployment-topology.drawio
```

Avoid generic filenames such as:

```text
image1.png
diagram-final.svg
new-diagram-v2.png
```

The filename should communicate the purpose of the asset independently of its visual content.

---

## 9. Immutability and Reuse Rules

KU identifiers are immutable.

Once assigned, an identifier:

```text
MCA-001
```

must always refer to the same Knowledge Unit.

Identifiers must never be reassigned or reused.

This remains true when a KU is:

* deprecated;
* superseded;
* withdrawn;
* archived.

For example, if:

```text
MCA-004
```

is deprecated, a future KU must not reuse `MCA-004`.

The next available sequence should be used instead.

Example:

```text
MCA-005
```

---
