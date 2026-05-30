#!/usr/bin/env python3
"""sync-from-xero — pre-fetch Xero connection state + TrustPager opps.

Before /sync-from-xero starts the reconciliation conversation, this
script confirms the Xero integration is connected, pulls the recent
Xero state (if available via TrustPager's integration query layer),
and pulls TrustPager opportunities for cross-referencing.

If Xero isn't connected, returns a structured "not_connected" state so
the skill can prompt the user to connect first.

Auth: TRUSTPAGER_API_KEY env var or ~/.claude/bos.json.

Usage:
    python skills/sync-from-xero/fetch.py
    python skills/sync-from-xero/fetch.py --days 60
"""

from __future__ import annotations

import argparse
import sys
from datetime import timedelta
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))
from trustpager_api import (  # noqa: E402
    BOSError, api_get, emit_error_and_exit, emit_json, force_utf8_stdout,
    log, now_utc, resolve_path,
)


SKILL = "sync-from-xero"


def fetch(days: int, quiet: bool) -> dict[str, Any]:
    now = now_utc()
    cutoff = (now - timedelta(days=days)).isoformat()
    log(SKILL, "checking integrations...", quiet=quiet)

    integrations_path = resolve_path("integrations")
    integrations_resp = api_get(integrations_path, limit=50)
    integrations = integrations_resp.get("data") or []

    xero = next(
        (i for i in integrations
         if (i.get("platform_type") or i.get("provider") or "").lower() == "xero"),
        None,
    )

    if not xero or (xero.get("status") or "").lower() not in {"active", "connected", "authorized"}:
        return {
            "generated_at": now.isoformat(),
            "connected": False,
            "status": (xero or {}).get("status") if xero else "not_installed",
            "headline": {
                "xero_connected": False,
                "next_step": "Install or reconnect Xero at /settings/integrations.",
            },
            "trustpager_opportunities": [],
        }

    log(SKILL, "Xero connected, pulling recent state...", quiet=quiet)

    # Pull recent TrustPager opportunities for matching (won + open in last N days)
    opps_resp = api_get(resolve_path("opportunities"), limit=200, after=cutoff)
    opps = opps_resp.get("data") or []

    # Try to query Xero data through the integration. The exact shape depends
    # on the platform; skill should call query_integration via MCP for the
    # detailed reconciliation. Here we just confirm the connection.
    xero_state: dict[str, Any] = {
        "id": xero.get("id"),
        "label": xero.get("label") or xero.get("name") or "Xero",
        "status": xero.get("status"),
        "connected_at": xero.get("connected_at") or xero.get("created_at"),
    }

    return {
        "generated_at": now.isoformat(),
        "window_days": days,
        "connected": True,
        "xero": xero_state,
        "trustpager_opportunities": [
            {
                "id": o.get("id"),
                "name": o.get("name"),
                "value": o.get("value"),
                "status": o.get("status"),
                "stage": ((o.get("placements") or [{}])[0]
                          .get("crm_pipeline_stages", {}) or {}).get("name"),
                "payment_status": o.get("payment_status"),
                "contact_id": o.get("contact_id"),
                "actual_close_date": o.get("actual_close_date"),
            }
            for o in opps
        ],
        "headline": {
            "xero_connected": True,
            "opportunities_in_window": len(opps),
        },
    }


def main() -> int:
    force_utf8_stdout()
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--days", type=int, default=90,
                        help="Days back to consider (default 90)")
    parser.add_argument("--json-only", action="store_true",
                        help="Suppress stderr progress logs")
    args = parser.parse_args()

    try:
        emit_json(fetch(args.days, quiet=args.json_only))
        return 0
    except BOSError as e:
        emit_error_and_exit(str(e), code=1)


if __name__ == "__main__":
    sys.exit(main())
