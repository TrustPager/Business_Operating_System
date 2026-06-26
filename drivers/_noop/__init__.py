"""No-op driver — a SECOND driver built on the kernel with NO TrustPager.

This driver exists to prove the kernel/driver boundary: it wires the
vendor-neutral kernel (kernel.runtime.*) exactly the way a real driver does —
its own DriverConfig describing a fake vendor, and a journaled write issued
THROUGH the kernel transport — while importing nothing from drivers.trustpager,
nothing from tools/, nothing with "trustpager" in it.

tests/test_driver_boundary.py (THE P0 GATE) imports this module fresh and
asserts (1) the write journals through the kernel exactly once and (2) no
TrustPager module is pulled into sys.modules. If building this driver ever
required something from the TrustPager side, that would be a real finding that
the split is incomplete — not something to work around.

Imports ONLY from kernel.runtime.* and stdlib.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

# Put the repo root on sys.path so `import kernel.runtime.*` resolves regardless
# of how this driver was reached (mirrors how a real driver bootstraps).
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from kernel.runtime import journal as _journal  # noqa: E402
from kernel.runtime import transport as _transport  # noqa: E402
from kernel.runtime.transport import DriverConfig  # noqa: E402

# The single no-op DriverConfig. A fabricated, never-resolvable vendor: the base
# URL is RFC-6761 reserved (.invalid never resolves), and the key resolver reads
# a throwaway env var. Constructing it registers the noop_ secret pattern via
# DriverConfig.__post_init__ — same arming path a real driver uses.
NOOP_CFG = DriverConfig(
    base_url="https://example.invalid",
    key_resolver=lambda: os.environ.get("NOOP_KEY", "noop"),
    secret_pattern=r"noop_[a-z0-9]+",
    error_map={},
    approval_url="https://example.invalid/approvals",
)


def write_ping(body: dict) -> Any:
    """Issue a JOURNALED write THROUGH the kernel — the real driver's pattern.

    The write is wrapped in kernel.runtime.journal.journaled so the outcome lands
    in the kernel's audit trail, and the underlying call routes through
    kernel.runtime.transport.request (which goes through the monkeypatchable
    transport._http). No vendor-specific code is involved.
    """
    return _journal.journaled(
        "POST", "ping", body,
        lambda: _transport.request(NOOP_CFG, "POST", "ping", body=body),
    )


__all__ = ["NOOP_CFG", "write_ping"]
