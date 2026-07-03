#!/usr/bin/env python3
"""Spend-safety gate for the ads write surface (spec §8 Layer 3.3).

Meta Ads writes spend real money. BOS creates PAUSED shells only and NEVER turns
an ad on. There are TWO activation paths, not one, and this checker closes both by
scanning every skill body:

  1. **The obvious switch** — a call to ``ads_activate_entity``. It is deliberately
     absent from ``run-my-ads``'s ``uses_tools``, so lint already fails a body that
     names it; this gate is the belt-and-suspenders that fails on the tool name
     appearing in ANY skill body, no matter its manifest.

  2. **The subtler switch** — ``ads_update_entity`` with a status set to ACTIVE.
     The live ``ads_update_entity`` schema accepts a free-form ``fields`` object of
     any name→value, including ``{"status":"ACTIVE"}``; its own description only
     *advises* against it, it does not enforce it. ``ads_update_entity`` legitimately
     stays in ``uses_tools`` (it renames or fixes an integer budget/bid on a
     still-PAUSED shell), so omission cannot guard this path. This gate does: it
     FAILS when a body co-locates ``ads_update_entity`` with a ``status`` field set
     to ACTIVE (or any ``status`` key inside an update ``fields`` blob).

This mirrors how ``check-onboarding-binding.py`` assertion C forbids TrustPager
coupling tokens in a keyless body. It is deliberately standalone (stdlib only, no
imports of BOS code) so it runs anywhere — as a CI gate and before any push.

Extending it: the never-call / never-set surface is data, not code. Add a tool
name to ``NEVER_CALL_TOOLS`` to forbid its call in any body, or add a
``tool -> [field, ...]`` entry to ``NEVER_SET_ACTIVE`` to forbid setting one of
those fields to ACTIVE via that tool. Both mirror the ``never_call`` / ``never_set``
metadata documented on the driver (spec §3b).

Exit codes:
    0 — clean (prints a one-line OK)
    2 — at least one activation path found (prints file:line, then a fix hint)

Usage:
    python tools/check-ads-safety.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

# --- The never-call / never-set surface (data, mirrors driver metadata §3b) ---
#
# Tool names BOS must never invoke from a skill body. Path 1: the obvious switch.
# To forbid another irreversible/spend tool, add its bare tool name here.
NEVER_CALL_TOOLS: tuple[str, ...] = (
    "ads_activate_entity",
)

# Per-tool field names BOS must never set to ACTIVE. Path 2: the subtler switch.
# Map each update-style tool to the field(s) that must never be set ACTIVE through
# it. To cover a future tool, add another ``tool: [field, ...]`` entry. Meta exposes
# three interchangeable status fields on an entity — ``status``, ``configured_status``,
# and ``effective_status`` — so all three are forbidden: a ``{"configured_status":
# "ACTIVE"}`` payload un-pauses just as surely as ``{"status":"ACTIVE"}``.
NEVER_SET_ACTIVE: dict[str, tuple[str, ...]] = {
    "ads_update_entity": ("status", "configured_status", "effective_status"),
}

# A ``status`` (or other named field) set to ACTIVE, in either JSON or Python-dict
# form, tolerant of whitespace and single or double quotes, AND tolerant of the key,
# colon, and value landing on SEPARATE physical lines (``re.DOTALL`` so ``\s`` — and
# the whitespace runs between tokens — span newlines). A pretty-printed ``fields``
# blob puts ``"status":`` and ``"ACTIVE"`` on different lines; that must still match:
#   "status": "ACTIVE"   'status':'ACTIVE'   "status" : "active"   "status":\n"ACTIVE"
def _active_field_pattern(field: str) -> re.Pattern[str]:
    return re.compile(
        r"""['"]""" + re.escape(field) + r"""['"]\s*:\s*['"]ACTIVE['"]""",
        re.IGNORECASE | re.DOTALL,
    )

# Don't scan binaries or vendored/build dirs (mirrors check-no-secrets.py).
SKIP_DIRS = {".git", "node_modules", "__pycache__", "_staging", "graphify-out",
             ".venv", "venv", ".pytest_cache"}
MAX_BYTES = 2_000_000


def _skill_bodies() -> list[tuple[Path, str]]:
    """Every skills/*/SKILL.md as (relative-path, text). Skips build/vendor dirs."""
    bodies: list[tuple[Path, str]] = []
    if not SKILLS_DIR.is_dir():
        return bodies
    for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        rel = skill_md.relative_to(REPO_ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        try:
            if skill_md.stat().st_size > MAX_BYTES:
                continue
            text = skill_md.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        bodies.append((rel, text))
    return bodies


def scan() -> int:
    findings: list[str] = []
    call_res = {tool: re.compile(re.escape(tool)) for tool in NEVER_CALL_TOOLS}
    set_res = {
        tool: [(field, _active_field_pattern(field)) for field in fields]
        for tool, fields in NEVER_SET_ACTIVE.items()
    }
    tool_res = {tool: re.compile(re.escape(tool)) for tool in NEVER_SET_ACTIVE}

    for rel, text in _skill_bodies():
        lines = text.splitlines()
        # Path 1 — a never-call tool named anywhere in the body. Per-line so we can
        # report the exact line the tool name appears on.
        for i, line in enumerate(lines, start=1):
            for tool, pat in call_res.items():
                if pat.search(line):
                    findings.append(
                        f"{rel}:{i}: never-call tool `{tool}` appears in the body — "
                        f"BOS must never turn an ad on. Remove it: build paused only."
                    )

        # Path 2 — a never-set field set to ACTIVE for an update-style tool. A body
        # sets status ACTIVE via ads_update_entity by naming the tool AND carrying a
        # `"status": "ACTIVE"` payload. The status write is the violation whether or
        # not the key, colon, and value share one physical line — a pretty-printed
        # `fields` blob spans lines. So we search the WHOLE body text (not per-line):
        # the pattern is DOTALL-tolerant, and we report the match's line by counting
        # newlines up to the match offset. The tool-name co-occurrence is already a
        # whole-text check, so both halves now see across line boundaries.
        for tool, field_pats in set_res.items():
            if not tool_res[tool].search(text):
                continue
            for field, fpat in field_pats:
                m = fpat.search(text)
                if m:
                    line_no = text.count("\n", 0, m.start()) + 1
                    findings.append(
                        f"{rel}:{line_no}: `{tool}` is used in this body AND a "
                        f"`{field}` field is set to ACTIVE here — setting "
                        f"{field}=ACTIVE is a spend action and is off-limits by "
                        f"the same rule as ads_activate_entity. Keep the shell "
                        f"PAUSED; the owner activates it in Ads Manager."
                    )

    if findings:
        print(f"FAIL: {len(findings)} ads-safety violation(s) — BOS never activates:\n")
        for fnd in findings:
            print(f"  {fnd}")
        print("\nBOS creates PAUSED shells and stops. It never calls "
              "ads_activate_entity and never sets a status field to ACTIVE via "
              "ads_update_entity (spec §8 Layer 3). The owner reviews in Ads Manager "
              "and switches it on themselves. Remove the activation and re-run.")
        return 2

    print("OK: no ads activation paths in any skill body "
          "(no ads_activate_entity call, no status=ACTIVE via ads_update_entity).")
    return 0


def main() -> int:
    return scan()


if __name__ == "__main__":
    sys.exit(main())
