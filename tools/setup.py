#!/usr/bin/env python3
"""Set up TrustPager API access for Claude Code skills (first-run wizard).

When to use:
- Right after cloning this repo. This is the first thing a customer runs.
- After regenerating your TrustPager API key.
- After running config.py --clear to wipe an old key.

What it does:
- Looks for an existing tp_live_* key in Claude Code's MCP config
  (~/.claude/.mcp.json or ~/.claude/settings.json or ~/.claude.json).
- If found, offers to reuse it (no copy-paste needed).
- Otherwise, prompts you to paste your tp_live_... key.
- Writes the key (and this clone's location, bos_home) to ~/.claude/bos.json.
- Writes a tiny launcher shim to ~/.claude/bos-run.py so skills can run their
  data-fetchers from any working directory (`python ~/.claude/bos-run.py <skill>`).
- Registers the keyless hosted firecrawl web-research MCP at user scope so
  every member can research a business from just its name/site on day 0.
- Copies skills and commands into ~/.claude/ so Claude Code discovers them
  automatically (no plugin or marketplace needed).

Usage:
    python tools/setup.py
    python tools/setup.py --force        # overwrite an existing key

Next step after this runs: python tools/check-install.py
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trustpager_api import CONFIG_PATH  # noqa: E402


def _repo_root() -> Path:
    """This clone's root (the dir that contains tools/ and requirements.txt)."""
    return Path(__file__).resolve().parent.parent


# The always-needed keyless document stack. Bundled here so a normal install has
# the floor with ZERO manual steps (D11: the BOS does setup, never hands the
# owner a command). These mirror requirements.txt; check-install.py --fix heals
# them later if anything is missing. Installed with the SAME interpreter
# (sys.executable -m pip) so there's no Windows multi-Python mismatch.
_DOC_STACK = [
    "markitdown[docx,pdf,xlsx,pptx]",
    "python-docx",
    "openpyxl",
    "reportlab",
    "pdfplumber",
]


def _install_doc_stack() -> int:
    """Install the bundled keyless document stack via this interpreter's pip.

    Best-effort: a failure here does not abort setup (the key step still runs,
    and check-install.py --fix can heal the doc stack later), but it is reported.
    Returns the pip return code (0 == success).
    """
    req = _repo_root() / "requirements.txt"
    if req.is_file():
        cmd = [sys.executable, "-m", "pip", "install", "-r", str(req)]
    else:
        cmd = [sys.executable, "-m", "pip", "install", *_DOC_STACK]
    print("Setting up the document tools (read/write Word, Excel, PDF). This is")
    print("a one-time install so you never have to touch a command yourself:")
    print(f"  {' '.join(cmd)}")
    try:
        rc = subprocess.run(cmd).returncode
    except OSError as e:
        print(f"  [warn] couldn't run pip ({e}). "
              "You can heal this later with: python tools/check-install.py --fix")
        return 1
    if rc == 0:
        print("  Document tools ready.")
    else:
        print("  [warn] document tools didn't fully install. "
              "Heal it later with: python tools/check-install.py --fix")
    print()
    return rc


# The keyless web-research capability that ships with the floor. The hosted
# firecrawl MCP needs no API key for scrape/search, so a brand-new member can
# research a business from just its name/site on day 0 (the "how did it know"
# beat in start-here). Registered at USER scope (~/.claude.json -> mcpServers),
# which Claude Code trusts by default (no approval prompt) and loads on the next
# session start (the restart the member does anyway). Best-effort, like the doc
# stack: a failure never aborts setup, and the built-in WebSearch/WebFetch still
# work as a fallback.
_FIRECRAWL_NAME = "firecrawl"
_FIRECRAWL_URL = "https://mcp.firecrawl.dev/v2/mcp"
_CLAUDE_JSON = Path.home() / ".claude.json"


def _firecrawl_already_registered() -> bool:
    """True if a user-scope firecrawl MCP server is already configured."""
    if not _CLAUDE_JSON.exists():
        return False
    try:
        data = json.loads(_CLAUDE_JSON.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return False
    servers = data.get("mcpServers")
    return isinstance(servers, dict) and _FIRECRAWL_NAME in servers


def _register_firecrawl_via_cli() -> bool:
    """Register firecrawl with the official CLI (forward-compatible). True on success."""
    claude = shutil.which("claude")
    if not claude:
        return False
    cmd = [claude, "mcp", "add", "--transport", "http", "--scope", "user",
           _FIRECRAWL_NAME, _FIRECRAWL_URL]
    try:
        return subprocess.run(cmd, capture_output=True, text=True).returncode == 0
    except OSError:
        return False


def _register_firecrawl_via_json() -> bool:
    """Merge firecrawl into ~/.claude.json mcpServers, preserving everything else.

    Fallback for when the `claude` CLI isn't on PATH (common on Windows). A full
    JSON round-trip keeps every existing key/value; only the firecrawl entry is
    added. Refuses to write if the existing file can't be parsed, so we never
    clobber a large, important config we couldn't read. Returns True on success.
    """
    data: dict[str, Any] = {}
    if _CLAUDE_JSON.exists():
        try:
            data = json.loads(_CLAUDE_JSON.read_text(encoding="utf-8")) or {}
        except (json.JSONDecodeError, OSError):
            return False
    servers = data.get("mcpServers")
    if not isinstance(servers, dict):
        servers = {}
    servers[_FIRECRAWL_NAME] = {"type": "http", "url": _FIRECRAWL_URL}
    data["mcpServers"] = servers
    try:
        _CLAUDE_JSON.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except OSError:
        return False
    return True


def _register_firecrawl_mcp() -> None:
    """Ensure the keyless firecrawl web-research MCP is registered (user scope).

    Best-effort and idempotent: if firecrawl is already configured we leave it
    untouched; otherwise we try the CLI, then the JSON merge. Never aborts setup.
    """
    if _firecrawl_already_registered():
        print("Web research (firecrawl) already set up. Leaving it as is.")
        print()
        return
    print("Setting up web research so I can look up a business from just its name")
    print("or website (free, no account, no key needed):")
    if _register_firecrawl_via_cli() or _register_firecrawl_via_json():
        print("  Web research ready. It loads when you restart Claude Code.")
    else:
        print("  [warn] couldn't auto-set-up firecrawl web research. The built-in "
              "web search still works; you can add firecrawl later.")
    print()


def _seed_brand(root: Path | None = None) -> None:
    """Seed the owner's brand kit from brand/defaults/ if the live files are missing.

    The live brand files (brand/brand.json, logo, favicons) are gitignored user-data,
    so a fresh clone ships only the neutral defaults under brand/defaults/. Copy any
    missing live file so the studios render and brand-my-workspace has a file to write.

    Never overwrites an existing file, so it is safe on every setup and never clobbers
    a brand the owner already set. This is what lets "git pull" updates never collide
    with someone's branding: the brand they own is untracked, seeded once, then theirs.

    ``root`` defaults to the BOS home; it is a parameter so it can be unit-tested
    against a temp tree.
    """
    root = root or Path(_bos_home())
    defaults = root / "brand" / "defaults"
    if not defaults.is_dir():
        return
    seeded = 0
    for src in sorted(defaults.iterdir()):
        if src.is_file():
            dst = root / "brand" / src.name
            if not dst.exists():
                shutil.copy2(src, dst)
                seeded += 1
    if seeded:
        print(f"Set up your blank-canvas brand ({seeded} file(s)). "
              "Run /brand-my-workspace anytime to make it yours.")
        print()


def _walk_for_key(obj: Any) -> str | None:
    if isinstance(obj, str):
        if obj.startswith("tp_live_") and len(obj) > 20:
            return obj
        return None
    if isinstance(obj, dict):
        for v in obj.values():
            r = _walk_for_key(v)
            if r:
                return r
    if isinstance(obj, list):
        for v in obj:
            r = _walk_for_key(v)
            if r:
                return r
    return None


def _find_key_in_mcp_config() -> str | None:
    """Look for an existing TrustPager API key in Claude Code's MCP config."""
    candidates = [
        Path.home() / ".claude" / ".mcp.json",
        Path.home() / ".claude" / "settings.json",
        Path.home() / ".claude.json",
    ]
    for path in candidates:
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        found = _walk_for_key(data)
        if found:
            return found
    return None


# The fixed-location shim. It lives at ~/.claude/bos-run.py — the one path that
# is known regardless of working directory or how BOS was installed. It reads
# bos_home from bos.json (same dir) and hands off to <bos_home>/tools/run.py,
# which carries the real logic and is versioned in the repo. Keep this DUMB so
# it rarely needs regenerating.
_SHIM_SOURCE = '''#!/usr/bin/env python3
# Auto-generated by Business Operating System setup.py. Do not edit by hand.
# Bootstraps the CWD-independent skill launcher from any working directory.
# Re-run `python tools/setup.py` to regenerate.
import json, subprocess, sys
from pathlib import Path

_cfg = Path.home() / ".claude" / "bos.json"
try:
    _home = json.loads(_cfg.read_text(encoding="utf-8")).get("bos_home")
except (OSError, ValueError):
    _home = None
if not _home:
    sys.stderr.write("[err] bos_home not set. Run: python tools/setup.py\\n")
    sys.exit(2)
_run = Path(_home) / "tools" / "run.py"
if not _run.is_file():
    sys.stderr.write(f"[err] launcher missing at {_run}. Re-run python tools/setup.py\\n")
    sys.exit(2)
# subprocess (not os.execv): execv on Windows splits argv entries containing
# spaces, which breaks install paths like "...\\Final Piece\\...".
sys.exit(subprocess.run([sys.executable, str(_run), *sys.argv[1:]]).returncode)
'''


def _bos_home() -> str:
    """Absolute path to this clone's root (the dir that contains tools/)."""
    return str(Path(__file__).resolve().parent.parent)


def _write_launcher_shim() -> Path:
    shim = CONFIG_PATH.parent / "bos-run.py"
    shim.write_text(_SHIM_SOURCE, encoding="utf-8")
    return shim


def _install_skills(bos_home: str, config_path: Path) -> tuple[int, int]:
    """Copy BOS skills and commands into ~/.claude/ for Claude Code discovery.

    Mechanism: file/directory COPY (not symlink). Symlinks require elevated
    privilege on Windows (Developer Mode or admin), making them unreliable for
    a conversational install. Copying is always available, is cross-OS safe,
    and stays correct on re-runs because we refresh BOS-owned targets in place.
    Re-running setup is the update path, so stale copies self-heal.

    Collision policy: if a target already exists AND was not placed by BOS
    (i.e., its name is not in the recorded installed_skills/installed_commands
    lists), we skip it and print a one-line warning. We never overwrite the
    user's own work.

    Idempotent: running twice does not error or duplicate. If the target exists
    and BOS owns it, we remove-and-recopy to refresh it.

    Recording: installed_skills (list of skill dir names) and
    installed_commands (list of command file basenames, no extension) are
    stored in bos.json so a future uninstall/update can manage only BOS-owned
    entries.

    Returns (n_skills_placed, n_commands_placed).
    """
    home_claude = config_path.parent  # ~/.claude/
    home_claude.mkdir(parents=True, exist_ok=True)

    # Load current bos.json so we know what BOS already owns.
    cfg: dict[str, Any] = {}
    if config_path.exists():
        try:
            cfg = json.loads(config_path.read_text(encoding="utf-8")) or {}
        except (json.JSONDecodeError, OSError):
            cfg = {}

    owned_skills: list[str] = list(cfg.get("installed_skills") or [])
    owned_commands: list[str] = list(cfg.get("installed_commands") or [])

    bos = Path(bos_home)
    skills_placed = 0
    commands_placed = 0

    # --- skills: each <bos_home>/skills/<name>/ containing SKILL.md ---
    src_skills_root = bos / "skills"
    dst_skills_root = home_claude / "skills"
    dst_skills_root.mkdir(exist_ok=True)

    if src_skills_root.is_dir():
        for src_skill in sorted(src_skills_root.iterdir()):
            if not src_skill.is_dir():
                continue
            if not (src_skill / "SKILL.md").exists():
                continue
            name = src_skill.name
            dst = dst_skills_root / name
            if dst.exists() and name not in owned_skills:
                print(f"  [skip] ~/.claude/skills/{name} exists and was not "
                      f"created by BOS; leaving it unchanged.")
                continue
            # BOS owns it (or it does not exist): refresh by replacing.
            if dst.exists():
                print(f"  [refresh] ~/.claude/skills/{name} (BOS-owned; "
                      f"local edits to this copy are replaced)")
                shutil.rmtree(dst)
            shutil.copytree(src_skill, dst)
            if name not in owned_skills:
                owned_skills.append(name)
            skills_placed += 1

    # --- commands: each <bos_home>/commands/<name>.md ---
    src_commands_root = bos / "commands"
    dst_commands_root = home_claude / "commands"
    dst_commands_root.mkdir(exist_ok=True)

    if src_commands_root.is_dir():
        for src_cmd in sorted(src_commands_root.iterdir()):
            if src_cmd.suffix != ".md" or not src_cmd.is_file():
                continue
            stem = src_cmd.stem
            dst = dst_commands_root / src_cmd.name
            if dst.exists() and stem not in owned_commands:
                print(f"  [skip] ~/.claude/commands/{src_cmd.name} exists and "
                      f"was not created by BOS; leaving it unchanged.")
                continue
            # BOS owns it (or it does not exist): write/overwrite.
            shutil.copy2(src_cmd, dst)
            if stem not in owned_commands:
                owned_commands.append(stem)
            commands_placed += 1

    # Persist the updated ownership lists back to bos.json.
    cfg["installed_skills"] = owned_skills
    cfg["installed_commands"] = owned_commands
    config_path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")

    return skills_placed, commands_placed


def _write_key(key: str) -> int:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    # Preserve any existing config keys; just update api_key + bos_home.
    cfg: dict[str, Any] = {}
    if CONFIG_PATH.exists():
        try:
            cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8")) or {}
        except (json.JSONDecodeError, OSError):
            cfg = {}
    cfg["api_key"] = key
    cfg["bos_home"] = _bos_home()
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    print(f"Wrote {CONFIG_PATH}")
    shim = _write_launcher_shim()
    print(f"Wrote {shim}  (skills run via: python ~/.claude/bos-run.py <skill>)")
    n_skills, n_cmds = _install_skills(_bos_home(), CONFIG_PATH)
    print(f"Made {n_skills} skills + {n_cmds} commands discoverable in ~/.claude/")
    print()
    print("Next: run `python tools/check-install.py` to verify everything works.")
    return 0


def _write_keyless() -> int:
    """Finish setup without a TrustPager key.

    Writes bos_home into bos.json and deploys the launcher shim so the
    keyless document floor is fully operational.  No api_key is written.
    """
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    cfg: dict[str, Any] = {}
    if CONFIG_PATH.exists():
        try:
            cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8")) or {}
        except (json.JSONDecodeError, OSError):
            cfg = {}
    cfg["bos_home"] = _bos_home()
    # Do not set or clear api_key; preserve any existing value.
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    shim = _write_launcher_shim()
    print(f"Wrote {shim}  (skills run via: python ~/.claude/bos-run.py <skill>)")
    n_skills, n_cmds = _install_skills(_bos_home(), CONFIG_PATH)
    print(f"Made {n_skills} skills + {n_cmds} commands discoverable in ~/.claude/")
    print()
    print("No key set. The keyless floor is ready to use. "
          "You can connect TrustPager later to unlock the connected features.")
    print()
    print("Next: run `python tools/check-install.py` to verify everything works.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--force", action="store_true",
                        help="Overwrite an existing key without prompting")
    parser.add_argument("--skip-deps", action="store_true",
                        help="Skip installing the bundled document stack")
    args = parser.parse_args()

    print("Business Operating System: first-run setup")
    print()

    # Bundle the always-needed keyless document stack first (D11). This makes the
    # keyless document floor work with zero manual steps. It is independent of any
    # TrustPager key, so a keyless owner gets it too.
    if not args.skip_deps:
        _install_doc_stack()

    # Register the keyless web-research MCP (firecrawl) as part of the floor, for
    # keyed and keyless members alike. Best-effort; runs before the key logic so
    # upgraders (existing-key early-return below) get it too.
    _register_firecrawl_mcp()

    # Seed the owner's blank-canvas brand kit if it isn't there yet. Runs before the
    # key logic so every path (keyless, keyed, upgrader) gets it. Never overwrites.
    _seed_brand()

    print(f"This will write your TrustPager API key to: {CONFIG_PATH}")
    print("(optional: the keyless floor works without it)")
    print()

    existing_key = None
    if CONFIG_PATH.exists() and not args.force:
        try:
            cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            existing_key = (cfg.get("api_key") or "").strip()
        except (json.JSONDecodeError, OSError):
            pass
        if existing_key:
            print(f"A key is already configured (ends ...{existing_key[-4:]}).")
            # Idempotent backfill for upgraders: ensure bos_home + the launcher
            # shim exist even when we're not touching the key.
            if cfg.get("bos_home") != _bos_home():
                cfg["bos_home"] = _bos_home()
                CONFIG_PATH.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
                print(f"Updated bos_home in {CONFIG_PATH}")
            shim = _write_launcher_shim()
            print(f"Ensured launcher shim at {shim}")
            n_skills, n_cmds = _install_skills(_bos_home(), CONFIG_PATH)
            print(f"Made {n_skills} skills + {n_cmds} commands discoverable in ~/.claude/")
            print("Re-run with --force to replace the key, or skip setup entirely.")
            return 0

    detected = _find_key_in_mcp_config()
    if detected:
        print(f"Detected an existing TrustPager API key in Claude Code config")
        print(f"  (ends ...{detected[-4:]}).")
        choice = input("Use this key for skill scripts too? [Y/n] ").strip().lower()
        if choice in ("", "y", "yes"):
            return _write_key(detected)

    print("Get your key from: https://app.trustpager.com/settings/api")
    print()
    key = input("Paste your tp_live_... key (or press Enter to skip): ").strip()
    if not key:
        return _write_keyless()
    if not key.startswith("tp_live_"):
        print(f"WARNING: key doesn't start with 'tp_live_'. Got '{key[:10]}...'",
              file=sys.stderr)
        confirm = input("Use it anyway? [y/N] ").strip().lower()
        if confirm not in ("y", "yes"):
            return 2
    return _write_key(key)


if __name__ == "__main__":
    sys.exit(main())
