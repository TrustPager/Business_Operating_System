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
data_path: local
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
strategy step leans on it. Which ideas earn a slot at all (the branch tree), what
effort a video is worth, and how the first run is shaped live in
[`knowledge/youtube-launch-method.md`](../../knowledge/youtube-launch-method.md).

It runs on reasoning and the owner's own words alone. Work the gates in order.
Only fall back to defaults where a gate says so.

## Step 1: Read the ground silently

Before asking anything, read what is already on the machine so the plan is in the
owner's voice and grounded in their business and their research:

- **`brand/brand.json`:** identity only, the business name and the tagline. The
  voice everything owner-facing in the plan is written in (titles, angles, the
  channel positioning) is `marketing-strategy/<BrandName>/voice.md`; when no voice
  doc exists, say so plainly and write from the owner's own words rather than
  inventing a voice for them (`knowledge/content-rules.md`).
- **`./CLAUDE.md`:** the business shape, the offer, who they sell to (`## My
  business` and `## My ideal customer`, which Step 3 uses), and the region **only
  if** a `Region:` line is explicitly set (that `Region:` line is the country-level
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
  demand-signal ideas with their verbatim evidence (comment-mined when `yt-dlp`
  was on the machine, search-and-discussion-mined otherwise), and the novel-packaging
  gap-and-angle map, plus a ranked cross-channel outlier board when the owner took
  that deepener (its branch labels are provisional working themes, so the pillars
  Step 4 sets are what a row is actually filtered against in Step 5). The video
  pipeline draws its ideas and angles straight from here, so every video traces
  back to real observed demand.
- **If present, existing brand strategy artifacts** under
  `marketing-strategy/<BrandName>/` (`content-pillars.yaml`, `voice.md`,
  `social-strategy.md`, and the positioning file, `first-brand-brief.md` or
  `positioning.md`): when they exist, the channel strategy should echo them, not
  contradict them. The positioning file is where the transformation and the point
  of view live, and reading it is what lets Step 3 skip the interview instead of
  asking an owner something they have already answered. If both positioning files
  exist, `positioning.md` wins (it is the evidence-anchored one) and the brief is
  the older draft.

If `youtube-research.md` is absent, you can still build the plan from what the
owner tells you in Step 2, but say plainly that running `research-my-channel`
first would ground the pipeline in real audience demand rather than guesses.

## Step 2: Confirm the goal and gather thin context

A channel is only worth planning if it is aimed. Confirm the ONE thing the
channel is for, the same way `build-social-strategy` pins a single target: more
enquiries and bookings, being the obvious local authority, a bigger audience, or
more product sales. One target per run.

If the research artifact and the owner's words together are too thin to plan
something genuinely theirs, ask ONE targeted question that unlocks it (what one
action a viewer should take; who the channel is for belongs to Step 3's
transformation ask and is never asked twice), then build from the answer. A sharp
plan from one good answer beats a generic one from nothing.

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
to one light question (fold it in with confirming the goal), and never put a place
in their mouth. If they would rather not say,
carry on and leave the local angle as an open slot they can fill later (Step 6).
Skip this ask entirely when the channel is not local (a national product, a
software channel): there is no town to own.

Step 3's gate may also need an ask. Its transformation question **replaces** the
who-is-this-for half above rather than joining it; fold whatever is left into the
same message.

## Step 3: The transformation and point-of-view gate

A channel that argues nothing is a channel with no angle to package. **Two brand
fields** have to be pinned before you set a strategy: **the transformation**, and
**the point of view**, which is one field carrying two labelled lines
(`**The belief:**` and `**What it argues against:**`). Step 4's pillars sit on
them, and Step 6's angle field has no contrarian take to reach for without them
(that take is exactly what the click-confirmation beat in
`knowledge/youtube-packaging-method.md` asks the script to open on, and nothing
else in the pack supplies it).

**These are brand fields, not YouTube fields.** They live beside `voice.md` in the
brand strategy home, `marketing-strategy/<BrandName>/`, inside the positioning
file. `build-brand-strategy` owns them, and
[`knowledge/marketing-strategy-method.md`](../../knowledge/marketing-strategy-method.md)
(Layer 3, `positioning.md`) defines both fields, their exact shape and headings,
and the pass/fail test each one has to meet. **Read it before you judge a field: a
field that fails its test counts as missing here.** Resolve the brand folder the
way the rest of the pack does: the directory under `marketing-strategy/`, or the
name in `brand/brand.json`, and confirm the path before writing anything.

The stance can be a disagreement or a surprising-but-positive claim. The mechanic
is that it provokes a reaction, and how sharp it is, is the owner's call
(`knowledge/distribution-method.md`, the framing flag).

Run the asking itself by
[`knowledge/conversation-method.md`](../../knowledge/conversation-method.md): the
specific give before the ask, the field-by-field sharpen pass before anything is
written, and its stuck exit when an owner cannot get there. Labelled divergence:
this gate deliberately stacks its two questions into one message rather than
spreading them over turns, so lead hard with what you already know about their
business.

**The profile counts as an answer too.** `## My ideal customer`, or the `## My
business` line in `./CLAUDE.md`, already names who this is for on the common
`start-here` path. Where it does, that satisfies the transformation's audience
half: say it back and ask only for the from-state and the to-state. Never re-ask
an owner who the channel is for when the profile answers it.

Then take the branch that matches what is already answered.

- **Answered → skip, ask nothing.** Say the fields back in one line as the frame
  for the run ("so this channel argues X, for Y going from A to B") and build
  straight from them. An owner is never re-interviewed on a field that passes its
  test.
- **Half answered → top up the missing field only.** One question, for that field
  alone, then write back that field alone. Never clobber a hand-tuned file: append
  and show the owner a short before/after, the same discipline `build-my-voice`
  follows when it touches a file it did not write.
- **Nothing is there → capture, then continue.** Ask inline, folded in with Step
  2's ask:

  > Two quick ones so the channel argues something: who exactly is this for, and
  > what is different for them afterwards? And what does your industry get wrong
  > that you would happily argue about?

  The second answer usually carries the belief and what it argues against
  together; when it carries only the belief, name the other half back in their
  words and let them correct it rather than deciding it yourself. Then write both
  fields, under Layer 3's headings, into `first-brand-brief.md` in the brand home
  (the day-one default; create it if there is none, and if a positioning file is
  already there, write into that one and preserve every field it already carries).
  Tell the owner where they went, and **if a profile exists**, leave one dated
  pointer line in it so a later session finds them:
  `Positioning captured (<date>): <the transformation in one line>, see <path>`,
  appended under `## How the business is running` with the same append-and-update
  discipline `build-my-voice` uses for a locked voice. On a cold workspace there is
  no `./CLAUDE.md` to append to (this skill can run before `start-here` ever has):
  skip the pointer, say in one line that the fields live in the brand home and a
  profile will pick them up later, and never create a profile just to hold a
  pointer. This is a two-field capture, not brand strategy: point at
  `build-brand-strategy` for the full brief and carry on with the channel plan.
- **They would rather not → carry on with the slots open.** Mark both clearly open
  the way a declined town is, and plan without them. Never fill an open slot with a
  belief you wrote.

**Shape guard.** Run `build-social-strategy`'s regulated-shape check (its
current-state read) before you accept a point of view. For a clinic, a broker, or
another regulated shape, the belief cannot become an outcome or result argument;
route it to the process, the care, and the logistics instead
(`knowledge/content-rules.md` §4).

## Step 4: Set the channel strategy (delegate to `build-social-strategy`)

Run the `build-social-strategy` method for this one channel, aimed at YouTube. It
owns the strategy's shape and every count in it; produce its outputs, do not
restate its framework here. What is genuinely YouTube-specific, and therefore
this skill's to add:

- **One avatar, held.** A channel that holds one audience and one topic band is
  what lets the algorithm learn who to push it to (audience matching,
  `knowledge/distribution-method.md`), so resist spreading across audiences even
  when an off-avatar idea looks tempting.
- **Cadence is costed as video, not as posts.** What that effort actually is, and
  how it differs between a filmed video and a rendered one, is the effort pyramid
  in `knowledge/youtube-launch-method.md` §2.
- **The pillars answer to Step 3.** Each one serves the transformation, and at
  least one carries the point of view. They become the branches the pipeline hangs
  off, so every video serves a pillar rather than being a random idea.
- **The metric is a channel metric**, tied to the goal, never a vanity number.

Under that one held avatar, use the **ring ladder** to choose topics
(`knowledge/distribution-method.md`, the audience bullseye): the channel's centre is the
exact viewer, which is the Step 3 transformation's audience rather than a fresh
decision, and the rings out are progressively broader topic bands. Bias the pipeline
to the centre and Ring 1 for topics (that is where conversion and algorithm confidence
come from), and reach for Ring 2 topics only to widen. This composes with the virality
formula already used below: a centre topic with a fresh lens, validated against a real
outlier, is the strongest row you can plan.

If `build-social-strategy` has already produced a `social-strategy.md` that
covers YouTube, build on it rather than re-running the whole thing: lift the
pillars and the metric, and only add what is YouTube-specific.

## Step 5: Build the video pipeline (delegate to `plan-my-content`)

Run the `plan-my-content` method to turn the pillars from Step 4 into a dated,
ordered pipeline of videos. It owns the calendar's rules and its bounded horizon;
apply them rather than restating them. The one thing to hold onto here: a pipeline
the owner can actually make beats a year-long firehose they never start.

**Commit to the run, date only the fortnight.** The first run is about twenty
videos; dated rows stay inside `plan-my-content`'s 1-2 week ceiling and get re-run
(`knowledge/youtube-launch-method.md` §3, which also owns the branch filter every
row has to pass).

Draw the ideas straight from `youtube-research.md` where it exists: the
demand-signal questions (comments where `yt-dlp` reached them, search and public
discussion otherwise), the "nobody explains X" gaps, and the untaken angles are
your best pipeline rows because they trace back to real audience demand.

## Step 6: Package every video (the four fields)

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
   duplicate. Where a row's angle is the contrarian one, it is the Step 3 point of
   view, in the owner's words, never an opinion you supplied. For a local-service
   channel the local-town angle is often the
   strongest row here: when the owner gave you their town in Step 2, name it in
   the angle and the working title (the "[Trade] for [Town] Homeowners" shape from
   `youtube-packaging-method.md`). When they chose not to share it, leave that
   row's local angle as a clearly marked open slot ("[your town] here") the owner
   can drop their town into later, never a place you made up.
3. **Working title** — a strong candidate title in the owner's brand voice. This
   seeds `script-my-video`'s `working_title` and `packaging.title_options`.
   **On a how-to or evergreen row, the title leads with the words viewers actually
   type.** Read the search-demand clusters from `youtube-research.md` (written by
   `research-my-channel`) and lead the title with the strongest on-topic cluster,
   keeping the owner's own outcome framing for the hook and the description when
   the outcome phrase has thin demand behind it. The method and the when-to-skip
   rule are the findability check in `knowledge/youtube-packaging-method.md`. On a
   browse or story row, intrigue out-pulls search-match: skip the demand lead and
   say so. When no research file exists, write the title from the owner's words and
   name the unverified findability in one line, rather than implying a demand read
   you did not do.
4. **Thumbnail concept** — the visual idea for the thumbnail, in one line. This
   seeds both `packaging.thumbnail_concept` in the script and the concept
   `make-thumbnail` renders.

Present the pipeline as a clean, dated, ordered table: each row an idea, its
angle, its working title, and its thumbnail concept, tied back to the pillar it
serves. That table is the handoff: an owner picks any row and runs
`script-my-video` on it.

## Step 7: Hand it over + name the next step

Show the strategy and the packaged pipeline, then make the next move obvious:

> That is your channel and your first run of videos, each one packaged and ready.
> When you want to make one real, pick a row and I will script it beat by beat.

Point at the execution follow-on by outcome: scripting a picked row is
`script-my-video`, which reads the four packaging fields straight from this plan.
Keep it an offer, not homework.

## Hard rules

- ❌ **Keyless. No accounts, no MCP tools.** This skill reads local files and the
  owner's words only, and names no connected tool. It writes exactly what Step 3
  captures and nothing else: the two brand fields into the brand strategy home when
  they are missing, and one dated pointer line into the profile.
- ✅ **Never write the owner's belief for them.** The point of view is quoted from
  what the owner said, in their words, and stays exactly as sharp or as soft as
  they said it. An invented belief is worse than an invented town: they are the one
  who has to defend it. On a decline, both fields stay clearly marked open slots.
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

A short framing line naming what the channel argues and who it changes (Step 3),
plus one line saying where those fields were read from or written to when Step 3
captured or topped one up. Then the channel strategy (platform-focus for YouTube,
cadence, 3-4 goal-mapped pillars, the content mix, the one metric), followed by a
dated, ordered video pipeline table where every row carries an idea, an angle, a
working title, and a thumbnail concept tied to its pillar, and a closing line
naming whose voice and research the plan is built from plus the offer to script
any row.

**Save it as `youtube-plan.md`** in the owner's working directory, beside the
`youtube-research.md` it was built from. The filename is fixed on purpose:
`script-my-video` Step 1 goes looking for "the matching pipeline row from
`plan-my-youtube`", and it can only find one if every run writes the same name. Show
the highlights inline as well, so the owner reads the plan rather than a file path.
