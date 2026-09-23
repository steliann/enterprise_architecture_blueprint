from __future__ import annotations
from pathlib import Path
import argparse, json, sys, shutil, yaml
from .initializer import initialize
from .registry import Registry
from .rendering import Renderer
from .ids import allocate
from .markdown import slugify
from .validator import Validator
from .packaging import package
from .evidence import index_evidence
from .migration import Migrator
from .inventory import BlueprintInventory
from .indexes import rebuild as rebuild_indexes
from .locking import write_lock
from .template_validation import validate_templates

SKILL_ROOT=Path(__file__).resolve().parents[2]
PREFIX_BY_TYPE={"business-use-case":"UC","required-capability":"RC","data-product":"DP","data-flow":"DF","quality-control":"QC","operational-capability":"OC","architecture-decision-record":"ADR"}

def cmd_init(a):
    initialize(SKILL_ROOT,Path(a.output),a.customer,a.solution,a.force)
    print(f"Created {Path(a.output).resolve()}")

def cmd_new(a):
    bp=Path(a.blueprint).resolve(); reg=Registry(SKILL_ROOT); _,spec=reg.spec_for_type(a.type)
    if spec.get("kind")!="record": raise SystemExit("new-record requires a record type")
    rid=allocate(bp,PREFIX_BY_TYPE[a.type]); renderer=Renderer(SKILL_ROOT)
    path=bp/spec["collection"]/f"{rid}-{slugify(a.title)}.md"
    path.write_text(renderer.render(spec["template"],id=rid,title=a.title,status=a.status,confidence=a.confidence),encoding="utf-8")
    print(path)

def cmd_validate(a):
    result=Validator(SKILL_ROOT).validate(Path(a.blueprint),a.strict)
    print(json.dumps(result.as_dict(),indent=2))
    raise SystemExit(0 if result.ok else 1)

def cmd_package(a):
    bp=Path(a.blueprint); out=Path(a.output) if a.output else bp.with_suffix(".zip")
    result=Validator(SKILL_ROOT).validate(bp,a.strict)
    if not result.ok and not a.allow_invalid: raise SystemExit("validation failed; use --allow-invalid to package anyway")
    package(bp,out); print(out.resolve())

def cmd_evidence(a): print(json.dumps(index_evidence(Path(a.evidence),Path(a.blueprint)),indent=2))
def cmd_inventory(a): print(json.dumps(BlueprintInventory(Path(a.blueprint)).counts(),indent=2))
def cmd_indexes(a):
    rebuild_indexes(SKILL_ROOT,Path(a.blueprint)); print(Path(a.blueprint).resolve())
def cmd_lock(a):
    print(write_lock(SKILL_ROOT,Path(a.blueprint)))
def cmd_templates(a):
    result=validate_templates(SKILL_ROOT); print(json.dumps(result.as_dict(),indent=2)); raise SystemExit(0 if result.ok else 1)
def cmd_migrate(a):
    m=Migrator(SKILL_ROOT); changes=m.plan(Path(a.blueprint))
    if a.apply: changes=m.apply(Path(a.blueprint))
    print(json.dumps(changes,indent=2))

def build_parser():
    p=argparse.ArgumentParser(prog="blueprint-okf")
    sub=p.add_subparsers(dest="command",required=True)
    x=sub.add_parser("init"); x.add_argument("--customer",required=True); x.add_argument("--solution",required=True); x.add_argument("--output",required=True); x.add_argument("--force",action="store_true"); x.set_defaults(func=cmd_init)
    x=sub.add_parser("new-record"); x.add_argument("blueprint"); x.add_argument("--type",required=True,choices=PREFIX_BY_TYPE); x.add_argument("--title",required=True); x.add_argument("--status",default="Candidate"); x.add_argument("--confidence",default="Low"); x.set_defaults(func=cmd_new)
    x=sub.add_parser("validate"); x.add_argument("blueprint"); x.add_argument("--strict",action="store_true"); x.set_defaults(func=cmd_validate)
    x=sub.add_parser("package"); x.add_argument("blueprint"); x.add_argument("--output"); x.add_argument("--strict",action="store_true"); x.add_argument("--allow-invalid",action="store_true"); x.set_defaults(func=cmd_package)
    x=sub.add_parser("index-evidence"); x.add_argument("evidence"); x.add_argument("--blueprint",required=True); x.set_defaults(func=cmd_evidence)
    x=sub.add_parser("inventory"); x.add_argument("blueprint"); x.set_defaults(func=cmd_inventory)
    x=sub.add_parser("refresh-indexes"); x.add_argument("blueprint"); x.set_defaults(func=cmd_indexes)
    x=sub.add_parser("template-lock"); x.add_argument("blueprint"); x.set_defaults(func=cmd_lock)
    x=sub.add_parser("validate-templates"); x.set_defaults(func=cmd_templates)
    x=sub.add_parser("migrate"); x.add_argument("blueprint"); g=x.add_mutually_exclusive_group(); g.add_argument("--dry-run",action="store_true"); g.add_argument("--apply",action="store_true"); x.set_defaults(func=cmd_migrate)
    return p

def main():
    args=build_parser().parse_args(); args.func(args)

if __name__=="__main__": main()
