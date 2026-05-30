#!/usr/bin/env python3
"""Find data gaps across your TrustPager workspace — the "what's broken" report.

When to use:
- "Where's the mess?"
- After importing a batch of records — what didn't land cleanly?
- Before a board / partner meeting — find the things that'll get asked about.
- Daily cleanup pass.

What it reports:
- 🔗 Opportunities without a contact attached.
- 🏷️  Opportunities without a value set.
- 🏢 Opportunities without a stage / pipeline placement.
- 📅 Tasks past their due date and not marked complete.
- 🚦 Tasks with no due date set at all.
- 👤 Opportunities with no assigned user (no one owns them).

Tight, scannable output — gives you a checklist for the next 10 minutes
of cleanup. All read-only.

Usage:
    python tools/find-gaps.py
    python tools/find-gaps.py --json
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trustpager_api import (  # noqa: E402
    BOSError, api_get, days_since, emit_error_and_exit, emit_json,
    force_utf8_stdout, now_utc, parallel_get, parse_iso, resolve_path,
)


def find_gaps() -> dict[str, Any]:
    now = now_utc()

    paths = {
        "opportunities": resolve_path("opportunities"),
        "tasks":         resolve_path("tasks"),
    }
    results = parallel_get([
        (paths["opportunities"], {"limit": 200}),
        (paths["tasks"], {"limit": 200}),
    ])
    opps = results.get(paths["opportunities"], {}).get("data", [])
    tasks = results.get(paths["tasks"], {}).get("data", [])

    no_contact: list[dict[str, Any]] = []
    no_value: list[dict[str, Any]] = []
    no_stage: list[dict[str, Any]] = []
    no_owner: list[dict[str, Any]] = []
    inactive_statuses = {"won", "lost", "cancelled", "abandoned", "archived"}

    for o in opps:
        if (o.get("status") or "").lower() in inactive_statuses:
            continue
        slim = {"id": o.get("id"), "name": o.get("name")}
        if not o.get("contact_id"):
            no_contact.append(slim)
        if not o.get("value"):
            no_value.append(slim)
        if not (o.get("placements") or []):
            no_stage.append(slim)
        if not (o.get("assigned_user_ids") or o.get("assigned_users") or o.get("owner_id")):
            no_owner.append(slim)

    overdue_tasks: list[dict[str, Any]] = []
    no_due_date_tasks: list[dict[str, Any]] = []
    for t in tasks:
        if t.get("completed_at"):
            continue
        due = t.get("due_date") or t.get("due_at")
        if not due:
            no_due_date_tasks.append({"id": t.get("id"), "title": t.get("title")})
            continue
        due_dt = parse_iso(due)
        if due_dt and due_dt < now:
            overdue_tasks.append({
                "id": t.get("id"),
                "title": t.get("title"),
                "days_overdue": days_since(due_dt, ref=now),
            })

    overdue_tasks.sort(key=lambda x: x["days_overdue"] or 0, reverse=True)

    return {
        "generated_at": now.isoformat(),
        "headline": {
            "opps_sampled": len(opps),
            "tasks_sampled": len(tasks),
            "opps_no_contact": len(no_contact),
            "opps_no_value": len(no_value),
            "opps_no_stage": len(no_stage),
            "opps_no_owner": len(no_owner),
            "tasks_overdue": len(overdue_tasks),
            "tasks_no_due_date": len(no_due_date_tasks),
        },
        "opps_no_contact": no_contact[:20],
        "opps_no_value": no_value[:20],
        "opps_no_stage": no_stage[:20],
        "opps_no_owner": no_owner[:20],
        "tasks_overdue_top_20": overdue_tasks[:20],
        "tasks_no_due_date": no_due_date_tasks[:20],
    }


def _print_human(r: dict[str, Any]) -> None:
    h = r["headline"]
    print("## Workspace gaps")
    print()
    print(f"_Sampled {h['opps_sampled']} opportunities, {h['tasks_sampled']} tasks._")
    print()
    issues = [
        ("🔗 Opportunities without a contact", h["opps_no_contact"], r["opps_no_contact"]),
        ("🏷️  Opportunities without a value", h["opps_no_value"], r["opps_no_value"]),
        ("🏢 Opportunities without a stage", h["opps_no_stage"], r["opps_no_stage"]),
        ("👤 Opportunities with no owner", h["opps_no_owner"], r["opps_no_owner"]),
        ("📅 Tasks overdue", h["tasks_overdue"], r["tasks_overdue_top_20"]),
        ("🚦 Tasks with no due date", h["tasks_no_due_date"], r["tasks_no_due_date"]),
    ]

    anything = False
    for title, count, samples in issues:
        if count == 0:
            continue
        anything = True
        print(f"### {title} — **{count}**")
        for s in samples[:5]:
            label = s.get("name") or s.get("title") or "(unnamed)"
            extra = ""
            if s.get("days_overdue") is not None:
                extra = f"  _({s['days_overdue']} days overdue)_"
            print(f"- {label}{extra}")
        if count > 5:
            print(f"- _… and {count - 5} more_")
        print()

    if not anything:
        print("✅ No gaps found in the sample window. Nice.")


def main() -> int:
    force_utf8_stdout()
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--json", action="store_true",
                        help="Output JSON instead of human-readable markdown")
    args = parser.parse_args()

    try:
        report = find_gaps()
        if args.json:
            emit_json(report)
        else:
            _print_human(report)
        return 0
    except BOSError as e:
        emit_error_and_exit(str(e), code=1)


if __name__ == "__main__":
    sys.exit(main())
