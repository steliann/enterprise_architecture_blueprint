from __future__ import annotations
from pathlib import Path
from .frontmatter import load
from .inventory import BlueprintInventory
from .initializer import LABELS, PURPOSES
from .rendering import Renderer

ORDER=[
  "business-use-case","required-capability","data-product","data-flow",
  "quality-control","operational-capability","architecture-decision-record"
]

def rebuild(skill_root: Path, blueprint: Path)->None:
    blueprint=blueprint.resolve()
    renderer=Renderer(skill_root)
    reg=renderer.registry
    root_meta,_=load(blueprint/"index.md")
    customer=root_meta.get("customer","Unknown Customer")
    solution=root_meta.get("solution","Unknown Solution")
    inv=BlueprintInventory(blueprint)
    inventory_rows=[]
    for type_name in ORDER:
        spec=reg.record_specs()[type_name]
        records=[]
        for rec in sorted(inv.by_type.get(type_name,[]),key=lambda x:x.metadata.get("id","")):
            records.append({
              "id":rec.metadata.get("id",""),
              "title":rec.metadata.get("title",""),
              "status":rec.metadata.get("status",""),
              "confidence":rec.metadata.get("confidence",""),
              "filename":rec.path.name,
            })
        content=renderer.render(
          spec["collection_index_template"],collection=spec["collection"],record_type=type_name,
          label=LABELS[type_name],purpose=PURPOSES[type_name],records=records,
        )
        (blueprint/spec["collection"]/"index.md").write_text(content,encoding="utf-8")
        inventory_rows.append({"label":LABELS[type_name],"count":len(records)})
    inventory_rows.extend([
      {"label":"Consumers","count":inv.counts().get("consumers",0)},
      {"label":"Sources","count":inv.counts().get("sources",0)},
      {"label":"Technologies","count":inv.counts().get("technologies",0)},
    ])
    package_spec=reg.documents["package-index"]
    (blueprint/"index.md").write_text(renderer.render(package_spec["template"],customer=customer,solution=solution,inventory=inventory_rows),encoding="utf-8")
