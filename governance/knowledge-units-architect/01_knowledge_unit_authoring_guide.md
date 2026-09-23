# Authoring Knowledge Units: A Companion Guide

A quick reference to keep open when you write a KU. Pairs with `02_knowledge_unit_template.md` (a blank, fill-in-ready variant with per-section guidance comments is at `03_knowledge_unit_template_blank.md`). It answers the questions that come up the first few times you try this.

**A note on vocabulary.** In v2 the KU section that holds the pattern is called **Guidance**, not Decision. The word **Decision** is now reserved for the customer side: a piece of KU Guidance becomes a Decision when an EA writes it into a customer ADR. This guide uses the two words that way throughout. When you read "guidance," think "what the KU says to do." When you read "decision," think "the choice the field faces, which ends up in an ADR."

---

## What makes a KU good

A good KU meets all five of these. If any one is missing, the KU is not ready to ship.

1. **It captures guidance for a recurring decision.** Not a fact. Not a single configuration detail. It answers a question a CSE or EA will face again on a future engagement.
2. **It is opinionated.** "It depends" is not guidance. For Tier 2 KUs, "it depends on these specific signals, and here is what to do in each case" is guidance. For Tier 3 KUs, the opinion is the list of questions worth asking before deciding.
3. **It tells the reader what to do and what not to do.** The Anti-Patterns section is not optional. It is often the most useful part of the KU.
4. **A peer recognizes the situation when they read the Context.** The Context section tells the reader they have seen this situation before. If they finish reading Context and do not say "yes, I have seen that," the KU is either too general or too narrow.
5. **It does not repeat the product manual.** If `help.qlik.com` already explains it, link to that page in `qlik_help_links`. The KU captures what the manual does not: the guidance, the trade-off, and the situational judgment.

---

## How much information is enough

A target shape, section by section. The order matches the v2 template.

- **Context.** Three to six sentences. Enough that another CSE recognizes the situation in the field. Do not repeat the product documentation.
- **Boundaries.** Optional. One short paragraph that says where the guidance applies and where it does not: which products, which source and target platforms, the prerequisites, and the cases where someone should not use it. Skip it when the Context already makes the scope obvious.
- **Guidance.** As long as it needs to be, but every sentence should describe something the reader can do. Configuration examples belong here. For Tier 2 KUs, list the valid variants and the criterion for choosing each one.
- **TOGAF Impact.** Required. A few sentences on how the guidance lands across the business, data, application, and technology layers. Use the four layers as the structure. Keep it short. You are noting where the pattern touches each layer, not writing an architecture chapter.
- **Well-Architected Impact.** Required. Map the guidance to the AWS Well-Architected pillars. For each pillar that matters, say what the pattern improves and what it costs. This is where you explain why it is good architecture, not only how it works.
- **Consequences.** What this approach makes possible. What it gives up in exchange. What to watch out for. Keep the pillar-by-pillar trade-off analysis in Well-Architected Impact. Here, describe the practical results and what breaks if the pattern is ignored.
- **Anti-Patterns.** One or two specific traps. Name them with specifics. "Customer enables logical replication on a transactional source database with no read replica" is better than "performance issues."
- **Customer-Ecosystem Notes.** Optional. Only fill this in if the pattern interacts with the wider customer stack. If it does not, leave it empty. An empty section is fine. A section padded just to fill space is not.
- **Field Qualification Questions (Tier 3).** Optional. The situational questions a CSE or EA should ask before applying the pattern. These are the judgment calls the library cannot answer. For a Tier 3 KU this is the main section. For Tier 1 and Tier 2 it is where you park the questions that still need a human.
- **Implementation Guidance.** Optional. Enough direction to avoid the common mistakes when applying the pattern. Not a full manual.
- **Operationalization Guidance.** Optional. What has to be in place after the pattern is applied so it can actually run and be supported in production: monitoring, ownership, alerting, runbooks.

**Rule of thumb on total size.** If a peer can read the KU in about three minutes and then apply it, the size is right. If they need ten minutes to get through it, it is too big. If they finish in thirty seconds and ask "but what would I actually do?", it is too small or too general. The two impact sections are usually short, so the three-minute target still holds. If TOGAF Impact or Well-Architected Impact starts running long, that is often a sign the KU is carrying more than one decision. See "How big is too big."

---

## How big is too big

The clearest test: **the supersession seam**.

Ask yourself one question: if a future Qlik Replicate release changes how component X works, would I only need to update part of this KU?

If yes, that part belongs in its own KU.

A KU should only contain things that will be replaced together. This matters because of the append-only model. A successor KU replaces the previous one in full. You should never need to write "this KU replaces paragraphs 4 to 7 of the previous one." If you find yourself wanting to, the original was too big.

Other signs that a KU is too big:

- The Guidance section has more than one "what to do."
- You would naturally assign different owners to different parts.
- One section is Tier 1 confident, another is Tier 3 situational.
- You find yourself writing "depending on whether..." three or more times. Each "depending on whether" is either a variant inside a Tier 2 Guidance section or a separate KU.
- Two adjacent customer ADRs would cite different sections of this KU and ignore the rest.

When you are unsure, split. Two short KUs that link to each other through the `related` field are easier to maintain than one large KU.

---

## How small is too small

This is the harder question, and it is where you will see the most disagreement. Use three tests together.

**Test 1: The re-askable question test.** A KU should answer a question someone would ask out loud. "How do we configure CDC from HANA to Snowflake?" is one such question. "What is the value of buffer parameter X?" is not, on its own. If you cannot name the question the KU answers, you have a configuration detail, not guidance. Fold it into the Guidance of the parent KU.

**Test 2: The independent citation test.** Could a customer ADR cite this KU on its own, without also citing the KU you considered folding it into? If no, fold it in. If yes, it can stand on its own.

**Test 3: The guidance vs. setting test.** A piece of guidance is a position you are taking ("default to log-based CDC for HANA sources"). A setting is a value that supports the position (the specific log retention window). Positions like that are KUs. Settings go inside the Guidance section of their parent KU.

**One important exception: configuration recipes that are looked up often.** Some KUs look small but deserve their own entry because they are referenced repeatedly and they form a complete answer to a re-askable question on their own. A self-contained "QDA Cloud SSO with Entra ID" recipe is a complete answer to "how do I set up SSO with Entra?" Do not fold that into a broader "SSO patterns" KU. Keep it as a separate KU. The signal is "do I keep needing the same exact configuration in front of me on different engagements?"

If your KU is small, run all three tests. If it fails any one, fold it in. If it passes all three, ship it small.

---

## Should you start big and break it up, or start atomic and build up?

Two different approaches. **Pick one per session, not both at once.**

**Starting from memory (atomic-first).** Open with the patterns you have explained to a colleague more than three times. Each one becomes one KU. Write the Guidance section first, then go back and fill in Context, the two impact sections, Consequences, and Anti-Patterns. This is the cheapest content to capture because you already know it well. It also produces the right-sized KUs by default. You stop writing when you have answered the question you have been answering out loud for years.

**Starting from existing material (big-then-carve).** When you have a reference architecture, a customer document, or a wiki page already on your hard drive, do the opposite. Bring the document in as one oversized draft KU. Then break it apart along the supersession seams, using the tests in "How big is too big" above. Each break produces a candidate KU. Some of those candidates will end up folding back into siblings, which is fine and expected.

**Why not both at once.** The two approaches require different ways of thinking. Atomic-first means creating structure from what you already know. Carving means finding structure inside something that already exists. Switching between them in one session usually means neither one gets finished. Set aside separate time for each.

**Which to do first.** Start with the atomic-first approach in week two. The patterns you have explained three times are the easiest content to capture and the most confident. Save the carving work for week three, after the schema has settled and you have a few KUs in hand to compare against.

---

## Tier guidance in one line each

The tier shapes how much you write and what shape the KU takes.

- **Tier 1 (Reusable As-Is).** Opinionated, tight, generalizable. The Guidance section is short because there is only one right answer. The Anti-Patterns section is especially valuable here.
- **Tier 2 (Contextually Reusable).** Most of your KUs will be Tier 2. The Guidance section lists the valid variants and the criterion for choosing each. If you have more than three or four variants, the KU is probably combining two separate decisions. Split it.
- **Tier 3 (Field-Expert Annotation Only).** The question, not the answer. The Field Qualification Questions section lists what to ask the customer. For Tier 3, the library's job is to point to the expert and to make sure the next person asks the same questions you would.

---

## Filling in the metadata

The v2 frontmatter is longer than the old one. Most fields are descriptive, and the template comments explain them. These are the ones that need a judgment call.

- **`yaml_version`.** Leave it at the schema version the template ships with. You only change it if the schema itself changes, which is not your job as an author.

- **`tier`.** 1 is Reusable As-Is, 2 is Contextually Reusable, 3 is Field-Expert Annotation Only. If you cannot decide, see "When to ask the workstream for help." Tier drives how much of the record you complete: Tier 1 and 2 get the full record. Tier 3 needs Context and Field Qualification Questions, and little else.

- **`source_basis`.** Where the pattern actually came from: field experience, customer ADRs, product documentation, or an architecture review. Be honest. A reader weighs a pattern drawn from three real engagements differently from one drawn from the manual.

- **The relationship fields.** These are the ones people mix up. `related` is "read this alongside." `alternatives` is "this solves the same problem a different way." `migration_path` is "the ordered KUs for moving from one pattern to another." `supersedes` and `superseded_by` are the lifecycle chain: the record this one replaces, and the record that replaces it. When two KUs solve the same problem, they are alternatives, not duplicates. Do not delete one.

- **`originating_adrs` and `related_assets`.** Provenance. List the customer ADRs the pattern was distilled from, and link the non-KU assets (blueprint, checklist, playbook, diagram) that go with it. This is how a reader gets from the general pattern back to the concrete cases.

- **`peer_reviewers`.** A KU does not reach Approved until a peer has reviewed it. Name the reviewer here. Until then it sits at Proposed, which is fine.

- **`confidence` and `status`.** Covered under Common objections below. Low confidence and Proposed status are both legitimate. Ship the pattern marked for what it is, rather than not shipping it. The full status ladder is Draft → Proposed → Approved (→ Deprecated or Superseded). Use Draft for a record that is written but not yet ready to put in front of the workstream — for example one with known gaps still marked in it. Proposed means "ready for a peer to review."

- **The customer-environment blocks (`external_technologies`, `deployment`).** Low judgment, high consequence. Describe the environment precisely, because whether the next person can reuse the pattern depends on how well their environment matches yours. Name the source and target versions, the cloud vendor, and whether it is containerized.

- **The AI-assistance fields (`used_ai_to_solve_it`, `ai_solutions_used`).** Record honestly whether AI helped produce the pattern and which tools. This is not a confession. It tells the next person where the pattern's reasoning came from.

---

## Common objections, answered

Short and direct. Use these when you meet resistance, including from yourself.

- **"It will go stale."** It will. The `review_by` field exists. Tie it to the product release cadence. Write a successor KU when product changes make the pattern wrong. Outdated content is fine if it is marked as outdated. A library fails when content is wrong and the reader does not know it.

- **"I am not confident enough to write this down."** The `confidence` field exists. Mark it Low. The status `Proposed` exists. Write down the pattern even if you do not yet have full proof. A peer review later moves it to Approved. Being wrong in the meantime is fine. You write a successor KU.

- **"Versioning will be a nightmare."** Append-only. You never edit a KU after it is published — and *published* means **Approved**. While a record is Draft or Proposed it is still wet cement: redline it in place, including during peer review. Once it reaches Approved, changes mean a new record that replaces it through the `supersedes` and `superseded_by` fields. The chain of links shows the history of how the practice has changed.

- **"This is just more documentation that no one reads."** Possibly. The patterns you have explained more than three times are the ones a peer is most likely to need next month. If you have explained it three times, someone will need to read it once. If you have never explained it, do not write it yet.

- **"My expertise cannot be captured."** Most of it cannot. That is what Tier 3 is for. The library captures the questions you ask yourself before recommending an architecture. It does not replace the judgment that answers them. The library points to you.

- **"I do not have time."** Five to ten patterns across thirty days is the target. Pull from material you already have. Use an LLM to write a first draft from a transcript or a wiki page, then edit it. The bottleneck is the redline, not the typing.

- **"The AI will absorb this and replace me."** The AI assistant in Phase 2 pulls from the library and surfaces your patterns to the next CSE. You benefit from this too. Tier 3 is, by definition, the part that cannot be captured. The library extends your expertise. It does not replace it.

---

## Ready-to-write checklist

Before you open the template, you should be able to answer yes to all five.

- I can name the question this KU answers, in one sentence.
- I have at least one customer engagement where this question came up.
- I know which tier this is, or I am willing to decide once I start writing.
- I know one specific Anti-Pattern that someone has actually fallen into.
- I have a working title that names the source, target, or scenario specifically (not "best practices for X").

If you cannot say yes to all five, the KU is not ready yet. Add a note in the workstream channel ("I think there is a pattern around X but I am not ready to write it") and move on. The note serves as a placeholder until you are ready. Do not try to write a KU you do not yet have.

---

## Tooling: the knowledge-unit-architect skill

A Claude skill (`knowledge-unit-architect.skill`, in this folder — install it via your
Claude settings) operationalizes this guide. It has three modes: build a KU from an
existing document (big-then-carve), build one from scratch through a structured interview
(atomic-first), and review existing KUs for quality, consistency, and validity. Every mode
scores the result against a rubric distilled from this guide, runs a schema validator over
the v4 frontmatter and required sections, and checks the draft for overlap against
existing KUs — distinguishing true duplicates, version-drift supersessions, and legitimate
alternatives — plus corroboration in the Knowledge Fabric where the connector is
available. Use it as the default way to draft and pre-review KUs; it does not replace the
human peer review that moves a record to Approved.

---

## When to ask the workstream for help

Three triggers. Use the workstream channel for these. Do not wait until the weekly session.

- You cannot decide which tier the KU is.
- You cannot decide whether to split or to keep one large KU.
- You cannot decide whether to fold a small candidate into a larger one.

These are the three judgment calls that the leads need to align on together. Once the workstream has answered a few of each, the team will share a consistent view.
