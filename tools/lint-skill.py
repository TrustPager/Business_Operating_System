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
- If fetch.py exists:
  - Imports from trustpager_api (or has a comment explaining why not).
  - No hardcoded tp_live_* API keys.
  - No hardcoded supabase.co URLs (use API_BASE from trustpager_api).
  - Uses resolve_path() when calling api_get() (so paths don't drift).

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

# Single parser owner: lint imports parse_frontmatter from tools/manifest.py
# rather than carrying its own copy (P1 Task 5 collapsed the fork).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from manifest import parse_frontmatter  # noqa: E402

REQUIRED_FRONTMATTER = {"name", "description", "triggers"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("skill_dir", help="Path to a skill directory (e.g. skills/sweep-my-day)")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).resolve()
    if not skill_dir.is_dir():
        print(f"ERROR: not a directory: {skill_dir}", file=sys.stderr)
        return 2

    issues: list[tuple[str, str]] = []

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        issues.append(("FAIL", f"missing {skill_md.name}"))
    else:
        text = skill_md.read_text(encoding="utf-8")
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
        if "api_get(" in py_text and "resolve_path(" not in py_text:
            issues.append(("WARN", "fetch.py calls api_get() but doesn't use resolve_path() — "
                                    "paths may drift if the API renames endpoints"))

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
