from __future__ import annotations
from pathlib import Path
from datetime import date
from .registry import Registry
from .frontmatter import load, write, FrontMatterError
from .markdown import headings

class Migrator:
    def __init__(self, skill_root: Path): self.registry=Registry(skill_root)
    def plan(self, blueprint: Path)->list[dict]:
        changes=[]
        specs={}
        for name,spec in self.registry.top_specs().items(): specs[blueprint/spec["path"]]=(name,spec)
        for name,spec in self.registry.record_specs().items():
            for p in (blueprint/spec["collection"]).glob("*.md") if (blueprint/spec["collection"]).exists() else []:
                if p.name!="index.md": specs[p]=(name,spec)
        for path,(name,spec) in specs.items():
            if not path.exists(): continue
            try: meta,body=load(path)
            except FrontMatterError: continue
            actual=headings(body,2)
            missing=[h for h in spec.get("required_headings",[]) if h not in actual]
            metadata=[]
            if "type" not in meta: metadata.append("type")
            expected_version=spec.get("schema_version",1)
            version_change=meta.get("schema_version")!=expected_version
            if missing or metadata or version_change:
                changes.append({"path":str(path.relative_to(blueprint)),"missing_headings":missing,"missing_metadata":metadata,"type":name,"from_schema_version":meta.get("schema_version"),"to_schema_version":expected_version})
        return changes
    def apply(self, blueprint: Path)->list[dict]:
        changes=self.plan(blueprint)
        for change in changes:
            path=blueprint/change["path"]
            meta,body=load(path)
            if "type" in change["missing_metadata"]: meta["type"]=change["type"]
            meta["schema_version"]=change["to_schema_version"]
            for h in change["missing_headings"]:
                body=body.rstrip()+f"\n\n## {h}\n\n<Added by conservative template migration; content requires review.>\n"
            meta["last_updated"]=date.today().isoformat()
            write(path,meta,body)
        return changes
