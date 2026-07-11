// voice.js — the connected TTS step (the bring-your-own-key VOICE rung, spec §6).
//
// The ONLY keyed subsystem in the whole studio. Render, captions, and effects are
// 100% local and keyless; this one step turns a faceless video's spoken beats into
// synthetic voiceover with a provider key the owner sets in their environment.
//
// Input:  <slug>  — reads per-beat spoken text from data/<slug>.script.json
//                    (falls back to each scene's on_screen_label/intent from
//                    data/<slug>.scenes.json when no script exists).
// Output: public/audio/<slug>/beat<N>.mp3  — ONE MP3 per beat, never concatenated.
//         data/<slug>.voice.json           — the manifest the faceless comp plays
//                                             (per-beat file + start + duration +
//                                             word/char timings for caption sync).
//
// Providers, in order:
//   1. ElevenLabs (ELEVENLABS_API_KEY) — POST /v1/text-to-speech/{voice}/with-timestamps.
//      Returns audio + CHAR-LEVEL alignment in one call, so captions auto-sync with
//      no extra transcription. This is the primary path.
//   2. OpenAI TTS (OPENAI_API_KEY) — POST /v1/audio/speech. Audio only; per-beat
//      duration is probed with ffmpeg, and word-level caption timing comes from the
//      LOCAL whisper path in scripts/caption.js (run `npm run caption` after). The
//      manifest marks timing_source: "whisper_pending" so the skill knows to sync.
//
// Graceful degrade: NO key set -> this does NOT fail. It prints a plain-English note
// that the video stays silent with on-screen captions (on-strategy for muted social
// autoplay) and exits 0. Silent-by-default is the keyless floor; voice is the upgrade.
//
// Keyless-safe, Windows-safe: no shell, args as arrays, files written UTF-8 no BOM.
//
// Usage:
//   ELEVENLABS_API_KEY=... npm run voice -- <slug> [--voice=<id>] [--model=<id>]
//   OPENAI_API_KEY=...     npm run voice -- <slug> [--voice=alloy] [--model=tts-1]

import {
  writeFileSync,
  mkdirSync,
  existsSync,
  readFileSync,
} from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { resolveFfmpeg, probeDurationSeconds } from "./ffmpeg.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.join(__dirname, "..");
const DATA_DIR = path.join(PROJECT_ROOT, "data");
const AUDIO_ROOT = path.join(PROJECT_ROOT, "public", "audio");

// ElevenLabs defaults — a public stock voice + the general multilingual model, both
// overridable (--voice / --model, or ELEVENLABS_VOICE_ID / ELEVENLABS_MODEL_ID).
const EL_DEFAULT_VOICE = "21m00Tcm4TlvDq8ikWAM"; // "Rachel", a stock public voice
const EL_DEFAULT_MODEL = "eleven_multilingual_v2";
// OpenAI defaults.
const OA_DEFAULT_VOICE = "alloy";
const OA_DEFAULT_MODEL = "tts-1";

function line(s = "") {
  console.log(s);
}
function fail(msg) {
  console.error(`\n[voice] ${msg}\n`);
  process.exit(1);
}

// --- Parse argv --------------------------------------------------------------
const argv = process.argv.slice(2);
let voiceOverride = null;
let modelOverride = null;
const positionals = [];
for (const arg of argv) {
  if (arg.startsWith("--voice=")) voiceOverride = arg.slice("--voice=".length);
  else if (arg.startsWith("--model=")) modelOverride = arg.slice("--model=".length);
  else if (!arg.startsWith("--")) positionals.push(arg);
}
const slugArg = positionals[0];
if (!slugArg) {
  line("Usage:");
  line("  npm run voice -- <slug> [--voice=<id>] [--model=<id>]");
  line("");
  line("Generates per-beat voiceover MP3s at public/audio/<slug>/ and a");
  line("data/<slug>.voice.json manifest. Needs ELEVENLABS_API_KEY (primary) or");
  line("OPENAI_API_KEY (secondary). With no key set, the video stays silent with");
  line("on-screen captions and this exits cleanly.");
  process.exit(slugArg ? 1 : 0);
}
const slug = String(slugArg).replace(/[^a-z0-9-_]/gi, "-").toLowerCase();

// --- Assemble the per-beat spoken text ---------------------------------------
// Primary source: the script's ground-truth spoken lines. Fallback: the scenes
// plan's on-screen label / intent. Each beat is keyed by the SAME id the scenes
// plan uses as beat_ref, so the faceless comp can match audio to scene.
function readJson(p) {
  try {
    return JSON.parse(readFileSync(p, "utf8"));
  } catch {
    return null;
  }
}

function assembleBeats() {
  const scriptPath = path.join(DATA_DIR, `${slug}.script.json`);
  const scenesPath = path.join(DATA_DIR, `${slug}.scenes.json`);
  const script = existsSync(scriptPath) ? readJson(scriptPath) : null;

  // Scenes plan is read either as the source (fallback) or just for per-scene
  // planned durations (so we can flag a beat whose VO overruns its scene window).
  const scenes = existsSync(scenesPath) ? readJson(scenesPath) : null;
  const plannedByRef = {};
  if (scenes && Array.isArray(scenes.scenes)) {
    for (const s of scenes.scenes) {
      const key = s.beat_ref || s.id;
      if (key) plannedByRef[key] = s.duration_s;
    }
  }

  let beats = [];
  let source = "none";
  if (script && Array.isArray(script.beats) && script.beats.length) {
    source = "script";
    beats = script.beats
      .map((b) => ({
        beat_ref: b.id,
        text: String(b.spoken || b.on_screen || "").trim(),
      }))
      .filter((b) => b.beat_ref && b.text);
  } else if (scenes && Array.isArray(scenes.scenes) && scenes.scenes.length) {
    source = "scenes";
    beats = scenes.scenes
      .map((s) => ({
        beat_ref: s.beat_ref || s.id,
        text: String(s.on_screen_label || s.intent || "").trim(),
      }))
      .filter((b) => b.beat_ref && b.text);
  }
  return { beats, source, plannedByRef };
}

// --- Provider selection ------------------------------------------------------
// ElevenLabs primary (char-level alignment in one call), OpenAI secondary (audio
// only + local whisper for timing). No key -> graceful degrade (silent + captions).
function pickProvider() {
  const el = process.env.ELEVENLABS_API_KEY;
  const oa = process.env.OPENAI_API_KEY;
  if (el && el.trim()) return { name: "elevenlabs", key: el.trim() };
  if (oa && oa.trim()) return { name: "openai", key: oa.trim() };
  return null;
}

function degradeSilent() {
  line("");
  line("No voice provider key is set, so this video stays SILENT with on-screen");
  line("captions — which is on-strategy: social autoplays muted, so caption-only");
  line("reads perfectly without a voiceover. Nothing failed.");
  line("");
  line("To add a synthetic voiceover later, set one of these in your environment");
  line("and re-run `npm run voice -- " + slug + "`:");
  line("  ELEVENLABS_API_KEY   (primary — voices caption themselves)");
  line("  OPENAI_API_KEY       (secondary — captioned via local whisper)");
  line("");
  process.exit(0); // graceful, never a failure
}

// --- ElevenLabs: audio + char-level alignment in one call --------------------
async function ttsElevenLabs(key, text, voiceId, modelId) {
  const url =
    `https://api.elevenlabs.io/v1/text-to-speech/${encodeURIComponent(voiceId)}` +
    `/with-timestamps?output_format=mp3_44100_128`;
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "xi-api-key": key,
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify({ text, model_id: modelId }),
  });
  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`ElevenLabs returned ${res.status}: ${body.slice(0, 300)}`);
  }
  const json = await res.json();
  const audio = Buffer.from(json.audio_base64, "base64");
  // Char-level alignment -> char timings and derived word timings. ElevenLabs
  // returns parallel arrays: characters[], character_start_times_seconds[],
  // character_end_times_seconds[].
  const a = json.alignment || json.normalized_alignment || {};
  const chars = Array.isArray(a.characters) ? a.characters : [];
  const starts = Array.isArray(a.character_start_times_seconds)
    ? a.character_start_times_seconds
    : [];
  const ends = Array.isArray(a.character_end_times_seconds)
    ? a.character_end_times_seconds
    : [];
  const charTimings = chars.map((c, i) => ({
    char: c,
    start_s: starts[i] ?? null,
    end_s: ends[i] ?? null,
  }));
  const words = charsToWords(charTimings);
  const durationS =
    ends.length > 0 ? Number(ends[ends.length - 1]) : null;
  return { audio, charTimings, words, durationS, timingSource: "elevenlabs_alignment" };
}

// Group char-level timings into word-level timings (for caption sync). A word ends
// at a whitespace boundary; its start is the first non-space char's start, its end
// the last non-space char's end.
function charsToWords(charTimings) {
  const words = [];
  let cur = null;
  for (const ct of charTimings) {
    const isSpace = /\s/.test(ct.char);
    if (isSpace) {
      if (cur) {
        words.push(cur);
        cur = null;
      }
      continue;
    }
    if (!cur) cur = { word: "", start_s: ct.start_s, end_s: ct.end_s };
    cur.word += ct.char;
    if (ct.end_s != null) cur.end_s = ct.end_s;
  }
  if (cur) words.push(cur);
  return words;
}

// --- OpenAI: audio only ------------------------------------------------------
async function ttsOpenAI(key, text, voice, model) {
  const res = await fetch("https://api.openai.com/v1/audio/speech", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${key}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ model, voice, input: text, response_format: "mp3" }),
  });
  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`OpenAI returned ${res.status}: ${body.slice(0, 300)}`);
  }
  const audio = Buffer.from(await res.arrayBuffer());
  // Audio only — no alignment. Duration is probed from the MP3 (below); word-level
  // caption timing comes from the local whisper path in caption.js.
  return { audio, charTimings: [], words: [], durationS: null, timingSource: "whisper_pending" };
}

// --- Main --------------------------------------------------------------------
async function run() {
  // Graceful degrade FIRST: with no provider key, the video stays silent with
  // captions and we exit 0 — never a failure, even before we look for a script
  // (spec §6). The key is the only thing this rung strictly needs.
  const provider = pickProvider();
  if (!provider) degradeSilent();

  const { beats, source, plannedByRef } = assembleBeats();
  if (!beats.length) {
    fail(
      `no spoken text found for "${slug}". Expected data/${slug}.script.json ` +
        `(beats[].spoken) or data/${slug}.scenes.json (scenes[].on_screen_label). ` +
        `Write a script with script-my-video first.`
    );
  }

  const voiceId =
    voiceOverride ||
    (provider.name === "elevenlabs"
      ? process.env.ELEVENLABS_VOICE_ID || EL_DEFAULT_VOICE
      : process.env.OPENAI_TTS_VOICE || OA_DEFAULT_VOICE);
  const modelId =
    modelOverride ||
    (provider.name === "elevenlabs"
      ? process.env.ELEVENLABS_MODEL_ID || EL_DEFAULT_MODEL
      : process.env.OPENAI_TTS_MODEL || OA_DEFAULT_MODEL);

  const outDir = path.join(AUDIO_ROOT, slug);
  mkdirSync(outDir, { recursive: true });

  // ffmpeg only needed for the OpenAI duration probe (ElevenLabs gives duration
  // from its alignment). Resolve once; degrade the probe, never the whole run.
  const { bin: ffbin } = await resolveFfmpeg();

  line("");
  line(
    `Generating voiceover for "${slug}" with ${provider.name} ` +
      `(voice: ${voiceId}, model: ${modelId}) — ${beats.length} beats, ` +
      `text from your ${source}.`
  );
  line("One MP3 per beat, never concatenated.");
  line("");

  const manifestBeats = [];
  const overruns = [];
  let cursorS = 0; // cumulative VO-timeline start (reference for caption sync)

  for (let i = 0; i < beats.length; i++) {
    const beat = beats[i];
    const fileName = `beat${i + 1}.mp3`;
    const outPath = path.join(outDir, fileName);
    line(`  beat ${i + 1}/${beats.length} (${beat.beat_ref}): "${beat.text.slice(0, 48)}${beat.text.length > 48 ? "…" : ""}"`);

    let result;
    try {
      result =
        provider.name === "elevenlabs"
          ? await ttsElevenLabs(provider.key, beat.text, voiceId, modelId)
          : await ttsOpenAI(provider.key, beat.text, voiceId, modelId);
    } catch (err) {
      fail(
        `voice generation failed on beat ${i + 1} (${beat.beat_ref}): ` +
          `${err && err.message ? err.message : err}\n` +
          `No audio was written, so your video is unchanged (silent + captions). ` +
          `Check the key and try again.`
      );
    }

    writeFileSync(outPath, result.audio);

    // Duration: from the provider (ElevenLabs) or probed from the MP3 (OpenAI).
    let durationS = result.durationS;
    if ((durationS == null || !(durationS > 0)) && ffbin) {
      durationS = probeDurationSeconds(ffbin, outPath);
    }
    if (durationS == null || !(durationS > 0)) durationS = 0; // last-resort, never crash

    const startS = +cursorS.toFixed(3);
    const dur = +Number(durationS).toFixed(3);
    manifestBeats.push({
      beat_ref: beat.beat_ref,
      file: fileName,
      start_s: startS,
      duration_s: dur,
      words: result.words,
      chars: result.charTimings,
    });
    cursorS += dur;

    // Flag a beat whose VO overruns its scene's planned window — the skill can then
    // lengthen that scene's duration_s so the audio is not clipped.
    const planned = plannedByRef[beat.beat_ref];
    if (typeof planned === "number" && dur > planned + 0.05) {
      overruns.push({ beat_ref: beat.beat_ref, vo_s: dur, scene_s: planned });
    }
  }

  const manifest = {
    slug,
    provider: provider.name,
    voice_id: voiceId,
    model_id: modelId,
    dir: `audio/${slug}`,
    timing_source:
      provider.name === "elevenlabs" ? "elevenlabs_alignment" : "whisper_pending",
    text_source: source,
    total_duration_s: +cursorS.toFixed(3),
    beats: manifestBeats,
  };
  const manifestPath = path.join(DATA_DIR, `${slug}.voice.json`);
  writeFileSync(manifestPath, JSON.stringify(manifest, null, 2) + "\n", "utf8");

  line("");
  line(`Wrote ${manifestBeats.length} beat MP3s → public/audio/${slug}/`);
  line(`Wrote the manifest → data/${slug}.voice.json`);

  if (provider.name === "openai") {
    line("");
    line("OpenAI voices are audio-only, so caption timing is not baked in. Run");
    line(`  npm run caption -- ${slug}`);
    line("to caption the voiceover locally with whisper (keyless). ElevenLabs");
    line("voices caption themselves; OpenAI voices get captioned by transcribing them.");
  }

  if (overruns.length) {
    line("");
    line("Heads up — these beats' voiceover runs longer than the scene's planned");
    line("window, so lengthen those scenes' duration_s so nothing is clipped:");
    for (const o of overruns) {
      line(`  ${o.beat_ref}: voice ${o.vo_s}s vs scene ${o.scene_s}s`);
    }
  }

  line("");
  line("Next: add \"voice\": \"audio/" + slug + "\" to data/" + slug + ".scenes.json,");
  line("then re-render — the faceless comp will layer each beat's voice on its scene.");
  process.exit(0);
}

run().catch((err) => {
  fail(`unexpected error: ${err && err.message ? err.message : err}`);
});
