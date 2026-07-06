#!/usr/bin/env python3
"""Hold the session-start surface flat: cap every skill/command description.

At every session start, Claude Code injects the name + frontmatter
``description`` of every installed skill AND every installed command into
context. That surface is paid for on every single turn, on every client
machine, for the life of the install. It is also the router: Claude decides
when to auto-invoke a skill from its description alone, so the description must
keep its trigger vocabulary ("what it does, when to use it, the phrases an
owner would say") while shedding benefit-marketing prose.

This gate stops the surface creeping back up as the catalog grows. It fails if:

  * any ``skills/*/SKILL.md`` frontmatter ``description`` exceeds 400 chars, or
  * any ``commands/*.md`` frontmatter ``description`` exceeds 150 chars.

The caps are deliberately looser than the working targets (skills trimmed to
<=350, command shims to <=120) so the gate catches genuine regressions without
nagging over a few characters. A command shim only labels the slash-command
menu; the full trigger surface lives on the skill, so its cap is much tighter.

Exit codes:
    0 — every description is within budget
    2 — at least one description is over its cap

Usage:
    python tools/check-surface-budget.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

from manifest import parse_frontmatter  # noqa: E402  (single frontmatter parser owner)

SKILL_CAP = 400
COMMAND_CAP = 150


def _description(md_path: Path) -> str:
    """Return the frontmatter ``description`` for a skill/command file, or ""."""
    try:
        text = md_path.read_text(encoding="utf-8")
    except OSError:
        return ""
    meta = parse_frontmatter(text)
    desc = meta.get("description", "")
    return desc if isinstance(desc, str) else ""


def _over(paths: list[Path], cap: int) -> list[tuple[str, int]]:
    findings: list[tuple[str, int]] = []
    for p in sorted(paths):
        n = len(_description(p))
        if n > cap:
            rel = str(p.relative_to(REPO_ROOT)).replace("\\", "/")
            findings.append((rel, n))
    return findings


def scan() -> int:
    skills = list((REPO_ROOT / "skills").glob("*/SKILL.md"))
    commands = list((REPO_ROOT / "commands").glob("*.md"))

    skill_over = _over(skills, SKILL_CAP)
    command_over = _over(commands, COMMAND_CAP)

    if not skill_over and not command_over:
        print(
            f"OK: surface within budget "
            f"({len(skills)} skills <= {SKILL_CAP}, "
            f"{len(commands)} commands <= {COMMAND_CAP})."
        )
        return 0

    total = len(skill_over) + len(command_over)
    print(f"FAIL: {total} description(s) over budget — the session-start "
          f"surface is the router and is paid for every turn:\n")
    for rel, n in skill_over:
        print(f"  {rel}: description {n} chars > {SKILL_CAP} cap")
    for rel, n in command_over:
        print(f"  {rel}: description {n} chars > {COMMAND_CAP} cap")
    print("\nTrim to keep trigger vocabulary (what it does, when to use it, the "
          "phrases an owner would say) and cut benefit-marketing prose. Skills "
          f"aim <= 350, command shims <= 120. Re-run when done.")
    return 2


def main() -> int:
    return scan()


if __name__ == "__main__":
    sys.exit(main())
