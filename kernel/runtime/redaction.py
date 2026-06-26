"""Secret redaction — a vendor-neutral registry of patterns to mask.

The kernel knows nothing about any specific credential shape. It ships with an
EMPTY registry. Callers register the patterns they care about:

    from kernel.runtime.redaction import register_secret_pattern, redact

    register_secret_pattern(r"sekret_[A-Za-z0-9]{16,}")
    redact("oops sekret_AbC...")  # -> "oops sekret_***REDACTED***" ... no:
                                  #    -> "oops ***REDACTED***"

`redact(text)` runs every registered pattern over the text and replaces each
match with a fixed placeholder. It is best-effort: it never raises, and falsy
input passes straight through.

Vendor patterns (e.g. a specific key prefix) register from OUTSIDE the kernel
— that keeps the kernel free of any vendor literal.
"""

from __future__ import annotations

import re

PLACEHOLDER = "***REDACTED***"

# The live registry. Empty by default — callers populate it. We store the
# source string alongside the compiled pattern so duplicate registrations are
# idempotent (registering the same regex twice is a no-op).
_PATTERNS: list[tuple[str, re.Pattern[str]]] = []


def register_secret_pattern(regex: str) -> None:
    """Register a regex whose matches redact() will mask.

    Idempotent: registering the same pattern string twice has no extra effect.
    Invalid regexes raise re.error at registration time (fail fast, not at
    redact time).
    """
    for existing_src, _ in _PATTERNS:
        if existing_src == regex:
            return
    _PATTERNS.append((regex, re.compile(regex)))


def redact(text: str | None) -> str | None:
    """Mask every registered secret pattern in `text`. Best-effort, never raises.

    Falsy input (None, "") is returned unchanged. If nothing is registered,
    the text is returned unchanged.
    """
    if not text:
        return text
    try:
        out = text
        for _, pat in _PATTERNS:
            out = pat.sub(PLACEHOLDER, out)
        return out
    except Exception:  # noqa: BLE001 — redaction must never break a caller
        return text


# --- Test/maintenance hooks. Not part of the public surface. ----------------

def _snapshot_patterns() -> list[tuple[str, re.Pattern[str]]]:
    """Return a shallow copy of the registry (for save/restore in tests)."""
    return list(_PATTERNS)


def _reset_patterns() -> None:
    """Clear the registry. Used by tests to isolate registration state."""
    _PATTERNS.clear()


def _restore_patterns(saved: list[tuple[str, re.Pattern[str]]]) -> None:
    """Restore a previously snapshotted registry."""
    _PATTERNS.clear()
    _PATTERNS.extend(saved)
