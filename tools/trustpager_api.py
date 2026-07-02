"""Compatibility shim — the real homes are `kernel/runtime/` (vendor-neutral)
and `drivers/trustpager/` (TrustPager). Kept so existing `skills/*/fetch.py`
imports keep working.

Every name below is re-exported (NOT redefined) from its one true home:

    kernel.runtime.errors      -> BOSError
    kernel.runtime.helpers     -> now_utc, parse_iso, days_since, group_count,
                                   top_n_by, log, emit_json,
                                   emit_error_and_exit, force_utf8_stdout
    kernel.runtime.offline     -> is_offline      (semi-private alias _is_offline)
    kernel.runtime.redaction   -> redact          (semi-private alias _redact)
    kernel.runtime.journal     -> JOURNAL_DIR
    drivers.trustpager         -> api_get, api_post, api_patch, idempotent_post,
                                   bulk_apply, resolve_path, get_catalog,
                                   inspect_endpoint, api_call_by_resource,
                                   get_api_key, ApprovalPending, TP_CFG, API_BASE,
                                   CATALOG_URL, CATALOG_CACHE_PATH, CONFIG_PATH,
                                   APPROVAL_URL

The only two names DEFINED here (not re-exported) are `parallel_get` /
`paginate` — thin wrappers over kernel.runtime.reads that preserve a test seam
(see below).

A skill script reaches these unchanged:

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))
    from trustpager_api import api_get, parallel_get, BOSError

Test seams preserved:
  - tools/test-skill.py reassigns `trustpager_api.api_get` to a fixture mock.
    `parallel_get` / `paginate` are thin wrappers defined HERE that look
    `api_get` up via *this* module's globals at call time, so the rebinding is
    observed. (`bulk_apply` takes its write fn explicitly, so it has no api_get
    global dependence and is re-exported straight from the driver.)
  - The write journal's directory lives only in kernel.runtime.journal; tests
    that need to redirect it patch `kernel.runtime.journal.JOURNAL_DIR`.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Iterator

# Callers only put tools/ on sys.path. Add the repo root (tools/'s parent) so
# `import kernel.runtime.*` and `import drivers.*` resolve.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

# --- Kernel re-exports (vendor-neutral) --------------------------------------
from kernel.runtime.errors import BOSError  # noqa: E402,F401
from kernel.runtime.helpers import (  # noqa: E402,F401
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
from kernel.runtime.journal import JOURNAL_DIR  # noqa: E402,F401
from kernel.runtime.offline import is_offline as _is_offline  # noqa: E402,F401
from kernel.runtime.redaction import redact as _redact  # noqa: E402,F401

# --- TrustPager driver re-exports --------------------------------------------
# Importing drivers.trustpager constructs TP_CFG, whose DriverConfig.__post_init__
# registers the tp_ secret pattern with the redaction registry — the SOLE
# registration point.
from drivers.trustpager import (  # noqa: E402,F401
    API_BASE,
    APPROVAL_URL,
    ApprovalPending,
    CATALOG_CACHE_PATH,
    CATALOG_URL,
    CONFIG_PATH,
    TP_CFG,
    api_call_by_resource,
    api_get,
    api_patch,
    api_post,
    bulk_apply,
    get_api_key,
    get_catalog,
    idempotent_post,
    inspect_endpoint,
    resolve_path,
)
from drivers.trustpager.auth import TP_SECRET_PATTERN as _TP_SECRET_PATTERN  # noqa: E402
from kernel.runtime import reads as _reads  # noqa: E402
from kernel.runtime.redaction import _snapshot_patterns as _redaction_snapshot  # noqa: E402

# The driver import above is load-bearing: constructing TP_CFG registers the
# tp_ secret pattern with the redaction registry. If a refactor ever reorders
# imports so that side effect stops firing, journal lines would carry raw keys.
# Fail loudly here instead. Checked against the TP pattern specifically (not
# just "registry non-empty") so a future second driver's registration can't
# mask a TrustPager regression.
if not any(src == _TP_SECRET_PATTERN for src, _ in _redaction_snapshot()):
    raise RuntimeError(
        "trustpager_api: TP_SECRET_PATTERN is not registered with the redaction "
        "registry — importing drivers.trustpager no longer registers it "
        "(DriverConfig.__post_init__). Fix the driver import before shipping."
    )


# --- Rebinding-aware read wrappers -------------------------------------------
# parallel_get / paginate are defined here (not re-exported from the driver) so
# they resolve `api_get` through THIS module's globals at call time. That keeps
# the tools/test-skill.py seam working: it reassigns `trustpager_api.api_get` to
# a fixture mock, and these wrappers pick it up. Signatures are identical to the
# driver's so the 22 skills/*/fetch.py call them unchanged.
def parallel_get(calls: list[tuple[str, dict[str, Any]]],
                 max_workers: int = _reads.DEFAULT_PARALLEL_WORKERS
                 ) -> dict[str, dict[str, Any]]:
    """Fan out multiple GET requests in parallel. See kernel.runtime.reads."""
    return _reads.parallel_get(api_get, calls, max_workers=max_workers)


def paginate(path: str, max_pages: int | None = None,
             **params: Any) -> Iterator[dict[str, Any]]:
    """Yield every row across every page of a list endpoint. See kernel.runtime.reads."""
    return _reads.paginate(api_get, path, max_pages=max_pages, **params)
