#!/usr/bin/env python3
from __future__ import annotations
import argparse, sys
from pathlib import Path
from pptx import Presentation
from common import open_package, PLACEHOLDER_RE, report
from extract_review_manifest import collect

def slide_text(slide):
    out=[]
    for sh in slide.shapes:
        if getattr(sh,"has_text_frame",False):
            t=sh.text.strip()
            if t: out.append(t)
    return "\n".join(out)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("pptx"); ap.add_argument("--review"); ap.add_argument("--allow-subset",action="store_true"); ap.add_argument("--allow-placeholders",action="store_true")
    args=ap.parse_args(); errors=[]; warnings=[]
    p=Path(args.pptx)
    if not p.exists(): print(f"File not found: {p}"); return 1
    try: prs=Presentation(p)
    except Exception as e: print(f"Cannot open PPTX: {e}"); return 1
    texts=[slide_text(s) for s in prs.slides]; alltext="\n".join(texts); low=alltext.lower()
    if len(prs.slides)<4: errors.append("Deck is too short to contain methodology, portfolio, detailed findings and next steps")
    if not any("assessment" in t.lower() and ("baseline" in t.lower() or "gap" in t.lower()) for t in texts): warnings.append("Methodology/evidence-rule slide not detected")
    if not any("validation" in t.lower() and "gap" in t.lower() for t in texts): warnings.append("Gap-vs-validation separation slide not detected")
    if not any("next" in t.lower() or "validate the findings" in t.lower() or "target sequence" in t.lower() for t in texts[-3:]): warnings.append("Closing/next-steps slide not detected near deck end")
    if not args.allow_placeholders and PLACEHOLDER_RE.search(alltext): errors.append("Unresolved template placeholders found in slides")
    td=None
    if args.review:
        root,td=open_package(args.review); man=collect(root)
        missing=[]; duplicates=[]
        for g in man["gaps"]:
            gid=str(g.get("id") or ""); title=str(g.get("title") or "")
            hits=[i+1 for i,t in enumerate(texts) if (gid and gid.lower() in t.lower()) or (title and title.lower() in t.lower())]
            if not hits: missing.append(f"{gid} - {title}")
            elif len(hits)>1: duplicates.append((gid,hits))
        if missing: (warnings if args.allow_subset else errors).append(f"Missing detailed gap slides for {len(missing)} gap(s): " + "; ".join(missing[:8]))
        for gid,hits in duplicates: warnings.append(f"{gid} appears on multiple slides {hits}; one-gap-per-slide traceability should remain explicit")
        # Detect slides that appear to contain more than one gap ID.
        for i,t in enumerate(texts,1):
            ids=[]
            for g in man["gaps"]:
                gid=str(g.get("id") or "")
                if gid and gid.lower() in t.lower(): ids.append(gid)
            if len(ids)>1: warnings.append(f"Slide {i} contains multiple gap IDs: {', '.join(ids)}")
        if td: td.cleanup()
    print(f"Slides: {len(prs.slides)}")
    return report(errors,warnings,"Architecture review slides validation")
if __name__=="__main__": sys.exit(main())
