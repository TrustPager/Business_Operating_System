#!/usr/bin/env python3
"""Skill manifest: parse + validate the capability contract in SKILL.md frontmatter.

P1 makes capability data-driven. Every skill's SKILL.md frontmatter carries a
small, flat **manifest** describing what the skill needs and does. A generator
(Task 2) reads these manifests into kernel/registry.json so the runtime can
decide — from data, not hardcoded logic — which skills are available given the
configured driver and credentials. Lint (Task 3) enforces the contract.

This module is the single source of truth for that contract. It exposes two
importable functions:

    parse_frontmatter(text) -> dict
        Lift the YAML-ish frontmatter block (between leading `---` fences) into
        a dict. Supports flat scalars and `  - ` string lists ONLY (the
        frontmatter is flat by design — no nesting, no PyYAML). Returns {} when
        there is no frontmatter. (Task 5 will harden this parser; for now it
        shares the same minimal logic used by tools/lint-skill.py.)

    validate_manifest(meta) -> list[str]
        Return a list of human-readable errors (empty == valid).

## Manifest keys vs passthrough keys

A SKILL.md frontmatter dict mixes two concerns, and validate_manifest treats
them differently:

- **Manifest keys** — the capability contract this module owns. Required:
  function_slot, requires_driver, requires_credential, data_path. Optional:
  uses_tools, unlocks, reads_for_profile, status.

- **Passthrough keys** — pre-existing non-manifest frontmatter that skills
  legitimately carry and that other tooling (Claude Code skill loading,
  lint-skill.py) reads: name, description, triggers. These are ALLOWED and are
  NOT treated as "unknown" — but they are not validated here either; that's
  lint-skill.py's job.

Any key that is neither a manifest key nor a passthrough key is "unknown" and
is reported as an error, so typos and drift get caught.

The decision these enums encode (founder decision D8): TrustPager apps run on
the MCP data path (`data_path: mcp_tools`, `requires_credential: mcp`); floor
apps are reasoning-only (`data_path: reasoning_only`, `requires_credential:
none`, `requires_driver: none`).
"""

from __future__ import annotations

from typing import Any

# --- The contract --------------------------------------------------------

# Required manifest keys (every skill must declare these).
REQUIRED_KEYS: tuple[str, ...] = (
    "function_slot",
    "requires_driver",
    "requires_credential",
    "data_path",
)

# Optional manifest list-typed keys.
OPTIONAL_LIST_KEYS: tuple[str, ...] = (
    "uses_tools",
    "unlocks",
    "reads_for_profile",
)

# Optional manifest scalar keys (with defaults applied by the generator, not here).
OPTIONAL_SCALAR_KEYS: tuple[str, ...] = ("status",)

# Pre-existing non-manifest frontmatter keys skills legitimately carry. These
# are allowed and are NOT validated as manifest fields (lint-skill.py owns them).
PASSTHROUGH_KEYS: tuple[str, ...] = ("name", "description", "triggers")

# Every key validate_manifest() recognises (manifest + passthrough).
KNOWN_KEYS: frozenset[str] = frozenset(
    REQUIRED_KEYS + OPTIONAL_LIST_KEYS + OPTIONAL_SCALAR_KEYS + PASSTHROUGH_KEYS
)

# Enum domains for scalar manifest fields.
FUNCTION_SLOTS: frozenset[str] = frozenset(
    {
        "crm",
        "accounting",
        "ads",
        "social",
        "creative",
        "comms",
        "documents",
        "money",
        "people",
        "strategy",
        "research",
        "floor",
    }
)
REQUIRES_CREDENTIAL: frozenset[str] = frozenset({"none", "mcp", "key"})
DATA_PATHS: frozenset[str] = frozenset(
    {"reasoning_only", "mcp_tools", "fetch_rest", "local"}
)
STATUSES: frozenset[str] = frozenset({"active", "deprecated", "removed"})


# --- Parser --------------------------------------------------------------


def parse_frontmatter(text: str) -> dict[str, Any]:
    """Extract the YAML-ish frontmatter block into a dict.

    Supports flat scalars (``key: value``) and ``  - item`` string lists only.
    Returns an empty dict when there is no leading ``---`` frontmatter block.

    Shares the minimal logic used by tools/lint-skill.py so the two don't drift;
    Task 5 will replace this with a hardened parser.
    """
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    block = text[4:end]
    out: dict[str, Any] = {}
    current_list_key: str | None = None
    for line in block.splitlines():
        if not line.strip():
            current_list_key = None
            continue
        if line.startswith("  - "):
            if current_list_key:
                out.setdefault(current_list_key, []).append(line[4:].strip())
            continue
        if ": " in line:
            k, v = line.split(": ", 1)
            k = k.strip()
            v = v.strip()
            if v:
                out[k] = v
                current_list_key = None
            else:
                current_list_key = k
        elif line.endswith(":"):
            current_list_key = line[:-1].strip()
    return out


# --- Validator -----------------------------------------------------------


def _check_enum(meta: dict[str, Any], key: str, allowed: frozenset[str],
                errors: list[str]) -> None:
    """If ``key`` is present, ensure its value is a scalar in ``allowed``."""
    if key not in meta:
        return
    value = meta[key]
    if isinstance(value, list):
        errors.append(f"{key}: expected a single value, got a list")
        return
    if value not in allowed:
        allowed_str = ", ".join(sorted(allowed))
        errors.append(f"{key}: '{value}' is not allowed (expected one of: {allowed_str})")


def validate_manifest(meta: dict[str, Any]) -> list[str]:
    """Return a list of human-readable errors for a manifest dict (empty == valid).

    Checks, in order:
      1. all required keys present;
      2. each enum field's value is in its allowed set;
      3. uses_tools / unlocks / reads_for_profile are lists if present;
      4. status (optional) is a valid enum if present;
      5. no unknown keys beyond the manifest + passthrough schema.
    """
    errors: list[str] = []

    # 1. Required keys present.
    for key in REQUIRED_KEYS:
        if key not in meta:
            errors.append(f"missing required key: {key}")

    # 2. Enum fields (only checked when present; absence handled above).
    _check_enum(meta, "function_slot", FUNCTION_SLOTS, errors)
    _check_enum(meta, "requires_credential", REQUIRES_CREDENTIAL, errors)
    _check_enum(meta, "data_path", DATA_PATHS, errors)
    # requires_driver is a free-form driver id or the literal 'none' — only
    # constrained to be a non-empty scalar.
    if "requires_driver" in meta:
        rd = meta["requires_driver"]
        if isinstance(rd, list):
            errors.append("requires_driver: expected a single value, got a list")
        elif not isinstance(rd, str) or not rd.strip():
            errors.append("requires_driver: must be a non-empty driver id or 'none'")

    # 3. Optional list-typed fields must be lists if present.
    for key in OPTIONAL_LIST_KEYS:
        if key in meta and not isinstance(meta[key], list):
            errors.append(f"{key}: must be a list (use '  - item' lines), got a scalar")

    # 4. Optional status enum.
    _check_enum(meta, "status", STATUSES, errors)

    # 5. Unknown keys (anything outside manifest + passthrough).
    for key in meta:
        if key not in KNOWN_KEYS:
            errors.append(f"unknown key: {key}")

    return errors


if __name__ == "__main__":  # pragma: no cover - tiny CLI for ad-hoc checks
    import sys
    from pathlib import Path

    if len(sys.argv) != 2:
        print("usage: python tools/manifest.py skills/<name>/SKILL.md", file=sys.stderr)
        raise SystemExit(2)
    md = Path(sys.argv[1])
    parsed = parse_frontmatter(md.read_text(encoding="utf-8"))
    problems = validate_manifest(parsed)
    if not problems:
        print(f"OK — {md} manifest is valid.")
        raise SystemExit(0)
    print(f"{md} manifest has {len(problems)} problem(s):")
    for p in problems:
        print(f"  - {p}")
    raise SystemExit(1)
