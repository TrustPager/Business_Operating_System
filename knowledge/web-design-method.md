# Web Design Method — how the BOS builds a bespoke, high-converting, findable page or site

The canonical knowledge for the site-builder floor (the `design-my-site` skill,
with `launch-my-site` deploying what it builds). This is the whole method in one
home: the conversion + on-page-SEO skeleton, the site layer / information
architecture, the on-page SEO wiring, and the Claude Design steering playbook.
The skill bodies stay lean and reference this file.

**The core idea.** BOS is the conversion + uniqueness engine that drives Claude
Design. Left to its own defaults, an AI design tool converges on one recognisable
house look and repeats layouts across projects. The value here is the opposite of
a template: capture the owner's taste and the sites they admire, then hand the
design tool a brief specific enough that it is forced off its defaults onto
something distinctive. BOS brings the structure that converts and the pressure
that keeps every build unique; the design tool brings the visual build; Vercel
ships it. Ranking and conversion come out of one artifact, not a bolt-on pass.

**The method is fractal.** A website is N pages sharing one art direction plus a
thin site layer. A landing page is the one-page case of the same skeleton. Build
either from the same four parts below.

---

## Part 1 — The conversion + on-page-SEO skeleton

The sections a page needs to convert, and the on-page SEO role of that same
section. Grounded in CRO research (NN/G, CXL, Unbounce, Baymard, BrightLocal).
The canonical service-business stack, in order:

### 1. Hero
- **Job:** headline + subhead + one real hero visual + one primary call to action.
- **Why it converts:** it communicates the value proposition inside the roughly
  ten-second window a visitor gives a page (NN/G dwell study across 205,873 pages).
  Say what you do, for whom, and the next step, above the fold.
- **Copy guidance (positive-only):** name the win and who it's for. "Emergency
  electrician in Geelong, on the phone in minutes." Lead with the outcome the
  visitor wants, never their frustration.
- **On-page SEO role:** holds the single **H1**, written as the primary keyword
  in human-benefit form ("Emergency electrician in Geelong"), mirrored in the
  title tag and meta description so the SERP listing message-matches the page.

### 2. Trust bar
- **Job:** rating + review count + licences / insured + years in business + client
  logos, high on the page.
- **Why it converts:** trust is the gate for a service business (BrightLocal: 97%
  of people read local reviews before choosing). Earn it before you ask for anything.
- **Copy guidance (positive-only):** state the credentials plainly and proudly.
  "Fully licensed and insured. 4.9 stars from 200+ local jobs."
- **On-page SEO role:** carries E-E-A-T signals and `Review` / `AggregateRating`
  schema near the top of the page.

### 3. Benefits block
- **Job:** benefit-led, feature-supported, 3-4 scannable items.
- **Why it converts:** visitors scan in an F-pattern; concise, objective,
  benefit-first copy raises usability (NN/G). Each item earns its line.
- **Copy guidance (positive-only):** lead each item with what the customer gets,
  then the feature that delivers it. "Back up and running the same day, because we
  carry the common parts on the van."
- **On-page SEO role:** home for H2s carrying secondary and long-tail service
  keywords.

### 4. How it works / what to expect
- **Job:** 3-4 plain steps showing what happens after the customer acts.
- **Why it converts:** it lowers perceived risk by making the process known and
  simple. Certainty moves people forward.
- **Copy guidance (positive-only):** frame each step as smooth and handled. "You
  call, we confirm a time that suits you, we arrive on time and sort it."
- **On-page SEO role:** `HowTo` / step content; captures "how does X work" intent.

### 5. Social proof
- **Job:** named testimonials, before/after, short case studies.
- **Why it converts:** placed where doubt peaks, real proof from real people is
  the strongest reassurance a page can carry.
- **Copy guidance (positive-only):** use genuine customer words that describe the
  result they got. Never fabricate a testimonial, a name, or a number: if the
  evidence isn't there yet, leave the slot for real proof and say so to the owner.
- **On-page SEO role:** verbatim customer language adds long-tail coverage; review
  schema reinforces the trust signals.

### 6. Objection handling / FAQ
- **Job:** answer the last few hesitations at the decision point.
- **Why it converts:** it clears the specific doubts that otherwise stall a ready
  buyer, right where they arise.
- **Copy guidance (positive-only):** answer the real question directly and
  confidently, framing the answer as a reason to go ahead.
- **On-page SEO role:** the single richest section for question keywords, `FAQPage`
  schema, and "near me" voice-search intent.

### 7. Final CTA with risk-reversal
- **Job:** one most-wanted action, a short form (1-3 fields), one clear reassurance.
- **Why it converts:** a single goal at a 1:1 attention ratio, with the smallest
  possible ask, converts best. Baymard shows form fields can be cut 20-60% with no
  data lost, and every removed field lifts completion.
- **Copy guidance (positive-only):** restate the win and make the next step
  effortless. "Get your free quote today, we usually reply within the hour."
- **On-page SEO role:** the conversion endpoint; keep it fast and semantic so it
  never drags Core Web Vitals.

### Ordering principles

These drive the section sequence:

1. Value proposition first, inside the ten-second window.
2. Reduce uncertainty progressively down the page.
3. Promise, then proof, then action.
4. One goal at a 1:1 attention ratio (one dominant action, minimal competing links).
5. Message-match the ad or search term to the hero.
6. Trust early for a service business.
7. Scannable, F-pattern, benefit-led copy.
8. Minimise the ask at the point of action.
9. Speed is a structural prerequisite (bounce rises roughly 32% as load goes from
   1s to 3s), so treat performance as part of the skeleton, not a later fix.

**Copy rule (hard):** positive-only, per the global content rule. Every section
names the win and what success looks like, never the visitor's pain or lack. No em
dashes in any customer-facing copy the skill emits.

---

## Part 2 — The site layer / information architecture

A website is the same skeleton (Part 1) applied to every page, plus a thin site
layer. Every page has one primary job and one primary action.

### The page set

- **Home** (transactional): the flagship, full skeleton.
- **Services hub** (informational): the parent that links to each service page.
- **Individual Service pages** (transactional): one per core service.
- **Service-Area / Location pages** (local): one per priority town or suburb.
- **About** (trust).
- **Reviews** (trust).
- **Contact** (transactional).
- **Blog / Resources** (informational, optional).

### Nav

- 5-7 plainly-labelled top items.
- One persistent primary CTA plus a sticky click-to-call.
- Shallow structure: any page reachable in 1-2 clicks.
- Mobile-first (roughly 61% of local traffic is mobile).

### Footer

- Full NAP (name, address, phone) identical to the Google Business Profile.
- Hours, service-area list.
- Links to every service and location page (the footer acts as a secondary sitemap).
- Map embed.

### Internal linking

- Hub-and-spoke: Services hub links to each service page and back.
- Cross-link service × location (each service to its area pages and vice versa).
- Link neighbouring area pages to each other.
- Use descriptive anchor text, never "click here".

### The per-page rule

Treat **every page as its own landing page**. Local visitors land deep from the
map pack and decide in seconds, so each page carries one dominant action repeated
in three positions and stands on its own. Two hard constraints wrap it:

- **Core Web Vitals:** mobile-first, sub-2-3s. Performance is a design constraint,
  not an afterthought.
- **Speed-to-lead:** the form or call must feed a sub-5-minute response (the odds
  of qualifying a lead drop roughly 80% after 5 minutes). This is where the built
  page hands off to the CRM / automation tier after launch.

---

## Part 3 — On-page SEO wiring (reuse, not reinvention)

One artifact, both outcomes: the skeleton above is authored so the same page that
converts is also the page that ranks. This section wires the two together and
points at the owning docs rather than restating them.

- **On-page checklist — link, do not duplicate.** The per-page on-page checklist
  (single H1, heading hierarchy, title + meta, semantic HTML, alt text, internal
  links, JSON-LD) lives in [`knowledge/seo-method.md`](seo-method.md). Author every
  page against that checklist; the starter's framework defaults carry the
  technical / performance half for free.
- **Local-first discipline (hard) — the gravity-stack gate.** For a locally-bought
  business, honour the local gravity stack in
  [`knowledge/business-method.md` §10.5](business-method.md): answer speed and a
  review engine come before any keyword-chasing. A page that ranks but drops the
  caller to voicemail still loses the job, so the method never trades the
  conversion and speed-to-lead fundamentals for a keyword. Read §10.5 before
  ordering any local fix.
- **Target-term grounding, connected depth.** Before writing copy, delegate the
  keyless SERP winnability spot-check to `get-found-online` to ground each page's
  target term on what is actually winnable. Real volumes, backlink data, and
  ongoing rank tracking are a later, connected-tier sharpener (surfaced reactively,
  never a cold pitch), also per `seo-method.md`.
- **Rule of reuse.** This file *references* `seo-method.md` and the skill
  *delegates* audits to `get-found-online`, exactly as `get-found-online` delegates
  competitor reads to `research-a-competitor`. No SEO logic is duplicated here.

For offer and conversion doctrine that underpins the copy (how an offer is built,
the four-doors and gravity-stack context), see
[`knowledge/marketing-strategy-method.md`](marketing-strategy-method.md) and
`business-method.md`. For the voice of any operational message the site triggers,
see [`knowledge/communication-voice.md`](communication-voice.md).

---

## Part 4 — The Claude Design steering playbook

The layer that overpowers a design tool's defaults. The chosen mechanism is
**design-system-first**: attach a real design system so the tool assembles from
the owner's actual tokens and named components and self-checks its output against
them, rather than inferring styling from loose adjectives.

### Levers (highest-leverage first)

1. **Attach a real design system.** Point the tool at a GitHub repo, local
   codebase, Figma export, raw token upload, or use `/design-sync`, so output is
   built inside the owner's components, not inferred.
2. **Specify tokens as exact literal values, never descriptions.** Hex colours,
   named typefaces plus weights, and an explicit border-radius scale.
   **Border-radius is the single most brand-defining and most-overridden property**
   (pin `radius-full: 0` when the brand uses no pills).
3. **Verify the font `@import` / `<link>` actually renders.** A named-but-unloaded
   font silently falls back to system-sans and the whole design reverts to generic.
   Confirm it loads.
4. **Anchor to a named design movement that carries rules**, not loose adjectives
   (Swiss / International minimalism, Bloomberg density, "in the style of Linear").
   A named movement brings a whole ruleset; an adjective brings nothing.
5. **Set density on the first prompt.** Use description + goal + constraints
   densely on the first turn, when the tool is most steerable.
6. **Negative-prompt each default paired with its replacement.** "Not cream, use
   pale silver-grey." A bare "don't" just moves the default somewhere else; the
   replacement is what redirects it.
7. **Give component-level rules**, not just global tokens: buttons, inputs, cards,
   nav states.
8. **Lead with reference web-captures, with the layer-override.** Attach 3-5
   reference screenshots or web-captures; when cloning a layout, add the override:
   replicate the *structure* only, apply OUR tokens, do not copy the source brand,
   type, or imagery.
9. **Refine via the Tweaks sliders and fresh sessions.** Refine with visual
   critique and the Tweaks sliders (off the chat meter); start a fresh session per
   design and re-anchor from the attached spec file rather than relying on
   in-thread memory.

### The ten-part art-direction brief

This is what the skill emits for the owner to drive the design tool with. Build it
in this order:

1. **Description** — what the page/site is and who it's for.
2. **Goal** — the one action it must drive.
3. **Aesthetic anchor** — the named design movement or reference.
4. **Colour tokens** — exact hex values, named.
5. **Typography** — named typefaces, weights, and the confirmed-loading import.
6. **Spacing / radius / shadow** — the explicit scales, with radius pinned.
7. **Component rules** — buttons, inputs, cards, nav states.
8. **Layout / grid** — structure and breakpoints.
9. **Negative constraints** — each default paired with its replacement.
10. **Iconography / imagery** — the style of icons and images to use.

### Anti-patterns (what lets it drift back to the house look)

- Vague adjectives instead of a named movement.
- Described colours instead of literal hex.
- Unspecified radius.
- Unverified font imports (the silent fallback to generic).
- Bare negative prompts with no replacement.
- Generic component requests.
- Marathon sessions instead of fresh ones per design.
- Relying on in-thread memory instead of re-anchoring from the spec file.
- Web-capture without the layer-override (copies the source brand).
- Treating the auto-inferred design system as ground truth (the tool *deduces* it,
  so validate the edge cases).

---

## Output rule

Everything the owner reads, and every line of customer-facing copy the skill
emits for the page, follows the positive-only rule and uses no em dashes (use
commas, colons, parentheses, or separate sentences). Name every section by the
win it delivers and what success looks like, never by the visitor's pain or lack.
A reference site's gap is fair as a sharp observation; the owner's own page is
always framed by what it goes and wins.
