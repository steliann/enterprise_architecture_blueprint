#!/usr/bin/env python3
"""
Validate an Architecture Blueprint customer-facing Markdown report.

Checks:
- YAML frontmatter presence and parsing
- required frontmatter keys
- allowed status
- required section headings and order
- report version represented in change_log and Appendix B
- common meta-document phrasing warnings
- assessment/gap-analysis headings warnings

Exit codes:
  0 = no errors
  1 = one or more errors
  2 = invocation/dependency problem
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(2)

REQUIRED_KEYS = [
    "artifact.type",
    "artifact.schema_version",
    "artifact.report_version",
    "title",
    "subtitle",
    "customer.name",
    "status",
    "dates.created",
    "dates.last_updated",
    "ownership.owner",
    "source_blueprint.artifact",
    "source_blueprint.version",
    "information_basis",
    "report_purpose",
    "change_log",
]

ALLOWED_STATUS = {"draft", "review", "validated", "published", "superseded"}

REQUIRED_SECTIONS = [
    "1. Purpose and Scope",
    "2. Executive Architecture Summary",
    "3. Business Outcomes and Use Cases",
    "4. Architecture Overview",
    "5. Data and Integration Landscape",
    "6. Data Products and Consumption",
    "7. Principal Architecture Choices",
    "8. Data Quality, Trust and Governance",
    "9. Operations and Resilience",
    "10. Architecture Evolution and Current Transitions",
    "11. Points to Validate",
    "12. Architecture Baseline Conclusion",
    "Appendix B — Document History",
]

META_OPENERS = [
    "This chapter describes",
    "This chapter presents",
    "This chapter explains",
    "This section describes",
    "This section presents",
    "The purpose of this chapter",
]

ASSESSMENT_HEADINGS = [
    "Gap Analysis",
    "Recommendations",
    "Architecture Gaps",
]

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def get_path(data, dotted):
    cur = data
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None, False
        cur = cur[part]
    return cur, True


def parse_frontmatter(text: str):
    if not text.startswith("---\n"):
        raise ValueError("Markdown must start with YAML frontmatter delimited by ---")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("Closing YAML frontmatter delimiter (---) not found")
    raw = text[4:end]
    body = text[end + 4:]
    data = yaml.safe_load(raw)
    if not isinstance(data, dict):
        raise ValueError("YAML frontmatter must parse to a mapping/object")
    return data, body


def section_positions(body: str):
    positions = {}
    for m in re.finditer(r"^(#{1,2})\s+(.+?)\s*$", body, re.MULTILINE):
        title = m.group(2).strip()
        positions.setdefault(title, m.start())
    return positions


def add(items, level, message):
    items.append({"level": level, "message": message})


def validate(path: Path):
    issues = []
    text = path.read_text(encoding="utf-8")

    try:
        fm, body = parse_frontmatter(text)
    except Exception as e:
        add(issues, "ERROR", str(e))
        return issues

    for key in REQUIRED_KEYS:
        value, ok = get_path(fm, key)
        if not ok or value is None or value == "" or value == []:
            add(issues, "ERROR", f"Missing or empty required frontmatter field: {key}")

    artifact_type, ok = get_path(fm, "artifact.type")
    if ok and artifact_type != "architecture-blueprint-report":
        add(issues, "ERROR", "artifact.type must be 'architecture-blueprint-report'")

    status, ok = get_path(fm, "status")
    if ok and status not in ALLOWED_STATUS:
        add(issues, "ERROR", f"status '{status}' is not one of {sorted(ALLOWED_STATUS)}")

    for date_key in ("dates.created", "dates.last_updated", "dates.validated_with_customer"):
        value, ok = get_path(fm, date_key)
        if ok and value not in (None, ""):
            if hasattr(value, "isoformat"):
                value = value.isoformat()
            if not isinstance(value, str) or not DATE_RE.match(value):
                add(issues, "WARNING", f"{date_key} should use YYYY-MM-DD or null")

    report_version, version_ok = get_path(fm, "artifact.report_version")
    change_log, log_ok = get_path(fm, "change_log")
    if version_ok and log_ok and isinstance(change_log, list):
        versions = {str(x.get("version")) for x in change_log if isinstance(x, dict)}
        if str(report_version) not in versions:
            add(issues, "ERROR", f"Current report_version {report_version} is missing from YAML change_log")

    positions = section_positions(body)
    last = -1
    for section in REQUIRED_SECTIONS:
        if section not in positions:
            add(issues, "ERROR", f"Missing required section heading: {section}")
        else:
            if positions[section] < last:
                add(issues, "ERROR", f"Section is out of order: {section}")
            last = positions[section]

    # Current version should appear in the visible document history.
    if version_ok and "Appendix B — Document History" in positions:
        appendix = body[positions["Appendix B — Document History"]:]
        if not re.search(rf"\|\s*{re.escape(str(report_version))}\s*\|", appendix):
            add(issues, "ERROR", f"Current report_version {report_version} is missing from Appendix B document history")

    # Style warnings.
    for phrase in META_OPENERS:
        if phrase.lower() in body.lower():
            add(issues, "WARNING", f"Meta-document phrasing found: '{phrase}'. Prefer direct architecture narrative.")

    for heading in ASSESSMENT_HEADINGS:
        pattern = re.compile(rf"^#{{1,3}}\s+.*{re.escape(heading)}.*$", re.IGNORECASE | re.MULTILINE)
        if pattern.search(body):
            add(issues, "WARNING", f"Assessment heading found in architecture baseline: '{heading}'")

    # Heading-specific opener check: first 500 chars after sections 3-12.
    for section in REQUIRED_SECTIONS[2:12]:
        if section not in positions:
            continue
        start = positions[section]
        next_positions = [p for p in positions.values() if p > start]
        end = min(next_positions) if next_positions else len(body)
        chunk = body[start:end][:800]
        for phrase in META_OPENERS:
            if phrase.lower() in chunk.lower():
                add(issues, "WARNING", f"Section '{section}' opens with meta-document phrasing.")

    # Basic placeholder warning.
    if re.search(r"<[^>\n]{2,80}>", body):
        add(issues, "WARNING", "Template-style angle-bracket placeholders appear to remain in the report.")

    return issues


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    if not args.report.exists():
        print(f"ERROR: file not found: {args.report}", file=sys.stderr)
        return 2

    issues = validate(args.report)
    errors = sum(1 for i in issues if i["level"] == "ERROR")
    warnings = sum(1 for i in issues if i["level"] == "WARNING")

    if args.json:
        print(json.dumps({
            "file": str(args.report),
            "errors": errors,
            "warnings": warnings,
            "issues": issues
        }, indent=2))
    else:
        for i in issues:
            print(f"{i['level']}: {i['message']}")
        if not issues:
            print("PASS: report structure and frontmatter validation succeeded.")
        else:
            print(f"\nSummary: {errors} error(s), {warnings} warning(s).")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
