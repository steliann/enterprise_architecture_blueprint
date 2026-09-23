from __future__ import annotations
from pathlib import Path
from datetime import date
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from .registry import Registry

class Renderer:
    def __init__(self, skill_root: Path):
        self.skill_root=skill_root.resolve()
        self.registry=Registry(self.skill_root)
        self.env=Environment(
            loader=FileSystemLoader(str(self.skill_root / "templates")),
            undefined=StrictUndefined,
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render(self, template_path: str, **context)->str:
        base={
            "date": date.today().isoformat(),
            "okf_version": self.registry.okf_version,
            "template_set": self.registry.template_set,
            "template_set_version": self.registry.template_set_version,
        }
        base.update(context)
        return self.env.get_template(template_path).render(**base).rstrip()+"\n"
