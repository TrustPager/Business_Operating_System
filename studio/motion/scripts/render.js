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
import { readFileSync, writeFileSync, unlinkSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.join(__dirname, "..");
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
if (propsRaw && (!plan || !Array.isArray(plan.scenes) || plan.scenes.length === 0)) {
  fail(
    "resolved plan has no scenes[]. Point --props at a <slug>.scenes.json (or an object with scenesPath)."
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
// Same shape as studio/video (spec §3): { slug, fps, beats:[{id,start_s,end_s}] }.
// Keyed by each scene's script beat (beat_ref, falling back to the scene id) so
// package-my-video maps chapters to the script. Cumulative scene durations, the
// natural beat timeline (transition overlap is a render-time nicety, not a beat
// boundary), mirroring studio/video's non-overlapping timeline.
function writeTiming() {
  if (!plan) return;
  const fps = typeof plan.fps === "number" ? plan.fps : 30;
  let cursor = 0;
  const beats = [];
  for (const scene of plan.scenes) {
    const frames = Math.max(1, Math.round((scene.duration_s ?? 0) * fps));
    const startFrame = cursor;
    const endFrame = cursor + frames;
    beats.push({
      id: scene.beat_ref || scene.id,
      start_s: +(startFrame / fps).toFixed(3),
      end_s: +(endFrame / fps).toFixed(3),
    });
    cursor = endFrame;
  }
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
