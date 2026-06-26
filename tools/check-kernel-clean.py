#!/usr/bin/env python3
"""Enforce the vendor-neutral-kernel invariant: kernel/ names no specific vendor.

The kernel (kernel/runtime/) is the vendor-agnostic core. Every vendor-specific
literal — a real key prefix, the vendor host, the vendor config filename, the
vendor name itself — belongs in a driver (drivers/<vendor>/), never in the
kernel. This is the gate that keeps that boundary honest in CI: if a literal
leaks into the kernel as code is moved around, this fails the build and names
the offending file and line so it can be moved out to a driver.

When to use:
- In CI, immediately after the secret scan (it's wired into
  .github/workflows/test.yml).
- Any time you move code into kernel/, to confirm you didn't drag a vendor
  literal along with it.

What it does:
- Scans every *.py under kernel/ for the case-insensitive pattern
  `tp_(live|test)_|api.trustpager.com|bos.json|trustpager`.
- On any match: prints each offending file:line and exits non-zero.
- If clean: prints an OK line and exits 0.

Exit codes:
    0 — clean (no vendor literals in kernel/)
    2 — at least one vendor literal found (prints file:line)

Usage:
    python tools/check-kernel-clean.py            # scan kernel/ (default)
    python tools/check-kernel-clean.py <dir>      # scan a different directory
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KERNEL_DIR = REPO_ROOT / "kernel"

# Case-insensitive: any of these substrings in a kernel .py file is a leak.
# Kept byte-for-byte in step with tests/test_kernel_vendor_neutral.py and the
# secret scanner's TrustPager prefix.
VENDOR_LITERAL = re.compile(
    r"tp_(?:live|test)_|api\.trustpager\.com|bos\.json|trustpager", re.IGNORECASE
)


def scan_dir(root: Path) -> list[str]:
    """Scan every *.py under `root` for vendor literals.

    Returns a list of "relative/path.py:LINE: <stripped line>" findings, one
    per matching line. Empty list means clean. Importable so the regression
    test can prove the checker has teeth.
    """
    root = Path(root)
    findings: list[str] = []
    for p in sorted(root.rglob("*.py")):
        if not p.is_file():
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        try:
            rel = p.relative_to(root)
        except ValueError:
            rel = p
        for i, line in enumerate(text.splitlines(), start=1):
            if VENDOR_LITERAL.search(line):
                findings.append(f"{rel}:{i}: {line.strip()[:160]}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument(
        "directory",
        nargs="?",
        default=str(KERNEL_DIR),
        help="Directory to scan (default: kernel/)",
    )
    args = parser.parse_args()

    root = Path(args.directory)
    if not root.exists():
        print(f"FAIL: directory does not exist: {root}")
        return 2

    findings = scan_dir(root)
    if findings:
        print(
            f"FAIL: {len(findings)} vendor literal(s) found in {root} - "
            "the kernel must stay vendor-neutral:\n"
        )
        for fnd in findings:
            print(f"  {fnd}")
        print(
            "\nMove the literal out to a driver (drivers/<vendor>/) or register "
            "it from outside the kernel, then re-run."
        )
        return 2

    print(f"OK: no vendor literals in {root} (kernel is vendor-neutral).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
