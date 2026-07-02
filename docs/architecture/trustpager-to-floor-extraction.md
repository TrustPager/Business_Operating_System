# TrustPager → Floor Extraction — the reusable pattern

How to take a capability that lives on the connected TrustPager side (paid,
MCP-tool-backed) and give the keyless floor a genuine version of it. The goal is
to widen how much impressive business coverage a brand-new owner has on day zero,
without lying about "keyless" and without duplicating what a connected tool does
better.

**Worked examples (built):**
1. **SEO** — `skills/get-found-online`, `knowledge/seo-method.md`, spec
   `docs/architecture/2026-07-02-seo-floor-extraction-design.md`.
2. **Proof / reputation** — `skills/build-my-proof` (transformation-story engine),
   `knowledge/proof-and-referrals-method.md`.
3. **Referrals** — `skills/set-up-referrals`, same method file.
4. **Call coaching** — `skills/coach-my-calls` (references `business-method.md`
   §12.5 directly). Batch spec:
   `docs/architecture/2026-07-02-proof-referrals-coaching-extraction.md`.

Read the SEO example alongside this recipe; the proof/referrals/coaching batch
shows the same split applied to method-heavy capabilities.

---

## The core insight

A TrustPager capability is three things stacked together:
1. **A method** — the know-how (how to audit SEO, how to score a lead, how to
   structure a proposal). This is *knowledge*, and knowledge always extracts.
2. **A keyless-computable slice** — the parts a floor skill can genuinely do with
   Firecrawl `scrape`/`search`, the built-in `WebSearch`/`WebFetch`, the local
   document tools, or pure reasoning over what the owner types.
3. **A paid-data / platform slice** — the parts that need a paid index, an API
   key, persistent storage, scheduling, or scale (search volumes, backlink
   graphs, rank tracking, live CRM data, recurring automation).

The extraction keeps (1) wholesale, builds (2) bounded on the floor, and leaves
(3) as a "gets sharper when connected" doorway. Most capabilities split cleanly
this way once you look tool-by-tool.

## The recipe (eight steps)

1. **Inventory the capability.** List its tools/functions and what each returns.
   For an MCP capability, load the tool schemas (via ToolSearch) — the
   descriptions and required scopes tell you what is paid ("costs credits",
   `*:write`, a `website_id`/account id) versus computable.

2. **Split each function by data-dependency.** For every function, decide:
   keyless-computable, partially computable (a directional keyless version
   exists), or paid-only. Write the split as a table (see the SEO spec §2). Be
   honest — a directional keyless version is fine and useful, but label it
   directional, never dress paid data up as if the floor has it.

3. **Keep the method wholesale.** Put the know-how in a `knowledge/<x>-method.md`
   file: the checklists, the how-to, the way to read the keyless signals. Link to
   `business-method.md` where a diagnosis doctrine already owns the strategy (SEO
   links to §10.5 for local) rather than restating it — one home, no drift.

4. **Build the keyless slice bounded.** A new `skills/<x>/SKILL.md`, gate-led and
   lean (it references the method file). Obey the floor doctrine: finishable in
   one sitting, bounded (cap the pages/items/terms), token-frugal. For web reads,
   obey the `knowledge/research-method.md` scope clamp — `scrape`/`search`/
   `interact` only, never `crawl`/`map`/`agent`/`extract` (those are paid).

5. **Mark the paid slice as a connected deepener.** A short doorway at the end of
   the skill that names what gets sharper when a tool is connected, as *outcomes*,
   reactively — never a cold TrustPager pitch. This is the honest upsell: the
   floor version is real and complete for what it does; the paid version adds the
   data the floor structurally can't get.

6. **Reuse existing floor skills for adjacent surface.** If a nearby skill already
   owns part of the ground, thread a lens into it rather than duplicate (SEO added
   a content-gap lens to `research-a-competitor` and a search-intent lens to
   `plan-my-content`). Keep threads additive; do not turn a `reasoning_only` skill
   into a network skill by accident (the `plan-my-content` caveat).

7. **Anchor in business-method doctrine where one applies.** If the diagnosis
   brain already has the strategy (which constraint this serves, the priority
   order), the keyless skill should execute against it, not invent its own. This
   is what makes the floor version feel like an operator, not a checklist.

8. **Name outcome-led + plain, register keyless, dogfood on Sonnet.** Outcome-led
   plain name (e.g. `get-found-online`, not `seo-audit-tool`). Register it and
   wire discovery (below). Then dogfood on Sonnet (the client run-tier) with a
   realistic owner; the pass bar is that it does the keyless slice well, stays
   bounded, marks the deepener without a cold pitch, and outputs positive-only /
   no em dash.

## The wiring checklist (where a new floor skill must land)

- **`kernel/registry.json`** — the entry (the routing allow-list + credential/
  data_path source of truth). Copy the nearest sibling's shape. A keyless
  firecrawl skill: `data_path: fetch_rest`, `requires_driver: firecrawl`,
  `requires_credential: none`, and **no `uses_tools` key** (driver in manifest,
  tools called in the body).
- **`knowledge/starter-projects.md`** — the hand-maintained onboarding menu (a
  group table row + the §2 keyless-core pool + the §4 relief→project mapping).
  This is what makes the skill reachable from the 3-options selection, and it is
  one of the three files `check-onboarding-binding.py` scans.
- **Do NOT hand-edit `skills/whats-possible/SKILL.md`** — it reads the live
  registry; a `status: active` skill appears there automatically.
- **`docs/CAPABILITIES.md`** — generated. Run `python tools/export-capabilities.py`
  and commit the result (the fresh-export test enforces this).

## The two guard scripts the pattern must pass

- **`tools/manifest.py`** forbids any `mcp__…` tool in the `uses_tools` of a
  `requires_credential: none` skill. Resolution: a keyless web skill declares the
  `firecrawl` driver and calls the firecrawl tools in the SKILL.md *body* — its
  `uses_tools` stays empty/absent, which passes.
- **`tools/check-onboarding-binding.py`** forbids TrustPager coupling tokens
  (`mcp__trustpager__*`, `dump-crm-bundle`, `dump-transcripts`,
  `api.trustpager.com`) in a `credential:none` body, and checks every onboarding
  offer is a real keyless win. A firecrawl body reference is not a coupling token,
  so it passes; `firecrawl` is in the check's keyless-driver set.

## Guardrails (what NOT to do)

- ❌ Don't put a paid feature on the floor (real volumes, backlink graphs, rank
  tracking, live CRM data). Those are deepeners, not floor.
- ❌ Don't dress directional keyless output up as hard data. Label estimates.
- ❌ Don't duplicate an existing skill's job — thread a lens instead.
- ❌ Don't make a `reasoning_only` skill fetch. If a thread needs live web, the
  fetch belongs in the firecrawl skill, and the reasoning skill consumes its
  output.
- ❌ Don't pitch TrustPager cold in the deepener doorway — outcomes only,
  reactive, per the §8 CRM-framing rule in the onboarding design.

## Candidates for the next extraction

Reputation/reviews, referrals, and call-coaching are now BUILT (worked examples
2-4 above). The same split still applies to remaining candidates with a large
keyless method + a paid data/automation tail:
- **Lead scoring / triage** — the scoring method is keyless (score a pasted lead
  list against an ICP); live scoring on inbound is the connected deepener.
  (`lead-triage` exists connected; a keyless slice is extractable.)
- **Needs-analysis → proposal inputs** — better as a lens threaded into
  `transcript-summary` → `write-a-proposal` than a standalone skill (heavy
  overlap); noted, not yet built.
- **Sales-pipeline design** (`ai_generate_pipeline`) — keyless pipeline/stage
  design as a spec; medium value, no floor home yet.
- **Prospect-list building** (`lead_gen_search`) — keyless slice is token-heavy
  and brushes the Firecrawl scope clamp; `research-before-call` covers the
  single-prospect case. Watch.

Genuinely native (leave connected): voice agents (telephony), automations, work
orders, signing, scheduling/bookings, live reporting, inventory. Each new
extraction gets its own spec; this recipe is the starting point.
