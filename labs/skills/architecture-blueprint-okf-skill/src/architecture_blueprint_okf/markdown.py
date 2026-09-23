from __future__ import annotations
from pathlib import Path
import re

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
INVENTORY_ID_RE = re.compile(r"^###\s+((?:CON|SRC|TECH)-\d{3})\s+[—-]\s+(.+?)\s*$", re.MULTILINE)

def headings(body: str, level: int = 2) -> list[str]:
    result=[]
    for marks, title in HEADING_RE.findall(body):
        if len(marks)==level:
            result.append(re.sub(r"\s+#+$", "", title).strip())
    return result

def links(body: str) -> list[str]:
    return [x.strip() for x in LINK_RE.findall(body)]

def inventory_ids(body: str) -> dict[str, str]:
    return {record_id:title.strip() for record_id,title in INVENTORY_ID_RE.findall(body)}

def slugify(value: str) -> str:
    value=value.lower().replace("&", " and ")
    value=re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "untitled"

def relative_link_target(source_path: Path, target: str) -> Path | None:
    target=target.split("#",1)[0].strip()
    if not target or target.startswith(("http://","https://","mailto:","#")):
        return None
    return (source_path.parent / target).resolve()
