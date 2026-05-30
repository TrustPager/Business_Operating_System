#!/usr/bin/env python3
"""log-this-call — resolve a person/opp identifier into the full call context.

The user just got off a call. They say "log my call with Sarah from Acme."
This fetch resolves "Sarah" → the contact, finds their open opportunities,
recent activity, and any tasks. So Claude can pick the right opp without
3-5 separate MCP roundtrips.

Lookup:
- If --query looks like a phone (digits + optional +) → match by phone
- If --query has @ → match by email
- Otherwise → name search (search_contacts equivalent)

Pulls (in parallel after best-match resolution):
- The matched contact's full record
- Their open opportunities + stage
- Most recent activities on the top opp
- Any open tasks tied to the top opp

Auth: TRUSTPAGER_API_KEY env var or ~/.claude/bos.json.

Usage:
    python skills/log-this-call/fetch.py --query "Sarah Lim"
    python skills/log-this-call/fetch.py --query "+61400000001"
    python skills/log-this-call/fetch.py --query "sarah@acme.com"
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


SKILL = "log-this-call"


def _is_phone(q: str) -> bool:
    cleaned = q.replace(" ", "").replace("-", "")
    return cleaned.startswith("+") or (cleaned.isdigit() and len(cleaned) >= 6)


def fetch(query: str, quiet: bool) -> dict[str, Any]:
    now = now_utc()
    contacts_path = resolve_path("contacts")
    log(SKILL, f"resolving '{query}'...", quiet=quiet)

    if _is_phone(query):
        params = {"phone": query, "limit": 5}
    elif "@" in query:
        params = {"email": query, "limit": 5}
    else:
        params = {"search": query, "limit": 5}

    contacts_response = api_get(contacts_path, **params)
    candidates = contacts_response.get("data", [])

    if not candidates:
        return {
            "generated_at": now.isoformat(),
            "query": query,
            "headline": {"matched_contacts": 0},
            "candidates": [],
            "best_match": None,
            "open_opportunities": [],
            "recent_activities": [],
            "open_tasks": [],
        }

    best = candidates[0]
    contact_id = best.get("id")

    log(SKILL, f"  best match: {best.get('first_name')} {best.get('last_name')} ({contact_id})",
        quiet=quiet)

    opps_path = f"contacts/{contact_id}/deals"
    activities_path = f"contacts/{contact_id}/activities"
    calls = [
        (opps_path, {"limit": 10}),
        (activities_path, {"limit": 10}),
    ]
    results = parallel_get(calls)

    opps = results.get(opps_path, {}).get("data", [])
    open_opps = [
        o for o in opps
        if (o.get("status") or "").lower() not in
        {"won", "lost", "cancelled", "abandoned"}
    ]

    # Open tasks for the top opportunity
    open_tasks: list[dict[str, Any]] = []
    if open_opps:
        top_opp_id = open_opps[0].get("id")
        try:
            tasks_resp = api_get(f"opportunities/{top_opp_id}/tasks", limit=10)
            for t in tasks_resp.get("data", []):
                if not t.get("completed_at"):
                    open_tasks.append({
                        "id": t.get("id"),
                        "title": t.get("title"),
                        "due_date": t.get("due_date") or t.get("due_at"),
                    })
        except BOSError:
            pass

    return {
        "generated_at": now.isoformat(),
        "query": query,
        "headline": {
            "matched_contacts": len(candidates),
            "open_opportunities": len(open_opps),
            "open_tasks": len(open_tasks),
        },
        "candidates": [
            {
                "id": c.get("id"),
                "name": f"{c.get('first_name', '')} {c.get('last_name', '')}".strip(),
                "email": c.get("email"),
                "phone": c.get("phone"),
                "company_id": c.get("company_id"),
            }
            for c in candidates
        ],
        "best_match": {
            "id": best.get("id"),
            "first_name": best.get("first_name"),
            "last_name": best.get("last_name"),
            "email": best.get("email"),
            "phone": best.get("phone"),
            "preferred_channel": best.get("preferred_channel"),
            "sms_unsubscribed": best.get("sms_unsubscribed"),
            "email_unsubscribed": best.get("email_unsubscribed"),
        },
        "open_opportunities": [
            {
                "id": o.get("id"),
                "name": o.get("name"),
                "value": o.get("value"),
                "currency": o.get("currency"),
                "stage": ((o.get("placements") or [{}])[0]
                          .get("crm_pipeline_stages", {}) or {}).get("name"),
            }
            for o in open_opps
        ],
        "recent_activities": [
            {
                "id": a.get("id"),
                "type": a.get("activity_type") or a.get("type"),
                "summary": a.get("summary") or a.get("title"),
                "created_at": a.get("created_at"),
            }
            for a in results.get(activities_path, {}).get("data", [])
        ][:5],
        "open_tasks": open_tasks,
    }


def main() -> int:
    force_utf8_stdout()
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--query", required=True,
                        help="Name, phone, email, or opportunity name to resolve")
    parser.add_argument("--json-only", action="store_true",
                        help="Suppress stderr progress logs")
    args = parser.parse_args()

    try:
        emit_json(fetch(args.query, quiet=args.json_only))
        return 0
    except BOSError as e:
        emit_error_and_exit(str(e), code=1)


if __name__ == "__main__":
    sys.exit(main())
