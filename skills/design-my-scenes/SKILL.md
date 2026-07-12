---
name: Design My Scenes
description: Turn a video script or a topic into a beat-by-beat visual plan the motion studio renders, each beat shown as one clear visual (a before-and-after, a flow, one big number, a bold line), never a wall of subtitles. Auto-picks a look and the right visual for every beat, on your own brand. Writes the plan file your studio reads. No accounts needed.
triggers:
  - design my scenes
  - plan my video scenes
  - make a scenes plan
  - visualise my video
  - turn my script into scenes
function_slot: creative
requires_driver: none
requires_credential: none
data_path: local
status: active
produces_customer_facing_copy: true
---

# Design My Scenes

You turn a video into a **visual plan**: for each beat, you choose the one visual
device that renders its *meaning* — a before-and-after, a step flow, a single big
number, a bold typographic line — never a paragraph of subtitle. You write one
machine-renderable `studio/motion/data/<slug>.scenes.json` that the Motion Studio
reads to render the video. Nothing here needs an account.

This is the planning half of the Motion Studio (module one of the Content Creation
Studio). The engine, the vocabulary, and the craft it draws on live in
[`studio/motion/CLAUDE.md`](../../studio/motion/CLAUDE.md) §4–§5 — read §4 (the
scenes schema + the registry of styles and devices) before you write a plan, so
the body stays lean and the vocabulary has one home. The schema is owned by design
spec §5.2 (`docs/architecture/2026-07-09-content-creation-studio-design.md`).

**This skill is DRAFT-FIRST.** You auto-assign the style and every visual device
from sensible defaults. You do NOT interrogate the owner on art direction — the
owner reacts to a rendered draft (that is `make-my-video`'s job), not to a plan
they have to approve upfront. Work the gates in order; only fall back to a default
where a gate says so.

## Step 1: Read the ground silently

Before writing anything, read what is already on the machine:

- **`brand/brand.json`** — the business name and voice. On-screen labels are in
  this voice. (Colour and type come from here at render time; you do not put hex or
  fonts in the plan.)
- **A `<slug>.script.json`** for this video, if one exists (from `script-my-video`).
  This is the ideal input: it already carries the beats, each with an `id`, a
  `role` (`hook`/`promise`/`point`/`proof`/`reset`/`cta`), the `spoken` line, the
  `on_screen` text, and a planned `duration_s`. When it exists, you are translating
  beats to visuals, not inventing a video.
- **`studio/motion/data/*.scenes.json`** — the committed samples, as worked
  examples of the shape and the device props.

If no script exists, work from the topic or brief the owner gives you, and keep a
tight beat list yourself (hook → one or two points → a closing line). If they want
a proper script first, that is `script-my-video`.

## Step 2: Fix the frame — mode, aspect, fps, style (all defaulted)

Set the plan's top-level direction from defaults; do not ask the owner to choose an
aesthetic:

- **`mode`**: `faceless` (the shipping mode). Talking-head and product-demo are
  later phases; do not emit them.
- **`aspect`**: take `meta.aspect` from the script if present, else `16:9`. Use
  `9:16` only when the owner has said it is a Short/Reel.
- **`fps`**: `30`.
- **`direction.style`**: default `clean_editorial` (the anchor). Pick `blueprint`
  for a how-it-works / technical explainer, or `bold_pop` for a punchy, high-energy
  promo — but only when the topic clearly leans that way. When unsure, default.
- **`direction`** also carries `palette_source` and `type_source`
  (both `"brand/brand.json"`), plus `motion`, `texture`, and `mood` — set these to
  the style's natural register (e.g. `restrained_spring` / `flat` / `confident` for
  editorial). These are hints; the style component owns the real motion.
- **`rules`**: always `{ "on_screen_max_words": 4, "visualize_not_transcribe": true,
  "one_device_per_scene": true }`.
- **`transition`**: `{ "type": "fade", "duration_frames": 12 }`.

## Step 3: Assign one visual device per beat

For each beat, choose exactly ONE device from the registry (see
`studio/motion/CLAUDE.md` §4). The four shipping devices:

| Device | Use it for | Structured `visual` props |
|---|---|---|
| `typographic_statement` | a hook or a single emphatic claim | `statement` (≤4 words), optional `kicker` (≤3 words), optional `index` ("01") |
| `before_after` | a transformation — the same thing, changed | `subject`, `before: {tag, value}`, `after: {tag, value}` |
| `process_flow` | proving it is a few simple steps | `kicker`, `steps: [{label}, …]` (2–4 short steps) |
| `big_stat` | landing one number or the payoff/CTA | `value` (number), optional `prefix`/`suffix`/`kicker`/`label`/`cta`, optional `decimals` |

Map by the beat's job, not its wording: a `hook` beat is usually a
`typographic_statement`; a `point` that contrasts old vs new is a `before_after`;
a `point` that lists how-it-works is a `process_flow`; a `proof` or `cta` that
lands a number is a `big_stat`. Aim for variety across the video — do not make
every beat a typographic statement.

**Translate the meaning into the device's props, never a subtitle.** The `spoken`
line drives the later voiceover; it does NOT go on screen. The on-screen label is
1–4 words that name the point, and the device's structured props carry the rest.

## Step 4: Write each scene

For each beat, emit a scene object:

```jsonc
{
  "id": "s1",                 // stable scene id (s1, s2, …)
  "beat_ref": "hook",         // the script beat id this realises (or the beat's role)
  "role": "hook",             // the beat role, carried through
  "intent": "…",              // one sentence: what this beat must land
  "visual_device": "typographic_statement",  // one of the four registry devices
  "on_screen_label": "Quote in 60 seconds",  // 1–4 words, brand voice
  "motion": "word_stagger",   // a hint; the style owns the real motion
  "duration_s": 3,            // from the script's planned duration_s, else your estimate
  "visual": { "index": "01", "kicker": "For tradies", "statement": "Quote in 60 seconds" }
}
```

Carry `duration_s` from the script's planned beat timing when present; otherwise
estimate from the beat's weight (a hook ~3s, a point ~4–5s, a closing stat ~3.5s).
Keep the whole video tight.

## Step 5: Lint before you write the file

Run this machine-checkable lint over every scene. If any check fails, fix it —
this is the guard that keeps the studio from drifting back into animated subtitles:

1. **`visual_device` is one of** `typographic_statement`, `before_after`,
   `process_flow`, `big_stat`. Nothing else renders.
2. **`direction.style` is one of** `clean_editorial`, `blueprint`, `bold_pop`.
3. **`on_screen_label` is 1–4 words.** Count them. Five words fails.
4. **One device per scene.** Never combine two devices in one beat.
5. **The `visual` object matches the device's props** (the table in Step 3). A
   `before_after` needs `before` and `after`; a `big_stat` needs a numeric `value`.
6. **No hex colours and no font names anywhere in the plan.** Colour and type come
   from `brand.json` at render time.
7. **No em dashes, positive framing, no third-party vendor names** in any
   `on_screen_label` (customer-facing copy — [`knowledge/content-rules.md`](../../knowledge/content-rules.md)).

## Step 6: Emit the plan

Write `studio/motion/data/<slug>.scenes.json`, where `<slug>` matches the script's
slug (or a short kebab-case slug from the topic). Say where you wrote it and give a
one-line summary of the plan (how many scenes, which style, the device per beat).
Do not render here — handing the plan to the studio is `make-my-video`'s job.

## Hard rules

- ❌ **Keyless. No accounts, no MCP tools.** Reads local files and the owner's
  words only; names no connected tool.
- ✅ **Draft-first, auto-defaulted.** You choose the style and every device from
  defaults. Do not gate the owner on art-direction choices; they react to a
  rendered draft in `make-my-video`.
- ✅ **Visualise, never transcribe.** One device per scene, 1–4 word labels, the
  meaning in the device's structured props — never a paragraph of caption text. A
  scene that reads as "centred text on a background" is the one failure mode.
- ✅ **Only registry vocabulary.** `visual_device` ∈ the four devices; `style` ∈
  the three styles. The lint (Step 5) is mandatory.
- ✅ **Content guardrails.** On-screen labels use no em dashes, invent no facts or
  numbers, and name no third-party vendor. Brand voice, from `brand.json`.

## Output shape

One machine-renderable `studio/motion/data/<slug>.scenes.json` per the schema
above: a defaulted `direction` (style + palette/type sources), the three `rules`, a
`transition`, and one scene per beat, each with a single registry `visual_device`,
a 1–4 word `on_screen_label`, structured `visual` props, and a `duration_s`. It
passes the Step 5 lint, and the Motion Studio renders it unchanged.
