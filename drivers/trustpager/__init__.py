"""TrustPager driver — the ONE DriverConfig + bound api_* over the kernel.

This is where the vendor-neutral kernel gets parameterized for TrustPager:

  - TP_CFG: the single DriverConfig (base URL, key resolver, secret shape,
    per-code messages, approval URL). Constructing it registers the tp_ secret
    pattern via DriverConfig.__post_init__ — so importing this package is what
    arms redaction for TrustPager keys.
  - ApprovalPending: the TrustPager subclass of the kernel's base, adding
    poll()/executed (which read the live API) and defaulting approval_url.
  - api_get / api_post / api_patch / idempotent_post: bound over
    kernel.runtime.transport.request(TP_CFG, ...), with writes wrapped in
    kernel.runtime.journal.journaled and 202s upgraded to the subclass.
  - bulk_apply: bound over kernel.runtime.reads. (parallel_get / paginate are
    defined in the shim, not here — see the bulk_apply section comment.)
  - resolve_path / get_catalog / inspect_endpoint: re-exported from .catalog.

Dependencies are one-way: this package imports from kernel.runtime.* and
stdlib only — never from tools/.
"""

from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

# Put the repo root on sys.path so `import kernel.runtime.*` resolves even when
# only tools/ was added by a skill caller.
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from kernel.runtime.errors import BOSError  # noqa: E402
from kernel.runtime import journal as _journal  # noqa: E402
from kernel.runtime import reads as _reads  # noqa: E402
from kernel.runtime import transport as _transport  # noqa: E402
from kernel.runtime.transport import (  # noqa: E402
    DriverConfig,
    ApprovalPending as _KernelApprovalPending,
)

from drivers.trustpager.auth import (  # noqa: E402
    APPROVAL_URL,
    CONFIG_PATH,
    TP_ERROR_MAP,
    TP_SECRET_PATTERN,
    get_api_key,
)
from drivers.trustpager.catalog import (  # noqa: E402
    API_BASE,
    CATALOG_CACHE_PATH,
    CATALOG_URL,
    api_call_by_resource,
    get_catalog,
    inspect_endpoint,
    resolve_path,
)

DEFAULT_TIMEOUT_SECONDS = 30

# The write journal's directory has exactly ONE home: kernel.runtime.journal
# .JOURNAL_DIR (a vendor-neutral path under the user's home). This driver does
# NOT keep its own copy — _journaled() below calls into the kernel without a
# journal_dir override, so the kernel's single constant governs the real write
# path. (Removed a duplicate constant here per the Task 3 code-quality finding.)


# =============================================================================
# The single TrustPager DriverConfig. Constructing it registers the tp_ secret
# pattern with the redaction registry (DriverConfig.__post_init__).
# =============================================================================
TP_CFG = DriverConfig(
    base_url=API_BASE,
    key_resolver=get_api_key,
    secret_pattern=TP_SECRET_PATTERN,
    error_map=TP_ERROR_MAP,
    approval_url=APPROVAL_URL,
)


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
    """
    approval_url: str = APPROVAL_URL

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


def _journaled(method: str, path: str, body: dict[str, Any] | None,
               fn: Callable[[], Any]) -> dict[str, Any] | ApprovalPending:
    """Run a write callable, journal the outcome (ok / approval_pending / error).

    No journal_dir override — the kernel journals to its single
    kernel.runtime.journal.JOURNAL_DIR home.
    """
    return _journal.journaled(method, path, body, fn,
                              approval_cls=_KernelApprovalPending)


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
# Scaled writes — bound wrapper over kernel.runtime.reads.
#
# The mechanism (bulk fan-out) is vendor-neutral in the kernel and takes the
# bound write callable as its first argument; bulk_apply has no api_get global
# dependence, so it's bound here.
#
# The read wrappers parallel_get / paginate are NOT defined here: they live in
# the shim (tools/trustpager_api.py) so they resolve api_get through the shim's
# globals at call time — that's the seam tools/test-skill.py rebinds with a
# fixture mock. Defining them here too would be dead code (nothing imports them
# from this package — the shim builds its own), so they were removed.
# =============================================================================


def bulk_apply(write_fn: Callable[[Any], Any], items: list[Any],
               parallelism: int = 4,
               on_error: str = "collect",
               progress: Callable[[int, int, str], None] | None = None
               ) -> dict[str, Any]:
    """Apply a write function across many items. See kernel.runtime.reads."""
    return _reads.bulk_apply(write_fn, items, parallelism=parallelism,
                             on_error=on_error, progress=progress,
                             approval_cls=_KernelApprovalPending)


__all__ = [
    "TP_CFG",
    "ApprovalPending",
    "api_get",
    "api_post",
    "api_patch",
    "idempotent_post",
    "bulk_apply",
    "resolve_path",
    "get_catalog",
    "inspect_endpoint",
    "api_call_by_resource",
    "get_api_key",
    "API_BASE",
    "CATALOG_URL",
    "CATALOG_CACHE_PATH",
    "CONFIG_PATH",
    "APPROVAL_URL",
]
