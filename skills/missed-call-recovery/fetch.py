#!/usr/bin/env python3
"""Missed-call recovery — find recent missed inbound calls + caller context.

Pulls every inbound call in the last N hours that was missed (no answer,
voicemail, or hung-up-before-pickup), enriches each with caller identity
(contact lookup by phone), open opportunity, and whether the call has
already been returned.

Output (stdout): JSON with one record per missed call, ranked by priority
(known caller with open opportunity > known caller > unknown number).
The companion SKILL.md tells Claude how to draft and send recovery
messages.

Auth: TRUSTPAGER_API_KEY env var or ~/.claude/bos.json. See tools/trustpager_api.py.

Usage:
    python skills/missed-call-recovery/fetch.py
    python skills/missed-call-recovery/fetch.py --hours 48
    python skills/missed-call-recovery/fetch.py --include-callbacks  # show even already-recovered ones
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from datetime import timedelta
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))
from trustpager_api import (  # noqa: E402
    BOSError, api_get, days_since, emit_error_and_exit, emit_json,
    force_utf8_stdout, log, now_utc, parallel_get, parse_iso, resolve_path,
)


SKILL = "missed-call-recovery"
MISSED_STATUSES = {"no-answer", "no_answer", "missed", "failed", "busy",
                   "voicemail", "abandoned", "no-answer-machine"}
INBOUND_DIRECTIONS = {"inbound", "incoming"}


def _is_missed(call: dict[str, Any]) -> bool:
    status = (call.get("status") or call.get("disposition") or "").lower().replace("_", "-")
    direction = (call.get("direction") or "").lower()
    if direction not in INBOUND_DIRECTIONS:
        return False
    if status in MISSED_STATUSES:
        return True
    # Heuristic fallback: very short call (<5s) + inbound + no transcript = missed
    dur = call.get("duration") or call.get("duration_seconds") or 0
    has_transcript = bool(call.get("transcript_id") or call.get("recording_url"))
    if dur < 5 and not has_transcript:
        return True
    return False


def _normalize_phone(raw: str | None) -> str | None:
    if not raw:
        return None
    return "".join(c for c in raw if c.isdigit() or c == "+")[-12:] or None


def fetch_and_digest(hours: int, include_callbacks: bool, quiet: bool) -> dict[str, Any]:
    now = now_utc()
    cutoff = now - timedelta(hours=hours)

    log(SKILL, f"fetching phone call logs from last {hours}h...", quiet=quiet)

    calls_path = resolve_path("phone", path_contains="call-logs")
    response = api_get(calls_path, limit=200, after=cutoff.isoformat())
    calls = response.get("data", [])
    log(SKILL, f"  {len(calls)} call log rows in window", quiet=quiet)

    # Filter to missed inbound
    missed = [c for c in calls if _is_missed(c)]
    log(SKILL, f"  {len(missed)} missed inbound calls", quiet=quiet)

    # Group by from_phone — if there are multiple missed calls from same number,
    # treat as one "session" (the latest one)
    by_phone: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for c in missed:
        phone = _normalize_phone(c.get("from_phone") or c.get("from") or c.get("caller_number"))
        if not phone:
            continue
        by_phone[phone].append(c)

    # Identify recovered numbers: any outbound or answered inbound call to/from
    # the same phone AFTER the latest missed call
    recovered: dict[str, dict[str, Any]] = {}
    for phone in by_phone:
        latest_miss = max(by_phone[phone], key=lambda c: c.get("started_at") or c.get("created_at") or "")
        miss_time = parse_iso(latest_miss.get("started_at") or latest_miss.get("created_at"))
        for c in calls:
            if c is latest_miss:
                continue
            # The "other party" depends on direction: outbound → to_phone, inbound → from_phone
            direction = (c.get("direction") or "").lower()
            if direction == "outbound":
                other_phone = _normalize_phone(c.get("to_phone") or c.get("to"))
            elif direction in INBOUND_DIRECTIONS:
                other_phone = _normalize_phone(
                    c.get("from_phone") or c.get("from") or c.get("caller_number"))
            else:
                continue
            if other_phone != phone:
                continue
            ct = parse_iso(c.get("started_at") or c.get("created_at"))
            if miss_time and ct and ct > miss_time:
                dur = c.get("duration") or c.get("duration_seconds") or 0
                if direction == "outbound" or (direction in INBOUND_DIRECTIONS and dur >= 5):
                    recovered[phone] = {
                        "recovered_at": c.get("started_at") or c.get("created_at"),
                        "by_call_id": c.get("id"),
                    }
                    break

    # Enrich each unique missed-caller with contact + open opp
    unique_phones = list(by_phone.keys())
    log(SKILL, f"  enriching {len(unique_phones)} unique numbers...", quiet=quiet)

    contacts_path = resolve_path("contacts", action="list")
    contact_calls = [(contacts_path, {"phone": ph, "limit": 1}) for ph in unique_phones]
    contact_results = parallel_get(contact_calls) if contact_calls else {}

    items: list[dict[str, Any]] = []
    for phone, missed_calls in by_phone.items():
        latest = max(missed_calls, key=lambda c: c.get("started_at") or c.get("created_at") or "")
        miss_time = parse_iso(latest.get("started_at") or latest.get("created_at"))
        minutes_ago = int((now - miss_time).total_seconds() / 60) if miss_time else None

        # Find the contact result keyed by path
        contact: dict[str, Any] | None = None
        for path, resp in contact_results.items():
            if "phone" not in path and not resp.get("data"):
                continue
            data = resp.get("data") or []
            if data and _normalize_phone(data[0].get("phone")) == phone:
                contact = data[0]
                break

        is_recovered = phone in recovered
        if is_recovered and not include_callbacks:
            continue

        item = {
            "phone": phone,
            "missed_count": len(missed_calls),
            "latest_call_id": latest.get("id"),
            "minutes_since_missed": minutes_ago,
            "missed_at": latest.get("started_at") or latest.get("created_at"),
            "recovered": is_recovered,
            "recovered_info": recovered.get(phone),
            "contact": None,
            "open_opportunity": None,
        }
        if contact:
            item["contact"] = {
                "id": contact.get("id"),
                "first_name": contact.get("first_name"),
                "last_name": contact.get("last_name"),
                "email": contact.get("email"),
                "phone": contact.get("phone"),
                "preferred_channel": contact.get("preferred_channel"),
                "sms_unsubscribed": contact.get("sms_unsubscribed"),
            }
            # Get most recent open opportunity for this contact
            try:
                opps_resp = api_get("contacts/" + contact["id"] + "/deals", limit=5)
                opps = opps_resp.get("data") or []
                open_opps = [o for o in opps
                             if (o.get("status") or "").lower() not in
                             {"won", "lost", "cancelled", "abandoned"}]
                if open_opps:
                    item["open_opportunity"] = {
                        "id": open_opps[0].get("id"),
                        "name": open_opps[0].get("name"),
                        "value": open_opps[0].get("value"),
                        "stage": ((open_opps[0].get("placements") or [{}])[0]
                                  .get("crm_pipeline_stages", {})
                                  or {}).get("name"),
                    }
            except BOSError:
                pass
        items.append(item)

    # Sort: known caller with open opp first, then known caller, then unknown
    def _priority(it: dict[str, Any]) -> int:
        if it["open_opportunity"]:
            return 0
        if it["contact"]:
            return 1
        return 2
    items.sort(key=lambda it: (_priority(it), it.get("minutes_since_missed") or 0))

    return {
        "generated_at": now.isoformat(),
        "window_hours": hours,
        "include_callbacks": include_callbacks,
        "headline": {
            "total_missed_unique_callers": len(by_phone),
            "already_recovered": sum(1 for p in by_phone if p in recovered),
            "needing_recovery": len([i for i in items if not i["recovered"]]),
            "known_callers": sum(1 for i in items if i["contact"]),
        },
        "items": items,
    }


def main() -> int:
    force_utf8_stdout()
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--hours", type=int, default=24,
                        help="How far back to look (default 24 hours)")
    parser.add_argument("--include-callbacks", action="store_true",
                        help="Also include calls that have already been recovered")
    parser.add_argument("--json-only", action="store_true",
                        help="Suppress stderr progress logs")
    args = parser.parse_args()

    try:
        digest = fetch_and_digest(args.hours, args.include_callbacks, quiet=args.json_only)
        emit_json(digest)
        return 0
    except BOSError as e:
        emit_error_and_exit(str(e), code=1)


if __name__ == "__main__":
    sys.exit(main())
