from __future__ import annotations
from pathlib import Path
from typing import Any
import re
import yaml

_FRONT = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.DOTALL)

class FrontMatterError(ValueError):
    pass

def parse_text(text: str) -> tuple[dict[str, Any], str]:
    match = _FRONT.match(text)
    if not match:
        raise FrontMatterError("missing YAML front matter")
    try:
        data = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        raise FrontMatterError(str(exc)) from exc
    if not isinstance(data, dict):
        raise FrontMatterError("front matter must be a mapping")
    return data, text[match.end():]

def load(path: Path) -> tuple[dict[str, Any], str]:
    return parse_text(path.read_text(encoding="utf-8"))

def dump(data: dict[str, Any], body: str) -> str:
    yaml_text = yaml.safe_dump(data, sort_keys=False, allow_unicode=True).rstrip()
    return f"---\n{yaml_text}\n---\n\n{body.lstrip()}"

def write(path: Path, data: dict[str, Any], body: str) -> None:
    path.write_text(dump(data, body), encoding="utf-8")
