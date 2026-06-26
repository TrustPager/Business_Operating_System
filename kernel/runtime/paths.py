"""Plugin path resolution for the BOS kernel.

ONE reliable way to find the plugin root, so skills and the kernel can locate
tools/, the shipped registry, etc. regardless of how BOS was installed.

Resolution order (first hit wins):
    1. $CLAUDE_PLUGIN_ROOT — the documented Claude Code anchor. Set by the
       loader on a plugin install. Adopted here (it was referenced nowhere in
       the repo before this) so plugin-only installs resolve correctly.
    2. Walk upward from this module's location until a directory containing
       .claude-plugin/ is found (the clone-install / dev case).
    3. Fall back to the repo root (two levels up from this file: kernel/runtime
       -> kernel -> repo), so callers always get a Path, never an exception.
"""

from __future__ import annotations

import os
from pathlib import Path


def plugin_root() -> Path:
    """Return the absolute path to the plugin/repo root.

    See module docstring for the resolution order. Always returns a Path;
    never raises.
    """
    env = os.environ.get("CLAUDE_PLUGIN_ROOT", "").strip()
    if env:
        return Path(env)

    here = Path(__file__).resolve()
    # here.parents = [kernel/runtime, kernel, <repo root>, ...]
    for candidate in here.parents:
        if (candidate / ".claude-plugin").is_dir():
            return candidate

    # Fallback: the repo root relative to this file's known location.
    return here.parents[2]
