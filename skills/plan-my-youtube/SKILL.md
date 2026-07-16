---
name: Plan My YouTube
description: Turn your channel research into a real plan: a clear channel strategy and a pipeline of videos, each with an idea, an angle, a working title, and a thumbnail concept ready to script. Builds on your social strategy and content plan so it all fits together. No accounts needed.
triggers:
  - plan my youtube
  - plan my channel
  - plan my youtube videos
  - build my youtube strategy
  - what should my channel be about
function_slot: strategy
requires_driver: none
requires_credential: none
data_path: reasoning_only
status: active
produces_customer_facing_copy: true
---

# Plan My YouTube

You turn channel research into a plan the owner can act on: a clear channel
strategy and a dated, ordered pipeline of videos, each one carrying the four
packaging fields that the rest of the factory reads. This is the bridge between
"I looked at my niche" and "I know exactly what to film next." Nothing here needs
an account.

This skill **composes**, it does not re-invent. YouTube is a social channel, so
the strategy craft already lives in two skills you delegate to:

- **[`build-social-strategy`](../build-social-strategy/SKILL.md)** owns the
  strategy layer: the platform focus and why, the cadence, the content pillars
  mapped to the goal, the content mix, the one metric to watch, and the first
  move this week. You run that thinking here **for YouTube specifically**, using
  its method. You do not restate or fork its logic.
- **[`plan-my-content`](../plan-my-content/SKILL.md)** owns the pipeline layer:
  turning pillars into a dated, ordered list of what to make. You run that
  thinking here to lay out the video pipeline. Again by reference, not copied.

Think of this skill as those two, aimed at one channel, with a YouTube-shaped
output: a strategy plus a video pipeline where every row is packaged and
ready to hand to `script-my-video`.

The packaging craft this plan leans on (outlier analysis, angle and title and
thumbnail differentiation, franchise thinking) lives in
[`knowledge/youtube-packaging-method.md`](../../knowledge/youtube-packaging-method.md).
Read it before you package the pipeline so the method has one home and this body
stays lean. Why a channel holds one avatar and one topic band (audience matching), and
why you don't cross-post a video's link from a faster platform, live in
[`knowledge/distribution-method.md`](../../knowledge/distribution-method.md) — the
strategy step leans on it.

It runs on reasoning and the owner's own words alone. Work the gates in order.
Only fall back to defaults where a gate says so.

## Step 1: Read the ground silently

Before asking anything, read what is already on the machine so the plan is in the
owner's voice and grounded in their business and their research:

- **`brand/brand.json`:** the business name, the voice, the tagline. Everything
  owner-facing in the plan (titles, angles, the channel positioning) uses this
  voice.
- **`./CLAUDE.md`:** the business shape, the offer, and the region **only if** a
  `Region:` line is explicitly set (that `Region:` line is the country-level
  signal the rest of the factory keys on, and it is never inferred).
- **A service town or suburb, if one is already known:** a location or
  service-area field in `brand/brand.json` when the brand carries one, or a place
  the owner has stated in `./CLAUDE.md`. This is the local packaging locale, a
  separate thing from the country-level `Region:` line, and it is what a local
  channel's strongest angle is built on. If none is on the machine, note it as
  not-yet-known and let Step 2 decide whether to ask. Never invent a town the
  owner has not given you.
- **If present, `youtube-research.md`** (from `research-my-channel`): this is the
  primary input when it exists. It carries the competitor content scan, the
  comment-mined ideas with their verbatim evidence, and the novel-packaging
  gap-and-angle map. The video pipeline draws its ideas and angles straight from
  here, so every video traces back to real observed demand.
- **If present, existing brand strategy artifacts** under
  `marketing-strategy/<BrandName>/` (`content-pillars.yaml`, `voice.md`,
  `social-strategy.md`): when they exist, the channel strategy should echo them,
  not contradict them.

If `youtube-research.md` is absent, you can still build the plan from what the
owner tells you in Step 2, but say plainly that running `research-my-channel`
first would ground the pipeline in real audience demand rather than guesses.

## Step 2: Confirm the goal and gather thin context

A channel is only worth planning if it is aimed. Confirm the ONE thing the
channel is for, the same way `build-social-strategy` pins a single target: more
enquiries and bookings, being the obvious local authority, a bigger audience, or
more product sales. One target per run.

If the research artifact and the owner's words together are too thin to plan
something genuinely theirs, ask ONE targeted question that unlocks it (who the
channel is for and what one action a viewer should take), then build from the
answer. A sharp plan from one good answer beats a generic one from nothing.

**Ask for the service town up front when the local angle is the play (here, not
after the plan is written).** For a local-service business the local-town angle is
usually the single strongest packaging play: the big generic channels in the niche
can't be local for you, so "[trade] for [Town]" is a lane a new channel can own
from zero (this is the untaken-angle move in `youtube-packaging-method.md`). When
that is the play and no town is known from Step 1, ask one short question before
you build, so the first row can carry the local angle while the owner is most
engaged, instead of landing as a half-formed slot after the plan is written:

> Quick one so I can package your strongest angle: what town or area do you serve?
> Putting your town front and centre is a lane you can own from day one, so it is
> often a local channel's best first move.

The owner naming their town is not inferring a region, it is the sanctioned way to
learn it, the same way `get-found-online` works from "[service] [suburb]." Keep it
to one light question (fold it in with confirming the goal so the owner is not
peppered), and never put a place in their mouth. If they would rather not say,
carry on and leave the local angle as an open slot they can fill later (Step 5).
Skip this ask entirely when the channel is not local (a national product, a
software channel): there is no town to own.

## Step 3: Set the channel strategy (delegate to `build-social-strategy`)

Run the `build-social-strategy` method for this one channel. Do not copy its
prose or re-derive its framework here: apply it, aimed at YouTube. Keep the pillars
tight to one avatar: a channel that holds one audience and one topic band is what lets
the algorithm learn who to push to (audience matching, `knowledge/distribution-method.md`),
so resist spreading the channel across audiences even when an off-avatar idea looks
tempting. The channel strategy names, tailored to this owner and this goal:

- **What the channel is about** and why it fits this business, in the owner's
  voice (the YouTube read of the platform-focus and current-state parts of the
  method).
- **A realistic upload cadence** the owner can actually hold (the cadence part),
  honest about the effort a video takes versus a social post.
- **3-4 content pillars mapped to the goal** (the pillars part). These become the
  recurring threads the video pipeline is built around, so every video serves a
  pillar rather than being a random idea.
- **The content mix** across those pillars (teach, proof, story, the occasional
  promo), tuned to the goal.
- **The one metric to watch** first, tied to the goal, not vanity numbers.

Under that one held avatar, use the **ring ladder** to choose topics
(`knowledge/distribution-method.md`, the audience bullseye): the channel's centre is the
exact viewer, and the rings out are progressively broader topic bands. Bias the pipeline
to the centre and Ring 1 for topics (that is where conversion and algorithm confidence
come from), and reach for Ring 2 topics only to widen. This composes with the virality
formula already used below: a centre topic with a fresh lens, validated against a real
outlier, is the strongest row you can plan.

If `build-social-strategy` has already produced a `social-strategy.md` that
covers YouTube, build on it rather than re-running the whole thing: lift the
pillars and the metric, and only add what is YouTube-specific.

## Step 4: Build the video pipeline (delegate to `plan-my-content`)

Run the `plan-my-content` method to turn the pillars from Step 3 into a dated,
ordered pipeline of videos. Again, apply the method, do not restate it: spread
the pillars so the mix is balanced, vary the format within a pillar rather than
repeating the theme, and carry a real calendar date on each row so the pipeline
is ordered, not a loose wish-list. Keep the horizon bounded the way
`plan-my-content` does: a pipeline the owner can actually make beats a
year-long firehose they never start.

Draw the ideas straight from `youtube-research.md` where it exists: the
comment-mined questions, the "nobody explains X" gaps, and the untaken angles are
your best pipeline rows because they trace back to real audience demand.

## Step 5: Package every video (the four fields)

This is what makes it a YouTube plan and not a generic calendar. Every row in the
pipeline carries the **four packaging fields**, packaged per
`knowledge/youtube-packaging-method.md`. These are the exact seeds that
`script-my-video`'s `packaging` block and `make-thumbnail` both read, so name
them the same way:

1. **Idea** — what the video is about, in one line. Where it came from research,
   note the demand it answers so the owner sees why it earns a slot.
2. **Angle** — the differentiated take. Not the topic everyone covers, but the
   specific angle that stands out, drawn from the untaken-angles map in the
   research. This is the packaging craft's core move: differentiate, do not
   duplicate. For a local-service channel the local-town angle is often the
   strongest row here: when the owner gave you their town in Step 2, name it in
   the angle and the working title (the "[Trade] for [Town] Homeowners" shape from
   `youtube-packaging-method.md`). When they chose not to share it, leave that
   row's local angle as a clearly marked open slot ("[your town] here") the owner
   can drop their town into later, never a place you made up.
3. **Working title** — a strong candidate title in the owner's brand voice. This
   seeds `script-my-video`'s `working_title` and `packaging.title_options`.
4. **Thumbnail concept** — the visual idea for the thumbnail, in one line. This
   seeds both `packaging.thumbnail_concept` in the script and the concept
   `make-thumbnail` renders.

Present the pipeline as a clean, dated, ordered table: each row an idea, its
angle, its working title, and its thumbnail concept, tied back to the pillar it
serves. That table is the handoff: an owner picks any row and runs
`script-my-video` on it.

## Step 6: Hand it over + name the next step

Show the strategy and the packaged pipeline, then make the next move obvious:

> That is your channel and your first run of videos, each one packaged and ready.
> When you want to make one real, pick a row and I will script it beat by beat.

Point at the execution follow-on by outcome: scripting a picked row is
`script-my-video`, which reads the four packaging fields straight from this plan.
Keep it an offer, not homework.

## Hard rules

- ❌ **Keyless. No accounts, no MCP tools.** This skill reads local files and the
  owner's words only. It names no connected tool.
- ✅ **Compose, never fork.** The strategy craft is `build-social-strategy`'s and
  the pipeline craft is `plan-my-content`'s. Delegate to them by reference and
  apply their methods to YouTube. Do not copy, paste, or re-derive their bodies
  here. If you find yourself writing out the six-part strategy framework or the
  five-field calendar rules from scratch, stop and reference the owning skill.
- ✅ **Every pipeline video carries all four packaging fields** (idea, angle,
  working title, thumbnail concept), named so `script-my-video` and
  `make-thumbnail` read them directly.
- ✅ **Grounded in real research where it exists.** When `youtube-research.md` is
  present, pipeline ideas and angles trace back to its observed demand and its
  verbatim evidence. Never invent audience demand, competitor outliers, or
  results to fill a row.
- ✅ **Never invent a place, but do ask for one.** Read the region and the service
  town from the machine, or ask the owner for their town when the local angle is
  the play: both are fine. Making up a town, suburb, or region the owner never
  gave you is not. On a decline, the local angle stays a clearly marked open slot,
  never a guess.
- ✅ **One channel, one goal per run.** A plan is aimed. Two goals or two brands
  is two runs.
- ✅ **Content guardrails.** Customer-facing copy uses no em dashes, invents no
  facts, quotes, or numbers, and names no third-party vendor. Write it in the
  owner's brand voice; the framing and the marketing psychology are the owner's
  choice. The rules are in `knowledge/content-rules.md`.
- ✅ **This is the plan, not the scripts.** Stop at the strategy and the packaged
  pipeline. Beat-by-beat scripting is `script-my-video`; the rendered thumbnail
  is `make-thumbnail`. Point at them by outcome, do not do their job here.

## Output shape

A short framing line, then the channel strategy (platform-focus for YouTube,
cadence, 3-4 goal-mapped pillars, the content mix, the one metric), followed by a
dated, ordered video pipeline table where every row carries an idea, an angle, a
working title, and a thumbnail concept tied to its pillar, and a closing line
naming whose voice and research the plan is built from plus the offer to script
any row.
