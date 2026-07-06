---
description: Design and render branded social posts for Instagram, LinkedIn, and X, ready to publish.
---

Run the **Make Social Post** skill.

Invoke the skill at `skills/make-social-post/SKILL.md`. Read the two
canonical design-rules files in `studio/social/` first (CLAUDE.md and the
templates/SocialPost.jsx JSDoc header) -- they hold the post anatomy, the
four formats, the data shape, and the brand rules.

Confirm the brief with the operator (which format(s), the one-line message,
the accent word, any visual), add the design to samples.json, iterate in the
browser at localhost:3216, render to PNG via `npm run shoot <key>`,
optionally publish to their TrustPager workspace via `npm run publish <key>`
if TrustPager is connected.
