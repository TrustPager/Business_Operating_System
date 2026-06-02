#!/usr/bin/env python3
"""nurture-health — read every auto queue's funnel + engagement into one digest.

Operators ship a nurture sequence and never look at whether it's working. This
fetcher pulls each auto queue's steps, enrolment funnel, per-step drop-off, and
(where the email-log endpoint exposes it) open/click rates — so Claude can say
exactly which step is leaking and whether the un-enrol side is firing.

Everything here is read-only. The endpoints for queues / enrolments / board /
email-logs vary by workspace and API version, so every phase is best-effort:
if a phase can't be reached it lands in `warnings` and `_sources`, and the
digest is emitted with whatever was gathered. The SKILL documents the MCP
fallbacks for anything that degrades.

Auth: TRUSTPAGER_API_KEY env var or ~/.claude/bos.json.

Usage:
    python skills/nurture-health/fetch.py
    python skills/nurture-health/fetch.py --json-only
    python skills/nurture-health/fetch.py --queue <queue_id>   # one queue only
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))
from trustpager_api import (  # noqa: E402
    BOSError, api_get, emit_error_and_exit, emit_json, force_utf8_stdout,
    log, now_utc, paginate, parallel_get, parse_iso, days_since, resolve_path,
)

SKILL = "nurture-health"

# Candidate catalog resource ids for the auto-queue resource, newest naming
# first. resolve_path raises if an id is unknown, so we try in order.
QUEUE_RESOURCE_CANDIDATES = ["event-queues", "auto-queues", "auto_queues", "event_queues"]
ENROLMENTS_PER_QUEUE_MAX_PAGES = 5      # cap so a huge queue can't run away
EMAIL_LOG_SAMPLE_LIMIT = 500            # recent email logs to sample for engagement
STALLED_GRACE_DAYS = 5                  # active + idle past next-step delay + this = stalled


def _resolve_any(candidates: list[str], **kw: Any) -> str:
    """Return the first resource id in `candidates` that resolves, else raise."""
    last: Exception | None = None
    for rid in candidates:
        try:
            return resolve_path(rid, **kw)
        except BOSError as e:
            last = e
    raise BOSError(f"None of {candidates} resolve in the API catalog. Last: {last}")


def _steps_of(queue: dict[str, Any]) -> list[dict[str, Any]]:
    """Pull the ordered step list off a queue detail record, whatever it's called."""
    steps = (queue.get("automation_event_queue_steps")
             or queue.get("steps")
             or queue.get("event_queue_steps") or [])
    return sorted(steps, key=lambda s: s.get("step_order") or 0)


def _day_label(step: dict[str, Any]) -> str:
    desc = (step.get("description") or "").strip()
    if desc:
        return desc.split("—")[0].strip() if "—" in desc else desc[:40]
    d, h, m = step.get("delay_days") or 0, step.get("delay_hours") or 0, step.get("delay_minutes") or 0
    if d == h == m == 0:
        return "immediate"
    return f"+{d}d {h}h {m}m".replace(" 0h", "").replace(" 0m", "")


def _enrolment_status(e: dict[str, Any]) -> str:
    return (e.get("status") or e.get("state") or "active").lower()


def _enrolment_step(e: dict[str, Any]) -> int:
    """Best guess at how far an enrolment has progressed (last completed step_order)."""
    for k in ("last_completed_step_order", "current_step_order", "step_order",
              "completed_steps", "current_step"):
        v = e.get(k)
        if isinstance(v, int):
            return v
    return 0


def _fetch_queue_health(queue_list_path: str, queue: dict[str, Any], quiet: bool) -> dict[str, Any]:
    qid = queue.get("id")
    name = queue.get("name") or "(unnamed queue)"
    warnings: list[str] = []

    # --- queue detail (steps + linked automation ids) ---
    detail = queue
    try:
        get_path = _resolve_any(QUEUE_RESOURCE_CANDIDATES, action="get")
        # get_path looks like "event-queues/:id" — substitute the id segment
        concrete = get_path.replace(":id", qid).replace(":queue_id", qid)
        resp = api_get(concrete)
        detail = resp.get("data", resp) if isinstance(resp, dict) else queue
    except BOSError as e:
        warnings.append(f"queue detail degraded ({name}): {str(e).splitlines()[0]}")

    steps = _steps_of(detail)
    step_automation = {s.get("step_order"): s.get("automation_id") for s in steps}

    # --- enrolments (best-effort, capped) ---
    enrolments: list[dict[str, Any]] = []
    enrol_source = "unavailable"
    for sub in ("enrolments", "enrollments"):
        try:
            enrolments = list(paginate(f"{queue_list_path}/{qid}/{sub}",
                                       limit=100, max_pages=ENROLMENTS_PER_QUEUE_MAX_PAGES))
            enrol_source = "ok"
            break
        except BOSError:
            continue
    if enrol_source == "unavailable":
        warnings.append(f"enrolments endpoint not reachable for {name} — funnel is step-only")

    # --- funnel from enrolment statuses ---
    status_mix: dict[str, int] = {}
    for e in enrolments:
        st = _enrolment_status(e)
        status_mix[st] = status_mix.get(st, 0) + 1
    enrolled = len(enrolments)
    active = status_mix.get("active", 0)
    completed = status_mix.get("completed", 0)
    cancelled = status_mix.get("cancelled", 0) + status_mix.get("removed", 0)
    completion_rate = round(completed / enrolled, 3) if enrolled else None

    # --- per-step reached counts (how many enrolments got to / past each step) ---
    reached_by_step: dict[int, int] = {}
    for e in enrolments:
        prog = _enrolment_step(e)
        for s in steps:
            so = s.get("step_order") or 0
            if prog >= so:
                reached_by_step[so] = reached_by_step.get(so, 0) + 1

    # --- engagement per step automation, if we sampled email logs ---
    # Filled by the caller via `engagement_by_automation`; placeholder here.
    return {
        "id": qid,
        "name": name,
        "is_active": bool(detail.get("is_active", detail.get("enabled", True))),
        "step_count": len(steps),
        "steps_raw": steps,
        "step_automation": step_automation,
        "funnel": {
            "enrolled": enrolled,
            "active": active,
            "completed": completed,
            "cancelled": cancelled,
            "completion_rate": completion_rate,
            "status_mix": status_mix,
            "_source": enrol_source,
        },
        "reached_by_step": reached_by_step,
        "enrolments_raw": enrolments,
        "warnings": warnings,
        "url": f"https://app.trustpager.com/auto/queues/{qid}",
    }


def _sample_engagement(quiet: bool) -> tuple[dict[str, dict[str, int]], str]:
    """Bucket recent email logs by automation_id → {sends, opens, clicks}. Best-effort."""
    try:
        logs_path = resolve_path("email", path_contains="logs")
    except BOSError:
        try:
            logs_path = resolve_path("email-logs")
        except BOSError:
            return {}, "unavailable"
    try:
        logs = list(paginate(logs_path, limit=100, max_pages=EMAIL_LOG_SAMPLE_LIMIT // 100))
    except BOSError:
        return {}, "unavailable"

    by_auto: dict[str, dict[str, int]] = {}
    for lg in logs:
        aid = lg.get("automation_id") or lg.get("source_automation_id")
        if not aid:
            continue
        b = by_auto.setdefault(aid, {"sends": 0, "opens": 0, "clicks": 0})
        b["sends"] += 1
        if lg.get("opened_at") or lg.get("opened") or (lg.get("open_count") or 0) > 0:
            b["opens"] += 1
        if lg.get("clicked_at") or lg.get("clicked") or (lg.get("click_count") or 0) > 0:
            b["clicks"] += 1
    return by_auto, ("ok" if by_auto else "no_automation_linkage")


def _finalise_steps(q: dict[str, Any], engagement: dict[str, dict[str, int]]) -> None:
    """Attach day labels, drop-off, and engagement rates to each step in place."""
    steps_out: list[dict[str, Any]] = []
    reached = q.pop("reached_by_step", {})
    prev_reached: int | None = None
    biggest_drop = {"step_order": None, "dropped": 0, "day_label": None}
    for s in q.pop("steps_raw", []):
        so = s.get("step_order") or 0
        r = reached.get(so)
        dropped_after = None
        if prev_reached is not None and r is not None and prev_reached >= r:
            dropped_after = prev_reached - r
            if dropped_after > biggest_drop["dropped"]:
                biggest_drop = {"step_order": so, "dropped": dropped_after,
                                "day_label": _day_label(s)}
        aid = s.get("automation_id")
        eng = engagement.get(aid)
        open_rate = round(eng["opens"] / eng["sends"], 3) if eng and eng["sends"] else None
        click_rate = round(eng["clicks"] / eng["sends"], 3) if eng and eng["sends"] else None
        steps_out.append({
            "step_order": so,
            "day_label": _day_label(s),
            "automation_id": aid,
            "reached": r,
            "dropped_after": dropped_after,
            "sends": eng["sends"] if eng else None,
            "open_rate": open_rate,
            "click_rate": click_rate,
        })
        if r is not None:
            prev_reached = r
    q["steps"] = steps_out
    q["leak_step"] = biggest_drop if biggest_drop["step_order"] is not None else None
    q.pop("step_automation", None)
    q.pop("enrolments_raw", None)


def fetch(quiet: bool, only_queue: str | None) -> dict[str, Any]:
    now = now_utc()
    log(SKILL, "resolving auto-queue endpoint...", quiet=quiet)
    list_path = _resolve_any(QUEUE_RESOURCE_CANDIDATES, action="list")

    log(SKILL, "listing queues...", quiet=quiet)
    queues = list(paginate(list_path, limit=100, max_pages=5))
    if only_queue:
        queues = [q for q in queues if q.get("id") == only_queue]

    log(SKILL, f"{len(queues)} queue(s); sampling engagement...", quiet=quiet)
    engagement, eng_source = _sample_engagement(quiet)

    log(SKILL, "building per-queue health...", quiet=quiet)
    out_queues: list[dict[str, Any]] = []
    all_warnings: list[str] = []
    for q in queues:
        health = _fetch_queue_health(list_path, q, quiet)
        all_warnings.extend(health.pop("warnings", []))
        _finalise_steps(health, engagement)
        out_queues.append(health)

    # headline
    total_active = sum(q["funnel"]["active"] for q in out_queues)
    total_completed = sum(q["funnel"]["completed"] for q in out_queues)
    total_cancelled = sum(q["funnel"]["cancelled"] for q in out_queues)
    leaks = [(q["name"], q.get("leak_step")) for q in out_queues if q.get("leak_step")]
    biggest_leak = None
    if leaks:
        biggest_leak = max(leaks, key=lambda nl: nl[1]["dropped"])
        biggest_leak = {"queue": biggest_leak[0], **biggest_leak[1]}

    return {
        "generated_at": now.isoformat(),
        "headline": {
            "queues": len(out_queues),
            "total_active": total_active,
            "total_completed": total_completed,
            "total_cancelled": total_cancelled,
            "biggest_leak": biggest_leak,
        },
        "queues": out_queues,
        "warnings": all_warnings,
        "_sources": {
            "queues": "ok" if out_queues else "empty",
            "engagement": eng_source,
        },
    }


def main() -> int:
    force_utf8_stdout()
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--json-only", action="store_true", help="Suppress stderr progress logs")
    parser.add_argument("--queue", metavar="ID", help="Only audit this queue id")
    args = parser.parse_args()
    try:
        emit_json(fetch(quiet=args.json_only, only_queue=args.queue))
        return 0
    except BOSError as e:
        emit_error_and_exit(str(e), code=1)


if __name__ == "__main__":
    sys.exit(main())


# =============================================================================
# Output shape — what Claude reads from stdout
# =============================================================================
#
# {
#   "generated_at": "...",
#   "headline": {
#     "queues": 2, "total_active": 140, "total_completed": 33,
#     "total_cancelled": 12,
#     "biggest_leak": {"queue": "Reawakening", "step_order": 2,
#                      "day_label": "Day 7", "dropped": 48}
#   },
#   "queues": [
#     {
#       "id": "...", "name": "Reawakening Sequence", "is_active": true,
#       "step_count": 7,
#       "funnel": {"enrolled": 174, "active": 120, "completed": 30,
#                  "cancelled": 24, "completion_rate": 0.172,
#                  "status_mix": {...}, "_source": "ok"},
#       "steps": [
#         {"step_order": 1, "day_label": "Day 0", "automation_id": "...",
#          "reached": 174, "dropped_after": null,
#          "sends": 174, "open_rate": 0.62, "click_rate": 0.18},
#         {"step_order": 2, "day_label": "Day 7", "automation_id": "...",
#          "reached": 126, "dropped_after": 48, "sends": 126,
#          "open_rate": 0.41, "click_rate": 0.07}
#       ],
#       "leak_step": {"step_order": 2, "day_label": "Day 7", "dropped": 48},
#       "url": "https://app.trustpager.com/auto/queues/..."
#     }
#   ],
#   "warnings": ["enrolments endpoint not reachable for X — funnel is step-only"],
#   "_sources": {"queues": "ok", "engagement": "ok"}
# }
