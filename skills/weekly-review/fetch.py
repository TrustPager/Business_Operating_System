#!/usr/bin/env python3
"""weekly-review — the Friday rollup: what shipped, what stalled, where the pipeline sits.

Returns one JSON document Claude turns into a weekly review: the wins (deals won,
tasks completed, new opportunities created), the stalls (deals gone quiet,
overdue tasks carried over), and the current pipeline shape. All read-only.

Window defaults to the last 7 days. Auth: TRUSTPAGER_API_KEY env var or
~/.claude/bos.json.

Usage:
    python skills/weekly-review/fetch.py
    python skills/weekly-review/fetch.py --days 7
    python skills/weekly-review/fetch.py --json-only
"""

from __future__ import annotations

import argparse
import sys
from datetime import timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))
from trustpager_api import (  # noqa: E402
    BOSError, emit_error_and_exit, emit_json, force_utf8_stdout,
    log, now_utc, parallel_get, parse_iso, days_since, resolve_path,
)

SKILL = "weekly-review"
QUIET_DAYS = 7  # an open deal with no activity in this many days = "going quiet"


def _opp_value(o: dict) -> float:
    try:
        return float(o.get("amount") or o.get("value") or 0)
    except (TypeError, ValueError):
        return 0.0


def _status(o: dict) -> str:
    return (o.get("status") or "").lower()


def fetch(days: int, quiet: bool) -> dict:
    now = now_utc()
    cutoff = now - timedelta(days=days)
    log(SKILL, f"pulling the last {days} days...", quiet=quiet)

    results = parallel_get([
        (resolve_path("opportunities"), {"limit": 200}),
        (resolve_path("tasks"), {"limit": 200}),
    ])
    opps = results.get(resolve_path("opportunities"), {}).get("data", []) or []
    tasks = results.get(resolve_path("tasks"), {}).get("data", []) or []

    won, lost, created = [], [], []
    quiet_open, open_value, open_count = [], 0.0, 0

    for o in opps:
        st = _status(o)
        changed = parse_iso(o.get("updated_at"))
        made = parse_iso(o.get("created_at"))
        row = {"id": o.get("id"), "name": o.get("name") or "(opportunity)", "value": _opp_value(o)}

        if st == "won" and changed and changed >= cutoff:
            won.append(row)
        elif st == "lost" and changed and changed >= cutoff:
            lost.append(row)
        if made and made >= cutoff:
            created.append(row)

        if st == "open":
            open_count += 1
            open_value += _opp_value(o)
            last_act = parse_iso(o.get("last_activity_at"))
            silent = days_since(last_act, now) if last_act else (days_since(made, now) if made else None)
            if silent is not None and silent >= QUIET_DAYS:
                quiet_open.append({**row, "days_silent": round(silent, 1)})

    completed_tasks, overdue_tasks = [], []
    for t in tasks:
        done = parse_iso(t.get("completed_at"))
        tstatus = (t.get("status") or "").lower()
        if done and done >= cutoff:
            completed_tasks.append({"id": t.get("id"), "title": t.get("title") or "(task)"})
        elif tstatus not in {"completed", "cancelled"} and not t.get("completed_at"):
            due = parse_iso(t.get("due_date"))
            if due and due < now:
                overdue_tasks.append({
                    "id": t.get("id"), "title": t.get("title") or "(task)",
                    "days_overdue": round(days_since(due, now), 1),
                })

    won.sort(key=lambda r: r["value"], reverse=True)
    quiet_open.sort(key=lambda r: (r["value"] * (r["days_silent"] or 1)), reverse=True)
    overdue_tasks.sort(key=lambda r: r["days_overdue"], reverse=True)

    return {
        "skill": SKILL,
        "generated_at": now.isoformat(),
        "window_days": days,
        "shipped": {
            "won": won,
            "won_value": round(sum(r["value"] for r in won), 2),
            "lost": lost,
            "new_opportunities": len(created),
            "tasks_completed": len(completed_tasks),
        },
        "stalled": {
            "going_quiet": quiet_open[:10],
            "going_quiet_count": len(quiet_open),
            "overdue_tasks": overdue_tasks[:10],
            "overdue_count": len(overdue_tasks),
        },
        "pipeline_now": {
            "open_count": open_count,
            "open_value": round(open_value, 2),
        },
    }


def main() -> None:
    force_utf8_stdout()
    ap = argparse.ArgumentParser(description="Weekly review rollup")
    ap.add_argument("--days", type=int, default=7, help="Window in days (default 7)")
    ap.add_argument("--json-only", action="store_true", help="Suppress progress logs")
    args = ap.parse_args()
    try:
        emit_json(fetch(args.days, quiet=args.json_only))
    except BOSError as e:
        emit_error_and_exit(e)


if __name__ == "__main__":
    main()
