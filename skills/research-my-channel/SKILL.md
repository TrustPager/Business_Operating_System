---
name: Research My Channel
description: Study your niche on YouTube and come back with video ideas that will actually land: what the top channels cover, what viewers keep asking for in the comments, and the angles nobody is taking yet. Every idea backed by what real viewers said, in their own words. No accounts needed.
triggers:
  - research my channel
  - research my youtube niche
  - what videos should i make
  - find video ideas
  - what is my competition doing on youtube
function_slot: research
requires_driver: none
requires_credential: none
data_path: reasoning_only
status: active
---

# Research My Channel

You study the owner's YouTube niche and hand back a research read that points
straight at videos worth making: what the top channels in the space cover, what
viewers keep asking for in the comments, and the angles nobody is taking yet.
Every idea is backed by what real viewers actually said, in their own words. It
reads like a sharp operator studied the niche for an afternoon, not like a scrape
dump. Nothing here needs an account.

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
page you could not read.

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

## Step 2: Comment mining (every idea carries verbatim evidence)

Read the visible comments on the videos that matter, mining for what viewers keep
saying:

- **Questions they keep asking** — the same question under video after video is a
  video waiting to be made.
- **"Nobody explains X" gaps** — where viewers say a topic is never covered well,
  or ask for something that is not there.
- **What they loved** — the moments and explanations viewers thanked the creator
  for, so the owner can do more of what already lands.

Turn each of these into a video idea, and **anchor every single idea to a
verbatim comment.** Each idea in this section carries a short evidence line: the
viewer's own words, quoted exactly as written, that the idea rests on. An idea
without a verbatim-evidence line does not belong in this section. This is the one
rule that keeps the read honest: you are surfacing what real viewers said, not
guessing what they might want.

Write this as the second section of `youtube-research.md`: a list of video ideas,
each with its verbatim comment quote underneath it.

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

The three sections above are built on the surface facts the web read reaches:
titles, descriptions, view counts, cadence, and visible top comments. That is the
whole packaging signal, and it is a complete first pass on its own.

When the owner wants to go further, offer the optional deepener from
[`drivers/yt-dlp/`](../../drivers/yt-dlp/README.md): the keyless local `yt-dlp`
tool can pull a video's full transcript or its complete comment thread, past the
handful the page shows. Offer it as a plain choice, never a prerequisite:

> That is the full read from what the pages show. If you want, I can go deeper on
> any video with a free local tool called yt-dlp: full transcripts for a close
> look at how a topic is taught, and the complete comment thread for an exhaustive
> sweep. Totally optional, and only worth it when you want that extra depth.

If the owner says yes, install and run the `yt-dlp` binary locally via Bash (it is
keyless, no account) and fold the deeper transcript or comment findings back into
the relevant section, still with verbatim evidence. Default to the web read;
`yt-dlp` is the "go deeper?" option, never the gate to a first result.

## Output shape — positive-only, no em dashes

`youtube-research.md` is the deliverable, with all three sections: the competitor
content scan, the comment-mined ideas (each with its verbatim quote), and the
novel-packaging gap-and-angle map. Show the highlights inline and save the full
read to `youtube-research.md` so `plan-my-youtube` can pick it up.

The read is customer-facing output: positive-only, no em dashes (use commas,
colons, parentheses, or separate sentences). Frame every idea as a video worth
making and the attention it can win, never as what the owner is missing. Naming a
rival's gap is a fair, sharp observation; framing the owner's own position by what
they lack is not.

## Hard rules

- ❌ **Keyless. No accounts, no MCP tools.** This skill reaches the web by
  delegating to the floor's keyless web-research capability, the same way the
  other research skills do. It names no connected tool in its steps.
- ❌ **No `crawl` / `map` / `agent` / `extract`.** Per-page read plus search only,
  capped at roughly 3 to 5 channels and their top videos. Those paid ops are not
  keyless and not on the floor.
- ❌ **Never fabricate.** Every mined idea carries a verbatim comment quote, exact
  as written. Every outlier and view count is one you actually saw. No invented
  comments, no invented numbers, no made-up outliers. "No comments visible on this
  video" is a real finding.
- ❌ **The packaging map cites real observed outliers**, never invented ones. Its
  confidence comes from the evidence in Steps 1 and 2.
- ❌ **No em dashes** in the owner-facing read. Commas, colons, parentheses, or
  separate sentences.
- ✅ **Positive-only, outcome-led.** Every idea is a video worth making and the
  attention it can win.
- ✅ **`yt-dlp` is optional.** Offer the deeper read as a choice, never a
  prerequisite; the web read always produces a complete first result.
- ✅ **Bound it.** Roughly 3 to 5 channels and their top videos, finishable in one
  sitting.
- ✅ If a fetch fails, say so and offer to read pasted content instead.
