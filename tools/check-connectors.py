#!/usr/bin/env python3
"""Connector gate — safety + structural conformance, from each driver's DRIVER dict.

This is the generalized successor to the one-off ads spend-safety gate. Instead
of hard-coding one vendor's tools, it discovers every connected driver under
``drivers/<id>/__init__.py`` that declares a top-level ``DRIVER`` dict and reads
that dict as the single source of truth for what BOS may never do (safety) and
what a well-formed connected add-on looks like (conformance). Add a new connected
driver with its own ``DRIVER`` dict and both its safety surface and its structure
are enforced automatically — no edit to this file.

Two families of checks, one findings list, one exit code:

**Safety** (spend/irreversible-action). A driver's ``DRIVER`` dict expresses two
off-limits paths, and this gate closes both by scanning every skill body:

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

**Conformance** (spec §6) — for each driver that ships a ``DRIVER`` dict:

  - ``kind`` is present and in the canonical taxonomy (§4).
  - ``requires_driver`` on EVERY skill manifest **resolves**, closing the
    typo-passes-silently hole. Resolution is threefold because keyless drivers are
    folderless: valid if ``none``, OR a known keyless driver id (``_KEYLESS_DRIVERS``
    reused from ``check-onboarding-binding.py``), OR a real ``drivers/<id>/`` folder
    exists. A naive "the folder must exist" check would wrongly fail every
    firecrawl/render skill.
  - For **connected** kinds (``claude_mcp``, ``keyed_cli``): a ``connect.md`` exists
    in the driver folder, AND a heading in ``knowledge/connectors.md`` **begins with**
    the ``display_name`` (prefix match — the house style appends a parenthetical, so
    an exact ``## <display_name>`` match would wrongly fail the real
    ``## Meta Ads (Facebook & Instagram ads)`` card).
  - The **connected frontmatter contract** holds for each skill whose
    ``requires_driver`` is an opted-in DRIVER-dict driver: ``requires_credential`` in
    ``{mcp, key}``, ``data_path`` in ``{mcp_tools, local}``, and every ``uses_tools``
    entry is driver-owned (contains the driver id). Floor skills
    (``requires_driver: none``) are not mechanically linked to a driver, so the gate
    enforces only this connected half; the floor keyless-clean contract stays with
    lint + onboarding-binding.

Parity note: a ``DRIVER`` dict stores FULLY-QUALIFIED tool names
(``mcp__<id>__<tool>``), but a skill body historically refers to the BARE name
(``ads_activate_entity``). To preserve the exact breadth of the original gate,
each ``never_call`` / ``never_set`` tool is expanded to BOTH forms and both are
searched — dropping the bare form would regress the gate.
``tests/test_check_connectors.py`` guards this parity.

A driver package with no top-level ``DRIVER`` dict (e.g. ``trustpager``) is
grandfathered — it contributes no rules — and underscore-prefixed dirs
(templates/scaffolding) are skipped. This gate is deliberately standalone (stdlib
plus the sibling ``manifest.py`` parser / ``check-onboarding-binding.py`` set, all
stdlib; static ``ast`` read — it never imports driver code) so it runs anywhere, as
a CI gate and before any push.

Exit codes:
    0 — clean (prints a one-line OK)
    2 — at least one off-limits path or conformance failure (prints details + hint)

Usage:
    python tools/check-connectors.py                 # scan the real repo
    python tools/check-connectors.py --root <dir>    # scan a fixture tree (tests)
"""

from __future__ import annotations

import argparse
import ast
import importlib.util
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_TOOLS_DIR = Path(__file__).resolve().parent


# --- Sibling imports (one home per fact) ---------------------------------
#
# The keyless-driver set and the frontmatter parser both already have owners in
# tools/. Reuse them rather than restate them (anti-drift). manifest.py imports by
# name (valid identifier); check-onboarding-binding.py is hyphenated, so it cannot
# be reached by ``import`` and must be loaded from its file path.

sys.path.insert(0, str(_TOOLS_DIR))
from manifest import (  # noqa: E402  (path set just above)
    DATA_PATHS,
    REQUIRES_CREDENTIAL,
    parse_frontmatter,
)


def _load_keyless_drivers() -> frozenset[str]:
    """Reuse ``_KEYLESS_DRIVERS`` from check-onboarding-binding.py (its home).

    That module is hyphenated, so it can't be imported by name; load it by path.
    Keeping one owner for the keyless set avoids the drift the doctrine warns about.
    """
    path = _TOOLS_DIR / "check-onboarding-binding.py"
    spec = importlib.util.spec_from_file_location("_check_onboarding_binding", path)
    if spec is None or spec.loader is None:
        # Co-located, so this never triggers today; guarding it makes the
        # fail-closed behavior explicit instead of an opaque AttributeError on None.
        raise ImportError(f"could not load _KEYLESS_DRIVERS from {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod._KEYLESS_DRIVERS


_KEYLESS_DRIVERS: frozenset[str] = _load_keyless_drivers()

# Canonical driver-kind taxonomy (spec §4). A DRIVER dict's ``kind`` must be one of
# these; anything else (or a missing kind) fails conformance.
CANONICAL_KINDS: frozenset[str] = frozenset(
    {"claude_mcp", "keyed_cli", "keyed_rest", "keyless_mcp", "local", "data_pack"}
)

# The connected kinds get the full structural checks (connect.md + card). The other
# kinds do not connect, so connect.md / card are not required of them (spec §6).
CONNECTED_KINDS: frozenset[str] = frozenset({"claude_mcp", "keyed_cli"})

# The connected frontmatter contract (spec §6) allows a strict SUBSET of the shared
# manifest enums: a connected add-on is never keyless, and it runs on a live data
# path. Single-source both against manifest.py so the imported enums stay meaningful
# (anti-drift) rather than being shadowed by hardcoded literals.
#
# credential: a clean subtraction (connected == every credential except 'none').
CONNECTED_CREDENTIALS: frozenset[str] = REQUIRES_CREDENTIAL - {"none"}   # {mcp, key}
# data_path: NOT a clean subtraction (reasoning_only AND fetch_rest are both excluded
# for different reasons), so name the subset explicitly and assert it is a genuine
# subset of the shared enum — the assert catches drift if manifest.py's DATA_PATHS
# ever changes shape, keeping the import load-bearing.
CONNECTED_DATA_PATHS: frozenset[str] = frozenset({"mcp_tools", "local"})
assert CONNECTED_DATA_PATHS <= DATA_PATHS, (
    "CONNECTED_DATA_PATHS drifted from manifest.py DATA_PATHS: "
    f"{CONNECTED_DATA_PATHS - DATA_PATHS} not in the shared enum"
)


# --- The never-call / never-set surface (DATA — read from each driver's DRIVER dict) ---
#
# The forbidden surface is no longer a module literal. Each connected driver owns
# its own safety facts in drivers/<id>/__init__.py's top-level DRIVER dict
# (never_call / never_set), and this gate aggregates them at runtime. Add a new
# connected driver with its own DRIVER dict and its rules are enforced with no edit
# here (spec §3b / §5).


def _load_driver_dicts(root: Path | None = None) -> dict:
    """{driver_id: DRIVER dict} for every drivers/<id>/__init__.py declaring a
    top-level DRIVER dict. Skips underscore-prefixed dirs (templates/scaffolding).
    Static ast.literal_eval - never imports driver code.

    ``root`` defaults to the module-level REPO_ROOT, read live (not bound at def
    time) so a test that reassigns ``cc.REPO_ROOT`` before calling with no argument
    still scans its temp tree — the existing driver-discovery hardening tests rely
    on this."""
    if root is None:
        root = REPO_ROOT
    out = {}
    ddir = root / "drivers"
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


def _forbidden_surface(drivers: dict) -> tuple[set[str], dict[str, tuple[str, ...]]]:
    """Aggregate every connected driver's never_call / never_set into the forms to
    search for. Returns (never_call_forms, {never_set_form: (fields...)}), each tool
    expanded to BOTH its fully-qualified and bare name via _name_forms."""
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


def _skill_bodies(root: Path | None = None) -> list[tuple[Path, str]]:
    """Every skills/*/SKILL.md as (relative-path, text). Skips build/vendor dirs.

    ``root`` defaults to the module-level REPO_ROOT, read live (not bound at def
    time) for the same reason as ``_load_driver_dicts``."""
    if root is None:
        root = REPO_ROOT
    bodies: list[tuple[Path, str]] = []
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        return bodies
    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        rel = skill_md.relative_to(root)
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


# --- Conformance (spec §6) -----------------------------------------------


def _connectors_headings(root: Path) -> list[str]:
    """Every markdown heading (``#``-prefixed) in knowledge/connectors.md, heading
    text only (markers + surrounding whitespace stripped). Empty if the file is
    absent."""
    card_file = root / "knowledge" / "connectors.md"
    if not card_file.is_file():
        return []
    try:
        text = card_file.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    headings: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            headings.append(stripped.lstrip("#").strip())
    return headings


def _resolves_driver(driver_id, drivers: dict, root: Path) -> bool:
    """Threefold requires_driver resolution (spec §6): valid if ``none``, OR a known
    keyless driver id (folderless by design), OR a real drivers/<id>/ folder exists.

    A DRIVER-dict driver id is a folder id, so the folder check covers it too; the
    ``drivers`` map is accepted for symmetry / future use. A non-string or empty id
    never resolves."""
    if not isinstance(driver_id, str) or not driver_id.strip():
        return False
    if driver_id == "none" or driver_id in _KEYLESS_DRIVERS:
        return True
    return (root / "drivers" / driver_id).is_dir()


def _driver_owns_tool(tool: str, driver_id: str) -> bool:
    """True if ``tool`` belongs to ``driver_id``. Case-insensitive substring of the
    driver id within the tool's fully-qualified name — the driver id appears as a
    segment of its tools' names (``mcp__<id>__*``). Mirrors manifest.py /
    lint-skill.py so the validators never disagree."""
    if not isinstance(driver_id, str) or not driver_id or driver_id == "none":
        return False
    return driver_id.lower() in tool.lower()


def _check_conformance(root: Path, drivers: dict) -> list[str]:
    """Return conformance findings (empty == conformant). Merged into the same list
    as the safety scan by ``scan``; one exit code, one report."""
    findings: list[str] = []

    # 1. Every DRIVER dict declares a kind in the canonical taxonomy.
    for drv_id, driver in sorted(drivers.items()):
        kind = driver.get("kind")
        if kind not in CANONICAL_KINDS:
            allowed = ", ".join(sorted(CANONICAL_KINDS))
            findings.append(
                f"drivers/{drv_id}/__init__.py: DRIVER 'kind' is {kind!r}, not in the "
                f"canonical taxonomy — set kind to one of: {allowed}."
            )

    # 2. requires_driver on EVERY skill manifest resolves (threefold).
    #    Parsed once here and reused for the connected-frontmatter contract below.
    parsed_manifests: list[tuple[Path, dict]] = []
    for rel, text in _skill_bodies(root):
        try:
            meta = parse_frontmatter(text)
        except ValueError:
            # A structurally invalid manifest is lint-skill.py's job to report; skip
            # it here rather than crash the connector gate.
            continue
        parsed_manifests.append((rel, meta))
        rd = meta.get("requires_driver")
        if rd is None:
            continue  # absence is a manifest-validation concern, not resolution
        if not _resolves_driver(rd, drivers, root):
            findings.append(
                f"{rel}: requires_driver {rd!r} does not resolve — it is not 'none', "
                f"not a known keyless driver ({', '.join(sorted(_KEYLESS_DRIVERS))}), "
                f"and there is no drivers/{rd}/ folder. Fix the id or add the driver."
            )

    # 3. Connected kinds: connect.md present + a connectors.md card whose heading
    #    begins with display_name (prefix match).
    headings = _connectors_headings(root)
    for drv_id, driver in sorted(drivers.items()):
        if driver.get("kind") not in CONNECTED_KINDS:
            continue
        if not (root / "drivers" / drv_id / "connect.md").is_file():
            findings.append(
                f"drivers/{drv_id}/: a connected driver (kind={driver.get('kind')!r}) "
                f"is missing connect.md — a connected add-on needs a connect.md with "
                f"the connect steps (spec §6)."
            )
        display_name = driver.get("display_name")
        if isinstance(display_name, str) and display_name.strip():
            if not any(h.startswith(display_name) for h in headings):
                findings.append(
                    f"drivers/{drv_id}/: no card in knowledge/connectors.md whose "
                    f"heading begins with the display_name {display_name!r} — add a "
                    f"'## {display_name} ...' card (prefix match; a parenthetical "
                    f"suffix is fine)."
                )
        else:
            findings.append(
                f"drivers/{drv_id}/: connected driver has no display_name, so its "
                f"connectors.md card cannot be matched — set display_name."
            )

    # 4. Connected frontmatter contract, for each skill whose requires_driver is an
    #    opted-in DRIVER-dict driver id.
    for rel, meta in parsed_manifests:
        rd = meta.get("requires_driver")
        if not isinstance(rd, str) or rd not in drivers:
            continue  # only the connected (DRIVER-dict) half is enforced here
        cred = meta.get("requires_credential")
        if cred not in CONNECTED_CREDENTIALS:
            findings.append(
                f"{rel}: connected skill (requires_driver={rd!r}) has "
                f"requires_credential={cred!r} — a connected add-on must be 'mcp' or "
                f"'key'."
            )
        dp = meta.get("data_path")
        if dp not in CONNECTED_DATA_PATHS:
            findings.append(
                f"{rel}: connected skill (requires_driver={rd!r}) has "
                f"data_path={dp!r} — a connected add-on must be 'mcp_tools' or 'local'."
            )
        tools = meta.get("uses_tools")
        if isinstance(tools, list):
            for tool in tools:
                if not isinstance(tool, str):
                    continue
                if not _driver_owns_tool(tool, rd):
                    findings.append(
                        f"{rel}: connected skill (requires_driver={rd!r}) lists a "
                        f"uses_tools entry {tool!r} that is not driver-owned — every "
                        f"tool must belong to the '{rd}' driver (contain its id)."
                    )
    return findings


def scan(root: Path | None = None) -> int:
    if root is None:
        root = REPO_ROOT
    findings: list[str] = []
    drivers = _load_driver_dicts(root)

    # --- Safety scan (preserved exactly; now root-parameterized) ---
    never_call_forms, never_set_forms = _forbidden_surface(drivers)
    call_res = {tool: re.compile(re.escape(tool)) for tool in never_call_forms}
    set_res = {
        tool: [(field, _active_field_pattern(field)) for field in fields]
        for tool, fields in never_set_forms.items()
    }
    tool_res = {tool: re.compile(re.escape(tool)) for tool in never_set_forms}

    for rel, text in _skill_bodies(root):
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

    # --- Conformance scan (spec §6), merged into the same findings list ---
    conformance = _check_conformance(root, drivers)

    if findings or conformance:
        total = len(findings) + len(conformance)
        print(f"FAIL: {total} connector issue(s):\n")
        if findings:
            print("Safety (BOS never activates):")
            for fnd in findings:
                print(f"  {fnd}")
            print("\nBOS creates PAUSED shells and stops. It never calls "
                  "ads_activate_entity and never sets a status field to ACTIVE via "
                  "ads_update_entity (spec §8 Layer 3). The owner reviews in Ads "
                  "Manager and switches it on themselves. Remove the activation and "
                  "re-run.")
        if conformance:
            if findings:
                print()
            print("Conformance (spec §6 — kind / requires_driver / connect.md + card "
                  "/ connected frontmatter):")
            for fnd in conformance:
                print(f"  {fnd}")
            print("\nEvery driver that ships a DRIVER dict must declare a canonical "
                  "kind, every skill's requires_driver must resolve, a connected "
                  "driver needs connect.md and a connectors.md card, and its "
                  "connected skills must honor the frontmatter contract. Fix the "
                  "above and re-run.")
        return 2

    print("OK: no ads activation paths in any skill body "
          "(no ads_activate_entity call, no status=ACTIVE via ads_update_entity), "
          "and every connector conforms (kind, requires_driver, connect.md + card, "
          "connected frontmatter).")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Connector safety + conformance gate (spec §5/§6)."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=REPO_ROOT,
        help="Repo root to scan (defaults to the real repo; tests point it at a "
             "self-contained fixture tree).",
    )
    args = parser.parse_args(argv)
    return scan(args.root.resolve())


if __name__ == "__main__":
    sys.exit(main())
