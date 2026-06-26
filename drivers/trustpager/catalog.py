"""TrustPager API catalog — fetch/cache the public endpoint index + resolve paths.

The catalog (docs.trustpager.com/api-index.json) is public and unauthenticated,
so fetching it is NOT gated by BOS_OFFLINE — it can't leak a key. This module
owns:
  - API_BASE / CATALOG_URL and the catalog cache path/TTL
  - the in-process catalog memo + freshness check + live fetch
  - get_catalog(), resolve_path(), inspect_endpoint()
  - PATH_OVERRIDES + the cross-catalog bridge (known docs-generator bug
    workarounds — resolve_path output is byte-identical to its old home)
  - api_call_by_resource() (resolve + issue in one call)

Imports only from kernel.runtime.* and stdlib — never from tools/.
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

# Put the repo root on sys.path so `import kernel.runtime.*` resolves even when
# only tools/ was added by a skill caller.
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from kernel.runtime.errors import BOSError  # noqa: E402

# The public TrustPager API base URL. Reaches the same gateway as the MCP.
API_BASE = "https://api.trustpager.com/functions/v1/api/v1"
CATALOG_URL = "https://docs.trustpager.com/api-index.json"
CATALOG_CACHE_PATH = Path.home() / ".claude" / "bos-cache" / "api-index.json"
CATALOG_TTL_SECONDS = 24 * 60 * 60  # 24h
DEFAULT_TIMEOUT_SECONDS = 30

# -----------------------------------------------------------------------------
# Path overrides — known docs/parser bugs that ship the wrong path in
# api-index.json. Remove entries here as upstream fixes ship.
#
# Discovered 2026-05-31: the docs generator flattens multi-segment SharedRoute
# patterns (e.g. ['scheduling', 'bookings']) into a single dashed string
# instead of preserving the slash. Verified live: the slashed paths 200, the
# dashed paths 404. Other dashed resources (voice-agent-kbs, event-queues,
# email-campaigns, etc.) are genuinely dashed paths and work correctly.
#
# STATUS (reviewed 2026-06-25, P0 substrate freeze): KEPT — load-bearing.
# resolve_path() relies on this to turn the catalog's dashed scheduling ids
# into the slashed paths the live API actually serves. We CANNOT verify from
# here whether the upstream docs-generator fix has shipped, so this stays until
# someone confirms api-index.json serves the slashed paths (then delete the
# matching entry). Do NOT remove blind — removing a still-needed entry 404s the
# scheduling calls. Paired with the cross-catalog bridge in resolve_path().
# -----------------------------------------------------------------------------
PATH_OVERRIDES: dict[str, str] = {
    # docs say                       # actually works
    "scheduling-bookings":          "scheduling/bookings",
    "scheduling-availability":      "scheduling/availability",
    "scheduling-event-types":       "scheduling/event-types",
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
    """Download api-index.json from docs.trustpager.com. No auth needed.

    NOT gated by BOS_OFFLINE: the catalog is public and unauthenticated, so
    fetching it can't leak a key. BOS_OFFLINE only blocks the authenticated
    request path that reads the API key.
    """
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
        resource_id: catalog resource id, e.g. "opportunities", "scheduling"
        method: HTTP method (default GET)
        action: one of "list" (simplest path, no params), "get" (path with one
                :id segment), "create" (POST root path), or "search" (POST
                with /search suffix). Default "list".
        path_contains: required when a resource has multiple sub-resources
                of the same action shape. e.g. "scheduling" has GET
                /scheduling/bookings AND GET /scheduling/availability — call
                with path_contains="bookings" to disambiguate.

    Returns:
        The API path WITHOUT the base URL or leading slash. Example:
            resolve_path("scheduling", "GET", "list", path_contains="bookings")
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

    # ---- Cross-catalog bridge (known docs-generator bug workaround) ----------
    # The upstream docs fix consolidates 3 dashed scheduling resources
    # (scheduling-bookings, scheduling-availability, scheduling-event-types)
    # under a single "scheduling" parent. Callers should already be using the
    # new shape:  resolve_path("scheduling", path_contains="bookings").
    # During the cutover window (DNS + 24h cache TTL) some clients still see
    # the legacy catalog where "scheduling" doesn't exist as a resource_id.
    # Fall back to the dashed legacy id so the same call works in both worlds.
    #
    # STATUS (reviewed 2026-06-25, P0 substrate freeze): KEPT until
    # verified-removable. The original "~48h post-cutover" note was a guess; we
    # cannot confirm from here whether every client's cached catalog has the
    # consolidated "scheduling" resource, and removing this early breaks callers
    # still on the legacy dashed catalog. Safe-by-design: this only fires when
    # the canonical resource_id is absent AND a path_contains hint is present,
    # so it is a no-op once the new catalog is everywhere. Remove this block +
    # the PATH_OVERRIDES scheduling entries together, only after confirming the
    # consolidated catalog has fully propagated.
    if not resource and path_contains:
        legacy_id = f"{resource_id}-{path_contains}"
        resource = next((r for r in catalog.get("resources", [])
                         if r.get("id") == legacy_id), None)
        if resource:
            resource_id = legacy_id  # keep downstream messages honest
    # --------------------------------------------------------------------------

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
    """Resolve the path from the catalog then issue the request. One call helper.

    The api_get/api_post/api_patch bindings live in drivers.trustpager (the
    package __init__). They are imported lazily here to avoid an import cycle
    (the package imports this module).
    """
    from drivers import trustpager as _tp  # local import breaks the cycle

    path = resolve_path(resource_id, method, action)
    if method == "GET":
        return _tp.api_get(path, **params)
    if method == "POST":
        body = params.pop("body", None)
        return _tp.api_post(path, body=body, **params)
    if method == "PATCH":
        body = params.pop("body", None)
        return _tp.api_patch(path, body=body, **params)
    raise BOSError(f"Unsupported method: {method}")
