// render.js — the one render entry the guided skill drives.
//
// It wraps the Remotion CLI so an owner (and `make-my-video`) never types a raw
// render command. Its whole job is the props seam:
//
//   npm run render -- <CompId> <output.mp4> --props='{"scenesPath":"data/x.scenes.json"}'
//   npm run render -- <CompId> <output.mp4> --props=data/x.scenes.json
//   npm run render -- <CompId> <output.mp4>            (sample comps, no plan)
//
// Remotion evaluates `calculateMetadata` INSIDE a headless browser, so it cannot
// read a file off disk. This wrapper does the disk read in Node: it resolves the
// plan (from a `scenesPath`, a plan file path, or an inline plan), writes the
// resolved plan to a temp file, and hands THAT to `remotion render --props=<file>`
// so the plan arrives inline as input props. Every other flag (`--gl`, `--scale`,
// `--concurrency`, ...) is forwarded untouched.
//
// After a successful render it writes `<slug>.timing.json` beside the MP4 (the
// same shape studio/video emits, spec §3), so `package-my-video` gets chapters.
//
// Keyless, local, no network. Windows-safe: spawns node on the CLI's own JS entry
// (no shell, no npx, no PATH assumptions), args passed as an array so paths with
// spaces survive.

import { spawn } from "node:child_process";
import { readFileSync, writeFileSync, unlinkSync, mkdtempSync, existsSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { resolveFfmpeg, probeDurationSeconds } from "./ffmpeg.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.join(__dirname, "..");
const PUBLIC_DIR = path.join(PROJECT_ROOT, "public");
const ENTRY = "src/index.ts";
const CLI_JS = path.join(
  PROJECT_ROOT,
  "node_modules",
  "@remotion",
  "cli",
  "remotion-cli.js"
);

function fail(msg) {
  console.error(`\n[render] ${msg}\n`);
  process.exit(1);
}

// --- Parse argv --------------------------------------------------------------
// Positional: <CompId> <output>. Everything else is a flag; --props is special.
const argv = process.argv.slice(2);
const positionals = [];
let propsRaw = null;
const passthrough = [];
for (const arg of argv) {
  if (arg.startsWith("--props=")) {
    propsRaw = arg.slice("--props=".length);
  } else if (arg === "--props") {
    // `--props <value>` (space-separated) is not supported by our wrapper; the
    // Remotion convention we use is `--props=<value>`. Guide the caller.
    fail("use --props=<json-or-path>, not a space-separated --props value.");
  } else if (arg.startsWith("--")) {
    passthrough.push(arg);
  } else {
    positionals.push(arg);
  }
}

const [compId, outputPath] = positionals;
if (!compId || !outputPath) {
  fail(
    "usage: npm run render -- <CompId> <output.mp4> [--props=<json-or-path>] [flags]"
  );
}

// --- Resolve the plan --------------------------------------------------------
// A --props value is one of:
//   * a path to a .json file (a plan, or an object carrying scenesPath),
//   * an inline JSON string (a plan, or {"scenesPath": "..."}).
// Resolving {"scenesPath": "..."} means reading THAT file as the plan.
function readJson(p) {
  const abs = path.isAbsolute(p) ? p : path.join(PROJECT_ROOT, p);
  try {
    return JSON.parse(readFileSync(abs, "utf8"));
  } catch (e) {
    fail(`could not read/parse JSON at ${p}: ${e.message}`);
  }
}

function resolvePlan(raw) {
  if (raw == null) return null;
  let obj;
  const trimmed = raw.trim();
  if (trimmed.startsWith("{") || trimmed.startsWith("[")) {
    try {
      obj = JSON.parse(trimmed);
    } catch (e) {
      fail(`--props is not valid JSON: ${e.message}`);
    }
  } else {
    obj = readJson(trimmed);
  }
  // An object whose only meaningful key is scenesPath points at the real plan.
  if (obj && typeof obj === "object" && obj.scenesPath && !obj.scenes) {
    return readJson(obj.scenesPath);
  }
  return obj;
}

const plan = resolvePlan(propsRaw);

// Two plan shapes travel through this one wrapper:
//   * a FACELESS plan carries scenes[] (Mode A, the scenes.json renderer);
//   * an OVERLAY plan carries a `recording` (Mode B, talking-head compositing).
// A plan with neither is a mistake; guide the caller.
const isOverlay = !!(plan && plan.recording);
if (propsRaw && !isOverlay && (!plan || !Array.isArray(plan.scenes) || plan.scenes.length === 0)) {
  fail(
    "resolved plan has neither scenes[] (faceless) nor a recording (talking-head). " +
      "Point --props at a <slug>.scenes.json or an overlay plan."
  );
}

// --- Overlay: probe the recording's real length in Node, inject durationInFrames.
// `calculateMetadata` runs in a headless browser and cannot read the file off
// disk, so the duration must be resolved HERE and handed in as a prop (design
// spec §5.2). The recording path is relative to public/ (it is loaded via
// staticFile in the composition).
if (isOverlay) {
  const fps = typeof plan.fps === "number" ? plan.fps : 30;
  const recAbs = path.isAbsolute(plan.recording)
    ? plan.recording
    : path.join(PUBLIC_DIR, plan.recording);
  if (!existsSync(recAbs)) {
    fail(
      `overlay recording not found at ${recAbs}. ` +
        `Run \`npm run ingest -- <input> ${plan.slug || "<slug>"}\` first.`
    );
  }
  const { bin } = await resolveFfmpeg();
  const durS = bin ? probeDurationSeconds(bin, recAbs) : null;
  if (durS && durS > 0) {
    plan.durationInFrames = Math.round(durS * fps);
    console.log(
      `[render] recording is ${durS.toFixed(1)}s → ${plan.durationInFrames} frames @ ${fps}fps`
    );
  } else if (typeof plan.durationInFrames !== "number" || plan.durationInFrames <= 0) {
    // Never crash: fall back to a sane default so the render still completes.
    plan.durationInFrames = fps * 5;
    console.warn(
      "[render] could not probe the recording length; using a 5s fallback. " +
        "Install ffmpeg (npm install) so the clip length is exact."
    );
  }
}

// --- Build child args + a temp props file ------------------------------------
let tmpDir = null;
let tmpProps = null;
const childArgs = [CLI_JS, "render", ENTRY, compId, outputPath, ...passthrough];
if (plan) {
  tmpDir = mkdtempSync(path.join(tmpdir(), "bos-motion-"));
  tmpProps = path.join(tmpDir, "props.json");
  writeFileSync(tmpProps, JSON.stringify(plan), "utf8");
  childArgs.push(`--props=${tmpProps}`);
}

// --- <slug>.timing.json (written on success) ---------------------------------
// Same shape as studio/video (spec §3): { slug, fps, beats:[{id,start_s,end_s}] }.
// Keyed by each scene's script beat (beat_ref, falling back to the scene id) so
// package-my-video maps chapters to the script. Times are on the SAME compressed
// timeline the render uses: TransitionSeries overlaps each cut by transitionFrames,
// so the final beat's end_s equals the video's real duration (computeFacelessMeta),
// never past the end. The per-scene clamp mirrors facelessFactory's sceneFrames.
function writeTiming() {
  if (!plan) return;
  const fps = typeof plan.fps === "number" ? plan.fps : 30;

  // Overlay (talking-head): the timeline is the recording's real length. Emit a
  // single beat spanning the clip (the same {slug, fps, beats[]} shape as faceless
  // + studio/video), so package-my-video still gets a valid sidecar.
  if (isOverlay) {
    const durationInFrames =
      typeof plan.durationInFrames === "number" && plan.durationInFrames > 0
        ? plan.durationInFrames
        : fps * 5;
    const slugO = plan.slug || path.basename(outputPath, path.extname(outputPath));
    const outAbsO = path.isAbsolute(outputPath)
      ? outputPath
      : path.join(PROJECT_ROOT, outputPath);
    const timingPathO = path.join(path.dirname(outAbsO), `${slugO}.timing.json`);
    writeFileSync(
      timingPathO,
      JSON.stringify(
        {
          slug: slugO,
          fps,
          beats: [
            { id: "recording", start_s: 0, end_s: +(durationInFrames / fps).toFixed(3) },
          ],
        },
        null,
        2
      ) + "\n",
      "utf8"
    );
    console.log(`[render] wrote ${path.relative(PROJECT_ROOT, timingPathO)}`);
    return;
  }

  const transitionFrames =
    plan.transition && typeof plan.transition.duration_frames === "number"
      ? plan.transition.duration_frames
      : 12;
  const n = plan.scenes.length;
  let cursor = 0; // start frame of the current scene on the compressed timeline
  const beats = [];
  plan.scenes.forEach((scene, i) => {
    const frames = Math.max(
      Math.round((scene.duration_s ?? 0) * fps),
      transitionFrames + 1
    );
    const startFrame = cursor;
    const endFrame = cursor + frames;
    beats.push({
      id: scene.beat_ref || scene.id,
      start_s: +(startFrame / fps).toFixed(3),
      end_s: +(endFrame / fps).toFixed(3),
    });
    // The next scene overlaps this one by transitionFrames (TransitionSeries),
    // so it begins transitionFrames earlier than a naive cursor.
    cursor = endFrame - (i < n - 1 ? transitionFrames : 0);
  });
  const slug =
    plan.slug || path.basename(outputPath, path.extname(outputPath));
  const outAbs = path.isAbsolute(outputPath)
    ? outputPath
    : path.join(PROJECT_ROOT, outputPath);
  const timingPath = path.join(path.dirname(outAbs), `${slug}.timing.json`);
  writeFileSync(
    timingPath,
    JSON.stringify({ slug, fps, beats }, null, 2) + "\n",
    "utf8"
  );
  console.log(`[render] wrote ${path.relative(PROJECT_ROOT, timingPath)}`);
}

function cleanup() {
  if (tmpProps) {
    try {
      unlinkSync(tmpProps);
    } catch {}
  }
}

// --- Spawn the Remotion CLI --------------------------------------------------
const child = spawn(process.execPath, childArgs, {
  cwd: PROJECT_ROOT,
  stdio: "inherit",
});

child.on("close", (code) => {
  cleanup();
  if (code === 0) {
    writeTiming();
    console.log(`[render] done → ${outputPath}`);
  } else {
    console.error(`[render] Remotion exited with code ${code}`);
  }
  process.exit(code ?? 1);
});

child.on("error", (err) => {
  cleanup();
  fail(`could not launch Remotion CLI: ${err.message}`);
});
