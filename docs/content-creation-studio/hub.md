# Content Creation Studio — the hub

**Status:** live, module one shipping. Owner of the umbrella brand + the module
convention. Design spec: [`../architecture/2026-07-09-content-creation-studio-design.md`](../architecture/2026-07-09-content-creation-studio-design.md).

## What the hub is

The **Content Creation Studio** is an umbrella for the content-production modules
a BOS owner uses to make professional media on their own brand, keyless from day
one. It is deliberately thin: a brand + a convention, not a framework. We do not
over-build an umbrella layer before there is a second module (YAGNI). The hub
reserves the *shape* so modules can grow into it.

**Promise:** high-quality media is no longer outside an owner's reach. Every
module renders on the owner's own `brand/brand.json`, with no accounts and no API
keys on the default path.

## The modules

| Module | Folder | What it makes | Status |
|---|---|---|---|
| **Motion** (video engine) | `studio/motion/` | Brand-driven motion-graphics video (MP4) from a `<slug>.scenes.json` plan. Faceless today; talking-head and product-demo are later phases. | Module one — shipping |

Future modules (voiceover, audio, and others named in the spec) attach under the
same hub brand as they ship. This table is the registry; add a row when a module
lands rather than describing modules in prose that rots.

## How a module attaches

A module is a direct child of `studio/` with its own `public/` folder, and it:

1. **Shares the BOS brand system.** It reads the root `brand/brand.json` through
   its own `src/brand.js` loader (byte-identical pattern to the still studios), so
   editing the brand once — or running `/brand-my-workspace` — reskins every
   module. `tools/sync-brand.py` auto-discovers any `studio/<module>/` that has a
   `public/` and pushes the logo + favicons on dev-server restart, no code change.
2. **Speaks the shared file contract.** It reads the same `<slug>.script.json`
   and emits the same `<slug>.timing.json` shape as the rest of the content
   factory (design spec §3.4), so `script-my-video`, `make-thumbnail`, and
   `package-my-video` drive it unchanged. A module may add a sidecar (Motion adds
   `<slug>.scenes.json`) but never rewrites the script.
3. **Owns its craft in its own `CLAUDE.md`.** The module's operating manual is the
   one home for its render reality and craft rules; the hub does not restate them.
4. **Is keyless on the default path.** Any keyed capability is a clearly-labelled
   upgrade rung, degrading gracefully to the keyless floor when no key is present.

## The guided owner flow (Motion module)

The owner never edits a composition or types a render flag. Two skills drive the
Motion module:

- **`design-my-scenes`** (keyless) — turns a script or a topic into a
  `<slug>.scenes.json` visual plan, auto-defaulting the style and per-beat visual
  devices. It does not interrogate the owner on art direction.
- **`make-my-video`** (`requires_driver: render`, keyless) — the DRAFT-FIRST flow:
  pick the mode, get or write the script, auto-plan the scenes, render a fast draft
  the owner reacts to, iterate one change at a time, then package for publishing.

The render engine and its contracts live in
[`../../studio/motion/CLAUDE.md`](../../studio/motion/CLAUDE.md).
