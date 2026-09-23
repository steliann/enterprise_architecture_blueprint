#!/usr/bin/env python3
from __future__ import annotations
import argparse, subprocess, sys
from pathlib import Path

def run(cmd):
    print("\n$", " ".join(map(str,cmd)))
    return subprocess.call([str(x) for x in cmd])

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--blueprint"); ap.add_argument("--review"); ap.add_argument("--coverage-config"); ap.add_argument("--docx"); ap.add_argument("--pptx"); ap.add_argument("--allow-subset",action="store_true")
    a=ap.parse_args(); here=Path(__file__).resolve().parent; codes=[]
    if a.blueprint: codes.append(run([sys.executable,here/"validate_blueprint_okf.py",a.blueprint]))
    if a.review:
        cmd=[sys.executable,here/"validate_review_okf.py",a.review]
        if a.blueprint: cmd += ["--blueprint",a.blueprint]
        if a.coverage_config: cmd += ["--coverage-config",a.coverage_config]
        codes.append(run(cmd))
    if a.docx:
        cmd=[sys.executable,here/"validate_report_docx.py",a.docx]
        if a.review: cmd += ["--review",a.review]
        if a.allow_subset: cmd += ["--allow-subset"]
        codes.append(run(cmd))
    if a.pptx:
        cmd=[sys.executable,here/"validate_review_slides.py",a.pptx]
        if a.review: cmd += ["--review",a.review]
        if a.allow_subset: cmd += ["--allow-subset"]
        codes.append(run(cmd))
    if not codes: ap.error("Provide at least one artifact")
    return 1 if any(c != 0 for c in codes) else 0
if __name__=="__main__": sys.exit(main())
