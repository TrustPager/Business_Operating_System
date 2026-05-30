#!/usr/bin/env python3
"""automate-this — pre-fetch trigger schemas + action types + existing automations.

So Claude doesn't have to discover the automation surface step-by-step
during the design conversation. Everything Claude needs to design an
automation is in one JSON blob.

Pulls (in parallel):
- All trigger schemas (every WHEN event TrustPager can react to)
- All action types (every DO operation an automation can perform)
- Existing automations (so we can flag overlap with "you already have
  an automation for that" before creating a duplicate)

Auth: TRUSTPAGER_API_KEY env var or ~/.claude/bos.json.

Usage:
    python skills/automate-this/fetch.py
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))
from trustpager_api import (  # noqa: E402
    BOSError, emit_error_and_exit, emit_json, force_utf8_stdout,
    log, now_utc, parallel_get, resolve_path,
)


SKILL = "automate-this"


def fetch(quiet: bool) -> dict:
    now = now_utc()
    log(SKILL, "fetching automation surface...", quiet=quiet)

    calls = [
        ("schemas/triggers", {}),
        ("automations/action-types", {}),
        (resolve_path("automations"), {"limit": 100}),
    ]
    results = parallel_get(calls)

    triggers = results.get("schemas/triggers", {})
    action_types = results.get("automations/action-types", {})
    automations = results.get(resolve_path("automations"), {})

    triggers_list = triggers.get("data") or triggers if isinstance(triggers, (dict, list)) else []
    if isinstance(triggers_list, dict):
        triggers_list = triggers_list.get("triggers") or []
    actions_list = action_types.get("data") or action_types if isinstance(action_types, (dict, list)) else []
    if isinstance(actions_list, dict):
        actions_list = actions_list.get("action_types") or []

    return {
        "generated_at": now.isoformat(),
        "available_triggers": triggers_list,
        "available_action_types": actions_list,
        "existing_automations": [
            {
                "id": a.get("id"),
                "name": a.get("name"),
                "enabled": a.get("enabled"),
                "trigger_count": len(a.get("triggers") or []),
                "action_count": len(a.get("actions") or []),
            }
            for a in (automations.get("data") or [])
        ],
        "headline": {
            "triggers_available": len(triggers_list) if isinstance(triggers_list, list) else 0,
            "action_types_available": len(actions_list) if isinstance(actions_list, list) else 0,
            "automations_in_workspace": len(automations.get("data") or []),
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
