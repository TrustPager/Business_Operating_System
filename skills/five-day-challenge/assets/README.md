# Capability tree

`capability-tree.png` — the one aspirational image Day 2 shows: the six floor
branches, the add-ons that build on top, and the summit goal everything builds
toward. Static, shown identically to every member every time, not tied to
anyone's real progress. See
`docs/architecture/2026-07-07-five-day-challenge-day2-redesign-design.md` for
the full history of how this got here (it started as a per-member progress
tracker, then was simplified to one static picture per founder direction).

## Why a wireframe, not the premium version

This is the **session-simple** version, meant to be reproducible directly in
this repo with no dependency beyond Pillow. The **premium** version (glowing
core + skills radiating, matching AI BOS's real visual bar) is a separate
deliverable built in `AI-BOS/skool-studio/` for posting to Skool, following
`THUMBNAIL-RECIPE.md` and `DESIGN-LOG.md` in that project. Same content and
structure, different bar, different pipeline. Don't conflate the two, or try
to make this one hit the premium bar, that's the other project's job.

## How it's made

`build_tree.py` (Pillow + numpy) draws everything in code: a radial
near-black-teal background, hexagon nodes for the floor/add-on/scaling tiers,
a highlight box for the summit, and glowing connector lines. No AI image
generation involved, this is simple enough to just draw directly, unlike the
premium version which leans on real photography and TrustPager image-gen for
its hero elements.

Colors are TrustPager's teal brand tokens (ACCENT `#29c6c6`, ACCENT_DEEP
`#1f9d86`, ACCENT_SOFT `#7fe6da`, CYAN `#54e6d8`, INK `#f3f6ff`, BOX_INK
`#04201e`), hardcoded at the top of the script. They're deliberately NOT
pulled from `brand/brand.json`, that file is the neutral placeholder every
customer's BOS instance gets reskinned from; this asset is TrustPager/AI BOS's
own course material, not something a customer's brand should touch.

## The content (edit these dicts to change the tree)

- `BASE` — the six floor branches (from `docs/CAPABILITIES.md`)
- `TIER1` — add-ons, each with a `parent` pointing at its base branch
- `TIER2` — deeper add-ons (currently just Advanced Money Models, off Value
  Equation/Offer Tune-Up)
- `SUMMIT` — the single goal node everything converges into

Re-run `python build_tree.py` after any edit; it regenerates
`capability-tree.png` deterministically. Requires Pillow and numpy; Segoe UI
for the on-brand look (falls back to Pillow's default font elsewhere).
