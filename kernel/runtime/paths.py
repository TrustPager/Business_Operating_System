"""Install-root path resolution for the BOS kernel.

ONE reliable way to find the BOS install root, so skills and the kernel can
locate tools/, the shipped registry, etc. regardless of where BOS was cloned.
The supported install is the "easy" clone + setup.py path (there is no plugin
marketplace path), so the anchor is the repo's own structure, not a plugin
manifest.

Resolution order (first hit wins):
    1. $CLAUDE_PLUGIN_ROOT — kept as a harmless override hook (e.g. a symlinked
       or relocated install can point resolution at the true root). Normally
       unset.
    2. Walk upward from this module's location until a directory that looks like
       the BOS root is found: it contains both tools/ and kernel/ (the
       clone-install / dev case).
    3. Fall back to the repo root (two levels up from this file: kernel/runtime
       -> kernel -> repo), so callers always get a Path, never an exception.

How tools import this
---------------------
A standalone script in tools/ shelled directly by Claude cannot use
``import kernel.runtime.paths`` without the repo root on sys.path. Use this
bootstrap idiom at the top of every such script:

    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
    from kernel.runtime.paths import plugin_root

After that, ``plugin_root()``, ``tool_path()``, and ``data_path()`` are all
available for locating sibling tools or bundled data files.
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
        if (candidate / "tools").is_dir() and (candidate / "kernel").is_dir():
            return candidate

    # Fallback: the repo root relative to this file's known location.
    return here.parents[2]


def tool_path(name: str) -> Path:
    """Return the absolute path to a named script inside the tools/ directory.

    Example:
        tool_path("check-no-secrets.py")  ->  <root>/tools/check-no-secrets.py
    """
    return plugin_root() / "tools" / name


def data_path(*parts: str) -> Path:
    """Return an absolute path rooted at plugin_root(), joining *parts*.

    Example:
        data_path("registry", "skills.json")  ->  <root>/registry/skills.json
    """
    return plugin_root().joinpath(*parts)
