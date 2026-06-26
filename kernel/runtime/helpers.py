"""Vendor-neutral helpers shared by tools and skill scripts.

Pure stdlib. Nothing here knows about any specific API vendor:

    - Date parsing/maths: now_utc, parse_iso, days_since
    - List digests:       group_count, top_n_by
    - Logging:            log
    - Output emitters:    force_utf8_stdout, emit_json, emit_error_and_exit
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from typing import Any


# =============================================================================
# Date helpers — shared parsing for ISO timestamps and date-only strings
# =============================================================================
#
# APIs commonly return dates in three shapes:
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
# Logging — shared `log` for skill scripts (replaces per-skill helpers)
# =============================================================================


def log(prefix: str, msg: str, *, quiet: bool = False) -> None:
    """Write a one-line progress message to stderr with a [prefix] tag.

    Skills should use this instead of redefining their own _log function:

        from kernel.runtime.helpers import log
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


def force_utf8_stdout() -> None:
    """Reconfigure stdout (and stderr) to UTF-8 with replace-on-error.

    Windows terminals default to cp1252 which can't encode emojis or many
    non-ASCII characters. Any tool that prints emojis to stdout should call
    this once at the top of main() so it works cross-platform.

    Safe to call multiple times. No-op on terminals that already speak UTF-8.
    """
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except (AttributeError, ValueError):
                pass


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
