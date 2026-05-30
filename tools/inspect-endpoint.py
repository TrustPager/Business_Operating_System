#!/usr/bin/env python3
"""Show the full schema for one TrustPager API endpoint (params, scopes, doc).

When to use:
- "What parameters does GET /opportunities take?"
- "Which scopes do I need for create_contact?"
- "Where's the doc page for this endpoint?"
- When writing a skill and you need to know exactly what to send.

What it prints:
- HTTP method + path
- Whether it's a write (needs higher scope)
- Required scopes
- Doc URL (deep link into docs.trustpager.com)
- Description
- Every parameter — name, location (query / body / path), type, required?,
  description.

Defaults to the "list" action (the simplest read on the resource). Pick a
different action if needed:

    --action list      simplest GET, no params         (default)
    --action get       GET with one :id segment
    --action create    POST root path
    --action search    POST with /search suffix

If a resource has multiple endpoints of the same shape (e.g. /email/threads
and /email/logs both match "list"), pass --contains <segment> to pick the
right one.

Usage:
    python tools/inspect-endpoint.py opportunities
    python tools/inspect-endpoint.py opportunities --action create
    python tools/inspect-endpoint.py email --contains threads
    python tools/inspect-endpoint.py contacts --method POST --action search

Related:
    python tools/list-endpoints.py <resource>     # all endpoints on a resource
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trustpager_api import BOSError, inspect_endpoint  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("resource_id")
    parser.add_argument("--method", default="GET")
    parser.add_argument("--action", default="list",
                        choices=["list", "get", "create", "search"])
    parser.add_argument("--contains", dest="path_contains", default=None,
                        help="Substring to disambiguate when a resource has multiple matches")
    args = parser.parse_args()

    try:
        info = inspect_endpoint(
            args.resource_id, method=args.method, action=args.action,
            path_contains=args.path_contains,
        )
    except BOSError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print(f"=== {info['method']} {info['path']} ===")
    print(f"Resource:    {info['resource_id']} — {info.get('resource_label', '')}")
    print(f"Write:       {'yes' if info['is_write'] else 'no'}")
    print(f"Scopes:      {' '.join(info['scopes']) if info['scopes'] else '(none)'}")
    print(f"Doc:         {info['doc_url']}")
    print()
    print(f"Description: {info['description']}")
    print()
    if info["params"]:
        print(f"Parameters ({len(info['params'])}):")
        for p in info["params"]:
            req = "required" if p.get("required") else "optional"
            print(f"  - {p.get('name', '?'):20s} {p.get('in', '?'):6s} "
                  f"{p.get('type', '?'):8s} {req}")
            desc = p.get("description", "")
            if desc:
                print(f"      {desc}")
    else:
        print("Parameters: (none)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
