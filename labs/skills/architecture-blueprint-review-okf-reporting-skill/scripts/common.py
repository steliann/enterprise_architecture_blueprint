from __future__ import annotations
import json, re, shutil, tempfile, zipfile
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc

ID_RE = re.compile(r"\b(?:UC|RC|DP|DF|QC|OC|ADR|SRC|CON|TEC|GAP|REC|VAL)-\d{3,}\b", re.I)
PLACEHOLDER_RE = re.compile(r"<[^>\n]{2,}>|\b(?:GAP|REC|VAL)-NNN\b")


def open_package(path: str | Path) -> Tuple[Path, tempfile.TemporaryDirectory | None]:
    p = Path(path)
    if p.is_dir():
        return normalize_root(p), None
    if not p.exists():
        raise FileNotFoundError(p)
    if p.suffix.lower() != ".zip":
        raise ValueError(f"Expected a directory or .zip package: {p}")
    td = tempfile.TemporaryDirectory(prefix="abr_okf_")
    with zipfile.ZipFile(p) as z:
        z.extractall(td.name)
    return normalize_root(Path(td.name)), td


def normalize_root(root: Path) -> Path:
    files = [x for x in root.iterdir() if x.name not in {"__MACOSX", ".DS_Store"}]
    dirs = [x for x in files if x.is_dir()]
    regular = [x for x in files if x.is_file()]
    if len(dirs) == 1 and not regular:
        return dirs[0]
    return root


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def parse_frontmatter(path: Path) -> Tuple[Dict[str, Any], str]:
    text = read_text(path)
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return {}, text
    parts = re.split(r"^---\s*$", text, maxsplit=2, flags=re.M)
    if len(parts) < 3:
        return {}, text
    try:
        data = yaml.safe_load(parts[1]) or {}
        if not isinstance(data, dict):
            data = {}
    except Exception as e:
        raise ValueError(f"Invalid YAML frontmatter in {path}: {e}")
    return data, parts[2].lstrip("\r\n")


def markdown_files(root: Path) -> List[Path]:
    return sorted([p for p in root.rglob("*.md") if "__MACOSX" not in p.parts])


def defined_ids(root: Path) -> Dict[str, Path]:
    out: Dict[str, Path] = {}
    for p in markdown_files(root):
        fm, body = parse_frontmatter(p)
        candidates: List[str] = []
        if isinstance(fm.get("id"), str):
            candidates.append(fm["id"].upper())
        m = re.match(r"((?:UC|RC|DP|DF|QC|OC|ADR|SRC|CON|TEC|GAP|REC|VAL)-\d{3,})", p.name, re.I)
        if m:
            candidates.append(m.group(1).upper())
        for hm in re.finditer(r"^#{1,4}\s+((?:SRC|CON|TEC)-\d{3,})\b", body, re.I | re.M):
            candidates.append(hm.group(1).upper())
        # tables/inventory definitions: ID at start of cell is treated as a definition for source/consumer/tech inventories
        for tm in re.finditer(r"^\|\s*((?:SRC|CON|TEC)-\d{3,})\s*\|", body, re.I | re.M):
            candidates.append(tm.group(1).upper())
        for cid in candidates:
            out.setdefault(cid, p)
    return out


def referenced_ids(root: Path) -> Dict[str, List[Path]]:
    refs: Dict[str, List[Path]] = {}
    for p in markdown_files(root):
        text = read_text(p)
        for token in sorted(set(x.upper() for x in ID_RE.findall(text))):
            refs.setdefault(token, []).append(p)
    return refs


def all_frontmatter(root: Path) -> List[Tuple[Path, Dict[str, Any], str]]:
    result = []
    for p in markdown_files(root):
        fm, body = parse_frontmatter(p)
        result.append((p, fm, body))
    return result


def heading_set(body: str) -> set[str]:
    return {re.sub(r"\s+", " ", m.group(1).strip()).lower() for m in re.finditer(r"^#{2,4}\s+(.+?)\s*$", body, re.M)}


def flatten_ids(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, str):
        found |= {x.upper() for x in ID_RE.findall(value)}
    elif isinstance(value, dict):
        for v in value.values():
            found |= flatten_ids(v)
    elif isinstance(value, list):
        for v in value:
            found |= flatten_ids(v)
    return found


def normalize_enum(v: Any) -> str:
    return str(v).strip().lower().replace(" ", "_").replace("-", "_")


def report(errors: List[str], warnings: List[str], title: str) -> int:
    print(f"\n{title}")
    print("=" * len(title))
    for e in errors:
        print(f"ERROR: {e}")
    for w in warnings:
        print(f"WARN : {w}")
    if not errors and not warnings:
        print("PASS : no errors or warnings")
    else:
        print(f"Summary: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


def write_json(obj: Any, path: str | Path):
    Path(path).write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")
