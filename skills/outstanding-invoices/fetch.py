#!/usr/bin/env python3
"""outstanding-invoices — pre-fetch the accounts-receivable picture.

Confirms the accounting integration is connected, then queries the
Invoices / Receivables report source for the open-AR ledger
(status = AUTHORISED, amount_due > 0): an aged-bucket summary plus the
individual overdue invoices, most-overdue first.

If the integration isn't connected, returns a structured "not_connected"
state. If it's connected but the receivables ledger has never been seeded
(zero rows), returns "ledger_empty" with the integration id so the skill
can offer the one-time catch-up sync.

Auth: TRUSTPAGER_API_KEY env var or ~/.claude/bos.json.

Usage:
    python skills/outstanding-invoices/fetch.py
    python skills/outstanding-invoices/fetch.py --json-only
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))
from trustpager_api import (  # noqa: E402
    BOSError, api_get, api_post, emit_error_and_exit, emit_json,
    force_utf8_stdout, log, now_utc, resolve_path,
)

SKILL = "outstanding-invoices"

# Display order for aged buckets (the report returns them unordered).
BUCKET_ORDER = ["current", "1-30", "31-60", "61-90", "90+"]

# The open-AR filter: authorised (unpaid / part-paid) invoices with a balance.
OPEN_AR_FILTERS = [
    {"field": "status", "operator": "eq", "value": "AUTHORISED"},
    {"field": "amount_due", "operator": "gt", "value": 0},
]


def _rows(resp: Any) -> list[dict[str, Any]]:
    """Pull the rows array out of a query_report response, tolerant of wrapping."""
    if not isinstance(resp, dict):
        return []
    payload = resp.get("data", resp)
    if isinstance(payload, dict):
        return payload.get("rows") or []
    return []


def fetch(quiet: bool) -> dict[str, Any]:
    now = now_utc()
    log(SKILL, "checking the accounting integration...", quiet=quiet)

    integrations = api_get(resolve_path("integrations"), limit=50).get("data") or []
    xero = next(
        (i for i in integrations
         if (i.get("platform_type") or i.get("provider") or "").lower() == "xero"),
        None,
    )
    connected = bool(xero) and (xero.get("status") or "").lower() in {
        "active", "connected", "authorized"
    }

    if not connected:
        return {
            "generated_at": now.isoformat(),
            "connected": False,
            "status": (xero or {}).get("status") if xero else "not_installed",
            "next_step": "Connect your accounting integration at "
                         "https://app.trustpager.com/auto/integrations, then re-run.",
        }

    integration_id = xero.get("id")
    log(SKILL, "querying the receivables ledger...", quiet=quiet)

    # Aged summary: amount due + invoice count, grouped by aged bucket.
    agg = api_post("reports/query", body={
        "source": "invoices",
        "measures": [
            {"field": "amount_due", "aggregation": "sum", "alias": "total_due"},
            {"field": "id", "aggregation": "count", "alias": "invoices"},
        ],
        "dimensions": ["aged_bucket"],
        "filters": OPEN_AR_FILTERS,
        "mode": "aggregate",
    })
    agg_rows = _rows(agg)

    # Ledger empty -> needs the one-time seed. Offer it from the skill.
    if not agg_rows:
        return {
            "generated_at": now.isoformat(),
            "connected": True,
            "integration_id": integration_id,
            "ledger_empty": True,
            "next_step": "The receivables ledger has no open invoices yet. If this is "
                         "the first run, seed it once via sync_receivables on integration "
                         f"{integration_id} (POST /integrations/{integration_id}/sync-receivables).",
        }

    # Normalise the aged summary into a fixed bucket order + grand totals.
    by_bucket = {r.get("aged_bucket"): r for r in agg_rows}
    buckets = []
    total_due = 0.0
    total_count = 0
    for name in BUCKET_ORDER:
        row = by_bucket.get(name) or {}
        due = float(row.get("total_due") or 0)
        cnt = int(row.get("invoices") or 0)
        buckets.append({"bucket": name, "amount_due": round(due, 2), "invoices": cnt})
        total_due += due
        total_count += cnt

    log(SKILL, "pulling the open invoices...", quiet=quiet)

    # Drilldown: the actual open invoices, most-overdue first (source default order).
    drill = api_post("reports/query", body={
        "source": "invoices",
        "mode": "drilldown",
        "measures": [{"field": "id", "aggregation": "count"}],
        "filters": OPEN_AR_FILTERS,
        "limit": 25,
    })
    open_invoices = [
        {
            "invoice_number": r.get("invoice_number"),
            "customer": r.get("customer_name"),
            "due_date": r.get("due_date"),
            "amount_due": r.get("amount_due"),
            "days_overdue": r.get("days_overdue"),
            "aged_bucket": r.get("aged_bucket"),
            "currency": r.get("currency_code"),
        }
        for r in _rows(drill)
    ]

    return {
        "generated_at": now.isoformat(),
        "connected": True,
        "integration_id": integration_id,
        "ledger_empty": False,
        "summary": {
            "total_due": round(total_due, 2),
            "total_open_invoices": total_count,
            "by_bucket": buckets,
        },
        "open_invoices": open_invoices,
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


# =============================================================================
# Output shape — what Claude reads from stdout
# =============================================================================
#
# Not connected:
#   {"connected": false, "status": "not_installed", "next_step": "..."}
#
# Connected but never seeded:
#   {"connected": true, "integration_id": "...", "ledger_empty": true, "next_step": "..."}
#
# Connected with data:
#   {
#     "connected": true, "integration_id": "...", "ledger_empty": false,
#     "summary": {
#       "total_due": 8999.10, "total_open_invoices": 7,
#       "by_bucket": [
#         {"bucket": "current", "amount_due": 8023.40, "invoices": 5},
#         {"bucket": "1-30",  "amount_due": 425.70, "invoices": 1},
#         {"bucket": "31-60", "amount_due": 0,      "invoices": 0},
#         {"bucket": "61-90", "amount_due": 0,      "invoices": 0},
#         {"bucket": "90+",   "amount_due": 550.00, "invoices": 1}
#       ]
#     },
#     "open_invoices": [
#       {"invoice_number": "INV-0053", "customer": "...", "due_date": "2026-02-24",
#        "amount_due": 550, "days_overdue": 97, "aged_bucket": "90+", "currency": "AUD"}
#     ]
#   }
