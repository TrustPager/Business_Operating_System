"""TrustPager auth + vendor identity — key resolution, secret shape, messages.

Everything here is TrustPager-specific and arrives at the kernel through the
DriverConfig built in drivers/trustpager/__init__.py:
  - get_api_key(): resolves the bearer token (env var, then ~/.claude/bos.json)
  - TP_SECRET_PATTERN: the key shape the redaction registry masks
  - TP_ERROR_MAP: per-HTTP-code, user-facing message templates
  - APPROVAL_URL: where the operator approves a queued (202) write

Imports only from kernel.runtime.* and stdlib — never from tools/.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# Callers (skills) only add tools/ to sys.path. Put the repo root (this file's
# drivers/ parent's parent) on the path first so `import kernel.runtime.*`
# resolves regardless of how the driver was reached.
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from kernel.runtime.errors import BOSError  # noqa: E402

# Where the installer writes the key. Read by get_api_key(); also re-exported
# through trustpager_api for tools/config.py and tools/setup.py.
CONFIG_PATH = Path.home() / ".claude" / "bos.json"

# 202 approve-here page. Surfaced on ApprovalPending so the operator knows where
# to go. Lives here (vendor identity) and is handed to the kernel via TP_CFG.
APPROVAL_URL = "https://app.trustpager.com/settings/api?tab=approvals"

# The vendor key shape the redaction registry masks. Matches a REAL key (a long
# token after the prefix), NOT the bare prefix that appears in docs/error
# messages. Registered with the kernel registry when TP_CFG is constructed
# (DriverConfig.__post_init__). The repo scanner keeps its own copy of this
# shape (tools/check-no-secrets.py, SECRET_PATTERNS) — change both together.
TP_SECRET_PATTERN = r"tp_(?:live|test)_[A-Za-z0-9_\-]{16,}"

# Per-code, user-facing messages. {path}/{url}/{detail}/{available} are filled
# by the kernel's _format_http_error. Retry/backoff for 429/5xx lives in the
# kernel transport; these templates are only used once retries are exhausted.
# The "5xx" string key is the kernel's band sentinel — it covers any 500-599
# code that has no exact-code entry (see kernel.runtime.transport).
TP_ERROR_MAP: dict[int | str, str] = {
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
    429: (
        "Rate-limited by TrustPager (429) on {path} after retries.\n"
        "Slow the request rate, or contact support to raise your limit.\n"
        "Server said: {detail}"
    ),
    # "5xx" band sentinel — used for any 500-599 code (the kernel falls back to
    # this when there's no exact-code entry).
    "5xx": (
        "TrustPager returned a server error ({code}) for {path}.\n"
        "This is usually temporary; try again shortly.\n"
        "If it persists, check status or contact support: "
        "https://app.trustpager.com/settings/api\n"
        "Server said: {detail}"
    ),
}


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
