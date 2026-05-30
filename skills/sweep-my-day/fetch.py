#!/usr/bin/env python3
"""Sweep My Day — consolidated data fetcher.

Runs 7 parallel API calls against the operator's TrustPager workspace, then
returns a single JSON document with everything `/sweep-my-day` needs to
produce its morning briefing.

Usage:
    python skills/sweep-my-day/fetch.py
    python skills/sweep-my-day/fetch.py --json-only   # suppress progress logs

Output to stdout: JSON shape documented at the bottom of this file.
Output to stderr: progress logs (so Claude can show them or suppress them).

Auth: reads TRUSTPAGER_API_KEY env var or ~/.claude/bos.json (see bos_lib.py).

This script is intentionally token-cheap: it digests the raw API responses
down to just the rows Claude needs, with consistent field names. The whole
output is typically under 5KB versus the ~16KB of raw MCP responses Claude
would otherwise have to consume.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

# Resolve the shared lib (lives in scripts/ at the repo root) regardless of
# where this script is invoked from.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
from bos_lib import (  # noqa: E402
    BOSError, api_get, days_since, emit_error_and_exit, emit_json, log,
    now_utc, parallel_get, parse_iso, resolve_path,
)


SKILL = "sweep-my-day"

# Statuses that mean the opportunity is no longer in active sales motion.
INACTIVE_OPP_STATUSES = {"won", "lost", "cancelled", "abandoned", "archived"}


def _opp_stage(opp: dict[str, Any]) -> str | None:
    """Extract the stage name from opportunity.placements[0].crm_pipeline_stages.name."""
    placements = opp.get("placements") or []
    if not placements:
        return None
    stage = placements[0].get("crm_pipeline_stages") or {}
    return stage.get("name")


def _opp_is_active(opp: dict[str, Any]) -> bool:
    """Active = status is 'open' AND its current stage isn't a won/lost stage."""
    status = (opp.get("status") or "").lower()
    if status in INACTIVE_OPP_STATUSES:
        return False
    placements = opp.get("placements") or []
    if placements:
        stage = placements[0].get("crm_pipeline_stages") or {}
        if stage.get("is_won_stage") or stage.get("is_lost_stage"):
            return False
    return True


def _log(msg: str, *, quiet: bool) -> None:
    log(SKILL, msg, quiet=quiet)


# =============================================================================
# Fetch + digest each category
# =============================================================================


def digest_hot_inbound(results: dict[str, dict[str, Any]], now: datetime) -> dict[str, Any]:
    """Anything that arrived in the last 24h and hasn't been replied to."""
    cutoff = now - timedelta(hours=24)
    items: list[dict[str, Any]] = []

    # Unread inbound email threads
    for thread in results.get("email/threads", {}).get("data", []):
        if thread.get("is_read", True):
            continue
        if thread.get("last_message_direction") != "inbound":
            continue
        last_at = parse_iso(thread.get("last_message_at"))
        if last_at and last_at >= cutoff:
            items.append({
                "kind": "email_thread",
                "id": thread.get("id"),
                "subject": thread.get("subject") or "(no subject)",
                "preview": (thread.get("last_message_preview") or "")[:120],
                "when": thread.get("last_message_at"),
                "message_count": thread.get("message_count"),
            })

    # Unread SMS conversations
    for conv in results.get("sms/conversations", {}).get("data", []):
        last_at = parse_iso(conv.get("last_message_at"))
        if last_at and last_at >= cutoff and (conv.get("unread_count") or 0) > 0:
            items.append({
                "kind": "sms_conversation",
                "id": conv.get("id"),
                "from": conv.get("external_phone_number"),
                "preview": (conv.get("last_message_preview") or "")[:120],
                "when": conv.get("last_message_at"),
                "unread_count": conv.get("unread_count"),
            })

    # Missed inbound phone calls (status in missed/no-answer/voicemail)
    for call in results.get("phone/call-logs", {}).get("data", []):
        if call.get("direction") != "inbound":
            continue
        if call.get("status") not in {"missed", "no-answer", "voicemail", "failed"}:
            continue
        call_at = parse_iso(call.get("start_time") or call.get("created_at"))
        if call_at and call_at >= cutoff:
            items.append({
                "kind": "missed_call",
                "id": call.get("id"),
                "from": call.get("from_number"),
                "duration_sec": call.get("duration"),
                "when": call.get("start_time") or call.get("created_at"),
                "recording_url": call.get("recording_url"),
                "linked_entities": call.get("linked_entities"),
            })

    # New form submissions in window
    for sub in results.get("forms/submissions", {}).get("data", []):
        sub_at = parse_iso(sub.get("completed_at") or sub.get("created_at"))
        if sub_at and sub_at >= cutoff:
            items.append({
                "kind": "form_submission",
                "id": sub.get("id"),
                "submitter_name": sub.get("recipient_name"),
                "submitter_email": sub.get("recipient_email"),
                "ai_summary": (sub.get("ai_summary") or "")[:200],
                "when": sub.get("completed_at") or sub.get("created_at"),
            })

    items.sort(key=lambda x: x.get("when") or "", reverse=True)
    return {"count": len(items), "items": items[:10]}


def digest_overdue(results: dict[str, dict[str, Any]], now: datetime) -> dict[str, Any]:
    """Tasks past due that haven't been completed, plus opportunities with
    a next_action_date in the past."""
    items: list[dict[str, Any]] = []

    for task in results.get("tasks", {}).get("data", []):
        if task.get("completed_at"):
            continue
        if (task.get("status") or "").lower() in {"completed", "cancelled"}:
            continue
        due = parse_iso(task.get("due_date"))
        if due and due < now:
            items.append({
                "kind": "task",
                "id": task.get("id"),
                "title": task.get("title"),
                "priority": task.get("priority"),
                "opportunity_id": task.get("deal_id"),
                "contact_id": task.get("contact_id"),
                "due": task.get("due_date"),
                "days_overdue": days_since(due, now),
            })

    # Opportunities with an overdue next_action_date — operator forgot to do something
    for opp in results.get("opportunities", {}).get("data", []):
        if not _opp_is_active(opp):
            continue
        nad = parse_iso(opp.get("next_action_date"))
        if nad and nad < now:
            items.append({
                "kind": "overdue_next_action",
                "id": opp.get("id"),
                "title": f"{opp.get('next_action_name') or 'Next action'} on {opp.get('name')}",
                "opportunity_id": opp.get("id"),
                "due": opp.get("next_action_date"),
                "days_overdue": days_since(nad, now),
                "value": opp.get("value"),
            })

    items.sort(key=lambda x: x.get("days_overdue") or 0, reverse=True)
    return {"count": len(items), "items": items[:5]}


def digest_going_quiet(results: dict[str, dict[str, Any]], now: datetime,
                       silence_days: int = 7) -> dict[str, Any]:
    """Active opportunities not touched in N+ days and with no scheduled next action."""
    cutoff_seconds = silence_days * 86400
    items: list[dict[str, Any]] = []

    for opp in results.get("opportunities", {}).get("data", []):
        if not _opp_is_active(opp):
            continue
        # If a future next-action is scheduled, this isn't "going quiet" — it's "in progress"
        nad = parse_iso(opp.get("next_action_date"))
        if nad and nad >= now:
            continue

        last_touch = parse_iso(opp.get("updated_at"))
        if not last_touch:
            continue
        seconds_since = (now - last_touch).total_seconds()
        if seconds_since < cutoff_seconds:
            continue

        items.append({
            "kind": "silent_opportunity",
            "id": opp.get("id"),
            "name": opp.get("name"),
            "value": opp.get("value"),
            "currency": opp.get("currency"),
            "stage": _opp_stage(opp),
            "lead_source": opp.get("lead_source"),
            "last_touch": opp.get("updated_at"),
            "days_silent": int(seconds_since // 86400),
            "primary_contact_id": opp.get("contact_id"),
        })

    # Rank: highest-value first; ties broken by longest silence
    items.sort(key=lambda x: (float(x.get("value") or 0), x.get("days_silent") or 0), reverse=True)
    return {"count": len(items), "items": items[:5]}


def digest_todays_calendar(results: dict[str, dict[str, Any]], now: datetime) -> dict[str, Any]:
    """Bookings starting today + tasks due today (UTC day window)."""
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)
    items: list[dict[str, Any]] = []

    for booking in results.get("scheduling/bookings", {}).get("data", []):
        if (booking.get("status") or "").lower() == "cancelled":
            continue
        when = parse_iso(booking.get("starts_at"))
        if when and today_start <= when < today_end:
            items.append({
                "kind": "booking",
                "id": booking.get("id"),
                "title": "Booking",  # event_type_name needs an expand we'd add later
                "booker_name": booking.get("booker_name"),
                "booker_email": booking.get("booker_email"),
                "when": booking.get("starts_at"),
                "ends_at": booking.get("ends_at"),
                "meeting_url": booking.get("google_meet_link"),
                "opportunity_id": booking.get("deal_id"),
                "contact_id": booking.get("contact_id"),
            })

    for task in results.get("tasks", {}).get("data", []):
        if task.get("completed_at"):
            continue
        due = parse_iso(task.get("due_date"))
        if due and today_start <= due < today_end:
            items.append({
                "kind": "task_today",
                "id": task.get("id"),
                "title": task.get("title"),
                "priority": task.get("priority"),
                "when": task.get("due_date"),
                "opportunity_id": task.get("deal_id"),
            })

    items.sort(key=lambda x: x.get("when") or "")
    return {"count": len(items), "items": items}


def digest_pipeline_pulse(results: dict[str, dict[str, Any]], now: datetime) -> dict[str, Any]:
    """Derive pipeline state from the opportunities list."""
    opportunities = results.get("opportunities", {}).get("data", [])
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    by_stage: dict[str, dict[str, Any]] = {}
    total_open_value = 0.0
    won_this_month_value = 0.0
    won_this_month_count = 0
    lost_this_month_value = 0.0
    lost_this_month_count = 0
    open_count = 0

    for opp in opportunities:
        status = (opp.get("status") or "").lower()
        value = float(opp.get("value") or 0)
        stage_name = _opp_stage(opp) or "Unstaged"

        bucket = by_stage.setdefault(stage_name, {"count": 0, "value": 0.0})
        bucket["count"] += 1
        bucket["value"] += value

        if _opp_is_active(opp):
            total_open_value += value
            open_count += 1
        else:
            close_date = parse_iso(opp.get("actual_close_date") or opp.get("lost_at"))
            if close_date and close_date >= month_start:
                if status == "won":
                    won_this_month_value += value
                    won_this_month_count += 1
                elif status == "lost":
                    lost_this_month_value += value
                    lost_this_month_count += 1

    return {
        "total_open_value": total_open_value,
        "open_count": open_count,
        "won_this_month_count": won_this_month_count,
        "won_this_month_value": won_this_month_value,
        "lost_this_month_count": lost_this_month_count,
        "lost_this_month_value": lost_this_month_value,
        "by_stage": by_stage,
    }


# =============================================================================
# Orchestrator
# =============================================================================


def fetch_and_digest(quiet: bool = False) -> dict[str, Any]:
    now = now_utc()
    yesterday = now - timedelta(hours=24)
    cutoff_iso = yesterday.isoformat()

    _log("resolving endpoint paths from catalog...", quiet=quiet)

    # Resolve every path via the public API catalog at docs.trustpager.com.
    # This insulates the script from path renames — when the API changes,
    # the catalog updates within ~24h and BOS picks up the new paths
    # automatically (or sooner if the user clears ~/.claude/bos-cache).
    try:
        paths = {
            "opportunities":    resolve_path("opportunities"),
            "tasks":            resolve_path("tasks"),
            "bookings":         resolve_path("scheduling", path_contains="bookings"),
            "email_threads":    resolve_path("email", path_contains="threads"),
            "sms_convos":       resolve_path("sms"),
            "phone_calls":      resolve_path("phone", path_contains="call-logs"),
            "form_subs":        resolve_path("forms", path_contains="submissions"),
        }
    except BOSError as e:
        raise BOSError(
            f"Could not resolve API paths from the catalog: {e}\n"
            f"Falling back is not yet implemented — please report this bug."
        ) from None

    _log("fanning out 7 parallel API calls...", quiet=quiet)

    calls = [
        (paths["opportunities"], {"limit": 100}),
        (paths["tasks"],         {"limit": 100}),
        (paths["bookings"],      {"limit": 50}),
        (paths["email_threads"], {"limit": 50}),
        (paths["sms_convos"],    {"limit": 50}),
        (paths["phone_calls"],   {"limit": 50}),
        (paths["form_subs"],     {"limit": 50}),
    ]

    results = parallel_get(calls)

    for path, _params in calls:
        if results.get(path, {}).get("error"):
            err_line = results[path]["error"].splitlines()[0]
            _log(f"  ! {path}: {err_line}", quiet=quiet)
        else:
            count = len(results.get(path, {}).get("data", []))
            _log(f"  ok {path}: {count} rows", quiet=quiet)

    _log("digesting...", quiet=quiet)

    return {
        "generated_at": now.isoformat(),
        "hot_inbound": digest_hot_inbound(results, now),
        "overdue": digest_overdue(results, now),
        "going_quiet": digest_going_quiet(results, now),
        "todays_calendar": digest_todays_calendar(results, now),
        "pipeline_pulse": digest_pipeline_pulse(results, now),
        "_raw_call_status": {
            path: ("ok" if not results.get(path, {}).get("error") else "error")
            for path, _ in calls
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Sweep My Day data fetcher")
    parser.add_argument("--json-only", action="store_true",
                        help="Suppress stderr progress logs")
    args = parser.parse_args()

    try:
        digest = fetch_and_digest(quiet=args.json_only)
        emit_json(digest)
        return 0
    except BOSError as e:
        emit_error_and_exit(str(e), code=1)
    except KeyboardInterrupt:
        emit_error_and_exit("Cancelled", code=130)


if __name__ == "__main__":
    sys.exit(main())


# =============================================================================
# Output shape — what Claude reads from stdout
# =============================================================================
#
# {
#   "generated_at": "2026-05-31T10:00:00+00:00",
#   "hot_inbound": {
#     "count": 4,
#     "items": [
#       {"kind": "email_thread", "id": "...", "subject": "...", "preview": "...",
#        "when": "...", "message_count": 2},
#       {"kind": "sms_conversation", "id": "...", "from": "+61...", "preview": "...",
#        "when": "...", "unread_count": 1},
#       {"kind": "missed_call", "id": "...", "from": "+61...", "duration_sec": 0,
#        "when": "...", "recording_url": "...", "linked_entities": {...}},
#       {"kind": "form_submission", "id": "...", "submitter_name": "...",
#        "submitter_email": "...", "ai_summary": "...", "when": "..."}
#     ]
#   },
#   "overdue": {
#     "count": 7,
#     "items": [
#       {"kind": "task", "id": "...", "title": "...", "priority": "high",
#        "opportunity_id": "...", "due": "...", "days_overdue": 3},
#       {"kind": "overdue_next_action", "id": "<opp_id>",
#        "title": "Call back on Acme deal", "due": "...", "days_overdue": 2,
#        "value": 12000}
#     ]
#   },
#   "going_quiet": {
#     "count": 12,
#     "items": [
#       {"kind": "silent_opportunity", "id": "...", "name": "...", "value": 35000,
#        "currency": "AUD", "stage": "Quote Sent", "lead_source": "Referral",
#        "last_touch": "...", "days_silent": 14, "primary_contact_id": "..."}
#     ]
#   },
#   "todays_calendar": {
#     "count": 3,
#     "items": [
#       {"kind": "booking", "id": "...", "booker_name": "...", "booker_email": "...",
#        "when": "...", "ends_at": "...", "meeting_url": "...",
#        "opportunity_id": "...", "contact_id": "..."},
#       {"kind": "task_today", "id": "...", "title": "...", "priority": "medium",
#        "when": "...", "opportunity_id": "..."}
#     ]
#   },
#   "pipeline_pulse": {
#     "total_open_value": 248500.00,
#     "open_count": 32,
#     "won_this_month_count": 4,
#     "won_this_month_value": 48000,
#     "lost_this_month_count": 2,
#     "lost_this_month_value": 8500,
#     "by_stage": { "Qualified": {"count": 8, "value": 95000}, ... }
#   },
#   "_raw_call_status": { "opportunities": "ok", "tasks": "ok", ... }
# }
