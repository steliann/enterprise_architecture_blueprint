from __future__ import annotations
from pathlib import Path
from datetime import date
import hashlib, json

TEXT_SUFFIXES={".txt",".md",".csv",".tsv",".json",".yaml",".yml",".vtt"}

def sha256(path: Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def index_evidence(evidence_dir: Path, blueprint: Path)->dict:
    ledger=blueprint/".okf"/"evidence-ledger.jsonl"
    existing=[]
    hashes=set()
    if ledger.exists():
        for line in ledger.read_text(encoding="utf-8").splitlines():
            if line.strip():
                item=json.loads(line); existing.append(item); hashes.add(item.get("content_hash"))
    next_num=max([int(x["id"].split("-")[1]) for x in existing if x.get("id","").startswith("EVD-")] or [0])+1
    added=[]
    for path in sorted(evidence_dir.rglob("*")):
        if not path.is_file(): continue
        digest=sha256(path)
        if digest in hashes: continue
        item={
          "id":f"EVD-{next_num:04d}",
          "source_file":str(path.resolve()),
          "source_type":"transcript" if path.suffix.lower() in {".vtt",".txt"} else "document",
          "session_or_date":date.today().isoformat(),
          "location":"file",
          "content_hash":digest,
          "summary":"Indexed for model review; detailed claim extraction pending.",
        }
        next_num+=1; added.append(item); existing.append(item); hashes.add(digest)
    ledger.parent.mkdir(parents=True,exist_ok=True)
    ledger.write_text("".join(json.dumps(x,ensure_ascii=False)+"\n" for x in existing),encoding="utf-8")
    return {"added":len(added),"total":len(existing),"items":added}
