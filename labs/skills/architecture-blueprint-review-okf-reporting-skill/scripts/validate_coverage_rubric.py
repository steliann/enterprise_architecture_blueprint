#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from coverage_rubric import load_rubric, model_hash, effective_weights, portable_document

ROOT=Path(__file__).resolve().parents[1]
DEFAULTS=ROOT/'config'/'defaults.yaml'

def main():
    ap=argparse.ArgumentParser(description='Validate and resolve a coverage rubric override.')
    ap.add_argument('config', nargs='?', help='Optional portable coverage-rubric.yaml override')
    args=ap.parse_args()
    try:
        rubric=load_rubric(DEFAULTS, Path(args.config) if args.config else None)
        out=portable_document(rubric)
        out['coverage_rubric']['model_hash']=model_hash(rubric)
        out['coverage_rubric']['effective_weights']=effective_weights(rubric)
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1
if __name__=='__main__': raise SystemExit(main())
