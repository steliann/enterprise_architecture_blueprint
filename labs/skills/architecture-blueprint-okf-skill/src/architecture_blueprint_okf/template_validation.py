from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass, field
import json
from jsonschema import Draft202012Validator
from .registry import Registry
from .rendering import Renderer
from .frontmatter import parse_text
from .markdown import headings

@dataclass
class TemplateIssue:
    severity: str
    path: str
    message: str

@dataclass
class TemplateResult:
    issues: list[TemplateIssue]=field(default_factory=list)
    @property
    def ok(self): return not any(x.severity=="error" for x in self.issues)
    def add(self,s,p,m): self.issues.append(TemplateIssue(s,p,m))
    def as_dict(self): return {"ok":self.ok,"issues":[x.__dict__ for x in self.issues]}

def validate_templates(skill_root: Path)->TemplateResult:
    result=TemplateResult(); reg=Registry(skill_root); renderer=Renderer(skill_root)
    prefixes=set(); collections=set()
    for name,spec in reg.documents.items():
        tpath=skill_root/"templates"/spec["template"]
        spath=skill_root/spec["schema"]
        if not tpath.exists(): result.add("error",str(tpath.relative_to(skill_root)),"template is missing"); continue
        if not spath.exists(): result.add("error",str(spath.relative_to(skill_root)),"schema is missing"); continue
        try:
            schema=json.loads(spath.read_text(encoding="utf-8")); Draft202012Validator.check_schema(schema)
        except Exception as exc:
            result.add("error",str(spath.relative_to(skill_root)),f"invalid JSON Schema: {exc}"); continue
        default_status = "Proposed" if name == "architecture-decision-record" else "Candidate"
        context={"customer":"Example","solution":"Example Solution","inventory":[],"id":f"{spec.get('id_prefix','UC')}-001","title":"Example Record","status":default_status,"confidence":"Low","collection":spec.get("collection","example"),"record_type":name,"label":"Example Records","purpose":"Example purpose.","records":[]}
        try:
            rendered=renderer.render(spec["template"],**context)
            meta,body=parse_text(rendered)
        except Exception as exc:
            result.add("error",str(tpath.relative_to(skill_root)),f"template cannot render or parse: {exc}"); continue
        for err in Draft202012Validator(schema).iter_errors(meta):
            result.add("error",str(tpath.relative_to(skill_root)),f"rendered front matter fails schema: {err.message}")
        actual=headings(body,2)
        for h in spec.get("required_headings",[]):
            if h not in actual: result.add("error",str(tpath.relative_to(skill_root)),f"registered heading absent from template: {h}")
        expected=spec.get("schema_version")
        if expected is not None and meta.get("schema_version")!=expected:
            result.add("error",str(tpath.relative_to(skill_root)),f"template schema_version {meta.get('schema_version')} does not match registry {expected}")
        if spec.get("id_prefix"):
            if spec["id_prefix"] in prefixes: result.add("error","templates/template-registry.yaml",f"duplicate ID prefix {spec['id_prefix']}")
            prefixes.add(spec["id_prefix"])
        if spec.get("collection"):
            if spec["collection"] in collections: result.add("error","templates/template-registry.yaml",f"duplicate collection {spec['collection']}")
            collections.add(spec["collection"])
    return result
