#!/usr/bin/env python3
"""audit-my-automations — pull every automation + recent run health into one digest.

Operators set automations up and never check them. This fetcher returns a single
JSON document Claude can turn into a health report: which automations are firing,
which are stale, which are erroring, which are missing safety dials, and which
overlap with each other.

What it computes (all from read-only endpoints):
- Per automation: enabled, trigger_count, action_count, dedup, daily cap,
  last_run_at, recent run status mix (completed / skipped / failed).
- Flags: disabled, no_actions, no_triggers, never_run, stale (enabled but no
  run in 30d), recent_failures, mostly_skipped, sends_without_dedup,
  webhook_without_cap.
- Cross-automation: trigger overlaps (≥2 enabled automations on the same
  trigger_type + source).

Auth: TRUSTPAGER_API_KEY env var or ~/.claude/bos.json.

Usage:
    python skills/audit-my-automations/fetch.py
    python skills/audit-my-automations/fetch.py --json-only
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))
from trustpager_api import (  # noqa: E402
    BOSError, api_get, emit_error_and_exit, emit_json, force_utf8_stdout,
    log, now_utc, paginate, parallel_get, parse_iso, days_since, resolve_path,
)

SKILL = "audit-my-automations"

STALE_DAYS = 30
RECENT_RUN_LIMIT = 10  # how many recent runs to sample per automation

# Action types that reach a customer / cost credits — these want dedup ON.
SEND_ACTION_TYPES = {
    "send_custom_email", "send_gmail_email", "send_sms", "send_whatsapp",
    "voice_outbound_call", "send_form", "send_for_signing", "send_marketing_email",
}
# Action types with an external/feedback path — these want a daily cap.
WEBHOOK_ACTION_TYPES = {"call_webhook", "facebook_conversion"}

# Trigger types that fire WITHOUT an automations_triggers row — they're driven by
# stage_id, a queue, a schedule, or a direct API/manual invoke. Having zero
# trigger rows is normal for these, so don't flag them as "no_triggers".
NO_TRIGGER_ROW_TYPES = {
    "stage_changed", "manual", "api", "event_queue_step", "auto_queue", "scheduled",
}


def _trigger_key(t: dict) -> str:
    return f"{t.get('trigger_type') or '?'}:{t.get('source_type') or 'any'}:{t.get('source_id') or '*'}"


def fetch(quiet: bool) -> dict:
    now = now_utc()
    log(SKILL, "listing automations...", quiet=quiet)

    # The list endpoint returns FLAT automations (no embedded triggers/actions).
    # GET /automations/:id DOES embed automations_triggers + automations_actions
    # + conditions, so we fetch detail per automation to know its real structure.
    listed = list(paginate(resolve_path("automations"), limit=100, max_pages=10))
    ids = [a["id"] for a in listed if a.get("id")]
    log(SKILL, f"{len(ids)} automations; fetching structure...", quiet=quiet)

    detail_by_path = parallel_get([(f"automations/{i}", {}) for i in ids]) if ids else {}

    def _detail(aid: str, fallback: dict) -> dict:
        resp = detail_by_path.get(f"automations/{aid}", {})
        if isinstance(resp, dict) and "error" not in resp:
            return resp.get("data", resp)
        return fallback  # detail fetch failed — degrade to the flat list row

    automations = [_detail(a["id"], a) for a in listed if a.get("id")]

    # Sample recent runs only for ENABLED automations (disabled ones can't fire,
    # and stale/failed flags only apply to live ones) — keeps the call count down.
    enabled_ids = [a["id"] for a in automations if a.get("id") and a.get("enabled")]
    log(SKILL, f"sampling runs for {len(enabled_ids)} enabled...", quiet=quiet)
    runs_by_path = parallel_get(
        [(f"automations/{i}/runs", {"limit": RECENT_RUN_LIMIT}) for i in enabled_ids]
    ) if enabled_ids else {}

    audited: list[dict] = []
    trigger_map: dict[str, list[str]] = {}  # trigger_key -> [automation names] (enabled only)

    for a in automations:
        aid = a.get("id")
        triggers = a.get("automations_triggers") or a.get("triggers") or []
        actions = a.get("automations_actions") or a.get("actions") or []
        enabled = bool(a.get("enabled"))
        trigger_type = a.get("trigger_type")

        runs_resp = runs_by_path.get(f"automations/{aid}/runs", {})
        runs = runs_resp.get("data", []) if isinstance(runs_resp, dict) else []
        last_run_at = None
        status_mix = {"completed": 0, "skipped": 0, "failed": 0, "other": 0}
        for r in runs:
            ts = parse_iso(r.get("started_at") or r.get("created_at"))
            if ts and (last_run_at is None or ts > last_run_at):
                last_run_at = ts
            st = (r.get("status") or "other").lower()
            status_mix[st if st in status_mix else "other"] += 1

        action_types = [ac.get("action_type") for ac in actions]
        has_send = any(at in SEND_ACTION_TYPES for at in action_types)
        has_webhook = any(at in WEBHOOK_ACTION_TYPES for at in action_types)
        dedup_on = bool(a.get("dedup_enabled"))
        daily_cap = a.get("max_executions_per_day")

        # ---- flags ----
        flags: list[str] = []
        if not enabled:
            flags.append("disabled")
        if not actions:
            flags.append("no_actions")
        if not triggers and trigger_type not in NO_TRIGGER_ROW_TYPES:
            flags.append("no_triggers")
        if enabled and not runs:
            flags.append("never_run")
        days_idle = days_since(last_run_at, now) if last_run_at else None
        if enabled and last_run_at and days_idle is not None and days_idle >= STALE_DAYS:
            flags.append(f"stale_{days_idle}d")
        if status_mix["failed"] > 0:
            flags.append(f"recent_failures_{status_mix['failed']}")
        sampled = sum(status_mix.values())
        if sampled >= 3 and status_mix["skipped"] >= sampled * 0.8:
            flags.append("mostly_skipped")  # conditions may be too tight
        if enabled and has_send and not dedup_on:
            flags.append("sends_without_dedup")
        if enabled and has_webhook and daily_cap is None:
            flags.append("webhook_without_daily_cap")

        if enabled:
            for t in (triggers or []):
                trigger_map.setdefault(_trigger_key(t), []).append(a.get("name") or aid)

        audited.append({
            "id": aid,
            "name": a.get("name"),
            "enabled": enabled,
            "trigger_type": trigger_type,
            "trigger_count": len(triggers),
            "triggers": [
                {"trigger_type": t.get("trigger_type"), "source_type": t.get("source_type"),
                 "source_id": t.get("source_id")} for t in triggers
            ],
            "action_count": len(actions),
            "action_types": action_types,
            "dedup_enabled": dedup_on,
            "max_executions_per_day": daily_cap,
            "last_run_at": last_run_at.isoformat() if last_run_at else None,
            "days_idle": days_idle,
            "recent_runs_sampled": sampled,
            "recent_status_mix": status_mix,
            "flags": flags,
            "url": f"https://app.trustpager.com/auto/automations/{aid}",
        })

    overlaps = [
        {"trigger": k, "automations": v}
        for k, v in trigger_map.items() if len(v) > 1
    ]

    needs_attention = [a for a in audited
                       if any(f.startswith(("recent_failures", "no_actions", "no_triggers"))
                              for f in a["flags"])]
    warnings = [a for a in audited
                if a not in needs_attention and any(
                    f.startswith(("stale_", "never_run", "mostly_skipped",
                                  "sends_without_dedup", "webhook_without_daily_cap"))
                    for f in a["flags"])]

    return {
        "generated_at": now.isoformat(),
        "headline": {
            "total": len(audited),
            "enabled": sum(1 for a in audited if a["enabled"]),
            "disabled": sum(1 for a in audited if not a["enabled"]),
            "needs_attention": len(needs_attention),
            "warnings": len(warnings),
            "trigger_overlaps": len(overlaps),
        },
        "needs_attention": needs_attention,
        "warnings": warnings,
        "trigger_overlaps": overlaps,
        "all_automations": audited,
    }


def main() -> int:
    force_utf8_stdout()
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--json-only", action="store_true", help="Suppress stderr progress logs")
    args = parser.parse_args()
    try:
        emit_json(fetch(quiet=args.json_only))
        return 0
    except BOSError as e:
        emit_error_and_exit(str(e), code=1)


if __name__ == "__main__":
    sys.exit(main())
