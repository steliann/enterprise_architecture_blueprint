from __future__ import annotations
from pathlib import Path
import yaml

def allocate(blueprint: Path, prefix: str)->str:
    path=blueprint/".okf"/"id-registry.yaml"
    data=yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    next_ids=data.setdefault("next_ids",{})
    number=int(next_ids.get(prefix,1))
    rid=f"{prefix}-{number:03d}"
    next_ids[prefix]=number+1
    path.write_text(yaml.safe_dump(data,sort_keys=False),encoding="utf-8")
    return rid
