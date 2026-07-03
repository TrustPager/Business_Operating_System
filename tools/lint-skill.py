#!/usr/bin/env python3
"""Validate a Claude Code skill folder before committing it (lint).

When to use:
- About to commit a new skill — sanity-check the format first.
- About to publish a community skill — catch missing required frontmatter.
- Debugging "skill not triggering" — verify it has the required pieces.

What it checks:
- SKILL.md exists.
- SKILL.md starts with YAML frontmatter (--- ... ---).
- Required frontmatter fields are present: name, description, triggers.
- "triggers" has at least 3 phrases (5+ recommended).
- The manifest contract (validate_manifest) passes — FAIL on any error. (P1 Task 3a)
- No mcp__ tool referenced in the SKILL.md body that is undeclared — i.e. not in
  uses_tools and not owned by the skill's requires_driver. (P1 Task 3c — FAIL)
- If fetch.py exists:
  - Imports from trustpager_api (or has a comment explaining why not).
  - No hardcoded tp_live_* API keys.
  - No hardcoded supabase.co URLs (use API_BASE from trustpager_api).
  - Uses resolve_path() when calling api_get() (so paths don't drift). (P1 Task 3b — FAIL)

Exit codes:
    0 — no issues
    1 — only warnings
    2 — at least one [FAIL]

Usage:
    python tools/lint-skill.py skills/sweep-my-day
    python tools/lint-skill.py skills/my-new-skill

Related:
    python tools/test-skill.py <skill>             # offline fixture test
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Single parser owner: lint imports parse_frontmatter + validate_manifest from
# tools/manifest.py rather than carrying its own copy (P1 Task 5 collapsed the
# parser fork; Task 3 added validate_manifest enforcement).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from manifest import parse_frontmatter, validate_manifest  # noqa: E402

REQUIRED_FRONTMATTER = {"name", "description", "triggers"}

# Any mcp__<server>__<tool> reference in a SKILL.md body. Tool names are
# [A-Za-z0-9_], and the server segment may itself carry hyphens (a kebab-case
# driver id like ``meta-ads``, or a uuid-with-hyphens), so the character class
# includes ``-`` — otherwise a token like ``mcp__meta-ads__ads_create_campaign``
# would be truncated at the hyphen to ``mcp__meta`` and never match its declared
# full name in uses_tools or its ``meta-ads`` driver owner.
_MCP_TOOL_RE = re.compile(r"mcp__[A-Za-z0-9_-]+")


def _driver_owns_tool(tool: str, driver: str | None) -> bool:
    """True if ``tool`` belongs to the skill's declared ``requires_driver``.

    An app may freely reference its own driver's tools without declaring each in
    uses_tools — a ``requires_driver: trustpager`` app may name any
    ``mcp__*trustpager*`` tool, a ``firecrawl`` app any firecrawl tool, etc. The
    match is a case-insensitive substring of the driver id within the tool name,
    which is deliberately loose: the driver id (e.g. ``trustpager``) appears as a
    segment of its tools' fully-qualified names. ``none`` owns nothing.
    """
    if not driver or driver == "none":
        return False
    return driver.lower() in tool.lower()


def _split_frontmatter_body(text: str) -> str:
    """Return the SKILL.md body (everything after the closing frontmatter fence)."""
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    if end < 0:
        return text
    return text[end + 4:]


def lint_skill(skill_dir: Path) -> list[tuple[str, str]]:
    """Run every lint check on one skill directory and return (severity, message) tuples.

    severity is "FAIL" or "WARN". An empty list means a clean pass. This is the
    importable core; ``main()`` wraps it for CLI exit codes.
    """
    issues: list[tuple[str, str]] = []

    skill_md = skill_dir / "SKILL.md"
    fm: dict | None = None
    body = ""
    if not skill_md.exists():
        issues.append(("FAIL", f"missing {skill_md.name}"))
    else:
        text = skill_md.read_text(encoding="utf-8")
        body = _split_frontmatter_body(text)
        try:
            fm = parse_frontmatter(text)
        except ValueError as exc:
            fm = None
            issues.append(("FAIL", f"SKILL.md frontmatter is malformed: {exc}"))
        if not fm:
            if not any(sev == "FAIL" for sev, _ in issues):
                issues.append(("FAIL", "SKILL.md missing YAML frontmatter (--- ... ---)"))
        else:
            missing = REQUIRED_FRONTMATTER - set(fm)
            for k in missing:
                issues.append(("FAIL", f"SKILL.md frontmatter missing required field: {k}"))
            triggers = fm.get("triggers")
            if isinstance(triggers, list) and len(triggers) < 3:
                issues.append(("WARN", f"SKILL.md has only {len(triggers)} trigger phrases; aim for 5+"))

            # (a) Manifest contract enforcement — FAIL on any validate_manifest error.
            for err in validate_manifest(fm):
                issues.append(("FAIL", f"manifest: {err}"))

            # (c) Undeclared mcp__ tool references in the body — FAIL.
            #     A referenced tool is OK if it's in uses_tools OR owned by the
            #     skill's requires_driver (an app may name its own driver's tools
            #     freely). Anything else is drift.
            declared = set(fm.get("uses_tools") or [])
            driver = fm.get("requires_driver")
            referenced = set(_MCP_TOOL_RE.findall(body))
            for tool in sorted(referenced):
                if tool in declared:
                    continue
                if _driver_owns_tool(tool, driver):
                    continue
                issues.append((
                    "FAIL",
                    f"SKILL.md body references tool '{tool}' that is neither declared in "
                    f"uses_tools nor owned by requires_driver "
                    f"('{driver or 'none'}') — add it to uses_tools or remove the reference",
                ))

    fetch_py = skill_dir / "fetch.py"
    if fetch_py.exists():
        py_text = fetch_py.read_text(encoding="utf-8")
        imports_lib = ("from trustpager_api import" in py_text
                       or "import trustpager_api" in py_text
                       or "from bos_lib import" in py_text)
        if not imports_lib:
            issues.append(("WARN", "fetch.py doesn't import from trustpager_api — "
                                    "likely missing shared helpers"))
        if re.search(r"tp_live_[A-Za-z0-9_]{20,}", py_text):
            issues.append(("FAIL", "fetch.py contains what looks like a hardcoded tp_live_* API key"))
        if "supabase.co" in py_text:
            issues.append(("WARN", "fetch.py references supabase.co directly — "
                                    "should use API_BASE from trustpager_api"))
        # (b) resolve_path discipline — promoted WARN -> FAIL. fetch.py must route
        #     api_get() calls through resolve_path() so endpoints don't drift.
        if "api_get(" in py_text and "resolve_path(" not in py_text:
            issues.append(("FAIL", "fetch.py calls api_get() but doesn't use resolve_path() — "
                                    "paths may drift if the API renames endpoints"))

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("skill_dir", help="Path to a skill directory (e.g. skills/sweep-my-day)")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).resolve()
    if not skill_dir.is_dir():
        print(f"ERROR: not a directory: {skill_dir}", file=sys.stderr)
        return 2

    issues = lint_skill(skill_dir)

    print(f"Linting {skill_dir.name}/...")
    if not issues:
        print("  OK — no issues found.")
        return 0
    for severity, msg in issues:
        marker = "[FAIL]" if severity == "FAIL" else "[WARN]"
        print(f"  {marker} {msg}")
    failures = sum(1 for s, _ in issues if s == "FAIL")
    return 2 if failures else 1


if __name__ == "__main__":
    sys.exit(main())
