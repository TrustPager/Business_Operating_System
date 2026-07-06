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
---

# Script My Video

You turn one topic into a beat-by-beat video script written in the owner's own
voice, structured so it can be filmed and rendered straight away. The script is
the spec: it writes one machine-renderable `<slug>.script.json` that the video
studio, the thumbnail, and the packaging step all read, plus a human-readable
`<slug>.script.md` the owner can film from. Nothing here needs an account.

This is the load-bearing skill of the YouTube factory floor. The craft it draws
on lives in [`knowledge/youtube-script-method.md`](../../knowledge/youtube-script-method.md):
hook patterns, retention structure, per-beat discipline, and the words-per-minute
default this skill uses. Read it before scripting so the body stays lean and the
method has one home.

It runs on reasoning and the owner's own words alone. Work the gates in order.
Only fall back to defaults where a gate says so.

## Step 1: Read the ground silently

Before asking anything, read what is already on the machine so the script is in
the owner's voice and grounded in their business:

- **Source A, `brand/brand.json`:** the business name, the voice, the tagline.
  Everything the script says in the owner-facing lines (titles, on-screen text,
  the call to action) uses this voice.
- **Source B, `./CLAUDE.md`:** the business shape, the offer, and the region
  **only if** a `Region:` line is explicitly set. Do not infer a region that
  isn't stated.
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
  `meta.duration_target_s`.
- **Aspect:** 16:9 for standard YouTube, 9:16 for a Short. Sets `meta.aspect`.

Ask the fewest questions that let you script it well. Naming the problem the
video solves is fine in this conversation: it is the owner's own planning, not
customer-facing copy.

## Step 3: Structure the beats

Build the beat list per `knowledge/youtube-script-method.md`. Every script needs,
at minimum, these roles, in this order:

- **`hook`**: the opening line that earns the next ten seconds. It must land
  inside `meta.hook_window_s` (default 5 seconds). This is the single most
  important beat.
- **`promise`**: what the viewer walks away with if they stay.
- **`point`**: one or more teaching or story beats that deliver the promise.
  Most videos have several. Use `reset` beats between points on longer videos to
  re-earn attention, and `proof` beats where a claim needs backing.
- **`cta`**: the one clear call to action from Step 2.

Each beat carries the fields in the schema below. The `role` is one of:
`hook`, `promise`, `point`, `reset`, `proof`, `cta`.

## Step 4: Emit the script artifacts

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
      "duration_s": 6              // optional: PLANNED duration (see Step 5)
    }
    // …promise, points, resets, proof, cta
  ]
}
```

Every beat carries `id`, `role`, `spoken`, `on_screen`, and `b_roll`. Add
`evidence_ref` where a claim rests on a real customer quote. Add `duration_s`
per Step 5.

## Step 5: Fill the planned timing

Fill each beat's optional `duration_s` from its `spoken` word count at a stated
words-per-minute rate. **Use 150 words per minute** as the default speaking pace
(the rationale is in `knowledge/youtube-script-method.md`). So a beat with 30
spoken words plans to about `30 / 150 * 60 = 12` seconds. State in the
`<slug>.script.md` that you used 150 wpm, so the owner knows what the planned
times assume.

This is the *planned* timing, the author half of the timing contract (spec §3).
The video studio writes the *actual* per-beat times to `<slug>.timing.json` after
it renders, and `package-my-video` prefers the actual times and falls back to
these planned `duration_s` when no render has happened yet. You write the plan;
you do not write `<slug>.timing.json`.

Sanity-check the sum of the planned `duration_s` against
`meta.duration_target_s`. If they are far apart, tighten or expand the beats so
the script fits the target, and note the fit in one line.

## Step 6: Anchor claims in real evidence

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
- ❌ **Never fabricate evidence.** No invented customer quotes, numbers, or
  testimonials. Anchor real claims via `evidence_ref` or write what the owner can
  genuinely stand behind.
- ❌ **No em dashes** in anything the owner or a viewer reads (titles, on-screen
  text, spoken lines, the call to action). Use commas, colons, or separate
  sentences.
- ✅ **Positive-only, outcome-led** owner-facing copy. Titles and calls to action
  name the win and the result, never the pain or what is missing.
- ✅ **The hook lands inside `meta.hook_window_s`.** The opening beat earns the
  next ten seconds within the window.
- ✅ **One call to action.** One `cta` beat driving the single action from Step 2.
- ✅ **Every beat carries `id`, `role`, `spoken`, `on_screen`, `b_roll`;** the
  minimum roles `hook`, `promise`, `point`, and `cta` are all present.

## Output shape

Two files in the owner's working directory: a machine-renderable
`<slug>.script.json` (the beat schema above, with planned `duration_s` on each
beat) and a human-readable `<slug>.script.md` teleprompter and shot-list view
that states the words-per-minute pace used. The hook lands inside the hook
window, there is exactly one call to action, every owner-facing line is
positive-only with no em dashes, and every claim is anchored in real evidence or
left as something the owner can stand behind.
