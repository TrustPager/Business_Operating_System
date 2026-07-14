#!/usr/bin/env python3
"""Answer "can TrustPager do X?" in plain English, and hand back the command.

When to use:
- "Can TrustPager send an SMS / take a payment / book a meeting / merge contacts?"
- You know the goal, not the endpoint. This searches the whole API catalog and
  returns the matching endpoints plus the exact `api.py` command to run each.
- Before writing a skill: find the endpoint you need without scanning 60+
  resources by hand.

Why this exists:
- list-endpoints browses; this SEARCHES. You describe the goal, it ranks every
  endpoint in the public catalog (docs.trustpager.com/api-index.json) by how
  well it matches, and prints the top hits with a ready-to-run command. That
  turns "which of 700 tools do I need" into "ask, get the one command."

What it prints (per hit):
- [R]/[W] read or write, the METHOD and path, the resource, a one-line
  description, and the copy-paste `python tools/api.py ...` command.

All read-only (it only reads the public catalog; it makes no API call).

Usage:
    python tools/find-capability.py "send an sms"
    python tools/find-capability.py "recurring invoice" --limit 8
    python tools/find-capability.py "book a meeting" --json
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trustpager_api import (  # noqa: E402
    BOSError,
    emit_error_and_exit,
    emit_json,
    force_utf8_stdout,
    get_catalog,
)

_WORD = re.compile(r"[a-z0-9]+")


def _tokens(text: str) -> list[str]:
    return _WORD.findall((text or "").lower())


def _score(query_terms: list[str], resource: dict[str, Any], ep: dict[str, Any]) -> int:
    """Rank an endpoint against the query. Path/label hits weigh more than blurb hits."""
    strong = set(_tokens(resource.get("id", ""))) \
        | set(_tokens(resource.get("label", ""))) \
        | set(_tokens(ep.get("path", "")))
    weak = set(_tokens(resource.get("description", ""))) \
        | set(_tokens(ep.get("description", "")))
    score = 0
    for term in query_terms:
        if term in strong:
            score += 3
        elif any(term in tok or tok in term for tok in strong):
            score += 2
        elif term in weak:
            score += 1
    return score


def _command_for(method: str, resource_id: str, ep: dict[str, Any]) -> str:
    """Build the copy-paste api.py command for one endpoint."""
    path = ep.get("path", "").lstrip("/")
    is_write = ep.get("is_write", False)
    is_search = path.endswith("/search")
    has_params = ":" in path
    root = path == resource_id

    if root and method == "GET":
        cmd = f"python tools/api.py GET {resource_id}"
    elif is_search:
        cmd = f'python tools/api.py {method} {resource_id} --action search --body \'{{"query":"..."}}\''
    elif root and method == "POST":
        cmd = f"python tools/api.py POST {resource_id} --body '{{...}}'"
    elif has_params:
        # Nested / :id paths go through the raw-path form with placeholders.
        cmd = f"python tools/api.py {method} {path}"
        if is_write:
            cmd += " --body '{...}'"
    else:
        cmd = f"python tools/api.py {method} {path}"
        if is_write:
            cmd += " --body '{...}'"

    if is_write and "--confirm" not in cmd:
        cmd += " --confirm"
    return cmd


def find(query: str, limit: int) -> list[dict[str, Any]]:
    query_terms = _tokens(query)
    if not query_terms:
        emit_error_and_exit('Describe what you want to do, e.g. "send an sms".')

    catalog = get_catalog()
    hits: list[dict[str, Any]] = []
    for resource in catalog.get("resources", []):
        for ep in resource.get("endpoints", []):
            score = _score(query_terms, resource, ep)
            if score <= 0:
                continue
            hits.append({
                "score": score,
                "resource_id": resource.get("id"),
                "resource_label": resource.get("label"),
                "method": ep.get("method"),
                "path": ep.get("path"),
                "is_write": ep.get("is_write", False),
                "scopes": ep.get("scopes", []),
                "description": ep.get("description"),
                "command": _command_for(ep.get("method", "GET"), resource.get("id", ""), ep),
            })

    # Highest score first; break ties with reads before writes, then shorter paths.
    hits.sort(key=lambda h: (-h["score"], h["is_write"], len(h["path"] or "")))
    return hits[:limit]


def main() -> int:
    force_utf8_stdout()
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("query", help='Plain-English goal, e.g. "send an sms".')
    parser.add_argument("--limit", type=int, default=6, help="Max results (default 6).")
    parser.add_argument("--json", action="store_true", help="Emit raw JSON instead of the table.")
    args = parser.parse_args()

    try:
        hits = find(args.query, args.limit)
    except BOSError as exc:
        emit_error_and_exit(str(exc))
        return 1

    if args.json:
        emit_json(hits)
        return 0

    if not hits:
        print(f'No endpoints matched "{args.query}".')
        print("Try broader words, or browse everything with: python tools/list-endpoints.py")
        return 0

    print(f'Top {len(hits)} matches for "{args.query}":\n')
    for h in hits:
        mark = "W" if h["is_write"] else "R"
        print(f"[{mark}] {h['method']:5s} {h['path']}")
        print(f"      {h['resource_label']}: {h['description'] or '(no description)'}")
        print(f"      run: {h['command']}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
