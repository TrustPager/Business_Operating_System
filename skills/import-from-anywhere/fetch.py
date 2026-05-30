#!/usr/bin/env python3
"""import-from-anywhere — compute the dedup baseline before any import.

When the user pastes a list to import, we want to detect duplicates
against existing records BEFORE writing anything. This script pre-builds
the lookup index:

- All existing contacts indexed by lowercased email + normalised phone +
  (first+last+company) key.
- All existing companies indexed by lowercased name + website domain.
- All open opportunities indexed by name (lowercased).

Output is a JSON document the skill loads in memory and consults for
each row of the paste. One bulk fetch instead of N "is this duplicate?"
lookups per row.

Auth: TRUSTPAGER_API_KEY env var or ~/.claude/bos.json.

Usage:
    python skills/import-from-anywhere/fetch.py
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))
from trustpager_api import (  # noqa: E402
    BOSError, api_get, emit_error_and_exit, emit_json, force_utf8_stdout,
    log, now_utc, parallel_get, resolve_path,
)


SKILL = "import-from-anywhere"


def _normalize_phone(raw: str | None) -> str | None:
    if not raw:
        return None
    s = "".join(c for c in raw if c.isdigit() or c == "+")
    return s[-12:] if s else None


def _domain_of(url: str | None) -> str | None:
    if not url:
        return None
    s = url.lower().strip()
    for prefix in ("https://", "http://", "www."):
        if s.startswith(prefix):
            s = s[len(prefix):]
    return s.split("/")[0].split("?")[0] or None


def fetch(quiet: bool) -> dict[str, Any]:
    now = now_utc()
    log(SKILL, "building dedup baseline...", quiet=quiet)

    calls = [
        (resolve_path("contacts"),      {"limit": 200}),
        (resolve_path("companies"),     {"limit": 200}),
        (resolve_path("opportunities"), {"limit": 200, "status": "open"}),
    ]
    results = parallel_get(calls)
    contacts = results.get(resolve_path("contacts"), {}).get("data", [])
    companies = results.get(resolve_path("companies"), {}).get("data", [])
    opportunities = results.get(resolve_path("opportunities"), {}).get("data", [])

    by_email: dict[str, str] = {}
    by_phone: dict[str, str] = {}
    by_name_company: dict[str, str] = {}
    for c in contacts:
        cid = c.get("id")
        if not cid:
            continue
        email = (c.get("email") or "").strip().lower()
        if email:
            by_email[email] = cid
        phone = _normalize_phone(c.get("phone"))
        if phone:
            by_phone[phone] = cid
        first = (c.get("first_name") or "").strip().lower()
        last = (c.get("last_name") or "").strip().lower()
        co = (c.get("company_id") or "")[-6:]
        if first and last:
            by_name_company[f"{first}|{last}|{co}"] = cid

    co_by_name: dict[str, str] = {}
    co_by_domain: dict[str, str] = {}
    for co in companies:
        cid = co.get("id")
        if not cid:
            continue
        name = (co.get("name") or "").strip().lower()
        if name:
            co_by_name[name] = cid
        dom = _domain_of(co.get("website"))
        if dom:
            co_by_domain[dom] = cid

    opp_by_name: dict[str, str] = {}
    for o in opportunities:
        oid = o.get("id")
        n = (o.get("name") or "").strip().lower()
        if oid and n:
            opp_by_name[n] = oid

    return {
        "generated_at": now.isoformat(),
        "headline": {
            "contacts_sampled":      len(contacts),
            "companies_sampled":     len(companies),
            "opportunities_sampled": len(opportunities),
        },
        "contacts": {
            "by_email": by_email,
            "by_phone": by_phone,
            "by_name_company": by_name_company,
        },
        "companies": {
            "by_name":   co_by_name,
            "by_domain": co_by_domain,
        },
        "open_opportunities": {
            "by_name": opp_by_name,
        },
    }


def main() -> int:
    force_utf8_stdout()
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--json-only", action="store_true",
                        help="Suppress stderr progress logs")
    args = parser.parse_args()

    try:
        emit_json(fetch(quiet=args.json_only))
        return 0
    except BOSError as e:
        emit_error_and_exit(str(e), code=1)


if __name__ == "__main__":
    sys.exit(main())
