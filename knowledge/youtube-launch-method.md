# YouTube Launch Method — which videos get made, what each one is worth, and how the first run is shaped

The canonical knowledge for *launching and holding* a channel.
[`youtube-packaging-method.md`](youtube-packaging-method.md) decides how a single
video earns its click. This file decides the three things that sit around it:
which ideas earn a slot at all, where the hours go on each video, and how many
videos happen before anyone is allowed to read the results.

Consumers that reference this file:

- [`plan-my-youtube`](../skills/plan-my-youtube/SKILL.md) — the branch-tree idea
  filter (§1) and the first-run shape, including the commitment-versus-calendar
  split (§3).
- [`what-worked`](../skills/what-worked/SKILL.md) — walks the effort pyramid back
  up to explain a result (§2), and runs the read-against-your-own-baseline loop (§3).
- [`script-my-video`](../skills/script-my-video/SKILL.md) — the mode-aware
  scripting depth (§2).
- [`package-my-video`](../skills/package-my-video/SKILL.md) — hands a published
  video into that results loop (§3).

When in doubt, this file wins over instinct. Instinct says "make each video as
good as I can make it". The method says "put the hours where the viewer actually
meets them, and ship the run".

> Source note (dev-facing): the effort pyramid and the fixed-first-run shape
> synthesise established channel-launch practice, rewritten for a service-business
> owner. The split across the two production modes is this system's own, because
> both modes ship.

---

## 1. The branch tree — pillars are branches, not a list of four videos

The most common way a planned channel stalls is reading its pillars as a to-do
list: four pillars, four videos, now what. Pillars are not videos. The channel is
a tree. The 3-4 content pillars are the **branches**
([`build-social-strategy`](../skills/build-social-strategy/SKILL.md) sets them and
owns the count; their data shape is `content-pillars.yaml` in
[`marketing-strategy-method.md`](marketing-strategy-method.md)). Every video is
one **leaf** hanging off one branch. A branch holds as many leaves as the niche
has real questions, which is always more than an owner will ever film. A channel
does not run out of topics. It runs out of branches worth hanging them on.

Three shapes sit close together here, and blurring them is what turns a plan to
mush. Each already has an owner:

| Shape | What it is | Owner |
|---|---|---|
| **Branch** (pillar) | A recurring theme the channel is about | `build-social-strategy` |
| **Ring** | How far a topic sits from the exact viewer | `distribution-method.md`, the audience bullseye |
| **Franchise** | A repeatable title-and-format template with one swappable variable | `youtube-packaging-method.md` |

A branch is *what the channel talks about*. A ring is *how close that talk sits to
the exact viewer*. A franchise is *the reusable shape a run of leaves gets made
in*. One branch can carry several franchises; a franchise never grows into a
branch.

Worked, so the shape is concrete. A painter's four branches: quoting and pricing,
prep and materials, jobs gone wrong, choosing a painter. Three leaves off "quoting
and pricing": how a quote gets to a number, what a quote should list, why two
quotes for the same room differ by a thousand dollars. Rejected leaf: "the ten best
power tools of the year" — a real question with real demand, hanging off no branch
this channel is building, so it does not get made.

### The filter — the one question that decides whether a leaf gets made

> **Does this idea answer a real question that sits on one of the branches?**

If yes, it earns a slot. If no, it does not get made, however good the idea looks
on its own. A branch is a lane the channel is building, and an off-branch video
builds no lane: it spends the week and leaves the next video nothing to stand on.
If the idea is also off-*avatar*, that is the harder no, and it is a different
rule with its own owner (`distribution-method.md`, Lever 1).

"Answers a real question" is a **demand test, not a framing instruction.** It asks
whether a real viewer actually wants this, not that the video be written around
their pain. How the owner frames it is their call
([`content-rules.md`](content-rules.md)).

Three tests already own the detail, so run them rather than restating them:

- **Is the demand real?** The relevance attribute in `distribution-method.md`,
  Lever 2. **Exception, and it is a real one:** on a browse, story, or
  point-of-view row the pull is intrigue rather than visible search demand, so the
  branch test is the whole test. Name which kind of row it is and carry on. A
  contrarian point of view the channel argues is never rejected for having no
  search volume behind it.
- **Is the topic close enough in?** Topics come from the centre or Ring 1 only,
  craft can be studied from anywhere (`distribution-method.md`, the sourcing
  rule). "Unlimited leaves" means unlimited *within* the rings, never permission
  to sprawl.
- **Is there evidence behind it?** Every idea carries its verbatim-evidence line
  (`youtube-packaging-method.md`). An idea with no evidence is a guess, and gets
  marked as one.

---

## 2. The MVP effort pyramid — where the hours go, and how that changes by mode

**Top to bottom: idea → packaging → script → film → edit.**

This is an **effort-allocation order, not a second leverage ranking.** The leverage
ranking is the three levers in `youtube-packaging-method.md` (idea, angle,
packaging), and the angle lives inside the packaging rung here because it is
decided with the title and thumbnail. The pyramid answers a different question:
where does the next hour buy the most?

**The top carries the weight because the production order is also the consumption
order.** The viewer meets the idea and the packaging first, and for most people
that is the only part they ever meet. Then the first line of the script. Only then
anything the film and edit rungs produced. An hour spent at the bottom of the
pyramid is an hour spent on the part fewest people reach. A beautifully edited
video on a topic nobody wants is a hidden video.

The pyramid comes from **filmed** production, where the bottom two rungs are real
human hours. In the **generated** path they collapse into a render, so the same
pyramid reads differently. The mode names are
[`make-my-video`](../skills/make-my-video/SKILL.md)'s: **talking-head** (the owner
records themselves) and **faceless** (motion graphics, the default).

| Rung | Talking-head (filmed) | Faceless (generated) |
|---|---|---|
| **Idea** | Identical. The filter in §1. | Identical. |
| **Packaging** | Identical. `youtube-packaging-method.md`. | Identical, and it absorbs some of the freed hours. |
| **Script** | Hook word for word; the rest can be an outline when the week is tight. | Every line word for word. Not optional. |
| **Film** | A real shoot. Gear order: **audio, then lighting, then resolution.** | No shoot. Scene design takes this rung. |
| **Edit** | Front-load the effort into the first minute. | A render. Refine one change at a time. |

**The filmed curve.** Filming and editing are the expensive rungs, so protect
them. Script the hook word for word because it is the one part every viewer meets
and the one part that cannot be fixed later; an outlined middle is a legitimate
scope cut when the week is tight, and it usually sounds more like the owner than a
read line does. Fix the sound before the light and the light before the picture,
because viewers forgive a soft image and leave over bad audio. And put the editing
hours in the first minute, where the audience is still there, rather than spreading
them evenly across a video most people never finish. The outlined middle is a
filming-day choice the owner makes, never a tool's output; the boundary is labelled
in [`script-my-video`](../skills/script-my-video/SKILL.md), which writes every line.

**The generated curve.** There is no shoot and no timeline, so the hours those
rungs would have taken move **up**, into the script, the scene design, and the
packaging. A full word-for-word script is the right default here and is not a
luxury: the render and the voiceover have no other narration source, so a beat-list
fallback ([`make-my-video`](../skills/make-my-video/SKILL.md) allows one on a very
short clip, [`voice-my-video`](../skills/voice-my-video/SKILL.md) drafts the line
from the scene's intent) hands the owner's words to something nobody wrote. The
hours the shoot would have taken are what buy that script. Scene design is this
mode's film rung
([`design-my-scenes`](../skills/design-my-scenes/SKILL.md) owns the craft: one
visual device per beat, meaning rather than subtitles). The audio rung becomes the
voiceover when a voice key is set, and the on-screen captions when the video is
silent; the shipping-loudness check has one home, `package-my-video`'s publish gate.
Render resolution is the studio's business, not an effort decision.

**Labelled boundary — front-loading stops at the render.** Front-load *thinking*
(idea, packaging, script). Do not front-load *approvals*. `make-my-video` is
deliberately draft-first: the owner reacts to a rendered draft and never signs off
a scene spec upfront. Those two rules are compatible, and reading "front-load the
effort" as "plan the visuals harder before rendering" breaks the flow.

---

## 3. First-run discipline — the first twenty videos

A channel is a skill, and a skill needs reps before it can be judged. So the first
run is planned as a *run*, not as a series of individual decisions.

**Gate first: capacity.** If the owner is already at delivery capacity, volume is
the wrong prescription and the capacity rule overrides it (`business-method.md`
§8.3 and §10.2; `build-social-strategy` runs this as its first gate). Everything
below assumes that gate passed.

**A fixed run of about twenty videos, one a week.** Twenty is enough reps to learn
the craft and enough data to read honestly. One a week is the **recommended
default, not a prescription**: the cadence rule is `build-social-strategy`'s, and a
rhythm the owner holds beats an aspirational one they abandon.

**Labelled split — the commitment is twenty, the calendar is a fortnight.** The
twenty-video run is what the owner *commits to*. It is not a twenty-week dated
plan. The dated calendar stays inside `plan-my-content`'s hard 1-2 week ceiling and
gets re-run; this file does not lift that clamp. Naming both stops a run from
either producing a firehose nobody follows or quietly abandoning the commitment at
video four.

**A one-week cap per video. If it runs long, cut scope; do not extend.** Going over
a week is a signal that effort is landing on the wrong layer of the pyramid, and
the fix is to take scope out, not to buy time. What "cut scope" means differs by
mode:

- **Talking-head:** fewer setups, fewer takes, a shorter cut. The overrun is
  usually in the shoot or the edit, which is the bottom of the pyramid.
- **Faceless:** fewer beats and one visual-device family, then ship. A render is
  minutes to hours, so a week is generous here; an overrun almost always means the
  idea or the script was still being re-decided mid-flight, which is the top of the
  pyramid and should have been settled before the render started.

**Do not stockpile the early videos.** Make one, publish it, read it, then make the
next. Five pre-produced videos aimed in the wrong direction is five wasted videos,
and the whole point of the run is that each one is allowed to change the next.
(This is about *pre-production*, a different thing from the batch of five that
`distribution-method.md` uses as the planning unit for the 3/1/1 audience spread.
Plan in batches; do not stockpile finished videos.)

**Read every result against the owner's own baseline.** The outlier multiple and
its bands have one home, `youtube-packaging-method.md`. The skill that runs it on
the owner's own uploads after a publish is
[`what-worked`](../skills/what-worked/SKILL.md).

**And judge nothing before the run is run.** A channel is tested only after
sustained volume (`business-method.md` §10.2, and §12.7 on input goals over outcome
goals). A new channel's start is slow partly because of small-account psychology,
not because the content is failing (`distribution-method.md`, the social-credibility
line). Reading video three as a verdict is the single most common way a channel
that would have worked gets stopped.

---

## Banned framings (launch edition)

- **Calling a channel dead before the run is run.** Three videos is not a test.
- **Extending a video past its week to "get it right".** Cut scope instead.
- **Writing the filmed effort rules as if they were universal.** Every effort rule
  in §2 names its mode or gives the other mode's equivalent.

---

## Common mistakes (don't re-walk these)

| Mistake | Fix |
|---|---|
| Reading four pillars as four videos | Pillars are branches; a branch holds as many leaves as the niche has real questions |
| An idea gets made because it is interesting | Run the filter: does it answer a real question on one of the branches? |
| "Unlimited topics" read as permission to sprawl | Unlimited *within* the rings; topics come from the centre or Ring 1 |
| Hours poured into the edit while the idea stays thin | Effort goes up the pyramid, where the viewer actually meets it |
| Outlining a faceless script by default | The render and the voiceover have no other narration source; the beat-list fallback costs the owner's own words |
| Buying a better camera before a better microphone | Audio, then lighting, then resolution, on the filmed path |
| Planning twenty dated videos up front | Commit to twenty; date only the next 1-2 weeks |
| Stockpiling five videos before publishing any | Publish, read, then make the next one |

---

## Output rule

This file is operator-facing planning doctrine and writes no customer-facing copy
itself. Any copy a consuming skill produces follows
[`content-rules.md`](content-rules.md); the owner's marketing framing is their own
choice.
