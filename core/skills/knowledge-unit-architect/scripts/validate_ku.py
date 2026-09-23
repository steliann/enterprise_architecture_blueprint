#!/usr/bin/env python3
"""Validate Knowledge Unit (v4 schema, canonical 11-section body) markdown files.

Usage:
    python validate_ku.py <ku_file.md> [more_files...] [--json]
    python validate_ku.py --corpus <directory> [--json]

File checks: frontmatter fields/enums/dates, canonical section order (6 required +
5 optional sections), subsection formats (TOGAF, Anti-Patterns), bundle-path
conformance, size heuristics.
Corpus checks (automatic when >1 file, or via --corpus): duplicate IDs, bundle
path/ID match, dangling relationship references, supersession reciprocity.

ID scheme and file location follow references/naming-standard.md: IDs are
ADL-NNN (Architecture area + Deployment scope + TOGAF Layer + sequence), and the
canonical path is knowledge-units/<ID>/knowledge-unit.md.

Exit codes: 0 = clean, 1 = warnings only, 2 = errors.
Requires: pyyaml (pip install pyyaml --break-system-packages if missing).
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write("pyyaml missing: pip install pyyaml --break-system-packages\n")
    sys.exit(2)

STATUS = {"Draft", "Proposed", "Approved", "Deprecated", "Superseded"}
CONFIDENCE = {"High", "Medium", "Low"}
SOURCE_BASIS = {"Field Experience", "Customer ADRs", "Product Documentation", "Architecture Review"}
# togaf_layers metadata may include Security; the ID's 3rd letter (below) is narrower (B/A/D/T only).
TOGAF = {"Business", "Data", "Application", "Technology", "Security"}
PILLARS = ["Reliability", "Operational Excellence", "Security",
           "Performance Efficiency", "Cost Optimization", "Sustainability"]
REQUIRED_FIELDS = ["id", "yaml_version", "title", "status", "tier", "confidence",
                   "source_basis", "togaf_layers", "well_architected_pillars",
                   "qlik_products", "external_technologies", "deployment",
                   "owner", "created", "last_reviewed", "review_by", "tags"]

# Canonical body: eleven H2 sections in this exact order per the naming/authoring standard.
REQUIRED_SECTIONS = ["Context", "Guidance", "TOGAF Impact", "Well-Architected Impact",
                     "Consequences", "Anti-Patterns"]
OPTIONAL_SECTIONS = ["Boundaries", "Customer-Ecosystem Notes",
                     "Field Qualification Questions (Tier 3)",
                     "Implementation Guidance", "Operationalization Guidance"]
CANON = ["Context", "Boundaries", "Guidance", "TOGAF Impact", "Well-Architected Impact",
         "Consequences", "Anti-Patterns", "Customer-Ecosystem Notes",
         "Field Qualification Questions (Tier 3)", "Implementation Guidance",
         "Operationalization Guidance"]
ALIASES = {  # accepted with a warning, normalized to the current canonical name
    "Operationalization": "Operationalization Guidance",
    "Field Qualification Questions": "Field Qualification Questions (Tier 3)",
}
# ID scheme per references/naming-standard.md: Architecture area / Deployment scope / TOGAF Layer.
AREA_CODES = set("AMTQIGO")       # Data Analytics, Data Movement, Data Transformation,
                                   # Data Quality, AI, Data Governance, Operations/DevOps
DEPLOYMENT_CODES = set("MCHA")    # Client-managed, Cloud, Hybrid, All
LAYER_CODES = set("BADT")         # Business, Application, Data, Technology (no Security here)
ID_RE = re.compile(
    r"^[{a}][{d}][{l}]-\d{{3}}$".format(
        a="".join(sorted(AREA_CODES)), d="".join(sorted(DEPLOYMENT_CODES)), l="".join(sorted(LAYER_CODES))
    )
)
LEGACY_ID_RE = re.compile(r"^[A-Z]{2,10}-\d{3}$")  # old product-prefix scheme (e.g. REPL-003), retired
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PLACEHOLDER_RE = re.compile(r"\[(Name / Role|Owner name|Title|Asset name or link|the customer problem|The pattern|TBD)", re.I)
ANTIPAT_RE = re.compile(r"^###\s+Anti-pattern\s+(\d+)\s+—\s+\S", re.M)
BUNDLE_FILENAME = "knowledge-unit.md"


def parse(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not m:
        return None, text
    return yaml.safe_load(m.group(1)), m.group(2)


def is_date(v):
    return DATE_RE.match(str(v).strip() if not isinstance(v, date) else v.isoformat()) is not None


def to_date(v):
    if isinstance(v, date):
        return v
    try:
        return date.fromisoformat(str(v).strip())
    except ValueError:
        return None


def na_marked(content):
    return bool(re.search(r"\bN/?A\b", content or ""))


def check(path):
    errors, warnings = [], []
    try:
        fm, body = parse(path)
    except yaml.YAMLError as e:
        return [f"frontmatter is not valid YAML: {e}"], []
    if fm is None:
        return ["no YAML frontmatter block found"], []

    # --- frontmatter: required fields ---
    for f in REQUIRED_FIELDS:
        if fm.get(f) in (None, "", []):
            errors.append(f"required field missing or empty: {f}")

    ku_id = str(fm.get("id", ""))
    if ku_id and not ID_RE.match(ku_id):
        if "XXX" in ku_id:
            warnings.append(f"id '{ku_id}' is a placeholder sequence — fine until allocated")
        elif LEGACY_ID_RE.match(ku_id):
            errors.append(
                f"id '{ku_id}' follows the retired product-prefix scheme (e.g. REPL-003) — "
                "allocate a new ID as Area+Deployment+Layer-NNN per references/naming-standard.md "
                f"(area in {sorted(AREA_CODES)}, deployment in {sorted(DEPLOYMENT_CODES)}, "
                f"layer in {sorted(LAYER_CODES)})")
        else:
            errors.append(
                f"id '{ku_id}' does not match ADL-NNN per references/naming-standard.md "
                f"(area in {sorted(AREA_CODES)}, deployment in {sorted(DEPLOYMENT_CODES)}, "
                f"layer in {sorted(LAYER_CODES)})")
    if fm.get("status") and fm["status"] not in STATUS:
        errors.append(f"status '{fm['status']}' not in {sorted(STATUS)}")
    if fm.get("tier") not in (1, 2, 3, None):
        errors.append(f"tier '{fm.get('tier')}' must be 1, 2 or 3")
    if fm.get("confidence") and fm["confidence"] not in CONFIDENCE:
        errors.append(f"confidence '{fm['confidence']}' not in {sorted(CONFIDENCE)}")
    for sb in fm.get("source_basis") or []:
        if sb not in SOURCE_BASIS:
            warnings.append(f"source_basis '{sb}' not a standard value {sorted(SOURCE_BASIS)}")
    for layer in fm.get("togaf_layers") or []:
        if layer not in TOGAF:
            errors.append(f"togaf_layers '{layer}' not in {sorted(TOGAF)} (schema enum)")
    for p in fm.get("well_architected_pillars") or []:
        if p not in PILLARS:
            errors.append(f"well_architected_pillars '{p}' not in {PILLARS}")
    for i, qp in enumerate(fm.get("qlik_products") or []):
        if not isinstance(qp, dict) or not qp.get("product"):
            errors.append(f"qlik_products[{i}] must be a mapping with 'product'")
        elif not qp.get("versions"):
            errors.append(f"qlik_products[{i}] ({qp.get('product')}): 'versions' is required by the schema "
                          "— use 'Not version-specific' rather than omitting it")

    # --- dates ---
    for f in ("created", "last_reviewed"):
        if fm.get(f) and not is_date(fm[f]):
            errors.append(f"{f} '{fm[f]}' is not an ISO date (YYYY-MM-DD)")
    if fm.get("review_by") and not is_date(fm["review_by"]):
        warnings.append(f"review_by '{fm['review_by']}' is not an ISO date — "
                        "acceptable if tied to a release, check it is intentional")
    lr, rb = to_date(fm.get("last_reviewed")), to_date(fm.get("review_by"))
    if lr and rb and rb <= lr:
        errors.append("review_by must be later than last_reviewed")
    cr = to_date(fm.get("created"))
    if cr and lr and lr < cr:
        warnings.append("last_reviewed is earlier than created")

    # --- lifecycle / ownership policy ---
    if fm.get("status") == "Approved" and not [
            r for r in (fm.get("peer_reviewers") or []) if not PLACEHOLDER_RE.search(str(r))]:
        errors.append("status is Approved but no real peer_reviewers named")
    if fm.get("status") == "Superseded" and not fm.get("superseded_by"):
        errors.append("status is Superseded but superseded_by is empty")
    if fm.get("superseded_by") and fm.get("status") not in ("Superseded", "Deprecated"):
        warnings.append("superseded_by is set but status is not Superseded/Deprecated")
    if fm.get("used_ai_to_solve_it") is True and not fm.get("ai_solutions_used"):
        warnings.append("used_ai_to_solve_it is true but ai_solutions_used is empty")
    if PLACEHOLDER_RE.search(str(fm.get("owner", ""))):
        errors.append("owner is still the template placeholder")
    for rel in ("related", "alternatives", "migration_path", "supersedes", "superseded_by"):
        vals = fm.get(rel)
        if isinstance(vals, list) and ku_id in [str(v) for v in vals]:
            errors.append(f"{rel} must not contain this KU's own id ({ku_id})")

    # --- body: collect H2 sections in order ---
    tier = fm.get("tier")
    raw_h2 = re.findall(r"^##\s+(.+?)\s*$", body, re.M)
    found, sections = [], {}
    parts = re.split(r"^##\s+", body, flags=re.M)[1:]
    for part in parts:
        name, _, content = part.partition("\n")
        name = re.sub(r"\s*\[optional\]\s*$", "", name.strip(), flags=re.I)
        if name in ALIASES:
            warnings.append(f"section '## {name}' accepted, but canonical heading is "
                            f"'## {ALIASES[name]}'")
            name = ALIASES[name]
        found.append(name)
        sections[name] = content

    for s in REQUIRED_SECTIONS:
        if s not in sections:
            errors.append(f"required section missing: ## {s}")
    if tier == 3 and "Field Qualification Questions (Tier 3)" not in sections:
        errors.append(
            "tier 3: '## Field Qualification Questions (Tier 3)' is the de facto main "
            "section for a Tier 3 KU and should not be omitted")
    # The other five sections are genuinely optional at every tier — an author may omit
    # them entirely when they don't add anything; no warning is raised for omitting them.
    extras = [s for s in found if s not in CANON]
    for s in extras:
        warnings.append(f"non-canonical H2 section: ## {s}")
    dupes = {s for s in found if found.count(s) > 1}
    for s in dupes:
        errors.append(f"duplicate H2 section: ## {s}")
    # order
    canon_found = [s for s in found if s in CANON]
    if canon_found != [s for s in CANON if s in sections]:
        errors.append("canonical sections out of order: found " + " > ".join(canon_found))

    # --- substance ---
    for s in CANON:
        content = sections.get(s)
        if content is None:
            continue  # omitting an optional section entirely is fine; nothing to check
        core_required_always = s in ("Context", "Field Qualification Questions (Tier 3)") and tier == 3
        light_ok = (s in OPTIONAL_SECTIONS) or (tier == 3 and s not in
                    ("Context", "Field Qualification Questions (Tier 3)"))
        if len(content.split()) < 20 and not (light_ok and na_marked(content)):
            (errors if (s in REQUIRED_SECTIONS or core_required_always) else warnings).append(
                f"section '{s}' is present but looks empty or placeholder-thin — "
                f"omit it instead of leaving a near-empty optional section" if s in OPTIONAL_SECTIONS
                else f"section '{s}' looks empty or placeholder-thin")

    # --- subsection formats ---
    def h3s(name):
        return re.findall(r"^###\s+(.+?)\s*$", sections.get(name, ""), re.M)

    if "TOGAF Impact" in sections:
        required = ["Business", "Data", "Application", "Technology"]
        allowed = required + ["Security"]
        got = h3s("TOGAF Impact")
        got_required = [g for g in got if g != "Security"]
        if got_required != required or any(g not in allowed for g in got):
            errors.append(
                f"TOGAF Impact must contain {required} in order, with an optional trailing "
                f"'Security' subsection; found {got}")
        declared = fm.get("togaf_layers") or []
        missing_layers = [l for l in declared if l not in got]
        if missing_layers and got:
            warnings.append(f"togaf_layers declared in YAML but lacking a subsection: {missing_layers}")
        if "Security" in got and "Security" not in declared:
            warnings.append("body has a '### Security' TOGAF subsection but togaf_layers YAML omits Security")

    if "Well-Architected Impact" in sections:
        got = h3s("Well-Architected Impact")
        declared = [p for p in (fm.get("well_architected_pillars") or [])]
        bad = [g for g in got if g not in PILLARS]
        if bad:
            errors.append(f"Well-Architected Impact has non-pillar subsections: {bad}")
        if declared and got != declared:
            warnings.append("Well-Architected subsections do not match YAML pillars in order: "
                            f"YAML {declared} vs body {got}")

    # Consequences is free-form prose/bullets per the authoring guide — no subsection
    # split is required. If the author does use '### Positive/Negative' subsections that's
    # fine too; nothing to enforce either way.

    if "Anti-Patterns" in sections:
        ap = ANTIPAT_RE.findall(sections["Anti-Patterns"])
        ap_h3 = h3s("Anti-Patterns")
        content_words = len(sections["Anti-Patterns"].split())
        if not ap and content_words < 20:
            errors.append("Anti-Patterns section is required and looks empty — "
                           "it should name at least one specific trap someone actually fell into")
        elif ap:
            if len(ap) != len(ap_h3):
                warnings.append("some Anti-Patterns subsections do not match '### Anti-pattern N — name'")
            if len(ap) > 6:
                warnings.append(f"{len(ap)} anti-patterns — the guide expects one or two; "
                                "check these aren't padding or hiding a second decision")
            blocks = re.split(r"^###\s+", sections["Anti-Patterns"], flags=re.M)[1:]
            without_pref = [b.partition("\n")[0].strip() for b in blocks
                            if "**Preferred approach**" not in b]
            if without_pref:
                warnings.append(f"anti-patterns missing a '**Preferred approach**' block: {without_pref} "
                                "(recommended format, not required)")

    if PLACEHOLDER_RE.search(body):
        warnings.append("template placeholder text still present in body")

    # --- size heuristics ---
    # The authoring guide's actual bar is behavioral, not a word count: "if a peer can
    # read the KU in about three minutes and then apply it, the size is right." At a
    # typical ~200-250 wpm reading pace that's roughly 600-750 words; "ten minutes to get
    # through it" (too big) is roughly 2000-2500 words. These are a rough proxy for that
    # test, not a target to write to — the actual signal is always the supersession seam
    # and the "what would I actually do?" gut check, not the count.
    words = len(body.split())
    if words > 2200:
        warnings.append(f"body is {words} words — probably more than a 3-minute read; "
                        "check the supersession seam (does more than one 'what to do' live here?)")
    elif words < 250 and tier != 3:
        warnings.append(f"body is only {words} words — a peer may finish in under a minute and ask "
                        "'but what would I actually do?'; check it isn't too thin or too general")
    dep = len(re.findall(r"depending on whether", body, re.I))
    if dep >= 3:
        warnings.append(f"'depending on whether' appears {dep}x — each one is a Tier-2 variant or a separate KU")

    # --- bundle path (references/naming-standard.md) ---
    fname = Path(path).name
    parent = Path(path).parent.name
    flat_convention = bool(ku_id) and re.match(re.escape(ku_id) + r"[ \-_]", fname)
    if fname == BUNDLE_FILENAME:
        if ku_id and parent != ku_id and "XXX" not in ku_id:
            errors.append(
                f"file is at '.../{parent}/{BUNDLE_FILENAME}' but id is '{ku_id}' — the bundle "
                f"directory name must equal the id exactly (knowledge-units/{ku_id}/{BUNDLE_FILENAME})")
    elif flat_convention:
        warnings.append(
            f"filename '{fname}' follows the retired flat convention (<id>-<title>.md) — "
            f"move to knowledge-units/{ku_id}/{BUNDLE_FILENAME} per references/naming-standard.md")
    else:
        warnings.append(
            f"filename '{fname}' is not '{BUNDLE_FILENAME}' — the standard bundle path is "
            f"knowledge-units/<id>/{BUNDLE_FILENAME}; confirm this is a draft not yet placed in its bundle")

    return errors, warnings


def corpus_checks(paths):
    """Cross-file integrity: duplicate IDs, bundle-path/ID match, dangling refs, reciprocity."""
    findings = {p: {"errors": [], "warnings": []} for p in paths}
    meta = {}
    for p in paths:
        try:
            fm, _ = parse(p)
        except yaml.YAMLError:
            continue
        if isinstance(fm, dict):
            meta[p] = fm
    ids = {}
    for p, fm in meta.items():
        kid = str(fm.get("id", ""))
        if not kid:
            continue
        ids.setdefault(kid, []).append(p)
        fname = Path(p).name
        parent = Path(p).parent.name
        if fname == BUNDLE_FILENAME:
            if parent != kid and "XXX" not in kid:
                findings[p]["errors"].append(
                    f"bundle directory '{parent}' does not match id '{kid}' "
                    f"(expected knowledge-units/{kid}/{BUNDLE_FILENAME})")
        # else: the per-file check() above already warns about the non-bundle filename.
    for kid, ps in ids.items():
        if len(ps) > 1:
            for p in ps:
                findings[p]["errors"].append(
                    f"id '{kid}' is used by {len(ps)} files: {[Path(x).name for x in ps]} — IDs are never reused")
    known = set(ids)
    for p, fm in meta.items():
        for rel in ("related", "alternatives", "migration_path", "supersedes", "superseded_by"):
            for v in (fm.get(rel) or [] if isinstance(fm.get(rel), list) else
                      ([fm[rel]] if fm.get(rel) else [])):
                if str(v) not in known:
                    findings[p]["warnings"].append(
                        f"{rel} references '{v}' which is not in this corpus (fine if it lives elsewhere)")
        sup = fm.get("supersedes")
        for v in (sup if isinstance(sup, list) else ([sup] if sup else [])):
            for old in ids.get(str(v), []):
                ofm = meta.get(old, {})
                sb = ofm.get("superseded_by")
                sb_list = sb if isinstance(sb, list) else ([sb] if sb else [])
                if str(fm.get("id")) not in [str(x) for x in sb_list]:
                    findings[p]["warnings"].append(
                        f"supersedes {v}, but {Path(old).name} does not set superseded_by: {fm.get('id')}")
    return findings


def main():
    argv = sys.argv[1:]
    as_json = "--json" in argv
    argv = [a for a in argv if a != "--json"]
    if argv and argv[0] == "--corpus":
        if len(argv) < 2:
            sys.stderr.write(__doc__)
            sys.exit(2)
        # rglob, not glob: KUs live in nested bundle dirs (knowledge-units/<ID>/knowledge-unit.md),
        # but a corpus may also still contain unmigrated flat files at any depth.
        paths = sorted(str(p) for p in Path(argv[1]).rglob("*.md"))
    else:
        paths = argv
    if not paths:
        sys.stderr.write(__doc__)
        sys.exit(2)

    results = {p: dict(zip(("errors", "warnings"), check(p))) for p in paths}
    if len(paths) > 1:
        for p, f in corpus_checks(paths).items():
            results[p]["errors"] += f["errors"]
            results[p]["warnings"] += f["warnings"]

    worst = 0
    for p in paths:
        e, w = results[p]["errors"], results[p]["warnings"]
        worst = max(worst, 2 if e else (1 if w else 0))
        if not as_json:
            print(f"\n=== {p} ===")
            print(f"{len(e)} error(s), {len(w)} warning(s)")
            for x in e:
                print(f"  ERROR   {x}")
            for x in w:
                print(f"  warning {x}")
            if not e and not w:
                print("  clean")
    if as_json:
        print(json.dumps(results, indent=2, default=str))
    sys.exit(worst)


if __name__ == "__main__":
    main()
