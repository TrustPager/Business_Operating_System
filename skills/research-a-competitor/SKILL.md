---
name: Research A Competitor
description: Read one rival's page and turn it into a sharp one-page operator's read — how they position, what they appear to charge, the offers they lead with, and where the openings are for YOUR business. One competitor, one page-read, built from the live web. No accounts or files needed.
triggers:
  - research a competitor
  - check out this competitor
  - read this rival's website
  - what is this competitor charging
  - how does this competitor position themselves
  - size up this competitor
  - look at this competitor's pricing
  - competitor read
function_slot: research
requires_driver: firecrawl
requires_credential: none
data_path: fetch_rest
status: active
---

# Research A Competitor

You take one rival's URL and hand the owner a single sharp page: how that
competitor positions, what they appear to charge, the offers they lead with,
and where the real openings are for THIS owner's business. It reads like a
switched-on operator sized them up in five minutes, not like a market report.

**This skill reads the live web.** It needs an internet connection to pull the
competitor's page. There are no accounts to connect and no key to enter: the
read works on day one. If there's no connection, say so plainly and offer to
work from anything the owner can paste instead.

The convention this follows is
[`knowledge/research-method.md`](../../knowledge/research-method.md) — read its
scope clamp before you fetch. One competitor, one page-read. Stay inside
`scrape` and `search`; never reach for bulk crawl, whole-site mapping, or
autonomous extraction.

## Step 0 — Anchor on THIS owner

A competitor read is only useful relative to the owner it's for. Before you
fetch anything, know two things:

- **Who the owner is** — their trade, their patch, who they serve. Pull this
  from the business profile if one exists; if not, ask in one line ("quick one:
  what do you do and where, so I can read this rival against you?").
- **The one rival URL** — the page the owner wants read. One page. If they
  hand you a bare business name instead of a link, use `firecrawl-search` on
  the name to find their main page, confirm it's the right business, then read
  that one page.

## Step 1 — Read the rival's page

Use the `firecrawl-scrape` skill on the single URL to pull clean content. That
one page (usually a home or services/pricing page) is the source. If the page
the owner gave is thin, you may run one `firecrawl-search` on the business name
to surface their pricing or reviews page, then read that. Keep it to one
page-read: do not walk the whole site.

If the fetch is slow, blocked, or comes back empty, don't stall and don't
guess. Say so ("couldn't get a clean read of that page") and offer the
fallback: "paste me what's on their site and I'll read it the same way."

**Read only what's on the page.** If a competitor's price isn't published, the
honest line is "no public pricing — they make you ask," which is itself a
finding. Never invent a number or a claim that isn't there.

## Step 2 — Synthesise the one-page read

Turn the page into four parts. Sharp, specific, and always anchored to
something actually on the page.

1. **How they position.** The promise they lead with and who they're talking
   to, in their own words. Quote the headline or hero line if it's telling.
2. **What they appear to charge.** Published prices, packages, or "from $X"
   signals. If pricing is hidden, say so and note what that implies (quote-only,
   premium-by-design, or simply not shown).
3. **The offers they lead with.** The packages, guarantees, free trials,
   bundles, or hooks on the page — what they're using to win the click.
4. **The openings for this owner.** Two or three places where THIS owner can
   stand apart: an angle the rival under-plays, a proof point the owner has and
   they don't, a segment the rival ignores. Each opening is framed as a move the
   owner can make, tied to what you saw on the page.

## Step 3 — Hand it over

Show the read, name the URL it came from, and point to the one or two openings
worth acting on first. If the owner wants, offer to save it to
`research/<competitor-name>-read.md`.

Then offer the natural next step in plain language, without overselling:

> Want me to turn the strongest opening into a positioning line or a content
> angle for you? And once your CRM is connected, I can keep a read like this on
> file against the right account so it's there next time you're pitching head to
> head.

## Output shape — positive-only, no em dashes

The read is customer-facing output: it follows the positive-only rule and uses
no em dashes (use commas, colons, parentheses, or separate sentences).

Frame the owner's openings as forward moves, never as what they lack. Naming a
rival's gap is fair game as a sharp observation ("they bury their pricing, so a
clear up-front price page would beat them on trust"). Framing the owner by
absence is not ("you don't have X yet"). Lead with the result the owner can go
get.

Template:

```
Competitor read: [Rival name]  (from [URL])

How they position:
  [one or two lines, their promise + who it's for, quoting the page]

What they appear to charge:
  [published prices / packages, or "no public pricing, quote-only"]

Offers they lead with:
  • [offer / hook 1]
  • [offer / hook 2]

Openings for you:
  1. [a move the owner can make, tied to the page]
  2. [a second move]
```

## Hard rules

- ❌ One competitor, one page-read. No crawling the whole site, no mapping every
  URL, no autonomous extraction (those need a paid key and aren't keyless).
- ❌ Don't invent prices, offers, or claims that aren't on the page. "Not
  published" is a real, useful finding.
- ❌ Don't frame the owner by what they lack. Openings are forward moves.
- ✅ Confirm the page is actually the right competitor before leaning on it.
- ✅ Quote the page where the exact words matter, so the owner trusts the read.
- ✅ If the fetch fails, say so and offer to read pasted content instead.
