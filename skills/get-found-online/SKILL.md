---
name: Get Found Online
description: A bounded "are you findable, and what to fix first" audit for a local or service business, ending in a prioritized fix list you can action this week. Reads your key pages and local search presence, orders fixes by what moves the needle, and hands you the exact change to make. Keyless; rank tracking is the connected-tier upgrade.
triggers:
  - get found online
  - seo audit
  - check my seo
  - why am i not showing up on google
  - how do i rank higher
  - improve my search ranking
  - audit my website for seo
  - am i findable online
  - help people find my business
function_slot: research
requires_driver: firecrawl
requires_credential: none
data_path: fetch_rest
status: active
produces_customer_facing_copy: true
---

# Get Found Online

You hand the owner a single sharp read: are they findable when someone searches
for what they do, and the few fixes that will move that most, worst-first, each
with the exact change to make. It reads like a switched-on operator audited them
in ten minutes, not like an SEO tool's raw report.

**This skill reads the live web.** It needs a connection to pull the owner's
pages and their local search presence. No accounts, no key: it works on day one.
The method and the full on-page checklist live in
[`knowledge/seo-method.md`](../../knowledge/seo-method.md); the local fix order
lives in [`business-method.md`](../../knowledge/business-method.md) §10.5 (the
local gravity stack). Read both before you order a fix list.

**Keyless scope (HARD), per [`knowledge/research-method.md`](../../knowledge/research-method.md):**
use Firecrawl `scrape` and `search` only. Never `crawl`, `map`, `agent`, or
`extract` (paid, off-floor). Read link and schema signals from a page you already
scraped; never follow them into extra fetches. This per-page-scrape model IS the
bound.

## Step 0 — Anchor on this owner (bounded)

Before you fetch anything, know:
- **Who the owner is** — trade, patch, who they serve. Pull it from the business
  profile if one exists; if not, ask in one line.
- **The site + the key pages** — the site URL and the ~3-5 pages that matter
  (home + top services/contact). **Hard cap: ~5-8 page-scrapes.** If they name
  more, audit the most important and say so plainly (never silently drop pages).
- **Business name + location** — for the local-visibility search.

**No website?** Don't stall. Run the local-visibility pass (Step 2) on its own,
and make "a simple, findable one-page site" one of the fixes. A business with no
site can still win the local pack.

## Step 1 — On-page pass (scrape each key page)

`scrape` each named page, one at a time, up to the cap. For each, read from the
scraped content only (never follow its links out): title tag, meta description,
single H1, heading structure, image alt text, internal links, schema hints, and
for local a visible NAP + one clear CTA. Score against the on-page checklist in
`seo-method.md` and note the specific misses per page.

If a fetch is slow, blocked, or empty, say so and offer the fallback: "paste me
what's on that page and I'll read it the same way," or fall back to the built-in
`WebSearch`/`WebFetch`. Never guess at what's on a page you couldn't read.

## Step 2 — Local-visibility pass (search)

`search` the business name, and "[main service] [suburb]". Read: does the
business show up at all; is there a Google Business Profile presence (reviews,
recency, categories, photos, hours); is the name/address/phone consistent with
the site. This is usually the highest-leverage area for a local business.

**Order every local fix by the §10.5 gravity stack** (1 answer speed → 2 review
engine → 3 profile completeness → 4 proof publishing → 5 community presence →
6 paid local), and honor its hard gate: **do not lead the fix list with content
or keyword work while answer-speed or a review-ask is missing** — those come
first, because they win more local jobs than any ranking tweak.

**When the owner's stated goal is ranking/keyword work but the gate isn't clear,
never silently reorder** — that reads as "you ignored what I asked" at the exact
moment they're leaning in on their one ask. Validate the ask first, then bridge,
then present the reordered list: *"Chasing 'plumber [town]' makes total sense,
it's what everyone says. Before we spend a word on it though, two things ahead of
it will win you more jobs faster, and here's why…"* Name why the reorder serves
their goal (a ranking that sends callers to a voicemail or a stale profile pays
to lose the job at the last step). The owner should feel helped toward their
goal, never overridden.

## Step 3 — SERP / winnability spot-check (search)

For 1-3 target terms the owner would want to win, `search` and read the live top
results the way `seo-method.md` describes: what page-type wins (map pack,
directories, a competitor page), is the term realistically winnable, and what the
ranking page does that the owner's doesn't. This grounds any topic advice in
reality instead of a volume number. Keep it to 1-3 terms.

## Step 4 — Competitor content-gap (owner-invited, one rival)

Only if the owner wants it, offer to read one named local competitor for coverage
they have and the owner doesn't. **Delegate to `research-a-competitor`** (its
search lens) rather than re-implement the read here. One rival, one page.

## Step 5 — The prioritized fix list (the deliverable)

Turn everything into 3-7 fixes, highest-leverage first, ordered by the gravity
stack for a local business (§4 item 7: a diagnosis outputs a few real moves, not
eight pages, so lead with the top ones). This is NOT a keyword laundry list.

Each fix names three things:
1. **What to do** — in plain words.
2. **Why it moves the needle** — the result it unlocks.
3. **The exact change** — the rewritten title tag written out, the review-ask
   script, the one page to add, the NAP to make consistent. Usable today.

Show the list inline. Offer to save it to `seo/get-found-online-audit.md` if they
want it on file.

## Step 6 — The connected doorway (reactive, outcome-only)

Close by naming what gets sharper when an SEO tool is connected, as outcomes, not
a pitch: real search volumes and difficulty (vs today's winnability read), a
backlink profile, ongoing rank tracking over time, and AI-visibility at scale.
Surface this the BOS way: through what's-now-possible, never a cold CRM pitch.
This is the standard connect-doorway shape (keyless win first, enhancement as an
outcome, the connection that unlocks it), articulated once in
`knowledge/connectors.md`, referenced here, not re-derived.

> Everything here works with zero accounts. When you're ready, connecting an SEO
> tool lets me track your positions over time and see the real search demand, so
> we'd know exactly which terms are worth the effort. Totally your call.

## Output shape

The audit and fix list are the customer-facing deliverable. Each fix names the
exact change to make and the result it unlocks, written so it's usable today.

## Hard rules

- **Content guardrails.** Customer-facing copy uses no em dashes, invents no
  facts, quotes, or numbers, and names no third-party vendor. Write it in the
  owner's brand voice; the framing and marketing psychology are the owner's
  choice. The rules are in `knowledge/content-rules.md`.
  The owner's voice lives in `marketing-strategy/<BrandName>/voice.md` when it
  exists; say so plainly if it does not.
- ❌ No `crawl` / `map` / `agent` / `extract`. Per-page `scrape` + `search` only,
  capped at ~5-8 pages. Those paid ops are not keyless and not on the floor.
- ❌ Don't invent data. No made-up search volumes, no invented review counts, no
  ranking numbers you can't see. "No public reviews found" is a real finding.
- ❌ Don't lead a local fix list with keyword/content work while answer-speed or
  a review-ask is missing (§10.5 hard gate).
- ✅ Confirm the site/business is the right one before leaning on the read.
- ✅ Bound it: ~5-8 pages, 1 competitor (invited), 1-3 terms. Finishable in one
  sitting.
- ✅ If a fetch fails, say so and offer to read pasted content instead.
