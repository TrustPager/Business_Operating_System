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
        a dict. Supports flat scalars (incl. quoted values containing `:`),
        `  - ` string lists, explicit empty lists (`key: []`), and bare `key:`
        empty values (kept as `""` so present-but-empty is distinct from
        absent). The frontmatter is flat by design — no nesting, no PyYAML.
        Returns {} when there is no frontmatter. Structurally invalid lines
        (mis-indented list items, nested mappings, orphan `  - ` items) raise
        ValueError rather than vanishing. This is the SINGLE parser owner;
        tools/lint-skill.py imports it instead of duplicating the logic.

    validate_manifest(meta) -> list[str]
        Return a list of human-readable errors (empty == valid).

## Manifest keys vs passthrough keys

A SKILL.md frontmatter dict mixes two concerns, and validate_manifest treats
them differently:

- **Manifest keys** — the capability contract this module owns. Required:
  function_slot, requires_driver, requires_credential, data_path. Optional:
  uses_tools, unlocks, reads_for_profile, status, requires_region.

- **Passthrough keys** — pre-existing non-manifest frontmatter that skills
  legitimately carry and that other tooling (Claude Code skill loading,
  lint-skill.py) reads: name, description, triggers, plus the two output-policy
  copy flags produces_customer_facing_copy and engagement_copy. These are ALLOWED
  and are NOT treated as "unknown" — but they are not validated here either;
  that's lint-skill.py's job. PASSTHROUGH_KEYS below is the authority; keep this
  list in step with it.

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
OPTIONAL_SCALAR_KEYS: tuple[str, ...] = ("status", "requires_region")

# Pre-existing non-manifest frontmatter keys skills legitimately carry. These
# are allowed and are NOT validated as manifest fields (lint-skill.py owns them).
PASSTHROUGH_KEYS: tuple[str, ...] = (
    "name", "description", "triggers", "produces_customer_facing_copy",
    # engagement_copy: the skill's output has to earn and hold attention (a video
    # script, a social post, ad copy, a nurture sequence, a content plan), so it
    # must route knowledge/storytelling-method.md. Functional documents and
    # operational service messages do not carry it. lint-skill.py enforces it; the
    # contract is in knowledge/content-rules.md.
    "engagement_copy",
)

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
        "deploy",
        "floor",
    }
)
REQUIRES_CREDENTIAL: frozenset[str] = frozenset({"none", "mcp", "key"})
DATA_PATHS: frozenset[str] = frozenset(
    {"reasoning_only", "mcp_tools", "fetch_rest", "local"}
)
STATUSES: frozenset[str] = frozenset({"active", "deprecated", "removed"})
# Allowed region values. Starts minimal (AU only); extend when a second region ships.
REGIONS: frozenset[str] = frozenset({"AU"})


# --- Parser --------------------------------------------------------------


# Indentation expected for a `  - item` list element (two spaces, then `- `).
_LIST_ITEM_PREFIX = "  - "


def _strip_quotes(value: str) -> str:
    """Strip a single pair of matching surrounding quotes, if present.

    ``"a: b"`` -> ``a: b``; ``'x'`` -> ``x``. A bare value is returned as-is.
    Only a matched leading+trailing pair of the SAME quote char is stripped,
    so an apostrophe inside prose (``it's``) is never touched.
    """
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> dict[str, Any]:
    """Extract the flat YAML-ish frontmatter block into a dict.

    The frontmatter contract is flat by design (no PyYAML): each line is one of
      * ``key: value``       — a scalar (value may itself contain ``:``);
                               surrounding matched quotes are stripped, so
                               ``key: "a: b"`` yields ``a: b``.
      * ``key: []``          — an explicit empty list.
      * ``key:``             — a key whose value is a following ``  - `` list,
                               OR (if no items follow) an empty value, kept as
                               ``""`` so it is *present-but-empty* rather than
                               silently absent.
      * ``  - item``         — one element of the most recent ``key:`` list.
      * a blank line         — closes any open list.

    Returns ``{}`` when there is no leading ``---`` frontmatter block.

    Hardened (P1 Task 5): structurally invalid lines no longer vanish. A list
    item at the wrong indent, a nested mapping (indented ``key: value``), or a
    ``  - `` item with no open list all raise ``ValueError`` so drift surfaces
    instead of producing a false pass. This is the single parser owner;
    tools/lint-skill.py imports it rather than carrying its own copy.
    """
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    block = text[4:end]

    out: dict[str, Any] = {}
    # The key opened by a bare ``key:`` line, awaiting its ``  - `` items. While
    # pending it is NOT yet committed to ``out`` — if no items arrive it resolves
    # to an empty string (present-but-empty).
    pending_key: str | None = None
    pending_has_items = False

    def _resolve_pending() -> None:
        nonlocal pending_key, pending_has_items
        if pending_key is not None and not pending_has_items:
            # A ``key:`` line with nothing following it: an empty value.
            out[pending_key] = ""
        pending_key = None
        pending_has_items = False

    for raw in block.splitlines():
        # Blank line: close any open list / resolve a dangling empty key.
        if not raw.strip():
            _resolve_pending()
            continue

        # A list element: must be exactly two-space indented (``  - ``) and
        # must belong to an open ``key:`` list.
        if raw.lstrip().startswith("- "):
            indent = len(raw) - len(raw.lstrip(" "))
            if indent != 2 or not raw.startswith(_LIST_ITEM_PREFIX):
                raise ValueError(
                    f"frontmatter: mis-indented list item (expected 2-space '  - '): {raw!r}"
                )
            if pending_key is None:
                raise ValueError(
                    f"frontmatter: list item with no preceding 'key:' opener: {raw!r}"
                )
            out.setdefault(pending_key, []).append(_strip_quotes(raw[len(_LIST_ITEM_PREFIX):].strip()))
            pending_has_items = True
            continue

        # Any other indented line is nested content — not part of the flat
        # contract. Reject it rather than silently dropping it.
        if raw[0] in (" ", "\t"):
            raise ValueError(
                f"frontmatter: unexpected indented (nested) line, flat schema only: {raw!r}"
            )

        # A new top-level key closes the previous open list / empty key.
        _resolve_pending()

        if ":" not in raw:
            raise ValueError(f"frontmatter: line is not 'key: value' or 'key:': {raw!r}")

        key, _, value = raw.partition(":")
        key = key.strip()
        value = value.strip()
        if not key:
            raise ValueError(f"frontmatter: empty key: {raw!r}")

        if value == "":
            # Bare ``key:`` — open a list / empty-value key, resolved later.
            pending_key = key
            pending_has_items = False
        elif value == "[]":
            # Explicit empty list, distinct from a missing key.
            out[key] = []
        else:
            out[key] = _strip_quotes(value)

    # End of block: resolve any still-open ``key:`` to an empty value.
    _resolve_pending()
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

    def _driver_owns_tool(tool: str, driver: Any) -> bool:
        """True if ``tool`` belongs to the skill's declared ``requires_driver``.

        Case-insensitive substring of the driver id within the tool's
        fully-qualified name (the driver id appears as a segment of its tools'
        names). ``none``/empty owns nothing. Mirrors lint-skill.py exactly so the
        two validators never disagree on the keyless-hosted-driver exception.
        """
        if not isinstance(driver, str) or not driver or driver == "none":
            return False
        return driver.lower() in tool.lower()

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

    # 4. Optional scalar enums.
    _check_enum(meta, "status", STATUSES, errors)
    _check_enum(meta, "requires_region", REGIONS, errors)

    # 4b. credential:none => no FOREIGN mcp__ tool in uses_tools. A keyless skill
    #     claims to run with zero accounts connected; listing an MCP tool it could
    #     only call through a connection is a contradiction (this is what catches a
    #     keyless app that quietly reaches into TrustPager, e.g. quote-from-photo's
    #     mcp__trustpager__list_products). The body-reference linter (lint-skill.py
    #     Task 3c) misses it because the tool IS declared; declaring it is the bug.
    #
    #     EXCEPTION: a keyless HOSTED driver (e.g. firecrawl) is credential-free but
    #     IS an MCP. A skill may own its OWN declared driver's tools. This mirrors
    #     lint-skill.py's _driver_owns_tool exception exactly, so the two validators
    #     agree: requires_driver: firecrawl + requires_credential: none may list
    #     mcp__firecrawl__* tools, while a foreign trustpager tool is still caught.
    if meta.get("requires_credential") == "none":
        tools = meta.get("uses_tools")
        driver = meta.get("requires_driver")
        if isinstance(tools, list):
            mcp_tools = [t for t in tools if isinstance(t, str) and t.startswith("mcp__")]
            for tool in mcp_tools:
                if _driver_owns_tool(tool, driver):
                    continue
                errors.append(
                    f"uses_tools: requires_credential is 'none' but lists a foreign "
                    f"mcp__ tool '{tool}': a keyless skill may only call its own "
                    f"keyless driver's tools; remove it or set requires_credential to 'mcp'"
                )

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
