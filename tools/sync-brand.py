#!/usr/bin/env python3
# sync-brand.py
#
# Copies brand assets from BOS/brand/ into each studio's public/ folder.
#
# When to use:
#   - After editing brand/brand.json or replacing brand/logo.png
#   - After running /brand-my-workspace (the skill writes brand/, you run this)
#   - Once on first install if studios don't have logo.png/favicons yet
#
# What it does:
#   - Copies brand/logo.png        -> studio/<each>/public/logo.png
#   - Copies brand/favicon.ico     -> studio/<each>/public/favicon.ico
#   - Copies brand/favicon-16x16.png  -> ...
#   - Copies brand/favicon-32x32.png  -> ...
#   - Copies brand/icon.png        -> studio/<each>/public/apple-touch-icon.png
#   - Copies brand/favicon-192x192.png -> ...android-chrome-192x192.png
#   - Copies brand/favicon-512x512.png -> ...android-chrome-512x512.png
#
# Studios pick up the new assets the next time their dev server serves
# /logo.png or /favicon.ico. Restart the dev server (or hard-refresh the
# tab) after running.
#
# Usage:
#   python tools/sync-brand.py
#   python tools/sync-brand.py --dry-run    # show what WOULD copy
#
# Adding a new studio? Drop it under studio/<name>/, give it a public/
# folder, and run this. It auto-discovers every direct child of studio/.

import shutil
import sys
from pathlib import Path

BOS = Path(__file__).resolve().parent.parent
BRAND = BOS / "brand"
STUDIOS_DIR = BOS / "studio"

# Map source filename in brand/ -> destination filename in studio/<x>/public/.
# Names differ because the brand/ folder uses clean naming while studios
# follow the standard favicon convention referenced from their index.html.
ASSET_MAP = {
    "logo.png":              "logo.png",
    "favicon.ico":           "favicon.ico",
    "favicon-16x16.png":     "favicon-16x16.png",
    "favicon-32x32.png":     "favicon-32x32.png",
    "icon.png":              "apple-touch-icon.png",
    "favicon-192x192.png":   "android-chrome-192x192.png",
    "favicon-512x512.png":   "android-chrome-512x512.png",
}

def main():
    dry_run = "--dry-run" in sys.argv

    if not BRAND.is_dir():
        print(f"ERROR: brand/ folder not found at {BRAND}", file=sys.stderr)
        return 1

    missing = [src for src in ASSET_MAP if not (BRAND / src).is_file()]
    if missing:
        print(f"ERROR: missing brand assets: {missing}", file=sys.stderr)
        print(f"Expected location: {BRAND}", file=sys.stderr)
        return 1

    if not STUDIOS_DIR.is_dir():
        print(f"No studios directory at {STUDIOS_DIR} -- nothing to sync.", file=sys.stderr)
        return 0

    studios = [s for s in STUDIOS_DIR.iterdir() if s.is_dir() and (s / "public").is_dir()]
    if not studios:
        print(f"No studios with public/ found under {STUDIOS_DIR}.")
        return 0

    print(f"Syncing brand assets from {BRAND}")
    print(f"Target studios: {[s.name for s in studios]}")
    if dry_run:
        print("(dry-run -- no files will be written)")
    print()

    copied = 0
    for studio in studios:
        public = studio / "public"
        print(f"-> studio/{studio.name}/public/")
        for src_name, dst_name in ASSET_MAP.items():
            src = BRAND / src_name
            dst = public / dst_name
            if dry_run:
                print(f"    {src_name}  ->  {dst_name}")
            else:
                shutil.copy2(src, dst)
                print(f"    [OK] {dst_name}")
                copied += 1
        print()

    print(f"Done. {copied} files copied across {len(studios)} studio(s).")
    print()
    print("Next: restart any running studio dev servers, or hard-refresh tabs")
    print("(browsers cache favicons aggressively).")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
