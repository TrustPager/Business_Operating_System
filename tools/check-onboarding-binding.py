#!/usr/bin/env python3
"""Bind the shipped onboarding surface to kernel/registry.json (Floor Wave 0).

The onboarding surface — `skills/start-here/SKILL.md`, `skills/whats-possible/
SKILL.md`, `knowledge/starter-projects.md` — is what a brand-new owner sees on
day one. It must never advertise an app that doesn't exist, dress a connected-tier
app up as a keyless instant-win, smuggle TrustPager coupling into a skill that
claims to be keyless, or surface an Australia-only app outside an explicitly
AU-gated section of the onboarding surface. The registry (`kernel/registry.json`,
generated from the skill manifests) is the single source of truth for what is real
and what is keyless; this checker makes "onboarding only ever offers real, keyless
wins" a checked invariant.

Four assertions:

  A (exists) — every app-id the surface references is a registry key with
      ``status: active``. A reference to an app with no registry entry (a phantom)
      FAILS, naming the offending ids and where they were referenced.

  B (keyless honesty) — any app the surface offers as a keyless win (tagged
      ``[live]`` + a keyless tag, or routed as a cold instant-win in start-here)
      must be ``requires_credential: none`` AND ``requires_driver`` in
      {none, markitdown, render, firecrawl, doclib}. A keyless-offered app the registry
      marks ``mcp``/``trustpager`` (or any non-keyless driver) FAILS. EXEMPT:
      apps explicitly tagged ``better_with_crm`` / ``needs_crm``, or placed in a
      non-routable "Planned" / "coming soon" section — those are honestly flagged
      connected-tier / unbuilt.

  C (no hidden coupling) — no ``requires_credential: none`` skill's SKILL.md body
      contains a TrustPager coupling token: an ``mcp__trustpager__*`` tool, a
      ``dump-crm-bundle`` / ``dump-transcripts`` script call, or an
      ``api.trustpager.com`` URL. FAILS naming the skill + the token.

  D (region honesty) — any app whose registry entry has ``requires_region`` set
      (e.g. ``requires_region: AU``) must ONLY be referenced from within a section
      of the onboarding surface that is explicitly AU-gated: either a heading that
      satisfies ``is_au_gated_heading`` (names Australia / Australian / the
      uppercase acronym AU), or a row/line carrying the inline tag
      ``requires_region:au``. A region-restricted app that appears in any UNMARKED
      context (including a plain keyless offer) FAILS D. D overrides B: even if an
      AU-only app is technically ``requires_credential: none``, surfacing it in an
      unmarked keyless offer is a D failure.

Exit codes:
    0 — clean (prints a one-line OK)
    1 — at least one A/B/C/D failure (prints a grouped report)

Runnable as ``python tools/check-onboarding-binding.py`` and import-testable
(``check_onboarding_binding(...)`` returns the list of failure strings).

Python stdlib only. No network, no key.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

# --- The keyless contract (mirrors the plan / whats-possible) -------------
#
# Keyless = requires_credential: none AND a driver that runs locally / keyless-
# hosted. A remote driver like trustpager needs a connection, so it is NOT keyless
# even if credential were somehow "none".
_KEYLESS_DRIVERS: frozenset[str] = frozenset({"none", "markitdown", "render", "firecrawl", "doclib"})

# Honest connected-tier / unbuilt tags that EXEMPT a reference from B (and, in a
# Planned section, from A too). These say "this isn't a keyless instant-win" out loud.
_CONNECTED_TIER_TAGS: frozenset[str] = frozenset({"better_with_crm", "needs_crm"})

# Backticked tokens that look like app-ids but are external harness/driver commands,
# not BOS registry apps — the keyless Firecrawl driver surfaces these. They are not
# subject to A (they are not registry keys and never will be).
_EXTERNAL_TOKENS: frozenset[str] = frozenset(
    {"firecrawl-scrape", "firecrawl-search", "firecrawl-crawl", "firecrawl-map",
     "firecrawl-agent", "firecrawl-download", "firecrawl-instruct"}
)

# TrustPager coupling tokens that must never appear in a credential:none body (C).
_COUPLING_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("mcp__trustpager__ tool", re.compile(r"mcp__trustpager__[A-Za-z0-9_]+")),
    ("dump-crm-bundle script", re.compile(r"dump-crm-bundle")),
    ("dump-transcripts script", re.compile(r"dump-transcripts")),
    ("api.trustpager.com URL", re.compile(r"api\.trustpager\.com")),
)

# A backticked token shaped like an app-id / command: kebab-case, optional leading
# slash (command form), no dots or internal slashes (so file paths are excluded).
_APP_ID_RE = re.compile(r"\A/?([a-z][a-z0-9]*(?:-[a-z0-9]+)+)\Z")

# Any backticked span in the markdown.
_BACKTICK_RE = re.compile(r"`([^`]+)`")

# A non-routable "Planned" / "coming soon" section heading. Matched on the heading
# text after the leading ``#`` markers.
_PLANNED_HEADING_RE = re.compile(r"planned|coming soon|not yet built|unbuilt", re.IGNORECASE)

# An inline "Planned" / not-yet-built flag on a single non-table line. Bullets/prose
# outside a Planned heading flag a not-yet-built app inline — either the word
# "planned" / "coming soon", or the ``[floor-new]`` build-status tag. A line carrying
# one is treated as Planned-exempt from A, the prose analogue of the section heading.
_PLANNED_INLINE_RE = re.compile(
    r"\bplanned\b|coming soon|not yet built|unbuilt|\[floor-new\]", re.IGNORECASE
)

# Build-status tags used in starter-projects rows.
_LIVE_TAG = "[live]"

# Concrete AU-gated section marker. A heading gates the section (every reference
# inside is AU-gated) only when it explicitly names Australia. The gate is STRICT:
#   - the geographic word ``Australia`` / ``Australian`` matches case-INSENSITIVELY
#     (so lowercase prose ``australia`` still gates);
#   - the bare acronym matches only the uppercase token ``AU`` case-SENSITIVELY,
#     so a bare lowercase word ``au`` (``au revoir``, ``review au integrations``)
#     never gates.
# Two patterns, not one, because the acronym branch needs case-sensitivity the
# geographic branch must not have. ``is_au_gated_heading`` combines them.
_AU_GATED_WORD_RE = re.compile(r"\baustrali(?:a|an)\b", re.IGNORECASE)
_AU_GATED_ACRONYM_RE = re.compile(r"\bAU\b")  # case-sensitive: only uppercase AU


def is_au_gated_heading(heading: str) -> bool:
    """True if a heading explicitly names Australia (strict AU gate).

    Matches ``Australia`` / ``Australian`` case-insensitively, OR the uppercase
    acronym ``AU`` case-sensitively. A bare lowercase ``au`` word never gates.
    """
    return bool(_AU_GATED_WORD_RE.search(heading) or _AU_GATED_ACRONYM_RE.search(heading))

# Inline AU-gated row/line tag. A table row or non-table line carrying this literal
# tag is treated as AU-gated for that reference, mirroring how ``better_with_crm``
# and ``needs_crm`` classify a row without requiring a section heading.
_AU_GATED_INLINE_TAG = "requires_region:au"


# --- Loading --------------------------------------------------------------


def _repo_root() -> Path:
    """Repo root = the parent of this tools/ directory."""
    return Path(__file__).resolve().parent.parent


def load_registry(path: Path | None = None) -> dict[str, Any]:
    """Load kernel/registry.json (default: <repo>/kernel/registry.json)."""
    if path is None:
        path = _repo_root() / "kernel" / "registry.json"
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _split_body(text: str) -> str:
    """Return the markdown body after a leading ``---`` frontmatter fence (if any)."""
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    if end < 0:
        return text
    return text[end + 4:]


def _is_active(registry: dict[str, Any], app_id: str) -> bool:
    entry = registry.get(app_id)
    return bool(entry) and entry.get("status", "active") == "active"


def _is_keyless(registry: dict[str, Any], app_id: str) -> bool:
    """True if the registry marks ``app_id`` as a keyless win."""
    entry = registry.get(app_id) or {}
    return (
        entry.get("requires_credential") == "none"
        and entry.get("requires_driver") in _KEYLESS_DRIVERS
    )


# --- Reference extraction -------------------------------------------------


class Reference:
    """One app-id reference found on the surface, with the context that gates it.

    ``offered_keyless`` — the surface presents it as a cold keyless win (a start-here
        route, or a starter-projects row tagged keyless / [live]+keyless).
    ``connected_tier`` — explicitly tagged better_with_crm / needs_crm (exempt from B).
    ``planned`` — sits in a non-routable Planned / coming-soon section (exempt from A & B).
    ``au_gated`` (D): the reference sits inside an AU-gated section (a heading that
        satisfies ``is_au_gated_heading``) or the row/line carries the
        ``requires_region:au`` inline tag. Required for D: a ``requires_region``
        app is valid only when au_gated is True.
    """

    __slots__ = ("app_id", "source", "offered_keyless", "connected_tier", "planned",
                 "au_gated")

    def __init__(self, app_id: str, source: str, *, offered_keyless: bool,
                 connected_tier: bool, planned: bool, au_gated: bool = False):
        self.app_id = app_id
        self.source = source
        self.offered_keyless = offered_keyless
        self.connected_tier = connected_tier
        self.planned = planned
        self.au_gated = au_gated


def _backticked_app_ids(text: str) -> list[str]:
    """All app-id-shaped backticked tokens in ``text`` (leading slash stripped)."""
    out: list[str] = []
    for span in _BACKTICK_RE.findall(text):
        m = _APP_ID_RE.match(span.strip())
        if m:
            out.append(m.group(1))
    return out


def extract_start_here_refs(body: str, source: str = "start-here") -> list[Reference]:
    """Routing tokens in start-here are cold keyless instant-win offers.

    start-here may only route to keyless apps (it is the cold entry path), so every
    app-id it backticks is treated as ``offered_keyless`` — subject to A and B. Known
    external driver commands (firecrawl-*) are dropped. start-here has no section
    headings, so AU-gated context is detected only by an inline ``requires_region:au``
    tag on the same line as the app-id backtick.
    """
    refs: list[Reference] = []
    seen: set[str] = set()
    for line in body.splitlines():
        au_gated = _AU_GATED_INLINE_TAG in line.lower()
        for app_id in _backticked_app_ids(line):
            if app_id in _EXTERNAL_TOKENS or app_id in seen:
                continue
            seen.add(app_id)
            refs.append(Reference(app_id, source, offered_keyless=True,
                                  connected_tier=False, planned=False,
                                  au_gated=au_gated))
    return refs


def extract_whats_possible_refs(body: str, source: str = "whats-possible") -> list[Reference]:
    """whats-possible reads the registry at runtime; any app-id it names is checked
    for existence (A) but not asserted keyless (it deliberately shows both tiers).
    AU-gated context is detected by an inline ``requires_region:au`` tag on the
    same line as the app-id backtick, or a heading satisfying ``is_au_gated_heading``.
    """
    refs: list[Reference] = []
    seen: set[str] = set()
    in_au_section = False
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            heading = stripped.lstrip("#").strip()
            in_au_section = is_au_gated_heading(heading)
            continue
        au_gated = in_au_section or _AU_GATED_INLINE_TAG in line.lower()
        for app_id in _backticked_app_ids(line):
            if app_id in _EXTERNAL_TOKENS or app_id in seen:
                continue
            seen.add(app_id)
            refs.append(Reference(app_id, source, offered_keyless=False,
                                  connected_tier=False, planned=False,
                                  au_gated=au_gated))
    return refs


def extract_starter_projects_refs(text: str, source: str = "starter-projects"
                                  ) -> list[Reference]:
    """Parse starter-projects.md row by row, binding each backticked app-id to its
    build-status tag, its keyless/CRM tag, and whether it sits in a Planned section.

    Robust to the markdown: we don't assume strict column positions. For each table
    row (a line containing ``|``), we read every backticked app-id in the row, and
    classify the row by the tags present anywhere in it:
      - ``planned`` if we're under a Planned / coming-soon heading;
      - ``connected_tier`` if the row carries a better_with_crm / needs_crm tag;
      - ``offered_keyless`` if the row carries the literal ``keyless`` tag and a
        ``[live]`` build-status tag (a live, keyless-offered app).

    Non-table lines (bullets / prose) can also name a buildable app, so a phantom
    smuggled into a bullet must not evade A. For each non-heading line *without* a
    ``|``, we emit every backticked app-id as a bare existence reference
    (``offered_keyless=False`` — a bullet carries no per-row keyless/CRM tag, so we
    can't classify it as a keyless *offer*; that's B's job, table-rows only). The
    Planned flag is honored: a bullet under a Planned heading, or one carrying an
    inline Planned / ``[floor-new]`` flag, stays exempt from A — same as a table row.
    """
    refs: list[Reference] = []
    in_planned = False
    in_au_section = False

    for raw in text.splitlines():
        stripped = raw.strip()

        # Section heading: flip the Planned and AU-gated flags.
        if stripped.startswith("#"):
            heading = stripped.lstrip("#").strip()
            in_planned = bool(_PLANNED_HEADING_RE.search(heading))
            in_au_section = is_au_gated_heading(heading)
            continue

        # Non-table line (bullet / prose). Still subject to A (existence) so a phantom
        # named here can't evade assertion. Not subject to B: a bullet has no per-row
        # keyless/CRM tag to classify it as a keyless offer. A line is Planned-exempt
        # when under a Planned heading OR carrying an inline Planned / [floor-new] flag.
        # AU-gated when under an AU-gated heading OR the line carries the inline tag.
        if "|" not in raw:
            line_planned = in_planned or bool(_PLANNED_INLINE_RE.search(raw))
            line_au_gated = in_au_section or _AU_GATED_INLINE_TAG in raw.lower()
            for app_id in _backticked_app_ids(raw):
                refs.append(Reference(app_id, source, offered_keyless=False,
                                      connected_tier=False, planned=line_planned,
                                      au_gated=line_au_gated))
            continue

        app_ids = _backticked_app_ids(raw)
        if not app_ids:
            continue

        low = raw.lower()
        connected_tier = any(tag in low for tag in _CONNECTED_TIER_TAGS)
        # A row is a keyless offer when it carries the literal keyless tag AND at
        # least one [live] build-status tag (i.e. it claims to ship today, keyless).
        has_keyless_tag = bool(re.search(r"(?<![a-z_])keyless(?![a-z_])", low))
        has_live = _LIVE_TAG in low
        offered_keyless = has_keyless_tag and has_live and not connected_tier
        # AU-gated: either we are under an AU-gated heading, or the row carries the
        # inline ``requires_region:au`` tag.
        row_au_gated = in_au_section or _AU_GATED_INLINE_TAG in low

        for app_id in app_ids:
            refs.append(Reference(app_id, source, offered_keyless=offered_keyless,
                                  connected_tier=connected_tier, planned=in_planned,
                                  au_gated=row_au_gated))
    return refs


# --- The three assertions -------------------------------------------------


def _check_exists(registry: dict[str, Any], refs: Iterable[Reference]) -> list[str]:
    """A — every referenced app-id is an active registry key (Planned rows exempt)."""
    phantoms: dict[str, set[str]] = {}
    for ref in refs:
        if ref.planned:
            continue  # honestly flagged unbuilt; not offered as buildable now
        if not _is_active(registry, ref.app_id):
            phantoms.setdefault(ref.app_id, set()).add(ref.source)
    failures: list[str] = []
    for app_id in sorted(phantoms):
        srcs = ", ".join(sorted(phantoms[app_id]))
        failures.append(
            f"A (phantom): `{app_id}` is referenced ({srcs}) but is not an active "
            f"key in kernel/registry.json."
        )
    return failures


def _check_keyless_honesty(registry: dict[str, Any], refs: Iterable[Reference]
                           ) -> list[str]:
    """B — a keyless-offered app must be registry-keyless (exemptions applied)."""
    offenders: dict[str, set[str]] = {}
    for ref in refs:
        if ref.planned or ref.connected_tier:
            continue  # exempt: honestly flagged connected-tier / unbuilt
        if not ref.offered_keyless:
            continue
        if not _is_active(registry, ref.app_id):
            continue  # A already reports the phantom; don't double-count
        if not _is_keyless(registry, ref.app_id):
            offenders.setdefault(ref.app_id, set()).add(ref.source)
    failures: list[str] = []
    for app_id in sorted(offenders):
        entry = registry.get(app_id, {})
        cred = entry.get("requires_credential")
        drv = entry.get("requires_driver")
        srcs = ", ".join(sorted(offenders[app_id]))
        failures.append(
            f"B (dishonest keyless): `{app_id}` is offered as a keyless win ({srcs}) "
            f"but the registry marks it requires_credential={cred!r}, "
            f"requires_driver={drv!r} — not keyless. Retag it better_with_crm/needs_crm "
            f"or move it to a Planned section."
        )
    return failures


def _has_requires_region(registry: dict[str, Any], app_id: str) -> bool:
    """True if the registry entry for ``app_id`` has a non-empty ``requires_region``."""
    entry = registry.get(app_id) or {}
    region = entry.get("requires_region")
    return bool(region) and region != "none"


def _check_region_honesty(registry: dict[str, Any], refs: Iterable[Reference]
                          ) -> list[str]:
    """D -- a region-restricted app must only appear in an AU-gated context.

    Any reference to an app whose registry entry has ``requires_region`` set
    (e.g. ``requires_region: AU``) FAILS when the reference's ``au_gated`` flag
    is False. This catches an AU-only app slipping into a universal keyless offer
    or any unmarked section of the onboarding surface.

    D overrides B: a technically-keyless AU app in an unmarked section is a D
    failure even if B would pass it (B only checks credential/driver, not region).
    Planned references are still exempt (they are not offered at all).
    """
    offenders: dict[str, set[str]] = {}
    for ref in refs:
        if ref.planned:
            continue  # not offered; no gate needed
        if not _is_active(registry, ref.app_id):
            continue  # A already reports the phantom
        if not _has_requires_region(registry, ref.app_id):
            continue  # not region-restricted; D does not apply
        if not ref.au_gated:
            offenders.setdefault(ref.app_id, set()).add(ref.source)
    failures: list[str] = []
    for app_id in sorted(offenders):
        entry = registry.get(app_id, {})
        region = entry.get("requires_region")
        srcs = ", ".join(sorted(offenders[app_id]))
        failures.append(
            f"D (region leak): `{app_id}` has requires_region={region!r} but is "
            f"referenced outside an AU-gated section ({srcs}). Move it under a "
            f"heading matching 'Australia/AU' or tag the row/line with "
            f"'requires_region:au' — never offer a region-restricted app universally."
        )
    return failures


def _check_no_coupling(registry: dict[str, Any], skills_dir: Path) -> list[str]:
    """C — no credential:none skill body carries a TrustPager coupling token."""
    failures: list[str] = []
    for app_id in sorted(registry):
        entry = registry[app_id]
        if entry.get("requires_credential") != "none":
            continue
        skill_md = skills_dir / app_id / "SKILL.md"
        if not skill_md.is_file():
            continue
        body = _split_body(skill_md.read_text(encoding="utf-8"))
        for label, pat in _COUPLING_PATTERNS:
            m = pat.search(body)
            if m:
                failures.append(
                    f"C (hidden coupling): credential:none skill `{app_id}` body "
                    f"contains a {label} (`{m.group(0)}`) — a keyless skill must not "
                    f"reach into TrustPager. Decouple it or reclassify the manifest."
                )
    return failures


# --- Orchestration --------------------------------------------------------


def check_onboarding_binding(
    *,
    registry: dict[str, Any],
    start_here_path: Path,
    whats_possible_path: Path,
    starter_projects_path: Path,
    skills_dir: Path | None = None,
) -> list[str]:
    """Run A + B + C + D and return the (possibly empty) list of failure strings.

    A, B, and D scan the three surface files for referenced app-ids. C scans the
    bodies of every credential:none skill in ``skills_dir`` (defaults to the parent
    of ``start_here_path``'s skill folder). An empty return == clean.
    """
    refs: list[Reference] = []
    if start_here_path.is_file():
        refs += extract_start_here_refs(_split_body(start_here_path.read_text(encoding="utf-8")))
    if whats_possible_path.is_file():
        refs += extract_whats_possible_refs(_split_body(whats_possible_path.read_text(encoding="utf-8")))
    if starter_projects_path.is_file():
        refs += extract_starter_projects_refs(starter_projects_path.read_text(encoding="utf-8"))

    if skills_dir is None:
        # start_here_path is skills/start-here/SKILL.md → skills/ is two parents up.
        skills_dir = start_here_path.resolve().parent.parent

    failures: list[str] = []
    failures += _check_exists(registry, refs)
    failures += _check_keyless_honesty(registry, refs)
    failures += _check_no_coupling(registry, skills_dir)
    failures += _check_region_honesty(registry, refs)
    return failures


def _default_paths() -> dict[str, Path]:
    root = _repo_root()
    return {
        "start_here_path": root / "skills" / "start-here" / "SKILL.md",
        "whats_possible_path": root / "skills" / "whats-possible" / "SKILL.md",
        "starter_projects_path": root / "knowledge" / "starter-projects.md",
        "skills_dir": root / "skills",
    }


def main(argv: list[str] | None = None) -> int:
    paths = _default_paths()
    try:
        registry = load_registry()
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[onboarding-binding] FAIL: cannot read kernel/registry.json ({exc})",
              file=sys.stderr)
        return 1

    failures = check_onboarding_binding(registry=registry, **paths)

    if not failures:
        print("[onboarding-binding] OK — every onboarding offer is a real, keyless win.")
        return 0

    # Grouped report: A, then B, then C, then D, in the order produced (already
    # grouped because check_onboarding_binding runs A -> B -> C -> D).
    print(
        f"[onboarding-binding] FAIL: {len(failures)} drift issue(s) — the onboarding "
        "surface advertises apps that don't exist, aren't keyless, hide TrustPager "
        "coupling, or surface a region-restricted app outside a gated section:",
        file=sys.stderr,
    )
    groups = {"A": "A — phantom (no registry entry)",
              "B": "B — dishonest keyless offer",
              "C": "C — hidden TrustPager coupling",
              "D": "D — region leak (AU-only app in unmarked section)"}
    for key, title in groups.items():
        bucket = [f for f in failures if f.startswith(key + " ")]
        if not bucket:
            continue
        print(f"\n  {title}:", file=sys.stderr)
        for f in bucket:
            print(f"    - {f}", file=sys.stderr)
    print(
        "\n[onboarding-binding] Fix: bind every onboarding offer to an active, keyless "
        "registry app (or honestly retag / move to Planned). Region-restricted apps "
        "must live under an AU-gated heading or carry a requires_region:au inline tag. "
        "The registry is the source of truth.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
