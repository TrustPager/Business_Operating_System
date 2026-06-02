#!/usr/bin/env python3
"""work-order-radar — pull every work order into one board + stall digest.

Owners raise work orders and then jobs quietly stall in one status. This fetcher
returns a single JSON document Claude turns into a report: the count by status,
plus the jobs that have sat too long in one status (stalled) and the ones marked
complete (candidates for a completion update / review ask).

Read-only (list_work_orders + list_work_order_statuses). Auth: TRUSTPAGER_API_KEY
env var or ~/.claude/bos.json.

Usage:
    python skills/work-order-radar/fetch.py
    python skills/work-order-radar/fetch.py --stall-days 14
    python skills/work-order-radar/fetch.py --json-only
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))
from trustpager_api import (  # noqa: E402
    BOSError, emit_error_and_exit, emit_json, force_utf8_stdout,
    log, now_utc, paginate, parse_iso, days_since, resolve_path,
)

SKILL = "work-order-radar"

# Status labels we treat as terminal (don't flag as stalled).
TERMINAL = {"complete", "completed", "done", "closed", "cancelled", "canceled"}


def _status_label(wo: dict) -> str:
    s = wo.get("status") or wo.get("status_name") or wo.get("work_order_status") or ""
    if isinstance(s, dict):
        s = s.get("name") or s.get("label") or ""
    return str(s)


def _days_in_status(wo: dict, now) -> float | None:
    ts = wo.get("status_changed_at") or wo.get("updated_at") or wo.get("created_at")
    dt = parse_iso(ts) if ts else None
    return days_since(dt, now) if dt else None


def fetch(stall_days: int, quiet: bool) -> dict:
    now = now_utc()
    log(SKILL, "listing work orders...", quiet=quiet)

    work_orders = list(paginate(resolve_path("work-orders"), limit=100, max_pages=20))

    by_status: dict[str, int] = {}
    stalled: list[dict] = []
    complete_recent: list[dict] = []

    for wo in work_orders:
        label = _status_label(wo) or "(no status)"
        by_status[label] = by_status.get(label, 0) + 1
        days = _days_in_status(wo, now)
        row = {
            "work_order_id": wo.get("id"),
            "name": wo.get("name") or wo.get("title") or wo.get("deal_name") or "(work order)",
            "deal_id": wo.get("deal_id"),
            "status": label,
            "days_in_status": round(days, 1) if days is not None else None,
        }

        is_terminal = label.strip().lower() in TERMINAL
        if is_terminal:
            if days is not None and days <= 7:
                complete_recent.append(row)
        elif days is not None and days >= stall_days:
            stalled.append(row)

    stalled.sort(key=lambda r: r["days_in_status"] or 0, reverse=True)

    return {
        "skill": SKILL,
        "generated_at": now.isoformat(),
        "stall_days_threshold": stall_days,
        "total_work_orders": len(work_orders),
        "by_status": by_status,
        "stalled": stalled,                 # sitting too long in a non-terminal status
        "recently_completed": complete_recent,  # candidates for a completion update / review ask
    }


def main() -> None:
    force_utf8_stdout()
    ap = argparse.ArgumentParser(description="Work order board + stall digest")
    ap.add_argument("--stall-days", type=int, default=14,
                    help="Flag a non-terminal work order once it's sat this many days in status (default 14)")
    ap.add_argument("--json-only", action="store_true", help="Suppress progress logs")
    args = ap.parse_args()
    try:
        emit_json(fetch(args.stall_days, quiet=args.json_only))
    except BOSError as e:
        emit_error_and_exit(e)


if __name__ == "__main__":
    main()
