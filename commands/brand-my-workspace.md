---
description: Point at the user's website, infer brand colours + logo + name, write `brand/brand.json` + drop assets, then sync them into every studio's `public/`. Every BOS studio is rebranded in one shot.
---

Run the **Brand My Workspace** skill.

Invoke the skill at `skills/brand-my-workspace/SKILL.md`. If the user
didn't give a URL with the command, ask once: "What's the URL of the
website I should pull your brand from?" Then follow the skill's 11
steps in order: fetch the homepage, find the logo, detect colours, set
the name + tagline, compose the gradients, write `brand/brand.json`,
sync the assets into every studio's `public/`.

Preserve any field you can't determine confidently — keep the existing
default rather than guessing.

When done, summarise what changed (brand name, primary colour, accent
colour, logo path, studios synced) and remind the user to hard-refresh
their studio tabs.
