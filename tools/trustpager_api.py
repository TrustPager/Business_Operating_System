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

import sys
from pathlib import Path
from typing import Any, Callable, Iterator

# --- Kernel re-exports -------------------------------------------------------
# The vendor-neutral primitives now live in kernel/runtime/. They were lifted
# out of this module (P0 Task 1). We re-import them here so every existing
# caller and all the skill fetch.py scripts keep importing them unchanged
# `from trustpager_api import BOSError, now_utc, ...`.
#
# Callers only add tools/ to sys.path, so put the repo root (tools/'s parent)
# on the path first to make `import kernel.runtime.*` and `import drivers.*`
# resolve.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from kernel.runtime.errors import BOSError  # noqa: E402,F401  (re-exported)
from kernel.runtime.offline import is_offline  # noqa: E402
from kernel.runtime.redaction import redact  # noqa: E402
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
from kernel.runtime.transport import (  # noqa: E402,F401
    DriverConfig,
    ApprovalPending as _KernelApprovalPending,
)

# --- TrustPager driver re-exports --------------------------------------------
# The vendor-specific config, auth, catalog and bound api_* now live in
# drivers/trustpager (P0 Task 3). We re-import them here so every existing
# caller and all the skill fetch.py scripts keep importing them unchanged
# `from trustpager_api import api_get, resolve_path, ApprovalPending, ...`.
#
# Importing drivers.trustpager constructs TP_CFG, whose DriverConfig.__post_init__
# registers the tp_ secret pattern — this is now the SOLE registration point
# (the interim duplicate that used to live here is gone).
from drivers.trustpager import (  # noqa: E402,F401  (re-exported)
    TP_CFG,
    ApprovalPending,
    api_get,
    api_patch,
    api_post,
    idempotent_post,
    get_api_key,
    get_catalog,
    inspect_endpoint,
    resolve_path,
    api_call_by_resource,
    API_BASE,
    CATALOG_URL,
    CATALOG_CACHE_PATH,
    CONFIG_PATH,
    APPROVAL_URL,
)
from drivers.trustpager.auth import TP_SECRET_PATTERN  # noqa: E402,F401  (re-exported)

# Backwards-compatible aliases for the semi-private names callers/tests still
# use (e.g. tests/test_safety.py references _redact and _is_offline). Keep
# these working so the existing suite passes unchanged.
_is_offline = is_offline
_redact = redact

DEFAULT_PARALLEL_WORKERS = 8

# Write audit trail (see tools/journal.py). The journal wrappers below pass this
# explicitly so tests that reassign trustpager_api.JOURNAL_DIR keep redirecting
# the journal. Kept module-level here (not in the driver) for that test seam.
JOURNAL_DIR = Path.home() / ".claude" / "bos-journal"


# =============================================================================
# Write journal — every write BOS issues is appended to ~/.claude/bos-journal.
# Reads are never journaled. Best-effort: journaling failures never break the
# write. Disable with BOS_JOURNAL=0. The mechanism lives in
# kernel/runtime/journal.py; these thin wrappers bind it to JOURNAL_DIR (which
# tests reassign) and the kernel ApprovalPending type.
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


# =============================================================================
# Scaled reads/writes — bound wrappers over kernel.runtime.reads.
#
# The mechanism (fan-out, pagination, bulk) is vendor-neutral in the kernel and
# takes the bound get/write callable as its first argument. These wrappers keep
# the SAME signatures the 22 skill fetch.py scripts already call:
#     parallel_get([(path, params), ...])
#     paginate(path, limit=100, max_pages=N)
#     bulk_apply(write_fn, items, ...)
# They look api_get up at call time (via THIS module's globals — the re-exported
# driver api_get) so tools/test-skill.py, which monkeypatches
# trustpager_api.api_get, is still observed.
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
