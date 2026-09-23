#!/usr/bin/env python3
from pathlib import Path
from datetime import date, timedelta
import argparse, re

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "templates" / "adr-ku-alignment-report.md"

p = argparse.ArgumentParser(description="Create an ADR–KU Alignment Report skeleton")
p.add_argument("--account", required=True)
p.add_argument("--owner", required=True)
p.add_argument("--program", default="")
p.add_argument("--account-id", default="")
p.add_argument("--sequence", type=int, default=1)
p.add_argument("--output", default="adr-ku-alignment-report.md")
args = p.parse_args()

today = date.today()
slug = re.sub(r"[^A-Za-z0-9]+", "-", args.account).strip("-").upper()
report_id = f"{slug}-ADRKU-{today.year}-{args.sequence:03d}"
review_by = today + timedelta(days=30)

text = TEMPLATE.read_text(encoding="utf-8")
repls = {
    "<ACCOUNT>-ADRKU-YYYY-NNN": report_id,
    "<Account>": args.account,
    "<Account name>": args.account,
    "<optional internal account identifier>": args.account_id,
    "<CSE / EA>": args.owner,
    "<optional program / domain scope>": args.program,
}
for a,b in repls.items(): text = text.replace(a,b)
# Replace first date placeholders in YAML only.
text = text.replace('created_on: "YYYY-MM-DD"', f'created_on: "{today.isoformat()}"', 1)
text = text.replace('last_updated: "YYYY-MM-DD"', f'last_updated: "{today.isoformat()}"', 1)
text = text.replace('assessment_as_of: "YYYY-MM-DD"', f'assessment_as_of: "{today.isoformat()}"', 1)
text = text.replace('review_by: "YYYY-MM-DD"', f'review_by: "{review_by.isoformat()}"', 1)
text = text.replace('kus_checked_as_of: "YYYY-MM-DD"', f'kus_checked_as_of: "{today.isoformat()}"', 1)
text = text.replace('account_context_as_of: "YYYY-MM-DD"', f'account_context_as_of: "{today.isoformat()}"', 1)

out = Path(args.output)
out.write_text(text, encoding="utf-8")
print(out.resolve())
