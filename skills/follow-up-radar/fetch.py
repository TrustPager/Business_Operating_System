#!/usr/bin/env python3
"""Follow-up Radar — silent-opportunity surfacer + contact enrichment.

Finds active opportunities that have gone quiet (no activity in 7+ days, no
scheduled next-action), ranks them by deal value × days silent, and enriches
the top N with contact details so the briefing AI can draft personalised
re-engagement messages.

Usage:
    python skills/follow-up-radar/fetch.py
    python skills/follow-up-radar/fetch.py --silence-days 14   # custom threshold
    python skills/follow-up-radar/fetch.py --top 10            # enrich top 10
    python skills/follow-up-radar/fetch.py --json-only

Output (stdout): JSON document with the enriched silent opportunities.
Output (stderr): progress logs.

Auth: TRUSTPAGER_API_KEY env var or ~/.claude/bos.json. See tools/trustpager_api.py.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))
from trustpager_api import (  # noqa: E402
    BOSError, api_get, emit_error_and_exit, emit_json, group_count, log,
    now_utc, parallel_get, parse_iso, resolve_path,
)


SKILL = "follow-up-radar"

INACTIVE_OPP_STATUSES = {"won", "lost", "cancelled", "abandoned", "archived"}


def _opp_stage(opp: dict[str, Any]) -> str | None:
    placements = opp.get("placements") or []
    if not placements:
        return None
    return (placements[0].get("crm_pipeline_stages") or {}).get("name")


def _opp_is_active(opp: dict[str, Any]) -> bool:
    if (opp.get("status") or "").lower() in INACTIVE_OPP_STATUSES:
        return False
    placements = opp.get("placements") or []
    if placements:
        stage = placements[0].get("crm_pipeline_stages") or {}
        if stage.get("is_won_stage") or stage.get("is_lost_stage"):
            return False
    return True


def _log(msg: str, *, quiet: bool) -> None:
    log(SKILL, msg, quiet=quiet)


def _score(opp: dict[str, Any], days_silent: int) -> float:
    """Rank function: $1k of value ~ 1 day of silence.

    Without this, fully-priced deals dominate the list and unpriced-but-
    long-silent leads vanish (a real problem we saw in FinalPiece data,
    where most opps have value=null).
    """
    value = float(opp.get("value") or 0)
    # Floor at 100 so a stale unpriced deal still has some pull.
    base = max(100.0, value / 1000.0)
    return base * (1 + days_silent / 30.0)


def find_silent(opportunities: list[dict[str, Any]],
                now: datetime,
                silence_days: int) -> list[dict[str, Any]]:
    """Return silent opportunities sorted by score (highest first)."""
    cutoff_seconds = silence_days * 86400
    silent: list[dict[str, Any]] = []
    for opp in opportunities:
        if not _opp_is_active(opp):
            continue
        # Scheduled next action in the future means it's NOT going quiet
        nad = parse_iso(opp.get("next_action_date"))
        if nad and nad >= now:
            continue
        last_touch = parse_iso(opp.get("updated_at"))
        if not last_touch:
            continue
        seconds_since = (now - last_touch).total_seconds()
        if seconds_since < cutoff_seconds:
            continue
        days_silent = int(seconds_since // 86400)
        silent.append({
            "id": opp.get("id"),
            "name": opp.get("name"),
            "value": opp.get("value"),
            "currency": opp.get("currency"),
            "stage": _opp_stage(opp),
            "lead_source": opp.get("lead_source"),
            "last_touch": opp.get("updated_at"),
            "days_silent": days_silent,
            "contact_id": opp.get("contact_id"),
            "customer_id": opp.get("customer_id"),
            "next_action_name": opp.get("next_action_name"),
            "_score": _score(opp, days_silent),
        })
    silent.sort(key=lambda x: x["_score"], reverse=True)
    return silent


def enrich_with_contacts(silent: list[dict[str, Any]],
                         quiet: bool) -> list[dict[str, Any]]:
    """Fetch contact + opportunity-activities for each top-N silent opp in parallel."""
    contact_ids = [s["contact_id"] for s in silent if s.get("contact_id")]
    if not contact_ids:
        return silent

    _log(f"enriching {len(contact_ids)} contacts in parallel...", quiet=quiet)
    contacts_path = resolve_path("contacts", "GET", "get")  # /contacts/:id pattern
    # contacts_path is "contacts/:contact_id" — we need to substitute
    calls = []
    for cid in contact_ids:
        path = contacts_path.replace(":contact_id", cid).replace(":id", cid)
        calls.append((path, {}))

    results = parallel_get(calls)
    contact_lookup: dict[str, dict[str, Any]] = {}
    for path, response in results.items():
        if response.get("error"):
            continue
        c = response.get("data") if isinstance(response.get("data"), dict) else response
        if not isinstance(c, dict):
            continue
        contact_lookup[c.get("id", "")] = c

    enriched: list[dict[str, Any]] = []
    for s in silent:
        cid = s.get("contact_id")
        contact = contact_lookup.get(cid, {}) if cid else {}
        enriched.append({
            **s,
            "contact": {
                "id": contact.get("id"),
                "first_name": contact.get("first_name"),
                "last_name": contact.get("last_name"),
                "email": contact.get("email"),
                "phone": contact.get("phone"),
                "job_title": contact.get("job_title"),
                "source": contact.get("source"),
                "email_unsubscribed": contact.get("email_unsubscribed"),
                "sms_unsubscribed": contact.get("sms_unsubscribed"),
            } if contact else None,
        })
    return enriched


def fetch_and_digest(silence_days: int, top_n: int, quiet: bool) -> dict[str, Any]:
    now = now_utc()
    _log("fetching opportunities...", quiet=quiet)

    opps_path = resolve_path("opportunities")
    response = api_get(opps_path, limit=100)
    opportunities = response.get("data", [])
    _log(f"  ok {opps_path}: {len(opportunities)} rows", quiet=quiet)

    silent = find_silent(opportunities, now, silence_days)
    _log(f"found {len(silent)} silent opportunities (>{silence_days}d quiet, no scheduled next action)",
         quiet=quiet)

    top = silent[:top_n]
    if top:
        top = enrich_with_contacts(top, quiet=quiet)

    return {
        "generated_at": now.isoformat(),
        "silence_threshold_days": silence_days,
        "total_silent": len(silent),
        "returned_top_n": len(top),
        "summary_by_source": group_count(silent, "lead_source"),
        "summary_by_stage": group_count(silent, "stage"),
        "items": top,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Follow-up Radar data fetcher")
    parser.add_argument("--silence-days", type=int, default=7,
                        help="Days of inactivity to qualify as 'going quiet' (default 7)")
    parser.add_argument("--top", type=int, default=10,
                        help="How many top-ranked silent opportunities to enrich and return (default 10)")
    parser.add_argument("--json-only", action="store_true",
                        help="Suppress stderr progress logs")
    args = parser.parse_args()

    try:
        digest = fetch_and_digest(args.silence_days, args.top, quiet=args.json_only)
        emit_json(digest)
        return 0
    except BOSError as e:
        emit_error_and_exit(str(e), code=1)
    except KeyboardInterrupt:
        emit_error_and_exit("Cancelled", code=130)


if __name__ == "__main__":
    sys.exit(main())


# =============================================================================
# Output shape
# =============================================================================
#
# {
#   "generated_at": "2026-05-31T10:00:00+00:00",
#   "silence_threshold_days": 7,
#   "total_silent": 35,
#   "returned_top_n": 10,
#   "summary_by_source": { "Facebook": 18, "Referral": 6, ... },
#   "summary_by_stage": { "Not Ready Yet": 12, "Quote Sent": 5, ... },
#   "items": [
#     {
#       "id": "<opp_uuid>",
#       "name": "...",
#       "value": 12000,
#       "currency": "AUD",
#       "stage": "Quote Sent",
#       "lead_source": "Referral",
#       "last_touch": "2026-05-17T...",
#       "days_silent": 14,
#       "contact_id": "...",
#       "customer_id": "...",
#       "next_action_name": null,
#       "_score": 12.4,
#       "contact": {
#         "id": "...", "first_name": "...", "last_name": "...",
#         "email": "...", "phone": "...", "job_title": "...",
#         "email_unsubscribed": false, "sms_unsubscribed": false
#       }
#     },
#     ...
#   ]
# }
