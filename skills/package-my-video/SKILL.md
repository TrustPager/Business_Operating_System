---
name: Package My Video
description: Turn your rendered video into one publish-ready folder (the video, the thumbnail, title options, a full description with chapters, tags, and a short upload checklist), so all you do is upload it to YouTube yourself. Everything gathered in one place, ready to go. No accounts needed.
triggers:
  - package my video
  - get my video ready to publish
  - prepare my video for youtube
  - make my youtube description
  - bundle my video for upload
function_slot: creative
requires_driver: none
requires_credential: none
data_path: local
status: active
produces_customer_facing_copy: true
---

# Package My Video

You gather everything a finished video needs to go live into ONE clean, named,
publish-ready folder: the rendered video, the thumbnail, a set of title options,
a full YouTube description with chapters, tags, and a short upload checklist. The
owner opens the folder, uploads the video to YouTube by hand, pastes the
description, and they are done. Nothing here needs an account.

This is the last step of the YouTube factory floor. It **extends the
`assemble-content-pack` pattern** (one clean, named, publish-ready folder with a
short readme) for a video instead of a social post. Read
[`skills/assemble-content-pack/SKILL.md`](../assemble-content-pack/SKILL.md) for
that base pattern: collate, never create; copy, never move; one pack per run.
This skill applies that same discipline to the six video pieces below and adds
the YouTube-specific parts (the description, chapters, tags, and the upload
checklist). It does not fork or restate the base skill's logic.

It collects and formats what already exists. It writes no new video, renders no
new thumbnail, and makes no network call. Work the gates in order. Only fall back
to defaults where a gate says so.

**This is packaging as collation, not packaging as ideation.** Deciding the idea,
the angle, the title, and the thumbnail concept happens at the START of the floor,
in [`plan-my-youtube`](../plan-my-youtube/SKILL.md); the title options are offered
for the owner's pick in [`script-my-video`](../script-my-video/SKILL.md). This skill
carries those decisions into a folder and runs the publish gate on the result. If
someone reaches for it to decide a title, point them back up the floor rather than
inventing one here. The routing table is in
[`knowledge/youtube-packaging-method.md`](../../knowledge/youtube-packaging-method.md).

## Step 1: Find the pieces

Confirm what you are packaging. A complete video pack draws on these inputs,
each already produced by an earlier step:

| Input | Where it comes from |
|---|---|
| `<slug>.script.json` | `script-my-video` (working title, `packaging.title_options`, `packaging.angle`, `beats`) |
| The rendered `<slug>.mp4` | `studio/video` output (usually `studio/video/output/<slug>/<slug>.mp4`) |
| `<slug>.timing.json` | `studio/video` output, beside the MP4 (the actual per-beat render times) |
| The thumbnail PNG | `make-thumbnail`, driven by `packaging.thumbnail_concept` |

Ask for the path to anything you cannot already see. If a piece is genuinely
missing, name the step that makes it rather than inventing it here, and degrade
gracefully so the pack still assembles from what is present:

- No script yet? That is `script-my-video`.
- No rendered video yet? That is `studio/video` (`npm run shoot <slug>`).
- No thumbnail yet? That is `make-thumbnail`, from `packaging.thumbnail_concept`.

Handle a missing input without crashing (Step 6 covers each case). The `.script.json`
is the one input you truly need, because the title options, tags, and chapter
labels all read from it. If even that is absent, say so plainly and stop, rather
than guessing a title.

## Step 2: Name the folder

Pick one clear, human folder name from the slug, for example
`quote-a-job-in-under-a-minute`. The folder lands wherever the owner keeps their
work (default to `video-packs/<slug>/` in the working directory, and say where
you put it). Confirm the name if the slug is not obvious.

A finished pack looks like this:

```
video-packs/quote-a-job-in-under-a-minute/
  README.md            — what is in the pack and how to upload it
  quote-a-job-in-under-a-minute.mp4    — the rendered video, ready to upload
  thumbnail.png        — the thumbnail, ready to set
  metadata.md          — title options, the full description, tags, the checklist
```

## Step 3: Collate the files

Make the folder, then copy each piece in under a clear, predictable name. Copy,
never move, so the originals stay where they are.

```bash
mkdir -p "video-packs/<slug>"
cp "<path-to-rendered-mp4>" "video-packs/<slug>/<slug>.mp4"
cp "<path-to-thumbnail-png>" "video-packs/<slug>/thumbnail.png"
```

Reference the MP4 from the studio output; do not re-render it. If a copy target
is missing, leave that file out of the pack and note it in the readme (Step 6)
rather than referencing a file that is not there.

## Step 4: Build the metadata

Write `metadata.md` with four sections, all from the script, all in the owner's
brand voice:

1. **Title options** — the entries from `packaging.title_options`, as a list the
   owner picks one from. Do not invent new titles; if `title_options` is thin,
   offer the `working_title` too and say so.
2. **Description** — a short opening line in the owner's voice (from the video's
   angle and promise), then a blank line, then the **CHAPTERS** block (Step 5),
   then the one call to action from the `cta` beat, then any relevant links the
   owner gives you. Never fabricate a link or a claim.
3. **Tags** — a handful of plain, relevant tags drawn from the topic, the angle,
   and the points. Keep them honest to the content.
4. **Upload checklist** — a short manual-upload checklist (Step 7).

## Step 5: Derive the YouTube chapters (the timing contract)

Chapters follow the timing contract (spec §3,
[`docs/architecture/2026-07-05-youtube-studio-design.md`](../../docs/architecture/2026-07-05-youtube-studio-design.md)).
Read the timing source in this order:

- **Prefer `<slug>.timing.json`** when present. It is keyed by beat `id`, with
  `start_s`/`end_s` as floats, an array in render order (the actual rendered
  times). Use each beat's `start_s`.
- **Fall back to the script's planned per-beat `duration_s`** when no
  `timing.json` exists yet (no render has happened). Take a running cumulative
  sum of `duration_s` from beat to beat, so beat 1 starts at 0, beat 2 at the
  first beat's duration, and so on. State in the readme that chapters are from
  planned timing, not a render.

**The three YouTube chapter rules you MUST respect** (an invalid list breaks
YouTube's chapter feature, so honour all three):

- The **first chapter is always `00:00`**. Force the first chapter to `0:00`
  even if the first beat somehow starts later.
- There must be **at least 3 chapters**. If merging (below) would leave fewer
  than 3, do not emit a chapter list at all; instead write the description
  without chapters and note in the readme that the video was too short or had too
  few distinct beats for valid chapters.
- **Consecutive chapter start times must be at least 10 seconds apart.** YouTube
  rejects the whole list otherwise. The final chapter may reach the video end in
  under 10 seconds; that is fine, because what matters is the spacing between starts.

**Merging short beats into valid chapters.** Beats are often shorter than 10
seconds (a hook, a reset, a call to action), so you cannot map one beat to one
chapter. Walk the beats in render order and grow the current chapter until its
span reaches 10 seconds, then start the next chapter at the next beat:

1. Start the first chapter at the first beat. Its label is that beat's
   `on_screen` text (fall back to a human phrasing of its `role`, for example
   "Introduction" for `hook`).
2. For each following beat, measure the gap from the current chapter's start to
   that beat's start. If the gap is under 10 seconds, absorb the beat into the
   current chapter. If it is 10 seconds or more, close the current chapter and
   open a new one at that beat, taking its label. Apply this same test to every
   beat, the last one included, so a new chapter only ever opens 10 or more
   seconds after the previous chapter's start.
3. The final chapter runs to the end of the video. A beat that lands under 10
   seconds after the current chapter's start (including a short closing call to
   action) is absorbed rather than given its own chapter, so the last chapter
   simply holds that tail. Only the final chapter may be under 10 seconds long.
4. Before emitting, run a safety check: confirm every consecutive pair of chapter
   starts is at least 10 seconds apart. If any pair is closer, merge the later
   chapter into the one before it. Then apply the "at least 3 chapters or none"
   rule above.

Format each chapter start as a timestamp: `M:SS` normally, and `H:MM:SS` once the
video passes an hour. The list is one line per chapter, timestamp first, then the
label, for example `0:00 Quote in under a minute`.

**Worked example** (the sample fixture's `timing.json`, beats at 0.0, 4.4, 11.6,
24.0, 30.8, 41.2, 50.4, 60.0, ending 68.8). Walking the rule above (open a new
chapter at each beat that lands 10 or more seconds after the current chapter's
start, absorb the rest) gives five valid chapters:

```
0:00 Quote in under a minute
0:12 Standard rates, ready on your phone
0:24 The part most people miss
0:41 Chosen over two others
1:00 Book your free quote call
```

Every consecutive pair of chapter starts is at least 10 seconds apart; only the
final chapter is shorter, holding the tail to the video end, which is allowed.
The first is `0:00`, and there are more than 3, so the list is valid. (Round each `start_s` to the nearest second for the timestamp, so
`11.6` becomes `0:12`.)

## Step 6: Degrade gracefully when an input is missing

Never crash on a missing input. Assemble what is present and note each gap
plainly in the readme:

- **No `timing.json`:** derive chapters from the script's planned `duration_s`
  (Step 5 fallback) and say so. If beats have no `duration_s` either, leave
  chapters out and note it.
- **No rendered MP4:** assemble the metadata, thumbnail, and readme, and note
  that the video file is still to be rendered (point at `studio/video`). The pack
  is a head start, not a blocker.
- **No thumbnail:** assemble the rest and note that the thumbnail is still to be
  made (point at `make-thumbnail`).
- **Too few beats for 3+ valid chapters:** write the description without a
  chapter block and note why.

## Step 7: Write the readme and the upload checklist

Write a short `README.md` in the folder saying what the pack is and the manual
steps to publish it. Manual upload is the honest ending of the floor: the owner
uploads the video to YouTube themselves. There is no account, no API, and no
automatic upload here.

```markdown
# Video pack: <working title>

**Status:** <from the Step 8 publish gate: "ready to upload", or "holding: <check>">

## Publish gate
<one line per check: passed, or what is holding it and what fixes it>

## What is in here
- `<slug>.mp4`: the video to upload
- `thumbnail.png`: the thumbnail to set
- `metadata.md`: the title options, the full description with chapters, and tags

## How to publish
1. Upload `<slug>.mp4` to YouTube.
2. Pick one of the title options from `metadata.md`.
3. Paste the description from `metadata.md` (the chapters work once the timestamps are in the description).
4. Set `thumbnail.png` as the custom thumbnail.
5. Add the tags from `metadata.md`.
6. Publish when you are ready.

Assembled on <date>. Give the title, description, and thumbnail one last read
before you publish.
```

If a piece was left out, drop its line rather than naming a file that is not
there, and add the one-line note about what is still to come.

## Step 8: Run the publish gate before you hand it over

A pack is "ready to upload" only after it passes the gate. Run every check, then
report the result as a short pass/hold list in the readme under **Publish gate**.
Nothing is called ready while a check is failing: say which check failed and what
fixes it.

The checks you can run yourself, from the pack on disk:

1. **A title is chosen.** `working_title` holds the owner's picked title (not a
   placeholder), and `metadata.md` carries the remaining options underneath it.
2. **The thumbnail is in the pack.** `thumbnail.png` exists and is the 1280x720
   render, not a placeholder. If it is missing, this check holds the pack.
3. **The video is in the pack.** `<slug>.mp4` exists and is a non-zero file.
4. **The description carries its chapters and exactly one call to action.** Chapters
   are a valid list (Step 5's three rules) or deliberately absent with the reason
   noted, and there is one CTA, matching the script's single `cta` beat.
5. **Every link in the description is one the owner gave you.** No invented link, no
   placeholder URL left in the text.
6. **Tags are present** and honest to the content.
7. **The copy passes the content guardrails.** Read the title, description, and tags
   once more for em dashes, invented facts, quotes or numbers, and third-party
   vendor names. This is the last surface before the words are public.

The two checks the owner runs, which you ask for rather than assert:

8. **The video ends on its rendered ending.** Ask the owner to watch the last few
   seconds and confirm the video ends where it was meant to, on the closing frame
   and the loop into the next video, not mid-beat or on a cut-off word. A truncated
   render is invisible in the file listing and obvious in the last two seconds.
9. **The audio is at a shipping level.** A raw render is usually well under the
   loudness a viewer expects, and a video that plays quiet reads as amateur before a
   word lands. If the render pipeline has a mastering pass, confirm it ran; the
   target to aim for is roughly -14 LUFS integrated with true peak under -1 dB, and
   a two-pass measure-then-normalise is the reliable way to hit it. If no mastering
   pass exists, say plainly that the audio is unmastered so the owner can decide.

Write the gate result into the readme's `**Status:**` line: `ready to upload` when
every check passed, or `holding: <the failing check>` when one did not. An honest
hold is the point of the gate; a pack that ships broken is the failure it prevents.

Once your YouTube account is connected in a later step, this same folder can be
uploaded for you, and the video's performance can feed back into your next round
of ideas. That is the upgrade. The publish-ready folder is the win today, and it
ships with zero accounts connected.

## Hard rules

- ❌ **Keyless and local.** This runs with zero accounts connected. No `mcp__`
  tools, no network, no upload. It reads local files and writes a folder on disk.
- ❌ **Collate and format only, never create.** No new video, no new thumbnail,
  no invented title, link, or claim. If a piece is missing, name the step that
  makes it and degrade gracefully.
- ✅ **Copy, never move.** The originals stay put; the pack holds copies.
- ✅ **Valid YouTube chapters or none.** First chapter `0:00`, at least 3
  chapters, each at least 10 seconds (merge short beats forward; the final
  chapter may hold a short tail). If a valid list is impossible, emit no chapter
  block and note why.
- ✅ **Prefer `timing.json`, fall back to planned `duration_s`.** Real render
  times when they exist; the script's planned timing otherwise, stated as such.
- ✅ **Content guardrails.** Customer-facing copy uses no em dashes, invents no
  facts, quotes, or numbers, and names no third-party vendor. Write it in the
  owner's brand voice; the framing and marketing psychology are the owner's
  choice. The rules are in `knowledge/content-rules.md`.
  The owner's voice lives in `marketing-strategy/<BrandName>/voice.md` when it
  exists; say so plainly if it does not.
- ✅ **The publish gate decides the status.** A pack reads `ready to upload` only
  when every Step 8 check passed. A failing check is named plainly in the readme and
  holds the pack; never call a pack ready because the files are present.
- ✅ **Manual upload is the ending.** The pack is ready for the owner to upload by
  hand. Uploading is a separate, later step, not part of this skill.

## Output shape

One clean, named, publish-ready folder holding the video, the thumbnail, and a
`metadata.md` (title options, a full YouTube description with a valid chapter
list, tags, and a manual-upload checklist), plus a short `README.md` whose status line and publish-gate list report the Step 8
result, so the owner can see what passed and what is holding. The chapters come from
`<slug>.timing.json` when present and from the script's planned `duration_s`
otherwise, and any missing input is noted plainly rather than crashing the run.
