# SEO Floor Extraction — the get-found-online skill + the TrustPager→floor extraction pattern

**Status:** Approved design (founder-approved 2026-07-02). Part 2 of the two-part
effort (Part 1 = consultative intake, shipped). Scope ruled by founder:
**flagship + reuse**; the reusable pattern lives in an architecture doc.

---

## 1. Why

The keyless floor has no SEO front door (verified: no SEO skill in `skills/`; only
incidental keyword mentions). The TrustPager side has a full paid SEO suite
(site audit, keyword research with volumes, rank tracking, backlinks, competitor
gap, local audit, SERP snapshots, AI-visibility) — every tool requires a
`website_id`, `seo:write` scope, and **costs credits**, so it is firmly the
connected/paid tier. This is the ideal pilot for extracting a TrustPager
capability to the keyless floor: keep the *method*, build the *keyless-computable
slice* bounded, and mark the *paid-data* functions as connected deepeners.

## 2. The capability map (what extracts, what doesn't)

| TrustPager SEO tool | What it does | Floor treatment |
|---|---|---|
| `seo_run_site_audit` | Crawl ≤100 pages: titles, broken links, slow pages | **Keyless (bounded):** Firecrawl `scrape` on ~5-8 owner-named key pages → titles, meta, single-H1, headings, alt text, internal links, schema hints, NAP. No `crawl`/`map` (paid) — per-page scrape only. |
| `seo_local_audit` | Map-pack listings, ratings, reviews | **Keyless (partial):** `search` the business + "[service] [suburb]"; check presence, review recency/volume, profile signals. Maps onto `business-method.md` §10.5 local gravity stack. |
| `seo_serp_snapshot` | Live top organic results for a keyword | **Keyless:** `search` captures live top results for 1-3 target terms. |
| `seo_competitor_gap` | Keywords a competitor ranks for | **Keyless (content gap only):** scrape one rival, compare coverage. Ranking-gap needs paid data → deepener. Delegates to `research-a-competitor`. |
| `seo_keyword_research` | Keywords + volume, CPC, difficulty | **Keyless (ideas only):** topic/intent ideas from SERP observation; real volumes/difficulty are paid → deepener. Threads into `plan-my-content`. |
| `seo_ai_visibility` | Brand visibility in AI answers | **Keyless (spot-check):** directional check via `search`; at-scale is paid → deepener. |
| `seo_backlinks` | Referring domains, domain rank | **Connected-only:** needs a paid backlink index. Deepener doorway. |
| `seo_track_keywords` | Recurring rank monitoring | **Connected-only:** needs platform + scheduling. Deepener doorway. |

## 3. The flagship skill — `get-found-online`

**Frontmatter (keyless firecrawl contract, per `knowledge/research-method.md`):**
```yaml
function_slot: research
requires_driver: firecrawl
requires_credential: none
data_path: fetch_rest
status: active
```
Driver in the manifest; firecrawl tools called in the BODY (never in `uses_tools`).
**Scope clamp (HARD):** `scrape` / `search` only — never `crawl` / `map` / `agent`
/ `extract` (those are paid and off-floor). The per-page scrape model IS the
"bounded, ~5-8 pages" guardrail.

**Purpose:** a bounded "are you findable, and what to fix first" audit that ends
in a prioritized fix list the owner can action this week. Reads like a
switched-on operator audited them in ten minutes, not an SEO tool's raw report.

**Gate-led flow:**
1. **Anchor + scope (bounded).** Pull owner identity from the profile (trade,
   patch, who they serve) or ask one line. Get: site URL, business name,
   location, and the ~3-5 key pages that matter (home + top services). No site →
   run the local-visibility path only and advise on the site. Hard cap ~5-8
   page-scrapes; if they name more, audit the most important and say so (no
   silent truncation).
2. **On-page pass** (`scrape` each key page): title tag (present, length, does it
   name the service + place), meta description, exactly one H1, heading
   structure, image alt text, internal links between pages, schema hints, and for
   local: visible NAP (name/address/phone) and a clear CTA. Flag issues per page.
   **Read internal-link and schema signals from the scraped page content only;
   never follow them into additional fetches beyond the ~5-8 cap** (that would be
   crawl/map, which is off-floor).
3. **Local-visibility pass** (`search`): does the business show for its name and
   for "[service] [suburb]"; review recency/volume, profile completeness signals.
   **Priority is driven by the §10.5 gravity-stack order** (its six tiers, in
   order: 1 answer speed → 2 review engine → 3 profile completeness → 4 proof
   publishing → 5 community presence → 6 paid local), including the hard gate: do NOT
   lead with content/keyword work if answer-speed or a review-ask are missing —
   those come first.
4. **SERP/intent spot-check** (`search`, 1-3 target terms): who ranks, what page
   type wins, is it realistically winnable. Grounds topic ideas in reality.
5. **Competitor content-gap (owner-invited, one rival).** Offer to read one named
   local competitor for coverage they have and the owner doesn't. Delegate to
   `research-a-competitor` (its SEO lens) rather than re-implement.
6. **Prioritized fix list.** 3-7 fixes, highest-leverage first, ordered by the
   gravity stack — not a keyword laundry list (§4 item 7: a diagnosis outputs
   1-3 moves, not eight pages; lead with the top few). Each fix: what, why it
   matters (in plain words), and the *exact*
   change — the rewritten title tag, the review-ask script, the one page to add.
   Usable today. Positive/outcome-led output, no em dash.
7. **Connected doorway.** Mark what deepens when an SEO tool is connected: real
   search volumes/difficulty, backlink profile, ongoing rank tracking,
   AI-visibility at scale. Outcome-only framing; reactive per the BOS rule —
   surfaced via `whats-possible`, never a cold TrustPager pitch.

**Guardrails:** bounded (≤~8 scrapes, 1 competitor, ≤3 terms), token-frugal,
finishable in one sitting. Firecrawl empty/slow → say so, offer to work from
pasted page content or `WebSearch`/`WebFetch` fallback. Confirm scraped identity
before trusting. Region-agnostic (works anywhere; local `search` uses whatever
location the owner gives — the paid `seo_*` tools default AU, the keyless floor
does not need a region set).

## 4. Reuse (light threading, no duplication)

- **`research-a-competitor`:** add a short SEO/content-gap lens — what
  pages/topics/services the rival covers for search that the owner doesn't, and
  how their site is structured for findability. Cross-ref `get-found-online`.
  (Keep its existing one-page-read shape; this is an added angle, not a rewrite.)
- **`plan-my-content`:** add search-intent topic selection — bias topic choice
  toward what people actually search and what's realistically winnable, cross-ref
  `get-found-online`. Keep its 1-2 week bound. **Critical:** `plan-my-content` is
  `requires_driver: none / reasoning_only` — the threading must NOT make it fire a
  firecrawl `search` itself (that would break its manifest and make it a network
  skill). It *consumes* a SERP spot-check the owner brings from `get-found-online`
  (or reasons from the owner's stated terms); it never fetches.

## 5. Knowledge home — `knowledge/seo-method.md`

The one home for SEO method: the on-page/technical checklist (what a good title
/meta/H1/heading/alt/internal-link/schema/NAP setup looks like) and the keyless
SERP-reading method (how to read a `search` result set for intent, page-type,
and winnability). It **links to `business-method.md` §10.5 for local strategy
rather than restating it** (one home). `get-found-online` references this file so
the SKILL.md stays lean and gate-led (per the CLAUDE.md skill standard). Ends
with the positive-only + no-em-dash output rule, like the other method files.

## 6. The codified pattern — `docs/architecture/trustpager-to-floor-extraction.md`

The reusable recipe for taking any TrustPager capability to the keyless floor,
with SEO as worked example #1:
1. **Inventory the capability** — list the tools/functions and what each returns.
2. **Split each function by data-dependency** — keyless-computable (via
   Firecrawl `scrape`/`search`, `WebSearch`/`WebFetch`, or pure reasoning) vs
   paid-data-only (search volumes, indexes, rank tracking, scale).
3. **Keep the method wholesale** — the doctrine/how-to is always extractable; it
   is knowledge, not data. It goes in a `knowledge/*-method.md`.
4. **Build the keyless slice bounded** — floor doctrine: finishable in one
   sitting, bounded, token-frugal; obey the firecrawl scope clamp
   (`scrape`/`search`/`interact` only).
5. **Mark paid functions as connected deepeners** — a doorway routing to the MCP
   tools, "gets sharper when connected," outcome-only, reactive framing.
6. **Reuse existing floor skills** for adjacent surface — thread, don't duplicate.
7. **Anchor in business-method doctrine** where one applies (SEO → §10.5).
8. **Name outcome-led + plain, register keyless, dogfood on Sonnet.**

The doc names the two guard scripts the pattern must pass: `tools/manifest.py`
(no `mcp__…` in a keyless skill's `uses_tools`) and
`tools/check-onboarding-binding.py` (no TrustPager coupling tokens in a
`credential:none` body). A firecrawl driver + body-level tool calls passes both.

## 7. Wiring + validation

- **Register** `get-found-online` in `kernel/registry.json` — copy the
  `research-a-competitor` entry exactly (`data_path: fetch_rest`,
  `function_slot: research`, `requires_credential: none`,
  `requires_driver: firecrawl`, `status: active`, **no `uses_tools` key**).
- **Do NOT hand-edit `skills/whats-possible/SKILL.md`** — it is a runtime
  registry reader and its own hard rules forbid a hand-kept list. Once the skill
  is `status: active` in the registry it appears there automatically.
- **Add it to `knowledge/starter-projects.md`** — the hand-maintained onboarding
  menu (and one of the three files `check-onboarding-binding.py` scans). Add a
  `[live] … keyless` row in the relevant group table (Win-work / market), add it
  to the §2 "Live keyless core" pool, and add an entry to the §4 relief→project
  mapping under "finding leads / get more known" so the 3-options selection can
  reach it.
- **Manifest/lint:** `python tools/lint-skill.py skills/get-found-online` clean;
  manifest + onboarding-binding checks green (keyless).
- **Offline tests:** per `research-method.md`, mock/skip the fetch; test the
  synthesis (feed a fixture page payload, assert the audit produces the right
  structured fix list ordered by the gravity stack). Keep the offline suite green.
- **Dogfood on Sonnet:** a local tradie with a thin one-page site + few reviews.
  Pass bar: the fix list LEADS with the gravity-stack order (answer speed +
  review-ask before content/keywords), gives exact changes (a rewritten title
  tag), stays bounded (no 100-page crawl, no invented volumes), and marks the
  connected deepeners without a cold TrustPager pitch. Output positive-only, no
  em dash.
  **Result (2026-07-02): 5/5 PASS** on a Ballarat plumber who asked to "rank for
  plumber Ballarat" — the skill overrode the stated goal, led with missed-call
  text-back + review engine, gave an honest directory-dominated-SERP winnability
  read, stayed bounded (1 scrape + 2 searches), and handed exact fixes. Dogfood
  surfaced one fix now applied: Step 2 now instructs *how* to phrase the reorder
  of the owner's stated goal (validate → bridge → reorder, never silent), the
  highest-trust-risk moment in the skill.

## 8. Non-goals (YAGNI)

- No paid-data features on the floor (volumes, backlinks, rank tracking) — those
  stay connected-tier deepeners.
- No `crawl`/`map`/`agent`/`extract` — off-floor.
- No standalone keyword or content-gap skill this round (folded into the flagship
  + the two reused skills).
- No CEO skill in this spec (separate, later).
- The pattern doc describes the recipe; it does not pre-build future extractions.
