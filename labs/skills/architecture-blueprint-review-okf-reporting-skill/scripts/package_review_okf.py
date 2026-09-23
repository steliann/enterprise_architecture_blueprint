#!/usr/bin/env python3
from __future__ import annotations
import argparse, subprocess, sys, zipfile
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(description='Validate and package an Architecture Blueprint Review OKF directory.')
    ap.add_argument('review_dir')
    ap.add_argument('output_zip')
    ap.add_argument('--blueprint')
    ap.add_argument('--skip-validation',action='store_true')
    a=ap.parse_args()
    root=Path(a.review_dir).resolve()
    if not root.is_dir():
        print(f'Not a directory: {root}'); return 1
    if root.name != 'architecture-blueprint-review':
        print("Review directory should be named 'architecture-blueprint-review' so the ZIP has one canonical top-level folder.")
        return 1
    if not a.skip_validation:
        cmd=[sys.executable, str(Path(__file__).resolve().parent/'validate_review_okf.py'), str(root)]
        if a.blueprint: cmd += ['--blueprint', a.blueprint]
        rc=subprocess.call(cmd)
        if rc: return rc
    out=Path(a.output_zip).resolve(); out.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(root.rglob('*')):
            if p.is_file(): z.write(p, p.relative_to(root.parent))
    print(out)
    return 0
if __name__=='__main__': sys.exit(main())
