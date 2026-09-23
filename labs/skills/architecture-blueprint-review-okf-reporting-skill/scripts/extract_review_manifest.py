#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from common import open_package, parse_frontmatter, write_json

def collect(root: Path):
    gaps=[]; vals=[]; recs=[]
    gdir=root/"gaps"; rdir=root/"recommendations"
    if gdir.exists():
        for p in sorted(gdir.glob("*.md")):
            if p.name=="index.md": continue
            fm,_=parse_frontmatter(p)
            if fm.get("artifact_type") == "Architecture Gap" or str(fm.get("id","")).startswith("GAP-"):
                gaps.append({"id":fm.get("id"),"title":fm.get("title"),"state":fm.get("state"),"priority":fm.get("priority"),"confidence":fm.get("confidence"),"horizon":fm.get("horizon"),"response_class":fm.get("response_class"),"recommendations":fm.get("recommendations",[]),"file":str(p.relative_to(root))})
        vdir=gdir/"validation"
        if vdir.exists():
            for p in sorted(vdir.glob("*.md")):
                if p.name=="index.md": continue
                fm,_=parse_frontmatter(p)
                if fm.get("artifact_type") == "Architecture Validation Item" or str(fm.get("id","")).startswith("VAL-"):
                    vals.append({"id":fm.get("id"),"title":fm.get("title"),"state":fm.get("state"),"confidence":fm.get("confidence"),"file":str(p.relative_to(root))})
    if rdir.exists():
        for p in sorted(rdir.glob("*.md")):
            if p.name=="index.md": continue
            fm,_=parse_frontmatter(p)
            if fm.get("artifact_type") == "Architecture Recommendation" or str(fm.get("id","")).startswith("REC-"):
                recs.append({"id":fm.get("id"),"title":fm.get("title"),"state":fm.get("state"),"horizon":fm.get("horizon"),"response_class":fm.get("response_class"),"originating_gaps":fm.get("originating_gaps",[]),"file":str(p.relative_to(root))})
    integ={}
    p=root/"architecture-blueprint-review.md"
    if p.exists(): integ,_=parse_frontmatter(p)
    gaps.sort(key=lambda x: (int(''.join(filter(str.isdigit,str(x.get('id','999999')))) or 999999)))
    recs.sort(key=lambda x: (int(''.join(filter(str.isdigit,str(x.get('id','999999')))) or 999999)))
    return {"review":integ,"counts":{"gaps":len(gaps),"candidate_gaps":sum(str(g.get('state','')).lower()=='candidate' for g in gaps),"active_gaps":sum(str(g.get('state','')).lower()=='active' for g in gaps),"validation_items":len(vals),"recommendations":len(recs)},"gaps":gaps,"validation_items":vals,"recommendations":recs}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("review"); ap.add_argument("--out")
    args=ap.parse_args(); root,td=open_package(args.review)
    try:
        data=collect(root)
        if args.out: write_json(data,args.out)
        else: print(json.dumps(data,indent=2,ensure_ascii=False))
    finally:
        if td: td.cleanup()
    return 0
if __name__=="__main__": sys.exit(main())
