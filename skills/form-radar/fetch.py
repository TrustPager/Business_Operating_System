#!/usr/bin/env python3
"""form-radar — pull every form submission into one funnel + follow-up digest.

Owners send forms and lose track of who filled them. This fetcher returns a
single JSON document Claude turns into a follow-up report: the sent → opened →
completed funnel, plus the follow-up buckets — "opened/started but not
completed" (stalled, nudge) and "sent but never opened, going stale" (chase).

Read-only (list_form_submissions). Auth: TRUSTPAGER_API_KEY env var or
~/.claude/bos.json.

Usage:
    python skills/form-radar/fetch.py
    python skills/form-radar/fetch.py --stale-days 5
    python skills/form-radar/fetch.py --json-only
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

SKILL = "form-radar"

STARTED_NOT_DONE = {"viewed", "opened", "in_progress"}
DONE = {"completed"}
DEAD = {"expired", "voided"}


def _age_days(sub: dict, now) -> float | None:
    ts = sub.get("sent_at") or sub.get("created_at") or sub.get("updated_at")
    dt = parse_iso(ts) if ts else None
    return days_since(dt, now) if dt else None


def fetch(stale_days: int, quiet: bool) -> dict:
    now = now_utc()
    log(SKILL, "listing form submissions...", quiet=quiet)

    subs = list(paginate(resolve_path("forms/submissions"), limit=100, max_pages=20))

    funnel = {"sent": 0, "opened": 0, "in_progress": 0, "completed": 0,
              "expired": 0, "voided": 0, "draft": 0, "other": 0}
    started_not_completed: list[dict] = []
    sent_never_opened_stale: list[dict] = []
    recently_completed: list[dict] = []

    for sub in subs:
        status = (sub.get("status") or "").lower()
        age = _age_days(sub, now)
        row = {
            "submission_id": sub.get("id"),
            "template_id": sub.get("template_id"),
            "template_name": sub.get("template_name") or "(form)",
            "deal_id": sub.get("deal_id"),
            "contact_id": sub.get("contact_id"),
            "status": status,
            "age_days": round(age, 1) if age is not None else None,
        }

        if status in ("viewed", "opened"):
            funnel["opened"] += 1
            started_not_completed.append(row)
        elif status == "in_progress":
            funnel["in_progress"] += 1
            started_not_completed.append(row)
        elif status == "completed":
            funnel["completed"] += 1
            if age is not None and age <= 7:
                recently_completed.append(row)
        elif status == "expired":
            funnel["expired"] += 1
        elif status == "voided":
            funnel["voided"] += 1
        elif status == "draft":
            funnel["draft"] += 1
        elif status in ("pending", "sent"):
            funnel["sent"] += 1
            if age is not None and age >= stale_days:
                sent_never_opened_stale.append(row)
        else:
            funnel["other"] += 1

    started_not_completed.sort(key=lambda r: r["age_days"] or 0, reverse=True)
    sent_never_opened_stale.sort(key=lambda r: r["age_days"] or 0, reverse=True)

    return {
        "skill": SKILL,
        "generated_at": now.isoformat(),
        "stale_days_threshold": stale_days,
        "total_submissions": len(subs),
        "funnel": funnel,
        "started_not_completed": started_not_completed,      # nudge — they began and stalled
        "sent_never_opened_stale": sent_never_opened_stale,  # chase or resend
        "recently_completed": recently_completed,
    }


def main() -> None:
    force_utf8_stdout()
    ap = argparse.ArgumentParser(description="Form submission funnel + follow-up digest")
    ap.add_argument("--stale-days", type=int, default=5,
                    help="Flag 'sent but never opened' once older than this many days (default 5)")
    ap.add_argument("--json-only", action="store_true", help="Suppress progress logs")
    args = ap.parse_args()
    try:
        emit_json(fetch(args.stale_days, quiet=args.json_only))
    except BOSError as e:
        emit_error_and_exit(e)


if __name__ == "__main__":
    main()
