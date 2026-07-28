# Capability tree

`capability-tree.png` — the one aspirational image Day 2 shows: the six floor
branches, the add-ons that build on top, and the summit goal everything builds
toward. Static, shown identically to every member every time, not tied to
anyone's real progress. See
`docs/architecture/2026-07-07-five-day-challenge-day2-redesign-design.md` for
the full history of how this got here (it started as a per-member progress
tracker, then was simplified to one static picture per founder direction).

## Source of truth (the premium render)

The shipped `capability-tree.png` is the **finished premium render**, identical
to the image the Day 2 lesson embeds. It is produced upstream by the
maintainer's own image studio (which leans on real photography and image
generation for its hero elements) and copied in byte-identical, so an owner
running Day 2 sees the premium picture, not a wireframe.

**To update:** re-copy the finished render over this file when it changes. Do
not hand-edit or regenerate this copy in-repo; the upstream studio owns the art.

## `build_tree.py` is SUPERSEDED — do not run it

`build_tree.py` is the old in-repo **wireframe** generator (Pillow + numpy, a
session-simple draw-it-in-code version). It has been replaced by the premium
render above and is kept only as history. **Do not run it:** it writes
`capability-tree.png` and would overwrite the premium render with the lower-bar
wireframe. If you ever need the wireframe for reference, render it to a different
filename, never over the shipped `capability-tree.png`.
