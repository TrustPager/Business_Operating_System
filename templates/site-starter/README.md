# Site Starter

**A lean Next.js starter carrying the seven-section conversion wireframe plus a
design-system-first token layer.** The BOS site-builder (`design-my-site`)
instantiates a copy of this into an owner's workspace, inlines their derived
design system, and steers Claude Design to build off it. `launch-my-site`
deploys the finished project to Vercel.

Part of the [Business Operating System](../../README.md). Same committed-app
precedent as the [studios](../../studio/) (source committed, `node_modules`
gitignored, versions pinned), but this is a **template**, not a shared render
surface: each instantiated copy becomes the owner's own project.

---

## What it is

A one-page landing site by default (the seven-section skeleton), with every
section built as a real, buildable component that reads its styling from design
tokens. A multi-page site is the same components reused per page plus the site
layer (Nav, Footer, internal linking). The method behind it lives in
[`knowledge/web-design-method.md`](../../knowledge/web-design-method.md); this
starter is that method made real in code.

The point is the opposite of a template look: the starter ships **neutral**
defaults so it builds standalone, then the skill overwrites the token layer with
the owner's brand and a derived, distinctive design system, so Claude Design is
forced off its house style onto something that is unmistakably the owner's.

---

## Quick start

```bash
npm install
npm run dev        # http://localhost:3220
```

`npm run build` produces a clean static production build. `npm run start` serves
it. `npm run lint` runs Next's linter.

Port **3220** is chosen to avoid the studio ports (3210 / 3213 / 3216 / 3217).

---

## The seven-section skeleton

`app/page.tsx` composes these in order (see `components/sections/`):

1. **Hero** — headline + subhead + one CTA, holds the single H1.
2. **TrustBar** — rating, licences, years, high on the page.
3. **Benefits** — 3-4 benefit-led, scannable items (H2s).
4. **HowItWorks** — 3-4 plain steps, lowers perceived risk.
5. **SocialProof** — named testimonials (placeholders; never fabricated).
6. **Faq** — objection handling, FAQPage schema.
7. **FinalCta** — one action, short form, one reassurance.

Plus **Nav** and **Footer** for the multi-page site case. All copy is
placeholder and positive-only; the skill replaces it with real, on-page-SEO-
correct copy.

Each section component carries a first-line `{/* @dsCard group="sections" */}`
JSX comment so Claude Design's Design System pane indexes it into
`_ds_manifest.json`.

---

## The design-system layer

`styles/tokens.css` **is** the design system: CSS variables for colours, fonts,
the radius scale, spacing, and elevation. Components read them directly (`var(--…)`)
and through the Tailwind theme map in `tailwind.config.js`, so one token change
reskins everything.

- These are **neutral** defaults on purpose, aligned with
  `brand/defaults/brand.json`, so the app looks coherent standalone.
- On instantiation, `inline_design_system.py` (part of `design-my-site`)
  **overwrites** `styles/tokens.css` with the owner's brand + derived overrides,
  self-contained (no dependency on the in-repo `../../../brand` path).
- **Radius is pinned explicitly** — the single most brand-defining, most-
  overridden property (see the method file, Part 4).

The font `<link>` in `app/layout.tsx` uses the confirm-loading pattern (preconnect
+ stylesheet) so the named typeface actually renders and never silently falls
back to system-sans. The neutral starter loads Inter; the skill swaps in the
owner's typeface and keeps the same wiring.

---

## SEO components

`components/seo/` holds JSON-LD components that emit `application/ld+json`:

- **LocalBusinessJsonLd** — NAP, hours, area served.
- **ServiceJsonLd** — one per service page.
- **FaqJsonLd** — mirrors the Faq section (keep them in sync).
- **ReviewJsonLd** — AggregateRating + Review; renders nothing without real data.

They render invented data never: pass real values, or leave the slot.

---

## How the skill instantiates it

1. `design-my-site` copies this whole folder into the owner's workspace as their
   project (never back into BOS).
2. It runs `inline_design_system.py`, which reads the owner's `brand/brand.json`
   and the derived overrides from `~/.claude/bos-cache/site-builder-profile.json`
   and writes a self-contained `styles/tokens.css` + `design-system.json`.
3. It hands the owner the art-direction brief to paste, which sites to
   web-capture, and `/design-sync` to attach the inlined design system so Claude
   Design builds inside it.
4. It runs `npm install` + `npm run dev` and opens `http://localhost:3220` so the
   owner sees their real page running locally. That is the day-one win, keyless.

`/design-sync` attaches to this project's design system (the `@dsCard` markers +
`design-system.json`), so Claude Design PULLs the tokens and named components in
and builds against them, then PUSHes code state back into the components here.

---

## File map

```
site-starter/
├── README.md                 ← you are here
├── CLAUDE.md                 AI-assistant entry point
├── package.json              pinned Next.js + React + Tailwind; dev on 3220
├── next.config.js
├── tailwind.config.js        theme maps utilities onto the token CSS vars
├── postcss.config.js
├── tsconfig.json
├── .gitignore                node_modules/, .next/, out/
├── app/
│   ├── layout.tsx            metadata + font <link> wiring + tokens + Nav/Footer
│   └── page.tsx              the seven sections in skeleton order + JSON-LD
├── components/
│   ├── sections/             Hero, TrustBar, Benefits, HowItWorks, SocialProof,
│   │                         Faq, FinalCta, Nav, Footer  (each has @dsCard)
│   └── seo/                  LocalBusinessJsonLd, ServiceJsonLd, FaqJsonLd,
│                             ReviewJsonLd
└── styles/
    ├── tokens.css            THE design system (overwritten per project)
    └── globals.css           Tailwind entry
```

---

## Dependency note

Pinned to the **Next.js 14.2 LTS** line at its latest patched release
(`14.2.35`), with Tailwind 3, React 18, and TypeScript. This is the conventional,
predictable app shape Claude Design's handoff and Vercel's build expect. `npm
audit` still lists the standard Next-14-line advisories whose only offered fix is
a jump to the next major (a breaking change we deliberately do not take for a
committed starter); staying on the patched LTS is the intentional choice. When
BOS bumps to a newer Next major across its apps, this starter moves with it.

`node_modules/` and `.next/` are gitignored and never committed.
