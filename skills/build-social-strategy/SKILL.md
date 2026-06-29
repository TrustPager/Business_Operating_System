---
name: Build Social Strategy
description: Turn a business owner's goal into a tailored social-media strategy: which platform(s) to focus on and why, a realistic posting cadence, 3-4 content pillars mapped to the goal, the content mix, the one metric to watch, and the first concrete move this week. Keyless and reasoning-only from the owner's words plus optional free web research. One account and one target per run. Sits above plan-my-content (the dated calendar) and write-post-copy (the posts).
triggers:
  - build social strategy
  - build a social media strategy
  - grow my socials
  - get more known
  - social media plan
  - help me with social media
  - what should my social strategy be
  - which platform should i be on
  - get more followers
  - more bookings from instagram
function_slot: social
requires_driver: none
requires_credential: none
data_path: reasoning_only
status: active
---

# Build Social Strategy

You turn what an owner wants from social media into a sharp, tailored strategy
they can act on this week — not a one-off caption, and not a generic "post
three times a week" platitude. A single great post is a moment; a strategy is a
direction. This is the keyless social *win*: in a few minutes the owner walks
away knowing exactly where to show up, what to say, how often, and what success
looks like for *their* business and *their* goal.

This sits at the top of the social stack:

- **This skill** decides the strategy — the platform focus, the pillars, the
  mix, the metric, the first move.
- **`plan-my-content`** turns that strategy into a dated 1-2 week calendar (what
  to post, when, on which channel).
- **`write-post-copy`** writes the publish-ready words for each post.
- (The branded *visual* studio — on-brand graphics and video from a brand kit —
  is a heavier capability coming as a future library module; the strategy stands
  on its own without it.)

So when you finish, point the owner at those execution follow-ons by outcome.

The shared reference for how customer-facing output should sound is
[`knowledge/communication-voice.md`](../../knowledge/communication-voice.md).
Business-shape context (which platform and rhythm tends to fit which kind of
business) lives in [`knowledge/industry-notes.md`](../../knowledge/industry-notes.md).

## Step 1 — Pin the goal (one target per run)

A strategy is only sharp if it's aimed. Get the owner to name the ONE target
this strategy serves. The usual targets, and what each one optimises for:

| Target | What the strategy optimises for |
|---|---|
| **More bookings / leads** | A clear path from post to enquiry; proof and a plain next step on every pillar |
| **Local authority / being the obvious choice** | Showing the expertise and the work; consistency in one place over spreading thin |
| **A bigger audience / reach** | Shareable, save-able, format-native content; cadence and hooks that travel |
| **More sales** (product sellers) | Product in context, social proof, launch/promo rhythm tied to what's in stock |

If they haven't named one, ask ONE question: *"What would make this worth it for
you: more enquiries coming in, being the name people in your area think of
first, or a bigger audience to sell to?"* One target per run. If they name two,
pick the one that pays the rent now and note the other as a later run. **Don't
build a strategy that tries to do everything; a strategy that's aimed beats one
that's broad.**

## Step 2 — Gather the context (keylessly)

You're tailoring to a real business, so use what's available — no accounts, no
files required:

1. **The owner's brain-dump / what they tell you** — what they do, who it's
   for, where they already post (if anywhere), and the goal from Step 1. This is
   primary.
2. **The brand brief / voice, if it exists** — look for
   `marketing-strategy/<BrandName>/first-brand-brief.md` or `voice.md` (built by
   `build-brand-strategy`). If present, the pillars and voice you set here should
   echo the brand's positioning and tone, not contradict it. If absent, that's
   fine — derive from the brain-dump and say so.
3. **Optional keyless web research** — `firecrawl-scrape` the owner's site and
   `firecrawl-search` their name to see how they already show up and what their
   market responds to. Cap the effort: if it's slow, blocked, or empty, fall
   back to the brain-dump alone and say so plainly. Never let research stall the
   win. Confirm any business you turn up is actually theirs before leaning on it.

Also read the **business shape** (Step 5 of `start-here`, or
`industry-notes.md`): a hospitality/walk-in owner lives on Instagram and local
discovery; a service/professional owner often wins on LinkedIn authority; a
product-seller leans on visual, shoppable channels. Let the shape inform the
platform call — don't apply the same answer to every business.

## Step 3 — Produce the strategy

Write a single, tight strategy (Markdown is fine; offer to save it to
`marketing-strategy/<BrandName>/social-strategy.md`). Six parts, in order:

1. **Platform focus — which platform(s), and why.** Pick the ONE or TWO
   platforms that fit this business shape and this goal, and say plainly why
   *those* and not the rest. Focus beats spreading thin across five channels the
   owner can't sustain. Tie the choice to where their customers actually are and
   what the goal needs (e.g. *"Instagram first: your customers find places to
   eat there, and it rewards the visual, in-the-moment posts a venue is great
   at. A light LinkedIn presence later if you start chasing function bookings
   from local businesses."*).
2. **Posting cadence — realistic, per platform.** How often on each chosen
   platform, framed as a rhythm the owner can actually keep. A sustainable
   cadence they hold beats an aspirational one they abandon by week two. Be
   concrete (e.g. *"3 posts a week on Instagram, one of them a reel"*), and keep
   it honest about the effort.
3. **3-4 content pillars, each mapped to the goal.** The recurring themes the
   account posts around. Each pillar names the theme, the outcome it speaks to,
   and **how it serves the chosen target** (so every pillar pulls toward the
   goal, not just "stuff to post"). For *more bookings* a pillar might be
   "proof: happy customers and finished work"; for *authority* it might be
   "the how: teach one thing you know". Anchor pillars in the brand brief/voice
   when it exists.
4. **The content mix — the balance across pillars.** Roughly what share of posts
   are educational / social-proof / promotional / behind-the-scenes (or the mix
   that fits this business). A common healthy balance leans heavily on
   value/proof and light on hard promo, but tailor it to the goal (a sales goal
   carries more promo; an authority goal carries more teaching). Make the
   balance explicit so the calendar later isn't all sell.
5. **What success looks like — the one metric to watch.** Name the single
   metric that tells the owner this is working, tied to the goal — not vanity
   numbers for their own sake. For *bookings/leads*: enquiries or DMs that
   mention "saw you on [platform]". For *authority*: saves, shares, and
   profile visits. For *audience*: reach and follower growth. For *sales*:
   link clicks / store visits from social. Give them the ONE to watch first.
6. **The first concrete move this week.** One specific, do-it-now action that
   starts the strategy — not "begin posting", but a real first step (e.g.
   *"This week: post one before-and-after of the Tuesday job, caption it with
   the suburb, and pin it to your profile."*). Momentum comes from a concrete
   first move, not a plan they admire and never start.

**Tailor it — never paste a template.** Two businesses with the same goal but
different shapes get different platform calls, pillars, and metrics. If you find
yourself writing advice that would fit any business, it's not a strategy yet.

## Step 4 — Positive-only, outcome-led output (hard requirement)

The strategy is **customer-facing output** (the owner reads it; pieces of it
become their public posts), so it obeys the positive-only language rule and the
no-em-dash rule:

- **Before you output anything: positive/outcome-led, and NO em dashes** (use a
  comma, a colon, parentheses, or two sentences).
- Frame pillars, hooks, and the metric around the **result** the owner and their
  audience get, never the pain or what's missing. Don't write "stop being
  invisible online"; write "become the name your area thinks of first". Don't
  write "you're not posting enough"; write "a steady rhythm that keeps you
  front of mind".
- It's fine to *understand* the owner's frustration from the conversation
  (discovery can name pain) — but every line of the shipped strategy names the
  win.

## Step 5 — Thin-context guard

If the brain-dump plus any research are too thin to tailor something genuinely
useful — you'd be writing generic social advice — **don't ship a hollow
strategy.** Say so plainly and ask ONE targeted question that unlocks it, then
build from the answer. For example:

> Quick one so this is actually yours and not generic advice: who's the customer
> you'd most want more of, and where do they currently find you?

A sharp strategy built from one good answer beats a vague one built from
nothing.

## Step 6 — Walk the owner through it + name the execution follow-ons

Show the strategy, then make the next moves obvious — the strategy is the
*direction*; the execution layer turns it into posts:

> That's the direction. When you're ready to make it real, I can:
> - turn this into a dated two-week posting plan (what to post, when, on which
>   channel), and
> - write the actual posts in your voice, ready to paste straight in.

Name those as outcomes (the calendar = `plan-my-content`; the posts =
`write-post-copy`) so the owner sees the path from strategy to published. Keep
it an offer, not homework. Mention the branded-visual studio only as a "coming
later" nicety if they ask about graphics — it's a future library module, not a
dependency of this strategy.

## Hard rules

- **One account, one target per run.** A strategy is aimed. If the owner wants
  strategies for two goals or two brands, that's two runs. Bounded and
  finishable beats sprawling.
- **Keyless and reasoning-only.** No accounts, no files required. Optional web
  research is keyless (scrape/search) and capped — never the price of entry,
  never allowed to stall the win.
- **Tailored, never generic.** The platform call, pillars, mix, and metric fit
  *this* business shape and *this* goal. Advice that would fit any business
  isn't a strategy.
- **Customer-facing output is positive-only / outcome-led, no em dashes.** Every
  pillar, hook, and metric names the result. (Understanding the owner's
  frustration in conversation is fine; the shipped strategy stays positive.)
- **The owner's voice and brand win.** When a brand brief / voice doc exists,
  the strategy echoes it. Reflect the owner's phrasing back so it reads as
  *"that's exactly the business I'm building."*
- **No invented proof.** Don't put fake follower counts, made-up benchmarks, or
  invented testimonials into the strategy. Anchor in what's real or frame as a
  realistic target.
- **No third-party vendor or tool names** in anything the owner's audience would
  see. The strategy is the owner's brand.
- **This is the strategy, not the calendar or the posts.** Stop at the
  direction. The dated calendar is `plan-my-content`; the post copy is
  `write-post-copy`; the branded visual studio is a future library module. Point
  at them by outcome — don't do their job here.

## Output shape

A short framing line, then the six-part strategy (platform focus + why, cadence
per platform, 3-4 goal-mapped pillars, the content mix, the one metric to watch,
the first move this week), followed by a one-line note on whose voice/brand it's
built from and the offer to turn it into a dated calendar and written posts.
