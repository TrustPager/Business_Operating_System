# Capability tree

`capability-tree.png` — the one aspirational image Day 2 shows: the six floor
branches, the add-ons that build on top, and the summit goal everything builds
toward. Static, shown identically to every member every time, not tied to
anyone's real progress. See
`docs/architecture/2026-07-07-five-day-challenge-day2-redesign-design.md` for
the full history of how this got here (it started as a per-member progress
tracker, then was simplified to one static picture per founder direction).

## Source of truth (the premium render)

The shipped `capability-tree.png` is the **premium teal render**, matching AI
BOS's real visual bar and identical to the image the Day 2 lesson embeds. The
**source of truth is `AI-BOS/skool-assets/AI-BOS-capability-tree.png`**, built by
the skool-studio pipeline (`THUMBNAIL-RECIPE.md` + `DESIGN-LOG.md` in that
project, which leans on real photography and image generation for its hero
elements). The copy here is kept byte-identical to that source so an owner
running Day 2 sees the premium picture, not a wireframe.

**To update:** when the source render changes, re-copy it here
(`cp AI-BOS/skool-assets/AI-BOS-capability-tree.png skills/five-day-challenge/assets/capability-tree.png`).
Do not hand-edit or regenerate this copy in-repo; the skool-studio pipeline owns
the art.

## `build_tree.py` is SUPERSEDED — do not run it

`build_tree.py` is the old in-repo **wireframe** generator (Pillow + numpy, a
session-simple draw-it-in-code version). It has been replaced by the premium
render above and is kept only as history. **Do not run it:** it writes
`capability-tree.png` and would overwrite the premium render with the lower-bar
wireframe. If you ever need the wireframe for reference, render it to a different
filename, never over the shipped `capability-tree.png`.
