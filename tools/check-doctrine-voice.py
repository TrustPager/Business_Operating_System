#!/usr/bin/env python3
"""Enforce the doctrine-voice rule: the vocabulary is the system's own.

knowledge/business-method.md carries a hard rule: the owner never hears a
source's coined term or a guru's name — every framework surfaces in plain
language or under the BOS's own names, and source coinages live only in the
doctrine's provenance spots and the research briefs behind it.

This is the gate that enforces it. It scans tracked files for the source
coinages and guru names, and fails with the BOS-native replacement to use
(from the crosswalk in business-method.md §19). Without this check the
crosswalk decays: one pasted phrase at a time, the system drifts back into
sounding like a tribute act instead of itself.

Allowed locations (the provenance spots):
- knowledge/business-method.md (header, §3 label, §19 crosswalk)
- docs/architecture/research/** (the cited research briefs)

Exit codes:
    0 — clean
    2 — at least one coined term found outside the allowed locations

Usage:
    python tools/check-doctrine-voice.py          # scan git-tracked files
    python tools/check-doctrine-voice.py --all    # scan the whole working tree
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Paths where source coinages are allowed: the provenance spots, plus this
# gate's own teeth-test (which plants the banned terms on purpose).
ALLOWED_PREFIXES = (
    "knowledge/business-method.md",
    # Internal architecture records: design docs, plans, and dogfood write-ups are
    # ABOUT the sources they synthesise, so naming one is the record doing its job.
    # Nothing here is read to an owner; the shipped surfaces (knowledge/, skills/,
    # studio/, templates/) are what this gate protects.
    "docs/architecture/",
    "tests/test_doctrine_voice.py",
)

# Each entry: (label, compiled pattern, the BOS-native replacement to suggest).
# Patterns are deliberately precise (case-sensitive title-case or all-caps
# where the plain word is common English) so prose like "Day 1 magic" or
# "come closer" never false-positives.
COINED_TERMS: list[tuple[str, re.Pattern[str], str]] = [
    ("Guru name", re.compile(r"\bHormozi\b"),
     "no guru names outside the doctrine's provenance spots"),
    ("Guru brand", re.compile(r"\bAcquisition\.com\b", re.IGNORECASE),
     "no source brands outside the doctrine's provenance spots"),
    ("Guru brand", re.compile(r"\bGym Launch\b"),
     "no source brands outside the doctrine's provenance spots"),
    ("Source book", re.compile(r"\$100M\s+(?:Offers|Leads|Money Models)\b"),
     "no source-book titles outside the doctrine's provenance spots"),
    ("Source author", re.compile(r"\bDunford\b"),
     "no source authors outside the doctrine's provenance spots"),
    ("Source book", re.compile(r"\bObviously Awesome\b"),
     "no source-book titles outside the doctrine's provenance spots"),
    ("Source author", re.compile(r"\bGerber\b"),
     "no source authors outside the doctrine's provenance spots"),
    ("Source book", re.compile(r"\bE-Myth\b"),
     "no source-book titles outside the doctrine's provenance spots"),
    ("Coined framework", re.compile(r"\bGrand Slam\b"),
     'use "the Category-of-One build" (business-method.md 7.1)'),
    ("Coined framework", re.compile(r"\bMAGIC\b"),
     'use "the five naming parts" (business-method.md 7.5)'),
    ("Coined framework", re.compile(r"\bCLOSER\b"),
     'use "the discovery arc" (business-method.md 12.5)'),
    ("Coined framework", re.compile(r"\bTriple-A\b"),
     'use "the concern loop" described in the discovery arc (12.5)'),
    ("Coined framework", re.compile(r"\bRule of 100\b"),
     'use "the volume floor" (business-method.md 10.2)'),
    ("Coined framework", re.compile(r"\bCore Four\b"),
     'use "the four doors" (business-method.md 10.1)'),
    ("Coined framework", re.compile(r"\bSilent Sixth\b"),
     'use "the standing engine" (business-method.md §4)'),
    ("Coined framework", re.compile(r"\bDelivery Cube\b"),
     'use "the delivery grid" (business-method.md 11.6)'),
    ("Coined framework", re.compile(r"\bFive Horsemen\b"),
     'use "the retention cadence" (business-method.md 11.4)'),
    ("Coined framework", re.compile(r"\bstarving crowd\b", re.IGNORECASE),
     'use "the market gate" (business-method.md 7.0)'),
    ("Coined framework", re.compile(r"\bniche slap\b", re.IGNORECASE),
     'use "the commit rule" (business-method.md 7.0)'),
    ("Coined framework", re.compile(r"\bBAMFAM\b"),
     'say it plainly: "book the next step before the meeting ends"'),
    ("Coined framework", re.compile(r"\bwoman in the red dress\b", re.IGNORECASE),
     'use "the shiny-object rule" (business-method.md 12.7)'),
    ("Coined framework", re.compile(r"\bSeven Deadly (?:Growth )?Sins\b", re.IGNORECASE),
     'use "the seven stuck-points" (business-method.md §3)'),
    ("Coined framework", re.compile(r"\bclient-financed acquisition\b", re.IGNORECASE),
     'use "the self-funding bar" (business-method.md 9.2)'),
    ("Coined variable", re.compile(r"\bDream Outcome\b"),
     'use "the Arrival" (business-method.md §6)'),
    ("Coined variable", re.compile(r"\bPerceived Likelihood\b"),
     'use "the Belief" (business-method.md §6)'),
    ("Coined variable", re.compile(r"\bTime Delay\b"),
     'use "the Wait" (business-method.md §6)'),
    ("Coined variable", re.compile(r"\bEffort & Sacrifice\b"),
     'use "the Work" (business-method.md §6)'),
    ("Source author", re.compile(r"\bKallaway\b"),
     "no source authors outside a labelled provenance line"),
]

# The brand-agnostic surfaces: what an owner's OWN brand fills in. A maintainer or
# vendor brand name here ships someone else's identity to every owner, which is the
# one thing the pack must never do (founder ruling 2026-07-27: BOS ships brand
# agnostic so users can fill it in). Scoped deliberately: the connected TrustPager
# driver, its tooling, the 40-plus skills that declare it, and the publish paths that
# upload to an owner's connected workspace all name it legitimately, and are NOT
# scanned here.
VENDOR_SURFACE_PREFIXES = (
    "studio/thumbnails/src/",
    "studio/social/src/templates/",
    "studio/social/src/data/",
    "studio/cta/src/templates/",
)

# There are no exceptions, and that is the point. The two this gate briefly carved
# out (an OG studio whose every hero depicted a vendor product feature, and a set of
# maintainer post designs inside the social studio) were moved out of the pack on
# 2026-07-28 rather than exempted, so the rule holds everywhere it applies.

VENDOR_NAMES = [
    ("Vendor brand", re.compile(r"\bTrustPager\b")),
    ("Maintainer brand", re.compile(r"\bFinalPiece\b")),
]

# Don't scan binaries or vendored/build dirs (mirrors check-no-secrets.py).
SKIP_EXTS = {".png", ".jpg", ".jpeg", ".ico", ".webp", ".gif", ".pdf", ".pyc",
             ".woff", ".woff2", ".ttf", ".zip", ".gz", ".json"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".worktrees", ".firecrawl",
             ".venv", "venv", ".pytest_cache", "output"}
MAX_BYTES = 2_000_000

# This file defines the patterns it hunts, so it exempts itself.
SELF = Path(__file__).resolve()


# A labelled provenance line is the one place a source may be named: the pack
# credits what it synthesises instead of passing it off as its own. Keyed on the
# explicit label, so it cannot be used to smuggle a name into ordinary prose.
_PROVENANCE_LINE = re.compile(
    r"source note|provenance|synthesi[sz]e|rewritten for|taught by", re.IGNORECASE)


def _is_allowed(rel: str) -> bool:
    rel_posix = rel.replace("\\", "/")
    return any(rel_posix.startswith(prefix) for prefix in ALLOWED_PREFIXES)


def _is_vendor_surface(rel: str) -> bool:
    """True if this path is a brand-agnostic surface an owner's own brand fills."""
    rel_posix = rel.replace("\\", "/")
    return any(rel_posix.startswith(p) for p in VENDOR_SURFACE_PREFIXES)


def _tracked_files() -> list[Path]:
    try:
        out = subprocess.run(["git", "ls-files"], cwd=REPO_ROOT,
                             capture_output=True, text=True, check=True)
        return [REPO_ROOT / p for p in out.stdout.splitlines() if p.strip()]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []


def _all_files() -> list[Path]:
    files: list[Path] = []
    for p in REPO_ROOT.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.relative_to(REPO_ROOT).parts):
            continue
        files.append(p)
    return files


def scan_text(text: str, vendor_surface: bool = False) -> list[tuple[int, str, str]]:
    """Return (line_number, label+match, suggestion) findings for one text.

    A labelled provenance line is exempt from the coined-term scan (crediting a
    source is the point of those lines). When ``vendor_surface`` is set, the
    brand-name scan runs too: on a surface an owner's own brand fills, a vendor or
    maintainer brand is the leak, and no provenance label excuses it.
    """
    findings: list[tuple[int, str, str]] = []
    for i, line in enumerate(text.splitlines(), start=1):
        if not _PROVENANCE_LINE.search(line):
            for label, pat, suggestion in COINED_TERMS:
                m = pat.search(line)
                if m:
                    findings.append((i, f"{label} '{m.group(0)}'", suggestion))
        if vendor_surface:
            for label, pat in VENDOR_NAMES:
                m = pat.search(line)
                if m:
                    findings.append((
                        i, f"{label} '{m.group(0)}'",
                        "this surface ships to every owner and carries THEIR brand: "
                        "use the owner's brand from brand/brand.json, or a neutral "
                        "placeholder",
                    ))
    return findings


def scan(scan_all: bool) -> int:
    files = _all_files() if scan_all else (_tracked_files() or _all_files())
    findings: list[str] = []

    for f in files:
        if f.resolve() == SELF:
            continue
        rel = str(f.relative_to(REPO_ROOT))
        if f.suffix.lower() in SKIP_EXTS:
            continue
        if any(part in SKIP_DIRS for part in Path(rel).parts):
            continue
        if _is_allowed(rel):
            continue
        try:
            if f.stat().st_size > MAX_BYTES:
                continue
            text = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for lineno, what, suggestion in scan_text(text, _is_vendor_surface(rel)):
            findings.append(f"{rel}:{lineno}: {what} -> {suggestion}")

    if findings:
        print(f"FAIL: {len(findings)} doctrine-voice violation(s) — the "
              f"vocabulary is the system's own:\n")
        for fnd in findings:
            print(f"  {fnd}")
        print("\nSource coinages belong only in knowledge/business-method.md's "
              "provenance spots and docs/architecture/research/. Use the BOS "
              "name (crosswalk: business-method.md section 19) and re-run.")
        return 2

    print(f"OK: doctrine voice clean "
          f"({'working tree' if scan_all else 'tracked files'}).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--all", action="store_true",
                        help="Scan the whole working tree, not just git-tracked files")
    args = parser.parse_args()
    return scan(scan_all=args.all)


if __name__ == "__main__":
    sys.exit(main())
