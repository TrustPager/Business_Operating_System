#!/usr/bin/env python3
"""Show or clear the stored TrustPager API config (key + cache).

When to use:
- "Where is my API key stored?"
- "What key is BOS using right now?"
- "I want to remove the stored key (e.g. moving machines, key rotated)."
- "Clear the catalog cache so it re-fetches fresh."

What it does:
- Without args: prints config file path, masked key, catalog cache location,
  cache age. Nothing destructive.
- --clear-key: deletes the stored API key from ~/.claude/bos.json.
- --clear-cache: deletes the catalog cache so the next call re-fetches.
- --clear-all: both of the above.

Usage:
    python tools/config.py
    python tools/config.py --clear-key
    python tools/config.py --clear-cache
    python tools/config.py --clear-all

Note: this only manages the LOCAL config. Your TrustPager API key itself
lives in your TrustPager workspace and is unchanged. To rotate the key
itself, do it at https://app.trustpager.com/settings/api then re-run setup.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trustpager_api import CATALOG_CACHE_PATH, CONFIG_PATH  # noqa: E402


def _show() -> int:
    print("TrustPager local config")
    print()
    print(f"Config file:  {CONFIG_PATH}")
    if CONFIG_PATH.exists():
        try:
            cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            key = (cfg.get("api_key") or "").strip()
            if key:
                masked = key[:14] + "..." + key[-4:] if len(key) > 20 else "(too short)"
                print(f"  API key:    {masked}")
            else:
                print("  API key:    (empty)")
        except (json.JSONDecodeError, OSError) as e:
            print(f"  API key:    (unreadable: {e})")
    else:
        print("  API key:    (not configured — run `python tools/setup.py`)")
    print()
    print(f"Catalog cache: {CATALOG_CACHE_PATH}")
    if CATALOG_CACHE_PATH.exists():
        mtime = datetime.fromtimestamp(CATALOG_CACHE_PATH.stat().st_mtime, tz=timezone.utc)
        age = datetime.now(timezone.utc) - mtime
        hours = age.total_seconds() / 3600
        print(f"  Last fetched: {mtime.isoformat()}  ({hours:.1f}h ago)")
    else:
        print("  Last fetched: (no cache yet)")
    print()
    print(f"Environment override: TRUSTPAGER_API_KEY = "
          + ("(set — overrides config file)"
             if _env_key_set() else "(not set)"))
    return 0


def _env_key_set() -> bool:
    import os
    return bool(os.environ.get("TRUSTPAGER_API_KEY"))


def _clear_key() -> int:
    if not CONFIG_PATH.exists():
        print(f"No config file at {CONFIG_PATH} — nothing to clear.")
        return 0
    CONFIG_PATH.unlink()
    print(f"Removed {CONFIG_PATH}")
    return 0


def _clear_cache() -> int:
    if not CATALOG_CACHE_PATH.exists():
        print(f"No catalog cache at {CATALOG_CACHE_PATH} — nothing to clear.")
        return 0
    CATALOG_CACHE_PATH.unlink()
    print(f"Removed {CATALOG_CACHE_PATH}")
    print("The next API call will re-fetch the catalog from docs.trustpager.com.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--clear-key", action="store_true",
                        help="Delete the stored TrustPager API key")
    parser.add_argument("--clear-cache", action="store_true",
                        help="Delete the cached API catalog (forces a re-fetch)")
    parser.add_argument("--clear-all", action="store_true",
                        help="Delete both the key and the catalog cache")
    args = parser.parse_args()

    if args.clear_all or args.clear_key:
        _clear_key()
    if args.clear_all or args.clear_cache:
        _clear_cache()
    if not (args.clear_key or args.clear_cache or args.clear_all):
        return _show()
    return 0


if __name__ == "__main__":
    sys.exit(main())
