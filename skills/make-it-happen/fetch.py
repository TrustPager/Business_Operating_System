#!/usr/bin/env python3
"""make-it-happen — pre-fetch the TrustPager discovery surface.

This is a "warm cache" fetch: pulls the AI-facing reference data Claude
will need to figure out which TrustPager primitives to use for any
plain-English request. Calling it once at the start of /make-it-happen
saves 3-5 sequential MCP discovery calls.

Pulls (in parallel):
- AI instructions for this workspace (workflow guidance + common mistakes)
- All available trigger schemas (for automation work)
- All available action types (for automation work)
- All available automations (so we can spot "you already have one of these")

Auth: TRUSTPAGER_API_KEY env var or ~/.claude/bos.json.

Usage:
    python skills/make-it-happen/fetch.py
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))
from trustpager_api import (  # noqa: E402
    BOSError, api_get, emit_error_and_exit, emit_json,
    force_utf8_stdout, log, now_utc, parallel_get, resolve_path,
)


SKILL = "make-it-happen"


def fetch(quiet: bool) -> dict:
    now = now_utc()
    log(SKILL, "warming discovery cache...", quiet=quiet)

    # Map each call to its resolved path. Some endpoints don't fit the
    # generic resolve_path action-shape, so we use raw paths there.
    calls = [
        ("ai-instructions", {}),
        ("schemas/triggers", {}),
        ("automations/action-types", {}),
        (resolve_path("automations"), {"limit": 100}),
    ]
    results = parallel_get(calls)

    ai_instructions = results.get("ai-instructions", {})
    triggers = results.get("schemas/triggers", {})
    action_types = results.get("automations/action-types", {})
    automations = results.get(resolve_path("automations"), {})

    return {
        "generated_at": now.isoformat(),
        "ai_instructions": ai_instructions,
        "trigger_schemas": triggers.get("data") or triggers,
        "action_types": action_types.get("data") or action_types,
        "existing_automations": [
            {"id": a.get("id"), "name": a.get("name"), "enabled": a.get("enabled")}
            for a in (automations.get("data") or [])
        ],
        "headline": {
            "trigger_count": len(triggers.get("data") or triggers or []) if isinstance(triggers, (list, dict)) else 0,
            "action_type_count": len(action_types.get("data") or action_types or []) if isinstance(action_types, (list, dict)) else 0,
            "automation_count": len(automations.get("data") or []),
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
