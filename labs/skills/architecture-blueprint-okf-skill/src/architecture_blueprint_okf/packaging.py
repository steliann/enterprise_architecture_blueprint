from __future__ import annotations
from pathlib import Path
import zipfile

def package(blueprint: Path, output: Path)->None:
    blueprint=blueprint.resolve(); output=output.resolve(); output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output,"w",zipfile.ZIP_DEFLATED) as z:
        for path in sorted(blueprint.rglob("*")):
            if path.is_file(): z.write(path,Path(blueprint.name)/path.relative_to(blueprint))
    with zipfile.ZipFile(output,"r") as z:
        bad=z.testzip()
        if bad: raise RuntimeError(f"ZIP integrity failed at {bad}")
