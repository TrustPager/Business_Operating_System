#!/usr/bin/env python3
"""Connector safety gate — reads each connected driver's own DRIVER dict.

This is the generalized successor to the one-off ads spend-safety gate. Instead
of hard-coding one vendor's tools, it discovers every connected driver under
``drivers/<id>/__init__.py`` that declares a top-level ``DRIVER`` dict and reads
that dict's ``never_call`` / ``never_set`` fields as the single source of truth
for what BOS may never do from a skill body. Add a new connected driver with its
own ``DRIVER`` dict and its safety surface is enforced automatically — no edit to
this file.

Spend/irreversible-action safety is the ONE thing this gate enforces today. A
driver's ``DRIVER`` dict expresses two off-limits paths, and this checker closes
both by scanning every skill body:

  1. **The obvious switch** — a call to a ``never_call`` tool (e.g. Meta Ads'
     ``ads_activate_entity``). BOS creates PAUSED shells and never turns an ad on;
     this gate fails on the tool name appearing in ANY skill body, no matter its
     manifest.

  2. **The subtler switch** — an update-style tool named in ``never_set`` with one
     of its listed fields set to ACTIVE (e.g. ``ads_update_entity`` carrying a
     ``{"status":"ACTIVE"}`` payload). The update tool legitimately stays in a
     skill's ``uses_tools`` (it renames or fixes an integer budget/bid on a
     still-PAUSED shell), so omission cannot guard this path — a value scan does.
     Meta exposes three interchangeable status fields (``status``,
     ``configured_status``, ``effective_status``); the DRIVER dict lists all three.

Parity note: a ``DRIVER`` dict stores FULLY-QUALIFIED tool names
(``mcp__<id>__<tool>``), but a skill body historically refers to the BARE name
(``ads_activate_entity``). To preserve the exact breadth of the original gate,
each ``never_call`` / ``never_set`` tool is expanded to BOTH forms and both are
searched — dropping the bare form would regress the gate.
``tests/test_check_connectors.py`` guards this parity.

A driver package with no top-level ``DRIVER`` dict (e.g. ``trustpager``) is
grandfathered — it contributes no rules — and underscore-prefixed dirs
(templates/scaffolding) are skipped. This gate is deliberately standalone (stdlib
only, static ``ast`` read — it never imports driver code) so it runs anywhere, as
a CI gate and before any push.

Conformance checks (kind / requires_driver / connect.md / card / frontmatter) are
NOT part of this gate yet; they arrive in a follow-up task.

Exit codes:
    0 — clean (prints a one-line OK)
    2 — at least one off-limits path found (prints file:line, then a fix hint)

Usage:
    python tools/check-connectors.py
"""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"


# --- The never-call / never-set surface (DATA — read from each driver's DRIVER dict) ---
#
# The forbidden surface is no longer a module literal. Each connected driver owns
# its own safety facts in drivers/<id>/__init__.py's top-level DRIVER dict
# (never_call / never_set), and this gate aggregates them at runtime. Add a new
# connected driver with its own DRIVER dict and its rules are enforced with no edit
# here (spec §3b / §5).


def _load_driver_dicts() -> dict:
    """{driver_id: DRIVER dict} for every drivers/<id>/__init__.py declaring a
    top-level DRIVER dict. Skips underscore-prefixed dirs (templates/scaffolding).
    Static ast.literal_eval - never imports driver code."""
    out = {}
    ddir = REPO_ROOT / "drivers"
    if not ddir.is_dir():
        return out
    for init in sorted(ddir.glob("*/__init__.py")):
        drv_id = init.parent.name
        if drv_id.startswith("_"):
            continue
        try:
            tree = ast.parse(init.read_text(encoding="utf-8", errors="ignore"))
        except (OSError, SyntaxError):
            continue
        for node in tree.body:
            # Match both `DRIVER = {...}` (Assign) and `DRIVER: dict = {...}`
            # (AnnAssign). A safety gate must not silently miss a driver's forbidden
            # surface just because the assignment carries a type annotation — natural
            # here since the files use `from __future__ import annotations`.
            value = None
            if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "DRIVER" for t in node.targets
            ):
                value = node.value
            elif (
                isinstance(node, ast.AnnAssign)
                and isinstance(node.target, ast.Name)
                and node.target.id == "DRIVER"
                and node.value is not None  # `DRIVER: dict` with no value binds nothing
            ):
                value = node.value
            if value is None:
                continue
            try:
                parsed = ast.literal_eval(value)
            except (ValueError, SyntaxError):
                continue
            # Fail safe: a non-dict DRIVER (e.g. a list) would crash the downstream
            # .get(...) — skip it exactly like an unparseable value.
            if isinstance(parsed, dict):
                out[drv_id] = parsed
    return out


def _name_forms(tool: str, driver_id: str) -> set:
    """Both forms of a tool name. A DRIVER dict stores the FULLY-QUALIFIED name
    (``mcp__<id>__<tool>``); a skill body historically names the BARE tool
    (``ads_activate_entity``). Searching both preserves the exact breadth of the
    original gate (parity) — dropping the bare form would regress it."""
    forms = {tool}
    prefix = f"mcp__{driver_id}__"
    if tool.startswith(prefix):
        forms.add(tool[len(prefix):])   # bare name, preserves current breadth
    return forms


def _forbidden_surface() -> tuple[set[str], dict[str, tuple[str, ...]]]:
    """Aggregate every connected driver's never_call / never_set into the forms to
    search for. Returns (never_call_forms, {never_set_form: (fields...)}), each tool
    expanded to BOTH its fully-qualified and bare name via _name_forms."""
    drivers = _load_driver_dicts()
    never_call_forms: set[str] = set()
    never_set_forms: dict[str, tuple[str, ...]] = {}
    for drv_id, driver in drivers.items():
        for tool in driver.get("never_call", ()):
            never_call_forms |= _name_forms(tool, drv_id)
        for tool, fields in driver.get("never_set", {}).items():
            fields_t = tuple(fields)
            for form in _name_forms(tool, drv_id):
                # Merge, de-duplicating, if two drivers ever name the same form.
                merged = tuple(dict.fromkeys((*never_set_forms.get(form, ()), *fields_t)))
                never_set_forms[form] = merged
    return never_call_forms, never_set_forms


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
    never_call_forms, never_set_forms = _forbidden_surface()
    call_res = {tool: re.compile(re.escape(tool)) for tool in never_call_forms}
    set_res = {
        tool: [(field, _active_field_pattern(field)) for field in fields]
        for tool, fields in never_set_forms.items()
    }
    tool_res = {tool: re.compile(re.escape(tool)) for tool in never_set_forms}

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
