from __future__ import annotations
from pathlib import Path
from datetime import date
import yaml
from .registry import Registry

def lock_data(skill_root: Path)->dict:
    reg=Registry(skill_root)
    return {
      "template_set":reg.template_set,
      "template_set_version":reg.template_set_version,
      "okf_version":reg.okf_version,
      "registry_sha256":reg.sha256,
      "locked_on":date.today().isoformat(),
      "documents":{name:{"schema_version":spec.get("schema_version",1)} for name,spec in reg.documents.items()},
    }

def write_lock(skill_root: Path, blueprint: Path)->Path:
    path=blueprint/".okf"/"template-lock.yaml"
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(yaml.safe_dump(lock_data(skill_root),sort_keys=False),encoding="utf-8")
    return path
