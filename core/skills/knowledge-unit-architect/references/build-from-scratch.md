# Mode: Build from Scratch ("atomic-first")

Capture a pattern that lives in the author's head. The method is **atomic-first**: nail the
single decision, write the Guidance first, then build the rest of the record around it.
The interview *is* the source document here, so it must be thorough — but respect the
author's time: batch questions, never re-ask what they've already said, and stop when the
record is full, not when the question list is empty.

## Stage 1 — Interrogate (three rounds, batched)

**Round 1 — Qualify the pattern.** Before anything else, establish the KU deserves to
exist. The readiness bar (all five, or stop):

1. The author can name the question this KU answers, in one sentence.
2. At least one real engagement where the question came up.
3. A tier — or willingness to decide one during the interview.
4. One specific anti-pattern someone actually fell into.
5. A working title naming the source/target/scenario specifically (not "best practices
   for X").

A good opener: *"What's the pattern you've explained to a colleague more than three
times?"* — that phrasing reliably surfaces the right content. If the author can't clear the
bar, don't force it: offer to record a one-line placeholder ("I think there is a pattern
around X") for the workstream channel instead, and stop. An unwritten KU is better than a
hollow one.

**Round 2 — The decision core.** Pull the closest existing KUs from the fabric first (see
`knowledge-fabric.md`, "fabric-assisted interrogation") and interview *against* them:

- The Guidance: what do you do, concretely? Config values where relevant. For Tier 2:
  which variants exist and what signal picks each one? For Tier 3: what questions do you
  ask the customer, and why does each one matter?
- The situation (→ Context): how do you recognize a customer in this situation? What goes
  wrong without the pattern?
- The trade-offs (→ Consequences / Well-Architected Impact): what does this give up?
  Which pillars does it favor, at what cost?
- The traps (→ Anti-Patterns): what's the common-mistake version? Name it with specifics.
- Boundaries: where does this NOT apply?

**Round 3 — The record.** Environment (product versions, source/target versions, cloud
vendor, containerized), provenance (engagements, originating ADRs, honest source_basis /
confidence / AI-assistance fields), ownership (owner, contributors, review_by tied to a
release), relationships (confirm the fabric-found candidates with the author), and the
**ID** — confirm architecture area, deployment scope, and highest TOGAF layer with the
author to derive the three-letter prefix per `references/naming-standard.md`, then find
the next free sequence number for that exact prefix.

Skip any question already answered. If rounds 2 and 3 fit one batch for a simple Tier 1
recipe, merge them.

## Stage 2 — Fabric cross-check

Largely done during Round 2; finish the four checks in `knowledge-fabric.md` (especially
the overlap triage — duplicate vs. supersession vs. alternative — and ID allocation)
before drafting.

## Stage 3 — Draft

Write Guidance first, from the author's own words — preserve their specifics; tighten, do
not generalize away the opinion. Then Context, the impact sections, Consequences,
Anti-Patterns, then frontmatter. Tier 3 KUs: Context + Field Qualification Questions carry
the record; mark the rest light or N/A rather than padding.

Show the draft to the author before formal assessment — they will catch wrong-in-fact
faster than any rubric catches wrong-in-form.

## Stages 4–5 — Assess, gate, deliver

Per SKILL.md and `quality-rubric.md`. In this mode a gate failure almost always means a
missing interview answer, so failed criteria map directly to one or two targeted follow-up
questions — ask exactly those, no more.
