#!/usr/bin/env python3
import argparse, subprocess, sys, tempfile, zipfile
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(description='Validate and package CSP Objectives OKF')
    ap.add_argument('csp_folder'); ap.add_argument('--review',required=True); ap.add_argument('--previous'); ap.add_argument('--blueprint'); ap.add_argument('--out',required=True)
    a=ap.parse_args(); root=Path(a.csp_folder)
    if root.name!='customer-success-plan-objectives':
        cand=root/'customer-success-plan-objectives'
        if cand.is_dir(): root=cand
    if not root.is_dir(): sys.exit('ERROR: CSP folder not found.')
    script=Path(__file__).with_name('validate_csp.py')
    with tempfile.TemporaryDirectory() as td:
        report=Path(td)/'validation-report.md'
        cmd=[sys.executable,str(script),str(root),'--review',a.review,'--report',str(report)]
        if a.previous: cmd += ['--previous',a.previous]
        if a.blueprint: cmd += ['--blueprint',a.blueprint]
        proc=subprocess.run(cmd)
        if proc.returncode: sys.exit(proc.returncode)
        out=Path(a.out); out.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
            for p in sorted(root.rglob('*')):
                if p.is_file(): z.write(p,Path(root.name)/p.relative_to(root))
            z.write(report,'validation-report.md')
        print(out)

if __name__=='__main__': main()
