# Site Builder — `design-my-site` (floor) + `launch-my-site` (shelf), driving Claude Design

**Status:** Draft for review. Design direction founder-approved in brainstorming
(2026-07-03). Pending the spec-review loop and a founder read of this written spec
before any implementation planning.

**One-line:** BOS becomes the *conversion + uniqueness engine* that drives Claude
Design: it supplies the structure that converts, the on-page SEO that ranks, and a
bespoke design system per project that forces Claude Design off its house style,
then lands the built page in a local Next.js preview ready to ship to Vercel.

---

## 1. Why

Two builders already exist and neither is this. TrustPager has a templated
website/page builder (`create_website`, the platform page builder), and there is a
`website-builder` product hero in the OG studio. Those serve the "get a functional
site up" job. This feature serves a different one: **premium, bespoke,
high-converting pages** whose layout is unique per client, grounded in proven
wireframe and conversion patterns, and built with Claude Design + Vercel.

The founder ruling that shapes everything: **the skill must not impose one BOS
house style.** Left alone, Claude Design converges on a recognisable look
(off-white/beige grounds, rusty-orange accents, large italic serif, tracked-out
subheads) and repeats layouts across projects. The value here is the opposite of a
template: capture the owner's taste and the sites they admire, then hand Claude
Design a brief specific enough that it is *forced* off its defaults onto something
distinctive. BOS brings the conversion discipline and the anti-sameness pressure;
Claude Design brings the visual build; Vercel ships it.

This mirrors the floor/deepener split the whole system runs on, and it is the same
extraction shape as the SEO floor
([2026-07-02-seo-floor-extraction-design.md](2026-07-02-seo-floor-extraction-design.md)):
keep the *method* wholesale, build the *keyless slice* bounded, mark the *paid /
connected* step as a deepener.

## 2. The shape (three skills, two new)

| Skill | Tier | Job |
|---|---|---|
| **`design-my-site`** (new) | Floor, keyless, studio-class | Everything except deploy: elicit taste + goal, research the reference sites, derive a unique design system + art-direction brief + real copy, scaffold a local Next.js base carrying that system, walk the owner through Claude Design, land the build back into a running local host view. |
| **`launch-my-site`** (new) | Tier-1 library shelf, connected | A thin wrapper over the Vercel plugin that takes the finished local project live. Declares a real credential (Vercel). |
| **`get-found-online`** (exists, reused) | Floor + connected | The SEO audit companion, run both before (target-term winnability) and after (live audit). Not rebuilt; delegated to. |

Founder-ruled scope: **both landing pages and multi-page websites from day one.**
This does not bloat because the method is fractal (see §3): a website is N pages
sharing one art direction, plus a thin site layer. A landing page is the one-page
degenerate case.

## 3. The method (the IP) — three layers in `knowledge/`

Two new method files, following the one-home rule and linking out rather than
restating:

- **`knowledge/web-design-method.md`** — the conversion skeleton, the site layer
  (IA), and the on-page SEO wiring. Links to `seo-method.md`,
  `business-method.md` §10.5, `marketing-strategy-method.md`, and
  `communication-voice.md`.
- **`knowledge/claude-design-method.md`** — the anti-sameness steering playbook.
  Kept separate because it is reusable by any future Claude-Design-driven skill,
  not just this one.

### 3a. Conversion + on-page-SEO skeleton (shared, proven, keyless)

The section a page needs to convert AND the on-page SEO role of that same section:
ranking and conversion come out of one artifact, not a bolt-on pass. The canonical
service-business stack, grounded in CRO research (NN/G, CXL, Unbounce, Baymard,
BrightLocal):

1. **Hero** (headline + subhead + real hero visual + one primary CTA). Communicate
   the value proposition inside the ~10s window (NN/G dwell study, 205,873 pages).
   Holds the single **H1** as the primary keyword written as the human benefit
   ("Emergency electrician in Geelong"), mirrored in the title/meta for SERP
   message-match.
2. **Trust bar** (rating + review count + licences/insured + years + logos). Trust
   is the gate for service businesses (BrightLocal: 97% read local reviews). Carries
   E-E-A-T signals and `Review`/`AggregateRating` schema high on the page.
3. **Benefits block** (benefit-led, feature-supported, 3-4 scannable items). F-pattern
   scanning; concise objective copy raises usability (NN/G). Home for H2s carrying
   secondary and long-tail service keywords.
4. **How it works / what to expect** (3-4 steps). Lowers perceived risk;
   `HowTo`/step content, captures "how does X work" intent.
5. **Social proof** (named testimonials, before/after, case studies). Placed where
   doubt peaks. Verbatim customer language adds long-tail coverage + review schema.
6. **Objection handling / FAQ.** Clears the last hesitations at the decision point;
   the single richest section for question keywords + `FAQPage` schema + "near me"
   voice intent.
7. **Final CTA with risk-reversal.** One most-wanted action, short form (1-3 fields;
   Baymard shows fields can be cut 20-60% with no lost data), 1:1 attention ratio.

**Ordering principles** (drive section sequence): value proposition first inside
the 10s window; reduce uncertainty progressively down the page; promise then proof
then action; one goal at a 1:1 attention ratio; message-match ad/search to hero;
trust early for service businesses; scannable F-pattern benefit-led copy; minimise
the ask at the point of action; speed is a structural prerequisite (bounce rises
~32% from 1s to 3s load).

**Copy rule (hard):** positive-only, per the global content rule. Every section
names the win and what success looks like, never the visitor's pain or lack. No em
dashes in any customer-facing copy the skill emits. The method file carries this
rule the way `get-found-online` does.

### 3b. The site layer for multi-page (thin wrapper on 3a)

A website = the same skeleton applied to every page + information architecture.
Grounded pages: Home (transactional), Services hub (informational), Individual
Service pages (transactional, one per core service), Service-Area/Location pages
(local, one per priority town), About (trust), Reviews (trust), Contact
(transactional), optional Blog/Resources (informational). Each page has one primary
job and one primary action.

- **Nav:** 5-7 plain-labelled top items; one persistent primary CTA + a sticky
  click-to-call; shallow structure (any page in 1-2 clicks); mobile-first (~61% of
  local traffic is mobile).
- **Footer:** full NAP identical to the Google Business Profile, hours,
  service-area list, links to every service + location page (footer as secondary
  sitemap), map embed.
- **Internal linking:** hub-and-spoke (Services hub ↔ service pages), cross-link
  service × location, link neighbouring area pages, descriptive anchor text.
- **Per-page rule:** treat EVERY page as its own landing page (local visitors land
  deep from the pack and decide in seconds), one dominant action repeated in three
  positions. Two hard constraints wrap it: Core Web Vitals (mobile-first,
  sub-2-3s), and speed-to-lead (the form/call must feed a sub-5-minute response;
  odds of qualifying drop ~80% after 5 minutes). The speed-to-lead constraint is
  where this hands to the CRM/automation tier post-launch.

### 3c. Art-direction derivation + anti-sameness playbook (`claude-design-method.md`)

The layer that overpowers Claude Design's defaults. Founder-chosen mechanism:
**design-system-first.** The strongest lever (per research) is attaching a real
design system so Claude Design assembles from the owner's actual tokens and named
components and self-checks its output against them, rather than inferring styling.
The playbook, distilled from the official docs + practitioner write-ups:

**Levers (highest-leverage first):**
- Attach a real design system (GitHub repo / local codebase / Figma export / raw
  token upload / `/design-sync`) so output is built in the owner's components.
- Specify tokens as exact literal values, never descriptions: hex colours, named
  typefaces + weights, and an explicit border-radius scale. **Border-radius is the
  single most brand-defining and most-overridden property** (pin `radius-full:0`
  when no pills).
- Verify the font `@import`/`<link>` actually renders (a named-but-unloaded font
  silently falls back to system-sans and the design reverts to generic).
- Anchor to a named design movement that carries rules (Swiss/International
  minimalism, Bloomberg density, "in the style of Linear"), not loose adjectives.
- Use description + goal + constraints densely on the first turn.
- Negative-prompt each default *paired with its replacement* ("not cream, use pale
  silver-grey"); a bare "don't" just moves it to another default.
- Component-level rules (buttons/inputs/cards/nav states), not just global tokens.
- Lead with 3-5 reference screenshots / web-captures; when cloning a layout, add
  the layer-override: replicate structure only, apply OUR tokens, do not copy the
  source brand/type/imagery.
- Refine via visual critique + the Tweaks sliders (off the chat meter); start a
  fresh session per design and re-anchor from the attached spec file.

**Anti-patterns** (things that let it drift back): vague adjectives, described
colours instead of hex, unspecified radius, unverified font imports, bare negative
prompts, generic component requests, marathon sessions, relying on in-thread
memory, web-capture without the layer-override, treating the auto-inferred design
system as ground truth (Claude *deduces* it, so validate edge cases).

The method file also carries the **art-direction-brief structure** (description →
goal → aesthetic anchor → colour tokens → typography → spacing/radius/shadow →
component rules → layout/grid → negative constraints → iconography/imagery), which
is what the skill emits for the owner to drive Claude Design with.

## 4. The pipeline (surface by surface)

1. **Elicit taste + goal (BOS, keyless).** Pull the owner + brand from the profile
   and `brand.json`. Ask for: the pages/site they want, the one action each page
   drives, and 2-5 reference sites they admire (+ what they like about each).
2. **Research the references (BOS, keyless, reuse).** Delegate to
   `research-a-competitor` / Firecrawl `scrape`+`search` for copy, structure, and
   offer patterns (scope clamp per `research-method.md`: no crawl/map/agent/extract).
   Optionally run `get-found-online`'s SERP winnability spot-check to ground each
   page's target term.
3. **Derive the design system + brief + copy (BOS, keyless).** Synthesise a unique
   token set (colour beyond `brand.json`, type pairing, spacing rhythm, radius
   scale, motion, section treatments) + the art-direction brief + the real,
   positive-only, on-page-SEO-correct copy per the skeleton.
4. **Scaffold the local base (BOS, keyless, studio-class).** Instantiate
   `templates/site-starter/` into the owner's workspace as their project, wired to
   the derived tokens as a real design system (see §6).
5. **Claude Design builds, steered hard (owner, in-box on Pro).** The skill hands
   the owner: the brief to paste, which sites to web-capture (+ the layer-override),
   and `/design-sync` to attach the scaffold's design system so Claude Design builds
   inside it. `/design-sync` is two-way (June 2026): PULL the system into Claude
   Code, PUSH code state back; it builds an explicit plan (files to write/delete)
   and returns a `planId` to approve, never overwriting silently. The `DesignSync`
   harness tool exposes this to Claude Code (`list_projects`/`get_project`/
   `get_file` to diff, `finalize_plan` → `planId`, `write_files` incrementally,
   one component at a time).
6. **Handoff to Claude Code (built-in export).** "Handoff to Claude Code" lands the
   design in the local scaffold and continues from existing work, not a screenshot.
7. **Local host view (BOS studio-class).** `npm run dev` on the instantiated
   project; the owner sees their real page running locally. This is the day-one
   win, no account required.
8. **Ship (deferred to `launch-my-site`).** When ready, the shelf skill deploys to
   Vercel (Claude Design's native Vercel integration is a fallback door).

## 5. The two skills in detail

### 5a. `design-my-site` (floor, keyless, studio-class)

**Frontmatter (studio-class keyless, matching `make-thumbnail` exactly):**
```yaml
function_slot: creative      # the creative studio slot (make-thumbnail uses creative; make-social-post uses social)
requires_driver: render      # studio-class local build; NOT a network/mcp skill
requires_credential: none
data_path: local
status: active
```
No `uses_tools` key naming any `mcp__` tool. Claude Design is used through its own
UI plus the built-in `/design-sync` + `DesignSync` (harness-level, in-box on a paid
Claude plan), **not** the Claude Design MCP server (that would be an `mcp__`
dependency and break the keyless binding check). Firecrawl reads are reached by
delegating to `research-a-competitor` / `get-found-online`, not re-implemented here.

**Gate-led flow:** (1) Anchor on owner + brand + goal, and confirm landing-page vs
site. (2) Gather 2-5 reference sites + what they like. (3) Research references
(delegate). (4) Derive design system + brief + positive-only copy against the
skeleton; for a site, produce the IA first, then the home/primary page fully, rest
iterative. (5) Scaffold the starter into the owner's workspace. (6) Hand the owner
the Claude Design steps (paste brief, web-capture + layer-override, `/design-sync`).
(7) Land the handoff and run the local host view. (8) Name `launch-my-site` and
`get-found-online` as the next doors (reactive, outcome-only).

**Guardrails:** bounded (a first win is one page live locally, not a whole site in
one sitting); token-frugal; studio setup (npm install + dev server) handled for the
owner, never asked of them; if a reference fetch fails, offer the pasted-content
fallback; never fabricate copy, testimonials, numbers, or reviews (safeguards).

### 5b. `launch-my-site` (Tier-1 library shelf, connected)

**Frontmatter (connected; the three commented values are open, see §10):**
```yaml
function_slot: creative       # deploy has no clean slot in the enum; least-bad existing fit, see §10
requires_driver: vercel       # no vercel driver exists yet; may need creating, see §10
requires_credential: mcp      # the enum is none|mcp|key, so wrapping the Vercel MCP is 'mcp', not 'vercel'
data_path: mcp_tools
status: active
```
A thin wrapper over the Vercel plugin (`vercel:deploy` / the Vercel MCP): confirm
the local project builds, deploy a preview, then production on approval, report the
URL. Honours the guard rails (never deploy without an explicit go; report the real
outcome; nothing announced as live until the deploy is confirmed). Offers the
post-launch loop: `get-found-online` live audit + the connected rank-tracking /
AI-visibility doorway.

## 6. The starter — `templates/site-starter/`

A Next.js app BOS ships (committed to BOS) and instantiates into the owner's
workspace (never committed into BOS). It carries:

- **Design tokens wired from `brand.json`** as CSS variables / Tailwind config, so
  the derived system is a real, attachable design system.
- **A design-system layer Claude Design can attach to** via `/design-sync` or
  point-at-codebase, including the `<!-- @dsCard group="..." -->` first-line markers
  Claude Design's Design System pane indexes into `_ds_manifest.json`.
- **A signature component base + the wireframe skeleton as components** (Hero,
  TrustBar, Benefits, HowItWorks, SocialProof, FAQ, FinalCTA; plus Nav/Footer for
  sites), so Claude Design *continues from existing bespoke work* instead of
  generating from zero.
- **SEO + performance defaults for free:** Next.js metadata API (title/meta per
  page), JSON-LD components (LocalBusiness / Service / FAQPage / Review), image/font
  optimisation, static rendering, Core Web Vitals headroom.

Chosen over static HTML and Vite because it is Vercel-native, gives file routing +
shared layout for the multi-page case, and is exactly what Claude Design's handoff
and native Vercel integration expect.

## 7. SEO wiring (reuse, not reinvention)

Two layers, same doctrine as everything else:

- **On-page, keyless, by construction.** The skeleton (§3a) pulls the on-page
  checklist from `knowledge/seo-method.md` so every page ships correct (single H1,
  heading hierarchy, title+meta, semantic HTML, alt text, internal links, JSON-LD).
  The starter's Next.js defaults carry the technical/performance half.
- **Target-term grounding + post-launch tracking, connected depth.** Before copy,
  `get-found-online`'s keyless SERP spot-check grounds targets on what is winnable;
  the connected `seo_*` tools (`seo_keyword_research`, `seo_competitor_gap`,
  `seo_ai_visibility`, `seo_track_keywords`) sharpen and monitor when TrustPager is
  connected.
- **Local-first discipline (hard).** Honour `get-found-online`'s gravity-stack gate
  (`business-method.md` §10.5): answer speed and a review engine come before
  keyword-chasing. A page that ranks but drops the caller to voicemail still loses
  the job, so the method never trades the conversion + speed-to-lead fundamentals
  for a keyword.
- **Rule of reuse:** `web-design-method.md` *references* `seo-method.md` and the
  skill *delegates* audits to `get-found-online`, exactly as `get-found-online`
  delegates competitor reads to `research-a-competitor`. No SEO logic duplicated.

## 8. Wiring + validation

- **Register** both skills in `kernel/registry.json` via the generator. A manifest
  that fails validation is silently skipped by the generator (and then trips the
  onboarding-binding phantom check), so the §5 frontmatter must pass
  `tools/manifest.py` first. `design-my-site` copies the studio-class keyless
  pattern from `make-thumbnail`; `launch-my-site` declares the connected credential.
- **Onboarding surface:** add `design-my-site` to `knowledge/starter-projects.md`
  under the market/win-work relief group as a keyless (studio-heavier) win; do NOT
  hand-edit `whats-possible` (runtime registry reader). `launch-my-site` appears as
  a connected doorway, not a cold pitch.
- **Guard scripts green:** `tools/manifest.py` (no `mcp__` in a keyless skill's
  `uses_tools`), `tools/check-onboarding-binding.py` (no TrustPager/credential
  coupling tokens in the `credential:none` body), `tools/lint-skill.py` clean.
- **Offline tests:** synthesis-tested on fixtures (a reference-site payload → a
  correct skeleton + brief + positive-only copy), never a live fetch or a live
  Claude Design call. Keep `BOS_OFFLINE` green.
- **Dogfood on Sonnet** (target model): a local tradie who names two admired sites
  and wants a landing page. Pass bar: the brief produces a *distinct* art direction
  (pinned radius, real font import, negative-prompts paired with replacements, not
  the Claude house look), the copy is positive-only and on-page-SEO-correct, the
  local host view runs, and the Vercel step stays out of the floor skill. A second
  dogfood on the multi-page path (home + one service page + IA).

## 9. Non-goals (YAGNI)

- No deploy inside the floor skill (that is `launch-my-site`).
- No Claude Design MCP server dependency on the floor (keeps it keyless-clean); the
  MCP path is an optional power-user setup, not a floor requirement.
- No hosted/multi-tenant builder, no CMS, no e-commerce checkout this round.
- No re-implementation of SEO, competitor research, or brand strategy: delegate.
- No new render studio in `studio/` (the site is the owner's project, not a shared
  render surface like og/social/thumbnails).

## 10. Open questions for the plan

- **`launch-my-site` has no clean `function_slot`.** The enum
  (`crm, accounting, ads, social, creative, comms, documents, money, people,
  strategy, research, floor`) has no deploy/publish value. Either accept the
  least-bad existing slot (`creative`, shown) or add a new one, which is a schema
  change touching `tools/manifest.py` + `manifest-schema.md`, not just a skill add.
  (`design-my-site` is settled: `creative`, matching `make-thumbnail`.)
- **`launch-my-site` driver + wrapping.** No `vercel` driver exists in `drivers/`
  yet. Decide whether it wraps the Vercel MCP (`requires_credential: mcp`,
  `data_path: mcp_tools`, plus a new `vercel` driver) or the `vercel` plugin's
  CLI-style skills, and create/register the driver accordingly. Note
  `tools/manifest.py` accepts any non-empty `requires_driver` string, so it will
  NOT catch a missing driver: the `vercel` driver must be created and registered
  before `launch-my-site` is generated, or the gap surfaces only at
  generation/runtime, not at manifest validation.
- One method file vs the proposed two (`web-design-method.md` +
  `claude-design-method.md`) — lean two for reusability; confirm.
- Whether the starter ships as a full committed Next.js app or a minimal generator
  the skill fills in (weigh repo weight vs first-run speed), and whether committing
  a Next.js app tree under `templates/` clears the repo's hygiene/kernel-clean
  gates (there is no `studio/`-style precedent for a committed full app).
