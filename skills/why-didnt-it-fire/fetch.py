#!/usr/bin/env python3
"""why-didnt-it-fire — pull one automation + its run history into a diagnostic bundle.

"My automation didn't fire" almost always resolves to one of:
  1. it's DISABLED
  2. NO run row exists  -> the trigger never matched (wrong trigger_type/source)
  3. a run exists with status SKIPPED -> a condition didn't pass
  4. a run FAILED -> an action errored (read error_message)
  5. it actually COMPLETED -> it DID fire; the operator expected a different outcome

This fetcher gathers everything needed to walk that ladder: the automation's
structure (enabled, triggers, conditions, actions) plus its recent runs with
status / trigger_type / error_message / skipped actions — and emits a
`likely_reason` hint Claude can confirm.

Auth: TRUSTPAGER_API_KEY env var or ~/.claude/bos.json.

Usage:
    python skills/why-didnt-it-fire/fetch.py <automation-id-or-name>
    python skills/why-didnt-it-fire/fetch.py "renewal reminder"
    python skills/why-didnt-it-fire/fetch.py 1965b66f-... --json-only
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))
from trustpager_api import (  # noqa: E402
    BOSError, api_get, emit_error_and_exit, emit_json, force_utf8_stdout,
    log, now_utc, paginate, parse_iso, days_since, resolve_path,
)

SKILL = "why-didnt-it-fire"
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)
RUN_LIMIT = 15


def _resolve_automation(ident: str, quiet: bool) -> dict:
    """Find the automation by UUID (exact) or by name fragment (search)."""
    if UUID_RE.match(ident.strip()):
        resp = api_get(f"automations/{ident.strip()}")
        a = resp.get("data", resp) if isinstance(resp, dict) else resp
        if a and a.get("id"):
            return a
        raise BOSError(f"No automation with id {ident}")

    log(SKILL, f"searching automations matching '{ident}'...", quiet=quiet)
    matches = [a for a in paginate(resolve_path("automations"), limit=100, max_pages=10)
               if ident.lower() in (a.get("name") or "").lower()]
    if not matches:
        raise BOSError(
            f"No automation whose name contains '{ident}'. "
            f"Run /audit-my-automations to list them, or pass the automation id."
        )
    if len(matches) > 1:
        names = ", ".join(f"{a.get('name')} ({a.get('id')})" for a in matches[:8])
        raise BOSError(
            f"'{ident}' matches {len(matches)} automations: {names}. "
            f"Re-run with the exact id."
        )
    # Re-fetch by id to get triggers/actions/conditions inline
    full = api_get(f"automations/{matches[0]['id']}")
    return full.get("data", full) if isinstance(full, dict) else matches[0]


def fetch(ident: str, quiet: bool) -> dict:
    now = now_utc()
    a = _resolve_automation(ident, quiet)
    aid = a.get("id")
    log(SKILL, f"diagnosing '{a.get('name')}' ({aid})...", quiet=quiet)

    triggers = a.get("automations_triggers") or a.get("triggers") or []
    actions = a.get("automations_actions") or a.get("actions") or []
    conditions = a.get("conditions")
    enabled = bool(a.get("enabled"))

    runs_resp = api_get(f"automations/{aid}/runs", limit=RUN_LIMIT)
    runs = runs_resp.get("data", []) if isinstance(runs_resp, dict) else []

    norm_runs = []
    last_run_at = None
    for r in runs:
        ts = parse_iso(r.get("started_at") or r.get("created_at"))
        if ts and (last_run_at is None or ts > last_run_at):
            last_run_at = ts
        norm_runs.append({
            "id": r.get("id"),
            "status": r.get("status"),
            "trigger_type": r.get("trigger_type"),
            "started_at": r.get("started_at") or r.get("created_at"),
            "error_message": r.get("error_message"),
            "error_details": r.get("error_details"),
            "actions_attempted": r.get("actions_attempted"),
            "actions_completed": r.get("actions_completed"),
            "actions_failed": r.get("actions_failed"),
            "skipped_action_ids": r.get("skipped_action_ids"),
            "triggered_by_type": r.get("triggered_by_type"),
            "triggered_by_id": r.get("triggered_by_id"),
        })

    latest = norm_runs[0] if norm_runs else None

    # ---- likely_reason ladder ----
    if not enabled:
        reason = "DISABLED — the automation is switched off, so it never runs. Enable it (after a test) to start."
    elif not triggers and a.get("trigger_type") != "stage_changed":
        reason = "NO_TRIGGERS — nothing is configured to fire it. Add a trigger."
    elif not actions:
        reason = "NO_ACTIONS — it fires but has no actions, so nothing visibly happens. Add actions."
    elif not norm_runs:
        reason = ("NO_RUNS — it's enabled but has never fired. The trigger/source likely doesn't match "
                  "the real event (wrong trigger_type, wrong source, or website-form-as-form_completed). "
                  "Compare the configured triggers below against how the event actually arrives.")
    elif latest and latest["status"] == "skipped":
        reason = ("SKIPPED — it fired but a CONDITION didn't pass, so actions didn't run. "
                  "Check the conditions against the event's data below.")
    elif latest and latest["status"] == "failed":
        reason = ("FAILED — it fired but an ACTION errored. Read error_message on the latest run below.")
    elif latest and latest["status"] == "completed":
        reason = ("COMPLETED — it DID fire and ran successfully. If the outcome wasn't what you expected, "
                  "the issue is in what an action did (e.g. a blank {{variable}}, wrong recipient, or wrong "
                  "target), not in whether it fired. Inspect the actions.")
    else:
        reason = "UNCLEAR — inspect the runs below."

    return {
        "generated_at": now.isoformat(),
        "automation": {
            "id": aid,
            "name": a.get("name"),
            "enabled": enabled,
            "trigger_type": a.get("trigger_type"),
            "dedup_enabled": a.get("dedup_enabled"),
            "dedup_window_minutes": a.get("dedup_window_minutes"),
            "max_executions_per_day": a.get("max_executions_per_day"),
            "conditions": conditions,
            "triggers": [
                {"trigger_type": t.get("trigger_type"), "source_type": t.get("source_type"),
                 "source_id": t.get("source_id"), "config": t.get("config")} for t in triggers
            ],
            "actions": [
                {"action_type": ac.get("action_type"), "sequence": ac.get("sequence")} for ac in actions
            ],
            "url": f"https://app.trustpager.com/auto/automations/{aid}",
        },
        "last_run_at": last_run_at.isoformat() if last_run_at else None,
        "days_since_last_run": days_since(last_run_at, now) if last_run_at else None,
        "recent_runs": norm_runs,
        "likely_reason": reason,
    }


def main() -> int:
    force_utf8_stdout()
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("automation", help="Automation id (UUID) or a fragment of its name")
    parser.add_argument("--json-only", action="store_true", help="Suppress stderr progress logs")
    args = parser.parse_args()
    try:
        emit_json(fetch(args.automation, quiet=args.json_only))
        return 0
    except BOSError as e:
        emit_error_and_exit(str(e), code=1)


if __name__ == "__main__":
    sys.exit(main())
