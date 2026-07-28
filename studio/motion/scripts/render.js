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
// the shape spec §3 defines), so `package-my-video` gets chapters.
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
let alphaMode = null; // null | "prores" | "vp9" — the ADVANCED transparent-export door
const passthrough = [];
for (const arg of argv) {
  if (arg.startsWith("--props=")) {
    propsRaw = arg.slice("--props=".length);
  } else if (arg === "--props") {
    // `--props <value>` (space-separated) is not supported by our wrapper; the
    // Remotion convention we use is `--props=<value>`. Guide the caller.
    fail("use --props=<json-or-path>, not a space-separated --props value.");
  } else if (arg === "--alpha" || arg.startsWith("--alpha=")) {
    // The "hand this to my video editor" escape hatch (design spec §5.4). NOT on
    // the default path — it swaps to a transparent-canvas render. `--alpha` (or
    // `--alpha=prores`) => ProRes 4444 .mov; `--alpha=vp9`/`--alpha=webm` => WebM
    // VP9. We intercept it here so Remotion never sees an unknown flag; the real
    // codec/pixel-format flags are injected below.
    const v = arg.includes("=") ? arg.slice("--alpha=".length).toLowerCase() : "prores";
    if (v === "" || v === "prores" || v === "mov") alphaMode = "prores";
    else if (v === "vp9" || v === "webm") alphaMode = "vp9";
    else fail(`--alpha value must be prores or vp9 (got "${v}")`);
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

// Three plan shapes travel through this one wrapper:
//   * a FACELESS plan carries scenes[] (Mode A, the scenes.json renderer);
//   * an OVERLAY plan carries a `recording` (Mode B, talking-head compositing);
//   * a PRODUCT-DEMO plan carries beats[] (Mode C add-on, "watch it get built").
// A plan with none of these is a mistake; guide the caller.
const isOverlay = !!(plan && plan.recording);
const isProductDemo = !!(plan && Array.isArray(plan.beats));
if (
  propsRaw &&
  !isOverlay &&
  !isProductDemo &&
  (!plan || !Array.isArray(plan.scenes) || plan.scenes.length === 0)
) {
  fail(
    "resolved plan has none of scenes[] (faceless), a recording (talking-head), " +
      "or beats[] (product-demo). Point --props at a valid plan."
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

// --- Faceless: inline the per-beat voice manifest (spec §6, the VOICE rung) ----
// A faceless plan opts into voiceover by carrying `voice` (a dir hint like
// "audio/<slug>", written by voice-my-video). The composition runs in a headless
// browser and cannot read a file off disk, so — exactly like the overlay duration
// probe above — we read data/<slug>.voice.json HERE in Node and inline it as
// { dir, beats } on the plan. Silent-by-default: no `voice` key, or a missing
// manifest, renders exactly as before (the keyless floor), never a hard-fail.
if (!isOverlay && plan && Array.isArray(plan.scenes) && plan.voice) {
  const slugV =
    plan.slug || path.basename(outputPath, path.extname(outputPath));
  const already =
    typeof plan.voice === "object" && Array.isArray(plan.voice.beats);
  if (!already) {
    const voicePath = path.join(PROJECT_ROOT, "data", `${slugV}.voice.json`);
    if (existsSync(voicePath)) {
      try {
        const manifest = JSON.parse(readFileSync(voicePath, "utf8"));
        const dir =
          (typeof plan.voice === "string" ? plan.voice : manifest.dir) ||
          `audio/${slugV}`;
        const beats = Array.isArray(manifest.beats) ? manifest.beats : [];
        plan.voice = { dir, beats };
        console.log(
          `[render] voiceover: layering ${beats.length} beat MP3s from ${dir}/ ` +
            `(${manifest.provider || "unknown provider"})`
        );
      } catch (e) {
        plan.voice = null;
        console.warn(
          `[render] could not read the voice manifest (${e.message}); ` +
            "rendering silent + captions."
        );
      }
    } else {
      plan.voice = null;
      console.warn(
        `[render] no voice manifest at data/${slugV}.voice.json; ` +
          "rendering silent + captions. Run `npm run voice -- " +
          slugV +
          "` to add a voiceover."
      );
    }
  }
}

// --- Alpha / transparent-overlay export (ADVANCED door, design spec §5.4) -----
// Off the default path. When --alpha is set we (a) mark the plan `transparent`
// so the composition drops its solid background (a solid background-color kills
// alpha), and (b) inject the codec + pixel-format flags that carry an alpha plane.
// These override the h264/yuv420p defaults from remotion.config.ts.
if (alphaMode) {
  if (plan && typeof plan === "object") {
    plan.transparent = true;
  }
  const outExt = path.extname(outputPath).toLowerCase();
  if (alphaMode === "prores") {
    passthrough.push(
      "--codec=prores",
      "--prores-profile=4444",
      "--pixel-format=yuva444p10le",
      "--image-format=png"
    );
    if (outExt !== ".mov") {
      console.warn(
        `[render] --alpha (ProRes 4444) writes a QuickTime stream; name the output .mov (got ${outExt || "no extension"}).`
      );
    }
  } else {
    passthrough.push("--codec=vp9", "--pixel-format=yuva420p");
    if (outExt !== ".webm") {
      console.warn(
        `[render] --alpha=vp9 writes a WebM stream; name the output .webm (got ${outExt || "no extension"}).`
      );
    }
  }
  console.log(
    `[render] ALPHA export (${alphaMode}): transparent canvas, alpha-carrying codec. ` +
      "This is the hand-to-your-editor path, not the default render."
  );
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
// The spec §3 shape: { slug, fps, beats:[{id,start_s,end_s}] }.
// Keyed by each scene's script beat (beat_ref, falling back to the scene id) so
// package-my-video maps chapters to the script. Times are on the SAME compressed
// timeline the render uses: TransitionSeries overlaps each cut by transitionFrames,
// so the final beat's end_s equals the video's real duration (computeFacelessMeta),
// never past the end. The per-scene clamp mirrors facelessFactory's sceneFrames.
function writeTiming() {
  if (!plan) return;
  const fps = typeof plan.fps === "number" ? plan.fps : 30;

  // Overlay (talking-head): the timeline is the recording's real length. Emit a
  // single beat spanning the clip (the same {slug, fps, beats[]} shape as faceless),
  // so package-my-video still gets a valid sidecar.
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

  // Product-demo (Mode C): beats laid end to end, no transition overlap. Emit the
  // same {slug, fps, beats[]} sidecar so package-my-video still gets chapters.
  if (isProductDemo) {
    const slugP = plan.slug || path.basename(outputPath, path.extname(outputPath));
    const outAbsP = path.isAbsolute(outputPath)
      ? outputPath
      : path.join(PROJECT_ROOT, outputPath);
    const timingPathP = path.join(path.dirname(outAbsP), `${slugP}.timing.json`);
    let cursorP = 0;
    const beatsP = [];
    for (const b of plan.beats) {
      const frames = Math.max(Math.round((b.duration_s ?? 0) * fps), 1);
      const startFrame = cursorP;
      const endFrame = cursorP + frames;
      beatsP.push({
        id: b.id || `beat-${beatsP.length}`,
        start_s: +(startFrame / fps).toFixed(3),
        end_s: +(endFrame / fps).toFixed(3),
      });
      cursorP = endFrame;
    }
    writeFileSync(
      timingPathP,
      JSON.stringify({ slug: slugP, fps, beats: beatsP }, null, 2) + "\n",
      "utf8"
    );
    console.log(`[render] wrote ${path.relative(PROJECT_ROOT, timingPathP)}`);
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
  // Signal remotion.config.ts to skip the h264-only CRF setting on the alpha
  // path (ProRes rejects --crf); the alpha render carries quality via its profile.
  env: alphaMode ? { ...process.env, BOS_ALPHA_EXPORT: alphaMode } : process.env,
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
