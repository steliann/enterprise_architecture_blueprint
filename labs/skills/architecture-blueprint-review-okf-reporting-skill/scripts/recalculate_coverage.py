#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

from common import open_package, parse_frontmatter
from coverage_rubric import load_rubric, model_hash, score_category, coverage_level, portable_document

ROOT = Path(__file__).resolve().parents[1]
DEFAULTS = ROOT / "config" / "defaults.yaml"


def write_document(path: Path, fm: dict[str, Any], body: str) -> None:
    text = "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=110).rstrip() + "\n---\n\n" + body.lstrip("\r\n")
    path.write_text(text, encoding="utf-8")


def replace_score_text(body: str, score: int, level: str, model: str, overall: bool = False) -> str:
    if overall:
        body = re.sub(r"\*\*Overall review-confidence score:\*\*\s*\*\*\d+/100\*\*", f"**Overall review-confidence score:** **{score}/100**", body)
        body = re.sub(r"\*\*Coverage level:\*\*\s*\*\*.*?\*\*", f"**Coverage level:** **{level}**", body)
    else:
        body = re.sub(r"\*\*Category score:\*\*\s*\*\*\d+/100\*\*", f"**Category score:** **{score}/100**", body)
        body = re.sub(r"\*\*Coverage:\*\*\s*\*\*.*?\*\*", f"**Coverage:** **{level}**", body)
    body = re.sub(r"\*\*Coverage model:\*\*\s*`[^`]+`", f"**Coverage model:** `{model}`", body)
    return body


def main() -> int:
    ap = argparse.ArgumentParser(description="Recalculate Review OKF coverage totals from retained raw dimension scores.")
    ap.add_argument("review", help="Review OKF directory or ZIP")
    ap.add_argument("--coverage-config", help="Portable coverage-rubric.yaml exported by the Workbench")
    ap.add_argument("--write", action="store_true", help="Write recalculated scores back; requires a directory input")
    ap.add_argument("--json", dest="json_path", help="Optional JSON result output")
    args = ap.parse_args()

    defaults_doc = yaml.safe_load(DEFAULTS.read_text(encoding="utf-8")) or {}
    levels = defaults_doc.get("coverage_levels") or []
    override = Path(args.coverage_config).expanduser().resolve() if args.coverage_config else None
    try:
        rubric = load_rubric(DEFAULTS, override)
    except Exception as exc:
        print(f"ERROR: invalid coverage rubric: {exc}", file=sys.stderr)
        return 1
    rubric_hash = model_hash(rubric)

    root, td = open_package(args.review)
    try:
        if args.write and not Path(args.review).is_dir():
            print("ERROR: --write requires an extracted Review OKF directory", file=sys.stderr)
            return 1
        cdir = root / "coverage" / "categories"
        if not cdir.is_dir():
            print(f"ERROR: coverage/categories not found under {root}", file=sys.stderr)
            return 1
        results = []
        for path in sorted(cdir.glob("[0-9][0-9]-*.md")):
            fm, body = parse_frontmatter(path)
            scores = fm.get("coverage_dimensions")
            if not isinstance(scores, dict):
                print(f"ERROR: {path.relative_to(root)} lacks coverage_dimensions; full coverage rescore required", file=sys.stderr)
                return 1
            try:
                score = score_category(rubric, scores)
            except Exception as exc:
                print(f"ERROR: {path.relative_to(root)}: {exc}", file=sys.stderr)
                return 1
            level = coverage_level(score, levels)
            results.append({"category_id": fm.get("category_id"), "category": fm.get("category"), "score": score, "level": level, "path": str(path.relative_to(root))})
            if args.write:
                fm["coverage_model_version"] = str(rubric.get("model_version") or "1.0")
                fm["coverage_model_hash"] = rubric_hash
                fm["category_score"] = score
                fm["coverage"] = level
                write_document(path, fm, replace_score_text(body, score, level, rubric_hash, overall=False))

        if not results:
            print("ERROR: no coverage category reports with numeric prefixes found", file=sys.stderr)
            return 1
        overall = int(round(sum(item["score"] for item in results) / len(results)))
        overall_level = coverage_level(overall, levels)
        combined = root / "coverage" / "architecture-coverage-view-trust-combine.md"
        if combined.exists() and args.write:
            fm, body = parse_frontmatter(combined)
            fm["coverage_model_version"] = str(rubric.get("model_version") or "1.0")
            fm["coverage_model_hash"] = rubric_hash
            fm["overall_score"] = overall
            fm["overall_level"] = overall_level
            # Keep common legacy field synchronized when present.
            if "overall_trust" in fm:
                fm["overall_trust"] = overall_level
            result_by_category={str(item.get("category") or "").strip():item for item in results}
            updated_lines=[]
            for line in body.splitlines():
                if line.lstrip().startswith("|"):
                    parts=line.split("|")
                    if len(parts)>=5:
                        category=parts[1].strip()
                        item=result_by_category.get(category)
                        if item:
                            parts[2]=f" {item['score']} "
                            parts[3]=f" {item['level']} "
                            line="|".join(parts)
                updated_lines.append(line)
            body="\n".join(updated_lines)+( "\n" if body.endswith("\n") else "")
            write_document(combined, fm, replace_score_text(body, overall, overall_level, rubric_hash, overall=True))
        if args.write:
            rubric_path = root / "review-model" / "coverage-rubric.yaml"
            rubric_path.parent.mkdir(parents=True, exist_ok=True)
            rubric_path.write_text(yaml.safe_dump(portable_document(rubric), sort_keys=False, allow_unicode=True, width=110), encoding="utf-8")

        result = {"coverage_model_hash": rubric_hash, "coverage_model_version": str(rubric.get("model_version") or "1.0"), "overall_score": overall, "overall_level": overall_level, "categories": results}
        print(json.dumps(result, indent=2, ensure_ascii=False))
        if args.json_path:
            Path(args.json_path).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        return 0
    finally:
        if td:
            td.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
