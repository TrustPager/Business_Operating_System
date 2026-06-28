---
name: Research Before Call
description: Walk into any prospect or partner meeting as the most prepared person in the room. Give me one name (a person or a company) and I'll build a one-page pre-meeting brief covering who they are, what they do, and the recent signals worth knowing, plus three sharp questions that open the conversation on your terms. Built keylessly from live web research; no accounts or files needed.
triggers:
  - research before call
  - research this prospect
  - brief me on this company before the meeting
  - who is this person I'm meeting
  - look up this company before the call
  - pre-meeting brief
  - prep me on a new prospect
function_slot: research
requires_driver: firecrawl
requires_credential: none
data_path: fetch_rest
status: active
---

# Research Before Call

The operator has a meeting with someone new (a prospect, a referral partner, a
supplier) and wants to walk in already knowing the room. Give them one page that
makes them the sharpest person at the table: who this person or company is, what
they actually do, the recent signals worth raising, and three questions that earn
respect in the first two minutes.

This builds on the keyless web-research convention in
[`knowledge/research-method.md`](../../knowledge/research-method.md) and follows
the same shape as `research-a-competitor`. Read that method doc first if you
haven't. The short version: web reading here is keyless and online, scoped to
`scrape` / `search` only, and synthesised into a tight customer-facing brief.

## Bounded: one prospect per run

One name in, one brief out. If the operator hands you a list, do the first and
say you'll take the rest one at a time. A focused single brief beats a shallow
batch; this is a pre-meeting weapon, not a bulk enrichment run.

## Step 1: pin down who you're researching

Get one clear subject before you fetch anything:

- **A company name** (with a website if they have one): research the business.
- **A person plus their company**: research the person in the context of that
  company (their role, what they own, what they've said publicly).
- **Just a person, no company**: ask the one question that unlocks it. "What
  company are they with, or what's the meeting about?" A name with no context
  produces a guess, not a brief.

Confirm the subject back in one line before you spend the research on it
("Researching Dana Liu, ops lead at Brightwater Plumbing, that the one?"). A
confident brief about the wrong person is worse than no brief.

## Step 2: gather the signals (keyless web research, scrape + search only)

Web reading here is keyless and online. Use the `firecrawl-scrape` and
`firecrawl-search` skills (no key needed). Stay inside `scrape` and `search`.
Do not reach for bulk crawl, sitemap mapping, or autonomous extraction; those
sit outside the floor scope set in the research method.

Pull from these sources, in order:

1. **Their own website.** `firecrawl-scrape` the company site (home, about,
   services, team/leadership page if there is one). This is the strongest
   source for what they do, how they describe themselves, who runs it, and the
   words they use about their own work.
2. **A focused search on the name.** `firecrawl-search` the company name (and
   the person's name if you have one) to surface recent signals: news, a funding
   or hiring note, an award, a new location, a press mention, a podcast or
   article quote, directory and review listings.
3. **Their public footprint.** `firecrawl-search` for a public professional
   profile or socials to confirm a role, tenure, or a recent post worth
   referencing in the room.

**Stay honest about what you find.** If a search is thin, blocked, or comes back
empty, say so plainly and build the brief from what you do have, rather than
padding it with guesses. Mark anything you're inferring as an inference, not a
fact. One verified detail the operator can open with beats five shaky ones.

**Confirm identity before leaning on a find.** Common name, multiple companies,
a stale listing: when there's any doubt it's actually them, flag it instead of
asserting it ("there's a Brightwater Plumbing in two states; this brief assumes
the WA one, say if it's the other").

## Step 3: synthesise the one-page brief

One page, scannable in the lift on the way to the meeting. Use this shape:

```
PRE-MEETING BRIEF: <Person / Company>  ·  <meeting context if known>

WHO THEY ARE
  <2-3 lines: the person's role and what they own, or the company's size,
   location, and where they sit in their market. Plain, specific, sourced.>

WHAT THEY DO
  <2-3 lines: their actual service or product, who they serve, and how they
   describe their own strength, in their words where you found them.>

RECENT SIGNALS
  → <a fresh, datable signal: a new hire, a new location, an award, a launch,
     a press mention, the kind of thing that shows you did the homework>
  → <a second signal if you found one; mark "(inferred)" if it's a read,
     not a confirmed fact>

WHERE YOU CONNECT
  <1-2 lines: the genuine overlap, what the operator offers that lines up
   with where this prospect is clearly heading. The reason this meeting is
   worth both people's time.>

THREE QUESTIONS THAT MAKE YOU THE PREPARED ONE
  1. <a question that proves you read their world, references a real signal>
  2. <a question that opens the value conversation on their terms>
  3. <a forward question about where they want to take things next>
```

### What makes the three questions sharp

- Each one is anchored in something real you found (a signal, a service, a
  stated goal), so it lands as "they actually looked into us," not a template.
- They open doors rather than interrogate. Aim them at where the prospect wants
  to go, so answering them feels good and moves the conversation toward value.
- Order them as a flow: earn credibility, open the value, then look forward.

## Step 4: hand it over

Show the one-page brief and point out the one detail most worth leading with
("if you open by mentioning their new Joondalup branch, you'll have them in the
first thirty seconds"). Offer to save it alongside the meeting if useful.

Then, only if it fits, mention the natural next step in plain language, without
turning it into a setup task:

> Once your customer records are connected, I can also keep this brief on the
> prospect's file and pull their history into it automatically, so every future
> meeting starts from everything you already know about them.

That's an outcome described in words, offered as a future convenience, never a
prerequisite. The brief stands on its own today, from the open web alone.

## Hard rules

- ✅ **One subject per run.** One name in, one brief out. A list gets done one at
  a time.
- ✅ **Scrape and search only.** Keyless web reading stays inside those two
  operations (see `knowledge/research-method.md`). No bulk crawl, mapping, or
  autonomous extraction on the floor.
- ✅ **Confirm identity before trusting a find.** Name the assumption when a
  subject is ambiguous; a wrong-person brief costs more trust than a thin one.
- ✅ **Mark inferences as inferences.** Datable facts are facts; reads are reads.
  Never present a guess as confirmed.
- ❌ **Don't invent signals, quotes, or history.** "Couldn't find much online, so
  this is built from their website alone" is a valid, honest brief.
- ❌ **Don't stall the win on slow or empty research.** Cap the effort and build
  from what you have; one good detail is enough to open well.
- ✅ **Network-dependent, keyless.** This reaches the live web, so it needs
  connectivity at runtime: keyless, but online. It is not an offline app.

## Output shape

The one-page pre-meeting brief in the fixed structure above (who they are, what
they do, recent signals, where you connect, and the three sharp questions),
written positive and outcome-led, ready to read in the minutes before the
operator walks in.
