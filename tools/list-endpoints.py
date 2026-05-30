#!/usr/bin/env python3
"""List all TrustPager API resources and their endpoints (browse catalog).

When to use:
- "What can the TrustPager API do?"
- "Does TrustPager have an endpoint for X?"
- "Show me every endpoint under opportunities."
- Before writing a new skill — confirm the API surface you're planning to call.

What it does:
- Without args: prints a summary table of all 60+ resources with their
  endpoint counts.
- With a resource id: prints every endpoint on that resource — method, path,
  scopes, and a [R]/[W] marker for read vs write.

The catalog is the same one published at docs.trustpager.com/api-index.json
(cached locally for 24h; force a refresh with `python tools/config.py
--clear-cache`).

Usage:
    python tools/list-endpoints.py
    python tools/list-endpoints.py opportunities
    python tools/list-endpoints.py contacts

Related:
    python tools/inspect-endpoint.py <resource>     # full schema for one
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trustpager_api import BOSError, CATALOG_URL, get_catalog  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("resource_id", nargs="?", default=None,
                        help="Optional: a specific resource id to drill into")
    args = parser.parse_args()

    try:
        catalog = get_catalog()
    except BOSError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    if args.resource_id:
        resource = next((r for r in catalog["resources"]
                         if r["id"] == args.resource_id), None)
        if not resource:
            print(f"Resource not found: {args.resource_id}", file=sys.stderr)
            print(f"Available: {', '.join(r['id'] for r in catalog['resources'][:20])}...",
                  file=sys.stderr)
            return 1
        print(f"=== {resource['id']}  —  {resource['label']} ===")
        print(f"Doc: {resource.get('doc_url', '(none)')}")
        print(f"Description: {resource.get('description', '(none)')}")
        print()
        print(f"Endpoints ({len(resource['endpoints'])}):")
        for ep in resource["endpoints"]:
            mark = "W" if ep.get("is_write") else "R"
            scopes = " ".join(ep.get("scopes", []))
            print(f"  [{mark}] {ep['method']:6s} {ep['path']:50s}  scopes={scopes}")
        return 0

    print(f"Catalog from: {CATALOG_URL}")
    print(f"Generated:    {catalog.get('generated_at', '?')}")
    print(f"Base URL:     {catalog.get('base_url', '?')}")
    print(f"Auth:         {catalog.get('auth', {}).get('format', '?')}")
    print()
    print(f"{len(catalog['resources'])} resources:")
    for r in catalog["resources"]:
        n = len(r.get("endpoints", []))
        print(f"  {r['id']:30s} {n:3d} endpoints  {r.get('label', '')}")
    print()
    print("For details on one resource: python tools/list-endpoints.py <resource_id>")
    print("For one endpoint's full schema: python tools/inspect-endpoint.py <resource_id>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
