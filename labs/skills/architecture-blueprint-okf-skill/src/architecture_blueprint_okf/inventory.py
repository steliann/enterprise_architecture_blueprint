from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass
from typing import Any
import re
from .frontmatter import load, FrontMatterError
from .markdown import inventory_ids

@dataclass
class Record:
    path: Path
    metadata: dict[str, Any]
    body: str

class BlueprintInventory:
    def __init__(self, blueprint: Path):
        self.blueprint=blueprint.resolve()
        self.records: dict[str, Record]={}
        self.by_type: dict[str, list[Record]]={}
        self.inventory_ids: dict[str, tuple[Path,str]]={}
        self.errors: list[str]=[]
        self.scan()

    def scan(self):
        for path in sorted(self.blueprint.rglob("*.md")):
            rel_parts = path.relative_to(self.blueprint).parts
            if any(part.startswith(".") for part in rel_parts) or (rel_parts and rel_parts[0] == "reports"):
                continue
            try:
                meta, body=load(path)
            except FrontMatterError as exc:
                self.errors.append(f"{path.relative_to(self.blueprint)}: {exc}")
                continue
            t=meta.get("type", "")
            if t in {"consumer-inventory","source-inventory","technology-inventory"}:
                for rid,title in inventory_ids(body).items():
                    if rid in self.inventory_ids:
                        self.errors.append(f"duplicate inventory ID {rid}")
                    self.inventory_ids[rid]=(path,title)
            rid=meta.get("id")
            if rid:
                if rid in self.records:
                    self.errors.append(f"duplicate record ID {rid}")
                rec=Record(path,meta,body)
                self.records[rid]=rec
                self.by_type.setdefault(t,[]).append(rec)

    def counts(self)->dict[str,int]:
        result={k:len(v) for k,v in self.by_type.items()}
        result["consumers"]=sum(1 for x in self.inventory_ids if x.startswith("CON-"))
        result["sources"]=sum(1 for x in self.inventory_ids if x.startswith("SRC-"))
        result["technologies"]=sum(1 for x in self.inventory_ids if x.startswith("TECH-"))
        return result

    def all_ids(self)->set[str]:
        return set(self.records) | set(self.inventory_ids)
