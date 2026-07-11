---
name: Voice My Video
description: Give your faceless video a real voiceover. First we lock the narration in your own voice, then, if you have set a voice provider key, I generate a clean per-beat voiceover that syncs to your captions. No key set is fine too: your video stays silent with on-screen captions, which is exactly right for muted social autoplay.
triggers:
  - voice my video
  - add a voiceover
  - add voiceover to my video
  - narrate my video
  - generate a voiceover
  - put a voice on my video
function_slot: creative
requires_driver: render
requires_credential: key
data_path: local
status: active
produces_customer_facing_copy: true
---

# Voice My Video

You give an owner's **faceless** video a synthetic voiceover, on their own machine,
one MP3 per beat, synced to the on-screen captions. This is the connected VOICE rung
of the Content Creation Studio (`studio/motion`, spec §6). It has two halves, and
the order matters:

- **The thinking (keyless).** Assemble and confirm the voiceover script from the
  video's beats, and run every line through the owner's brand voice and the
  no-em-dash rule **before** any audio is generated. This half needs no key and no
  account, and it is the half that determines whether the voice sounds like the
  owner.
- **The doing (connected).** Generate the per-beat audio with the owner's own voice
  provider key, and write the manifest the studio plays. This half needs a key.

**Silent is a real, on-strategy answer, not a failure.** Social autoplays muted, so
a faceless video with sharp on-screen captions reads perfectly with no voiceover.
If no provider key is set, say so plainly, leave the video silent with captions, and
stop cleanly. The voiceover is an upgrade on top of a floor that already works.

The engine, the props-render contract, and the render-survival reality live in
[`studio/motion/CLAUDE.md`](../../studio/motion/CLAUDE.md). The content rules live in
[`knowledge/content-rules.md`](../../knowledge/content-rules.md). This body drives the
flow and stays lean.

## Step 1: Read the beats and confirm the video

Voiceover attaches to a video that already exists. Read what is on hand:

- **`data/<slug>.script.json`** — the ground-truth spoken lines (`beats[].spoken`).
  This is the preferred source of the narration.
- **`data/<slug>.scenes.json`** — the visual plan. Its `scenes[].beat_ref` keys are
  what the voiceover manifest matches against, so each beat's audio lands on its own
  scene. If there is no script, the scenes' `on_screen_label` / `intent` are the
  fallback source.

If neither exists, there is nothing to voice yet. Point the owner at `make-my-video`
(which writes the script and scenes) and stop.

## Step 2: Lock the narration in the owner's voice (keyless — the real work)

Before a single second of audio is generated, get the words right. This is the half
that no key can do for you.

- Assemble the spoken line for each beat from the script (or draft one from the
  scene's intent when there is no script line).
- Run every line through the owner's **brand voice** (from `brand/brand.json`) and
  **no em dashes**, and invent no facts, quotes, or numbers. The framing and the
  marketing angle are the owner's choice, in their own voice.
- Keep each beat's line tight enough to fit its scene's window. A line that would run
  long is a line to shorten, not a scene to stretch by default. If a line truly needs
  the room, note that its scene's `duration_s` should grow (the render will warn you
  too — see Step 4).
- Show the owner the full narration script and confirm it. This is the one place they
  react to words; the audio should be a formality after this.

Write the confirmed lines back into `data/<slug>.script.json` (`beats[].spoken`) so
the generator and the captions read the same ground truth.

## Step 3: Choose the provider (or degrade to silent)

The voiceover needs one of two provider keys, set in the environment. The owner sets
their own key; you never handle it in plain text and never put it in a file.

- **ElevenLabs (`ELEVENLABS_API_KEY`) — primary, recommended.** One call returns the
  audio **and** char-level timing, so the captions sync to the voice automatically,
  no extra step.
- **OpenAI (`OPENAI_API_KEY`) — secondary.** Cheaper, audio only. The captions are
  synced afterward by transcribing the voiceover locally with whisper (`npm run
  caption`). State the tradeoff plainly: *"ElevenLabs voices caption themselves;
  OpenAI voices get captioned by transcribing them back, so their timing can drift a
  little."*
- **No key set — silent.** Do not treat this as an error. Tell the owner the video
  stays silent with on-screen captions (on-strategy for muted autoplay), and that
  they can add a voiceover any time by setting a key. Then stop.

If the owner has no key and wants one, point them to their provider's dashboard to
create it and set it in their environment themselves. You never enter or store a key.

## Step 4: Generate the per-beat voiceover (connected — the doing)

With a key set and the narration confirmed, generate the audio:

```bash
cd studio/motion
npm run voice -- <slug>            # ElevenLabs if its key is set, else OpenAI
# optional: --voice=<id> --model=<id> to override the default voice/model
```

`scripts/voice.js`:

- reads the confirmed per-beat text (script first, scenes as fallback);
- generates **one MP3 per beat** at `public/audio/<slug>/beat<N>.mp3`, **never
  concatenated** into a single file;
- writes `data/<slug>.voice.json` — the manifest the studio plays (per-beat file,
  start, duration, and word/char timings for caption sync);
- **degrades to silent and exits cleanly (0) when no key is set** — the same
  graceful path as Step 3, enforced in code so a missing key can never fail a run;
- **fails loudly only on a real provider error** (a bad key, a network error), and
  when it does, no audio is written, so the video is unchanged.

If it reports that a beat's voiceover runs longer than its scene's window, lengthen
that scene's `duration_s` in `data/<slug>.scenes.json` so the audio is not clipped,
then move on. For the OpenAI path, run `npm run caption -- <slug>` afterward to sync
the captions to the generated speech.

## Step 5: Play the voice and re-render

Point the scenes plan at the voiceover and re-render:

- Add `"voice": "audio/<slug>"` to `data/<slug>.scenes.json` (the dir under
  `public/` where the beats live).
- Re-render:

```bash
cd studio/motion
npm run render -- Video output/<slug>.mp4 --props=data/<slug>.scenes.json --scale=1
```

`scripts/render.js` reads `data/<slug>.voice.json` and inlines it into the plan (the
composition runs in a headless browser and cannot read a file itself), so the
faceless engine layers each beat's MP3 on that beat's scene, on the existing
timeline. Nothing else changes: the visual duration is unchanged, and a beat with no
audio simply stays silent. **Read the finished MP4 to confirm** the voice lands on
the right scenes and the captions match, before handing off.

Then hand back to `make-my-video` / `package-my-video` to package the final video as
usual. The voiceover is just another layer the studio mixed in.

## Hard rules

- **The thinking is keyless; the doing needs a key.** Never generate audio before the
  narration is confirmed in the owner's brand voice and run through the no-em-dash
  rule. Getting the words right is the half that matters, and it needs no key.
- **Silent is a valid outcome, never a failure.** No key set means the video stays
  silent with on-screen captions, on-strategy for muted social. Say so plainly and
  exit cleanly. Never block the video on a missing key.
- **One MP3 per beat, never concatenated.** Each beat is its own file so the studio
  can align it to its own scene and re-generate one beat without redoing the rest.
- **Never handle a provider key in plain text.** The owner sets `ELEVENLABS_API_KEY`
  or `OPENAI_API_KEY` in their own environment. You never enter it, echo it, store it
  in a file, or commit it. `public/audio/` and `data/*.voice.json` are gitignored.
- **Content guardrails on everything the viewer hears.** No em dashes, no invented
  facts, quotes, or numbers, no third-party vendor names in the narration. The
  owner's brand voice, from `brand.json`; the framing is the owner's choice
  ([`knowledge/content-rules.md`](../../knowledge/content-rules.md)).
- **ElevenLabs primary, OpenAI secondary.** ElevenLabs' single-call timestamps sync
  the captions for free; OpenAI is audio-only and captioned via the local whisper
  path. State that tradeoff when the owner is on OpenAI.

## Output shape

Per-beat voiceover MP3s at `studio/motion/public/audio/<slug>/`, a
`data/<slug>.voice.json` manifest, and a re-rendered `output/<slug>.mp4` where each
beat's voice plays on its scene, synced to the captions. Or, with no key set, a clear
plain-English note that the video stays silent with on-screen captions and nothing
failed. Either way the owner confirmed the narration in their own voice first.
