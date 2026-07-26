---
name: Script My Video
description: Turn a topic into a beat-by-beat video script in your own voice, written so it can be filmed and rendered straight away. Covers the hook, the promise, the points, and a clear call to action. Every claim rests on real evidence, never invented. Writes a script file your studio and thumbnail both read. No accounts needed.
triggers:
  - script my video
  - write a video script
  - script a youtube video
  - write my youtube script
  - turn this into a video script
function_slot: creative
requires_driver: none
requires_credential: none
data_path: local
status: active
produces_customer_facing_copy: true
engagement_copy: true
---

# Script My Video

You turn one topic into a beat-by-beat video script written in the owner's own
voice, structured so it can be filmed and rendered straight away. The script is
the spec: it writes one machine-renderable `<slug>.script.json` that the video
studio, the thumbnail, and the packaging step all read, plus a human-readable
`<slug>.script.md` the owner can film from. Nothing here needs an account.

This is the load-bearing skill of the YouTube factory floor. The craft it draws on
lives in two method files; read both before scripting so the body stays lean.
[`knowledge/youtube-script-method.md`](../../knowledge/youtube-script-method.md) owns
the YouTube-specific application: hook window, per-beat discipline, retention
structure, and the words-per-minute default this skill uses.
[`knowledge/storytelling-method.md`](../../knowledge/storytelling-method.md) owns the
attention craft it rests on: the three-step hook formula, the four-step addiction
loop, the dance (but/therefore), rhythm, and the last dab.

It runs on reasoning and the owner's own words alone. Work the gates in order.
Only fall back to defaults where a gate says so.

## Step 1: Read the ground silently

Before asking anything, read what is already on the machine so the script is in
the owner's voice and grounded in their business:

- **Source A, `brand/brand.json`:** the business name and tagline. This file is
  identity (name, tagline, colours, fonts), not voice.
- **Source B, `marketing-strategy/<BrandName>/voice.md`:** the owner's writing
  voice (built by `build-my-voice` or `build-brand-strategy`). If it exists, read
  it and write to it: the tone adjectives and signature moves, the vocabulary
  available, and the watch-out-for register. Everything the script says in the
  owner-facing lines (the spoken VO, titles, on-screen text, the call to action)
  uses this voice. If it does not exist, fall back to the brand name plus what the
  owner tells you in Step 2, and say plainly that no voice doc was found.
- **Source C, `./CLAUDE.md`:** the business shape and the offer, so the script is
  grounded in what this business actually does. Read it, do not just scan it for
  one line. The **region** is the conditional part: take it only if a `Region:`
  line is explicitly set, and never infer one that isn't stated.
- **If present, `youtube-research.md`** (from `research-my-channel`) and the
  matching pipeline row from `plan-my-youtube`: these carry the idea, the angle,
  the working title, and the thumbnail concept. When they exist, the topic and
  packaging are already chosen, so consume them rather than re-asking.
- **If present, a `build-customer-voice` synthesis:** the real customer quotes
  you will anchor claims against. Note the quote ids for `evidence_ref`.

If none of these exist, run anyway from what the owner tells you in Step 2.

## Step 2: Interview the video-specific bucket only

Ask only for what Step 1 did not already give you. When a `plan-my-youtube` row
supplied the topic and packaging, most of this is answered. Keep it to the
video-specific pieces:

- **Topic:** what this one video is about, in a sentence.
- **The one action:** the single thing the video drives the viewer to do (book a
  call, download the guide, subscribe). One call to action, not three.
- **Target length:** how long the video should run. This sets
  `meta.duration_target_s`. If the owner has no view, do not invent a number
  silently: propose one from the job the video does, and say which you assumed.
  A single-idea video or a Short runs about 60 to 90 seconds; a how-to or a
  walkthrough that has to teach something runs about 6 to 10 minutes. Pick the
  target BEFORE you draft the beats, and do not quietly revise it afterwards to
  match what you wrote, or Step 6's fit check is measuring you against yourself.
- **Aspect:** 16:9 for standard YouTube, 9:16 for a Short. Sets `meta.aspect`.

Ask the fewest questions that let you script it well. Naming the problem the
video solves is fine in this conversation: it is the owner's own planning, not
customer-facing copy.

### Lock the title before you script (the owner's pick)

The hook has to pay off the promise the title made, so the title is decided first,
by the owner, not chosen for them after the script exists.

- **Offer three to five title options**, not one. Build them from the plan row's
  working title and the angle, each option pulling a different lever (the outcome,
  the number or timeframe, the honest intrigue, the searchable phrasing). The title
  craft is `knowledge/youtube-packaging-method.md`.
- **On a how-to or evergreen video, at least one option leads with real search
  demand.** When `youtube-research.md` carries search-demand clusters, lead an
  option with the strongest on-topic cluster and say which cluster it came from.
  When there is no research file, say plainly that findability is unverified and
  point at `research-my-channel` for the demand read. Never present an invented
  search volume as evidence for a title.
- **Take the owner's pick and write it as `working_title`.** The options they did
  not pick stay in `packaging.title_options` for `package-my-video` to carry into
  the publish folder. If the owner has no preference, recommend one and say why in
  a line, then proceed on that.

This is a gate, not a formality: script the beats against the title the owner
chose. If they later change the title, re-check that the hook still pays it off.

## Step 3: Structure the beats

Build the beat list per `knowledge/youtube-script-method.md`. Every script needs,
at minimum, these roles, in this order:

- **`hook`**: the opening line that earns the next ten seconds. It must land
  inside `meta.hook_window_s` (default 5 seconds), and Step 4 fits it to that
  window by word count before its timing is written. This is the single most
  important beat. Build it with the three-step hook formula in
  `knowledge/storytelling-method.md` (context lean-in → scroll-stop → contrarian
  snapback), and open a clear curiosity loop. Step 4 scores it against the six
  power words before it is locked; a hook that has not been scored is not finished.
- **`promise`**: what the viewer walks away with if they stay.
- **`point`**: one or more teaching or story beats that deliver the promise.
  Most videos have several. Use `reset` beats between points on longer videos to
  re-earn attention, and `proof` beats where a claim needs backing. A `reset` is a
  re-hook (`knowledge/storytelling-method.md`): close one loop and open the next in
  the same breath, don't leave a flat seam.
- **`cta`**: the one clear call to action from Step 2.

Each beat carries the fields in the schema below. The `role` is one of:
`hook`, `promise`, `point`, `reset`, `proof`, `cta`.

## Step 4: Score the hook, then fit it to its window

The hook passes two gates before it is locked, in this order: it carries the pieces
that make a hook work, and it lands inside its window. Both are checks you run on
the words, not judgements you make by ear.

### Gate 1: score the hook against the six power words

Score every drafted hook against the six hook power words in
[`knowledge/storytelling-method.md`](../../knowledge/storytelling-method.md). This is
required, not a fallback for when a hook feels weak: a hook that reads confidently
can still be missing its subject or its end state, and by-ear judgement is exactly
how that ships.

1. **Quote the words** in your hook line that carry each of the four core pieces:
   subject clarity, action, objective / end state, contrast. Write them out beside
   the piece; naming a piece without pointing at the words is not a score.
2. **A piece you cannot quote words for is missing.** Rewrite the hook so it carries
   that piece, then score again. All four core pieces present is the floor for a
   hook that ships. **Contrast is the one that fails quietly:** it needs words for
   BOTH states, the base state and the new one. If the viewer has to supply the
   other half themselves ("Claude wrote it" only reads as contrast if they infer
   "instead of me writing it by hand"), the piece is inferred, not carried, and it
   counts as missing. Quote both sides or rewrite the line.
3. **Add an optional piece if there is room.** Proof and time are the upgrade; fit
   them only if Gate 2 still passes afterwards.
4. **Show the owner the score** in one short line when you present the script, so
   they can see what the hook is carrying rather than taking "it lands" on trust.

If you restructure the beats later (add a story, reorder the demo, change the
promise), re-score the hook against this gate. A hook drafted early and left alone
while everything around it moved is the common way a scored hook drifts soft again.

### Gate 2: fit the hook to its window

The hook is the one beat with a hard time limit: it has to land inside
`meta.hook_window_s` (default 5 seconds). A hook that reads fine on the page can
still run long once it is spoken, so fit it by the numbers before you lock it in,
not by eye.

Do this before you write the hook's `duration_s`:

1. **Count** the spoken words in the hook line.
2. **Convert to seconds** at the pace you will use for every beat, 150 words per
   minute by default: `seconds = words / 150 * 60`, which is just `words * 0.4`
   at 150 wpm. (The pace and why it is 150 live in
   [`knowledge/youtube-script-method.md`](../../knowledge/youtube-script-method.md),
   the one home for the method.)
3. **Compare** the result to `meta.hook_window_s`. If it fits, the hook is ready.
   If it runs over, **tighten the line** (cut words, split the idea, drop the
   runway) and count again, until it fits.
4. **Then**, and only then, write the fitted seconds as the hook's `duration_s`.

Worked example, a 5-second window at 150 wpm:

- A first-draft hook of 16 spoken words comes to `16 * 0.4 = 6.4s`. That is past
  a 5-second window, so it does not ship as written.
- Tightened to *"I quote most jobs in under a minute, on the spot."* it is 11
  words, `11 * 0.4 = 4.4s`, inside the 5-second window. That is the one you write.

Quick rule: at 150 wpm a 5-second window holds about 12 spoken words, so a hook
much longer than that will miss it. The schema check in
`tests/test_script_schema.py` rejects a hook whose `duration_s` is past
`meta.hook_window_s`, so a hook that skips this gate is caught later anyway. Fit
it here and it lands the first time.

## Step 5: Emit the script artifacts

Write two files into the owner's working directory:

1. **`<slug>.script.json`**: the machine-renderable beat script. This is the
   contract every downstream surface reads.
2. **`<slug>.script.md`**: the human-readable teleprompter and shot-list view:
   each beat as a heading with its spoken line, on-screen text, and b-roll note,
   so the owner can film straight from it.

The `<slug>` is a short kebab-case slug derived from the working title.

**The beat schema** (this skill owns the author half of the contract; the one
owner of the schema is spec §3, `docs/architecture/2026-07-05-youtube-studio-design.md`):

```jsonc
{
  "slug": "quote-in-60-seconds",
  "working_title": "How I Quote a Job in Under a Minute",
  "packaging": {
    "title_options": [ "..." ],   // several title candidates, owner's brand voice
    "thumbnail_concept": "...",    // drives make-thumbnail
    "angle": "..."                 // the differentiated take
  },
  "meta": {
    "duration_target_s": 75,       // target length from Step 2
    "aspect": "16:9",              // 16:9 or 9:16 from Step 2
    "hook_window_s": 5             // the hook must land within this many seconds
  },
  "beats": [
    {
      "id": "hook",                // unique, kebab-case, stable
      "role": "hook",             // hook | promise | point | reset | proof | cta
      "spoken": "…",              // the owner's-voice line (drives voiceover later)
      "on_screen": "…",           // the text/graphic callout (drives studio/video)
      "b_roll": "…",              // visual note: owner's own footage or stock guidance
      "evidence_ref": "…",        // optional: a customer-voice quote id the claim rests on
      "duration_s": 4              // optional: PLANNED duration (see Step 6)
    }
    // …promise, points, resets, proof, cta
  ]
}
```

Every beat carries `id`, `role`, `spoken`, `on_screen`, and `b_roll`. Add
`evidence_ref` where a claim rests on a real customer quote. Add `duration_s`
per Step 6.

## Step 6: Fill the planned timing

You already fitted the hook to its window in Step 4, so keep that `duration_s`
and apply the same maths to every other beat. Fill each beat's optional
`duration_s` from its `spoken` word count at a stated words-per-minute rate.
**Use 150 words per minute** as the default speaking pace (the rationale is in
`knowledge/youtube-script-method.md`). So a beat with 30 spoken words plans to
about `30 / 150 * 60 = 12` seconds. State in the `<slug>.script.md` that you used
150 wpm, so the owner knows what the planned times assume. If you revised the
hook line, or restructured the beats around it, run both Step 4 gates once more:
score it against the six power words, then re-check its window.

This is the *planned* timing, the author half of the timing contract (spec §3).
The video studio writes the *actual* per-beat times to `<slug>.timing.json` after
it renders, and `package-my-video` prefers the actual times and falls back to
these planned `duration_s` when no render has happened yet. You write the plan;
you do not write `<slug>.timing.json`.

Sanity-check the sum of the planned `duration_s` against
`meta.duration_target_s`. If they are far apart, tighten or expand the beats so
the script fits the target, and note the fit in one line.

## Step 7: Anchor claims in real evidence

Where the script makes a claim about results, numbers, or what customers say,
anchor it. If a `build-customer-voice` synthesis exists, point the beat's
`evidence_ref` at the real quote id and phrase the on-screen and spoken lines
from what the customer actually said. If no synthesis exists, write claims the
owner can stand behind from their own knowledge, and never manufacture a quote,
a statistic, or a testimonial to fill a beat. A strong true line beats an
invented impressive one.

## Hard rules

- ❌ **Keyless. No accounts, no MCP tools.** This skill reads local files and the
  owner's words only. It names no connected tool.
- **Content guardrails.** Customer-facing copy uses no em dashes, invents no
  facts, quotes, or numbers, and names no third-party vendor. Write it in the
  owner's brand voice; the framing and marketing psychology are the owner's
  choice. The rules are in `knowledge/content-rules.md`.
- ✅ **The hook lands inside `meta.hook_window_s`.** The opening beat earns the
  next ten seconds within the window.
- ✅ **The hook is scored, not felt.** Both Step 4 gates run before the hook is
  locked: the four core power words are each quoted from the line, then the window
  check passes. Re-score after any structural rewrite.
- ✅ **One call to action.** One `cta` beat driving the single action from Step 2.
- ✅ **Every beat carries `id`, `role`, `spoken`, `on_screen`, `b_roll`;** the
  minimum roles `hook`, `promise`, `point`, and `cta` are all present.

## Output shape

Two files in the owner's working directory: a machine-renderable
`<slug>.script.json` (the beat schema above, with planned `duration_s` on each
beat) and a human-readable `<slug>.script.md` teleprompter and shot-list view
that states the words-per-minute pace used. The hook lands inside the hook
window, there is exactly one call to action, and every claim is anchored in real
evidence or left as something the owner can stand behind.
