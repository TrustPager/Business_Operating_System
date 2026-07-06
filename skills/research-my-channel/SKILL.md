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
---

# Research My Channel

You study the owner's YouTube niche and hand back a research read that points
straight at videos worth making: what the top channels in the space cover, what
viewers keep asking for across search and public discussion, and the angles nobody
is taking yet. Every idea is backed by a real demand signal you actually saw, not
a guess. It reads like a sharp operator studied the niche for an afternoon, not
like a scrape dump. Nothing here needs an account. (Want real viewer comments in
their own words? The keyless web read cannot reach YouTube comment threads, so the
skill offers the free local `yt-dlp` deepener for that, no account either.)

This is the first step of the YouTube factory floor. Its output,
`youtube-research.md`, feeds `plan-my-youtube` (which turns it into a channel
strategy and a video pipeline) and then `script-my-video`. The packaging craft it
draws on lives in
[`knowledge/youtube-packaging-method.md`](../../knowledge/youtube-packaging-method.md):
outlier analysis, angle and title and thumbnail differentiation, franchise
thinking. Read it before you build the gap-and-angle map so the body stays lean
and the method has one home.

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
  most relevant and say so plainly; never silently drop one.

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
- **Outliers** — the videos that plainly outperformed that channel's own
  baseline (far more views than its typical upload). These outliers are the
  strongest packaging signal in the whole read; the method file explains how to
  read them.

Write this as the first section of `youtube-research.md`: a short, sharp scan of
what the niche's winners cover, how they package it, and which specific videos
broke out. Cite the real observed outliers by their actual titles and visible view
counts. Never invent an outlier or a number you did not see.

## Step 2: Viewer demand signals (every idea carries real evidence)

Mine for what the audience keeps asking for. The keyless web read does not reach
YouTube comment threads (they load through a separate client-side call the scrape
never triggers), so gather the demand signal from the public sources it **does**
reach: the `search` results for the niche's real questions, the "how do I..." and
"why won't my..." phrasings people type, forum and Q&A threads, and the adjacent
public discussion where viewers ask the same thing again and again. Look for:

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

Write this as the second section of `youtube-research.md`: a list of video ideas,
each with its real evidence quote underneath it.

**For real viewer comments in their own words, offer the deepener.** Comments are
the richest demand signal, and the keyless web read cannot reach them. When the
owner wants that depth, offer the free local `yt-dlp` tool (Step 4): "YouTube
hides comment threads from the keyless web read, so to mine real viewer comments
in their own words I can use the free local yt-dlp tool, no account needed. Want
me to?" Keep it offered, never forced: this section stands on its own from search
and public discussion.

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

Write this as the third section of `youtube-research.md`: a gap-and-angle map that
names, for the strongest opportunities, the untaken angle and a standout
title/thumbnail/franchise concept. **Ground every observation in a real outlier or
a real pattern you saw in Steps 1 and 2**, never an invented one. The map earns
its confidence from the evidence above it.

## Step 4: Offer the deeper read (optional, never required)

The three sections above are built on the surface facts the keyless web read
actually reaches on YouTube: channel and video titles, descriptions, tags, view
counts, and posting cadence, plus the demand signals you can gather from search
results and adjacent public discussion. That is a real packaging signal and a
complete first pass on its own. What the keyless read does **not** reach is a
video's comment thread: YouTube loads comments through a separate client-side call
the keyless page-scrape never triggers, so real viewer comments are not in the
first-pass read.

That is exactly where the optional deepener earns its keep. When the owner wants
real viewer comments in their own words, or a video's full transcript, offer the
keyless local `yt-dlp` tool from
[`drivers/yt-dlp/`](../../drivers/yt-dlp/README.md). It is a free local
command-line tool, no account and no key, that pulls a video's complete comment
thread and its full transcript, past what any page shows. Offer it as a plain
choice, never a prerequisite:

> YouTube hides comment threads from the keyless web read, so to mine real viewer
> comments in their own words I can use a free local tool called yt-dlp. No
> account needed, it just runs on your machine. It also pulls a video's full
> transcript for a close look at how a topic is taught. Want me to?

If the owner says yes, install and run the `yt-dlp` binary locally via Bash (it is
keyless, no account) and fold the real comment and transcript findings back into
the relevant section, always with verbatim evidence. Default to the web read for
the first pass; `yt-dlp` is the "go deeper?" option that unlocks true comment
mining, never the gate to a first result.

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

**Primary recovery: reach for the local `yt-dlp` deepener (Step 4) first.** It runs
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
what a finished idea looks like once the real search signal fills it in.

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
too, so run the same em-dash sweep on it (see Output shape) before you send it.

## Output shape — positive-only, no em dashes

`youtube-research.md` is the deliverable, with all three sections: the competitor
content scan, the demand-signal video ideas (each with its real evidence quote),
and the novel-packaging gap-and-angle map. Show the highlights inline and save the
full read to `youtube-research.md` so `plan-my-youtube` can pick it up.

The read is customer-facing output: positive-only, no em dashes (use commas,
colons, parentheses, or separate sentences). Frame every idea as a video worth
making and the attention it can win, never as what the owner is missing. Naming a
rival's gap is a fair, sharp observation; framing the owner's own position by what
they lack is not.

**Pre-write gate (do this before you write any line to `youtube-research.md`):**
before you commit a single line to the file, replace every em dash with a period,
a comma, a colon, or parentheses. This file is owner-facing and it runs long: the
em-dash ban applies to every line of it, not just the short titles and idea names.
It is easy to hold the rule in a title and lose it across the scan prose, the idea
list, and the gap-and-angle map, so hold it everywhere.

This, not that:

- Write this: "Fix It Yourself, specific named-part repair tutorials". Not this:
  "Fix It Yourself — specific named-part repair tutorials".
- Write this: "231,773 views on a beginners guide". Not this: "... beginners
  guide — 231,773 views".

**Post-write self-check (before you declare this step done):** after you write
`youtube-research.md`, do a literal find-and-replace of the em-dash character
across the WHOLE file (a replace-all, not a visual read: em dashes hide easily in
long prose, so sweep them mechanically), swapping each for a comma, colon, period,
or parentheses. Then re-read for any line that frames the owner by what they lack
and fix it. Only then is the output done.

## Hard rules

- ❌ **Keyless. No accounts, no MCP tools.** This skill reaches the web by
  delegating to the floor's keyless web-research capability, the same way the
  other research skills do. It names no connected tool in its steps.
- ❌ **No `crawl` / `map` / `agent` / `extract`.** Per-page read plus search only,
  capped at roughly 3 to 5 channels and their top videos. Those paid ops are not
  keyless and not on the floor.
- ❌ **Never fabricate, and your own knowledge is not evidence.** Every
  demand-signal idea carries a real evidence quote (the exact search query, thread
  title, or public phrasing you saw), exact as written. Every outlier and view
  count is one you actually saw. What you already know about the niche, however
  confident it sounds, is NOT evidence: if you did not see it on a page or a search
  result this run, it does not go in the file. No invented quotes, no invented
  numbers, no made-up outliers. "No clear demand signal found for this" is a real
  finding.
- ❌ **The keyless read does not reach YouTube comment threads.** Never present
  invented viewer comments. Real comment mining in a viewer's own words needs the
  optional `yt-dlp` deepener (Step 4); until the owner opts in, source demand from
  search and public discussion instead.
- ❌ **The packaging map cites real observed outliers**, never invented ones. Its
  confidence comes from the evidence in Steps 1 and 2.
- ❌ **No em dashes** anywhere in the owner-facing read, not just titles. Run the
  pre-write gate and the post-write self-check in Output shape. Commas, colons,
  parentheses, or separate sentences.
- ✅ **Positive-only, outcome-led.** Every idea is a video worth making and the
  attention it can win.
- ✅ **`yt-dlp` is optional.** Offer the deeper read as a choice, never a
  prerequisite; the web read always produces a complete first result. It is the
  one path to real viewer comments in their own words, so offer it whenever the
  owner wants comment mining.
- ✅ **Bound it.** Roughly 3 to 5 channels and their top videos, finishable in one
  sitting.
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
