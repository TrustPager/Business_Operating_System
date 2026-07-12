// ingest.js — normalise an owner's raw recording into a render-safe clip.
//
// Talking-head footage from a phone or OBS is the #1 sync trap in the whole
// pipeline: it is often variable-frame-rate (VFR), portrait with a rotation flag
// instead of baked-in rotation, and iPhone HEVC (which forces the slow
// <OffthreadVideo> fallback inside @remotion/media). Left raw, it drifts out of
// sync against the graphics layer. This pre-pass fixes all of that ONCE, on the
// way in, so the Overlay composition only ever sees clean, constant-frame-rate,
// upright, H.264/AAC video (design spec §5.2, Phase 3).
//
// What it does:
//   * autorotate portrait footage upright (ffmpeg bakes the display-matrix
//     rotation when it re-encodes, so the pixels are upright, no flag to honour);
//   * scale-to-fit the target composition (letterbox-pad to the EXACT target
//     dimensions so the recording never distorts and always fills a known frame);
//   * force constant frame rate at 30fps (`-vsync cfr -r 30`);
//   * re-encode to H.264 + AAC (`-c:v libx264 -c:a aac`), yuv420p, +faststart.
//
// Output: public/recordings/<slug>.mp4 (staticFile('recordings/<slug>.mp4') is
// what the Overlay plan references). Keyless: it reuses the shared three-arm
// ffmpeg resolver (bundled ffmpeg-static preferred → system ffmpeg → a positive
// install pointer, never a hard-fail).
//
// Usage:
//   npm run ingest -- <input-path> <slug> [--aspect=9:16|16:9|1:1]

import {
  mkdirSync,
  existsSync,
  renameSync,
  rmSync,
} from "node:fs";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { resolveFfmpeg, probeDurationSeconds, probeDimensions } from "./ffmpeg.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.join(__dirname, "..");
const RECORDINGS_DIR = path.join(PROJECT_ROOT, "public", "recordings");

const TARGET_DIMS = {
  "16:9": { width: 1920, height: 1080 },
  "9:16": { width: 1080, height: 1920 },
  "1:1": { width: 1080, height: 1080 },
};

const FPS = 30;

function line(s = "") {
  console.log(s);
}
function fail(msg) {
  console.error(`\n[ingest] ${msg}\n`);
  process.exit(1);
}

// --- Parse argv --------------------------------------------------------------
const argv = process.argv.slice(2);
let aspect = "9:16"; // talking-head defaults to portrait
const positionals = [];
for (const arg of argv) {
  if (arg.startsWith("--aspect=")) {
    aspect = arg.slice("--aspect=".length);
  } else if (arg.startsWith("--")) {
    // ignore unknown flags rather than crash
  } else {
    positionals.push(arg);
  }
}
const [inputPath, slugArg] = positionals;

if (!inputPath || !slugArg) {
  line("Usage:");
  line("  npm run ingest -- <input-path> <slug> [--aspect=9:16|16:9|1:1]");
  line("");
  line("Normalises a raw recording into public/recordings/<slug>.mp4:");
  line("constant 30fps, upright, scaled to fit, H.264/AAC — ready for Overlay.");
  process.exit(inputPath || slugArg ? 1 : 0);
}

const target = TARGET_DIMS[aspect];
if (!target) fail(`unknown --aspect "${aspect}" (use 16:9, 9:16, or 1:1).`);

const slug = String(slugArg).replace(/[^a-z0-9-_]/gi, "-").toLowerCase();
const inAbs = path.isAbsolute(inputPath)
  ? inputPath
  : path.resolve(process.cwd(), inputPath);
if (!existsSync(inAbs)) fail(`input file not found: ${inAbs}`);

// --- Resolve ffmpeg (three-arm, never hard-fail) -----------------------------
const { bin, arm } = await resolveFfmpeg();
if (!bin) {
  line("");
  line("Your recording is safe — it just needs ffmpeg to normalise it once.");
  line("Install it and re-run this, no account needed:");
  line("");
  line("  npm install            # brings in the bundled ffmpeg-static");
  line("  # or install a system ffmpeg from https://ffmpeg.org/download.html");
  line("");
  line(`Recording: ${inAbs}`);
  process.exit(0);
}

mkdirSync(RECORDINGS_DIR, { recursive: true });
const outPath = path.join(RECORDINGS_DIR, `${slug}.mp4`);
const partPath = path.join(RECORDINGS_DIR, `${slug}.part.mp4`);

// Scale-to-fit then pad to the EXACT target so the clip always fills a known
// frame with no distortion. setsar=1 normalises pixel aspect; format=yuv420p +
// bt709 keep it broadly playable. ffmpeg autorotates on re-encode by default.
const vf = [
  `scale=${target.width}:${target.height}:force_original_aspect_ratio=decrease`,
  `pad=${target.width}:${target.height}:(ow-iw)/2:(oh-ih)/2`,
  `setsar=1`,
  `format=yuv420p`,
].join(",");

const ffArgs = [
  "-y",
  "-i", inAbs,
  "-vf", vf,
  "-vsync", "cfr",
  "-r", String(FPS),
  "-c:v", "libx264",
  "-preset", "medium",
  "-crf", "20",
  "-pix_fmt", "yuv420p",
  "-color_primaries", "bt709",
  "-color_trc", "bt709",
  "-colorspace", "bt709",
  "-c:a", "aac",
  "-b:a", "160k",
  "-ac", "2",
  "-movflags", "+faststart",
  partPath,
];

line("");
line(`Normalising your recording (${arm}) → ${aspect}, ${FPS}fps, H.264/AAC...`);
const res = spawnSync(bin, ffArgs, { stdio: "inherit" });
if (res.status !== 0) {
  rmSync(partPath, { force: true });
  fail(
    `ffmpeg could not normalise the recording (exit ${res.status}). ` +
      `Check the file plays, then try again.`
  );
}
// Atomic: only publish the final name once ffmpeg returns clean.
renameSync(partPath, outPath);

// --- Report in one plain sentence --------------------------------------------
const durS = probeDurationSeconds(bin, outPath);
const dims = probeDimensions(bin, outPath);
const durTxt = durS ? `${durS.toFixed(1)}s` : "unknown length";
const dimTxt = dims ? `${dims.width}x${dims.height}` : `${target.width}x${target.height}`;
line("");
line(
  `Got your clip — ${durTxt}, ${dimTxt} (${aspect}), 30fps, fixed and ready.`
);
line(`Saved to public/recordings/${slug}.mp4`);
line("");
// A machine-readable line the caller (make-my-video / render.js) can pick up.
line(
  `INGEST_RESULT ${JSON.stringify({
    slug,
    recording: `recordings/${slug}.mp4`,
    aspect,
    fps: FPS,
    durationInSeconds: durS,
    width: dims?.width ?? target.width,
    height: dims?.height ?? target.height,
  })}`
);
