---
name: What Worked
description: See what actually worked on your own channel after you publish. Pulls your uploads keylessly on your machine, scores each against your own recent baseline, then names what was different about the ones that moved (idea, packaging, script, film, edit) and the one thing to repeat next time. Every number real and observed. No accounts.
triggers:
  - what worked
  - how did my last video do
  - did that video work
  - read my channel results
  - what should i repeat
  - how is my channel doing
  - review my last upload
function_slot: research
requires_driver: none
requires_credential: none
data_path: local
status: active
produces_customer_facing_copy: true
---

# What Worked

You read the owner's **own** channel after a publish and answer one question:
what moved, and what should they do again? Not a dashboard. A short, honest read
that names the one thing worth repeating in the next video.

**This is not [`break-down-a-channel`](../break-down-a-channel/SKILL.md).** That
skill studies a *stranger's* channel and brings back one move to borrow. This one
reads the owner's *own* last upload and picks the next. Same engine, opposite
direction: borrow versus repeat. If the owner points you at someone else's
channel, that is the other skill; say so and route them.

The two method files behind this read, so this body stays lean: the outlier
multiple and its bands live in
[`knowledge/youtube-packaging-method.md`](../../knowledge/youtube-packaging-method.md);
the effort pyramid you walk from the top, and the read-against-your-own-baseline
discipline, live in
[`knowledge/youtube-launch-method.md`](../../knowledge/youtube-launch-method.md).

**YouTube only, keyless, local.** The data path is the same flat `yt-dlp` dump
`break-down-a-channel` runs, and [`drivers/yt-dlp/`](../../drivers/yt-dlp/README.md)
owns that boundary. No TikTok or Instagram path here; say so plainly if asked.

Work the gates in order.

## Step 0: Confirm whose channel, and which video

Get the owner's own channel handle or URL, and confirm it back before pulling
anything. Ask which upload they want read if it is not simply the most recent
one. One channel per run.

Ask which mode that video was made in if you cannot tell:
**talking-head** (they recorded themselves) or **faceless** (motion graphics).
The vocabulary is [`make-my-video`](../make-my-video/SKILL.md)'s, and it changes
which causes are even available in Step 3.

## Step 1: Pull the owner's uploads (local, keyless)

```bash
yt-dlp --flat-playlist --dump-json "https://www.youtube.com/@<handle>/videos" > <slug>-dump.jsonl
```

One JSON line per video, with a rounded `view_count` and the channel's
reverse-chronological order. Flat mode returns **no dates** by design, so this
skill works from upload order, never a calendar date (the driver README owns that
boundary). If `yt-dlp` is not installed, install the binary locally (keyless, no
account); if the pull is blocked or empty, say so plainly and offer to read a
list the owner pastes instead. Never invent a video or a number.

## Step 2: Score every upload against the owner's own baseline

```bash
python ~/.claude/bos-run.py tool channel_breakdown <slug>-dump.jsonl --window 10 --min-segment 5 --out <slug>-results.json
```

Read `<slug>-results.json`. The `timeline` runs **oldest to newest**, so the
owner's latest upload is the last row, and each row's `outlier` is that video's
views over the median of the previous ten. The engine is the source of every
number; do not re-derive one by eye.

Three honesty gates before you interpret anything:

- **`outlier` is `null`** on a video with fewer than three uploads before it. That
  is "no baseline yet", not a zero. Say so and stop reading multiples.
- **The newest upload is the youngest**, so its multiple is the least settled
  number in the file. Name it as still compounding rather than as a verdict.
- **Below ~1x is "below this channel's typical", never "under-performing".** By
  definition about half a healthy channel sits there. The bands are in
  `youtube-packaging-method.md`.

If `breakout.status` is `ok`, the channel took a durable step up at that video,
which is worth naming. `no_upward_inflection` is not a failure finding; it is
simply not this run's question.

## Step 3: Name what was different (walk the pyramid from the top)

Only run the cause read on a video that genuinely moved. **A mover is ~2x or
above** against the owner's own baseline (the bands in
`youtube-packaging-method.md`). Nothing at 2x or above means nothing moved: say
so plainly, skip the table, and take Step 4's no-mover branch. Manufacturing a
cause for an on-baseline video is the main way this read goes wrong.

Walk the effort pyramid from the top — **idea → packaging → script → film → edit**,
which `youtube-launch-method.md` §2 owns. Take the rungs in that order, which is the
order the effort was spent (it is the same pyramid read for diagnosis, not a second
leverage ranking)
and stop at the first one that genuinely differed from the owner's other uploads.

| Rung | What was different | Where to look |
|---|---|---|
| Idea | The topic itself, or the branch it sat on | The title and the question it answers |
| Packaging | The title promise, the thumbnail, the angle inside them, and the repeatable format shape (teardown, walkthrough, list, story) | Against the owner's other titles, thumbnails, and formats |
| Script | The first ten to twenty seconds, the beat order, and where the payoff sat | Whether the click got confirmed fast, then the script's beat order |
| Film (talking-head) or scene design (faceless) | Talking-head: delivery, energy, framing. Faceless: the visual device per beat and the voiceover | What the shoot or the scene plan did that the owner's other videos did not |
| Edit (talking-head) or render (faceless) | Pacing. Talking-head: cut rhythm. Faceless: beat length and how often the visual changes | The first minute, where the effort belongs |

**The bottom two rungs are mode-specific**, which is why Step 0 asked. Do not
credit a cause at those two rungs without naming the mode: a talking-head video
has delivery and a cut rhythm to credit, a faceless one has scene design and beat
length and no delivery at all.

Two rules on attribution. One video is one data point, so say plainly when a
cause is a reasonable read rather than a certainty. And a cause that shows up in
**two or more** movers is worth far more than a confident story about one.

## Step 4: Say what to replicate — keep the style, change the job

Close with one thing to repeat in the next video, and be specific about what
transfers. **The style transfers; the topic does not.** Re-making the same video
gets a fraction of the first one's audience, because the people who wanted it
already watched it. Take the layer that worked (the format, the packaging shape,
the hook move, the pacing) and point it at the next real question on the same
branch. That is exactly the franchise move, and `youtube-packaging-method.md`
owns it: a title-and-format template with one swappable variable.

Name it as one concrete next video, not a principle.

**If nothing moved, this step still runs.** There is no winner to repeat, so the
answer is the pyramid rung above wherever the effort went last time, which is
usually the idea or the packaging. Name one concrete next video that changes that
rung.

## Step 5: Hand it to the next one

Point at the follow-on by outcome: turning the finding into the next planned
video is [`plan-my-youtube`](../plan-my-youtube/SKILL.md), and scripting the one
you just named is [`script-my-video`](../script-my-video/SKILL.md). Keep it an
offer.

## Hard rules

- ❌ **Real observed numbers only.** Every view count and multiple comes from the
  engine's output on the real dump. Never invent a video, a number, or a multiple.
- ❌ **No manufactured cause.** "This one sat on your baseline" is a real, useful
  finding. A confident story about why an average video was average is not.
- ✅ **Their channel, their baseline.** Never rank the owner's videos against
  another channel's raw view counts.
- ✅ **One channel per run.** Bounded and finishable.
- ✅ **Content guardrails.** Customer-facing copy uses no em dashes, invents no
  facts, quotes, or numbers, and names no third-party vendor. Write it in the
  owner's brand voice; the framing and the marketing psychology are the owner's
  choice. The rules are in `knowledge/content-rules.md`. The owner's voice lives
  in `marketing-strategy/<BrandName>/voice.md` when it exists; say so plainly if
  it does not.

## Output shape

A short read shown inline, nothing written to disk: the latest upload's multiple
with its honesty caveats, the real movers across the timeline, the rung that best
explains the biggest one (or a plain "nothing moved this time"), and one concrete
next video, whether it repeats a winner or changes the rung.
