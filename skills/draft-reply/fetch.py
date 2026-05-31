#!/usr/bin/env python3
"""draft-reply — find inbound messages awaiting a reply, ranked.

Pulls every inbound email thread + SMS conversation in the last N hours
where we haven't replied yet, ranked by:
- Recency (newer first)
- Whether the sender has an open opportunity with us
- Sender's contact value / "VIP" flag if your workspace uses one

Output (stdout): JSON document with all items, prioritised. The skill
chooses one to draft a reply to, OR shows the list and asks the user.

Auth: TRUSTPAGER_API_KEY env var or ~/.claude/bos.json.

Usage:
    python skills/draft-reply/fetch.py
    python skills/draft-reply/fetch.py --hours 24
    python skills/draft-reply/fetch.py --channel email     # or sms or all
"""

from __future__ import annotations

import argparse
import sys
from datetime import timedelta
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))
from trustpager_api import (  # noqa: E402
    BOSError, emit_error_and_exit, emit_json, force_utf8_stdout,
    log, now_utc, parallel_get, parse_iso, resolve_path,
)


SKILL = "draft-reply"


def fetch(hours: int, channel: str, quiet: bool) -> dict[str, Any]:
    now = now_utc()
    cutoff = (now - timedelta(hours=hours)).isoformat()
    log(SKILL, f"finding unanswered inbound in last {hours}h...", quiet=quiet)

    calls = []
    if channel in ("email", "all"):
        calls.append((resolve_path("email", path_contains="threads"),
                     {"limit": 50, "direction": "inbound", "we_replied": "false",
                      "after": cutoff,
                      "sort": "last_message_at", "order": "desc"}))
    if channel in ("sms", "all"):
        calls.append((resolve_path("sms", path_contains="conversations"),
                     {"limit": 50, "after": cutoff,
                      "sort": "last_message_at", "order": "desc"}))

    results = parallel_get(calls) if calls else {}

    items: list[dict[str, Any]] = []

    if channel in ("email", "all"):
        threads = results.get(resolve_path("email", path_contains="threads"), {}).get("data", [])
        for t in threads:
            if t.get("we_replied"):
                continue  # belt + braces vs the query filter
            items.append({
                "channel": "email",
                "thread_id": t.get("id"),
                "subject": t.get("subject"),
                "from_name": (t.get("contact") or {}).get("first_name", "") + " "
                              + (t.get("contact") or {}).get("last_name", ""),
                "from_email": (t.get("contact") or {}).get("email") or t.get("from_email"),
                "received_at": t.get("last_message_at") or t.get("last_inbound_at"),
                "has_open_opportunity": bool(t.get("deal_id") or t.get("opportunity_id")),
                "opportunity_id": t.get("deal_id") or t.get("opportunity_id"),
                "contact_id": (t.get("contact") or {}).get("id"),
                "snippet": (t.get("latest_message") or {}).get("plain_text", "")[:200],
            })

    if channel in ("sms", "all"):
        convos = results.get(resolve_path("sms", path_contains="conversations"), {}).get("data", [])
        for c in convos:
            if c.get("we_replied") or (c.get("outbound_count") or 0) > 0:
                # Determine if there's an inbound newer than the latest outbound
                last_inbound = parse_iso(c.get("last_inbound_at"))
                last_outbound = parse_iso(c.get("last_outbound_at"))
                if last_outbound and last_inbound and last_outbound >= last_inbound:
                    continue
            items.append({
                "channel": "sms",
                "conversation_id": c.get("id"),
                "from_name": (c.get("contact") or {}).get("first_name", "") + " "
                              + (c.get("contact") or {}).get("last_name", ""),
                "from_phone": (c.get("contact") or {}).get("phone") or c.get("from_phone"),
                "received_at": c.get("last_inbound_at"),
                "has_open_opportunity": bool(c.get("deal_id")),
                "opportunity_id": c.get("deal_id"),
                "contact_id": (c.get("contact") or {}).get("id"),
                "snippet": (c.get("last_inbound_body") or "")[:200],
            })

    # Rank: open opp first, then by recency
    items.sort(key=lambda x: (
        0 if x.get("has_open_opportunity") else 1,
        -(parse_iso(x.get("received_at")).timestamp() if parse_iso(x.get("received_at")) else 0),
    ))

    return {
        "generated_at": now.isoformat(),
        "window_hours": hours,
        "channel": channel,
        "headline": {
            "total_unanswered": len(items),
            "with_open_opportunity": sum(1 for i in items if i.get("has_open_opportunity")),
            "email_count": sum(1 for i in items if i["channel"] == "email"),
            "sms_count": sum(1 for i in items if i["channel"] == "sms"),
        },
        "items": items,
    }


def main() -> int:
    force_utf8_stdout()
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--hours", type=int, default=48,
                        help="How far back to look (default 48 hours)")
    parser.add_argument("--channel", choices=["email", "sms", "all"], default="all",
                        help="Which channel(s) to include (default: all)")
    parser.add_argument("--json-only", action="store_true",
                        help="Suppress stderr progress logs")
    args = parser.parse_args()

    try:
        emit_json(fetch(args.hours, args.channel, quiet=args.json_only))
        return 0
    except BOSError as e:
        emit_error_and_exit(str(e), code=1)


if __name__ == "__main__":
    sys.exit(main())
