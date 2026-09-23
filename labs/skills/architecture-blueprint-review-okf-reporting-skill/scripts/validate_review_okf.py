#!/usr/bin/env python3
from __future__ import annotations
import argparse, re, sys
import yaml
from pathlib import Path
from common import open_package, parse_frontmatter, markdown_files, heading_set, flatten_ids, defined_ids, PLACEHOLDER_RE, normalize_enum, report
from coverage_rubric import load_rubric, model_hash, score_category, coverage_level

STATUS={"current","planned","target","transitional","deprecated","retired"}
CONF={"high","medium","low","not_assessed"}
VALID={"confirmed","needs_correction","incomplete","unable_to_validate","not_applicable"}
GSTATE={"candidate","active","planned","in_progress","mitigated","closed","absorbed","superseded","rejected"}
RSTATE={"proposed","accepted","planned","in_progress","implemented","validated","completed","rejected","deferred","superseded"}
VSTATE={"open","resolved","accepted_limitation","superseded"}

def enum_check(errors, p, fm, key, allowed):
    if key not in fm: errors.append(f"{p}: missing frontmatter '{key}'"); return
    v=normalize_enum(fm[key])
    if v not in allowed: errors.append(f"{p}: invalid {key}={fm[key]!r}")

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("review"); ap.add_argument("--blueprint"); ap.add_argument("--coverage-config"); ap.add_argument("--allow-placeholders",action="store_true")
    args=ap.parse_args(); errors=[]; warnings=[]
    root,td=open_package(args.review)
    btd=None; bdefs={}
    try:
        required=["index.md","architecture-blueprint-review.md","review-model/knowledge-model.md","review-model/review-guide.md","coverage/index.md","coverage/architecture-coverage-view-trust-combine.md","gaps/index.md","gaps/validation/index.md","recommendations/index.md"]
        for r in required:
            if not (root/r).exists(): errors.append(f"Missing Review artifact: {r}")
        if args.blueprint:
            broot,btd=open_package(args.blueprint); bdefs=defined_ids(broot)
        gaps={}; vals={}; recs={}
        gdir=root/"gaps"; rdir=root/"recommendations"; vdir=gdir/"validation"
        if gdir.exists():
            for p in sorted(gdir.glob("*.md")):
                if p.name=="index.md": continue
                fm,body=parse_frontmatter(p); rid=str(fm.get("id","")).upper()
                if not rid.startswith("GAP-"): warnings.append(f"{p.relative_to(root)} is in gaps/ but has no GAP id"); continue
                if rid in gaps: errors.append(f"Duplicate gap id {rid}")
                gaps[rid]=(p,fm,body)
                for k,a in [("status",STATUS),("confidence",CONF),("validation",VALID),("state",GSTATE)]: enum_check(errors,p.relative_to(root),fm,k,a)
                if not fm.get("title"): errors.append(f"{p.relative_to(root)}: missing title")
                if not isinstance(fm.get("recommendations",[]),list): errors.append(f"{p.relative_to(root)}: recommendations must be a list")
                hs=heading_set(body)
                # Compatibility with the supplied review: legacy gaps may use Architecture Context rather than explicit expected/current headings.
                if "architecture gap" not in hs: errors.append(f"{p.relative_to(root)}: missing 'Architecture Gap' section")
                if not any(h in hs for h in ["impact if not addressed","impact rationale"]): errors.append(f"{p.relative_to(root)}: missing impact section")
                if not ({"expected architecture condition","current architecture condition"} <= hs):
                    if "architecture context" in hs: warnings.append(f"{p.relative_to(root)}: legacy gap structure; explicit expected/current condition sections are recommended")
                    else: warnings.append(f"{p.relative_to(root)}: expected/current conditions are not explicit")
                if "traceability" not in hs: warnings.append(f"{p.relative_to(root)}: no Traceability heading")
        if vdir.exists():
            for p in sorted(vdir.glob("*.md")):
                if p.name=="index.md": continue
                fm,body=parse_frontmatter(p); rid=str(fm.get("id","")).upper()
                if not rid.startswith("VAL-"): warnings.append(f"{p.relative_to(root)} is in validation/ but has no VAL id"); continue
                if rid in vals: errors.append(f"Duplicate validation id {rid}")
                vals[rid]=(p,fm,body)
                for k,a in [("status",STATUS),("confidence",CONF),("validation",VALID),("state",VSTATE)]: enum_check(errors,p.relative_to(root),fm,k,a)
        if rdir.exists():
            for p in sorted(rdir.glob("*.md")):
                if p.name=="index.md": continue
                fm,body=parse_frontmatter(p); rid=str(fm.get("id","")).upper()
                if not rid.startswith("REC-"): warnings.append(f"{p.relative_to(root)} is in recommendations/ but has no REC id"); continue
                if rid in recs: errors.append(f"Duplicate recommendation id {rid}")
                recs[rid]=(p,fm,body)
                for k,a in [("status",STATUS),("confidence",CONF),("validation",VALID),("state",RSTATE)]: enum_check(errors,p.relative_to(root),fm,k,a)
                og=fm.get("originating_gaps")
                if not isinstance(og,list) or not og: errors.append(f"{p.relative_to(root)}: originating_gaps must be a non-empty list")
                hs=heading_set(body)
                if "recommendation basis" not in hs: warnings.append(f"{p.relative_to(root)}: missing Recommendation Basis")
                if not any(h in hs for h in ["recommended architectural direction","architecture advice — current entitlement","architecture advice - current entitlement","architecture advice — expanded entitlement","architecture advice - expanded entitlement"]):
                    warnings.append(f"{p.relative_to(root)}: no explicit target/current/expanded architecture advice heading detected")
                if not any(h.startswith("expected benefits") for h in hs): warnings.append(f"{p.relative_to(root)}: no Expected Benefits section detected")
        # Mapping integrity
        for gid,(p,fm,body) in gaps.items():
            for rid in fm.get("recommendations",[]) or []:
                ru=str(rid).upper()
                if ru not in recs: errors.append(f"{gid} references missing recommendation {ru}")
        for rid,(p,fm,body) in recs.items():
            for gid in fm.get("originating_gaps",[]) or []:
                gu=str(gid).upper()
                if gu not in gaps: errors.append(f"{rid} originates from missing gap {gu}")
        unmapped=[gid for gid,(p,fm,b) in gaps.items() if not (fm.get("recommendations") or [])]
        for gid in unmapped: warnings.append(f"{gid} has no recommendation mapping")
        # Index counts
        gp=root/"gaps/index.md"
        if gp.exists():
            fm,_=parse_frontmatter(gp)
            expected={"total_gaps":len(gaps),"active_gaps":sum(normalize_enum(x[1].get('state'))=='active' for x in gaps.values()),"candidate_gaps":sum(normalize_enum(x[1].get('state'))=='candidate' for x in gaps.values()),"validation_items":len(vals)}
            for k,v in expected.items():
                if k in fm and fm[k] != v: errors.append(f"gaps/index.md {k}={fm[k]} but actual is {v}")
        rp=root/"recommendations/index.md"
        if rp.exists():
            fm,_=parse_frontmatter(rp)
            if "total_recommendations" in fm and fm["total_recommendations"] != len(recs): errors.append(f"recommendations/index.md total_recommendations={fm['total_recommendations']} but actual is {len(recs)}")
        vp=root/"gaps/validation/index.md"
        if vp.exists():
            fm,_=parse_frontmatter(vp)
            if "total_validation_items" in fm and fm["total_validation_items"] != len(vals): errors.append(f"gaps/validation/index.md total_validation_items={fm['total_validation_items']} but actual is {len(vals)}")
        # Coverage rubric consistency and arithmetic mean
        defaults_path=Path(__file__).resolve().parents[1]/"config"/"defaults.yaml"
        try:
            rubric=load_rubric(defaults_path, Path(args.coverage_config).expanduser().resolve() if args.coverage_config else None)
            rubric_hash=model_hash(rubric)
            defaults_doc=yaml.safe_load(defaults_path.read_text(encoding="utf-8")) or {}
            levels=defaults_doc.get("coverage_levels") or []
        except Exception as exc:
            errors.append(f"Coverage rubric could not be resolved: {exc}")
            rubric=None; rubric_hash=""; levels=[]
        cats=[]
        cdir=root/"coverage/categories"
        if cdir.exists():
            for p in sorted(cdir.glob("*.md")):
                if p.name in {"index.md","category-template.md"}: continue
                fm,_=parse_frontmatter(p)
                if "category_score" in fm:
                    try: cats.append(int(fm["category_score"]))
                    except: errors.append(f"{p.relative_to(root)}: category_score is not an integer")
                scores=fm.get("coverage_dimensions")
                if rubric:
                    if not isinstance(scores,dict):
                        warnings.append(f"{p.relative_to(root)}: coverage_dimensions missing; deterministic weight-only recalculation is unavailable")
                    else:
                        try:
                            calc_score=score_category(rubric,scores)
                            if int(fm.get("category_score",-1)) != calc_score:
                                errors.append(f"{p.relative_to(root)}: category_score={fm.get('category_score')} but rubric calculation is {calc_score}")
                            expected_level=coverage_level(calc_score,levels)
                            if fm.get("coverage") and str(fm.get("coverage")) != expected_level:
                                warnings.append(f"{p.relative_to(root)}: coverage={fm.get('coverage')} but rubric level is {expected_level}")
                            if fm.get("coverage_model_hash") and str(fm.get("coverage_model_hash")) != rubric_hash:
                                warnings.append(f"{p.relative_to(root)}: coverage_model_hash differs from supplied/default rubric; recalculate coverage")
                        except Exception as exc:
                            errors.append(f"{p.relative_to(root)}: invalid coverage_dimensions: {exc}")
        cp=root/"coverage/architecture-coverage-view-trust-combine.md"
        if cp.exists() and cats:
            fm,_=parse_frontmatter(cp); calc=round(sum(cats)/len(cats))
            if "overall_score" in fm and int(fm["overall_score"]) != calc: errors.append(f"Combined coverage overall_score={fm['overall_score']} but arithmetic mean of category scores is {calc}")
            if rubric_hash and fm.get("coverage_model_hash") and str(fm.get("coverage_model_hash")) != rubric_hash:
                warnings.append("Combined coverage coverage_model_hash differs from supplied/default rubric; recalculate coverage")
        # Blueprint traceability
        if bdefs:
            for kind,items in [("gap",gaps),("recommendation",recs)]:
                for rid,(p,fm,body) in items.items():
                    for token in flatten_ids(fm):
                        if token.startswith(("GAP-","REC-","VAL-")): continue
                        if token not in bdefs: warnings.append(f"{rid} references Blueprint id {token} with no detected definition")
        if not args.allow_placeholders:
            for p in markdown_files(root):
                if PLACEHOLDER_RE.search(p.read_text(encoding='utf-8',errors='replace')):
                    errors.append(f"Unresolved template placeholder in {p.relative_to(root)}")
        print(f"Review root: {root}")
        print(f"Gaps: {len(gaps)} | Validation items: {len(vals)} | Recommendations: {len(recs)} | Coverage categories with scores: {len(cats)}")
        return report(errors,warnings,"Architecture Blueprint Review OKF validation")
    finally:
        if td: td.cleanup()
        if btd: btd.cleanup()
if __name__=="__main__": sys.exit(main())
