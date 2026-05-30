#!/usr/bin/env python3
"""Audit your TrustPager contacts — find duplicates, gaps, dormant records.

When to use:
- "Why is the contact list so messy?"
- Before running an email blast — find the bad addresses first.
- After importing a new contact source — find duplicates with existing records.
- Quarterly hygiene pass.

What it reports:
- 📭 Missing email — contacts with no email at all.
- 📵 Missing phone — contacts with no phone at all.
- 🚫 Bad email — contacts whose email doesn't have an @ or domain.
- 👻 Likely duplicates — contacts with identical email, OR identical
  first+last name + same company.
- 💤 Dormant — contacts with no activity in 365+ days AND no open opps.
- 🔗 Orphan — contacts not linked to any opportunity or company.

All read-only. Doesn't change anything in your workspace.

Usage:
    python tools/audit-contacts.py
    python tools/audit-contacts.py --dormant-days 180   # different dormant threshold
    python tools/audit-contacts.py --json
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trustpager_api import (  # noqa: E402
    BOSError, api_get, days_since, emit_error_and_exit, emit_json,
    force_utf8_stdout, now_utc, parse_iso, resolve_path,
)


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def audit(dormant_days: int, json_only: bool) -> dict[str, Any]:
    now = now_utc()
    path = resolve_path("contacts")
    response = api_get(path, limit=200)
    contacts = response.get("data", [])

    missing_email: list[dict[str, Any]] = []
    missing_phone: list[dict[str, Any]] = []
    bad_email: list[dict[str, Any]] = []
    dormant: list[dict[str, Any]] = []
    orphan: list[dict[str, Any]] = []

    by_email: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_name_company: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)

    for c in contacts:
        cid = c.get("id")
        first = (c.get("first_name") or "").strip().lower()
        last = (c.get("last_name") or "").strip().lower()
        company_id = c.get("company_id") or ""
        email = (c.get("email") or "").strip()
        phone = (c.get("phone") or "").strip()
        last_activity = parse_iso(c.get("last_activity_at") or c.get("updated_at"))
        has_open_opps = bool(c.get("open_opportunity_count", 0))
        has_any_opps = bool(c.get("opportunity_count", c.get("open_opportunity_count", 0)))
        has_company = bool(company_id)

        slim = {
            "id": cid,
            "name": f"{c.get('first_name') or ''} {c.get('last_name') or ''}".strip(),
            "email": email,
            "phone": phone,
        }

        if not email:
            missing_email.append(slim)
        elif not EMAIL_RE.match(email):
            bad_email.append(slim)
        else:
            by_email[email.lower()].append(slim)

        if not phone:
            missing_phone.append(slim)

        if first and last:
            by_name_company[(first, last, company_id)].append(slim)

        if last_activity:
            ds = days_since(last_activity, ref=now) or 0
            if ds >= dormant_days and not has_open_opps:
                dormant.append({**slim, "days_dormant": ds})

        if not has_any_opps and not has_company:
            orphan.append(slim)

    duplicate_email_groups = [
        {"email": e, "contacts": grp}
        for e, grp in by_email.items() if len(grp) > 1
    ]
    duplicate_name_groups = [
        {"key": f"{f.title()} {l.title()}" + (f" @ company:{co[-6:]}" if co else ""),
         "contacts": grp}
        for (f, l, co), grp in by_name_company.items() if len(grp) > 1
    ]
    dormant.sort(key=lambda x: x["days_dormant"], reverse=True)

    return {
        "generated_at": now.isoformat(),
        "dormant_threshold_days": dormant_days,
        "headline": {
            "total_contacts": len(contacts),
            "missing_email": len(missing_email),
            "missing_phone": len(missing_phone),
            "bad_email": len(bad_email),
            "duplicate_email_groups": len(duplicate_email_groups),
            "duplicate_name_groups": len(duplicate_name_groups),
            "dormant": len(dormant),
            "orphan": len(orphan),
        },
        "missing_email": missing_email[:20],
        "missing_phone": missing_phone[:20],
        "bad_email": bad_email[:20],
        "duplicate_email_groups": duplicate_email_groups[:10],
        "duplicate_name_groups": duplicate_name_groups[:10],
        "dormant_top_20": dormant[:20],
        "orphan": orphan[:20],
    }


def _print_human(r: dict[str, Any]) -> None:
    h = r["headline"]
    print("## Contact audit")
    print()
    print(f"- Total contacts sampled: **{h['total_contacts']}**")
    print(f"- Missing email: **{h['missing_email']}**")
    print(f"- Missing phone: **{h['missing_phone']}**")
    print(f"- Malformed email: **{h['bad_email']}**")
    print(f"- Likely duplicates (by email): **{h['duplicate_email_groups']}** groups")
    print(f"- Likely duplicates (by name + company): **{h['duplicate_name_groups']}** groups")
    print(f"- Dormant ({r['dormant_threshold_days']}+ days, no open opps): **{h['dormant']}**")
    print(f"- Orphan (no opps, no company): **{h['orphan']}**")
    print()
    if r["duplicate_email_groups"]:
        print("### 👻 Duplicate email groups (top 5)")
        for g in r["duplicate_email_groups"][:5]:
            names = ", ".join(c["name"] or "(no name)" for c in g["contacts"])
            print(f"- `{g['email']}` → {len(g['contacts'])} contacts: {names}")
        print()
    if r["missing_email"]:
        print(f"### 📭 Missing email (showing first 10 of {h['missing_email']})")
        for c in r["missing_email"][:10]:
            print(f"- {c['name'] or '(no name)'} — phone: {c['phone'] or '(none)'}")
        print()
    if r["dormant_top_20"]:
        print(f"### 💤 Dormant contacts (top 10)")
        for c in r["dormant_top_20"][:10]:
            print(f"- {c['name'] or '(no name)'} — last activity **{c['days_dormant']}** days ago")
        print()


def main() -> int:
    force_utf8_stdout()
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--dormant-days", type=int, default=365,
                        help="Days of inactivity to qualify as dormant (default 365)")
    parser.add_argument("--json", action="store_true",
                        help="Output JSON instead of human-readable markdown")
    args = parser.parse_args()

    try:
        report = audit(args.dormant_days, json_only=args.json)
        if args.json:
            emit_json(report)
        else:
            _print_human(report)
        return 0
    except BOSError as e:
        emit_error_and_exit(str(e), code=1)


if __name__ == "__main__":
    sys.exit(main())
