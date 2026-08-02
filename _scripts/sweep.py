"""Business Operating System — Private Data Sweep

Scans every text file in the repository for patterns that should never reach a
public repo: secrets, internal UUIDs, personal contact info, internal
infrastructure paths, named customer references, and FinalPiece-internal
persona names.

Usage:
    python _scripts/sweep.py                    # scan tracked files, exit non-zero on any match
    python _scripts/sweep.py --fail-only        # report/gate on FAIL only (what CI runs)
    python _scripts/sweep.py path/to/file       # scan a single file or directory
    python _scripts/sweep.py --all              # walk the working tree, not just tracked files
    python _scripts/sweep.py --staging          # include _staging/ (work-in-progress)
    python _scripts/sweep.py --quiet            # report only summary, not per-line matches
    python _scripts/sweep.py --hash "New Name"  # print the deny-list entry for a new identity

This file is tracked in a PUBLIC repo, so the deny list itself must not be a
client list: literal identities live only as SHA-256 hashes (HASHED_IDENTITIES
below). Structural patterns (key shapes, path shapes) stay readable regexes.

Exit codes:
    0 = clean (or only INFO-level findings)
    1 = WARN-level findings present (review needed)
    2 = FAIL-level findings present (must fix before publish)

What CI gates on: `--fail-only`, which suppresses the WARN tier and exits 0
unless a FAIL pattern matched. The WARN tier is deliberately noisy (every
internal first name in the architecture docs trips it) and is a review aid,
not a gate — gating on it would train everyone to ignore the whole check.
Run the plain sweep by hand before a release to read the WARN tier.

Default scope is `git ls-files`, matching tools/check-no-secrets.py: only
what would actually be published can block publishing. An explicit path
argument or --all overrides that.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
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
    # PERSONAL CONTACT INFO — auto-fail. Only patterns that reveal nothing on
    # their own live here; every literal identity (names, UUIDs, phone numbers,
    # hostnames) is in HASHED_IDENTITIES below so this public file never
    # carries the plaintext it exists to keep out.
    # -------------------------------------------------------------------------
    _p("Personal Gmail", "FAIL", r"s\.k[a-z]+@gmail\.com", "you@yourdomain.com", re.IGNORECASE),
    _p("FinalPiece work email", "FAIL", r"\b[a-z][a-z\.]+@finalpiece\.ai\b", "you@yourdomain.com", re.IGNORECASE),
    _p("Test pool emails", "FAIL", r"test\d+@finalpiece\.ai", "(omit)", re.IGNORECASE),

    # -------------------------------------------------------------------------
    # INTERNAL INFRASTRUCTURE — warn (some may be intentional).
    # -------------------------------------------------------------------------
    _p("Windows dev path", "WARN", r"[Dd]:[\\/]Dev[\\/]", "~/your-project/"),
    _p("Windows user path", "FAIL", r"C:[\\/]Users[\\/][A-Za-z0-9_\-]+[\\/]", "~/"),
    _p("Keys manifest filename", "FAIL", r"\.trustpager-keys\.json", "(omit)"),
    _p("Internal .net subdomains", "WARN", r"\b(fulfillment|fulfilment|operations)\.trustpager\.net", "(omit — internal infra)"),
    _p("Cloudflare tunnel id", "WARN", r"\b[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\b", "(verify — looks like UUID)"),

    # -------------------------------------------------------------------------
    # INTERNAL PERSONA NAMES — warn (context matters — "Adam" inside SKILL.md
    # for the BOS sidekick persona is fine; "Adam wrote this" attributing the
    # FinalPiece engineering assistant is not).
    # -------------------------------------------------------------------------
    _p("Operator first name", "WARN", r"(?<![A-Za-z])Simon(?![A-Za-z])", "you / the operator"),
    _p("Internal sales-agent name", "WARN", r"(?<![A-Za-z])Evan(?![A-Za-z])", "(verify — internal persona name)"),
    _p("Internal support-agent name", "WARN", r"(?<![A-Za-z])Evie(?![A-Za-z])", "(verify — internal persona name)"),
    _p("Team member (Vic)", "WARN", r"(?<![A-Za-z])Vic(?![A-Za-z])", "(omit — internal team member)"),
    _p("Team member (Jonathan)", "WARN", r"(?<![A-Za-z])Jonathan(?![A-Za-z])", "(omit — internal team member)"),
    _p("Team member (Cesar)", "WARN", r"(?<![A-Za-z])Cesar(?![A-Za-z])", "(omit — internal team member)"),
    _p("Team member (Micael)", "WARN", r"(?<![A-Za-z])Micael(?![A-Za-z])", "(omit — internal team member)"),

]


# =============================================================================
# HASHED IDENTITIES — auto-fail, all of them.
#
# Real customer business names, real people's names, internal UUIDs, internal
# hostnames, and personal phone numbers. This file is tracked in a PUBLIC
# repo, so the deny list itself must not be a client list: only SHA-256 hashes
# of the normalized identity live here. The scanner hashes candidate strings
# from every line and compares — same detection, nothing to read.
#
# To add one:   python _scripts/sweep.py --hash "The Name Or Identifier"
# and paste the printed entry below. NEVER paste the plaintext into this file,
# a comment, a commit message, or a test.
#
# To remove one: don't. Removing an entry to get a green build defeats the
# check; fix the content instead. Entries only leave this list when the person
# or business has consented to public attribution.
#
# Labels are deliberately anonymous (#N): a label that identifies the person
# would defeat the hashing.
#
# Three normalization channels, matched in _hash_scan_line():
#   words:   lowercase, tokens of [a-z0-9&]+, joined by single spaces —
#            catches names in any casing, hyphenation, or punctuation
#   compact: the identifier lowercased verbatim — UUIDs, hostnames, refs
#   digits:  all non-digits stripped — phone numbers in any formatting
# =============================================================================


def _h(label: str, digest: str) -> tuple[str, str]:
    return (label, digest)


_HASHED_ENTRIES: list[tuple[str, str]] = [
    # words channel — customer business names
    _h("Customer reference #1", "00c7cc2aa6c2103de02a316a4305229563c2ad64cd4c4271b371ce8568c741df"),
    _h("Customer reference #2", "bb0b4632971e175a9167dbf5d64f6ba710985f15e30de2a755822720bafeed27"),
    _h("Customer reference #3", "fcde0e2623a33b5c70a434ec756440f4630bee3765c290fb31a96a96c9542078"),
    _h("Customer reference #4", "d773801194a9266d4d772d3ce8349a1d08be69ece6512e1d5893c5074625e6af"),
    _h("Customer reference #5", "ee33048ee7db443351d86e03d47d3fbaa8e04cac8789122afbeb339d28b7c818"),
    _h("Customer reference #6", "ce83be8cd17b1e67d3fcf038083ddfbbc829b98388926f1ddc36041957f7c9ba"),
    _h("Customer reference #7", "afb13080693d210ecd7364b045c8b14201b08ea58feec24ca812fe69aeb04afa"),
    _h("Customer reference #8", "d1c583322437ccb58f31c2194520789f01459b771d84fb2819ad0181ae2ca9fb"),
    _h("Customer reference #9", "91380effd216347681c8f89b05d7f7cbeca1f7495f87df92643ca5973fd1a7d9"),
    _h("Customer reference #10", "a468bcc740fb3589b5ff6bc72caa1e936958992c1700a303d1ab0ec43d90c328"),
    _h("Customer reference #11", "a30cc63df519865fede674f1deff85589c67e20cdb40aa3892f93f59544f2f17"),
    _h("Customer reference #12", "c25b5c313ca13eb1bc686ed78b45ab2807b1fc63d8751b10b32582359b210bda"),
    _h("Customer reference #13", "1cad17c842d8cd0b47f676fb5dec43254d923ab82f1367f2570711b51086abb6"),
    _h("Customer reference #14", "39579ad85c95afc87feffaecd324b32d6831bb64b437588d3b31d9c98ee3f6fc"),
    _h("Customer reference #15", "311a7f93580767872f1743f45b7d22a2e158622678e0a61eb6371a8d5f0bb00b"),
    _h("Customer reference #16", "3b0bcceeb1f87b394c3c34e00f5b38fad27de44ba74884f1c4e78d283d11989f"),
    _h("Customer reference #17", "47cbb00f8fe54e02d4f6bc39161907e437c1ae5ee9d52a41770cdf00bd2a3dd1"),
    _h("Customer reference #18", "8f182bdbed919d45538c5c795ef5dbc23956a55190bfd65da8803c1749767edc"),
    _h("Customer reference #19", "9b7733ae188f1a3d70d1ad1e8230b5924b467e482af677c08ccbc63e3eaec77f"),
    _h("Customer reference #20", "900e813fb16e231b16e99d71a7a0894ac09a0aae50f4ef1783528ada0f4b2e1b"),
    # words channel — customer personal names
    _h("Customer personal name #1", "e469cd90ac11585e70574077124334304daf3b7961b790583b10b9bc2be38849"),
    _h("Customer personal name #2", "1508ac400232710add1be60b2471697676c9bbf698ae0e4d7a22f70a54c15349"),
    _h("Customer personal name #3", "af8a3160e0aed393d69cbf5366fa578c003a56bbaffa792fb2b76cdb5ee9c8de"),
    _h("Customer personal name #4", "b0c00590e538488de368da885cc24df5236091b25be6f0dd02a755259ea0391c"),
    _h("Customer personal name #5", "c76fd65d7dceb61efe0279d9125e4f47a6ca8396046806dfdf00c9c0c1ce03ef"),
    _h("Customer personal name #6", "78e1cabc7b3470d1af421f40436bc3f96fdd000ab320b559e59d1a3e576e9f31"),
    _h("Customer personal name #7", "7b12115d48dcd306633990510ec05fdb2cc5d7fc7101b67c67175a2f0f336d57"),
    _h("Customer personal name #8", "de529f9ace7a2683ef913d407ae790c093c712f9ceb4914367aa5af4d6f582a4"),
    _h("Customer personal name #9", "1f0315a81d7773fa43830e00a64cc07f1bc1e57137f70a86e883863a5f0d8d53"),
    _h("Customer personal name #10", "d3ac3314b459ab66c47e77e20658264581fae955219eaa35a5b6e8318515570a"),
    _h("Customer personal name #11", "cc7a9c17bf7a4d391a0f81d66d094560447aebb7423c574cd981499549ca4be4"),
    _h("Customer personal name #12", "16d04d4fe67c1cf84b7a84ce1dde96d045cabf6c368bea840de73744b7d862fe"),
    _h("Customer personal name #13", "8eb0cd1e677d5a754e96ed31fe7d24a809972170a3ca25a20eddb25140e8f9e3"),
    _h("Customer personal name #14", "fe9b060ce5de4daad983ebf7f2326c9302250d46bcf602b75781ec19430a76e4"),
    _h("Customer personal name #15", "7cda228fe9a5bad468181e80a9902a0560cc2879b2302cb2e275ce9645ab60c0"),
    # words channel — internal names and codenames
    _h("Internal name #1", "db40ee2afe9fb04b79d05effb7d62aabbe75b46289e6f34b7edb17f25806412f"),
    _h("Internal name #2", "5e570eb37e5ebc937d04020ba525cf7f75f7f59152c977d3db821fe238c2f745"),
    _h("Internal name #3", "800a6afa1c50000b4593541f0321958bdd077dcf360f7923a9d8e4aa04a285d3"),
    _h("Internal name #4", "96a4bc2602655473120fcc571ee3d8cfe5f8801f8038ccc06323d305e323331c"),
    # compact channel — UUIDs, hostnames, project refs
    _h("Supabase project ref", "7f16e56be7db4d84cf824df0cf9425b7989a6a294e9c950f99dd869b9a910ea1"),
    _h("Internal hostname", "8be8d63be8eb1112c455952a07b4f5b4bf1d08e717641bd5c83c892a54b8a4c0"),
    _h("Internal company id #1", "840471e1a954e40dabe634443271236e04d5e4d5f24600369e903b6e119d4136"),
    _h("Internal company id #2", "9c7355e056fea55afe03baa1243d95c565233e6745219097ed1e0363155f109e"),
    _h("Internal user id #1", "9a51e7ae18c1cc08abb0ff2c955abf1df65355fb4b18de89450178ea13d5368b"),
    _h("Internal user id #2", "b70076508f01f686d443d5a7fc3a7296d92c5819a826f53fd65fd111150c7f55"),
    # digits channel — personal phone numbers
    _h("Personal phone #1", "10797cfd3579becb13a6ad38caffb25f99f46d5ecc7cc95aa37a24c7f44c9414"),
    _h("Personal phone #2", "57e58ee1feeec0e17b147ed1bacf0a66c882fd6d2d6ff3244402618a8f654f56"),
]

# digest -> label, for O(1) lookup during the scan
HASHED_IDENTITIES: dict[str, str] = {digest: label for label, digest in _HASHED_ENTRIES}


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


def _tracked_files() -> list[Path]:
    """Everything git would publish. Same helper shape as
    tools/check-no-secrets.py — an empty list means 'no git here', and the
    caller falls back to walking the tree."""
    try:
        out = subprocess.run(["git", "ls-files"], cwd=REPO_ROOT,
                             capture_output=True, text=True, check=True)
        return [REPO_ROOT / p for p in out.stdout.splitlines() if p.strip()]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []


def _iter_files(root: Path, include_staging: bool, tracked_only: bool = False):
    if root.is_file():
        if _should_scan(root, include_staging=True):
            yield root
        return
    if tracked_only:
        tracked = _tracked_files()
        if tracked:
            for path in tracked:
                if path.exists() and _should_scan(path, include_staging):
                    yield path
            return
        # No git (tarball install, exported copy) — walking the tree is the
        # safer failure mode than silently scanning nothing.
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


_WORD_RE = re.compile(r"[a-z0-9&]+")
_COMPACT_RE = re.compile(r"[a-z0-9][a-z0-9.@+_\-]{4,}")
_DIGITS_RE = re.compile(r"\d(?:[\d\s\-().]{5,})\d")
_MAX_NGRAM = 4  # longest hashed name is four words


def _sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _hash_scan_line(line: str) -> list[tuple[str, str]]:
    """Return (label, matched-candidate) for every hashed identity on the
    line. Three channels, mirroring how identities were normalized when
    hashed: word n-grams for names, compact tokens for identifiers, stripped
    digit runs for phone numbers."""
    hits: list[tuple[str, str]] = []
    lower = line.lower()

    words = _WORD_RE.findall(lower)
    for n in range(1, _MAX_NGRAM + 1):
        for start in range(len(words) - n + 1):
            candidate = " ".join(words[start:start + n])
            label = HASHED_IDENTITIES.get(_sha(candidate))
            if label:
                hits.append((label, candidate))

    for token in _COMPACT_RE.findall(lower):
        label = HASHED_IDENTITIES.get(_sha(token))
        if label:
            hits.append((label, token))

    for run in _DIGITS_RE.findall(lower):
        label = HASHED_IDENTITIES.get(_sha(re.sub(r"\D", "", run)))
        if label:
            hits.append((label, run))

    return hits


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
        for label, candidate in _hash_scan_line(line):
            findings.append(Finding(
                file=path,
                line=i,
                severity="FAIL",
                pattern=label,
                match=candidate,
                replacement="(remove — real identity; invent a fictional one)",
                context=line.strip()[:140],
            ))
    return findings


def _scan_repo(root: Path, include_staging: bool, tracked_only: bool = False) -> list[Finding]:
    all_findings: list[Finding] = []
    for path in _iter_files(root, include_staging, tracked_only):
        all_findings.extend(_scan_file(path))
    return all_findings


# =============================================================================
# Reporting
# =============================================================================


SEVERITY_RANK = {"FAIL": 2, "WARN": 1, "INFO": 0}
SEVERITY_BADGE = {"FAIL": "[FAIL]", "WARN": "[WARN]", "INFO": "[INFO]"}


def _print_report(findings: list[Finding], quiet: bool, fail_only: bool = False) -> int:
    if fail_only:
        findings = [f for f in findings if f.severity == "FAIL"]

    if not findings:
        scope = "no FAIL matches found" if fail_only else "no matches found"
        print(f"Sweep clean — {scope}.")
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


def _force_utf8_stdout() -> None:
    """The report prints the replacement hints and matched source lines
    verbatim, and both contain non-ASCII (arrows, em dashes). On a Windows
    console defaulting to cp1252 that raises UnicodeEncodeError partway
    through, so the run dies with a traceback instead of a verdict. Encode
    with replacement rather than crashing: a mangled glyph in one hint is
    worth less than a gate that never reports."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def main() -> int:
    _force_utf8_stdout()

    parser = argparse.ArgumentParser(description="Sweep the repo for private data.")
    parser.add_argument("path", nargs="?", default=None,
                        help="File or directory to scan (default: all tracked files)")
    parser.add_argument("--all", action="store_true",
                        help="Walk the whole working tree, not just tracked files")
    parser.add_argument("--fail-only", action="store_true",
                        help="Report and exit on FAIL findings only (what CI gates on)")
    parser.add_argument("--staging", action="store_true",
                        help="Include the _staging/ directory (work-in-progress)")
    parser.add_argument("--quiet", action="store_true",
                        help="Print only the summary, not per-line matches")
    parser.add_argument("--hash", metavar="IDENTITY",
                        help="Print the deny-list entry for a new identity "
                             "(name, UUID, hostname, or phone) and exit. "
                             "Paste ONLY the printed hash into this file — "
                             "never the plaintext.")
    args = parser.parse_args()

    if args.hash:
        raw = args.hash.strip()
        print("Add ONE of these to _HASHED_ENTRIES (pick the channel that fits),")
        print("with an anonymous #N label. Never paste the plaintext anywhere.")
        word_form = " ".join(_WORD_RE.findall(raw.lower()))
        print(f'  words   (names):        _h("<label #N>", "{_sha(word_form)}"),')
        print(f'  compact (uuid/host):    _h("<label #N>", "{_sha(raw.lower())}"),')
        digits = re.sub(r"\D", "", raw)
        if digits:
            print(f'  digits  (phone):        _h("<label #N>", "{_sha(digits)}"),')
        return 0

    # An explicit path means "scan exactly this"; only the default scope is
    # narrowed to tracked files.
    tracked_only = args.path is None and not args.all
    root = Path(args.path).resolve() if args.path else REPO_ROOT
    if not root.exists():
        print(f"Error: path does not exist: {root}", file=sys.stderr)
        return 2

    findings = _scan_repo(root, include_staging=args.staging, tracked_only=tracked_only)
    return _print_report(findings, quiet=args.quiet, fail_only=args.fail_only)


if __name__ == "__main__":
    sys.exit(main())
