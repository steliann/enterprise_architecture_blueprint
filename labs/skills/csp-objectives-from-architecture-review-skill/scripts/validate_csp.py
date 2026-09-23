#!/usr/bin/env python3
import argparse, datetime as dt, re, sys, tempfile, zipfile
from pathlib import Path
try:
    import yaml
except Exception:
    sys.exit('ERROR: PyYAML is required (import yaml failed).')

FM_RE=re.compile(r'^---\s*\n(.*?)\n---\s*\n',re.S)
BO_REQ=['id','artifact_type','schema_version','title','status','confidence','validation','objective_state','planning_state','primary_business_use_cases','created_date','last_updated_date']
TO_REQ=['id','artifact_type','schema_version','title','status','confidence','validation','objective_state','planning_state','horizon','impact','category','source_recommendations','business_objectives','created_date','last_updated_date']
BO_SECS=['Objective','Primary Business Use Cases','Business Success Measures','Customer Success Plan Fields','Acceptance']
TO_SECS=['Objective','Business Objectives','Source Recommendations','Architecture Rationale','Technical Success Measures','Customer Success Plan Fields','Acceptance']
ENUMS={
 'status':{'target','transitional'}, 'confidence':{'high','medium','low'},
 'objective_state':{'draft','proposed','approved','achieved','withdrawn','superseded'},
 'planning_state':{'not_planned','planned','in_progress','at_risk','blocked','completed','cancelled'},
 'horizon':{'now','next','later'}, 'impact':{'high','medium','low'} }

def materialize(path):
    if not path: return None,None
    p=Path(path)
    if p.is_dir(): return p,None
    if p.suffix.lower()=='.zip':
        td=tempfile.TemporaryDirectory(); zipfile.ZipFile(p).extractall(td.name); return Path(td.name),td
    raise ValueError(f'Unsupported path: {p}')

def find_root(base, name, marker):
    if not base: return None
    if base.name==name and (base/marker).exists(): return base
    direct=base/name
    if direct.is_dir() and (direct/marker).exists(): return direct
    for d in base.rglob(name):
        if d.is_dir() and (d/marker).exists(): return d
    return None

def parse_md(p, errors=None):
    text=p.read_text(encoding='utf-8')
    m=FM_RE.match(text)
    if not m:
        if errors is not None: errors.append(f'{p}: missing YAML frontmatter')
        return {},text
    try: meta=yaml.safe_load(m.group(1)) or {}
    except Exception as e:
        if errors is not None: errors.append(f'{p}: invalid YAML frontmatter: {e}')
        meta={}
    return meta,text[m.end():]

def obj_text(body):
    m=re.search(r'^##\s+Objective\s*$\n(.*?)(?=^##\s+|\Z)',body,re.M|re.S|re.I)
    s=m.group(1) if m else ''
    return re.sub(r'\W+',' ',s.lower()).strip()

def valid_date(v):
    try: dt.date.fromisoformat(str(v)); return True
    except Exception: return False

def sections(body): return set(re.findall(r'^##\s+(.+?)\s*$',body,re.M))

def ids_from_files(root, prefix):
    d=root/('business-objectives' if prefix=='BO' else 'technical-objectives')
    out={}
    for p in sorted(d.glob(f'{prefix}-*.md')):
        if p.name=='index.md': continue
        meta,body=parse_md(p)
        if meta.get('id'): out[meta['id']]={'meta':meta,'body':body,'path':p}
    return out

def review_recs(review_root, errors):
    recs={}
    if not review_root: return recs,None
    main=review_root/'architecture-blueprint-review.md'; version=None
    if main.exists(): version=parse_md(main,errors)[0].get('review_version')
    for p in sorted((review_root/'recommendations').glob('REC-*.md')):
        meta,body=parse_md(p,errors)
        rid=meta.get('id')
        if rid: recs[rid]={'meta':meta,'body':body,'path':p}
    return recs,version

def main():
    ap=argparse.ArgumentParser(description='Validate CSP Objectives OKF')
    ap.add_argument('csp'); ap.add_argument('--review'); ap.add_argument('--previous'); ap.add_argument('--blueprint')
    ap.add_argument('--report'); ap.add_argument('--strict-one-to-one',action='store_true')
    a=ap.parse_args(); errors=[]; warnings=[]; temps=[]
    try:
        cbase,t=materialize(a.csp); temps.append(t); croot=find_root(cbase,'customer-success-plan-objectives','customer-success-plan-objectives.md')
        if not croot: raise SystemExit('ERROR: could not locate customer-success-plan-objectives root.')
        rroot=None; recs={}; review_version=None
        if a.review:
            rbase,t=materialize(a.review); temps.append(t); rroot=find_root(rbase,'architecture-blueprint-review','recommendations')
            if not rroot: errors.append('Could not locate architecture-blueprint-review root.')
            else: recs,review_version=review_recs(rroot,errors)
        prevroot=None
        if a.previous:
            pbase,t=materialize(a.previous); temps.append(t); prevroot=find_root(pbase,'customer-success-plan-objectives','customer-success-plan-objectives.md')
            if not prevroot: errors.append('Could not locate previous CSP root.')
        broot=None
        if a.blueprint:
            bbase,t=materialize(a.blueprint); temps.append(t); broot=find_root(bbase,'architecture-blueprint','index.md')
            if not broot: warnings.append('Could not locate architecture-blueprint root; BO use-case resolution skipped.')

        required=['index.md','customer-success-plan-objectives.md','knowledge-model/index.md','knowledge-model/knowledge-model.md','knowledge-model/objective-guide.md','business-objectives/index.md','technical-objectives/index.md']
        for rel in required:
            if not (croot/rel).exists(): errors.append(f'Missing required file: {rel}')
        bos={}; tos={}; seen=set()
        for kind,folder,patt,req,atype,secs in [
            ('BO','business-objectives',r'^BO-\d{3,}$',BO_REQ,'Customer Success Plan Business Objective',BO_SECS),
            ('TO','technical-objectives',r'^TO-\d{3,}$',TO_REQ,'Customer Success Plan Technical Objective',TO_SECS)]:
            d=croot/folder
            if not d.is_dir(): errors.append(f'Missing folder: {folder}'); continue
            for p in sorted(d.glob(f'{kind}-*.md')):
                meta,body=parse_md(p,errors); oid=meta.get('id')
                for k in req:
                    if k not in meta: errors.append(f'{p.name}: missing frontmatter key {k}')
                if not oid: continue
                if not re.match(patt,str(oid)): errors.append(f'{p.name}: invalid ID {oid}')
                if oid in seen: errors.append(f'Duplicate objective ID {oid}')
                seen.add(oid)
                if not p.name.startswith(oid+'-'): warnings.append(f'{p.name}: filename does not start with {oid}-')
                if meta.get('artifact_type')!=atype: errors.append(f'{oid}: artifact_type must be {atype!r}')
                if meta.get('schema_version')!=2: errors.append(f'{oid}: schema_version must be 2')
                for k,allowed in ENUMS.items():
                    if k in meta and str(meta[k]).lower() not in allowed: errors.append(f'{oid}: invalid {k}={meta[k]}')
                for k in ['created_date','last_updated_date']:
                    if k in meta and not valid_date(meta[k]): errors.append(f'{oid}: invalid ISO date {k}={meta[k]}')
                relkeys=['primary_business_use_cases'] if kind=='BO' else ['source_recommendations','business_objectives']
                for k in relkeys:
                    if not isinstance(meta.get(k),list) or len(meta.get(k) or [])==0: errors.append(f'{oid}: {k} must be a non-empty list')
                hs=sections(body)
                for s in secs:
                    if s not in hs: errors.append(f'{oid}: missing section ## {s}')
                item={'meta':meta,'body':body,'path':p}
                (bos if kind=='BO' else tos)[oid]=item
        if not bos: errors.append('No business objectives found.')
        if not tos: errors.append('No technical objectives found.')

        # Cross references.
        for tid,item in tos.items():
            m=item['meta']
            for bid in m.get('business_objectives') or []:
                if bid not in bos: errors.append(f'{tid}: references missing business objective {bid}')
            for rid in m.get('source_recommendations') or []:
                if recs and rid not in recs: errors.append(f'{tid}: references recommendation {rid} absent from current review')
            if recs and len(m.get('source_recommendations') or [])==1:
                rid=m['source_recommendations'][0]; rm=recs.get(rid,{}).get('meta',{})
                for k in ['horizon','impact']:
                    if rm.get(k) and m.get(k) and str(rm[k]).lower()!=str(m[k]).lower(): errors.append(f'{tid}: {k}={m[k]} does not match {rid} {k}={rm[k]}')
                if rm.get('category') and m.get('category') and str(rm['category'])!=str(m['category']): warnings.append(f'{tid}: category {m["category"]} differs from {rid} category {rm["category"]}')
        if recs:
            covered={rid:[] for rid in recs}
            for tid,item in tos.items():
                for rid in item['meta'].get('source_recommendations') or []:
                    if rid in covered: covered[rid].append(tid)
            for rid,tids in covered.items():
                if not tids: errors.append(f'Current recommendation {rid} has no active technical objective')
                elif len(tids)>1: (errors if a.strict_one_to_one else warnings).append(f'{rid} maps to multiple technical objectives: {", ".join(tids)}')
            for tid,item in tos.items():
                rs=item['meta'].get('source_recommendations') or []
                if len(rs)>1: (errors if a.strict_one_to_one else warnings).append(f'{tid} consolidates multiple recommendations: {", ".join(rs)}')

        # Optional Blueprint use-case existence.
        if broot:
            uc_ids=set()
            for p in broot.rglob('UC-*.md'):
                meta,_=parse_md(p)
                if meta.get('id'): uc_ids.add(meta['id'])
            for bid,item in bos.items():
                for uid in item['meta'].get('primary_business_use_cases') or []:
                    if uc_ids and uid not in uc_ids: errors.append(f'{bid}: primary use case {uid} not found in supplied Blueprint')

        # Portfolio declared counts.
        pp=croot/'customer-success-plan-objectives.md'
        if pp.exists():
            pm,_=parse_md(pp,errors)
            if pm.get('business_objective_count') is not None and pm.get('business_objective_count')!=len(bos): errors.append(f'Portfolio business_objective_count={pm.get("business_objective_count")} but found {len(bos)}')
            if pm.get('technical_objective_count') is not None and pm.get('technical_objective_count')!=len(tos): errors.append(f'Portfolio technical_objective_count={pm.get("technical_objective_count")} but found {len(tos)}')
            if review_version and pm.get('source_review_version') and str(pm.get('source_review_version'))!=str(review_version): warnings.append(f'Portfolio source_review_version={pm.get("source_review_version")} differs from review {review_version}')

        # Refresh identity heuristics.
        preserved=[]; new=[]
        if prevroot:
            pb=ids_from_files(prevroot,'BO'); pt=ids_from_files(prevroot,'TO'); prev={**pb,**pt}
            nums=[int(x.split('-')[1]) for x in pt if re.match(r'^TO-\d+$',x)]; max_to=max(nums) if nums else 0
            for oid,item in {**bos,**tos}.items():
                if oid in prev:
                    preserved.append(oid)
                    pm=prev[oid]['meta']; nm=item['meta']
                    if str(pm.get('created_date'))!=str(nm.get('created_date')): warnings.append(f'{oid}: created_date changed from {pm.get("created_date")} to {nm.get("created_date")}')
                    po=obj_text(prev[oid]['body']); no=obj_text(item['body'])
                    # Heuristic only: flag likely ID reuse, not normal rewrites. Stable title and
                    # stable business scope are strong evidence that an objective was refreshed
                    # rather than repurposed, even if the prose was substantially improved.
                    ps=set(po.split()); ns=set(no.split()); sim=len(ps&ns)/max(1,len(ps|ns))
                    old_title=set(re.sub(r'\W+',' ',str(pm.get('title','')).lower()).split())
                    new_title=set(re.sub(r'\W+',' ',str(nm.get('title','')).lower()).split())
                    title_sim=len(old_title&new_title)/max(1,len(old_title|new_title))
                    old_scope=set(pm.get('business_objectives') or pm.get('primary_business_use_cases') or [])
                    new_scope=set(nm.get('business_objectives') or nm.get('primary_business_use_cases') or [])
                    scope_sim=len(old_scope&new_scope)/max(1,len(old_scope|new_scope)) if (old_scope or new_scope) else 1.0
                    if po and no and sim<0.18 and title_sim<0.50 and scope_sim<0.50:
                        warnings.append(f'{oid}: objective meaning may have changed materially (text={sim:.2f}, title={title_sim:.2f}, scope={scope_sim:.2f}); verify immutable-ID semantics')
                else:
                    new.append(oid)
                    if oid.startswith('TO-') and int(oid.split('-')[1])<=max_to: warnings.append(f'{oid}: new TO ID is not above previous historical maximum TO-{max_to:03d}; verify ID recycling')
        horizon={h:0 for h in ['now','next','later']}
        for x in tos.values():
            h=str(x['meta'].get('horizon','')).lower()
            if h in horizon: horizon[h]+=1
        coverage=len({rid for x in tos.values() for rid in (x['meta'].get('source_recommendations') or []) if rid in recs}) if recs else 0
        result='PASS' if not errors else 'FAIL'
        lines=['# CSP Objectives OKF Validation','',f'- Result: **{result}**',f'- Source review: {review_version or "not supplied"}',f'- Business objectives: {len(bos)}',f'- Active technical objectives: {len(tos)}']
        if recs: lines.append(f'- Recommendation coverage: {coverage} of {len(recs)}')
        lines += [f'- Horizon distribution: Now {horizon["now"]} / Next {horizon["next"]} / Later {horizon["later"]}',f'- Errors: {len(errors)}',f'- Warnings: {len(warnings)}']
        if prevroot: lines += [f'- Preserved IDs: {", ".join(sorted(preserved)) or "None"}',f'- New IDs: {", ".join(sorted(new)) or "None"}']
        lines += ['','## Errors'] + (['- None'] if not errors else [f'- {e}' for e in errors]) + ['','## Warnings'] + (['- None'] if not warnings else [f'- {w}' for w in warnings])
        report='\n'.join(lines)+'\n'
        if a.report: Path(a.report).write_text(report,encoding='utf-8')
        print(report,end='')
        sys.exit(1 if errors else 0)
    finally:
        for t in temps:
            if t: t.cleanup()

if __name__=='__main__': main()
