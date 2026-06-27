#!/usr/bin/env python3
"""Generate kernel/registry.json from skill manifests (P1 Task 2).

P1 makes capability data-driven. Each skill's SKILL.md frontmatter carries a
flat **manifest** (see tools/manifest.py for the contract). This generator
walks ``skills/*/SKILL.md``, lifts each manifest with the SHARED parser, and
emits a single ``kernel/registry.json`` the runtime reads to decide — from
data, not hardcoded logic — which skills are available for the configured
driver and credentials.

Design rules this module upholds:

- **One parser.** We reuse ``tools/manifest.py``'s ``parse_frontmatter`` and
  ``validate_manifest`` — we do NOT write a second/third parser.

- **A bad manifest can't dark the registry.** A skill with no manifest keys is
  silently skipped (it predates the contract / is intentionally manifest-free).
  A skill that declares manifest keys but fails validation is skipped with a
  warning to stderr. Either way, one broken skill never crashes the whole run.

- **Deterministic output.** Entries are keyed by skill folder name, the JSON is
  emitted with ``indent=2``, ``sort_keys=True`` and a trailing newline, so
  running the generator twice produces byte-identical output (and a clean git
  diff). ``status`` defaults to ``"active"`` when a manifest omits it.

- **registry.json is DATA, not kernel code.** It lives under ``kernel/`` for
  the runtime to find via ``plugin_root()``, but the vendor-neutral-kernel gate
  (tools/check-kernel-clean.py) only scans ``*.py``, so manifest values such as
  ``requires_driver: trustpager`` are fine here — they're driver ids, not
  secrets.

CLI:
    python tools/registry-generator.py            # write kernel/registry.json
    python tools/registry-generator.py --out PATH # write somewhere else

It prints a one-line summary to stderr (N included, M skipped).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Reuse the single source of truth for the manifest contract. tools/manifest.py
# has an import-safe name (no hyphen), so add tools/ to sys.path and import it
# directly rather than re-loading by path — this guarantees one parser, one
# validator, one schema.
_TOOLS_DIR = Path(__file__).resolve().parent
if str(_TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(_TOOLS_DIR))

from manifest import (  # noqa: E402  (path set above)
    OPTIONAL_LIST_KEYS,
    OPTIONAL_SCALAR_KEYS,
    REQUIRED_KEYS,
    parse_frontmatter,
    validate_manifest,
)

# The manifest fields (and only these) that get carried into a registry entry.
# Passthrough frontmatter (name/description/triggers) is deliberately excluded:
# the registry is the capability contract, not a copy of the skill's prose.
_MANIFEST_KEYS: tuple[str, ...] = (
    REQUIRED_KEYS + OPTIONAL_LIST_KEYS + OPTIONAL_SCALAR_KEYS
)

# A skill is considered to "have a manifest" if its frontmatter declares at
# least one manifest key. Frontmatter with only passthrough keys (or none) is
# treated as manifest-free and skipped silently.
_MANIFEST_KEY_SET = frozenset(_MANIFEST_KEYS)


def _has_manifest(meta: dict[str, Any]) -> bool:
    """True if the frontmatter declares any manifest key."""
    return any(key in meta for key in _MANIFEST_KEY_SET)


def _entry_from_manifest(meta: dict[str, Any]) -> dict[str, Any]:
    """Project a validated manifest dict down to its registry entry.

    Carries only manifest fields (required + optional) that are present, and
    applies the ``status`` default of ``"active"``.
    """
    entry: dict[str, Any] = {}
    for key in _MANIFEST_KEYS:
        if key in meta:
            entry[key] = meta[key]
    entry.setdefault("status", "active")
    return entry


def generate_registry(skills_dir: Path | str) -> dict[str, dict[str, Any]]:
    """Build the registry mapping ``skill_folder_name -> manifest entry``.

    Walks ``<skills_dir>/*/SKILL.md``. For each skill:
      - parse the frontmatter with the shared parser;
      - if it declares no manifest keys → skip silently (manifest-free skill);
      - else validate; if invalid → skip with a stderr warning;
      - else include an entry carrying the manifest fields (status defaulting
        to "active").

    Robust by design: a missing skills dir, an unreadable file, or a single
    bad manifest never raises — the worst case is a skipped skill and a warning.
    The returned dict is insertion-ordered by sorted skill name.
    """
    skills_dir = Path(skills_dir)
    registry: dict[str, dict[str, Any]] = {}

    if not skills_dir.is_dir():
        return registry

    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        name = skill_md.parent.name
        try:
            text = skill_md.read_text(encoding="utf-8")
        except OSError as exc:  # unreadable file — skip, don't crash
            print(f"[registry] skip {name}: cannot read SKILL.md ({exc})",
                  file=sys.stderr)
            continue

        try:
            meta = parse_frontmatter(text)
        except Exception as exc:  # defensive: a parser hiccup can't dark the run
            print(f"[registry] skip {name}: frontmatter parse failed ({exc})",
                  file=sys.stderr)
            continue

        if not _has_manifest(meta):
            # No manifest keys at all — predates the contract / intentionally
            # manifest-free. Skip silently (not a warning: this is expected
            # until Task 4 backfills the remaining skills).
            continue

        errors = validate_manifest(meta)
        if errors:
            print(
                f"[registry] skip {name}: invalid manifest — "
                + "; ".join(errors),
                file=sys.stderr,
            )
            continue

        registry[name] = _entry_from_manifest(meta)

    # Deterministic key order (sorted by skill name).
    return {name: registry[name] for name in sorted(registry)}


def serialize_registry(registry: dict[str, Any]) -> str:
    """Serialize the registry deterministically.

    indent=2, sort_keys=True, and a single trailing newline so two runs over
    the same inputs produce byte-identical text (clean git diffs).
    """
    return json.dumps(registry, indent=2, sort_keys=True) + "\n"


def _default_skills_dir() -> Path:
    """The repo's skills/ dir, resolved via plugin_root() when available."""
    try:
        sys.path.insert(0, str(_TOOLS_DIR.parent))
        from kernel.runtime.paths import plugin_root  # noqa: E402

        return plugin_root() / "skills"
    except Exception:
        # Fall back to the repo root computed from this file's location:
        # tools/ -> repo root -> skills/.
        return _TOOLS_DIR.parent / "skills"


def _default_out_path() -> Path:
    """kernel/registry.json under the resolved repo root."""
    return _default_skills_dir().parent / "kernel" / "registry.json"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate kernel/registry.json from skill manifests."
    )
    parser.add_argument(
        "--skills-dir",
        default=None,
        help="Directory containing skill folders (default: <repo>/skills).",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Output path (default: <repo>/kernel/registry.json).",
    )
    args = parser.parse_args(argv)

    skills_dir = Path(args.skills_dir) if args.skills_dir else _default_skills_dir()
    out_path = Path(args.out) if args.out else _default_out_path()

    registry = generate_registry(skills_dir)
    text = serialize_registry(registry)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")

    # How many skills did we look at vs include? Skipped = scanned - included.
    scanned = sum(1 for _ in Path(skills_dir).glob("*/SKILL.md")) \
        if Path(skills_dir).is_dir() else 0
    included = len(registry)
    skipped = scanned - included
    print(
        f"[registry] wrote {out_path} — {included} included, {skipped} skipped",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
