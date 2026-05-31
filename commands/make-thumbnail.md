---
description: Design and render a 1280×720 YouTube thumbnail for a tutorial video using the bundled studio. Browser preview → puppeteer-rendered PNG → optional one-command publish to your TrustPager Files folder.
---

Run the **Make Thumbnail** skill.

Invoke the skill at `skills/make-thumbnail/SKILL.md`. Read the three
canonical design-rules files in `studio/thumbnails/` first
(YOUTUBE_TITLES.md, the templates/YouTubeThumbnail.jsx JSDoc, and
heroes/index.js header) — those distil 22+ iterations of corrections
that you'll otherwise re-walk.

Confirm the brief with the operator (video topic, title, hero family),
add the design to samples.json, iterate in the browser at
localhost:3210, render to PNG via `npm run shoot <key>`, optionally
publish to their TrustPager workspace via `npm run publish <key>`.
