"""Write journal — an append-only audit trail of every write BOS issues.

Reads are never journaled. Best-effort: a journaling failure never breaks the
underlying write. Disable with BOS_JOURNAL=0.

Vendor-neutral: the journal records method/path/status/ids only and runs every
value through redact() before it touches disk, so a key can never land here.
The journal directory is a parameter (default JOURNAL_DIR) so callers/tests can
point it elsewhere.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Callable

from kernel.runtime.errors import BOSError
from kernel.runtime.helpers import now_utc
from kernel.runtime.redaction import redact

# Default audit-trail location. Vendor-neutral path under the user's home.
JOURNAL_DIR = Path.home() / ".claude" / "bos-journal"


def _journaling_disabled() -> bool:
    return os.environ.get("BOS_JOURNAL", "1").strip().lower() in {"0", "false", "no", "off"}


def record_write(method: str, path: str, body: dict[str, Any] | None, *,
                 status: str, result_id: str | None = None,
                 approval_id: str | None = None, error: str | None = None,
                 journal_dir: Path | None = None) -> None:
    """Append one write-attempt line to today's journal file. Never raises."""
    if _journaling_disabled():
        return
    target = journal_dir if journal_dir is not None else JOURNAL_DIR
    try:
        target.mkdir(parents=True, exist_ok=True)
        body_summary: str | None = None
        if body is not None:
            try:
                body_summary = json.dumps(body, default=str)[:1000]
            except (TypeError, ValueError):
                body_summary = str(body)[:1000]
        # Redact any secret token before it touches disk — a write body should
        # never carry a key, but if one ever did, it must not land in the journal.
        entry = {
            "ts": now_utc().isoformat(),
            "method": method,
            "path": path,
            "status": status,
            "result_id": result_id,
            "approval_id": approval_id,
            "error": redact(error[:300]) if error else None,
            "body_summary": redact(body_summary),
        }
        day = now_utc().strftime("%Y-%m-%d")
        with (target / f"{day}.jsonl").open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, default=str) + "\n")
    except Exception:  # noqa: BLE001 — journaling must never break a real write
        pass


def journaled(method: str, path: str, body: dict[str, Any] | None,
              fn: Callable[[], Any],
              *, approval_cls: type | None = None,
              journal_dir: Path | None = None) -> Any:
    """Run a write callable, journal the outcome (ok / approval_pending / error).

    `approval_cls` is the type that signals "queued for approval" (the caller's
    ApprovalPending). When the callable returns an instance of it, the journal
    records status=approval_pending with the approval_id. Kept as a parameter so
    the journal stays decoupled from the transport module.
    """
    try:
        result = fn()
    except BOSError as e:
        record_write(method, path, body, status="error", error=str(e),
                     journal_dir=journal_dir)
        raise
    if approval_cls is not None and isinstance(result, approval_cls):
        record_write(method, path, body, status="approval_pending",
                     approval_id=getattr(result, "approval_id", None),
                     journal_dir=journal_dir)
    else:
        result_id = None
        if isinstance(result, dict):
            data = result.get("data", result)
            if isinstance(data, dict):
                result_id = data.get("id")
        record_write(method, path, body, status="ok", result_id=result_id,
                     journal_dir=journal_dir)
    return result
