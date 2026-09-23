#!/usr/bin/env python3
from __future__ import annotations
import argparse, sys
from pathlib import Path
from common import open_package, markdown_files, parse_frontmatter, defined_ids, referenced_ids, report, PLACEHOLDER_RE

ANCHORS = ["index.md", "knowledge-model.md", "high-level-architecture.md"]
EXPECTED_HINTS = [
    "business-use-cases", "required-capabilities", "data-products", "data-flows",
    "quality-controls", "operational-capabilities", "architecture-decision-records"
]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("blueprint")
    ap.add_argument("--allow-placeholders", action="store_true")
    args = ap.parse_args()
    errors=[]; warnings=[]
    try:
        root, td = open_package(args.blueprint)
    except Exception as e:
        print(e); return 1
    try:
        files = markdown_files(root)
        if not files:
            errors.append("No Markdown files found in Blueprint package")
        for a in ANCHORS:
            if not (root/a).exists(): errors.append(f"Missing required Blueprint anchor: {a}")
        for hint in EXPECTED_HINTS:
            if not (root/hint).exists(): warnings.append(f"Expected model area not found: {hint}/ (allowed if out of declared scope)")
        ids = defined_ids(root)
        if not ids: errors.append("No defined architecture IDs detected")
        refs = referenced_ids(root)
        # Only blueprint-model IDs are evaluated here.
        prefixes = ("UC-","RC-","DP-","DF-","QC-","OC-","ADR-","SRC-","CON-","TEC-")
        dangling = sorted(k for k in refs if k.startswith(prefixes) and k not in ids)
        for k in dangling:
            sample = ", ".join(str(p.relative_to(root)) for p in refs[k][:3])
            warnings.append(f"Reference {k} has no detected definition (seen in {sample})")
        seen={}
        for p in files:
            try: fm, body = parse_frontmatter(p)
            except Exception as e: errors.append(str(e)); continue
            rid = fm.get("id")
            if isinstance(rid,str):
                u=rid.upper()
                if u in seen and seen[u] != p: errors.append(f"Duplicate frontmatter id {u}: {seen[u]} and {p}")
                seen[u]=p
            if not args.allow_placeholders and PLACEHOLDER_RE.search(body):
                warnings.append(f"Placeholder-looking text found in {p.relative_to(root)}")
        print(f"Blueprint root: {root}")
        print(f"Markdown files: {len(files)} | Defined IDs: {len(ids)} | Referenced IDs: {len(refs)}")
        return report(errors,warnings,"Blueprint OKF validation")
    finally:
        if td: td.cleanup()

if __name__ == "__main__": sys.exit(main())
