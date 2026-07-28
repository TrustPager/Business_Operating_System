---
name: Research My Channel
description: Study your niche on YouTube and come back with video ideas that will actually land: what the top channels cover, what viewers keep asking for across search and public discussion, and the angles nobody is taking yet. Every idea backed by a real demand signal you can see. No accounts needed.
triggers:
  - research my channel
  - research my youtube niche
  - what videos should i make
  - find video ideas
  - what is my competition doing on youtube
function_slot: research
requires_driver: none
requires_credential: none
data_path: fetch_rest
status: active
produces_customer_facing_copy: true
---

# Research My Channel

You study the owner's YouTube niche and hand back a research read that points
straight at videos worth making: what the top channels in the space cover, what
viewers keep asking for across search and public discussion, and the angles nobody
is taking yet. Every idea is backed by a real demand signal you actually saw, not
a guess. It reads like a sharp operator studied the niche for an afternoon, not
like a scrape dump. Nothing here needs an account. (Real viewer comments, in their
own words, come from `yt-dlp`, a free local tool, not the web read: the web read
cannot reach a comment thread at all, it loads through a separate client-side call
the scrape never triggers. `yt-dlp` is keyless too, so when it is already on the
machine, comment-mining runs as part of Step 2 with no extra asking; when it is
not, this skill still delivers a complete read and recommends the one-time install
as the next best move.)

This is the first step of the YouTube factory floor. Its output,
`youtube-research.md`, feeds `plan-my-youtube` (which turns it into a channel
strategy and a video pipeline) and then `script-my-video`. The packaging craft it
draws on lives in
[`knowledge/youtube-packaging-method.md`](../../knowledge/youtube-packaging-method.md):
outlier analysis, angle and title and thumbnail differentiation, franchise
thinking. Read it before you build the gap-and-angle map so the body stays lean
and the method has one home. The distribution logic behind idea selection — the
virality formula (uncommon idea + normal lens, or common idea + unique lens), reading
the addressable audience, and remixing validated outliers — lives in
[`knowledge/distribution-method.md`](../../knowledge/distribution-method.md).

**This skill reads the live web.** It needs a connection to study the niche. No
accounts, no key: it works on day one. Keyless does not mean offline. It is
keyless but online, so it needs connectivity at runtime.

**Keyless web-research scope (HARD), per [`knowledge/research-method.md`](../../knowledge/research-method.md):**
read the niche by delegating to the keyless web-research capability the research
skills already use (`scrape` a page you name, `search` a query). Never `crawl`,
`map`, `agent`, or `extract`. Those are paid and off-floor. Read what a page you
already fetched shows you; never follow its links into extra fetches. This
per-page model is the bound. Do not name a raw web-tool in your own steps; reach
the web the same way the other floor research skills do, by delegation.

Work the gates in order. Only fall back to defaults where a gate says so.

## Step 0: Anchor on this owner and this niche (bounded)

Before you fetch anything, know:

- **Who the owner is** — trade, patch, who they serve. Pull it from the business
  profile (`brand/brand.json`, `./CLAUDE.md`) if one exists; if not, ask in one
  line.
- **The niche** — the topic space the channel will live in, in the viewer's
  words. "Quoting and pricing for tradies", not "B2B SME enablement".
- **A channel URL or two to study** — the top channels the owner already watches
  or competes with, if they can name any. If they cannot, `search` the niche and
  pick the channels that keep coming up. **Hard cap: study roughly 3 to 5
  channels and a handful of their top videos.** If the owner names more, study the
  most relevant and say so plainly; never silently drop one. That cap bounds the
  page read only: note any extra channel names `search` surfaced, since the
  optional outlier board (Step 4b) scores a handle without page-reading it.
  **Check that a channel search surfaced is actually IN the niche, not merely
  ranking for it.** A generalist channel with one video on the topic will rank for
  the topic and teach you nothing about the niche; glance at its other recent
  uploads before you study it, and drop it if the niche is a one-off for them. A
  channel presented to the owner as a "top channel in your niche" when it is not is
  a wrong finding, not a rounding error.

If a fetch is slow, blocked, or empty, say so and offer the fallback: "paste me
what is on that page and I will read it the same way." Never guess at what is on a
page you could not read. If it is not one page but both public routes failing at
once, that is a locked-down network: work the "When both public sources are
unreachable" branch below, which owns the trigger and the recovery order, instead
of forcing a thin read.

## Step 1: Competitor content scan

Read the top channels in the niche and the handful of their videos that clearly
did well. For each, note from what the page shows you:

- **Topics** — what subjects the channel covers, and which ones it returns to.
- **Formats** — talking-head, tutorial, listicle, story, and the like.
- **Cadence** — how often it posts, from visible upload dates.
- **Outliers** — the videos that outperformed that channel's own baseline. Compute
  and report the **outlier multiple** (views over the median of the channel's recent
  uploads you can see) as a plain number: "did ~4x this channel's baseline", not just
  "did well". These outliers are the strongest packaging signal in the whole read;
  `knowledge/youtube-packaging-method.md` owns how to compute and read the multiple
  (including the interpretation bands and the young-video / small-sample caveats).

Write this as the first section of `youtube-research.md`: a short, sharp scan of
what the niche's winners cover, how they package it, and which specific videos
broke out. Cite the real observed outliers by their actual titles, visible view
counts, and the computed multiple ("4.2x baseline"). Never invent an outlier, a
view count, or a multiple you did not derive from numbers you actually saw.

**When the channel page gives you no per-video counts, say so and use the dump.**
A channel's `/videos` grid is client-side rendered, so a page read often returns a
shell with the subscriber and video totals and no per-video views at all: there is
then nothing to compute a multiple *from*, and inventing one is the worst available
move. When `yt-dlp` is on the machine (Step 2 already checked), take the flat dump
for this channel and compute the multiples from real numbers, exactly as
`break-down-a-channel` does. When it is not, report the outliers you could actually
see and say plainly that the counts were not on the page, rather than reporting a
multiple you did not derive.

This scan reads outliers from whatever counts you genuinely obtained. The wide
version, scored across several channels at once and pooled, is Step 4b.

## Step 2: Viewer demand signals (every idea carries real evidence)

Mine for what the audience keeps asking for. Real comments, in viewers' own words,
are the richest version of this signal, and `yt-dlp` reaches them keylessly where
the web read cannot. **Check once, silently** (`yt-dlp --version`), and branch:

- **Installed: mine comments as the standard read, no asking.** Pull the comment
  thread for the videos most worth reading (Step 1's outliers, or the channel's
  most-discussed uploads) and fold real comment quotes into the evidence below
  alongside search and public discussion. This is part of the normal pass, not a
  deepener: an owner should not have to ask twice for the strongest signal
  available. The runnable invocation, what it writes, and its bounds live in
  [`drivers/yt-dlp/README.md`](../../drivers/yt-dlp/README.md) under the
  comment-mining use; read it rather than working the flags out from scratch.
- **Not installed: read from search and public discussion, then recommend the
  install.** Gather the demand signal from what is reachable without it: the
  `search` results for the niche's real questions, the "how do I..." and "why
  won't my..." phrasings people type, forum and Q&A threads, and the adjacent
  public discussion where viewers ask the same thing again and again. Deliver a
  complete read from these first, then recommend the free one-time install as the
  next best move, framed as adding a tool rather than working around a limitation:
  *"Real comments would sharpen this further. Want me to install `yt-dlp` (free,
  keyless, no account) so the next read can quote what viewers actually said?"*

Either way, look for:

- **Questions they keep asking** — the same question surfacing across search
  results and threads is a video waiting to be made.
- **"Nobody explains X" gaps** — where people say a topic is never covered well,
  or ask for something that does not exist yet.
- **What lands** — the explanations and moments people point to and thank
  creators for, so the owner can do more of what already works.

Turn each of these into a video idea, and **anchor every single idea to a real
observed signal.** Each idea in this section carries a short evidence line: the
exact search query, thread title, or public phrasing you actually saw, quoted as
written. An idea without a real-evidence line does not belong in this section.
This is the one rule that keeps the read honest: you are surfacing what real
people actually asked for, not guessing what they might want.

**Then read the search-demand clusters** (the findability check in
`knowledge/youtube-packaging-method.md`, which owns the method). Fetch YouTube's own
public suggestion endpoint once per seed, keylessly, for 4 to 6 seed phrasings around
the niche (the raw topic, the outcome, the audience, the tool or method), and cluster
what comes back by search intent. These are the words viewers actually type, ordered
by real search popularity, which is exactly what the owner's own phrasing for their
work is not. Report the clusters as observed phrasings, never as invented volumes:
you are reading which phrasings exist and how they rank, not a keyword volume figure.
If the endpoint is blocked or empty, say so and leave the clusters out rather than
guessing them.

Write this as the second section of `youtube-research.md`: a list of video ideas,
each with its real evidence quote underneath it, then the search-demand clusters as
a short list (the cluster, its strongest observed phrasings). `plan-my-youtube` reads
those clusters so every how-to and evergreen title it writes leads with words that
have real search demand behind them.

## Step 3: Novel-packaging gap-and-angle map

Now step back and read the niche for packaging, per
`knowledge/youtube-packaging-method.md`:

- **Identically-packaged topics** — where every channel covers the same subject
  with the same title shape and the same thumbnail, so a fresh take stands out on
  sight.
- **Untaken angles** — the honest, true angle on a well-covered topic that nobody
  in the niche is using yet.
- **Standout concepts** — the title, thumbnail, and franchise (a repeatable
  series shape) ideas that would break the pattern.

Weigh each angle with the virality formula (`knowledge/distribution-method.md`): an
uncommon idea can run with a plain lens, while a common idea needs a unique lens to
stand out, and the strongest opportunities are validated ones (a proven outlier you
can remix with the owner's own angle), not untested guesses.

Write this as the third section of `youtube-research.md`: a gap-and-angle map that
names, for the strongest opportunities, the untaken angle and a standout
title/thumbnail/franchise concept. **Ground every observation in a real outlier or
a real pattern you saw in Steps 1 and 2**, never an invented one. The map earns
its confidence from the evidence above it.

## Step 4: The remaining deepeners (optional, never required)

The three sections above are a complete first pass on their own: the surface
facts the web read reaches (titles, descriptions, tags, view counts, cadence),
the demand signals from search and public discussion, and comments too when
`yt-dlp` was already on the machine at Step 2. What is left is genuinely optional
depth, not a gap in the first pass: a video's full transcript, a retroactive
comment-mine if `yt-dlp` was not installed earlier, and the cross-channel outlier
board.

The free local `yt-dlp` tool ([`drivers/yt-dlp/`](../../drivers/yt-dlp/README.md))
covers all three, 4a and 4b below. It is a command-line tool with no account and
no key. Ask about the install once per run and reuse the same session after that.
Offer each use separately: 4a and 4b are different amounts of work.

### 4a. Full transcripts, and comments if you skipped them at Step 2

A video's full transcript is worth pulling for a close read of how a topic is
taught beat by beat, and is never part of the standard pass regardless of
`yt-dlp`'s presence (it is a heavier fetch than Step 2 needs). If `yt-dlp` was not
installed when Step 2 ran, this is also the retroactive way to add real comment
quotes to the read already delivered. Offer either as a plain choice, never a
prerequisite:

> I can pull a video's full transcript with a free local tool called `yt-dlp`, no
> account needed, for a close look at how a topic is taught. [If comments were not
> already mined: It also reaches YouTube comment threads, which the page read
> cannot, so I can go back and add real viewer quotes to what I already gave you.]
> Want me to?

If the owner says yes, install and run the `yt-dlp` binary locally via Bash (it is
keyless, no account) and fold the transcript and any comment findings back into
the relevant section, always with verbatim evidence. This never blocks or redoes
the first result; it only adds to it.

### 4b. The cross-channel outlier board (per channel)

Step 1 read outliers by eye. The board is the wide version, scored by tool. Offer
it as its own choice:

> I can also build you an outlier board. That same free local tool pulls the recent
> uploads from up to ten channels in your niche, scores every video against what
> that channel normally does, and ranks the breakouts into one list, so you see
> which angles are winning across the niche and not just on one channel. Want me to?

On a yes, gather the handles first: a handle is enough, so if fewer than ten are in
hand from Step 0, run one more `search` to fill the list before pulling. Then, per
channel:

```bash
# ten channels at most
yt-dlp --flat-playlist --playlist-end 30 --dump-json "https://www.youtube.com/@<handle>/videos" > <slug>-dump.jsonl
python ~/.claude/bos-run.py tool channel_breakdown <slug>-dump.jsonl --window 10 --min-segment 5 --out <slug>-board.json
```

Same engine `break-down-a-channel` and `what-worked` run, so a multiple means the
same thing here as anywhere else on the floor. Read each result's `timeline` only
(its `breakout` block answers the single-channel teardown's question, not this one;
`break-down-a-channel` is the follow-on when one board row is worth a deep read),
and pool them per that file's "look across the niche" rule. Selection happens once,
at the cap below: do not also pre-filter by band here.

**Each row carries the title, its multiple, its channel, and one line on what was
different (topic, angle, title promise, or thumbnail).** Keep every scored row:
which ideas earn a slot is `plan-my-youtube`'s call, at the point where its Step 4
has set the real pillars. Where `content-pillars.yaml` already exists under
`marketing-strategy/<BrandName>/`, label each row with the branch it pairs to;
otherwise label from the working themes of Steps 0 and 1 and say the label is
provisional. **Cap the board at its top ten to fifteen rows by pooled multiple.**
The board goes into section 1 of `youtube-research.md`.

**Hand it over with its limits stated, not buried.** The view counts are rounded and
flat mode returns no dates (the driver README owns that boundary), so the board ranks
into bands rather than an exact league table, two rows within about a tenth of each
other are a tie, and the pull is each channel's most recent thirty *uploads* rather
than a stretch of time: months on a weekly channel, years on a monthly one, so the
board mixes time horizons and can never say "the last year". The oldest rows inside
each thirty have no baseline yet (`outlier` is `null`) or a short one, so skip them
rather than reading them as zero (`what-worked` Step 2 owns that gate). Check each
result's `video_count` against the thirty you asked for and name the gap: a channel
too thin to score, or videos the engine skipped for a missing count, gets said out
loud, never dropped quietly. And the board measures channels that are already named;
finding them is Step 0's job. Never invent a view count, a date, or a row.

The honest cost is a first-time install and the owner's attention on the board, not
a wait. If `yt-dlp` will not install (a locked-down machine, no package manager, no
network), say so in one line and keep the Step 1 read: it is a complete result on
its own, not a degraded one. If a pull comes back blocked or empty, say so and offer
to read a channel list the owner pastes instead. A declined board is a normal
ending, so do not re-offer the board later in the run.

## When both public sources are unreachable (an occasional, expected environment)

Most runs reach the live web fine: the keyless web read renders live pages, so the
channel scan and the search signals come back with real titles, view counts, and
phrasings. Once in a while a run lands somewhere locked down instead: a corporate
firewall, an air-gapped site, or a web read that returns a page's bare shell rather
than its rendered content. This is uncommon, and it is a normal environment to
meet, so here is how the read still moves forward on real evidence.

You are in this branch when **both** public routes come back empty, not one page:
the channel and video reads *and* the search and public-discussion reads. Give it
the same patience you would before offering Step 0's paste fallback on a single
page: retry once, and confirm that at least a couple of different channel or video
reads *and* a couple of different search queries all come back empty or as bare
shells before you conclude the network is locked down. One flaky page is Step 0's
paste fallback. Both routes failing across a few reads each is this branch. When in
doubt, assume the web read is fine and keep going: this branch is the exception,
not the reflex.

**Primary recovery: reach for the local `yt-dlp` deepener (Step 4a) first.** It runs
on the owner's machine and reaches YouTube by a different route than the page read
(the video's own data feed, not the rendered page), so it can still pull real
titles, full transcripts, and real comment threads even when the page read only saw
a shell. That is the way back to real observed evidence, so offer it first here, not
last:

> The live web read is not getting through on this network. The free local yt-dlp
> tool reaches YouTube a different way and can still pull real titles, transcripts,
> and viewer comments, no account needed. Want me to run it so your read is built
> on real data?

`yt-dlp` works a video at a time, so point it at the two or three videos that matter
most. Anchoring even a few real transcripts and comment threads keeps the
demand-signal and packaging sections standing on real evidence.

**Second recovery: pasted page content is real data too.** If `yt-dlp` is not an
option (the owner declines, or the network blocks it as well), the owner's own
screen still is: "paste me what is on the channel or video page and I will read it
the same way." Pasted content is real observed evidence and needs no network or
local tool, so try it before dropping to an illustrative read.

**Last resort: a clearly-labelled illustrative read.** Only when neither `yt-dlp`
nor pasted content yields real data, ship the illustrative template rather than a
thin guess dressed as findings. Do not reinvent the framing each run: fill the
template below. This is the one place the read may carry lines you did not observe,
and it is allowed only because every line is loudly labelled illustrative. It shows
the owner the exact shape their real research will take and the fastest route to
fill it with live evidence, framed as what is coming, not what is missing.

```markdown
# YouTube research (illustrative worked example)

Quick note: this run could not reach the live web, so the read below is an
illustrative worked example built from general knowledge of your niche. It shows
the exact shape your real research will take, section by section. It is a preview,
not observed data, so treat every line as an example to confirm live. The fastest
routes to your real read are at the bottom.

## 1. Competitor content scan (illustrative)
Two or three example channels typical of this niche, with the formats they run and
the kind of outlier video that tends to break out. Every line here is an example to
confirm against your live read.

## 2. Video ideas from viewer demand (illustrative)
Two or three example video ideas the niche tends to reward. Each carries an
"evidence to capture live:" line in place of a real quote, so you can see exactly
what a finished idea looks like once the real search signal fills it in. The
search-demand clusters are left empty here, because the phrasings viewers actually
type can only come from the live read.

## 3. Novel-packaging gap-and-angle map (illustrative)
One or two example angles and a standout title or thumbnail concept, marked
illustrative. The real map earns its confidence from the observed outliers in
section 1.

## Get your live read
- Re-run on a connected network and I will replace every line above with real
  observed evidence.
- Or let me run the free local yt-dlp tool now: it reaches YouTube a different way
  and can pull real titles, transcripts, and comments even when the page read
  cannot.
- Or paste what is on a channel or video page and I will read it the same way.
```

Keep the illustrative read short. Its whole job is to show the shape and point at
the real version, never to stand in for it. The illustrative read is owner-facing
too, so hold it to the same content guardrails (see Hard rules) before you send it.

## Output shape

`youtube-research.md` is the deliverable, with all three sections: the competitor
content scan, the demand-signal video ideas (each with its real evidence quote) plus
the observed search-demand clusters, and the novel-packaging gap-and-angle map. Show the highlights inline and save the
full read to `youtube-research.md` so `plan-my-youtube` can pick it up. When the
owner took the Step 4b deepener, section 1 also carries the ranked cross-channel
outlier board.

## Hard rules

- ❌ **Keyless. No accounts, no MCP tools.** This skill reaches the web by
  delegating to the floor's keyless web-research capability, the same way the
  other research skills do. It names no connected tool in its steps.
- ❌ **No `crawl` / `map` / `agent` / `extract`.** Per-page read plus search only,
  within Step 0's cap. Those paid ops are not keyless and not on the floor.
- ❌ **Never fabricate, and your own knowledge is not evidence.** Every
  demand-signal idea carries a real evidence quote (the exact search query, thread
  title, or public phrasing you saw), exact as written. Every outlier and view
  count is one you actually saw. What you already know about the niche, however
  confident it sounds, is NOT evidence: if you did not see it on a page or a search
  result this run, it does not go in the file. No invented quotes, no invented
  numbers, no made-up outliers. "No clear demand signal found for this" is a real
  finding.
- ❌ **The web-scrape read does not reach YouTube comment threads; `yt-dlp` does,
  and it is keyless too.** Never present invented viewer comments. Mine real
  comments via `yt-dlp` when it is already on the machine (Step 2, standard, no
  asking); when it is not, source demand from search and public discussion and
  recommend the install rather than treating comments as unreachable.
- ❌ **The packaging map cites real observed outliers**, never invented ones. Its
  confidence comes from the evidence in Steps 1 and 2.
- ✅ **Content guardrails.** Customer-facing copy uses no em dashes, invents no
  facts, quotes, or numbers, and names no third-party vendor. Write it in the
  owner's brand voice; the framing and the marketing psychology are the owner's
  choice. The rules are in `knowledge/content-rules.md`.
  The owner's voice lives in `marketing-strategy/<BrandName>/voice.md` when it
  exists; say so plainly if it does not.
- ✅ **`yt-dlp` mines comments as standard when present, and stays optional for the
  rest.** Check for it once at Step 2 and mine comments straight into the read with
  no asking when it is there; when it is not, the web read still produces a
  complete first result and the install is recommended, never forced. Full
  transcripts (4a) and the cross-channel outlier board (4b) stay offered choices
  either way. Ask about a fresh install once per run; offer 4a and 4b separately,
  since they are different amounts of work.
- ✅ **Bound it.** Step 0's cap on the page read; on the optional board, ten
  channels in and its top ten to fifteen rows out. Finishable in one sitting.
- ✅ If a fetch fails, say so and offer to read pasted content instead.
- ✅ **Both public sources down is an expected environment, not a dead end.** When
  the channel reads and the search reads both come back empty, name it plainly,
  reach for the `yt-dlp` deepener first (it takes a different route to real data),
  and only then fall to a labelled illustrative read. See "When both public sources
  are unreachable."
- ❌ **Never pass an illustrative read as observed.** If you must ship the
  illustrative template, label it illustrative in the title and every section, and
  give the routes to the real version. Illustrative is a preview of the shape, never
  a finding.
