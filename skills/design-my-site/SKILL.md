---
name: Design My Site
description: A bespoke, high-converting landing page or website built from the sites you admire and your own taste, running on your machine in a sitting. On-brand, findable, and unmistakably yours, not a template. No accounts needed to build it.
triggers:
  - design my site
  - build my website
  - build a landing page
  - make a website
  - i want a website like
  - design a page that converts
function_slot: creative
requires_driver: render
requires_credential: none
data_path: local
status: active
---

# Design My Site

You build the owner a page that is unmistakably theirs, running on their own
machine before you finish. Not a template, not the generic AI-design house look:
a bespoke, high-converting page grounded in the sites they admire and their own
taste, with copy that converts and ranks in one pass. BOS is the conversion and
uniqueness engine here; Claude Design does the visual build; the owner watches
their real page come up on localhost. No accounts, no keys, day one.

The whole method lives in one home:
[`knowledge/web-design-method.md`](../../knowledge/web-design-method.md), the
conversion + on-page-SEO skeleton (Part 1), the site layer / information
architecture (Part 2), the SEO wiring (Part 3), and the Claude Design steering
playbook (Part 4). **Read it before you derive anything.** This skill body stays
lean and references it rather than restating it. The voice of any customer-facing
line is [`knowledge/communication-voice.md`](../../knowledge/communication-voice.md);
the local fix-order gate is [`business-method.md`](../../knowledge/business-method.md)
§10.5.

This is the keyless floor of the site stack. Deploy is a different act and a
different skill: `launch-my-site` puts the finished page on a real URL. Do not do
any of that here (see Hard rules).

---

## Hard rules (read first, these override everything below)

1. **Keyless.** No `mcp__` tools, no direct Firecrawl calls, no accounts, no keys.
   Web reads happen by delegating to the sibling skills (`research-a-competitor`,
   `get-found-online`), never by calling a tool here. This keeps the manifest
   keyless-clean.
2. **Positive-only, no em dashes** in every line of copy the page carries and
   everything the owner reads. Name the win and what success looks like, never the
   visitor's pain or lack. Use a comma, a colon, parentheses, or two sentences in
   place of an em dash. Understanding the owner's frustration in the conversation
   is fine; the shipped page stays positive (per the global content rule and the
   method file's output rule).
3. **Never fabricate proof.** No invented testimonials, names, ratings, review
   counts, NAP, hours, or numbers. If real evidence is not there yet, leave the
   slot marked for real proof and say so to the owner plainly.
4. **Bounded first win.** The win is ONE page live locally (the landing page, or a
   site's home/primary page), not a whole multi-page site in one sitting. Land that
   first, then iterate the rest reactively. Say this bound out loud.
5. **Personalization is DATA, never a forked skill file.** Per-owner detail lives
   in the profile JSON (Step 1). Never template, copy, or fork this skill file per
   owner: a fork gets clobbered on update, blocks updates, and causes drift.
6. **Deploy is not this skill.** No `vercel`, no deploy logic, no live URL claims.
   That is `launch-my-site`, named as a reactive next door in Step 7.

---

## Step 1 — Make it yours (the Source A/B/C/D intake)

Read the profile first: `~/.claude/bos-cache/site-builder-profile.json`, with the
plain Read tool (it is plain JSON at a fixed path, outside the repo, so updates
never touch it and no `.gitignore` entry is needed). If it exists, load it,
confirm it in a line, and skip to Step 3. If it is **absent**, run this intake
once. It mirrors the shared Source A/B/C/D shape `run-my-ads` uses, so both skills
onboard the same way. Almost everything is auto-filled; you only *ask* the small
site-specific bucket.

### Source A — read `brand/brand.json` silently

Business name, colours, logo, voice, tagline. This is where brand identity comes
from. Read it, never copy brand fields into the profile: brand's one home is
`brand/brand.json`, and `inline_design_system.py` reads it directly at scaffold
time (Step 4).

### Source B — read `./CLAUDE.md` silently

The business shape (trade / service / ecommerce / hospitality / clinic), the
offer, the region (only if a `Region:` line is explicitly set, never inferred),
the diagnosed pressure point, and the owner's stated goal. Let it aim the page.

### Source C — ask only the site-specific bucket (the ONLY interview)

Keep it to the small handful the files cannot answer:

- **Landing page or multi-page site?** And the ONE action each page must drive
  (the single most-wanted action per the skeleton's 1:1 attention rule).
- **2-5 reference sites they admire, and what they like about each.** Specific
  beats vague: a layout, a colour feel, a type treatment, a section that landed.
- **Taste and anti-taste.** What look feels like them, and what to stay away from.

Ask these together, conversationally, in as few turns as you can. This is the
whole interview: everything else is read or researched.

### Source D — no live account read (this add-on is keyless)

There is no account to read. Source D here is the delegated reference-site
research in Step 2: it auto-fills the profile to CONFIRM in words, never a fifth
round of questions. Do not ask the owner to retype what the research will find.

### Write the profile

Write `~/.claude/bos-cache/site-builder-profile.json` with the Source C answers
(page-type, per-page action, reference sites + what they like, taste / anti-taste)
plus a slot for the Step-2 research findings and, under a `design_overrides` key,
the Step-3 derived design overrides. Brand fields stay in `brand/brand.json` and
are never copied in. This profile is the resume point: a returning session reads
it and picks up mid-build.

---

## Step 2 — Research the references (delegate, this IS Source D)

Ground the taste in what those sites actually do, and ground the copy targets in
what is winnable, both by delegation, never by a direct tool call:

- **Delegate the reference read to `research-a-competitor`** for each named site:
  structure, section order, offer patterns, and what makes the look work. Feed it
  the site and what the owner said they liked, and read back what it returns.
- **Delegate the target-term winnability read to `get-found-online`'s SERP
  spot-check** (1-3 terms the owner would want each page to win), so the copy aims
  at terms that are realistically winnable, per `web-design-method.md` Part 3.

Auto-fill the profile from what comes back and confirm it in words ("here's what I
took from the sites you love, does that read right?"). If a reference fetch is
slow, blocked, or empty, say so and offer the fallback: "paste me what's on that
page and I'll read it the same way." Never call `mcp__` or Firecrawl tools
directly here; the delegation keeps this skill keyless-clean.

---

## Step 3 — Derive the design system, brief, and copy

This is the uniqueness engine. Per `web-design-method.md` Part 4, derive a design
system distinctive enough that Claude Design is forced off its defaults:

- **A unique design system:** colour tokens beyond `brand.json` (exact hex, never
  described), a type pairing (named typefaces + weights + a confirmed-loading
  import), a spacing rhythm, and **the radius scale pinned** (radius is the single
  most brand-defining property, per Part 4 lever 2), plus per-section treatments.
- **The ten-part art-direction brief** (Part 4): description, goal, aesthetic
  anchor (a named design movement, not loose adjectives), colour tokens,
  typography, spacing / radius / shadow, component rules, layout / grid, negative
  constraints (each default paired with its replacement), iconography / imagery.
- **The real copy for the seven-section skeleton** (Part 1: Hero, Trust bar,
  Benefits, How it works, Social proof, FAQ, Final CTA), positive-only and
  on-page-SEO-correct (single H1 as the benefit-keyword, H2 hierarchy, title +
  meta, FAQ block, JSON-LD), honouring the §10.5 local gravity-stack gate (answer
  speed and reviews before keyword-chasing). Never fabricate proof (Hard rule 3).

**For a multi-page site:** produce the information architecture first (the page
set + nav + footer + internal-linking plan, Part 2), then the home / primary page
fully. The rest of the pages are iterative, after the first page is live (Hard
rule 4). A landing page is the one-page case, done fully in one pass.

Persist the derived design overrides (the token deltas, pinned radius, type
pairing) into the profile JSON under the `design_overrides` key, so Step 4 can
read them back and pass them to the inliner.

---

## Step 4 — Scaffold the owner's project

Copy `templates/site-starter/` into the owner's workspace as THEIR project (a
sensible folder name from the business name). It carries the seven-section
skeleton as real components, the design-system token layer, and the SEO +
performance defaults, so Claude Design continues from bespoke work, not from zero.

Then inline a self-contained design system into the copy. `inline()` is a pure
function (it takes `brand` + `overrides` and writes the files; it reads nothing
itself), so the skill loads `brand/brand.json` and the profile's `design_overrides`
and passes them in. Run this, adjusting the project-dir path:

```python
# load brand + the profile's derived overrides, then inline into the copied project
import json, pathlib, sys
sys.path.insert(0, "skills/design-my-site")
from inline_design_system import inline

brand = json.loads(pathlib.Path("brand/brand.json").read_text(encoding="utf-8"))
profile = json.loads(
    pathlib.Path.home().joinpath(".claude/bos-cache/site-builder-profile.json").read_text(encoding="utf-8")
)
overrides = profile.get("design_overrides", {})

inline(pathlib.Path("<the instantiated project dir>"), brand, overrides)  # writes styles/tokens.css + design-system.json
```

`inline(project_dir, brand, overrides)` deep-merges the derived overrides over
`brand/brand.json` and writes a standalone `styles/tokens.css` + `design-system.json`
into the copied project. After it runs the copy depends on nothing in the BOS repo
(no `../../../brand` path): it is portable and, later, deployable on its own.

---

## Step 5 — Steer Claude Design

Hand the owner what they paste into Claude Design (in-box on their paid Claude
plan; this is the studio, not an `mcp__` dependency). Per `web-design-method.md`
Part 4:

1. **The art-direction brief** from Step 3, to paste as the dense first prompt.
2. **Which reference sites to web-capture, with the layer-override:** replicate
   the *structure* only, apply OUR tokens, do not copy the source brand, type, or
   imagery.
3. **`/design-sync`** to attach the inlined design system (the `@dsCard` markers +
   `design-system.json`), so Claude Design builds inside the owner's components and
   pushes code state back. It builds an explicit plan and returns a `planId` to
   approve; it never overwrites silently.

Remind the owner of the anti-patterns that let it drift back (Part 4): described
colours instead of hex, unspecified radius, unverified font imports, bare negative
prompts, marathon sessions. Refine via the Tweaks sliders and a fresh session per
design, re-anchoring from the brief file.

---

## Step 6 — Land it and show them

Use Claude Design's "Handoff to Claude Code" to land the build in the copied
project (it continues from existing work, not a screenshot). Then bring the page
up for the owner, and do the studio setup for them, never ask them to:

```bash
cd <the-owner's-project>
npm install
npm run dev        # http://localhost:3220
```

Open `http://localhost:3220` and show them their real page running on their own
machine. This is the day-one win: a bespoke, on-brand, findable page, live
locally, no account required.

---

## Step 7 — Close (reactive, outcome-only next doors)

Name the next doors as outcomes the owner can reach when ready, never as a routed
offer or a cold pitch:

- **`launch-my-site`** puts this page on a real, shareable URL. It connects a
  Vercel account once, then every future update ships with a word.
- **`get-found-online`** runs a live audit once the page is up, so it keeps
  winning searches over time.

> Your page is running on your machine right now, yours to keep. When you want it
> on a real URL people can visit, I can take it live for you, that is a one-time
> account connection and I'll walk you through it. And once it's live, I can audit
> how findable it is and keep it sharp. Both are whenever you're ready.

For a multi-page site, the reactive door is also the next page: offer to build the
next page off the same art direction when the owner wants it (Hard rule 4).

---

## Output shape

The customer-facing deliverables (the art-direction brief and every line of page
copy) are positive-only, no em dashes, and never fabricate proof. The intake asks
one small bucket of questions (Source C) and reads or researches everything else.
The win is one page running at `http://localhost:3220`, built off a design system
distinctive enough to be unmistakably the owner's, with `launch-my-site` and
`get-found-online` named as the doors that come next.
