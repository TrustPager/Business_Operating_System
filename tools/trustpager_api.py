"""TrustPager API — shared library for skill scripts and tools.

Stdlib-only. No `pip install` required. Every script in this repo imports
from here so we get one consistent place for: API auth, base URL, GET/POST
helpers, parallel fetches, paginated reads, bulk writes, catalog-driven
path resolution, and friendly error messages for non-developer users.

Usage in a skill script:

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))
    from trustpager_api import api_get, parallel_get, BOSError

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
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Iterator

# --- Kernel re-exports -------------------------------------------------------
# The vendor-neutral primitives now live in kernel/runtime/. They were lifted
# out of this module (P0 Task 1). We re-import them here so every existing
# caller and all the skill fetch.py scripts keep importing them unchanged
# `from trustpager_api import BOSError, now_utc, ...`.
#
# Callers only add tools/ to sys.path, so put the repo root (tools/'s parent)
# on the path first to make `import kernel.runtime.*` resolve.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from kernel.runtime.errors import BOSError  # noqa: E402,F401  (re-exported)
from kernel.runtime.offline import is_offline  # noqa: E402
from kernel.runtime.redaction import (  # noqa: E402
    redact,
    register_secret_pattern,
)
from kernel.runtime.helpers import (  # noqa: E402,F401  (re-exported)
    days_since,
    emit_error_and_exit,
    emit_json,
    force_utf8_stdout,
    group_count,
    log,
    now_utc,
    parse_iso,
    top_n_by,
)
from kernel.runtime import journal as _journal  # noqa: E402
from kernel.runtime import reads as _reads  # noqa: E402
from kernel.runtime import transport as _transport  # noqa: E402
from kernel.runtime.transport import (  # noqa: E402
    DriverConfig,
    ApprovalPending as _KernelApprovalPending,
)

# Backwards-compatible aliases for the semi-private names callers/tests still
# use (e.g. tests/test_safety.py references _redact and _is_offline). Keep
# these working so the existing suite passes unchanged.
_is_offline = is_offline
_redact = redact

# Vendor secret pattern registration. The kernel ships an EMPTY redaction
# registry; the vendor-specific key shape registers here. This matches a REAL
# key (a long token after the prefix), not the bare prefix that appears in
# docs/error messages. It is also exposed as `_SECRET_RE` for callers/tests
# that reference the compiled pattern directly.
#
# INTERIM HOME: this registration relocates to drivers/trustpager in P0 Task 3.
_SECRET_RE = re.compile(r"tp_(?:live|test)_[A-Za-z0-9_\-]{16,}")
register_secret_pattern(r"tp_(?:live|test)_[A-Za-z0-9_\-]{16,}")
# -----------------------------------------------------------------------------

# The public TrustPager API base URL. Reaches the same gateway as the MCP.
API_BASE = "https://api.trustpager.com/functions/v1/api/v1"
CATALOG_URL = "https://docs.trustpager.com/api-index.json"
CONFIG_PATH = Path.home() / ".claude" / "bos.json"
CATALOG_CACHE_PATH = Path.home() / ".claude" / "bos-cache" / "api-index.json"
JOURNAL_DIR = Path.home() / ".claude" / "bos-journal"  # write audit trail (see tools/journal.py)
APPROVAL_URL = "https://app.trustpager.com/settings/api?tab=approvals"  # 202 approve-here page
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


@dataclass
class ApprovalPending(_KernelApprovalPending):
    """Returned (NOT raised) when an API write returns 202 + approval_id.

    The action has been queued for human approval, not executed. Scripts can:
      - return the approval_id to the operator for them to approve in-app
      - call .poll() to check current status without re-issuing the write
      - access .body for the full 202 response payload

    Skills that don't care about the approval flow can pass ApprovalPending
    results back to the operator as-is — the str() form is human-readable.

    The vendor-neutral base (kernel.runtime.transport.ApprovalPending) carries
    approval_id/body/approval_url + the human-readable __str__. This subclass
    adds the TrustPager-specific poll()/executed behaviour (which read the live
    API) and defaults approval_url to the TrustPager approvals page.

    INTERIM HOME: this TrustPager-specific subclass relocates to
    drivers/trustpager in P0 Task 3.
    """
    approval_url: str = "https://app.trustpager.com/settings/api?tab=approvals"

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


def _to_tp_approval(result: Any) -> Any:
    """Upgrade a kernel ApprovalPending into the TrustPager subclass.

    transport.request() returns the vendor-neutral base ApprovalPending. Wrap
    it so callers/skills get the poll()/executed methods they already rely on,
    and so isinstance(result, ApprovalPending) keeps matching.
    """
    if isinstance(result, _KernelApprovalPending) and not isinstance(result, ApprovalPending):
        return ApprovalPending(
            approval_id=result.approval_id,
            body=result.body,
            approval_url=result.approval_url or APPROVAL_URL,
        )
    return result


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


# =============================================================================
# Transport — INTERIM TrustPager DriverConfig wiring the kernel HTTP seam.
#
# The vendor-neutral HTTP mechanism (DriverConfig + request + retries + 202)
# now lives in kernel/runtime/transport.py. Here we build the ONE TrustPager
# DriverConfig that parameterizes it: the base URL, the key resolver, the key
# shape to redact, the per-HTTP-code human messages (lifted verbatim from the
# old _request 401/402/403/404/422 branches), and the approval URL.
#
# INTERIM HOME: this TrustPager config relocates to drivers/trustpager in P0
# Task 3. Until then it lives next to its callers so trustpager_api stays a
# drop-in for every existing skill and test.
# =============================================================================

# Per-code, user-facing messages. {path}/{url}/{detail} are filled by the
# kernel's _format_http_error. 429/5xx use the kernel's generic message (their
# retry/backoff behaviour is preserved in the kernel transport).
_TP_ERROR_MAP: dict[int, str] = {
    401: (
        "Your TrustPager API key was rejected (401 Unauthorized).\n"
        "Check that it starts with 'tp_live_' and hasn't been revoked.\n"
        "Manage keys: https://app.trustpager.com/settings/api"
    ),
    402: (
        "Your TrustPager workspace is out of credits or has a billing issue (402).\n"
        "Manage billing: https://app.trustpager.com/settings/billing\n"
        "Server said: {detail}"
    ),
    403: (
        "Your API key doesn't have permission for {path} (403 Forbidden).\n"
        "Add the required scope at https://app.trustpager.com/settings/api\n"
        "Server said: {detail}"
    ),
    404: (
        "Endpoint not found: {path} (404).\n"
        "This may be a BOS bug, a path that's been renamed, or a typo.\n"
        "Browse the live API catalog: https://docs.trustpager.com/api-index.json\n"
        "Full URL was: {url}"
    ),
    422: (
        "Validation failed on {path} (422).\n"
        "Server said: {detail}{available}"
    ),
}

# The single TrustPager DriverConfig. Constructing it registers the tp_ secret
# pattern with the redaction registry (already registered above; idempotent).
TP_CFG = DriverConfig(
    base_url=API_BASE,
    key_resolver=get_api_key,
    secret_pattern=r"tp_(?:live|test)_[A-Za-z0-9_\-]{16,}",
    error_map=_TP_ERROR_MAP,
    approval_url=APPROVAL_URL,
)


def _request(method: str, path: str, params: dict[str, Any] | None = None,
             body: dict[str, Any] | None = None, timeout: int = DEFAULT_TIMEOUT_SECONDS,
             extra_headers: dict[str, str] | None = None) -> dict[str, Any] | ApprovalPending:
    """Low-level HTTP request — thin alias over the kernel transport bound to TP_CFG.

    Returns:
        - dict on 2xx (parsed JSON response)
        - ApprovalPending on 202 (write was queued, not executed)
        - Raises BOSError on every other failure mode

    Retry/backoff (429 honouring Retry-After, 5xx) and the offline-guard-before-
    key ordering all live in the kernel transport now. We upgrade the kernel's
    plain ApprovalPending into the TrustPager subclass so poll()/executed work.
    """
    result = _transport.request(TP_CFG, method, path, params=params, body=body,
                                timeout=timeout, extra_headers=extra_headers)
    return _to_tp_approval(result)


# =============================================================================
# Write journal — every write BOS issues is appended to ~/.claude/bos-journal.
# Reads are never journaled. Best-effort: journaling failures never break the
# write. Disable with BOS_JOURNAL=0. The mechanism lives in
# kernel/runtime/journal.py; these thin wrappers bind it to JOURNAL_DIR (which
# tests reassign) and the TrustPager ApprovalPending type.
# =============================================================================


def _record_write(method: str, path: str, body: dict[str, Any] | None, *,
                  status: str, result_id: str | None = None,
                  approval_id: str | None = None, error: str | None = None) -> None:
    """Append one write-attempt line to today's journal file. Never raises.

    Passes the module-level JOURNAL_DIR explicitly so tests that reassign
    trustpager_api.JOURNAL_DIR keep redirecting the journal.
    """
    _journal.record_write(method, path, body, status=status, result_id=result_id,
                          approval_id=approval_id, error=error, journal_dir=JOURNAL_DIR)


def _journaled(method: str, path: str, body: dict[str, Any] | None,
               fn: Callable[[], Any]) -> dict[str, Any] | ApprovalPending:
    """Run a write callable, journal the outcome (ok / approval_pending / error)."""
    return _journal.journaled(method, path, body, fn,
                              approval_cls=_KernelApprovalPending,
                              journal_dir=JOURNAL_DIR)


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

    Every call is recorded to the write journal (~/.claude/bos-journal).
    """
    return _journaled("POST", path, body, lambda: _request("POST", path, params=params, body=body))


def api_patch(path: str, body: dict[str, Any] | None = None, **params: Any) -> dict[str, Any] | ApprovalPending:
    """PATCH a path. For updates. Returns ApprovalPending on 202.

    Every call is recorded to the write journal (~/.claude/bos-journal).
    """
    return _journaled("PATCH", path, body, lambda: _request("PATCH", path, params=params, body=body))


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
    return _journaled("POST", path, body, lambda: _request(
        "POST", path, params=params, body=body,
        extra_headers={"Idempotency-Key": idempotency_key}))


# =============================================================================
# Scaled reads/writes — bound wrappers over kernel.runtime.reads.
#
# The mechanism (fan-out, pagination, bulk) is vendor-neutral in the kernel and
# takes the bound get/write callable as its first argument. These wrappers keep
# the SAME signatures the 22 skill fetch.py scripts already call:
#     parallel_get([(path, params), ...])
#     paginate(path, limit=100, max_pages=N)
#     bulk_apply(write_fn, items, ...)
# They look api_get up at call time (via this module's globals) so tools/
# test-skill.py, which monkeypatches trustpager_api.api_get, is still observed.
# =============================================================================


def parallel_get(calls: list[tuple[str, dict[str, Any]]],
                  max_workers: int = DEFAULT_PARALLEL_WORKERS) -> dict[str, dict[str, Any]]:
    """Fan out multiple GET requests in parallel. See kernel.runtime.reads."""
    return _reads.parallel_get(api_get, calls, max_workers=max_workers)


def paginate(path: str, max_pages: int | None = None,
             **params: Any) -> Iterator[dict[str, Any]]:
    """Yield every row across every page of a list endpoint. See kernel.runtime.reads."""
    return _reads.paginate(api_get, path, max_pages=max_pages, **params)


def bulk_apply(write_fn: Callable[[Any], Any], items: list[Any],
               parallelism: int = 4,
               on_error: str = "collect",
               progress: Callable[[int, int, str], None] | None = None
               ) -> dict[str, Any]:
    """Apply a write function across many items. See kernel.runtime.reads."""
    return _reads.bulk_apply(write_fn, items, parallelism=parallelism,
                             on_error=on_error, progress=progress,
                             approval_cls=_KernelApprovalPending)


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
    fetching it can't leak a key. BOS_OFFLINE only blocks `_request` — the
    authenticated path that reads the API key.
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
