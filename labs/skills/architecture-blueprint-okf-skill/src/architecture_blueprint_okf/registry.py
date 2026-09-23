from __future__ import annotations
from pathlib import Path
from typing import Any
import hashlib
import yaml

class Registry:
    def __init__(self, skill_root: Path):
        self.skill_root=skill_root.resolve()
        self.path=self.skill_root / "templates" / "template-registry.yaml"
        self.data=yaml.safe_load(self.path.read_text(encoding="utf-8"))
        self.documents=self.data["documents"]

    @property
    def template_set(self)->str:
        return self.data["template_set"]

    @property
    def template_set_version(self)->str:
        return str(self.data["template_set_version"])

    @property
    def okf_version(self)->str:
        return str(self.data["okf_version"])

    @property
    def sha256(self)->str:
        return hashlib.sha256(self.path.read_bytes()).hexdigest()

    def record_specs(self):
        return {k:v for k,v in self.documents.items() if v.get("kind")=="record"}

    def top_specs(self):
        return {k:v for k,v in self.documents.items() if v.get("kind") in {"top-level","inventory"}}

    def spec_for_type(self, type_name: str) -> tuple[str, dict[str, Any]]:
        if type_name not in self.documents:
            raise KeyError(f"unknown document type: {type_name}")
        return type_name, self.documents[type_name]
