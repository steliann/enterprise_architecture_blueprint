# Using the Qlik Knowledge Fabric Connector

The Knowledge Fabric is Qlik's MCP-accessible search service over internal knowledge. Use
it in stage 2 (before drafting) in build modes, and in the validity stage of review mode.

## What it looks like (observed August 2026 — verify at runtime)

The connector is named **"Knowledge Fabric (VPN Required)"**. Observed tools:
`list_available_indexes`, `get_available_filters`, `search_documents_simple` (query +
size + truncate_length, searches all permitted indexes), plus filtered/index-scoped
variants (`search_documents`, `search_documents_in_indexes`, `search_documents_with_filters`).

Observed indexes: `help_pages`, `sfdc_knowledge_articles`, `case_information` (support
cases), `qlik_dev`, `qlik_com`, `stitch_docs`, `stitch_conversations_processed`,
`qlik_youtube_videos`, and `call_transcripts` (Qlik sales-call transcripts — summary +
per-topic chunks; a separate `call_transcripts_raw` may hold verbatim text for the same
calls). `call_transcripts` is sales/account data, not architecture guidance — apply the
same privacy-hygiene rule to it as to `case_information` (check 4 below): corroborate
with it, never copy account names or deal specifics into a KU. Useful filters include
`qlik_product` and `intent_categories` (Troubleshooting / How-to / Concept / Announcement).

Results come back as chunks with `content_title`, `content_text`/`chunk_text`,
`source URL`/`source_url`, `_index`, and security flags. Relevance `_score` values can be
flat/uninformative — judge relevance by reading the content, not the score.

Deployments evolve, so still verify at the start: call `list_available_indexes` (cheap)
and adapt to what you actually see. If the tool names differ, look for any MCP server
whose name suggests knowledge/fabric search and probe one cheap call before relying on it.

**If no fabric tools are available** (typically: VPN not connected), tell the user once —
they can connect the "Knowledge Fabric" connector and re-run, or proceed without it.
**Proceed either way** — but every skipped check below must appear in the quality report
as "fabric unavailable — skipped", and the delivery recommendation must say these checks
are required before the KU reaches Approved.

## Where the KUs themselves live

As of mid-2026 the fabric indexes documentation and field evidence but has **no KU index
yet** — the KU library is the corpus being built. So for KU-vs-KU checks (duplicates,
relationships, IDs), the authoritative source is the team's KU library folder/repo. If the
user has it mounted, search it locally; if a KU index appears in `list_available_indexes`
later, prefer that. If neither is reachable, record the check as skipped.

## The four checks

### 1. Overlap triage (against the KU corpus)
Search the KU corpus for the working title, tags, and 2–3 phrasings of the re-askable
question. For every overlapping hit, do not just flag it — **diagnose why it overlaps**
and recommend a disposition. Compare the two side by side: the decision answered, the
Guidance position, version scopes (`qlik_products`, `external_technologies`), deployment
context, and status/confidence. The dispositions:

- **True duplicate** (same decision, same answer, same applicability) → don't write a new
  KU. Recommend strengthening the existing one instead — under the append-only model that
  means a *successor* record if the existing KU is Approved (carrying any new evidence,
  anti-patterns, or engagement provenance the author brings), or a direct edit only if it
  is still Draft/Proposed. Surface the existing ID either way.
- **Version drift** (existing KU is correct for prior product versions; the new pattern
  reflects current versions or changed product behavior) → this is a **supersession**, the
  system working as designed. Write the new KU, set `supersedes: <old ID>`, and recommend
  the old KU's owner set `superseded_by` and status `Superseded`. Before concluding drift,
  confirm the *decision itself* changed — if the old guidance still holds for customers on
  the old version and both versions are in the field, consider instead scoping both KUs'
  Boundaries/version fields so they coexist, and linking them via `related`.
- **Same problem, different answer, both currently valid** (the choice depends on context,
  not version) → an *alternative*, not a duplicate. Both live; wire via `alternatives` and
  state the choosing criterion in each KU's Boundaries. Never recommend deleting either.
- **Partial overlap** (the new draft contains a piece an existing KU already owns) → carve
  that piece out of the draft and cite the existing KU via `related` instead of restating.
- **Adjacent decision** (upstream/downstream, same journey) → candidate for `related`.

Present the triage to the author as: existing ID → what overlaps → diagnosis → recommended
disposition. The author decides; supersession of someone else's KU is a recommendation for
that KU's owner, not something to enact unilaterally. Record the disposition in the
quality report.

### 2. Relationship harvest (against the KU corpus)
Find KUs covering the same products, the same source/target pairing, and the
upstream/downstream steps of the same engagement journey. Populate `related`,
`alternatives`, `migration_path` only with real IDs found — never invent IDs. Allocate the
new KU's ID per `references/naming-standard.md` (architecture area + deployment scope +
highest TOGAF layer gives the three-letter prefix; find the next free sequence number for
that exact prefix in the corpus); if the corpus is unreachable, leave `<PREFIX>-XXX` with
a note — a colliding ID is worse than a placeholder.

### 3. Corroboration and contradiction (against the fabric)
This is where the fabric shines even without a KU index:

- **Verify product claims**: search `help_pages` / `qlik_dev` (filter by `qlik_product`)
  for the draft's core mechanism. The KU should link these pages in `qlik_help_links`
  rather than restating them.
- **Corroborate field evidence**: search `case_information` and `sfdc_knowledge_articles`
  for the same failure mode or pattern. Support cases showing other customers hitting the
  same trap strengthen `confidence` and make excellent Anti-Pattern evidence.
- **Contradiction**: if the fabric shows current documentation or recent cases conflicting
  with the draft's position, surface it — the pattern may be stale, version-bound, or
  wrong. Never leave a silent conflict; resolve via Boundaries scoping, supersession, or
  correction.

### 4. Privacy hygiene
`case_information` chunks can carry customer-identifying details and `security_pii_flag:
true`. Use cases to *corroborate* a pattern; do not copy customer names, case numbers, or
identifying specifics into a KU. Cite as "confirmed by support case evidence" and put case
links (internal) in `related_assets` only if the team's conventions allow it.

## Build-from-scratch extra: fabric-assisted interrogation

After the author names the decision, retrieve the 2–3 closest existing KUs (corpus) and
the most relevant help/case content (fabric), and interview *against* them — "QDQ-001
already covers the baseline assessment; is your pattern the next step after it, or an
alternative?" This keeps new KUs positioned in the library rather than floating.

## Etiquette

- Read-only by default; never write/publish anywhere unless explicitly asked.
- Cite findings by KU ID or URL in the quality report so the author can verify.
- Keep queries few and cheap: small `size`, modest `truncate_length`, title + tags +
  question phrasings is normally enough. Don't trawl.
