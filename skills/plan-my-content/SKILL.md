---
name: Plan My Content
description: Turn your content pillars and voice into a dated, ready-to-post content calendar for the next 1-2 weeks. Reads content-pillars.yaml and voice.md when they exist, or derives working pillars from a short brief so you're never blocked. Every slot names the date, channel, pillar, ring, hook, and format. Bounded to a 1-2 week horizon, never a 90-day firehose.
triggers:
  - plan my content
  - build a content calendar
  - what should I post this week
  - content plan for the next two weeks
  - turn my pillars into posts
  - schedule my social posts
  - give me a posting calendar
  - map out my content
  - weekly content plan
function_slot: social
requires_driver: none
requires_credential: none
data_path: reasoning_only
status: active
produces_customer_facing_copy: true
engagement_copy: true
---

# Plan My Content

You turn what a brand stands for into what it posts this week. The hard part
of content is never "what could we say" — it's "what do I post, where, and
when." This is the bridge: pillars and voice in, a dated calendar out, so the
owner opens it and knows exactly what to publish on each day.

This is the calendar layer the strategy method has been missing.
[`knowledge/marketing-strategy-method.md`](../../knowledge/marketing-strategy-method.md)
runs Layer 3 (the brand strategy docs) down to `content-pillars.yaml`, then
jumps to Layer 4 (live nurture email in a connected auto queue). This skill
fills the gap in between: it takes the pillars and turns them into a dated,
multi-channel posting plan you can act on by hand today — no accounts, no
queue, no connection required. (The auto-queue and CRM scheduling layers of
that method are the connected-tier upgrade, NOT a dependency of this calendar.)

Why a calendar held to one avatar out-reaches a scattered one, and the levers that
drive engagement, live in
[`knowledge/distribution-method.md`](../../knowledge/distribution-method.md).

## Step 1 — Find the brand's pillars and voice

Look for the strategy artifacts the owner already has, in this order:

1. **`content-pillars.yaml`** — usually under `marketing-strategy/<BrandName>/`,
   produced by `build-brand-strategy`. This is the spine of the plan: each
   pillar becomes a recurring thread in the calendar. Read every pillar's
   `name`, `pain_addressed`, `default_channel`, `cadence`, and
   `example_topics`.
2. **`voice.md`** — same folder. Read it so every hook you draft sounds like
   the owner, not like generic agency copy. The founder's voice IS the brand.
3. **`positioning.md` / `value-props.yaml`** — read if present, for the promise,
   the transformation, the point of view, and the outcomes to lean on in hooks.
   Optional, not required.

If those files exist, build straight from them — don't re-interview the owner
for things the pillars already answer.

## Step 2 — If there are no pillars yet, derive working ones (don't block)

A brand-new owner may not have run `build-brand-strategy` yet. Do NOT stop and
demand the file. Instead, ask for a short brief and derive 3-4 working pillars
on the spot, so the calendar still lands today:

> Quick one before I map out your two weeks: what are the 3 or 4 things you'd
> most want to be known for, and which channels do you actually post on?

From their answer, sketch 3-4 lightweight pillars (a name + the outcome each
one speaks to) and tell the owner plainly that these are working pillars you
derived from the brief, sharpened later by `build-brand-strategy`. A real plan
from a good brief beats a blank page waiting on a file.

## Step 3 — Confirm the calendar shape

Lock four things before you draft a single slot:

1. **Horizon — 1 or 2 weeks.** Default to 2 weeks. This is a hard ceiling:
   never plan past 14 days. A bounded plan gets acted on; a 90-day firehose
   gets ignored.
2. **Start date.** Default to the next Monday (or today if the owner wants to
   start now). Every slot carries a real calendar date.
3. **Channels.** Use the `default_channel` values from the pillars; confirm the
   final set with the owner (e.g. Instagram, LinkedIn, a weekly email).
4. **Cadence per channel.** How many posts a week on each channel. Honour each
   pillar's `cadence` where it's set. Keep it realistic — a plan the owner can
   actually sustain beats an aspirational one they abandon by Wednesday.

## Step 4 — Build the dated calendar

**Shape guard (check FIRST).** Read the profile's business shape: prefer an
explicit `Business shape:` line in `## How the business is running` (start-here
records it, with any regulated override spelled out) and fall back to inferring
it from the `## My business` context in the workspace `CLAUDE.md`. Treat the
business as regulated if that line carries a `Regulated:` clause, or (when
inferring) the business is a regulated one (clinic / appointment, or the
finance / mortgage broking, insurance, or legal verticals). For a regulated
business, do NOT plan before/after, outcome-testimonial, or urgency / countdown
slots for owned channels. Route those slots to compliant angles instead: service-level
proof (response time, we-handle-everything), the experience, the process, and
education. The per-shape overrides live in `knowledge/industry-notes.md` (the
Clinic / appointment and Service / professional shapes) and
`knowledge/business-method.md` §7.2 and §15, pointed to from
`knowledge/content-rules.md` §4. For all other shapes, run the full format mix.

Spread the pillars across the dates so the mix is balanced (no channel goes
three posts deep on one pillar while another pillar never appears). When a
pillar recurs, vary the FORMAT, not the theme: the same proof pillar can
appear as a before/after, a customer story, and a one-tip carousel
(business-method.md §4.4). (The before/after and outcome-testimonial formats are
disallowed for regulated shapes per the shape guard above — use service-level or
process proof there instead.)

**Search-intent lens (bias topic choice toward what people actually search).**
Where a pillar can be aimed at a real search, prefer topics close to buying
("cost to rewire a house", "emergency [trade] [suburb]") over broad awareness
ones, and favour topics the owner can win (see `knowledge/seo-method.md`). If the
owner has run `get-found-online`, use the winnability read it produced to steer
topic choice. **This skill is reasoning-only: do not run a web search yourself**
— reason from the pillars, the owner's terms, or a spot-check they bring;
`get-found-online` is where live SERP reads happen.

**Hold the calendar to one avatar** (`knowledge/distribution-method.md`): posting for
the same audience across the two weeks is what lets each platform learn who to show the
account to, so vary the format freely but resist scattering across different audiences.
Where a slot's job is engagement, the comment-driving levers (a clear stance, a genuine
question, real emotion) live in that same file.

**Spread the batch across the audience rings — 3/1/1** (the audience bullseye in that
same file). Holding one avatar does not mean every post aims at the dead centre. Across a
batch of five, aim three at the centre (the exact viewer), one a ring wider, one two rings
wider, so the calendar builds conversion and reach at once. This is a *separate axis* from
the pillar/content-type: note the ring alongside each slot's pillar (for example
"proof × centre" or "teach × Ring 2"), so the two compose rather than compete.

For EVERY slot, fill all six fields:

- **Date** — the real calendar date (and weekday).
- **Channel** — where it posts.
- **Pillar** — which content pillar this slot serves (ties every post back to
  strategy, so the plan is never random).
- **Ring** — which bullseye ring this slot targets (centre / Ring 1 / Ring 2),
  so the batch holds the 3/1/1 audience spread. This composes with the pillar,
  it does not replace it (e.g. "proof × centre").
- **Hook / angle** — the specific opening line or idea for THIS
  post, written in the brand's voice. Not a vague topic ("talk about speed") —
  an actual angle the owner could open with. Draft each one against the hook craft
  in [`knowledge/storytelling-method.md`](../../knowledge/storytelling-method.md)
  (the three-step formula, and the six power words as the scoring gate), so a slot
  hands over a hook that can actually open a post rather than a topic label.
- **Format** — what kind of post it is (e.g. carousel, single image, short
  video, customer story, tip, behind-the-scenes, plain-text post, weekly
  email).

Present it as a clean dated table the owner can read top to bottom, grouped by
week. Keep hooks tight — one line each. This is a plan, not the finished copy.

## Step 5 — Hand it over + offer the next step

Show the calendar, then:

- Point out how the pillars are balanced across the two weeks (so they see
  every theme gets airtime).
- Frame the two weeks as one slice of a longer consistent run: results are
  judged over the sustained run, not at day 14 (business-method.md §10.2,
  directional).
- Flag any slot you left open for them to choose (e.g. "Thursday's customer
  story needs a real client — which one?").
- Offer the natural next move: *"Want me to turn any of these hooks into a
  finished, rendered post? That's the `make-social-post` skill."*

## Hard rules

- **Horizon is clamped to 1-2 weeks. Never plan past 14 days.** Bounded and
  token-frugal beats a sprawling quarter no one follows.
- **Every slot names all six fields** — date, channel, pillar, ring, hook, format.
  A slot missing its pillar is a random post, not a planned one; a slot missing
  its ring drops the audience spread the batch is built on.
- **Built on the brand's real pillars and voice.** When `content-pillars.yaml`
  and `voice.md` exist, use them. When they don't, derive working pillars from
  a brief and say so — never invent a strategy and present it as the owner's.
- **Content guardrails.** Customer-facing copy uses no em dashes, invents no
  facts, quotes, or numbers, and names no third-party vendor. Write it in the
  owner's brand voice; the framing and marketing psychology are the owner's
  choice. The rules are in `knowledge/content-rules.md`.
- **Regulated shapes have extra limits.** For a clinic / appointment or finance
  shape (and insurance / legal), never plan before/after, outcome-testimonial,
  or urgency / countdown slots for owned channels. Route them to service-level
  proof, the experience, the process, and education (`content-rules.md` §4,
  which points to `industry-notes.md` and `business-method.md` §7.2 / §15).
- **One idea per slot.** Each post is a single hook. If a slot is carrying two
  angles, split it into two slots (or two weeks).
- **Don't over-plan the cadence.** A sustainable rhythm the owner keeps beats a
  punishing one they drop. Match the pillars' cadence, then sanity-check it's
  realistic.
- **This is a plan, not the posts.** Hooks are one line. Rendering finished
  graphics is `make-social-post`; this skill stops at the dated calendar.

## Output shape

A short framing line, then a dated calendar table grouped by week — every row
carrying date (with weekday), channel, pillar, hook, and format — followed by a
one-line note on how the pillars are balanced and the offer to render any hook
into a finished post.
