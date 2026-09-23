#!/usr/bin/env python3
from pathlib import Path
import argparse, re, sys
try:
    import yaml
except Exception:
    print("ERROR: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

ALLOWED_STATUS = {"draft","proposed","approved","superseded"}
REQUIRED_SECTIONS = [
    "Purpose and boundary",
    "1. Account Context",
    "2. Decision Portfolio Inventory",
    "3. KU Currency and Alignment Summary",
    "4. Material Findings",
    "5. Architecture Whitespace / Discovery Flags",
    "6. Risk and Governance Rollup",
    "7. Customer-Success Opportunity Signals",
    "8. Trajectory",
    "9. Prioritized CSE / EA Engagement Agenda",
    "10. Executive Rollup",
    "11. Customer-Shareable Derivative Guidance",
]
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

def err(msg, errors): errors.append(msg)
def warn(msg, warnings): warnings.append(msg)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('report')
    args=ap.parse_args()
    p=Path(args.report)
    text=p.read_text(encoding='utf-8')
    errors=[]; warnings=[]
    if not text.startswith('---\n'):
        err('Missing YAML front matter', errors); data={}
    else:
        parts=text.split('---',2)
        try: data=yaml.safe_load(parts[1]) or {}
        except Exception as e:
            err(f'Invalid YAML: {e}', errors); data={}

    req_top=['schema_version','report_id','report_type','title','status','version','classification','account','ownership','dates','scope','evidence_snapshot','lineage']
    for k in req_top:
        if k not in data: err(f'Missing YAML field: {k}', errors)
    if data.get('report_type')!='adr-ku-alignment': err('report_type must be adr-ku-alignment', errors)
    if data.get('status') not in ALLOWED_STATUS: err(f"status must be one of {sorted(ALLOWED_STATUS)}", errors)
    if data.get('classification')!='internal': warn('Canonical report classification should normally be internal', warnings)

    scope=data.get('scope') or {}
    if set(scope.get('included_adr_statuses') or []) != {'accepted','proposed'}:
        err('scope.included_adr_statuses must contain exactly accepted and proposed', errors)
    excluded=set(scope.get('excluded_adr_statuses') or [])
    for s in ['draft','superseded','deprecated']:
        if s not in excluded: err(f'scope.excluded_adr_statuses must include {s}', errors)

    ev=data.get('evidence_snapshot') or {}
    # Canonical presentation uses accepted_adrs / proposed_adrs. Newer assessed aliases
    # are also accepted for backward/forward compatibility, but are not required visibly.
    accepted = ev.get('accepted_adrs', ev.get('accepted_adrs_assessed'))
    proposed = ev.get('proposed_adrs', ev.get('proposed_adrs_assessed'))
    if not isinstance(accepted, int) or accepted < 0:
        err('evidence_snapshot.accepted_adrs (or accepted_adrs_assessed) must be a non-negative integer', errors)
    if not isinstance(proposed, int) or proposed < 0:
        err('evidence_snapshot.proposed_adrs (or proposed_adrs_assessed) must be a non-negative integer', errors)
    if 'contextual_adrs_considered' in ev and (not isinstance(ev.get('contextual_adrs_considered'), int) or ev.get('contextual_adrs_considered') < 0):
        err('evidence_snapshot.contextual_adrs_considered must be a non-negative integer when present', errors)

    dates=data.get('dates') or {}
    for k in ['created_on','last_updated','assessment_as_of','review_by']:
        v=str(dates.get(k,''))
        if not DATE_RE.match(v): err(f'dates.{k} must be YYYY-MM-DD', errors)
    for k in ['kus_checked_as_of','account_context_as_of']:
        v=str(ev.get(k,''))
        if not DATE_RE.match(v): err(f'evidence_snapshot.{k} must be YYYY-MM-DD', errors)

    for sec in REQUIRED_SECTIONS:
        if not re.search(r'^##\s+'+re.escape(sec)+r'(?:\s|$)', text, flags=re.M):
            err(f'Missing required section: {sec}', errors)

    # Presentation checks based on canonical ACME/Northstar pattern.
    if not re.search(r'\|\s*ADR\s*\|\s*ADR status\s*\|\s*Cited KU\s*\|\s*Current KU state\s*\|\s*Declared Alignment\s*\|\s*Observed Alignment\s*\|', text, flags=re.I):
        warn('Section 3 does not use the canonical compact KU alignment table columns.', warnings)
    if not re.search(r'\|\s*Priority\s*\|\s*Conversation\s*\|\s*Why now\s*\|\s*Intended (?:customer )?outcome\s*\|\s*Type\s*\|', text, flags=re.I):
        warn('Section 9 does not use the canonical compact engagement-agenda columns.', warnings)

    # Semantic guardrail heuristics.
    contextual_lines=[ln for ln in text.splitlines() if 'contextual' in ln.lower() and 'no ku coverage' in ln.lower()]
    for ln in contextual_lines:
        if not any(x in ln.lower() for x in ['not','neither','must never']):
            warn('Possible semantic issue: Contextual ADR mentioned with No KU Coverage: '+ln.strip(), warnings)

    print(f'Validation: {p}')
    for w in warnings: print('WARNING:', w)
    for e in errors: print('ERROR:', e)
    if errors:
        print(f'FAILED: {len(errors)} error(s), {len(warnings)} warning(s)')
        return 1
    print(f'PASSED: 0 errors, {len(warnings)} warning(s)')
    return 0

if __name__=='__main__': raise SystemExit(main())
