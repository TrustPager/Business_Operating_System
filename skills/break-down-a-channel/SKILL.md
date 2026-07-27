---
name: Break Down A Channel
description: Study one YouTube channel deeply and come back with how it grew: an upload-order performance timeline, the moment its views durably stepped up (or the one-off spike that faded), what changed at that point, and the one move you can borrow. Every number is real and observed. Keyless, runs on your machine, no accounts.
triggers:
  - break down a channel
  - break down this channel
  - how did this channel blow up
  - how did they grow so fast
  - reverse engineer a youtube channel
  - when did this channel take off
  - study this creator
  - what changed when they took off
function_slot: research
requires_driver: none
requires_credential: none
data_path: local
status: active
produces_customer_facing_copy: true
---

# Break Down A Channel

You take one YouTube channel and hand back a teardown that answers a single
question: **how did this channel grow, and what can the owner borrow?** Not a
data dump. A short, honest read that points at the moment things changed and the
one move worth stealing.

This is a study tool, and it is the deep-on-one companion to
[`research-my-channel`](../research-my-channel/SKILL.md): that skill reads a whole
niche to decide what the owner should make; this one goes deep on a *single*
channel to reverse-engineer how it took off. The performance craft it draws on
(the outlier multiple, reading a video against its own channel's baseline) lives
in [`knowledge/youtube-packaging-method.md`](../../knowledge/youtube-packaging-method.md);
read it before you write the "what changed" section so the method has one home.

**YouTube only, keyless, local.** The channel history comes from the local
`yt-dlp` tool ([`drivers/yt-dlp/`](../../drivers/yt-dlp/README.md)) — no account,
no key, it runs on the owner's machine. There is no TikTok or Instagram path here;
say so plainly if asked.

Work the gates in order.

## Step 0: Get the one channel

You study **one** channel per run. Get a handle or URL (`@kallawaymarketing`,
`https://www.youtube.com/@kallawaymarketing`). If the owner names several, do the
most relevant one and say the others are separate runs. Confirm which channel back
to them before pulling anything.

## Step 1: Pull the channel history (local, keyless)

Pull the channel's video list with `yt-dlp` in flat mode, via Bash:

```bash
yt-dlp --flat-playlist --dump-json "https://www.youtube.com/@<handle>/videos" > <slug>-dump.jsonl
```

This returns one JSON line per video with `view_count` (rounded) and
`playlist_index` (reverse-chronological order). It returns **no dates** in flat
mode, which is expected and fine: this skill works from upload *order*, not
calendar dates (see the driver README). If `yt-dlp` is not installed, install the
binary locally (it is keyless, no account); if the pull is blocked or empty, say
so plainly and offer to read a channel-page list the owner pastes instead. Never
invent a video or a number.

## Step 2: Run the breakout engine

Run the deterministic engine on the dump:

```bash
python ~/.claude/bos-run.py tool channel_breakdown <slug>-dump.jsonl --window 10 --min-segment 5 --out <slug>-breakdown.json
```

It returns a `timeline` (each video's rounded views and its **outlier multiple** =
views over the median of the previous ~10 videos in order) and a `breakout` verdict
(`ok` with a trigger video, or `no_upward_inflection`). The engine is the source of
the numbers; do not re-derive them by eye. Read `<slug>-breakdown.json`.

## Step 3: Write the teardown

Write `channel-breakdown-<handle>-<date>.md` and show the highlights inline. Five
parts, in order:

1. **The performance timeline.** Describe the shape across upload order (steady,
   climbing, spiky) and call out the handful of biggest outliers by their real
   multiple and title ("this one did 11x the channel's baseline"). This is the spine.

2. **The breakout moment.** If `breakout.status` is `ok`, name the trigger video and
   what its multiple and the before/after median views say: the channel durably
   stepped up here. If it is `no_upward_inflection`, say so honestly: there was no
   durable step in this window; the wins were spikes that settled back, which is its
   own useful finding.

3. **Spike or step?** Say plainly whether the channel *leveled up* (a durable higher
   base) or *fired a hit and returned to normal*. The engine's minimum-segment rule
   means a lone viral spike will read as no durable step; trust that and say it.

4. **What changed.** For the trigger video (or the top outliers if there was no
   durable step), read *what was different* against
   `knowledge/youtube-packaging-method.md`: the topic, the angle, the title promise,
   the format. This is the transferable part, and the reason matters more than the
   number. Ground it in the real titles you can see; if a cause is a reasonable read
   rather than certain, say so.

5. **The one move to borrow.** Close with a single, do-it-this-week takeaway for
   the owner's own channel, drawn straight from what worked here.

## Hard rules

- ❌ **Keyless, YouTube-only, local.** `yt-dlp` (kind local) is the data path; no
  account, no key, no other platform. Say plainly if asked for TikTok/Instagram.
- ❌ **Real observed numbers only.** Every view count and multiple comes from the
  engine's output on the real dump. Never invent a video, a number, or a multiple.
  "No durable step in this window" is a real, valid finding.
- ❌ **No dates claimed from the flat dump.** The timeline is upload *order*; do not
  present an invented calendar date as if observed.
- ❌ **The funnel/monetization layer is out of scope (v1).** No comment-to-DM,
  ManyChat, or offer/non-offer pillar analysis. Keep to the packaging-transferable core.
- ✅ **Content guardrails.** Customer-facing copy uses no em dashes, invents no
  facts, quotes, or numbers, and names no third-party vendor. Write it in the
  owner's brand voice; the framing and the marketing psychology are the owner's
  choice. The rules are in `knowledge/content-rules.md`.
  The owner's voice lives in `marketing-strategy/<BrandName>/voice.md` when it
  exists; say so plainly if it does not.
- ✅ **One channel per run.** Bounded and finishable.
- ✅ **Bands are relative, not quality.** A video below ~1x is "below this channel's
  typical", never "under-performing"; roughly half a healthy channel sits there.

## Output shape

`channel-breakdown-<handle>-<date>.md` with the five parts (timeline, breakout
moment, spike-or-step, what changed, the one move to borrow), highlights shown
inline, the full read saved to the file.
