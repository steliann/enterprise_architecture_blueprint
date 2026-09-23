#!/usr/bin/env python3
"""Validate a canonical Architecture Assessment / Review Markdown OKF.

This validator is intentionally structural/editorial. Existing customer review
OKFs with a different established package structure should be validated against
their own schema while applying the content rules in SKILL.md.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(2)

REQUIRED_KEYS = [
    "artifact.type", "artifact.schema_version", "artifact.review_version",
    "title", "status", "dates.created", "dates.last_updated",
    "source_blueprint.artifact", "source_blueprint.version",
    "scope.assessment_lenses", "assessment_principle",
    "recommendation_principle", "benefit_model", "change_log",
]

REQUIRED_SECTIONS = [
    "1. Assessment Position",
    "2. Classification Model",
    "3. Executive Assessment",
    "4. Coverage Findings",
    "5. Validation Items / Design Topics",
    "6. Candidate and Active Gaps",
    "7. Recommendations",
    "8. Cross-Gap Architecture Themes",
    "10. Aggregated Architecture Conclusions",
    "11. Assessment Disposition",
]

COMMERCIAL_WARNINGS = [
    "Expanded Entitlement",
    "QTC-led target-state roadmap",
    "Impact if the Opportunity Is Not Evaluated",
]

PRODUCT_GAP_PATTERNS = [
    r"gap.{0,80}\bdoes not (use|have|adopt)\b.{0,50}\bQTC\b",
    r"gap.{0,80}\bmissing\b.{0,40}\bQTC\b",
]


def get_path(data, dotted):
    cur = data
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None, False
        cur = cur[part]
    return cur, True


def parse_frontmatter(text):
    if not text.startswith("---\n"):
        raise ValueError("Markdown must start with YAML frontmatter delimited by ---")
    end = text.find("\n---", 4)
    if end < 0:
        raise ValueError("Closing YAML frontmatter delimiter not found")
    data = yaml.safe_load(text[4:end])
    if not isinstance(data, dict):
        raise ValueError("YAML frontmatter must parse to a mapping/object")
    return data, text[end + 4:]


def headings(body):
    out = []
    for m in re.finditer(r"^(#{1,6})\s+(.+?)\s*$", body, re.MULTILINE):
        out.append((len(m.group(1)), m.group(2).strip(), m.start()))
    return out


def add(issues, level, msg):
    issues.append({"level": level, "message": msg})


def validate(path):
    issues = []
    text = path.read_text(encoding="utf-8")
    try:
        fm, body = parse_frontmatter(text)
    except Exception as exc:
        add(issues, "ERROR", str(exc))
        return issues

    for key in REQUIRED_KEYS:
        val, ok = get_path(fm, key)
        if not ok or val in (None, "", []):
            add(issues, "ERROR", f"Missing or empty required frontmatter field: {key}")

    typ, ok = get_path(fm, "artifact.type")
    if ok and typ != "architecture-blueprint-review":
        add(issues, "ERROR", "artifact.type must be 'architecture-blueprint-review'")

    hs = headings(body)
    pos = {title: p for level, title, p in hs if level <= 2}
    last = -1
    for section in REQUIRED_SECTIONS:
        if section not in pos:
            add(issues, "ERROR", f"Missing required section: {section}")
        elif pos[section] < last:
            add(issues, "ERROR", f"Section out of order: {section}")
        else:
            last = pos[section]

    gap_count = len(re.findall(r"^###\s+GAP-\d+\s+—", body, re.MULTILINE))
    rec_count = len(re.findall(r"^###\s+REC-\d+\s+—", body, re.MULTILINE))
    val_count = len(re.findall(r"^###\s+VAL-\d+\s+—", body, re.MULTILINE))
    if gap_count and not rec_count:
        add(issues, "ERROR", "GAP records exist but no REC records were found")

    # One-to-one or many-to-one can be valid, but every GAP should be referenced by a REC.
    gap_ids = set(re.findall(r"^###\s+(GAP-\d+)\s+—", body, re.MULTILINE))
    rec_addr = set(re.findall(r"\*\*Addresses:\*\*\s*([^\n]+)", body))
    addressed = set()
    for group in rec_addr:
        addressed.update(re.findall(r"GAP-\d+", group))
    for gap in sorted(gap_ids - addressed):
        add(issues, "WARNING", f"{gap} is not referenced by any **Addresses:** recommendation field")

    for phrase in COMMERCIAL_WARNINGS:
        if phrase.lower() in body.lower():
            add(issues, "WARNING", f"Commercial/product-first phrasing found: '{phrase}'")

    for pattern in PRODUCT_GAP_PATTERNS:
        if re.search(pattern, body, flags=re.IGNORECASE | re.DOTALL):
            add(issues, "WARNING", "A gap may be framed as absence of QTC/product adoption rather than an architecture mismatch")

    # Check recommendation ordering within each REC block.
    rec_matches = list(re.finditer(r"^###\s+REC-\d+\s+—.*$", body, re.MULTILINE))
    for i, m in enumerate(rec_matches):
        block = body[m.start():(rec_matches[i+1].start() if i+1 < len(rec_matches) else len(body))]
        wanted = [
            "Recommended architectural direction",
            "Practical implications",
            "Options and trade-offs / key considerations",
            "Validation and acceptance",
            "Qlik/Talend role",
        ]
        loc = {w: block.find("#### " + w) for w in wanted}
        for w, p in loc.items():
            if p < 0:
                add(issues, "WARNING", f"{m.group(0).strip()} is missing recommended subsection '{w}'")
        present = [loc[w] for w in wanted if loc[w] >= 0]
        if present != sorted(present):
            add(issues, "ERROR", f"{m.group(0).strip()} does not follow architecture-first recommendation order")

    return issues, {"gaps": gap_count, "recommendations": rec_count, "validation_items": val_count}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("assessment", type=Path)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if not args.assessment.exists():
        print(f"ERROR: file not found: {args.assessment}", file=sys.stderr)
        return 2

    result = validate(args.assessment)
    if isinstance(result, tuple):
        issues, counts = result
    else:
        issues, counts = result, {}
    errors = sum(i["level"] == "ERROR" for i in issues)
    warnings = sum(i["level"] == "WARNING" for i in issues)
    if args.json:
        print(json.dumps({"file": str(args.assessment), "errors": errors, "warnings": warnings,
                          "counts": counts, "issues": issues}, indent=2))
    else:
        for i in issues:
            print(f"{i['level']}: {i['message']}")
        print(f"Summary: {errors} error(s), {warnings} warning(s); counts={counts}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
