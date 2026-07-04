"""Inline a self-contained design system into an instantiated site-starter copy.

Task 1.3 of the Site Builder plan. When `design-my-site` copies
`templates/site-starter/` into an owner's workspace as THEIR project, this
helper writes a standalone `styles/tokens.css` + `design-system.json` from the
owner's brand plus the skill's derived per-project token overrides. After it
runs, the copied project depends on NOTHING in the BOS repo, no `../../../brand`
path, no shared JSON. That is what makes an instantiated site portable and
deployable on its own.

Purity contract (see tests/test_inline_design_system.py):
  - `inline(project_dir, brand, overrides)` is a PURE function: it deep-merges
    `overrides` over `brand`, writes the two files, and returns the merged dict.
    It does not mutate its inputs, read any key, or touch the network.
  - The skill body is what reads `brand/brand.json` and the derived overrides
    (persisted to ~/.claude/bos-cache/site-builder-profile.json) and passes them
    in. This helper never reads those sources itself.

Var-name alignment (the load-bearing contract):
  The generated tokens.css uses the SAME CSS-variable names that
  templates/site-starter/styles/tokens.css declares and
  templates/site-starter/tailwind.config.js reads. brand/defaults/brand.json
  uses camelCase colour keys (primaryDeep, pageBg, textMuted); the starter's CSS
  vars are kebab-case (--color-primary-deep, --color-page-bg,
  --color-text-muted). COLOR_VAR_MAP below is the single source of that mapping,
  so an instantiated copy's components actually consume the tokens.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

# --- The var-name contract with templates/site-starter -----------------------
# Maps a brand.json colour key (camelCase) -> the CSS variable the starter's
# components + tailwind.config.js read (kebab-case). Keep this in lockstep with
# templates/site-starter/styles/tokens.css and tailwind.config.js.
COLOR_VAR_MAP = {
    "primary": "--color-primary",
    "primaryDeep": "--color-primary-deep",
    "accent": "--color-accent",
    "text": "--color-text",
    "textMuted": "--color-text-muted",
    "panel": "--color-panel",
    "border": "--color-border",
    "pageBg": "--color-page-bg",
}

# Fonts: brand.json fonts.* keys -> the starter's CSS var names.
FONT_VAR_MAP = {
    "primary": "--font-sans",
    "serif": "--font-serif",
}

# The starter declares the full radius scale --radius-sm/md/lg/full. Pin every
# rung so a project's radius is a deliberate choice, never a design-tool default
# (web-design-method.md Part 4, lever 2). Overrides win; these are the fallback.
RADIUS_KEYS = ("sm", "md", "lg", "full")
RADIUS_DEFAULTS = {"sm": "4px", "md": "8px", "lg": "16px", "full": "9999px"}


def _deep_merge(base: dict, over: dict) -> dict:
    """Return a new dict: `over` recursively merged over `base`. Inputs untouched."""
    out = copy.deepcopy(base)
    for key, value in over.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _deep_merge(out[key], value)
        else:
            out[key] = copy.deepcopy(value)
    return out


def _render_tokens_css(ds: dict) -> str:
    """Render the merged design system as a self-contained tokens.css.

    Only emits vars for keys present in the merged system (plus the pinned full
    radius scale), using the starter's exact var names via COLOR_VAR_MAP /
    FONT_VAR_MAP. No import of brand.json, no ../../../brand path.
    """
    colors = ds.get("colors", {})
    fonts = ds.get("fonts", {})
    radius = ds.get("radius", {})

    color_lines = [
        f"  {COLOR_VAR_MAP[key]}: {value};"
        for key, value in colors.items()
        if key in COLOR_VAR_MAP
    ]
    font_lines = [
        f"  {FONT_VAR_MAP[key]}: {value};"
        for key, value in fonts.items()
        if key in FONT_VAR_MAP
    ]
    radius_lines = [
        f"  --radius-{key}: {radius.get(key, RADIUS_DEFAULTS[key])};"
        for key in RADIUS_KEYS
    ]

    blocks = [
        "/*",
        " * Design-system tokens for THIS site (self-contained).",
        " *",
        " * Written by inline_design_system.py when the site-builder instantiated",
        " * this project. These CSS variables ARE the design system: every component",
        " * reads them (directly or via the Tailwind theme map), so changing a token",
        " * here reskins the whole site. This file carries no dependency on the BOS",
        " * repo, it is free-standing on purpose.",
        " */",
        "",
        ":root {",
    ]
    if color_lines:
        blocks.append("  /* Colour tokens */")
        blocks.extend(color_lines)
        blocks.append("")
    if font_lines:
        blocks.append("  /* Typography */")
        blocks.extend(font_lines)
        blocks.append("")
    blocks.append("  /* Radius scale (pinned: a deliberate choice, never a tool default) */")
    blocks.extend(radius_lines)
    blocks.append("}")
    blocks.append("")
    return "\n".join(blocks)


def inline(project_dir, brand: dict, overrides: dict) -> dict:
    """Write a self-contained tokens.css + design-system.json into project_dir.

    Args:
        project_dir: the instantiated site-starter copy (a path-like).
        brand:       the owner's brand dict (shape of brand/brand.json).
        overrides:   the skill's derived per-project token overrides.

    Returns:
        The merged design-system dict (overrides deep-merged over brand). The
        same dict is written to design-system.json for /design-sync.
    """
    project_dir = Path(project_dir)
    merged = _deep_merge(brand or {}, overrides or {})

    styles_dir = project_dir / "styles"
    styles_dir.mkdir(parents=True, exist_ok=True)
    (styles_dir / "tokens.css").write_text(_render_tokens_css(merged), encoding="utf-8")

    (project_dir / "design-system.json").write_text(
        json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return merged
