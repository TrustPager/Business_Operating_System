#!/usr/bin/env python3
"""Audit your TrustPager sales pipeline — stage health, stale deals, drop-offs.

When to use:
- Weekly review of pipeline health.
- "Where am I losing deals?"
- "Which stage has the most stuck money?"
- Before a forecasting conversation with a partner / advisor.

What it reports (one section per insight):
- 💰 Pipeline value by stage — count + total $ at each stage of each pipeline.
- 🐢 Stuck deals — opportunities that haven't moved stage in 14+ days,
  ranked by value × days stuck.
- 🚪 Conversion drop-offs — stage-to-stage where the most volume is being lost
  (count of opps that went to a "lost" stage from each upstream stage).
- 📊 Headline — total open value, top stage, avg days in pipeline.

All read-only. Doesn't change anything in your workspace.

Usage:
    python tools/audit-pipeline.py
    python tools/audit-pipeline.py --stuck-days 21      # different stale threshold
    python tools/audit-pipeline.py --json               # machine-readable output
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trustpager_api import (  # noqa: E402
    BOSError, api_get, days_since, emit_error_and_exit, emit_json,
    force_utf8_stdout, now_utc, paginate, parse_iso, resolve_path,
)


SKILL = "audit-pipeline"


def _stage_of(opp: dict[str, Any]) -> dict[str, Any] | None:
    placements = opp.get("placements") or []
    if not placements:
        return None
    return placements[0].get("crm_pipeline_stages") or None


def _is_open(opp: dict[str, Any]) -> bool:
    if (opp.get("status") or "").lower() in {"won", "lost", "cancelled", "abandoned", "archived"}:
        return False
    s = _stage_of(opp) or {}
    return not (s.get("is_won_stage") or s.get("is_lost_stage"))


def audit(stuck_days: int, json_only: bool) -> dict[str, Any]:
    now = now_utc()
    opps_path = resolve_path("opportunities")

    # Pull up to 500 — good enough for most workspaces. --full could be added if needed.
    response = api_get(opps_path, limit=200)
    opportunities = response.get("data", [])

    if not json_only:
        print(f"# Pipeline audit", file=sys.stderr)
        print(f"# Total opportunities sampled: {len(opportunities)}", file=sys.stderr)

    # By stage
    by_stage: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"count": 0, "value": 0.0, "stuck": 0, "stage_id": None})
    stuck: list[dict[str, Any]] = []
    lost_from_upstream: dict[str, int] = defaultdict(int)
    total_open_value = 0.0
    open_days_total = 0.0
    open_days_count = 0

    for opp in opportunities:
        stage = _stage_of(opp) or {}
        stage_name = stage.get("name") or "(unstaged)"

        if _is_open(opp):
            v = float(opp.get("value") or 0)
            total_open_value += v
            by_stage[stage_name]["count"] += 1
            by_stage[stage_name]["value"] += v
            by_stage[stage_name]["stage_id"] = stage.get("id")

            # Stuck = stage hasn't moved in stuck_days
            stage_changed = parse_iso(opp.get("stage_changed_at") or opp.get("updated_at"))
            if stage_changed:
                ds = days_since(stage_changed, ref=now) or 0
                if ds >= stuck_days:
                    by_stage[stage_name]["stuck"] += 1
                    stuck.append({
                        "id": opp.get("id"),
                        "name": opp.get("name"),
                        "stage": stage_name,
                        "value": v,
                        "days_stuck": ds,
                        "score": (max(100.0, v / 1000.0)) * (1 + ds / 30.0),
                    })

            created = parse_iso(opp.get("created_at"))
            if created:
                open_days_total += days_since(created, ref=now) or 0
                open_days_count += 1
        elif stage.get("is_lost_stage"):
            # Track where lost deals came from
            prev = (opp.get("previous_stage") or {}).get("name")
            if prev:
                lost_from_upstream[prev] += 1

    stuck.sort(key=lambda x: x["score"], reverse=True)
    avg_days_open = (open_days_total / open_days_count) if open_days_count else 0

    by_stage_sorted = sorted(
        ((name, v) for name, v in by_stage.items()),
        key=lambda kv: kv[1]["value"], reverse=True,
    )
    top_stage = by_stage_sorted[0][0] if by_stage_sorted else "(none)"

    return {
        "generated_at": now.isoformat(),
        "stuck_threshold_days": stuck_days,
        "headline": {
            "total_open_value": round(total_open_value, 2),
            "open_opportunities": sum(v["count"] for v in by_stage.values()),
            "top_stage_by_value": top_stage,
            "avg_days_open": round(avg_days_open, 1),
        },
        "by_stage": [
            {"stage": name, **v}
            for name, v in by_stage_sorted
        ],
        "stuck_top_20": stuck[:20],
        "lost_from_upstream": dict(lost_from_upstream),
    }


def _print_human(report: dict[str, Any]) -> None:
    h = report["headline"]
    print("## Pipeline audit")
    print()
    print(f"- Open opportunities: **{h['open_opportunities']}** worth "
          f"**${h['total_open_value']:,.0f}**")
    print(f"- Top stage by value: **{h['top_stage_by_value']}**")
    print(f"- Average days in pipeline: **{h['avg_days_open']}** days")
    print()
    print("### 💰 By stage")
    print()
    print("| Stage | Count | Value | Stuck (>" + str(report["stuck_threshold_days"]) + "d) |")
    print("|---|---:|---:|---:|")
    for s in report["by_stage"]:
        print(f"| {s['stage']} | {s['count']} | ${s['value']:,.0f} | {s['stuck']} |")
    print()
    print(f"### 🐢 Top stuck deals (no stage change in {report['stuck_threshold_days']}+ days)")
    print()
    if not report["stuck_top_20"]:
        print("_None — every open deal has moved recently. 🎉_")
    else:
        print("| Deal | Stage | Days stuck | Value |")
        print("|---|---|---:|---:|")
        for d in report["stuck_top_20"][:10]:
            v = f"${d['value']:,.0f}" if d['value'] else "(unpriced)"
            print(f"| {d['name'][:40]} | {d['stage']} | {d['days_stuck']} | {v} |")
    print()
    print("### 🚪 Where deals are lost from")
    print()
    if not report["lost_from_upstream"]:
        print("_No lost deals in the sample window._")
    else:
        items = sorted(report["lost_from_upstream"].items(), key=lambda x: -x[1])
        for stage, n in items:
            print(f"- **{stage}** → lost: {n}")


def main() -> int:
    force_utf8_stdout()
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--stuck-days", type=int, default=14,
                        help="Days without a stage change to flag as stuck (default 14)")
    parser.add_argument("--json", action="store_true",
                        help="Output JSON instead of human-readable markdown")
    args = parser.parse_args()

    try:
        report = audit(args.stuck_days, json_only=args.json)
        if args.json:
            emit_json(report)
        else:
            _print_human(report)
        return 0
    except BOSError as e:
        emit_error_and_exit(str(e), code=1)


if __name__ == "__main__":
    sys.exit(main())
