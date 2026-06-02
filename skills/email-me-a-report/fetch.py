#!/usr/bin/env python3
"""email-me-a-report — pre-fetch what's reportable and what already exists.

Lists the operator's existing report dashboards (candidates to schedule),
the available report sources (raw material for a new dashboard), and any
auto schedules already running (so we don't duplicate one).

Auth: TRUSTPAGER_API_KEY env var or ~/.claude/bos.json.

Usage:
    python skills/email-me-a-report/fetch.py
    python skills/email-me-a-report/fetch.py --json-only
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))
from trustpager_api import (  # noqa: E402
    BOSError, api_get, emit_error_and_exit, emit_json,
    force_utf8_stdout, log, now_utc, resolve_path,
)

SKILL = "email-me-a-report"


def _resolve_or(resource: str, fallback: str, **kw: Any) -> str:
    """Resolve a path from the public catalog (so it survives endpoint renames),
    falling back to a known literal if the catalog can't be reached/matched."""
    try:
        return resolve_path(resource, **kw)
    except BOSError:
        return fallback


def _safe_list(path: str, quiet: bool, **params: Any) -> list[dict[str, Any]]:
    """GET a list endpoint, returning [] (and logging) on failure rather than bailing."""
    try:
        return api_get(path, **params).get("data") or []
    except BOSError as e:
        log(SKILL, f"  ! {path}: {str(e).splitlines()[0]}", quiet=quiet)
        return []


def fetch(quiet: bool) -> dict[str, Any]:
    now = now_utc()
    log(SKILL, "listing dashboards, sources, and schedules...", quiet=quiet)

    # All three live under the catalog. Dashboards + sources are sub-resources
    # of "reports"; schedules are their own "auto-schedules" resource.
    dashboards = _safe_list(
        _resolve_or("reports", "report-dashboards", path_contains="report-dashboards"),
        quiet, limit=100)
    sources = _safe_list(
        _resolve_or("reports", "reports/sources", path_contains="sources"), quiet)
    schedules = _safe_list(
        _resolve_or("auto-schedules", "auto-schedules"), quiet, limit=100)

    return {
        "generated_at": now.isoformat(),
        "dashboards": [
            {"id": d.get("id"), "name": d.get("name"),
             "description": d.get("description")}
            for d in dashboards
        ],
        "sources": [
            {"name": s.get("name"), "label": s.get("label"),
             "description": s.get("description")}
            for s in sources
        ],
        "existing_schedules": [
            {"id": s.get("id"), "name": s.get("name"),
             "cron": s.get("cron") or s.get("schedule"),
             "enabled": s.get("enabled", s.get("is_active"))}
            for s in schedules
        ],
        "headline": {
            "dashboard_count": len(dashboards),
            "source_count": len(sources),
            "schedule_count": len(schedules),
        },
    }


def main() -> int:
    force_utf8_stdout()
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--json-only", action="store_true",
                        help="Suppress stderr progress logs")
    args = parser.parse_args()
    try:
        emit_json(fetch(quiet=args.json_only))
        return 0
    except BOSError as e:
        emit_error_and_exit(str(e), code=1)


if __name__ == "__main__":
    sys.exit(main())


# Output shape:
# {
#   "dashboards": [{"id": "...", "name": "Sales Overview", "description": "..."}],
#   "sources":    [{"name": "opportunities", "label": "Opportunities", "description": "..."},
#                  {"name": "tasks", ...}, {"name": "invoices", ...}],
#   "existing_schedules": [{"id": "...", "name": "...", "cron": "0 7 * * 1-5", "enabled": true}],
#   "headline": {"dashboard_count": 3, "source_count": 3, "schedule_count": 1}
# }
