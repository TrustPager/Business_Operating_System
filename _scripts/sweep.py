"""Business Operating System — Private Data Sweep

Scans every text file in the repository for patterns that should never reach a
public repo: secrets, internal UUIDs, personal contact info, internal
infrastructure paths, named customer references, and FinalPiece-internal
persona names.

Usage:
    python _scripts/sweep.py                    # scan whole repo, exit non-zero on any match
    python _scripts/sweep.py path/to/file       # scan a single file or directory
    python _scripts/sweep.py --staging          # scan only _staging/ (work-in-progress)
    python _scripts/sweep.py --quiet            # report only summary, not per-line matches

Exit codes:
    0 = clean (or only INFO-level findings)
    1 = WARN-level findings present (review needed)
    2 = FAIL-level findings present (must fix before publish)

Add to pre-push hook to make this a hard gate on the public repo.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# =============================================================================
# Deny-list — every pattern has a severity:
#   FAIL  must not appear in published files; sweep exits 2
#   WARN  almost certainly should be removed; sweep exits 1
#   INFO  context-dependent; reviewer's call
# =============================================================================


@dataclass(frozen=True)
class Pattern:
    name: str
    severity: str          # 'FAIL' | 'WARN' | 'INFO'
    regex: re.Pattern
    replacement_hint: str  # what to substitute when fixing


# Compile once at module load.
def _p(name: str, severity: str, pattern: str, replacement: str, flags: int = 0) -> Pattern:
    return Pattern(name, severity, re.compile(pattern, flags), replacement)


PATTERNS: list[Pattern] = [
    # -------------------------------------------------------------------------
    # SECRETS — auto-fail.
    # -------------------------------------------------------------------------
    _p("TrustPager API key", "FAIL", r"tp_live_[A-Za-z0-9_]{8,}", "(redacted — use placeholder tp_live_YOUR_KEY)"),
    _p("TrustPager OAuth token", "FAIL", r"tp_oauth_[A-Za-z0-9_]{8,}", "(redacted)"),
    _p("Supabase secret key", "FAIL", r"sb_secret_[A-Za-z0-9_]{8,}", "(redacted)"),
    _p("Stripe live key", "FAIL", r"sk_live_[A-Za-z0-9]{8,}", "(redacted)"),
    _p("Stripe test key", "FAIL", r"sk_test_[A-Za-z0-9]{8,}", "(redacted)"),
    _p("Slack bot token", "FAIL", r"xoxb-[A-Za-z0-9\-]{8,}", "(redacted)"),
    _p("GitHub PAT", "FAIL", r"ghp_[A-Za-z0-9]{8,}", "(redacted)"),
    _p("JWT-shaped token", "WARN", r"eyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}", "(redacted — verify if JWT)"),

    # -------------------------------------------------------------------------
    # KNOWN INTERNAL UUIDs — auto-fail.
    # -------------------------------------------------------------------------
    # Pattern split via concatenation so this script file doesn't itself
    # contain the literal company_id as a single contiguous string. The
    # compiled regex still matches the live UUID anywhere it leaks into
    # repo content.
    _p("FinalPiece company_id", "FAIL", r"[uuid]" + "-0000-0000-0000-" + "000000000001", "{{your_company_id}}"),
    _p("Demo Company company_id", "FAIL", r"[uuid]", "(omit — internal test workspace)"),
    _p("Operator user_id (internal)", "FAIL", r"[uuid]", "{{your_user_id}}"),
    _p("Internal persona user_id", "FAIL", r"[uuid]", "(omit)"),

    # -------------------------------------------------------------------------
    # PERSONAL CONTACT INFO — auto-fail.
    # -------------------------------------------------------------------------
    _p("Personal Gmail", "FAIL", r"s\.k[a-z]+@gmail\.com", "you@yourdomain.com", re.IGNORECASE),
    _p("FinalPiece work email", "FAIL", r"\b[a-z][a-z\.]+@finalpiece\.ai\b", "you@yourdomain.com", re.IGNORECASE),
    _p("Test pool emails", "FAIL", r"test\d+@finalpiece\.ai", "(omit)", re.IGNORECASE),
    _p("Operator surname", "FAIL", r"\b[name]\b", "(omit)", re.IGNORECASE),
    _p("AU phone E.164", "FAIL", r"\0400 000 000", "+61 4XX XXX XXX"),
    _p("AU phone local", "FAIL", r"\b0431\s?377\s?068\b", "0400 000 000"),

    # -------------------------------------------------------------------------
    # INTERNAL INFRASTRUCTURE — warn (some may be intentional).
    # -------------------------------------------------------------------------
    _p("Windows dev path", "WARN", r"[Dd]:[\\/]Dev[\\/]", "~/your-project/"),
    _p("Windows user path", "FAIL", r"C:[\\/]Users[\\/][A-Za-z0-9_\-]+[\\/]", "~/"),
    _p("EVE hostname", "FAIL", r"eve\.[internal-host]\.net", "(omit — internal infra)"),
    _p("Supabase project ref", "FAIL", r"[project-ref]", "<your-supabase-project>"),
    _p("Keys manifest filename", "FAIL", r"\.trustpager-keys\.json", "(omit)"),
    _p("Internal .net subdomains", "WARN", r"\b([internal]|fulfillment|fulfilment|operations)\.trustpager\.net", "(omit — internal infra)"),
    _p("Cloudflare tunnel id", "WARN", r"\b[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\b", "(verify — looks like UUID)"),

    # -------------------------------------------------------------------------
    # INTERNAL PERSONA NAMES — warn (context matters — "Adam" inside SKILL.md
    # for the BOS sidekick persona is fine; "Adam wrote this" attributing the
    # FinalPiece engineering assistant is not).
    # -------------------------------------------------------------------------
    _p("Operator first name", "WARN", r"(?<![A-Za-z])Simon(?![A-Za-z])", "you / the operator"),
    _p("Internal name ([name])", "FAIL", r"[name]", "(omit)"),
    _p("Internal codename [internal]", "FAIL", r"\b[internal]\b", "(omit)"),
    _p("Internal codename [internal]", "FAIL", r"\b[internal]\b", "(omit)"),
    _p("Internal sales-agent name", "WARN", r"(?<![A-Za-z])Evan(?![A-Za-z])", "(verify — internal persona name)"),
    _p("Internal support-agent name", "WARN", r"(?<![A-Za-z])Evie(?![A-Za-z])", "(verify — internal persona name)"),
    _p("Team member (Vic)", "WARN", r"(?<![A-Za-z])Vic(?![A-Za-z])", "(omit — internal team member)"),
    _p("Team member (Jonathan)", "WARN", r"(?<![A-Za-z])Jonathan(?![A-Za-z])", "(omit — internal team member)"),
    _p("Team member (Cesar)", "WARN", r"(?<![A-Za-z])Cesar(?![A-Za-z])", "(omit — internal team member)"),
    _p("Team member (Micael)", "WARN", r"(?<![A-Za-z])Micael(?![A-Za-z])", "(omit — internal team member)"),

    # -------------------------------------------------------------------------
    # NAMED CUSTOMER REFERENCES from the marketing synthesis — auto-fail.
    # These are real prospects who did not consent to public attribution.
    # -------------------------------------------------------------------------
    _p("Customer reference", "FAIL", r"\b[client]\b", "(generic)"),
    _p("Customer reference", "FAIL", r"\b[client]\b", "(generic)"),
    _p("Customer reference", "FAIL", r"\b[client]\b", "(generic)"),
    _p("Customer reference", "FAIL", r"\b[client]\b", "(generic)"),
    _p("Customer reference", "FAIL", r"\b[client]\b", "(generic)"),
    _p("Customer reference", "FAIL", r"\b[client]\b", "(generic)"),
    _p("Customer reference", "FAIL", r"\bM&M [Pp]rinting\b", "(generic)"),
    _p("Customer reference", "FAIL", r"\b[client]\b", "(generic)"),
    _p("Customer reference", "FAIL", r"\b[client]\b", "(generic)"),
    _p("Customer reference", "FAIL", r"\b[client]\b", "(generic)"),
    _p("Customer reference", "FAIL", r"\b[client]\b", "(generic)"),
    _p("Customer reference", "FAIL", r"\b[client]\b", "(generic)"),
    _p("Customer reference", "FAIL", r"\b[client]\b", "(generic)"),
    _p("Customer reference", "FAIL", r"\b[client]\b", "(generic)"),
    _p("Customer reference", "FAIL", r"\b[client]\b", "(generic)"),
    _p("Customer reference", "FAIL", r"\b(Blu Ray|Bluray) Concreting\b", "(generic)"),
    _p("Customer reference", "FAIL", r"\b[client]\b", "(generic)"),
    _p("Customer reference", "FAIL", r"\b[client]\b", "(generic)"),
    _p("Customer reference", "FAIL", r"\b[client]\b", "(generic)"),

    _p("Customer personal name", "FAIL", r"\b[name]\b", "(generic)"),
    _p("Customer personal name", "FAIL", r"\b[name]\b", "(generic)"),
    _p("Customer personal name", "FAIL", r"\b[name]\b", "(generic)"),
    _p("Customer personal name", "FAIL", r"\b[name]\b", "(generic)"),
    _p("Customer personal name", "FAIL", r"\b[name]\b", "(generic)"),
    _p("Customer personal name", "FAIL", r"\b[name]\b", "(generic)"),
    _p("Customer personal name", "FAIL", r"\b[name]\b", "(generic)"),
    _p("Customer personal name", "FAIL", r"\b[name]\b", "(generic)"),
    _p("Customer personal name", "FAIL", r"\b[name]\b", "(generic)"),
    _p("Customer personal name", "FAIL", r"\b[name]\b", "(generic)"),
    _p("Customer personal name", "FAIL", r"\b[name]\b", "(generic)"),
    _p("Customer personal name", "FAIL", r"\b[name]\b", "(generic)"),
    _p("Customer personal name", "FAIL", r"\b[name]\b", "(generic)"),
    _p("Customer personal name", "FAIL", r"\b[name]\b", "(generic)"),
    _p("Customer personal name", "FAIL", r"\b[name]\b", "(generic)"),
    _p("Customer personal name", "FAIL", r"\b[name]\b", "(omit)"),
]


# =============================================================================
# File walking
# =============================================================================

REPO_ROOT = Path(__file__).resolve().parent.parent

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", ".pytest_cache"}
SKIP_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".svg",
    ".pdf", ".zip", ".tar", ".gz",
    ".mp3", ".mp4", ".mov", ".wav",
    ".woff", ".woff2", ".ttf", ".eot",
    ".pyc", ".pyo",
}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB — skip larger files


SELF_PATH = Path(__file__).resolve()


def _should_scan(path: Path, include_staging: bool) -> bool:
    if path.is_dir():
        return False
    # The sweep script itself contains the literal patterns it scans for.
    # Scanning it would always self-flag. Exclude by absolute path.
    if path.resolve() == SELF_PATH:
        return False
    if any(part in SKIP_DIRS for part in path.parts):
        return False
    if not include_staging and "_staging" in path.parts:
        return False
    if path.suffix.lower() in SKIP_EXTENSIONS:
        return False
    try:
        if path.stat().st_size > MAX_FILE_SIZE:
            return False
    except OSError:
        return False
    return True


def _iter_files(root: Path, include_staging: bool):
    if root.is_file():
        if _should_scan(root, include_staging=True):
            yield root
        return
    for path in root.rglob("*"):
        if _should_scan(path, include_staging):
            yield path


# =============================================================================
# Scanning
# =============================================================================


@dataclass
class Finding:
    file: Path
    line: int
    severity: str
    pattern: str
    match: str
    replacement: str
    context: str


def _scan_file(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return findings

    for i, line in enumerate(text.splitlines(), start=1):
        for pat in PATTERNS:
            for m in pat.regex.finditer(line):
                findings.append(Finding(
                    file=path,
                    line=i,
                    severity=pat.severity,
                    pattern=pat.name,
                    match=m.group(0),
                    replacement=pat.replacement_hint,
                    context=line.strip()[:140],
                ))
    return findings


def _scan_repo(root: Path, include_staging: bool) -> list[Finding]:
    all_findings: list[Finding] = []
    for path in _iter_files(root, include_staging):
        all_findings.extend(_scan_file(path))
    return all_findings


# =============================================================================
# Reporting
# =============================================================================


SEVERITY_RANK = {"FAIL": 2, "WARN": 1, "INFO": 0}
SEVERITY_BADGE = {"FAIL": "[FAIL]", "WARN": "[WARN]", "INFO": "[INFO]"}


def _print_report(findings: list[Finding], quiet: bool) -> int:
    if not findings:
        print("Sweep clean — no matches found.")
        return 0

    by_severity: dict[str, list[Finding]] = {"FAIL": [], "WARN": [], "INFO": []}
    for f in findings:
        by_severity[f.severity].append(f)

    worst_rank = max(SEVERITY_RANK[f.severity] for f in findings)

    if not quiet:
        for severity in ("FAIL", "WARN", "INFO"):
            items = by_severity[severity]
            if not items:
                continue
            print(f"\n{SEVERITY_BADGE[severity]} {severity} ({len(items)} match{'es' if len(items) != 1 else ''}):")
            for f in items:
                rel = f.file.relative_to(REPO_ROOT) if f.file.is_relative_to(REPO_ROOT) else f.file
                print(f"  {rel}:{f.line}  [{f.pattern}]")
                print(f"    match: {f.match!r}")
                print(f"    fix:   {f.replacement}")
                print(f"    line:  {f.context}")

    print("\n" + "=" * 60)
    print(f"Summary: {len(by_severity['FAIL'])} FAIL, {len(by_severity['WARN'])} WARN, {len(by_severity['INFO'])} INFO")
    print("=" * 60)

    if worst_rank == 2:
        print("Result: BLOCKED — fix all FAIL matches before publishing.")
        return 2
    if worst_rank == 1:
        print("Result: WARNINGS — review before publishing.")
        return 1
    return 0


# =============================================================================
# CLI
# =============================================================================


def main() -> int:
    parser = argparse.ArgumentParser(description="Sweep the repo for private data.")
    parser.add_argument("path", nargs="?", default=str(REPO_ROOT),
                        help="File or directory to scan (default: repo root)")
    parser.add_argument("--staging", action="store_true",
                        help="Include the _staging/ directory (work-in-progress)")
    parser.add_argument("--quiet", action="store_true",
                        help="Print only the summary, not per-line matches")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        print(f"Error: path does not exist: {root}", file=sys.stderr)
        return 2

    findings = _scan_repo(root, include_staging=args.staging)
    return _print_report(findings, quiet=args.quiet)


if __name__ == "__main__":
    sys.exit(main())
