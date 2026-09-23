from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any
import json, re, yaml
from jsonschema import Draft202012Validator
from .frontmatter import load, FrontMatterError
from .markdown import headings, links, relative_link_target, inventory_ids
from .inventory import BlueprintInventory
from .registry import Registry

@dataclass
class Issue:
    severity: str
    code: str
    path: str
    message: str

@dataclass
class ValidationResult:
    issues: list[Issue]=field(default_factory=list)
    counts: dict[str,int]=field(default_factory=dict)
    @property
    def errors(self): return [x for x in self.issues if x.severity=="error"]
    @property
    def warnings(self): return [x for x in self.issues if x.severity=="warning"]
    @property
    def ok(self): return not self.errors
    def add(self,severity,code,path,message): self.issues.append(Issue(severity,code,path,message))
    def as_dict(self): return {"ok":self.ok,"counts":self.counts,"issues":[x.__dict__ for x in self.issues]}

class Validator:
    def __init__(self, skill_root: Path):
        self.skill_root=skill_root.resolve()
        self.registry=Registry(self.skill_root)
        self.relationships=yaml.safe_load((self.skill_root/"config/relationship-rules.yaml").read_text(encoding="utf-8"))["rules"]

    def validate(self, blueprint: Path, strict: bool=False)->ValidationResult:
        blueprint=blueprint.resolve(); result=ValidationResult()
        inv=BlueprintInventory(blueprint); result.counts=inv.counts()
        for err in inv.errors: result.add("error","inventory",str(blueprint),err)
        all_ids=inv.all_ids()
        # Top-level and inventory documents
        for type_name,spec in self.registry.top_specs().items():
            path=blueprint/spec["path"]
            if not path.exists():
                result.add("error","missing-file",spec["path"],f"required {type_name} document is missing")
                continue
            self._validate_document(path, blueprint, type_name, spec, result, strict)
        # Collection indexes and record documents
        for type_name,spec in self.registry.record_specs().items():
            collection=blueprint/spec["collection"]
            if not collection.is_dir():
                result.add("error","missing-folder",spec["collection"],"required collection folder is missing")
                continue
            index=collection/"index.md"
            if not index.exists():
                result.add("error","missing-index",str(index.relative_to(blueprint)),"collection index.md is missing")
            else:
                self._validate_collection_index(index, blueprint, type_name, spec, result)
            for path in sorted(collection.glob("*.md")):
                if path.name=="index.md": continue
                self._validate_document(path, blueprint, type_name, spec, result, strict)
                if not re.match(spec["filename_pattern"],path.name):
                    result.add("error","filename",str(path.relative_to(blueprint)),f"filename does not match {spec['filename_pattern']}")
                try: meta,_=load(path)
                except FrontMatterError: continue
                rid=meta.get("id","")
                if rid and not path.name.startswith(rid+"-"):
                    result.add("error","filename-id",str(path.relative_to(blueprint)),f"filename does not start with record ID {rid}")
        # Record references
        for rid,rec in inv.records.items():
            for key,value in rec.metadata.items():
                if isinstance(value,list):
                    for item in value:
                        if isinstance(item,str) and re.match(r"^(CON|SRC|TECH|UC|RC|DP|DF|QC|OC|ADR)-\d{3}$",item) and item not in all_ids:
                            result.add("error","missing-id",str(rec.path.relative_to(blueprint)),f"{key} references missing ID {item}")
        # Inverse relationships
        for rule in self.relationships:
            left_records=inv.by_type.get(rule["left_type"],[])
            for rec in left_records:
                for target_id in rec.metadata.get(rule["left_field"],[]) or []:
                    target=inv.records.get(target_id)
                    if not target: continue
                    inverse=target.metadata.get(rule["right_field"],[]) or []
                    if rec.metadata.get("id") not in inverse:
                        sev="error" if strict else "warning"
                        result.add(sev,"inverse-link",str(rec.path.relative_to(blueprint)),f"{target_id}.{rule['right_field']} does not reference {rec.metadata.get('id')}")
        # Template lock
        lock=blueprint/".okf"/"template-lock.yaml"
        if not lock.exists():
            result.add("error","template-lock",str(lock.relative_to(blueprint)),"template lock is missing")
        else:
            try: data=yaml.safe_load(lock.read_text(encoding="utf-8")) or {}
            except Exception as exc: result.add("error","template-lock",str(lock.relative_to(blueprint)),str(exc)); data={}
            if str(data.get("template_set_version"))!=self.registry.template_set_version:
                result.add("warning","template-version",str(lock.relative_to(blueprint)),f"blueprint uses {data.get('template_set_version')}; current is {self.registry.template_set_version}")
            if data.get("registry_sha256")!=self.registry.sha256:
                result.add("warning","template-hash",str(lock.relative_to(blueprint)),"template registry hash differs from current skill")
            locked_docs=data.get("documents",{}) or {}
            for name,spec in self.registry.documents.items():
                locked=(locked_docs.get(name) or {}).get("schema_version")
                if locked!=spec.get("schema_version",1):
                    result.add("warning","template-schema-lock",str(lock.relative_to(blueprint)),f"{name} locked schema {locked}; current is {spec.get('schema_version',1)}")
        self._write_reports(blueprint,result)
        return result


    def _validate_collection_index(self,index,blueprint,type_name,spec,result):
        rel=str(index.relative_to(blueprint))
        try: meta,body=load(index)
        except FrontMatterError as exc:
            result.add("error","frontmatter",rel,str(exc)); return
        schema=json.loads((self.skill_root/"schemas/collection-index.schema.json").read_text(encoding="utf-8"))
        for err in Draft202012Validator(schema).iter_errors(meta):
            result.add("error","schema",rel,f"{'.'.join(map(str,err.path)) or '<root>'}: {err.message}")
        required=["Purpose","Records","Maintenance Notes"]
        actual=headings(body,2)
        for h in required:
            if h not in actual: result.add("error","missing-heading",rel,f"missing heading: {h}")
        linked={x.split('#',1)[0] for x in links(body) if x.split('#',1)[0].endswith('.md')}
        expected={p.name for p in index.parent.glob('*.md') if p.name!='index.md'}
        missing=expected-linked
        extra={x for x in linked if x!='index.md'}-expected
        for name in sorted(missing): result.add("error","index-coverage",rel,f"record missing from index: {name}")
        for name in sorted(extra): result.add("error","index-coverage",rel,f"index references non-record file: {name}")

    def _validate_document(self,path,blueprint,type_name,spec,result,strict):
        rel=str(path.relative_to(blueprint))
        try: meta,body=load(path)
        except FrontMatterError as exc:
            result.add("error","frontmatter",rel,str(exc)); return
        expected_schema_version=spec.get("schema_version")
        if expected_schema_version is not None and meta.get("schema_version")!=expected_schema_version:
            result.add("error","schema-version",rel,f"document schema_version {meta.get('schema_version')} does not match registry {expected_schema_version}")
        schema_path=self.skill_root/spec["schema"]
        schema=json.loads(schema_path.read_text(encoding="utf-8"))
        validator=Draft202012Validator(schema)
        for err in sorted(validator.iter_errors(meta),key=lambda e:list(e.path)):
            result.add("error","schema",rel,f"{'.'.join(map(str,err.path)) or '<root>'}: {err.message}")
        actual=headings(body,2)
        required=spec.get("required_headings",[])
        missing=[h for h in required if h not in actual]
        for h in missing: result.add("error","missing-heading",rel,f"missing heading: {h}")
        indexes=[actual.index(h) for h in required if h in actual]
        if indexes!=sorted(indexes): result.add("error","heading-order",rel,"required headings are out of order")
        placeholder=re.compile(self.registry.data["placeholder_pattern"])
        if placeholder.search(body):
            sev="error" if strict else "warning"
            result.add(sev,"placeholder",rel,"unresolved template placeholder found")
        for target in links(body):
            resolved=relative_link_target(path,target)
            if resolved is not None and not resolved.exists():
                result.add("error","broken-link",rel,f"link target does not exist: {target}")

    def _write_reports(self,blueprint,result):
        internal=blueprint/".okf"; internal.mkdir(exist_ok=True)
        (internal/"validation-report.json").write_text(json.dumps(result.as_dict(),indent=2)+"\n",encoding="utf-8")
        reports=blueprint/"reports"; reports.mkdir(exist_ok=True)
        lines=["# Validation Report","",f"**Result:** {'PASS' if result.ok else 'FAIL'}","",f"Errors: {len(result.errors)}  ",f"Warnings: {len(result.warnings)}","","## Issues",""]
        if not result.issues: lines.append("No issues found.")
        else:
            lines += [f"- **{i.severity.upper()} {i.code}** — `{i.path}`: {i.message}" for i in result.issues]
        (reports/"validation-report.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
