from __future__ import annotations
from pathlib import Path
from datetime import date
import hashlib
from .registry import Registry
from .rendering import Renderer
from .locking import write_lock

LABELS={
 "business-use-case":"Business Use Cases",
 "required-capability":"Required Capabilities",
 "data-product":"Data Products",
 "data-flow":"Data Flows",
 "quality-control":"Quality Controls",
 "operational-capability":"Operational Capabilities",
 "architecture-decision-record":"Architecture Decision Records",
}
PURPOSES={
 "business-use-case":"Business outcomes, decisions, accountabilities, and obligations supported by the solution.",
 "required-capability":"Implementation-independent functional and non-functional abilities required by the use cases.",
 "data-product":"Managed information offerings made available to defined consumers.",
 "data-flow":"Principal logical movements and transformations that produce or update products.",
 "quality-control":"Preventive, detective, and corrective mechanisms that establish trust.",
 "operational-capability":"Repeatable abilities to run, observe, recover, secure, scale, deploy, and retire the solution.",
 "architecture-decision-record":"Material architecture choices, rationale status, alternatives, and consequences.",
}

def initialize(skill_root: Path, output: Path, customer: str, solution: str, force: bool=False)->None:
    output=output.resolve()
    if output.exists() and any(output.iterdir()) and not force:
        raise FileExistsError(f"output is not empty: {output}")
    output.mkdir(parents=True, exist_ok=True)
    renderer=Renderer(skill_root)
    reg=renderer.registry
    context={"customer":customer,"solution":solution,"inventory":[]}
    for _,spec in reg.top_specs().items():
        path=output/spec["path"]
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(renderer.render(spec["template"], **context),encoding="utf-8")
    for type_name,spec in reg.record_specs().items():
        collection=output/spec["collection"]
        collection.mkdir(parents=True,exist_ok=True)
        index=renderer.render(spec["collection_index_template"], collection=spec["collection"], record_type=type_name, label=LABELS[type_name], purpose=PURPOSES[type_name], records=[])
        (collection/"index.md").write_text(index,encoding="utf-8")
    (output/"reports").mkdir(exist_ok=True)
    (output/"reports/change-summary.md").write_text("# Change Summary\n\nInitial blueprint structure created.\n",encoding="utf-8")
    (output/"reports/open-questions.md").write_text("# Open Questions\n\nNo questions have been extracted yet.\n",encoding="utf-8")
    (output/"reports/validation-report.md").write_text("# Validation Report\n\nValidation has not yet been run.\n",encoding="utf-8")
    internal=output/".okf"; internal.mkdir(exist_ok=True)
    for tpl,name in [
      ("internal/manifest.yaml.j2","manifest.yaml"),
      ("internal/id-registry.yaml.j2","id-registry.yaml"),
      ("internal/claim-map.yaml.j2","claim-map.yaml"),
    ]:
        (internal/name).write_text(renderer.render(tpl,customer=customer,solution=solution),encoding="utf-8")
    write_lock(skill_root, output)
    (internal/"evidence-ledger.jsonl").write_text("",encoding="utf-8")
    (internal/"validation-report.json").write_text("{}\n",encoding="utf-8")
