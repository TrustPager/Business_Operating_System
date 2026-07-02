#!/usr/bin/env python3
"""Scan the repo for leaked secrets before they get committed or shipped.

The whole testing strategy rests on one rule: a real API key never enters the
repo. This is the gate that enforces it. It scans tracked files (or the working
tree) for things that look like live credentials — TrustPager keys, private-key
blocks, AWS keys, Anthropic keys — and a stray `bos.json`.

It is deliberately precise: it matches a REAL key (a long token after the
prefix), NOT the bare `tp_live_` string that legitimately appears in docs,
error messages, and this scanner. So `README` saying "your key starts with
tp_live_" does not trip it; an actual `tp_live_AbC123...` does.

When to use:
- As a pre-commit hook and in CI (it's wired into .github/workflows/test.yml).
- Any time before you push, especially after editing fixtures or docs.

Exit codes:
    0 — clean
    2 — at least one likely secret found (prints file:line, redacted)

Usage:
    python tools/check-no-secrets.py            # scan git-tracked files
    python tools/check-no-secrets.py --all       # scan the whole working tree
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Each pattern matches an ACTUAL credential, not a bare prefix mentioned in prose.
# This list is deliberately standalone (no imports) so the pre-commit hook runs
# anywhere. The TrustPager shape must stay in sync with TP_SECRET_PATTERN in
# drivers/trustpager/auth.py; when a new driver lands, add its key shape here too.
SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("TrustPager API key", re.compile(r"tp_(?:live|test)_[A-Za-z0-9_\-]{16,}")),
    ("Anthropic API key", re.compile(r"sk-ant-[A-Za-z0-9_\-]{20,}")),
    ("AWS access key id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Private key block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |)?PRIVATE KEY-----")),
    ("Generic bearer secret", re.compile(r"\bsk-[A-Za-z0-9]{32,}\b")),
]

# Don't scan binaries or vendored/build dirs.
SKIP_EXTS = {".png", ".jpg", ".jpeg", ".ico", ".webp", ".gif", ".pdf", ".pyc",
             ".woff", ".woff2", ".ttf", ".zip", ".gz"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", "_staging", "graphify-out",
             ".venv", "venv", ".pytest_cache"}
MAX_BYTES = 2_000_000  # don't read anything huge


def _redact(line: str) -> str:
    out = line
    for _, pat in SECRET_PATTERNS:
        out = pat.sub(lambda m: m.group(0)[:8] + "***REDACTED***", out)
    return out.strip()[:160]


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


def scan(scan_all: bool) -> int:
    files = _all_files() if scan_all else (_tracked_files() or _all_files())
    findings: list[str] = []

    for f in files:
        rel = f.relative_to(REPO_ROOT)
        if f.suffix.lower() in SKIP_EXTS:
            continue
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        # A tracked bos.json is itself a finding — that file holds the key.
        if f.name == "bos.json":
            findings.append(f"{rel}: bos.json must never be committed (it stores your API key)")
            continue
        try:
            if f.stat().st_size > MAX_BYTES:
                continue
            text = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            for label, pat in SECRET_PATTERNS:
                if pat.search(line):
                    findings.append(f"{rel}:{i}: {label} -> {_redact(line)}")

    if findings:
        print(f"FAIL: {len(findings)} possible secret(s) found - do NOT commit:\n")
        for fnd in findings:
            print(f"  {fnd}")
        print("\nRemove the secret, rotate the key if it was real "
              "(https://app.trustpager.com/settings/api), and re-run.")
        return 2

    print(f"OK: no secrets found ({'working tree' if scan_all else 'tracked files'}).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--all", action="store_true",
                        help="Scan the whole working tree, not just git-tracked files")
    args = parser.parse_args()
    return scan(scan_all=args.all)


if __name__ == "__main__":
    sys.exit(main())
