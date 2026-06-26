"""Offline guard — the switch that keeps tests and CI off the network.

When BOS_OFFLINE is set, the transport layer refuses every authenticated
network call and never reads a real API key. Tests and CI run with this on so
no live request can ever fire.
"""

from __future__ import annotations

import os


def is_offline() -> bool:
    """True when BOS_OFFLINE is set — tests/CI run with this on so no network
    call can ever fire and no real API key is ever read."""
    return os.environ.get("BOS_OFFLINE", "").strip().lower() in {"1", "true", "yes", "on"}
