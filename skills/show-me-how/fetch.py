#!/usr/bin/env python3
"""show-me-how — pre-fetch help-center search results + workspace context.

The help-center search itself is a TrustPager MCP tool (search_help_center)
that doesn't have a public REST equivalent. So the SKILL.md still calls
that via MCP. What this script CAN do up front:

- Fetch the workspace's own Playbooks for the
  topic — "here's also what's in your own training materials."
- Fetch AI instructions, which sometimes contain workflow guidance
  that supersedes the generic help-center answer.

Output is a thin context bundle the skill merges with the live MCP
search_help_center result.

Auth: TRUSTPAGER_API_KEY env var or ~/.claude/bos.json.

Usage:
    python skills/show-me-how/fetch.py --query "add a new lead source"
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))
from trustpager_api import (  # noqa: E402
    BOSError, emit_error_and_exit, emit_json, force_utf8_stdout,
    log, now_utc, parallel_get,
)


SKILL = "show-me-how"


def fetch(query: str, quiet: bool) -> dict[str, Any]:
    now = now_utc()
    log(SKILL, f"pre-fetching context for '{query}'...", quiet=quiet)

    calls = [
        ("ai-instructions", {}),
        ("playbooks", {"limit": 20, "search": query}),
    ]
    results = parallel_get(calls)
    ai_instructions = results.get("ai-instructions", {})
    canvases_resp = results.get("playbooks", {})
    canvases = canvases_resp.get("data") or []

    return {
        "generated_at": now.isoformat(),
        "query": query,
        "ai_instructions": ai_instructions,
        "workspace_playbooks": [
            {
                "id": c.get("id"),
                "name": c.get("name"),
                "description": c.get("description"),
                "url": f"https://app.trustpager.com/training/playbooks?playbook={c.get('id')}",
                "card_count": c.get("card_count"),
            }
            for c in canvases
        ],
        "headline": {
            "playbooks_matched": len(canvases),
            "ai_instructions_available": bool(ai_instructions),
            "next_step": "Call mcp__trustpager__search_help_center for the canonical articles.",
        },
    }


def main() -> int:
    force_utf8_stdout()
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--query", required=True, help="The how-to question")
    parser.add_argument("--json-only", action="store_true",
                        help="Suppress stderr progress logs")
    args = parser.parse_args()

    try:
        emit_json(fetch(args.query, quiet=args.json_only))
        return 0
    except BOSError as e:
        emit_error_and_exit(str(e), code=1)


if __name__ == "__main__":
    sys.exit(main())
