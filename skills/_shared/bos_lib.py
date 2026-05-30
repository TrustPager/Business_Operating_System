"""Business Operating System — shared library for skill scripts.

Stdlib-only. No `pip install` required. Every BOS skill script imports from
here so we get one consistent place for: API auth, base URL, GET/POST helpers,
parallel fetches, and friendly error messages for non-developer users.

Usage in a skill script:

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))
    from bos_lib import api_get, parallel_get, BOSError

    # Single call
    opportunities = api_get("opportunities", limit=100)

    # Parallel fan-out
    results = parallel_get([
        ("opportunities", {"limit": 100}),
        ("tasks", {"completed": "false"}),
        ("bookings", {"date_from": "today"}),
    ])

API key resolution order (first hit wins):
    1. $TRUSTPAGER_API_KEY environment variable (good for CI / scripts)
    2. ~/.claude/bos.json -> {"api_key": "tp_live_..."} (written by installer)
    3. Friendly error explaining how to set it
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Iterator

# The public TrustPager API base URL. Reaches the same gateway as the MCP.
API_BASE = "https://api.trustpager.com/functions/v1/api/v1"
CATALOG_URL = "https://docs.trustpager.com/api-index.json"
CONFIG_PATH = Path.home() / ".claude" / "bos.json"
CATALOG_CACHE_PATH = Path.home() / ".claude" / "bos-cache" / "api-index.json"
CATALOG_TTL_SECONDS = 24 * 60 * 60  # 24h
DEFAULT_TIMEOUT_SECONDS = 30
DEFAULT_PARALLEL_WORKERS = 8

# -----------------------------------------------------------------------------
# Path overrides — known docs/parser bugs that ship the wrong path in
# api-index.json. Remove entries here as upstream fixes ship.
#
# Discovered 2026-05-31: the docs generator flattens multi-segment SharedRoute
# patterns (e.g. ['scheduling', 'bookings']) into a single dashed string
# instead of preserving the slash. Verified live: the slashed paths 200, the
# dashed paths 404. Other dashed resources (voice-agent-kbs, event-queues,
# email-campaigns, etc.) are genuinely dashed paths and work correctly.
# -----------------------------------------------------------------------------
PATH_OVERRIDES: dict[str, str] = {
    # docs say                       # actually works
    "scheduling-bookings":          "scheduling/bookings",
    "scheduling-availability":      "scheduling/availability",
    "scheduling-event-types":       "scheduling/event-types",
}


class BOSError(Exception):
    """Friendly, user-facing error. The message is intended for end users."""


@dataclass
class ApprovalPending:
    """Returned (NOT raised) when an API write returns 202 + approval_id.

    The action has been queued for human approval, not executed. Scripts can:
      - return the approval_id to the operator for them to approve in-app
      - call .poll() to check current status without re-issuing the write
      - access .body for the full 202 response payload

    Skills that don't care about the approval flow can pass ApprovalPending
    results back to the operator as-is — the str() form is human-readable.
    """
    approval_id: str
    body: dict[str, Any]
    approval_url: str = "https://app.trustpager.com/settings/api?tab=approvals"

    def __str__(self) -> str:
        return (
            f"Queued for approval (id: {self.approval_id}). "
            f"Approve at {self.approval_url}"
        )

    def poll(self) -> dict[str, Any]:
        """Fetch the current state of this approval. Returns the approval row."""
        return api_get(f"approvals/{self.approval_id}")

    @property
    def executed(self) -> bool:
        """Has this approval been approved AND executed yet?"""
        try:
            row = self.poll()
            return bool(row.get("executed") or row.get("executed_at"))
        except BOSError:
            return False


def get_api_key() -> str:
    """Resolve the user's TrustPager API key.

    Order: env var, then ~/.claude/bos.json. Raises BOSError with a fix-it
    message if neither is set.
    """
    env = os.environ.get("TRUSTPAGER_API_KEY", "").strip()
    if env:
        return env

    if CONFIG_PATH.exists():
        try:
            config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            key = (config.get("api_key") or "").strip()
            if key:
                return key
        except (json.JSONDecodeError, OSError):
            pass  # Fall through to friendly error

    raise BOSError(
        "TrustPager API key not found.\n"
        "\n"
        "Fix it with one of:\n"
        f"  - Set TRUSTPAGER_API_KEY in your shell environment, or\n"
        f"  - Re-run the BOS installer to create {CONFIG_PATH}, or\n"
        "  - Create the file manually with the JSON shape:\n"
        '      {"api_key": "<paste your tp_live_... key here>"}'
    )


def _build_url(path: str, params: dict[str, Any] | None = None) -> str:
    """Build a full URL from a path (with or without leading slash) and query params."""
    path = path.lstrip("/")
    url = f"{API_BASE}/{path}"
    if params:
        # Drop None values; stringify everything else
        clean = {k: ("true" if v is True else "false" if v is False else str(v))
                 for k, v in params.items() if v is not None}
        if clean:
            url = f"{url}?{urllib.parse.urlencode(clean)}"
    return url


DEFAULT_RETRIES_ON_429 = 3
DEFAULT_RETRIES_ON_5XX = 2


def _parse_response_body(raw: bytes) -> dict[str, Any]:
    """Parse a JSON response body. Returns {} for empty/non-JSON bodies."""
    if not raw:
        return {}
    try:
        return json.loads(raw.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {"_raw": raw[:300].decode("utf-8", errors="replace")}


def _request(method: str, path: str, params: dict[str, Any] | None = None,
             body: dict[str, Any] | None = None, timeout: int = DEFAULT_TIMEOUT_SECONDS,
             extra_headers: dict[str, str] | None = None,
             _attempt: int = 0) -> dict[str, Any] | ApprovalPending:
    """Low-level HTTP request with rich error handling.

    Returns:
        - dict on 2xx (parsed JSON response)
        - ApprovalPending on 202 (write was queued, not executed)
        - Raises BOSError on every other failure mode

    Retry behaviour:
        - 429: retries up to DEFAULT_RETRIES_ON_429 times, honouring Retry-After
        - 5xx: retries up to DEFAULT_RETRIES_ON_5XX times with exponential backoff
        - Network errors: no retry — bubbles up immediately
    """
    api_key = get_api_key()
    url = _build_url(path, params)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "User-Agent": "BusinessOperatingSystem/1.0",
    }
    if extra_headers:
        headers.update(extra_headers)
    data: bytes | None = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = resp.read()
            parsed = _parse_response_body(payload)
            # 202 = queued for approval. Return ApprovalPending, don't raise.
            if resp.status == 202:
                approval_id = (
                    parsed.get("approval_id")
                    or parsed.get("id")
                    or (parsed.get("data") or {}).get("approval_id")
                    or "unknown"
                )
                return ApprovalPending(approval_id=approval_id, body=parsed)
            return parsed
    except urllib.error.HTTPError as e:
        detail_raw = b""
        try:
            detail_raw = e.read()
        except OSError:
            pass
        detail_parsed = _parse_response_body(detail_raw)
        detail_str = (detail_raw or b"").decode("utf-8", errors="replace")[:500]
        docs_hint = "See https://docs.trustpager.com for details."

        # 401 — bad / missing key
        if e.code == 401:
            raise BOSError(
                f"Your TrustPager API key was rejected (401 Unauthorized).\n"
                f"Check that it starts with 'tp_live_' and hasn't been revoked.\n"
                f"Manage keys: https://app.trustpager.com/settings/api"
            ) from None

        # 402 — billing / out of credits
        if e.code == 402:
            raise BOSError(
                f"Your TrustPager workspace is out of credits or has a billing issue (402).\n"
                f"Manage billing: https://app.trustpager.com/settings/billing\n"
                f"Server said: {detail_str}"
            ) from None

        # 403 — missing scope
        if e.code == 403:
            raise BOSError(
                f"Your API key doesn't have permission for {path} (403 Forbidden).\n"
                f"Add the required scope at https://app.trustpager.com/settings/api\n"
                f"Server said: {detail_str}"
            ) from None

        # 404 — bad path
        if e.code == 404:
            raise BOSError(
                f"Endpoint not found: {path} (404).\n"
                f"This may be a BOS bug, a path that's been renamed, or a typo.\n"
                f"Browse the live API catalog: https://docs.trustpager.com/api-index.json\n"
                f"Full URL was: {url}"
            ) from None

        # 422 — validation error. The API helpfully puts valid values in details.available.
        if e.code == 422:
            err = detail_parsed.get("error", {})
            msg = err.get("message") or detail_str
            available = (err.get("details") or {}).get("available")
            avail_str = f"\nValid options: {available}" if available else ""
            raise BOSError(
                f"Validation failed on {path} (422).\n"
                f"Server said: {msg}{avail_str}"
            ) from None

        # 429 — rate limited. Retry honouring Retry-After.
        if e.code == 429 and _attempt < DEFAULT_RETRIES_ON_429:
            retry_after = e.headers.get("Retry-After") if hasattr(e, "headers") else None
            wait = int(retry_after) if retry_after and retry_after.isdigit() else 2 ** _attempt
            time.sleep(min(wait, 30))
            return _request(method, path, params=params, body=body,
                            timeout=timeout, extra_headers=extra_headers,
                            _attempt=_attempt + 1)
        if e.code == 429:
            raise BOSError(
                f"Rate-limited by the TrustPager API after {DEFAULT_RETRIES_ON_429} retries.\n"
                f"Slow down the request rate or contact support to raise your limit."
            ) from None

        # 5xx — server error. Retry a couple of times then give up.
        if 500 <= e.code < 600:
            if _attempt < DEFAULT_RETRIES_ON_5XX:
                time.sleep(2 ** _attempt)
                return _request(method, path, params=params, body=body,
                                timeout=timeout, extra_headers=extra_headers,
                                _attempt=_attempt + 1)
            raise BOSError(
                f"TrustPager API returned a server error ({e.code}) after "
                f"{DEFAULT_RETRIES_ON_5XX} retries.\n"
                f"This is usually temporary. {docs_hint}\n"
                f"Server said: {detail_str}"
            ) from None

        # Catch-all
        raise BOSError(f"HTTP {e.code} on {path}. {docs_hint}\nServer said: {detail_str}") from None
    except urllib.error.URLError as e:
        raise BOSError(
            f"Could not reach the TrustPager API.\n"
            f"Check your internet connection. Underlying error: {e.reason}"
        ) from None
    except (json.JSONDecodeError, OSError) as e:
        raise BOSError(f"Unexpected response from {path}: {e}") from None


def api_get(path: str, **params: Any) -> dict[str, Any]:
    """GET a path. Query parameters passed as kwargs.

    Example:
        opportunities = api_get("opportunities", limit=100, stage="qualified")
    """
    return _request("GET", path, params=params)


def api_post(path: str, body: dict[str, Any] | None = None, **params: Any) -> dict[str, Any] | ApprovalPending:
    """POST to a path. Body is the JSON payload; kwargs are query params.

    Returns ApprovalPending on 202 (action queued for human approval) — check
    `isinstance(result, ApprovalPending)` if your skill needs to handle that path.
    """
    return _request("POST", path, params=params, body=body)


def api_patch(path: str, body: dict[str, Any] | None = None, **params: Any) -> dict[str, Any] | ApprovalPending:
    """PATCH a path. For updates. Returns ApprovalPending on 202."""
    return _request("PATCH", path, params=params, body=body)


def idempotent_post(path: str, body: dict[str, Any] | None = None,
                    idempotency_key: str | None = None,
                    **params: Any) -> dict[str, Any] | ApprovalPending:
    """POST with an Idempotency-Key header to prevent duplicate writes on retry.

    The key defaults to a deterministic SHA-256 hash of the request body. This
    means: same body -> same key -> the server dedupes if you hit a transient
    network error and the caller retries. Pass `idempotency_key=` explicitly
    to override (e.g. when retrying intentionally with a new key).

    Use for any write where a duplicate would be a problem: sending email,
    creating an opportunity, charging a customer, firing an automation.
    """
    if idempotency_key is None:
        # Deterministic key from body so a retry of the same payload dedupes
        body_bytes = json.dumps(body or {}, sort_keys=True).encode("utf-8")
        idempotency_key = "bos-" + hashlib.sha256(body_bytes).hexdigest()[:24]
    return _request("POST", path, params=params, body=body,
                    extra_headers={"Idempotency-Key": idempotency_key})


def parallel_get(calls: list[tuple[str, dict[str, Any]]],
                 max_workers: int = DEFAULT_PARALLEL_WORKERS) -> dict[str, dict[str, Any]]:
    """Fan out multiple GET requests in parallel.

    Args:
        calls: list of (path, params_dict) tuples. The path is also the result key.
        max_workers: parallel HTTP threads (default 8).

    Returns:
        Dict mapping each path to its response (or an `{"error": "..."}` dict
        on failure). Never raises — failures land per-key in the result.

    Example:
        results = parallel_get([
            ("opportunities", {"limit": 100}),
            ("tasks", {"completed": "false"}),
            ("bookings", {"date_from": "today"}),
        ])
        opps = results["opportunities"].get("data", [])
    """
    out: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        future_to_path = {
            pool.submit(api_get, path, **params): path
            for path, params in calls
        }
        for future in as_completed(future_to_path):
            path = future_to_path[future]
            try:
                out[path] = future.result()
            except BOSError as e:
                out[path] = {"error": str(e)}
            except Exception as e:  # noqa: BLE001 — last-resort safety net
                out[path] = {"error": f"Unexpected error on {path}: {e}"}
    return out


def paginate(path: str, max_pages: int | None = None,
             **params: Any) -> Iterator[dict[str, Any]]:
    """Yield every row across every page of a list endpoint.

    Auto-follows pagination.next_cursor until has_more is false (or max_pages
    is reached, if set). Use when you need ALL records, not just the first
    page. Default API limit is 25, max 100 — pass limit=100 to minimise calls.

    Example:
        all_opps = list(paginate("opportunities", limit=100))
        for contact in paginate("contacts", limit=100, source="referral"):
            do_something(contact)

    The path-param `after` is reserved for the cursor — don't pass it manually.
    """
    cursor: str | None = None
    pages = 0
    while True:
        call_params = dict(params)
        if cursor:
            call_params["after"] = cursor
        response = api_get(path, **call_params)
        rows = response.get("data", []) if isinstance(response, dict) else []
        for row in rows:
            yield row
        pages += 1
        if max_pages is not None and pages >= max_pages:
            return
        pagination = response.get("pagination", {}) if isinstance(response, dict) else {}
        if not pagination.get("has_more"):
            return
        cursor = pagination.get("next_cursor")
        if not cursor:
            return


def bulk_apply(write_fn: Callable[[Any], Any], items: list[Any],
               parallelism: int = 4,
               on_error: str = "collect",
               progress: Callable[[int, int, str], None] | None = None
               ) -> dict[str, Any]:
    """Apply a write function across many items with progress + error aggregation.

    Args:
        write_fn: callable taking a single item, returning anything
        items: list of inputs to write_fn
        parallelism: concurrent writes (default 4 — keep low to avoid 429s)
        on_error: 'collect' (default) accumulates errors and continues
                  'raise' raises on first failure
        progress: optional callback(completed, total, item_summary) for logging

    Returns:
        {
          "total": N,
          "succeeded": [{"item": ..., "result": ...}, ...],
          "failed":    [{"item": ..., "error": "..."}, ...],
          "queued":    [{"item": ..., "approval_id": "..."}, ...],   # 202 responses
        }

    Use for any bulk write — bulk send emails, bulk-update opportunities,
    bulk-create contacts. Pair with idempotent_post for safe retries.
    """
    succeeded: list[dict[str, Any]] = []
    failed: list[dict[str, Any]] = []
    queued: list[dict[str, Any]] = []
    total = len(items)
    completed = 0

    with ThreadPoolExecutor(max_workers=parallelism) as pool:
        futures = {pool.submit(write_fn, item): item for item in items}
        for future in as_completed(futures):
            item = futures[future]
            completed += 1
            try:
                result = future.result()
                if isinstance(result, ApprovalPending):
                    queued.append({"item": item, "approval_id": result.approval_id})
                else:
                    succeeded.append({"item": item, "result": result})
            except BOSError as e:
                if on_error == "raise":
                    raise
                failed.append({"item": item, "error": str(e)})
            except Exception as e:  # noqa: BLE001
                if on_error == "raise":
                    raise
                failed.append({"item": item, "error": f"Unexpected: {e}"})
            if progress:
                summary = str(item)[:60]
                progress(completed, total, summary)

    return {
        "total": total,
        "succeeded": succeeded,
        "failed": failed,
        "queued": queued,
    }


# =============================================================================
# Catalog — fetch + cache the public API endpoint index from docs.trustpager.com
# =============================================================================

_catalog_cache: dict[str, Any] | None = None  # in-process cache to avoid re-reading the file


def _catalog_is_fresh(path: Path, ttl_seconds: int) -> bool:
    if not path.exists():
        return False
    try:
        age = (datetime.now().timestamp() - path.stat().st_mtime)
        return age < ttl_seconds
    except OSError:
        return False


def _fetch_catalog_live() -> dict[str, Any]:
    """Download api-index.json from docs.trustpager.com. No auth needed."""
    req = urllib.request.Request(
        CATALOG_URL,
        headers={"Accept": "application/json", "User-Agent": "BusinessOperatingSystem/1.0"},
    )
    with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT_SECONDS) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_catalog(force_refresh: bool = False) -> dict[str, Any]:
    """Return the TrustPager API endpoint catalog.

    Order of operations:
        1. In-process memo (free)
        2. ~/.claude/bos-cache/api-index.json if younger than 24h
        3. Fetch from docs.trustpager.com, update cache
        4. If fetch fails, fall back to whatever's on disk (any age)
        5. If nothing is on disk, raise BOSError

    The catalog is public and unauthenticated — no API key needed.
    """
    global _catalog_cache
    if _catalog_cache is not None and not force_refresh:
        return _catalog_cache

    # Try fresh local cache
    if not force_refresh and _catalog_is_fresh(CATALOG_CACHE_PATH, CATALOG_TTL_SECONDS):
        try:
            _catalog_cache = json.loads(CATALOG_CACHE_PATH.read_text(encoding="utf-8"))
            return _catalog_cache
        except (json.JSONDecodeError, OSError):
            pass  # corrupt cache — fall through to refetch

    # Fetch live, write cache
    try:
        catalog = _fetch_catalog_live()
        try:
            CATALOG_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
            CATALOG_CACHE_PATH.write_text(json.dumps(catalog), encoding="utf-8")
        except OSError:
            pass  # cache write failures aren't fatal — we still have the catalog in memory
        _catalog_cache = catalog
        return catalog
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as e:
        # Fall back to any cached copy, regardless of age
        if CATALOG_CACHE_PATH.exists():
            try:
                _catalog_cache = json.loads(CATALOG_CACHE_PATH.read_text(encoding="utf-8"))
                return _catalog_cache
            except (json.JSONDecodeError, OSError):
                pass
        raise BOSError(
            f"Could not fetch the TrustPager API catalog from {CATALOG_URL}.\n"
            f"Underlying error: {e}\n"
            f"No cached copy is available. Check your internet connection."
        ) from None


def resolve_path(resource_id: str, method: str = "GET",
                 action: str = "list",
                 path_contains: str | None = None) -> str:
    """Resolve a canonical API path from the public catalog.

    Args:
        resource_id: catalog resource id, e.g. "opportunities", "scheduling-bookings"
        method: HTTP method (default GET)
        action: one of "list" (simplest path, no params), "get" (path with one
                :id segment), "create" (POST root path), or "search" (POST
                with /search suffix). Default "list".
        path_contains: required when a resource has multiple sub-resources
                of the same action shape. e.g. "email" has GET /email/threads
                AND GET /email/logs AND GET /email/configs — call with
                path_contains="threads" to disambiguate.

    Returns:
        The API path WITHOUT the base URL or leading slash. Example:
            resolve_path("scheduling-bookings", "GET", "list")
            -> "scheduling/bookings"
            resolve_path("email", "GET", "list", path_contains="threads")
            -> "email/threads"

    Path overrides (PATH_OVERRIDES) are applied AFTER catalog lookup. They
    exist to work around the known docs bug where multi-segment scheduling
    patterns are flattened to dashed strings (see PATH_OVERRIDES comment).
    """
    catalog = get_catalog()
    resource = next((r for r in catalog.get("resources", [])
                     if r.get("id") == resource_id), None)
    if not resource:
        raise BOSError(
            f"Unknown resource '{resource_id}'. Check the catalog at {CATALOG_URL}."
        )

    # Filter endpoints by method
    candidates = [ep for ep in resource.get("endpoints", [])
                  if ep.get("method") == method]
    if not candidates:
        raise BOSError(
            f"No {method} endpoint on resource '{resource_id}'."
        )

    # Narrow by action shape
    if action == "list":
        # Simplest GET: no :params, doesn't end in /search
        candidates = [c for c in candidates
                      if ":" not in c.get("path", "")
                      and not c.get("path", "").endswith("/search")]
    elif action == "get":
        candidates = [c for c in candidates
                      if c.get("path", "").count(":") == 1
                      and not c.get("path", "").endswith("/search")]
    elif action == "create":
        candidates = [c for c in candidates
                      if ":" not in c.get("path", "")
                      and not c.get("path", "").endswith("/search")]
    elif action == "search":
        candidates = [c for c in candidates
                      if c.get("path", "").endswith("/search")]
    else:
        raise BOSError(f"Unknown action '{action}'. Use list, get, create, or search.")

    # Narrow by sub-resource hint
    if path_contains:
        candidates = [c for c in candidates if path_contains in c.get("path", "")]

    if not candidates:
        raise BOSError(
            f"No {method} endpoint on '{resource_id}' matches action '{action}'"
            + (f" with path containing '{path_contains}'" if path_contains else "")
            + "."
        )

    # If multiple candidates and no path_contains hint, prefer the natural root:
    # - For "list":   /<resource_id>          (e.g. /tasks vs /tasks/categories)
    # - For "get":    /<resource_id>/:<id>    (e.g. /contacts/:id vs /contacts/:id/deals)
    # - For "create": /<resource_id>          (same as list)
    # If exactly one candidate matches that shape, use it.
    if len(candidates) > 1 and not path_contains:
        natural_root = "/" + resource_id
        if action in ("list", "create"):
            root_match = [c for c in candidates if c.get("path") == natural_root]
        elif action == "get":
            # The shortest single-segment-after-root :param path
            # e.g. /contacts/:contact_id  not  /contacts/:contact_id/deals
            root_match = [c for c in candidates
                          if c.get("path", "").startswith(natural_root + "/:")
                          and c.get("path", "").count("/") == 2]
        else:
            root_match = candidates
        if len(root_match) == 1:
            candidates = root_match

    if len(candidates) > 1:
        paths = [c.get("path", "") for c in candidates]
        raise BOSError(
            f"Ambiguous: {len(candidates)} {method} endpoints on '{resource_id}' "
            f"match action '{action}': {paths}. Pass path_contains='<segment>' "
            f"to disambiguate."
        )

    ep = candidates[0]
    raw_path = ep.get("path", "").lstrip("/")

    # Apply known docs-bug overrides (see PATH_OVERRIDES comment up top).
    # Strip any trailing segments past the override key so /scheduling-bookings/:id
    # becomes /scheduling/bookings/:id.
    for bad, good in PATH_OVERRIDES.items():
        if raw_path == bad:
            return good
        if raw_path.startswith(bad + "/"):
            return good + raw_path[len(bad):]

    return raw_path


def inspect_endpoint(resource_id: str, method: str = "GET",
                     action: str = "list",
                     path_contains: str | None = None) -> dict[str, Any]:
    """Return the full catalog entry for an endpoint — schema, scopes, doc URL.

    Use this when you're debugging a fetch script and need to know "what
    params does this take?" without leaving Python. Returns:

        {
          "resource_id": "...", "method": "...", "path": "...",
          "scopes": [...], "is_write": bool,
          "params": [{"name": ..., "in": ..., "type": ..., "required": ...}],
          "description": "...",
          "doc_url": "https://docs.trustpager.com/api/.../...md"
        }

    Raises BOSError if the endpoint can't be resolved unambiguously — pass
    `path_contains=` to disambiguate the same way resolve_path does.
    """
    catalog = get_catalog()
    resource = next((r for r in catalog.get("resources", [])
                     if r.get("id") == resource_id), None)
    if not resource:
        raise BOSError(f"Unknown resource '{resource_id}'.")

    # Same selection logic as resolve_path
    candidates = [ep for ep in resource.get("endpoints", [])
                  if ep.get("method") == method]
    if action == "list":
        candidates = [c for c in candidates
                      if ":" not in c.get("path", "")
                      and not c.get("path", "").endswith("/search")]
    elif action == "get":
        candidates = [c for c in candidates
                      if c.get("path", "").count(":") == 1
                      and not c.get("path", "").endswith("/search")]
    elif action == "create":
        candidates = [c for c in candidates
                      if ":" not in c.get("path", "")
                      and not c.get("path", "").endswith("/search")]
    elif action == "search":
        candidates = [c for c in candidates
                      if c.get("path", "").endswith("/search")]
    if path_contains:
        candidates = [c for c in candidates if path_contains in c.get("path", "")]
    if len(candidates) > 1 and not path_contains:
        natural_root = "/" + resource_id
        if action in ("list", "create"):
            root_match = [c for c in candidates if c.get("path") == natural_root]
        elif action == "get":
            root_match = [c for c in candidates
                          if c.get("path", "").startswith(natural_root + "/:")
                          and c.get("path", "").count("/") == 2]
        else:
            root_match = candidates
        if len(root_match) == 1:
            candidates = root_match

    if not candidates:
        raise BOSError(
            f"No matching {method} endpoint on '{resource_id}'."
        )
    if len(candidates) > 1:
        paths = [c.get("path", "") for c in candidates]
        raise BOSError(
            f"Ambiguous: {len(candidates)} candidates: {paths}. Pass path_contains."
        )

    ep = candidates[0]
    return {
        "resource_id": resource_id,
        "resource_label": resource.get("label"),
        "method": ep.get("method"),
        "path": ep.get("path"),
        "description": ep.get("description"),
        "scopes": ep.get("scopes", []),
        "is_write": ep.get("is_write", False),
        "params": ep.get("params", []),
        "doc_url": ep.get("doc_url"),
    }


def api_call_by_resource(resource_id: str, method: str = "GET",
                         action: str = "list", **params: Any) -> dict[str, Any]:
    """Resolve the path from the catalog then issue the request. One call helper."""
    path = resolve_path(resource_id, method, action)
    if method == "GET":
        return api_get(path, **params)
    if method == "POST":
        body = params.pop("body", None)
        return api_post(path, body=body, **params)
    if method == "PATCH":
        body = params.pop("body", None)
        return api_patch(path, body=body, **params)
    raise BOSError(f"Unsupported method: {method}")


# =============================================================================
# Date helpers — shared parsing for ISO timestamps and date-only strings
# =============================================================================
#
# The TrustPager API returns dates in three shapes:
#   - Full ISO timestamp with tz:  "2026-05-29T07:31:26.165+00:00"
#   - ISO timestamp with Z:        "2026-05-29T07:31:26Z"
#   - Date-only:                   "2026-05-29"  (assumed midnight UTC)
# All three are normalised to tz-aware datetimes so comparisons against
# `now_utc()` work without TypeError.
# =============================================================================


def now_utc() -> datetime:
    """Current time in UTC, tz-aware."""
    return datetime.now(timezone.utc)


def parse_iso(s: str | None) -> datetime | None:
    """Parse an ISO-8601 timestamp or date string into a tz-aware datetime.

    Returns None on falsy input or parse failure.
    Naive timestamps (no tz) are treated as UTC.
    """
    if not s:
        return None
    try:
        if len(s) == 10 and s[4] == "-" and s[7] == "-":
            return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (ValueError, AttributeError):
        return None


def days_since(ts: datetime | None, ref: datetime | None = None) -> int | None:
    """Whole days between `ts` and `ref` (default: now). Returns None if ts is None."""
    if ts is None:
        return None
    ref = ref or now_utc()
    return max(0, int((ref - ts).total_seconds() // 86400))


# =============================================================================
# Digest helpers — common shapes for summarising lists of records
# =============================================================================


def group_count(items: list[dict[str, Any]], key: str,
                missing: str = "(none)") -> dict[str, int]:
    """Count items grouped by a key, returned sorted by count descending.

    Example:
        group_count(opportunities, "lead_source")
        # -> {"Facebook": 18, "Referral": 6, "(none)": 4, ...}
    """
    out: dict[str, int] = {}
    for it in items:
        k = it.get(key) or missing
        out[k] = out.get(k, 0) + 1
    return dict(sorted(out.items(), key=lambda kv: kv[1], reverse=True))


def top_n_by(items: list[dict[str, Any]], key: str, n: int = 5,
             reverse: bool = True) -> list[dict[str, Any]]:
    """Return the top-N items sorted by a field.

    Args:
        items: list of dicts
        key: field to sort by — supports dot-notation for nested fields,
             e.g. "contact.email"
        n: how many to return
        reverse: True (default) = descending; False = ascending
    """
    def keyfn(it: dict[str, Any]) -> Any:
        val: Any = it
        for part in key.split("."):
            if not isinstance(val, dict):
                return 0
            val = val.get(part)
        # Coerce numeric strings, None, etc. so sort doesn't crash
        if val is None:
            return float("-inf") if reverse else float("inf")
        if isinstance(val, (int, float)):
            return val
        try:
            return float(val)
        except (ValueError, TypeError):
            return val
    return sorted(items, key=keyfn, reverse=reverse)[:n]


# =============================================================================
# Logging — shared `_log` for skill scripts (replaces per-skill helpers)
# =============================================================================


def log(prefix: str, msg: str, *, quiet: bool = False) -> None:
    """Write a one-line progress message to stderr with a [prefix] tag.

    Skills should use this instead of redefining their own _log function:

        from bos_lib import log
        def _log(msg, *, quiet): log("sweep-my-day", msg, quiet=quiet)

    Or even simpler:

        log("sweep-my-day", "fetching opportunities...", quiet=args.json_only)
    """
    if not quiet:
        sys.stderr.write(f"[{prefix}] {msg}\n")
        sys.stderr.flush()


# =============================================================================
# Output emitters
# =============================================================================


def emit_json(payload: Any) -> None:
    """Print JSON to stdout with consistent formatting.

    Used by skill scripts so Claude can parse the output. Uses indent=2 for
    human readability when developers are debugging the scripts directly.

    `ensure_ascii=True` is intentional — any non-ASCII character in the
    response (emojis in email subjects, smart quotes, etc.) gets escaped to
    \\uXXXX so the output is safe to print on any terminal encoding,
    including Windows cp1252 stdout. JSON readers (including Claude) decode
    the escapes transparently.
    """
    json.dump(payload, sys.stdout, indent=2, default=str, ensure_ascii=True)
    sys.stdout.write("\n")


def emit_error_and_exit(msg: str, code: int = 1) -> None:
    """Print a friendly error to stderr (so Claude sees it) and exit non-zero."""
    sys.stderr.write(f"ERROR: {msg}\n")
    sys.exit(code)
