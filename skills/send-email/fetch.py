#!/usr/bin/env python3
"""send-email — gather all context needed to draft a personalised email.

Given a contact (and optionally an opportunity) we want to send to, pull:
- The contact's full record
- The opportunity (if linked)
- Recent email threads with this contact (so we don't start a new thread
  when we should reply to one)
- The last few sent emails by ANY user in the workspace (for tone
  calibration — Claude reads them before drafting)
- Email capabilities + active email config (which sender + signature)

One bulk call instead of 5 sequential ones.

Auth: TRUSTPAGER_API_KEY env var or ~/.claude/bos.json.

Usage:
    python skills/send-email/fetch.py --contact-id <id>
    python skills/send-email/fetch.py --contact-id <id> --opportunity-id <id>
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))
from trustpager_api import (  # noqa: E402
    BOSError, api_get, emit_error_and_exit, emit_json, force_utf8_stdout,
    log, now_utc, parallel_get, resolve_path,
)


SKILL = "send-email"


def fetch(contact_id: str, opportunity_id: str | None, quiet: bool) -> dict[str, Any]:
    now = now_utc()
    log(SKILL, f"gathering send context for contact {contact_id}...", quiet=quiet)

    # Resolve listable endpoints via the catalog (resolves correctly across
    # any future API rename). The :id-templated ones are interpolated raw.
    threads_path = resolve_path("email", path_contains="threads")
    configs_path = resolve_path("email", path_contains="configs")

    calls = [
        (f"contacts/{contact_id}", {}),
        (threads_path, {"contact_id": contact_id, "limit": 5}),
        ("email/capabilities", {}),
        (configs_path, {}),
    ]
    if opportunity_id:
        calls.append((f"opportunities/{opportunity_id}", {}))

    results = parallel_get(calls)

    contact = results.get(f"contacts/{contact_id}", {})
    threads_with_contact = (results.get(threads_path, {}).get("data") or [])
    capabilities = results.get("email/capabilities", {})
    configs = results.get(configs_path, {}).get("data") or []
    opportunity = results.get(f"opportunities/{opportunity_id}", {}) if opportunity_id else None

    # Second call for "recent sent across workspace" — different params, same path
    recent_sent_resp = api_get(threads_path, limit=5, direction="outbound",
                               sort="last_message_at", order="desc")
    recent_sent = recent_sent_resp.get("data") or []

    active_config = next((c for c in configs if c.get("is_default")), None) or (configs[0] if configs else None)

    return {
        "generated_at": now.isoformat(),
        "contact": contact.get("data") if isinstance(contact, dict) and "data" in contact else contact,
        "opportunity": opportunity.get("data") if opportunity and isinstance(opportunity, dict) and "data" in opportunity else opportunity,
        "recent_threads_with_contact": [
            {
                "id": t.get("id"),
                "subject": t.get("subject"),
                "last_message_at": t.get("last_message_at"),
                "message_count": t.get("message_count"),
                "we_replied": t.get("we_replied"),
            }
            for t in threads_with_contact
        ],
        "recent_sent_by_workspace": [
            {
                "id": t.get("id"),
                "subject": t.get("subject"),
                "last_message_at": t.get("last_message_at"),
                "to": t.get("contact_email") or t.get("to_email"),
            }
            for t in recent_sent
        ],
        "email_capabilities": capabilities,
        "active_email_config": active_config,
        "headline": {
            "existing_thread_with_contact": len(threads_with_contact) > 0,
            "recent_sent_sampled": len(recent_sent),
            "has_email_config": active_config is not None,
        },
    }


def main() -> int:
    force_utf8_stdout()
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--contact-id", required=True, help="Contact UUID to gather context for")
    parser.add_argument("--opportunity-id", default=None, help="Optional opportunity UUID")
    parser.add_argument("--json-only", action="store_true",
                        help="Suppress stderr progress logs")
    args = parser.parse_args()

    try:
        emit_json(fetch(args.contact_id, args.opportunity_id, quiet=args.json_only))
        return 0
    except BOSError as e:
        emit_error_and_exit(str(e), code=1)


if __name__ == "__main__":
    sys.exit(main())
