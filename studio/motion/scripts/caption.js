// caption.js — local, keyless captions for a talking-head recording.
//
// The keyless path (design spec §5.2 / §6): transcribe the owner's ACTUAL speech
// with local whisper.cpp (@remotion/install-whisper-cpp), so a casual off-script
// recording captions itself with no API key. The whole chain lives in that one
// package: installWhisperCpp (compiles whisper.cpp locally), downloadWhisperModel
// (~75MB-1GB one-time), transcribe, toCaptions.
//
// The FRAGILE step is the whisper.cpp COMPILE: it needs a C/C++ build toolchain,
// which a stock Windows laptop may not have. Per the spec that step is allowed to
// fail — it must degrade gracefully to SCRIPT-DERIVED captions (estimated timing
// from the beats' spoken text), never block the render. This script attempts the
// real transcription and, on ANY failure, writes the script-derived fallback and
// says plainly which path it took.
//
// Output: data/<slug>.captions.json — a Caption[] ({text, startMs, endMs}) that
// the Overlay plan's `captions` field points at (CaptionTrack renders it).
//
// Usage:
//   npm run caption -- <slug> [--model=tiny.en|base.en|small.en] [--label="..."]

import {
  writeFileSync,
  mkdirSync,
  existsSync,
  readFileSync,
  rmSync,
  mkdtempSync,
} from "node:fs";
import { spawnSync } from "node:child_process";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { resolveFfmpeg } from "./ffmpeg.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.join(__dirname, "..");
const RECORDINGS_DIR = path.join(PROJECT_ROOT, "public", "recordings");
const DATA_DIR = path.join(PROJECT_ROOT, "data");
const WHISPER_DIR = path.join(PROJECT_ROOT, "whisper");
const WHISPER_VERSION = "1.5.5"; // whisper.cpp release installWhisperCpp knows how to build

function line(s = "") {
  console.log(s);
}
function fail(msg) {
  console.error(`\n[caption] ${msg}\n`);
  process.exit(1);
}

// --- Parse argv --------------------------------------------------------------
const argv = process.argv.slice(2);
let model = "tiny.en"; // smallest/fastest for the first attempt; owner can go bigger
let label = null;
const positionals = [];
for (const arg of argv) {
  if (arg.startsWith("--model=")) model = arg.slice("--model=".length);
  else if (arg.startsWith("--label=")) label = arg.slice("--label=".length);
  else if (!arg.startsWith("--")) positionals.push(arg);
}
const slugArg = positionals[0];
if (!slugArg) {
  line("Usage:");
  line("  npm run caption -- <slug> [--model=tiny.en|base.en] [--label=\"...\"]");
  line("");
  line("Transcribes public/recordings/<slug>.mp4 to data/<slug>.captions.json");
  line("with local whisper.cpp, degrading to script-derived captions if the");
  line("whisper compile is not available on this machine.");
  process.exit(slugArg ? 1 : 0);
}
const slug = String(slugArg).replace(/[^a-z0-9-_]/gi, "-").toLowerCase();
const recording = path.join(RECORDINGS_DIR, `${slug}.mp4`);
const outCaptions = path.join(DATA_DIR, `${slug}.captions.json`);

mkdirSync(DATA_DIR, { recursive: true });

// --- Fallback: script-derived captions (keyless, always available) -----------
// Reads data/<slug>.script.json (the ground-truth spoken text) and estimates
// per-caption timing at ~2.6 words/second, or uses a supplied --label. This is
// the graceful degrade the spec requires when the whisper compile is unavailable.
function scriptDerivedCaptions() {
  const scriptPath = path.join(DATA_DIR, `${slug}.script.json`);
  const WPS = 2.6; // words per second (spec §6: estimated timing suits short beats)
  const captions = [];
  let cursorMs = 0;

  const push = (textRaw) => {
    const t = String(textRaw || "").trim();
    if (!t) return;
    const words = t.split(/\s+/).length;
    const durMs = Math.max(Math.round((words / WPS) * 1000), 700);
    captions.push({ text: t, startMs: cursorMs, endMs: cursorMs + durMs });
    cursorMs += durMs;
  };

  if (label) {
    push(label);
    return { captions, source: "label" };
  }
  if (existsSync(scriptPath)) {
    try {
      const script = JSON.parse(readFileSync(scriptPath, "utf8"));
      const beats = Array.isArray(script.beats) ? script.beats : [];
      for (const b of beats) push(b.spoken || b.on_screen || "");
      if (captions.length) return { captions, source: "script" };
    } catch {
      /* fall through to the empty note below */
    }
  }
  // Nothing to derive from — write an empty track with a clear note.
  return { captions: [], source: "none" };
}

function writeCaptions(captions, note) {
  writeFileSync(outCaptions, JSON.stringify(captions, null, 2) + "\n", "utf8");
  line("");
  line(note);
  line(`Wrote ${captions.length} captions → data/${slug}.captions.json`);
}

function degrade(reasonSentence) {
  // If the whisper folder is half-built (exists but never produced an
  // executable), remove it so a later attempt on a machine WITH a C/C++
  // toolchain starts clean rather than short-circuiting on the stale folder.
  try {
    const exe = path.join(WHISPER_DIR, "main.exe");
    const exeNix = path.join(WHISPER_DIR, "main");
    if (existsSync(WHISPER_DIR) && !existsSync(exe) && !existsSync(exeNix)) {
      rmSync(WHISPER_DIR, { recursive: true, force: true });
    }
  } catch {
    /* best-effort cleanup */
  }
  const { captions, source } = scriptDerivedCaptions();
  if (source === "script") {
    writeCaptions(
      captions,
      `${reasonSentence} Used your script's words with estimated timing instead ` +
        `(accurate wording, timing you can nudge). This is the keyless fallback.`
    );
  } else if (source === "label") {
    writeCaptions(captions, `${reasonSentence} Used the label you supplied.`);
  } else {
    writeCaptions(
      [],
      `${reasonSentence} No script (data/${slug}.script.json) or --label was ` +
        `available to derive captions from, so the track is empty for now. ` +
        `Add a script or pass --label="..." and re-run.`
    );
  }
  process.exit(0);
}

// --- Attempt the real local transcription ------------------------------------
async function transcribeLocally() {
  if (!existsSync(recording)) {
    fail(
      `recording not found at ${recording}. ` +
        `Run \`npm run ingest -- <input> ${slug}\` first.`
    );
  }

  // whisper.cpp needs 16kHz mono WAV. Extract it with the shared ffmpeg resolver.
  const { bin } = await resolveFfmpeg();
  if (!bin) {
    degrade(
      "Captions need ffmpeg to prepare the audio, and none was found."
    );
    return;
  }
  const { installWhisperCpp, downloadWhisperModel, transcribe, toCaptions } =
    await import("@remotion/install-whisper-cpp");

  // Keep the temp WAV OUT of WHISPER_DIR so installWhisperCpp's "already
  // installed" check (it keys off the target folder) is not tricked into
  // skipping the real clone + compile.
  const wavDir = mkdtempSync(path.join(tmpdir(), "bos-caption-"));
  const tmpWav = path.join(wavDir, `${slug}.16k.wav`);
  line("Preparing audio for transcription (16kHz mono WAV)...");
  const wav = spawnSync(
    bin,
    ["-y", "-i", recording, "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", tmpWav],
    { encoding: "utf8" }
  );
  if (wav.status !== 0 || !existsSync(tmpWav)) {
    degrade("Could not extract the audio track from the recording.");
    return;
  }

  // The fragile step: compile whisper.cpp locally (needs a C/C++ toolchain).
  line("");
  line("Setting up local speech-to-text (whisper.cpp). The first time, this");
  line("compiles a small program and downloads a model — it needs a C/C++ build");
  line("toolchain and can take a few minutes. No account, no API key.");
  line("");
  await installWhisperCpp({ to: WHISPER_DIR, version: WHISPER_VERSION, printOutput: true });
  await downloadWhisperModel({ model, folder: WHISPER_DIR, printOutput: true });

  line("");
  line(`Transcribing your recording with the ${model} model...`);
  const result = await transcribe({
    inputPath: tmpWav,
    whisperPath: WHISPER_DIR,
    whisperCppVersion: WHISPER_VERSION,
    model,
    modelFolder: WHISPER_DIR,
    tokenLevelTimestamps: true,
  });

  const { captions } = toCaptions({ whisperCppOutput: result });
  rmSync(wavDir, { recursive: true, force: true });

  if (!captions || captions.length === 0) {
    degrade("Whisper ran but produced no words (the recording may be silent).");
    return;
  }
  writeCaptions(
    captions,
    "Transcribed your recording locally with whisper.cpp — real captions from " +
      "your actual speech, no API key."
  );
  process.exit(0);
}

transcribeLocally().catch((err) => {
  // ANY failure in the whisper chain (compile toolchain missing, model download
  // blocked, transcribe crash) degrades gracefully — never blocks the render.
  degrade(
    `Local speech-to-text is not available on this machine (${err && err.message ? err.message : err}).`
  );
});
