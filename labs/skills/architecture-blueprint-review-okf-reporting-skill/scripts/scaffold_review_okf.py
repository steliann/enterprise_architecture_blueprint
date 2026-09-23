#!/usr/bin/env python3
from __future__ import annotations
import argparse, shutil, sys
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("output_dir"); ap.add_argument("--force",action="store_true")
    a=ap.parse_args(); src=Path(__file__).resolve().parents[1]/"templates/review-okf"; dst=Path(a.output_dir)/"architecture-blueprint-review"
    if dst.exists():
        if not a.force: print(f"Destination exists: {dst}; use --force to replace"); return 1
        shutil.rmtree(dst)
    shutil.copytree(src,dst)
    print(dst)
    return 0
if __name__=="__main__": sys.exit(main())
