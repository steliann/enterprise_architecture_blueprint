#!/usr/bin/env python3
"""Validate Architecture Decision Record Markdown files.

Checks, in order:
  1. YAML front matter exists and parses.
  2. Frontmatter shape: required fields, enums, ID format, nesting, placeholders.
  3. House quoting rule: title, decision_owner, decision_type, supersedes,
     superseded_by, and the non-null items of contributors, technology_scope's
     qlik/talend/third_party, related_patterns, related_adrs,
     impacted_architecture_views, related_assets, and tags must be quoted in
     the YAML source.
  4. Optional JSON Schema conformance (--schema).
  5. Lifecycle, date, relationship, and AI-provenance consistency.
  6. Required Markdown sections, canonical order, no duplicates.
  7. Required subsection structure (Options, Architecture Impact, Consequences, KU Alignment).
  8. Decision-quality rules and density heuristics.
  9. Naming standard: id / H1 / filename three-way alignment.

Dependencies: pyyaml (required), jsonschema (only when --schema is used).
    pip install pyyaml jsonschema

Usage:
    python3 validate_adr.py ADR.md [MORE.md ...]
    python3 validate_adr.py ADR.md --schema architecture-decision-record.schema.json
    python3 validate_adr.py decision-records/*.md --json
    python3 validate_adr.py decision-records/*.md --corpus

Exit codes: 0 clean, 1 warnings only, 2 errors.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    print("Missing dependency. Install with: pip install pyyaml", file=sys.stderr)
    raise SystemExit(2) from exc


# ---------------------------------------------------------------- contract

REQUIRED_SECTIONS = [
    "Context",
    "Decision",
    "Decision Drivers",
    "Options Considered",
    "Decision Outcome",
    "Architecture Impact",
    "Consequences",
    "Implementation Implications",
    "Operational Implications",
    "Risks and Mitigations",
    "Review Triggers",
    "Open Questions",
]

# Optional sections, mapped to the required section they must precede.
OPTIONAL_SECTIONS = {"Knowledge Unit Alignment": "Architecture Impact"}

ARCHITECTURE_IMPACT_SUBSECTIONS = ["Business", "Data", "Application", "Technology"]
CONSEQUENCES_SUBSECTIONS = ["Positive Consequences", "Negative Consequences / Trade-offs"]
OPTION_LABELS = ["Benefits", "Limitations", "Fit assessment"]
KU_ALIGNMENT_SUBSECTIONS = [
    "Supporting Knowledge Units",
    "Conditional Support and Constraints",
    "Contradictions or Exceptions",
    "Alignment Outcome",
]

REQUIRED_FIELDS = [
    "id",
    "yaml_version",
    "title",
    "status",
    "date",
    "decision_owner",
    "decision_type",
    "architecture_domain",
    "decision_scope",
    "decision_level",
    "confidence",
    "technology_scope",
    "used_ai_to_prepare",
]

ENUMS = {
    "status": {"Draft", "Proposed", "Accepted", "Superseded", "Deprecated"},
    "architecture_domain": {
        "Data", "Application", "Integration", "Security",
        "Platform", "Operations", "Governance", "Other",
    },
    "decision_scope": {
        "Customer", "Product Platform", "Program", "Enterprise", "Reference Architecture",
    },
    "decision_level": {"Strategic", "Tactical", "Operational"},
    "confidence": {"High", "Medium", "Low"},
}

LIST_FIELDS = [
    "contributors",
    "related_patterns",
    "related_adrs",
    "impacted_architecture_views",
    "related_assets",
    "ai_solutions_used",
    "tags",
]

TECH_SCOPE_KEYS = ["qlik", "talend", "third_party"]

# House style: these scalar fields must be a quoted string in the YAML *source*
# whenever they carry a value, even when YAML would parse them fine unquoted.
# This is checked against raw text, not the parsed dict - yaml.safe_load throws
# the quoting away once it parses successfully either way.
SCALAR_QUOTED_FIELDS = ["title", "decision_owner", "decision_type", "supersedes", "superseded_by"]

# Same rule for every non-null item in these list fields.
LIST_QUOTED_FIELDS = [
    "contributors",
    "related_patterns",
    "related_adrs",
    "impacted_architecture_views",
    "related_assets",
    "tags",
]

# Same rule for the three nested technology_scope lists specifically.
TECH_SCOPE_QUOTED_KEYS = ["qlik", "talend", "third_party"]

QUOTED_VALUE_RE = re.compile(r"^(\".*\"|'.*')$")

ID_RE = re.compile(r"^(?:[A-Z][A-Z0-9]{1,9}-)?ADR-(\d{3}|XXX)$")
BULLET_RE = re.compile(r"^\s*[-*]\s+\S", re.MULTILINE)
RISK_RE = re.compile(r"^\s*[-*]\s+Risk:\s+\S.*?\.\s*Mitigation:\s+\S", re.MULTILINE)
OPTION_HEADING_RE = re.compile(r"^Option\s+\d+\s+[—-]\s+\S")
PLACEHOLDER_RE = re.compile(r"(<[A-Za-z][^>]*>|\[(?:Name|Owner|Asset|title|ADR)[^\]]*\]|TODO|TBD|FIXME|XXX)")
ALIGNMENT_OUTCOMES = (
    "aligned",
    "conditionally aligned",
    "misaligned",
    "requires a governance exception",
    "requires governance exception",
)

# Section density targets: (min_bullets, max_bullets_soft)
DENSITY = {
    "Decision Drivers": (5, 8),
    "Implementation Implications": (6, 10),
    "Operational Implications": (5, 8),
    "Risks and Mitigations": (4, 8),
    "Review Triggers": (5, 8),
}
CONSEQUENCE_DENSITY = (5, 8)


# ---------------------------------------------------------------- helpers


class Report:
    def __init__(self, path: Path):
        self.path = path
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    @property
    def ok(self) -> bool:
        return not self.errors and not self.warnings

    def as_dict(self) -> dict:
        return {
            "file": str(self.path),
            "errors": self.errors,
            "warnings": self.warnings,
            "status": "error" if self.errors else ("warning" if self.warnings else "ok"),
        }

    def render(self) -> str:
        lines = [f"== {self.path}"]
        for msg in self.errors:
            lines.append(f"  ERROR   {msg}")
        for msg in self.warnings:
            lines.append(f"  WARNING {msg}")
        if self.ok:
            lines.append("  OK: Architecture Decision Record is valid.")
        return "\n".join(lines)


def split_front_matter(text: str) -> tuple[str, str]:
    if not re.match(r"^---\r?\n", text):
        raise ValueError("File must start with YAML front matter delimited by ---")
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?(.*)$", text, flags=re.DOTALL)
    if not match:
        raise ValueError("Could not find closing --- for YAML front matter")
    return match.group(1), match.group(2)


def h2_headings(body: str) -> list[str]:
    return [h.strip() for h in re.findall(r"^##\s+(.+?)\s*$", body, flags=re.MULTILINE)]


def h3_headings(text: str) -> list[str]:
    return [h.strip() for h in re.findall(r"^###\s+(.+?)\s*$", text, flags=re.MULTILINE)]


def section(body: str, name: str) -> str:
    pattern = rf"^##\s+{re.escape(name)}\s*$([\s\S]*?)(?=^##\s+|\Z)"
    match = re.search(pattern, body, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def subsection(parent: str, name: str) -> str:
    pattern = rf"^###\s+{re.escape(name)}\s*$([\s\S]*?)(?=^###\s+|\Z)"
    match = re.search(pattern, parent, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def strip_comments(text: str) -> str:
    return re.sub(r"<!--[\s\S]*?-->", "", text)


def count_bullets(text: str) -> int:
    return len(BULLET_RE.findall(strip_comments(text)))


def prose_words(text: str) -> int:
    cleaned = strip_comments(text)
    cleaned = re.sub(r"^#{1,6}\s+.*$", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"`{1,3}[^`]*`{1,3}", "", cleaned)
    return len(cleaned.split())


def first_line(text: str) -> str:
    for line in strip_comments(text).splitlines():
        if line.strip():
            return line.strip()
    return ""


def parse_iso(value: object, field: str, rep: Report) -> date | None:
    if value is None:
        return None
    if isinstance(value, date):
        return value
    if not isinstance(value, str):
        rep.error(f"{field} must be a YYYY-MM-DD string or null")
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        rep.error(f"{field} must use YYYY-MM-DD format, got: {value!r}")
        return None


def kebab(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower())
    return slug.strip("-")


# ---------------------------------------------------------------- frontmatter


def _strip_inline_comment(line: str) -> str:
    """Drop a trailing ' # comment', but only outside an open quote, so a '#'
    inside a quoted value (rare, but legal YAML) doesn't truncate the value."""
    out = []
    in_quotes = False
    quote_char = ""
    for ch in line:
        if in_quotes:
            out.append(ch)
            if ch == quote_char:
                in_quotes = False
            continue
        if ch in "\"'":
            in_quotes = True
            quote_char = ch
            out.append(ch)
            continue
        if ch == "#":
            break
        out.append(ch)
    return "".join(out)


def check_quoting(fm_raw: str, rep: Report) -> None:
    """Enforce the house quoting rule against the raw YAML text.

    Scoped to the skill's own controlled frontmatter shape: top-level scalar
    fields at column 0, technology_scope's three children indented two
    spaces under it, and list items introduced with '-' at any indentation.
    A field set to null, or left empty pending fill-in, is exempt - there's
    nothing to quote yet, and that gap is already reported elsewhere."""

    current_field: str | None = None
    current_subfield: str | None = None

    for raw_line in fm_raw.splitlines():
        line = _strip_inline_comment(raw_line).rstrip()
        if not line.strip():
            continue

        top_match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if top_match:
            current_field, current_subfield = top_match.group(1), None
            value = top_match.group(2).strip()
            if current_field in SCALAR_QUOTED_FIELDS and value and value != "null":
                if not QUOTED_VALUE_RE.match(value):
                    rep.error(
                        f"{current_field} must be a quoted string in the YAML source "
                        f'(e.g. {current_field}: "{value}") - got unquoted: {value!r}'
                    )
            continue

        sub_match = re.match(r"^\s{2}([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if sub_match and current_field == "technology_scope":
            current_subfield = sub_match.group(1)
            continue

        item_match = re.match(r"^\s*-\s+(.*)$", line)
        if item_match:
            value = item_match.group(1).strip()
            if not value or value == "null":
                continue
            if current_field == "technology_scope" and current_subfield in TECH_SCOPE_QUOTED_KEYS:
                if not QUOTED_VALUE_RE.match(value):
                    rep.error(
                        f"technology_scope.{current_subfield} items must be quoted in the "
                        f'YAML source (e.g. - "{value}") - got unquoted: {value!r}'
                    )
            elif current_field in LIST_QUOTED_FIELDS:
                if not QUOTED_VALUE_RE.match(value):
                    rep.error(
                        f"{current_field} items must be quoted in the YAML source "
                        f'(e.g. - "{value}") - got unquoted: {value!r}'
                    )
            continue


def check_frontmatter(meta: dict, rep: Report) -> None:
    for field in REQUIRED_FIELDS:
        if field not in meta:
            rep.error(f"Missing required frontmatter field: {field}")
        elif meta[field] is None:
            rep.error(f"Required frontmatter field is null: {field}")

    # Common YAML-nesting failure: technology_scope children flattened to top level.
    flattened = [k for k in TECH_SCOPE_KEYS if k in meta]
    if flattened:
        rep.error(
            f"technology_scope children found as top-level keys ({', '.join(flattened)}) - "
            "indentation was lost; nest them under technology_scope"
        )

    scope = meta.get("technology_scope")
    if scope is not None:
        if not isinstance(scope, dict):
            rep.error("technology_scope must be a mapping with qlik, talend, third_party")
        else:
            for key in TECH_SCOPE_KEYS:
                if key not in scope:
                    rep.error(f"technology_scope is missing required key: {key}")
                elif scope[key] is not None and not isinstance(scope[key], list):
                    rep.error(f"technology_scope.{key} must be a list or null")
            for key in scope:
                if key not in TECH_SCOPE_KEYS:
                    rep.warn(f"Unexpected technology_scope key: {key}")
            if all(not scope.get(k) for k in TECH_SCOPE_KEYS):
                rep.warn("technology_scope lists no products at all - is that right?")

    if meta.get("yaml_version") != 1:
        rep.error(f"yaml_version must be 1, got: {meta.get('yaml_version')!r}")

    if meta.get("decision_type") != "Architecture":
        rep.error(f"decision_type must be 'Architecture', got: {meta.get('decision_type')!r}")

    for field, allowed in ENUMS.items():
        value = meta.get(field)
        if value is not None and value not in allowed:
            rep.error(f"{field} must be one of {sorted(allowed)}, got: {value!r}")

    adr_id = meta.get("id")
    if isinstance(adr_id, str):
        if not ID_RE.match(adr_id):
            rep.error(
                f"id must match ADR-NNN or SCOPE-ADR-NNN with a three-digit sequence, got: {adr_id!r}"
            )
        elif adr_id.endswith("-XXX"):
            rep.warn(f"id {adr_id} is a placeholder - allocate the real sequence number before commit")
    elif adr_id is not None:
        rep.error("id must be a string")

    title = meta.get("title")
    if isinstance(title, str):
        if PLACEHOLDER_RE.search(title):
            rep.error(f"title still contains a placeholder: {title!r}")
        elif len(title.split()) < 4:
            rep.warn(f"title looks like a topic rather than a decision: {title!r}")

    owner = meta.get("decision_owner")
    if isinstance(owner, str) and PLACEHOLDER_RE.search(owner):
        rep.error(f"decision_owner is still a placeholder: {owner!r}")

    for field in LIST_FIELDS:
        value = meta.get(field)
        if value is None:
            continue
        if not isinstance(value, list):
            rep.error(f"{field} must be a list or null, got {type(value).__name__}")
            continue
        if not value:
            rep.error(f"{field} is an empty list - use null instead")
            continue
        for item in value:
            if isinstance(item, str) and (not item.strip() or PLACEHOLDER_RE.search(item)):
                rep.error(f"{field} contains an unfilled placeholder entry: {item!r}")
        seen = [v for v in value if isinstance(v, str)]
        for dup in sorted({v for v in seen if seen.count(v) > 1}):
            rep.error(f"Duplicate {field} entry: {dup}")

    tags = meta.get("tags")
    if isinstance(tags, list):
        for tag in tags:
            if isinstance(tag, str) and tag.strip() and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", tag):
                rep.warn(f"tag should be lowercase and hyphenated: {tag!r}")


def check_lifecycle(meta: dict, rep: Report) -> None:
    status = meta.get("status")
    superseded_by = meta.get("superseded_by")
    supersedes = meta.get("supersedes")
    adr_id = meta.get("id")

    if status == "Superseded" and not superseded_by:
        rep.error("status Superseded requires superseded_by to reference the replacement ADR")
    if status != "Superseded" and superseded_by:
        rep.warn("superseded_by is normally null unless status is Superseded")
    if status == "Accepted" and meta.get("confidence") == "Low":
        rep.error("status Accepted must not carry confidence Low")

    own_id = adr_id if isinstance(adr_id, str) else None

    for field, value in (("supersedes", supersedes), ("superseded_by", superseded_by)):
        if isinstance(value, str):
            if own_id and value == own_id:
                rep.error(f"{field} must not reference this ADR's own id ({own_id})")
            elif not ID_RE.match(value):
                rep.error(f"{field} must be a valid ADR id or null, got: {value!r}")

    related = meta.get("related_adrs")
    if isinstance(related, list):
        for item in related:
            if own_id and item == own_id:
                rep.error(f"related_adrs must not contain this ADR's own id ({own_id})")
            elif isinstance(item, str) and not ID_RE.match(item):
                rep.warn(f"related_adrs entry does not look like an ADR id: {item!r}")
        if isinstance(superseded_by, str) and superseded_by in related:
            rep.warn(f"{superseded_by} appears in both related_adrs and superseded_by")

    decision_date = parse_iso(meta.get("date"), "date", rep)
    review_by = parse_iso(meta.get("review_by"), "review_by", rep)
    if decision_date and review_by and review_by <= decision_date:
        rep.error("review_by must be later than date")
    if status in {"Accepted", "Proposed"} and review_by is None:
        rep.warn(f"status {status} with review_by null - the decision has no review horizon")
    if review_by and review_by < date.today() and status == "Accepted":
        rep.warn(f"review_by {review_by.isoformat()} has passed on an Accepted ADR - due for review")

    used_ai = meta.get("used_ai_to_prepare")
    solutions = meta.get("ai_solutions_used")
    if used_ai is False and solutions is not None:
        rep.error("ai_solutions_used must be null when used_ai_to_prepare is false")
    if used_ai is True and not (isinstance(solutions, list) and solutions):
        rep.error("ai_solutions_used must be a non-empty list when used_ai_to_prepare is true")

    patterns = meta.get("related_patterns")
    if isinstance(patterns, list):
        for item in patterns:
            if isinstance(item, str) and not re.search(r"[A-Z]{2,8}[-_]\d{3}", item):
                rep.warn(f"related_patterns entry does not clearly identify a KU id: {item!r}")


# ---------------------------------------------------------------- sections


def check_sections(body: str, rep: Report) -> None:
    headings = h2_headings(body)
    present = set(headings)

    for name in REQUIRED_SECTIONS:
        if name not in present:
            rep.error(f"Missing required section: ## {name}")

    for dup in sorted({h for h in headings if headings.count(h) > 1}):
        rep.error(f"Duplicate H2 section: ## {dup}")

    allowed = set(REQUIRED_SECTIONS) | set(OPTIONAL_SECTIONS)
    for heading in headings:
        if heading not in allowed:
            rep.warn(f"Non-standard H2 section: ## {heading}")

    expected = REQUIRED_SECTIONS.copy()
    for optional, precedes in OPTIONAL_SECTIONS.items():
        if optional in present:
            expected.insert(expected.index(precedes), optional)
    found = [h for h in headings if h in expected]
    wanted = [h for h in expected if h in found]
    if found != wanted:
        rep.error(f"H2 sections are out of canonical order. Found {found}, expected {wanted}")

    if not re.search(r"^#\s+\S", body, flags=re.MULTILINE):
        rep.error("Missing H1 title line (# <ID> — <Title>)")


def check_subsections(body: str, rep: Report) -> None:
    impact = section(body, "Architecture Impact")
    if impact:
        found = h3_headings(impact)
        for name in ARCHITECTURE_IMPACT_SUBSECTIONS:
            if name not in found:
                rep.error(f"Missing Architecture Impact subsection: ### {name}")
            elif prose_words(subsection(impact, name)) < 15:
                rep.warn(f"Architecture Impact / {name} is too thin to be meaningful")

    consequences = section(body, "Consequences")
    if consequences:
        found = h3_headings(consequences)
        for name in CONSEQUENCES_SUBSECTIONS:
            if name not in found:
                rep.error(f"Missing Consequences subsection: ### {name}")
                continue
            count = count_bullets(subsection(consequences, name))
            low, high = CONSEQUENCE_DENSITY
            if count == 0:
                rep.error(f"Consequences / {name} has no bullets")
            elif count < low:
                rep.warn(f"Consequences / {name} has {count} bullets, target {low}-{high}")
            elif count > high:
                rep.warn(f"Consequences / {name} has {count} bullets, target {low}-{high}")

    options = section(body, "Options Considered")
    if options:
        option_headings = [h for h in h3_headings(options) if OPTION_HEADING_RE.match(h)]
        other = [h for h in h3_headings(options) if not OPTION_HEADING_RE.match(h)]
        for heading in other:
            rep.warn(f"Options Considered subsection is not '### Option N — Name': ### {heading}")
        if len(option_headings) < 2:
            rep.error(
                f"Options Considered needs at least two '### Option N — Name' subsections, found {len(option_headings)}"
            )
        numbers = [int(re.match(r"^Option\s+(\d+)", h).group(1)) for h in option_headings]
        if numbers and numbers != list(range(1, len(numbers) + 1)):
            rep.warn(f"Option numbers are not sequential from 1: {numbers}")
        for heading in option_headings:
            text = subsection(options, heading)
            for label in OPTION_LABELS:
                if not re.search(rf"^\*\*{re.escape(label)}\*\*", text, flags=re.MULTILINE):
                    rep.error(f"{heading} is missing **{label}**")
            for label in ("Benefits", "Limitations"):
                block = re.search(
                    rf"^\*\*{label}\*\*\s*$([\s\S]*?)(?=^\*\*|\Z)", text, flags=re.MULTILINE
                )
                if block and count_bullets(block.group(1)) == 0:
                    rep.error(f"{heading} / {label} has no bullets")
            fit = re.search(r"^\*\*Fit assessment\*\*\s*$([\s\S]*?)(?=^\*\*|\Z)", text, flags=re.MULTILINE)
            if fit and prose_words(fit.group(1)) < 8:
                rep.warn(f"{heading} / Fit assessment is too thin to justify the disposition")

    ku = section(body, "Knowledge Unit Alignment")
    if ku:
        found = h3_headings(ku)
        if "Alignment Outcome" not in found:
            rep.error("Knowledge Unit Alignment must include ### Alignment Outcome")
        for name in KU_ALIGNMENT_SUBSECTIONS:
            if name not in found:
                rep.warn(f"Knowledge Unit Alignment is missing ### {name}")
        outcome = subsection(ku, "Alignment Outcome").lower()
        if outcome and not any(o in outcome for o in ALIGNMENT_OUTCOMES):
            rep.warn(
                "Alignment Outcome should state aligned, conditionally aligned, misaligned, "
                "or requires a governance exception"
            )
        # A contradiction is only "recorded" when the outcome says so. Prose in the
        # Contradictions subsection is often an explicit "no contradiction" statement.
        contradiction_recorded = any(
            o in outcome for o in ("misaligned", "requires a governance exception", "requires governance exception")
        )
        if contradiction_recorded:
            for target in ("Risks and Mitigations", "Review Triggers", "Open Questions"):
                text = section(body, target)
                if "Knowledge Unit" not in text and "KU" not in text:
                    rep.warn(
                        f"Alignment Outcome records a KU contradiction but {target} does not mention KU alignment"
                    )
        contradictions = subsection(ku, "Contradictions or Exceptions")
        if not contradictions:
            rep.warn("Knowledge Unit Alignment / Contradictions or Exceptions is empty - state 'no contradiction' explicitly")


def check_quality(body: str, rep: Report) -> None:
    decision = section(body, "Decision")
    if decision:
        opening = first_line(decision)
        if not opening.startswith("We will"):
            rep.error("Decision section must open with a sentence starting 'We will'")
        words = prose_words(decision)
        if words < 25:
            rep.warn(f"Decision section is {words} words - probably not explicit enough to review")
        if words > 220:
            rep.warn(f"Decision section is {words} words - it may be carrying rationale that belongs in Decision Outcome")
        if re.search(r"^###\s", decision, flags=re.MULTILINE):
            rep.warn("Decision section has subsections - it should be one paragraph")

    outcome = section(body, "Decision Outcome")
    if outcome:
        match = re.search(r"Selected option:\s*Option\s+(\d+)\s+[—-]\s+(\S.*)", outcome)
        if not match:
            rep.error("Decision Outcome must open with 'Selected option: Option N — <name>.'")
        else:
            chosen = int(match.group(1))
            options = section(body, "Options Considered")
            numbers = [
                int(re.match(r"^Option\s+(\d+)", h).group(1))
                for h in h3_headings(options)
                if OPTION_HEADING_RE.match(h)
            ]
            if numbers and chosen not in numbers:
                rep.error(
                    f"Decision Outcome selects Option {chosen}, which is not in Options Considered {numbers}"
                )

    context = section(body, "Context")
    if context:
        paragraphs = [p for p in re.split(r"\n\s*\n", strip_comments(context).strip()) if p.strip()]
        if len(paragraphs) < 2:
            rep.warn(f"Context has {len(paragraphs)} paragraph(s), target 2-4")
        elif len(paragraphs) > 4:
            rep.warn(f"Context has {len(paragraphs)} paragraphs, target 2-4")

    for name, (low, high) in DENSITY.items():
        text = section(body, name)
        if not text:
            continue
        count = count_bullets(text)
        if count == 0:
            rep.error(f"{name} has no bullets")
        elif count < low:
            rep.warn(f"{name} has {count} bullets, target {low}-{high}")
        elif count > high:
            rep.warn(f"{name} has {count} bullets, target {low}-{high}")

    risks = section(body, "Risks and Mitigations")
    if risks:
        matched = len(RISK_RE.findall(strip_comments(risks)))
        total = count_bullets(risks)
        if matched == 0:
            rep.error("Risks and Mitigations must use the form '- Risk: <risk>. Mitigation: <mitigation>.'")
        elif matched < total:
            rep.warn(f"{total - matched} of {total} risk bullets do not use the Risk/Mitigation form")

    triggers = section(body, "Review Triggers")
    if triggers and not re.search(r"Review this ADR if:", triggers):
        rep.warn("Review Triggers should open with 'Review this ADR if:'")

    open_q = section(body, "Open Questions")
    if open_q:
        cleaned = strip_comments(open_q).strip()
        none_stated = "No open questions at the time of this ADR" in cleaned
        if not none_stated and count_bullets(open_q) == 0:
            rep.error(
                "Open Questions must list 3-8 bullets or state 'No open questions at the time of this ADR.'"
            )

    body_clean = strip_comments(body)
    if PLACEHOLDER_RE.search(body_clean):
        found = sorted({m.group(0) for m in PLACEHOLDER_RE.finditer(body_clean)})[:5]
        rep.error(f"Body still contains unfilled placeholders: {', '.join(found)}")

    words = prose_words(body)
    if words > 3200:
        rep.warn(
            f"Body is ~{words} words - beyond a three-to-five-minute read; check for multiple decisions"
        )
    elif words < 500:
        rep.warn(f"Body is ~{words} words - likely too thin to justify the decision")

    if re.search(r"^\s*\d+\.\s+(Open|Click|Navigate|Select|Go to|In the .* menu)", body, flags=re.MULTILINE):
        rep.warn("Body contains numbered UI steps - an ADR is not a product tutorial")


def check_naming(path: Path, meta: dict, body: str, rep: Report) -> None:
    adr_id = meta.get("id")
    if not isinstance(adr_id, str):
        return

    h1 = re.search(r"^#\s+(.+?)\s*$", body, flags=re.MULTILINE)
    if h1:
        heading = h1.group(1).strip()
        if not heading.startswith(adr_id):
            rep.error(f"H1 must start with the ADR id {adr_id}, got: {heading!r}")
        elif not re.match(rf"^{re.escape(adr_id)}\s+—\s+\S", heading):
            rep.warn(f"H1 should read '{adr_id} — <Title>' with an em dash, got: {heading!r}")
        title = meta.get("title")
        if isinstance(title, str) and title and title not in heading:
            rep.warn("H1 title text does not match the frontmatter title")

    stem = path.stem
    if stem != stem.lower():
        rep.error(f"Filename must be lowercase: {path.name}")
    if "_" in stem:
        rep.error(f"Filename must use hyphens, not underscores: {path.name}")
    if not stem.startswith(adr_id.lower()):
        rep.error(f"Filename must start with the lowercase ADR id ({adr_id.lower()}): {path.name}")
    for token in ("draft", "proposed", "accepted", "superseded", "deprecated", "final"):
        if re.search(rf"(?:^|-){token}(?:-|$)", stem):
            rep.error(f"Filename must not encode status ('{token}'): {path.name}")
    if re.search(r"\d{4}-\d{2}-\d{2}", stem):
        rep.warn(f"Filename encodes a date - keep dates in YAML unless materially part of the decision: {path.name}")
    if path.parent.name and path.parent.name != "decision-records":
        rep.warn(f"ADRs belong in decision-records/, found in {path.parent.name}/")

    title = meta.get("title")
    if isinstance(title, str) and title:
        slug_part = stem[len(adr_id.lower()):].lstrip("-")
        if slug_part:
            title_tokens = set(kebab(title).split("-"))
            slug_tokens = [t for t in slug_part.split("-") if t]
            overlap = sum(1 for t in slug_tokens if t in title_tokens)
            if slug_tokens and overlap / len(slug_tokens) < 0.5:
                rep.warn("Filename title portion does not resemble the ADR title")
        else:
            rep.warn(f"Filename has no title portion after the ADR id: {path.name}")


def json_safe(value):
    """PyYAML turns unquoted ISO dates into date objects, which no JSON Schema
    'string' rule can match. Normalize before validating."""
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [json_safe(v) for v in value]
    return value


def check_schema(meta: dict, schema_path: Path, rep: Report) -> None:
    try:
        from jsonschema import Draft7Validator, FormatChecker
    except ImportError:
        rep.warn("--schema given but jsonschema is not installed; skipped (pip install jsonschema)")
        return
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        rep.warn(f"Could not load schema {schema_path}: {exc}")
        return
    validator = Draft7Validator(schema, format_checker=FormatChecker())
    for err in sorted(validator.iter_errors(json_safe(meta)), key=lambda e: list(e.path)):
        where = ".".join(str(p) for p in err.path) or "<root>"
        rep.error(f"Schema violation at {where}: {err.message}")


# ---------------------------------------------------------------- corpus


def check_corpus(records: list[tuple[Path, dict]]) -> list[str]:
    findings: list[str] = []
    by_id: dict[str, list[Path]] = {}
    for path, meta in records:
        adr_id = meta.get("id")
        if isinstance(adr_id, str):
            by_id.setdefault(adr_id, []).append(path)

    for adr_id, paths in sorted(by_id.items()):
        if len(paths) > 1:
            names = ", ".join(p.name for p in paths)
            findings.append(f"ERROR   ID collision: {adr_id} used by {names}")

    known = set(by_id)
    for path, meta in records:
        adr_id = meta.get("id")
        refs = []
        for field in ("supersedes", "superseded_by"):
            value = meta.get(field)
            if isinstance(value, str):
                refs.append((field, value))
        related = meta.get("related_adrs")
        if isinstance(related, list):
            refs += [("related_adrs", v) for v in related if isinstance(v, str)]
        for field, target in refs:
            if target not in known:
                findings.append(f"WARNING {path.name}: {field} references {target}, not present in this set")

        superseded_by = meta.get("superseded_by")
        if isinstance(superseded_by, str) and superseded_by in known:
            replacement = next(m for p, m in records if m.get("id") == superseded_by)
            if replacement.get("supersedes") != adr_id:
                findings.append(
                    f"ERROR   One-way supersession: {adr_id} points to {superseded_by}, "
                    f"which does not declare supersedes: {adr_id}"
                )

    prefixes: dict[str, list[int]] = {}
    for adr_id in known:
        match = re.match(r"^(?:([A-Z][A-Z0-9]{1,9})-)?ADR-(\d{3})$", adr_id)
        if match:
            prefixes.setdefault(match.group(1) or "ADR", []).append(int(match.group(2)))
    for prefix, numbers in sorted(prefixes.items()):
        numbers.sort()
        gaps = [n for n in range(1, max(numbers) + 1) if n not in numbers]
        if gaps:
            findings.append(
                f"WARNING Scope {prefix}: sequence gaps at {gaps} - expected if numbers were retired, "
                "otherwise records are missing"
            )
    return findings


# ---------------------------------------------------------------- driver


def validate(path: Path, schema_path: Path | None) -> tuple[Report, dict | None]:
    rep = Report(path)
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        rep.error(f"Could not read file: {exc}")
        return rep, None

    try:
        fm_raw, body = split_front_matter(raw)
    except ValueError as exc:
        rep.error(str(exc))
        return rep, None

    try:
        meta = yaml.safe_load(fm_raw)
    except yaml.YAMLError as exc:
        detail = str(exc).replace("\n", " ")
        hint = ""
        if "alias" in detail:
            hint = " (a leading '*' is a YAML alias - use '-' for list bullets)"
        rep.error(f"Front matter is not valid YAML: {detail}{hint}")
        return rep, None

    if not isinstance(meta, dict):
        rep.error("Front matter must be a mapping")
        return rep, None

    check_frontmatter(meta, rep)
    check_quoting(fm_raw, rep)
    check_lifecycle(meta, rep)
    if schema_path:
        check_schema(meta, schema_path, rep)
    check_sections(body, rep)
    check_subsections(body, rep)
    check_quality(body, rep)
    check_naming(path, meta, body, rep)
    return rep, meta


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Architecture Decision Records.")
    parser.add_argument("paths", nargs="+", type=Path, help="ADR Markdown file(s)")
    parser.add_argument("--schema", type=Path, default=None, help="optional JSON Schema for frontmatter")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument("--corpus", action="store_true", help="also run cross-record corpus checks")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors in the exit code")
    args = parser.parse_args()

    if args.schema and not args.schema.exists():
        print(f"ERROR: schema not found: {args.schema}", file=sys.stderr)
        return 2

    reports: list[Report] = []
    records: list[tuple[Path, dict]] = []
    for path in args.paths:
        if not path.exists():
            rep = Report(path)
            rep.error("File not found")
            reports.append(rep)
            continue
        rep, meta = validate(path, args.schema)
        reports.append(rep)
        if meta is not None:
            records.append((path, meta))

    corpus_findings = check_corpus(records) if args.corpus and len(records) > 1 else []
    corpus_errors = sum(1 for f in corpus_findings if f.startswith("ERROR"))
    corpus_warnings = len(corpus_findings) - corpus_errors

    n_errors = sum(len(r.errors) for r in reports) + corpus_errors
    n_warnings = sum(len(r.warnings) for r in reports) + corpus_warnings

    if args.json:
        print(json.dumps({
            "files": [r.as_dict() for r in reports],
            "corpus": corpus_findings,
            "totals": {"errors": n_errors, "warnings": n_warnings, "files": len(reports)},
        }, indent=2))
    else:
        for rep in reports:
            print(rep.render())
        if corpus_findings:
            print("\n== corpus")
            for finding in corpus_findings:
                print(f"  {finding}")
        print()
        if n_errors:
            print(f"FAILED: {n_errors} error(s), {n_warnings} warning(s) across {len(reports)} file(s).")
        elif n_warnings:
            print(f"PASSED WITH WARNINGS: {n_warnings} warning(s) across {len(reports)} file(s).")
        else:
            print(f"OK: {len(reports)} file(s) valid.")

    if n_errors:
        return 2
    if n_warnings:
        return 2 if args.strict else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
