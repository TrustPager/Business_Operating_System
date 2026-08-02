# BOS Re-Architecture — Founder Decisions (locked)

These are the calls the founder (Vic) has made on the open questions surfaced by the
architecture stress-test ([bos-rearchitecture-review.md](bos-rearchitecture-review.md), §7).
They are the inputs to the implementation plan. One home for these decisions — link here, don't restate.

## North star
The lowest common denominator is a business owner who **just wants to feel powerful** and has
**never touched code**. Every experience decision optimises for that person — even technically
capable users get the same brain-dead-simple path. BOS must self-actualise into their business
partner with the least possible friction.

## D1 — Install: one conversational path (clone + setup.py)
- **One supported install, conversational. No terminal ceremony for the owner.**
- The owner tells Claude something like *"go get the business operating system"* → Claude fetches
  the public repo, runs `setup.py` (doc-lib floor + `bos-run.py` signpost + skills/commands into
  `~/.claude/`), and walks them through it in conversation.
- `CLAUDE_PLUGIN_ROOT` is kept only as an optional override hook; path resolution otherwise anchors
  on the BOS repo structure (a dir containing `tools/` and `kernel/`). The `bos-run.py` launcher
  STAYS — it is the floor's cwd-independent signpost, not a seam to retire.
- Rationale: first-run / churn risk for a paid community is the thing to kill.

> **[SUPERSEDED 2026-06-30, Dogfooding-V1 / R1 — founder-reaffirmed]** The original D1 called for a
> *plugin-marketplace* install (`/plugin install`) and retiring the clone + `bos-run.py` seam.
> Dogfooding V1 found the plugin path skips the keyless floor (it never runs `setup.py`, so no doc
> libs and no `bos-run.py` — document skills break). Decision reversed: the `.claude-plugin/`
> manifests are removed, and the conversational clone + `setup.py` path above is the single
> supported install. See `AI-BOS/Dogfooding-V1.md` (R1) and the decisions locked there.

## D2 — TrustPager key: no read-only available → lock it down
- TrustPager does not mint read-only keys today, so the two-key model (read-only for read
  fan-out, MCP for writes) is **off the table for now**.
- Instead, **harden the stored key tightly**: restricted file permissions (e.g. `chmod 0600` on
  `bos.json`), minimised scope where possible, and rotation guidance documented in `SECURITY.md`.
- Revisit the two-key model if/when TrustPager ships scoped read-only keys.

## D3 — TrustPager lives in its own opt-in section
- Everything TrustPager-related sits behind a *"connect this and here's everything it unlocks"*
  section — discoverable, not foregrounded.
- The partner is **knowledgeable** about TrustPager and answers when asked, but is **never pushy
  or salesy**. Context-triggered, relevant-only — never "pushy pushy pushy."

## D4 — Spend protection: gentle, dismissible, nice-to-have
- **Nice-to-have, not a blocker.** Build it only if it's cheap to add.
- On a **large** credit spend (TrustPager or any credit-based tool), a light heads-up:
  *"by the way, this'll use a bit of credits, just so you know"* — so nothing happens by accident.
- The owner can **switch it off** (*"I know what I'm doing"*).
- Posture: **warn-and-proceed**, dismissible — not a hard block.

## D5 — Existing clients: recommend they redownload
- Recommend existing TrustPager clients **redownload the new repository / reinstall the new
  version** to pick up the re-architecture and rebrand.

## D6 — Floor & catalog strategy
**The model: curated floor ON, everything else pinnable.**
- A small, opinionated set of floor apps is **active by default** — instant minute-one value, zero
  setup, no pinning required.
- Everything else lives in a **browsable catalog** (*"here's everything I can do"*); the owner
  **pins/activates** what they want. Pinning IS the registry-activation mechanism (= the OS
  review's P2 fix: keep un-pinned apps out of the always-loaded trigger surface, discoverable via
  `/whats-possible`). This avoids both the setup-wall of "all off" and the token-tax + overwhelm +
  trigger-collisions of "all on."
- The partner offers to switch things on **contextually** (relevant-only, never pushy).

**Floor drivers (no account/key needed):**
- **Firecrawl** — the keyless hosted MCP (scrape/search/interact need no key). Ships in the floor.
  Unlocks research apps: `research-a-competitor`, `scan-the-market`, `enrich-this-lead`,
  `research-before-call`.
- **Remotion (brand video)** — local rendering, no account, but lives in the separate
  `Remotion-VideoStudio` repo (hard rule: video work only happens there). The BOS video capability
  is a **bridge** to that studio, not a drop-in. **Pin-on** (heavier, not universal).
  *(Superseded on YouTube scope, labelled 2026-07-05: YouTube-scope video is superseded by
  [2026-07-05-youtube-studio-design.md](2026-07-05-youtube-studio-design.md) — in-repo
  `studio/video` frame-capture, not an RVS bridge; the `make-brand-video` RVS bridge is
  unaffected.)*

**Process frameworks = invisible infrastructure, never user toggles:**
- **Superpowers** — bake the useful framing into the kernel/apps; the partner just works
  methodically. Take the shape, drop what the model now does natively. Never a user-facing toggle.
- **Grill-me** — the technique powers the onboarding interview (invisible). Plus one visible
  **floor app**: *"grill me on this decision"* (stress-test a hire / price change / big job —
  pure reasoning, no tools).

## D7 — Money: location-agnostic core + opt-in regional pack
- The MONEY cluster is **location-agnostic at the core** — cash flow, profit-per-job, expenses,
  budgeting, margin: universal business math that works for any business anywhere, no region set.
- **Regional tax/compliance is a swappable data module** (a "regional pack") selected during
  onboarding (the profile records the locale). **Australia ships first and complete** (Simpler-BAS
  G1/1A/1B, GST, super, PAYG, Fair-Work basics via a versioned ATO/Fair-Work constants file). Other
  regions are a clean extension point — stubbed now, filled on demand. Same thin-core + swappable-
  module pattern as drivers; no new architecture.
- Region-specific apps (e.g. `estimate-my-bas`) only surface once a region is set; the universal
  core works with none. **We prepare figures; the owner lodges** (no direct tax-authority filing —
  DSP accreditation is incompatible with the MIT floor).
- **Why:** keeps "anyone can run it" honest (a US/UK owner gets the universal money apps day one)
  while preserving the AU depth that's our edge for the Skool base.

## D8 — TrustPager data path: MCP-first / keyless (revises bos-rearchitecture-review §5)
Verified against TrustPager's own help center (read live via the connector):
- The **MCP connector in claude.ai (OAuth)** is the documented way to connect Claude — *"Connect Claude
  to TrustPager"*, *"Edit OAuth Client Scopes"* (Claude.com is a connected OAuth integration with
  per-scope tiers + revocable user tokens), *"Scopes — the guardrails for agents"*.
- The **REST API + `tp_live_` keys** is a SEPARATE developer path — *"Use the TrustPager REST API"*,
  *"Create and Manage API Keys"*.

**Ruling:**
- The TrustPager driver is **MCP-first / keyless by default.** BOS apps reach TrustPager through the
  connected MCP (authed via the user's OAuth connection — no key paste). Onboarding follows the help
  center's connector flow. This is how real users (incl. Vic) actually operate, and it makes install
  truly keyless.
- The `fetch.py` + `tp_live_` REST fan-out is **demoted**: the kernel keeps the keyed-REST transport
  for OTHER drivers (third-party APIs with no MCP), and it stays available only as an optional,
  off-by-default "turbo reads" mode for TrustPager. Never the default, never required.
- The digest/ranking logic currently in `fetch.py` moves into the skills (driven over MCP tools) and
  leans on TrustPager's aggregate MCP tools (`get_pipeline_summary`, `get_agent_dashboard`,
  `query_report`) to keep reads cheap in one call.
- **Supersedes** bos-rearchitecture-review §5 ("keep the 22 fetch.py as the read path on a read-only
  key") — that assumed the key path was worth keeping for speed; real usage (everything via MCP) makes
  keyless MCP the right default. P0's kernel/driver abstraction is exactly what makes this a
  driver-*type* swap (keyed-REST → MCP), not a rewrite.
- **Roadmap impact:** install (P8) drops the `tp_live_`/`bos.json` key step for TrustPager; a new work
  item re-points the TrustPager read apps from key'd `fetch.py` to MCP tools; manifests (P1) carry
  `requires_credential: mcp` + `data_path: mcp_tools` for TrustPager apps. The manifest enums below are
  the contract that encodes this.

## D9 — The floor is defined by the first-win roster, and onboarding is registry-bound (2026-06-27)
- **The floor is defined by the set of tangible first-win projects we offer a brand-new owner**, not by
  whatever skills happen to exist. The roster IS the floor spec — see [floor-roster.md](floor-roster.md).
  A win is "on the floor" only when it is genuinely keyless (zero accounts, zero files), produces a real
  artifact, is finishable in one sitting, and is token-frugal. The floor build proceeds in the roster's
  unlock-priority order.
- **Onboarding is bound to the registry as the single source of truth (belt-and-suspenders):** a CI
  binding check asserts every app the onboarding surface names exists + is correctly classified; a
  manifest rule forbids `mcp__` tools on `requires_credential: none` skills; and `start-here` may only
  *route* to registry-keyless apps at runtime. The curated `starter-projects.md` library is kept for
  vertical-tailored project selection, but it can never point at a phantom or a mislabelled-keyless app.
- **Why:** P3 shipped an onboarding that advertised 10 unbuilt apps + several CRM-coupled apps as keyless
  wins, because the surface was authored against the design vision with nothing binding it to the built
  registry. This decision makes "onboarding only ever offers real, keyless wins" a checked invariant.
- **Roadmap impact:** re-frames P4/P5 around the roster; adds the guardrail (Wave 0) as the prerequisite
  to all further floor work; the `design-nurture-sequence` registry mislabel is corrected to connected-tier.

## D10 — Token-frugality is a first-class constraint; the connected tier must not flood context (2026-06-28)
- **The concern (founder-raised):** a brand-new owner is likely on a Pro plan. If connecting a tool loads
  a large MCP tool surface every turn (TrustPager alone exposes ~600 tools), it taxes context on every
  turn and can burn their usage within a few turns — an unacceptable first-impression cost. "Designed
  intelligently" is a hard requirement, not a nice-to-have.
- **The floor is already safe.** Every floor app is `reasoning_only` / `local` / `firecrawl` and loads
  zero *connected-driver* MCP tools. The one MCP the floor ships is the small, keyless hosted Firecrawl
  server (registered by `setup.py`), whose handful of tools the client defers until called. The bloat
  risk is strictly a CONNECTED-tier concern (TrustPager's ~600 tools), so it does not block the floor build.
- **v1 strategy (no new moving parts):** lean on the client's native tool-deferral / tool-search (Claude
  Code already defers connected-MCP tools, surfacing names + loading schemas on demand) + TrustPager's
  **OAuth scoping** (connect only the tool groups the owner needs, trimming the surface at the source) +
  the kernel's **REST path** for read-heavy skills (call the API in python → zero MCP tools loaded).
- **Planned path for the multi-driver future:** a thin BOS **gateway/proxy** fronting all connected MCP
  servers and exposing a small `search_tools` + `invoke_tool` façade (a "driver multiplexer" in the
  kernel/driver model). Adopt ONLY if measurement + scoping prove insufficient, and weigh against D1's
  "no install ceremony" (a proxy is a running process — local or hosted — with its own trust/dependency
  surface).
- **A DEEP investigation is queued (founder-ruled scope) BEFORE finalizing the TrustPager re-slot (P7) /
  install (P8) connection design:** measure real per-turn tool overhead on Claude Code vs the claude.ai
  connector; confirm how granular TrustPager's OAuth scopes are; survey + vet public MCP proxy/router
  projects (license + no-ceremony fit); prototype the chosen lever; write it up as the connected-tier
  loading spec. Do not lock P7/P8 connection design until this lands.

## D11 — Brain-dead self-sufficiency: the BOS does setup, it never hands the owner a command (2026-06-28)
- **The standard:** the BOS either runs self-sufficiently with what we ship, or — for anything that must
  run on the owner's own machine — it gets that done FOR them, with permission. It never tells a
  non-technical owner to "go run this file" or pastes a `pip install` line and walks away.
- **The anti-pattern (founder-spotted in Claude Code):** "Hey, you need to run X and do Y." Wrong. The
  correct shape is: *"To do this I need to add the document reader. Here's what that involves and I can do
  it for you — may I go ahead?"* → on yes, the BOS runs it itself (against the right interpreter), then
  verifies it worked and continues. Permission first, then action — not instruction.
- **Implementation contract:** (1) BUNDLE the always-needed dependencies in setup so a normal install has
  them; (2) for the rest, tools emit a machine-readable "missing dependency X, fix = `python -m pip install
  Y`" signal (and exit non-zero on real failure), and the SKILL layer turns that into a detect → offer →
  do-on-yes → verify loop; (3) a plain-language `knowledge/` setup doc so any unavoidable manual step is
  stress-free; (4) `check-install.py` gets a keyless-floor mode that verifies the document stack (write→read
  round-trip) and offers to fix what's missing. The field test proved the old `pip install` hints are a
  churn trap for exactly the non-technical owner we build for.

## D12 — Inclusive via business-shapes, not industry niches (2026-06-28)
- **Scope:** the BOS serves ANY small business, not just service businesses. The field test confirmed the
  floor already delivers excellent first wins for ecommerce and hospitality owners with NO matching vertical
  (the generic reasoning carried them) — so verticals are inference shortcuts, not gates.
- **The model:** cover a small, finite set of **business shapes** (service/professional, trades/on-the-tools,
  product-seller/ecommerce-retail, hospitality/walk-in, clinic/appointment) that any industry maps onto,
  backed by the proven generic fallback. This is inclusive AND scalable, versus chasing infinite per-industry
  niches. `industry-notes.md` re-frames around shapes; `starter-projects.md` follows.
- **Marketing may still LEAD with service businesses** (where the Darren Locke / Martin Keane proof lives)
  without the product excluding anyone. Positioning ≠ product scope.

## D13 — The zero-state floor stays lean; heavy/optional power lives in an off-the-shelf library (2026-06-28)
- **The split:** what ships standard (zero-state) is the lean keyless floor that gives EVERY owner a fast
  first win with no heavy setup. Tools that are powerful but heavy, or useful-to-many-but-not-all, are NOT
  shipped standard — they are **packaged as ready-to-go modules in a library** the owner browses and grabs
  off the shelf as needed. This is how we stay token-frugal (D10) + brain-dead to install (D11) + inclusive
  (D12): the standard ship is light; power is opt-in, pulled in exactly to fit the business.
- **The Remotion creative studio is a tier-1 LIBRARY item, and a FUTURE build — not zero-state.** It is
  useful to many businesses but not all, and it is heavy (~1GB Chromium install, render pipeline). It gets
  genericised (TIAC engine → brand-kit-fillable: palette/logo/fonts → branded stills + looped MP4s) and
  boxed as a grab-and-go library module, with a brand-kit builder companion. Not built in the pre-ship
  hardening phase.
- **The social first-win is a STRATEGY, not a single post.** A one-off caption is not exciting; a tailored
  social-media STRATEGY aimed at the owner's target (more bookings / leads / authority / audience) is. The
  keyless floor produces the strategy (reasoning_only); the content calendar (`plan-my-content`) and copy
  (`write-post-copy`) are the execution layer beneath it; the branded VISUAL studio is the library module
  above it. So `make-social-post` (a heavy render studio) leaves the zero-state cold-win slot and is slated
  for the library; the cold social win becomes `build-social-strategy`.
- **Roadmap impact:** introduces a future "Creative Engine + off-the-shelf library" phase (the library
  mechanism + the genericised Remotion module + the brand-kit builder). Pre-ship hardening only adds the
  keyless `build-social-strategy` win and re-tiers `make-social-post` out of the zero-state cold offers.

## D14 — The Content Creation Studio: the genericised Remotion engine ships in-repo as `studio/motion` (2026-07-09)
- **What:** build the genericised, brand-agnostic Remotion video studio and ship it IN-REPO as `studio/motion`, module one of an umbrella "Content Creation Studio" hub. Keyless-first, brand-driven via `brand/brand.json`, guided for a non-dev owner. Full spec + phased plan: [2026-07-09-content-creation-studio-design.md](2026-07-09-content-creation-studio-design.md).
- **Realizes D13** ("the genericised Remotion creative studio is a tier-1 library module, a future build"). This is that build. It chooses the **in-repo module** over D6's cross-repo **RVS bridge** for the full creative-studio scope — the same move Decision 8 made for the floor/YouTube case.
- **Revises (LABELLED)** the single line in [2026-07-05-youtube-studio-design.md](2026-07-05-youtube-studio-design.md) Decision 8(b) that said "the heavyweight Remotion render engine stays *only* in `Remotion-VideoStudio`." A genericised Remotion engine now also lives in BOS at `studio/motion`. Decision 8 otherwise stands: the keyless `studio/video` floor is untouched.
- **Accepted cost:** BOS carries two render engines (keyless Puppeteer floor + Remotion premium module). Justified — they are different rungs on the floor/shelf ladder, not a reskin of each other. The floor's keyless promise is preserved; Remotion is the premium shelf.
- **Product shape (founder calls, 2026-07-09):** lead with faceless + talking-head modes; the "watch it get built" product-demo / Claude-chat kit is a separate labelled founder/SaaS add-on, off the default owner flow. Talking-head captions are keyless via local whisper.cpp. Installs via `update-bos` like other add-ons.
- **Remotion licence:** no API key, but a 4+ person for-profit company needs a paid Remotion Company Licence to publish commercially — surfaced as a one-time in-flow acknowledgement; marketed as "no API keys," never "free."
- **Roadmap impact:** supersedes D13's "future build / not-yet" status for the creative studio (now in build). The RVS repo itself is untouched (it is the source of the port, not modified); decoupling its source from TrustPager is a medium mechanical sweep (spec §4).
