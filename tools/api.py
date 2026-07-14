#!/usr/bin/env python3
"""Call any TrustPager API endpoint from one command (the generic escape hatch).

When to use:
- You want a resource the named tools/skills don't wrap yet. There are 60+ API
  resources and hundreds of endpoints; this reaches all of them without loading
  the MCP tool surface into context.
- Quick one-off reads ("show me the first 5 pipelines") or a single write.
- Building or debugging a skill: prove the exact call works before wiring it in.

Why this exists:
- The MCP connector exposes 700+ tools. A chat client can only surface a ranked
  subset at a time, so some tools (often the read/list ones) get ranked out and
  look "missing". This command is a FIXED surface over the same REST API, so a
  call can never be ranked out. It resolves paths from the public catalog
  (docs.trustpager.com/api-index.json), the same source list-endpoints uses.

Addressing a call two ways:
- By resource id (resolved from the catalog):
    python tools/api.py GET opportunities --limit 20
    python tools/api.py GET contacts --action search --body '{"query":"acme"}'
    python tools/api.py POST contacts --body '{"first_name":"Sam"}' --confirm
- By raw path (anything with a "/", or force it with --raw). This is the
  long-tail escape hatch for endpoints that take an :id or nested segments:
    python tools/api.py GET opportunities/7f3a...
    python tools/api.py PATCH opportunities/7f3a... --body '{"status":"won"}' --confirm
    python tools/api.py GET pipelines/7f3a.../deals

Reads are free. Writes (POST/PATCH) cost credits, are recorded to the write
journal, and REQUIRE --confirm so nothing writes by accident. If a write comes
back queued for approval (HTTP 202), it is NOT done: approve it in-app at the
printed approval URL, then it runs. Never re-issue a queued write.

Output: the parsed JSON response on stdout (indent=2). Progress and the queued-
for-approval notice go to stderr, so stdout stays pipeable.

Related:
    python tools/list-endpoints.py [resource]     # browse the whole catalog
    python tools/inspect-endpoint.py <resource>   # one endpoint's full schema
    python tools/find-capability.py "<goal>"      # "can it do X?" -> the command
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trustpager_api import (  # noqa: E402
    ApprovalPending,
    BOSError,
    api_get,
    api_patch,
    api_post,
    emit_error_and_exit,
    emit_json,
    force_utf8_stdout,
    log,
    resolve_path,
)

WRITE_METHODS = {"POST", "PATCH"}
DEFAULT_ACTION = {"GET": "list", "POST": "create", "PATCH": "get"}


def _parse_query(pairs: list[str]) -> dict[str, str]:
    """Turn ['limit=20', 'stage=qualified'] into {'limit': '20', ...}."""
    params: dict[str, str] = {}
    for raw in pairs:
        if "=" not in raw:
            emit_error_and_exit(
                f"--query expects key=value, got '{raw}'. "
                f"Example: --query limit=20 --query stage=qualified"
            )
        key, value = raw.split("=", 1)
        key = key.strip()
        if not key:
            emit_error_and_exit(f"--query has an empty key in '{raw}'.")
        params[key] = value
    return params


def _load_body(body: str | None, body_file: str | None) -> dict[str, Any] | None:
    """Resolve the request body from --body (inline JSON) or --body-file."""
    if body and body_file:
        emit_error_and_exit("Pass --body OR --body-file, not both.")
    raw: str | None = None
    if body_file:
        try:
            raw = Path(body_file).read_text(encoding="utf-8")
        except OSError as exc:
            emit_error_and_exit(f"Could not read --body-file '{body_file}': {exc}")
    elif body:
        raw = body
    if raw is None:
        return None
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        emit_error_and_exit(f"--body must be valid JSON: {exc}")
    if not isinstance(parsed, dict):
        emit_error_and_exit("--body must be a JSON object, e.g. '{\"name\":\"Acme\"}'.")
    return parsed


def _resolve_target(method: str, target: str, action: str | None,
                    path_contains: str | None, raw: bool) -> str:
    """Return the API path to call. Raw/pathy targets pass through verbatim."""
    if raw or "/" in target:
        return target.lstrip("/")
    # Bare resource id -> resolve from the catalog by action shape.
    act = action or DEFAULT_ACTION[method]
    if method == "PATCH" and act == "get":
        emit_error_and_exit(
            f"PATCH needs a specific record path, e.g. '{target}/<id>'. "
            f"Pass the full path (with the id) rather than the bare resource."
        )
    try:
        return resolve_path(target, method, act, path_contains=path_contains)
    except BOSError as exc:
        emit_error_and_exit(
            f"{exc}\nTip: browse ids with `python tools/list-endpoints.py`, or "
            f"pass a raw path with a leading resource/id (e.g. '{target}/<id>')."
        )
    return ""  # unreachable; emit_error_and_exit raises SystemExit


def main() -> int:
    force_utf8_stdout()

    parser = argparse.ArgumentParser(
        description="Call any TrustPager API endpoint by resource id or raw path.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("method", help="HTTP method: GET, POST, or PATCH (case-insensitive).")
    parser.add_argument("target", help="A catalog resource id (e.g. opportunities) or a raw path (e.g. opportunities/<id>).")
    parser.add_argument("--action", choices=["list", "get", "create", "search"], default=None,
                        help="Endpoint shape when target is a bare resource id. Default: list for GET, create for POST.")
    parser.add_argument("--path-contains", default=None,
                        help="Disambiguate sub-resources of the same shape (e.g. --path-contains bookings).")
    parser.add_argument("-q", "--query", action="append", default=[], metavar="KEY=VALUE",
                        help="Query parameter (repeatable), e.g. -q limit=20 -q stage=qualified.")
    parser.add_argument("--limit", type=int, default=None,
                        help="Shorthand for -q limit=<n> on list reads.")
    parser.add_argument("--body", default=None, help="Request body as inline JSON (POST/PATCH).")
    parser.add_argument("--body-file", default=None, help="Path to a file containing the JSON body.")
    parser.add_argument("--raw", action="store_true",
                        help="Treat target as a literal API path, skip catalog resolution.")
    parser.add_argument("--confirm", action="store_true",
                        help="Required for POST/PATCH. Confirms you intend to write.")
    args = parser.parse_args()

    method = args.method.upper()
    if method not in ("GET", "POST", "PATCH"):
        emit_error_and_exit(f"Unsupported method '{args.method}'. Use GET, POST, or PATCH.")

    query = _parse_query(args.query)
    if args.limit is not None:
        query.setdefault("limit", str(args.limit))

    body = _load_body(args.body, args.body_file)

    if method in WRITE_METHODS and not args.confirm:
        emit_error_and_exit(
            f"{method} is a write and costs credits. Re-run with --confirm once "
            f"you're sure. (Writes are journaled; a write may queue for in-app "
            f"approval depending on your key.)",
            code=2,
        )

    path = _resolve_target(method, args.target, args.action, args.path_contains, args.raw)
    log("api", f"{method} {path}" + (f"  query={query}" if query else ""))

    try:
        if method == "GET":
            result = api_get(path, **query)
        elif method == "POST":
            result = api_post(path, body=body, **query)
        else:  # PATCH
            result = api_patch(path, body=body, **query)
    except BOSError as exc:
        emit_error_and_exit(str(exc))
        return 1  # unreachable

    if isinstance(result, ApprovalPending):
        log("api", "Queued for approval — NOT executed. Approve it in-app, then it runs.")
        emit_json({
            "status": "pending_approval",
            "executed": False,
            "approval_id": result.approval_id,
            "approval_url": result.approval_url,
            "note": "This write was queued for human approval. Do not re-run it. "
                    "Approve it at the approval_url, then the platform executes it.",
        })
        return 0

    emit_json(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
