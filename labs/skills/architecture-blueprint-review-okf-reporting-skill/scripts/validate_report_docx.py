#!/usr/bin/env python3
from __future__ import annotations
import argparse, re, sys
from pathlib import Path
from docx import Document
from common import open_package, parse_frontmatter, PLACEHOLDER_RE, report
from extract_review_manifest import collect

REQUIRED_SECTIONS=[
"About this architecture assessment","Executive assessment","Assessment approach and classification",
"Findings and recommendations at a glance","Detailed architecture findings and recommended responses",
"Cross-gap architecture themes","Validation items and evidence to capture","Aggregated architecture conclusions",
"Assessment disposition","Document status"]

def doc_text(doc):
    parts=[]
    for p in doc.paragraphs:
        if p.text.strip(): parts.append(p.text.strip())
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                txt=cell.text.strip()
                if txt: parts.append(txt)
    return "\n".join(parts)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("docx"); ap.add_argument("--review"); ap.add_argument("--allow-subset",action="store_true"); ap.add_argument("--allow-placeholders",action="store_true")
    args=ap.parse_args(); errors=[]; warnings=[]
    p=Path(args.docx)
    if not p.exists(): print(f"File not found: {p}"); return 1
    try: doc=Document(p)
    except Exception as e: print(f"Cannot open DOCX: {e}"); return 1
    text=doc_text(doc); low=text.lower()
    for s in REQUIRED_SECTIONS:
        if s.lower() not in low: errors.append(f"Missing required report section: {s}")
    if not args.allow_placeholders and PLACEHOLDER_RE.search(text): errors.append("Unresolved template placeholders found in report")
    if "unknown" not in low or "gap" not in low: warnings.append("Evidence rule / Unknown-is-not-a-gap wording was not detected")
    td=None
    if args.review:
        root,td=open_package(args.review); man=collect(root)
        missing=[]
        for g in man["gaps"]:
            title=str(g.get("title") or "").strip()
            gid=str(g.get("id") or "")
            if title and title.lower() not in low and gid.lower() not in low: missing.append(f"{gid} - {title}")
        if missing:
            msg=f"{len(missing)} Review gap(s) not represented in report: " + "; ".join(missing[:8])
            (warnings if args.allow_subset else errors).append(msg)
        # Validation items should be represented unless subset is explicit.
        vm=[]
        for v in man["validation_items"]:
            title=str(v.get("title") or "").strip(); vid=str(v.get("id") or "")
            if title and title.lower() not in low and vid.lower() not in low: vm.append(f"{vid} - {title}")
        if vm: (warnings if args.allow_subset else errors).append(f"{len(vm)} Validation Item(s) not represented in report")
        if td: td.cleanup()
    # basic style sanity
    names={p.style.name for p in doc.paragraphs if p.style}
    if "Heading 1" not in names: warnings.append("Heading 1 style not used")
    print(f"DOCX paragraphs: {len(doc.paragraphs)} | tables: {len(doc.tables)}")
    return report(errors,warnings,"Word architecture assessment validation")
if __name__=="__main__": sys.exit(main())
