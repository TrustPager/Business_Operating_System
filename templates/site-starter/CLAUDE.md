# Site Starter — Instructions for AI Assistants

You're in `templates/site-starter/` inside the Business Operating System. This
is the **committed lean Next.js starter** the site-builder instantiates. It
carries the seven-section conversion wireframe as components plus a
design-system-first token layer.

**Read [README.md](README.md) first** for the full picture. This file is the
short AI-facing version.

## What this is (and is not)

- It **is** a template: `design-my-site` copies this whole folder into an
  owner's workspace as *their* project, inlines their design system, and steers
  Claude Design to build off it.
- It is **not** a shared render studio like `studio/og`. Instantiated copies
  live in the owner's workspace and are never committed back into BOS.
- Only the **source** is committed here. `node_modules/` and `.next/` are
  gitignored and must never be committed.

## The two things you'll touch most

1. **`styles/tokens.css`** — the design system as CSS variables. Neutral
   defaults on purpose so the app builds standalone. `inline_design_system.py`
   overwrites this per project with the owner's brand + derived overrides,
   self-contained. **Never hardcode a hex or a font in a component** — add it as
   a token here.
2. **`components/sections/`** — the seven skeleton components + Nav + Footer.
   Each carries a first-line `{/* @dsCard group="sections" */}` JSX comment so
   Claude Design's Design System pane indexes it. Keep that marker on line 1 of
   any new section component, and keep it a JSX comment, never a raw HTML
   `<!-- -->` comment.

## Rules (do / don't)

- **DO** read design tokens as `var(--…)` CSS variables (directly or via the
  Tailwind theme map in `tailwind.config.js`). One token change reskins the site.
- **DO** keep the single **H1** in `Hero` only. Every other heading is an H2/H3.
  A page has exactly one H1 (on-page SEO, per `web-design-method.md` Part 3).
- **DO** keep the FAQ questions in `app/page.tsx` in sync between the visible
  `Faq` section and `FaqJsonLd` (they share one `faqItems` array on purpose).
- **DO** keep the font `<link>` in `app/layout.tsx` as the confirm-loading
  preconnect + stylesheet pattern so the typeface actually renders. If you swap
  the typeface, keep the wiring and verify it loads.
- **DON'T** fabricate testimonials, ratings, review counts, NAP, or hours. The
  placeholders are clearly marked; fill real data or leave the slot and say so.
- **DON'T** commit `node_modules/` or `.next/`.
- **DO** keep `package-lock.json` committed and in sync: if the skill or the
  inliner ever bumps a dependency, run `npm install` to regenerate the lockfile
  and recommit it, or `npm ci` (and the deploy) will fail on a mismatch.
- **DON'T** add an external asset or runtime dependency to keep it lean. The
  starter is only our components + a thin app shell + pinned deps.
- **DON'T** import `../../../brand` here. The instantiated copy must be
  self-contained; the inliner writes the tokens in.

## Build / run

```
npm install
npm run dev        # http://localhost:3220
npm run build      # clean static production build
```

Port 3220 avoids the studio ports (3210 / 3213 / 3216 / 3217).

## How /design-sync attaches

`/design-sync` reads this project's design system (the `@dsCard` markers +
`design-system.json` the inliner writes) so Claude Design PULLs the owner's
tokens and named components in, builds against them, and PUSHes code state back
into `components/`. It builds an explicit plan and returns a `planId` to approve;
it never overwrites silently.
