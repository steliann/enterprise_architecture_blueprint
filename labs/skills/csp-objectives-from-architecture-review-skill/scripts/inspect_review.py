#!/usr/bin/env python3
import argparse, json, re, sys, tempfile, zipfile
from pathlib import Path
try:
    import yaml
except Exception:
    sys.exit('ERROR: PyYAML is required (import yaml failed).')

FM_RE=re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.S)

def read_md(p):
    text=p.read_text(encoding='utf-8')
    m=FM_RE.match(text)
    meta=yaml.safe_load(m.group(1)) if m else {}
    return meta or {}, text[m.end():] if m else text

def materialize(path):
    p=Path(path)
    if p.is_dir(): return p, None
    if p.suffix.lower()=='.zip':
        td=tempfile.TemporaryDirectory()
        with zipfile.ZipFile(p) as z: z.extractall(td.name)
        return Path(td.name), td
    raise SystemExit(f'Unsupported input: {p}')

def find_review_root(base):
    candidates=[]
    for p in [base]+[x for x in base.rglob('architecture-blueprint-review.md')]:
        if p.is_file() and p.name=='architecture-blueprint-review.md': candidates.append(p.parent)
    if not candidates:
        for d in base.rglob('architecture-blueprint-review'):
            if d.is_dir() and (d/'recommendations').is_dir(): candidates.append(d)
    if not candidates: raise SystemExit('Could not locate architecture-blueprint-review root.')
    return sorted(set(candidates), key=lambda x: len(x.parts))[0]

def sec(body, heading):
    pat=re.compile(rf'^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s+|\Z)', re.M|re.S|re.I)
    m=pat.search(body); return m.group(1).strip() if m else ''

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('review')
    ap.add_argument('--json', dest='json_out')
    ap.add_argument('--markdown', dest='md_out')
    a=ap.parse_args()
    base,tmp=materialize(a.review); root=find_review_root(base)
    report_meta={}
    if (root/'architecture-blueprint-review.md').exists(): report_meta,_=read_md(root/'architecture-blueprint-review.md')
    recs=[]
    recdir=root/'recommendations'
    for p in sorted(recdir.glob('REC-*.md')):
        meta,body=read_md(p)
        recs.append({
            'id':meta.get('id'),'title':meta.get('title'),'state':meta.get('state'),'status':meta.get('status'),
            'confidence':meta.get('confidence'),'horizon':meta.get('horizon'),'impact':meta.get('impact'),
            'category':meta.get('category'),'originating_gaps':meta.get('originating_gaps') or [],
            'affected_elements':meta.get('affected_elements') or {},'file':p.name,
            'architecture_context':sec(body,'Architecture Context'),
            'architecture_advice': next((sec(body,h) for h in ['Architecture Advice','Architecture Advice — Current Entitlement','Architecture Advice — Expanded Entitlement','Recommendation'] if sec(body,h)), ''),
            'expected_benefits':sec(body,'Expected Benefits'),
            'customer_validation':sec(body,'Customer Validation Before Acceptance'),
            'traceability':sec(body,'Traceability')
        })
    out={'review_version':report_meta.get('review_version'),'blueprint_version':report_meta.get('blueprint_version'),'recommendation_count':len(recs),'recommendations':recs}
    if a.json_out: Path(a.json_out).write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    lines=[f"# Architecture Review Recommendation Inventory",'',f"- Review version: {out['review_version'] or 'unknown'}",f"- Recommendations: {len(recs)}",'', '| ID | Title | Horizon | Impact | Category | State | Confidence |','|---|---|---|---|---|---|---|']
    for r in recs: lines.append(f"| {r['id']} | {r['title']} | {r['horizon']} | {r['impact']} | {r['category']} | {r['state']} | {r['confidence']} |")
    md='\n'.join(lines)+'\n'
    if a.md_out: Path(a.md_out).write_text(md,encoding='utf-8')
    if not a.json_out and not a.md_out: print(md,end='')
    if tmp: tmp.cleanup()

if __name__=='__main__': main()
