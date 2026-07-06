#!/usr/bin/env node

// Headless Video Renderer (NET-NEW for the video studio).
//
// Unlike the still studios' render.js (a single-PNG screenshotter), this one
// implements the full MOTION pipeline (spec §5 Task 1.4 + Decision 4):
//
//   1. Load a <slug>.script.json (from data/ by slug, or an explicit path).
//   2. Build a per-beat timeline at a fixed fps via the shared src/timing.js
//      (the ONE place that owns the timing math, so the sidecar and the frame
//      loop can never drift). TIMING CONTRACT OWNER: spec §3.
//   3. FRAME-DRIVE INTERFACE: iterate frames 0..totalFrames DETERMINISTICALLY,
//      navigating the dev server with ?frame=N each step and screenshotting the
//      .video-canvas element. Never realtime/video capture — this is what makes
//      the render reproducible (the motion generalisation of the still studios).
//   4. Stitch the frames to an MP4 (H.264) + a preview GIF with ffmpeg.
//   5. AUDIO: the MP4 carries a SILENT STEREO audio track, so the Phase-2 voice
//      rung is a track REPLACEMENT/remux, not a container change (Decision 4).
//   6. Write <slug>.timing.json (spec §3 / Pin 1 shape) beside the video, keyed
//      by beat id, seconds as floats, array in render order. package-my-video
//      (Task 1.6) reads this exact shape.
//
// FFMPEG DECISION (Decision 4 leaves the arm to implementation):
//   Preferred arm: the npm-bundled `ffmpeg-static` binary, so the studio is
//   self-contained and keyless. Fallback arm (REQUIRED): if ffmpeg-static is not
//   installed/resolvable, shell a system `ffmpeg` on PATH. If NEITHER is
//   available, the render NEVER hard-fails silently: it keeps the captured frame
//   PNGs and the <slug>.timing.json, and prints a clear, positive keyless install
//   pointer so the owner is never blocked. Which arm shipped is recorded in the
//   README's ffmpeg note.
//
// Usage:
//   npm run dev                                  # start the dev server (port 3218, or $BOS_VIDEO_PORT)
//   npm run render -- <slug>                     # render data/<slug>.script.json
//   npm run render -- --script path/to.script.json   # render an explicit script
//   npm run render -- <slug> --no-gif            # skip the preview GIF

import puppeteer from 'puppeteer';
import { readFileSync, mkdirSync, writeFileSync, rmSync, renameSync, existsSync } from 'fs';
import { resolve, dirname, isAbsolute } from 'path';
import { fileURLToPath } from 'url';
import { spawnSync } from 'child_process';
import { buildTimeline, totalFrames, timingSidecar, FPS } from '../src/timing.js';
import { safeSlug, frameName } from './_filename.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = resolve(__dirname, '..');
const OUTPUT_DIR = resolve(PROJECT_ROOT, 'output');
const DATA_DIR = resolve(PROJECT_ROOT, 'data');
// Dev-server port defaults to 3218; override with BOS_VIDEO_PORT (the same var
// vite.config.js reads, so the server and the renderer stay on the same port).
const DEV_PORT = Number(process.env.BOS_VIDEO_PORT) || 3218;
const DEV_SERVER = `http://localhost:${DEV_PORT}`;

const args = process.argv.slice(2);
const noGif = args.includes('--no-gif');
const scriptFlagIdx = args.indexOf('--script');
let scriptPath = null;
let slugArg = null;
if (scriptFlagIdx !== -1) {
  scriptPath = args[scriptFlagIdx + 1];
} else {
  slugArg = args.find((a) => !a.startsWith('--'));
}

function resolveScriptPath() {
  if (scriptPath) return isAbsolute(scriptPath) ? scriptPath : resolve(process.cwd(), scriptPath);
  if (slugArg) return resolve(DATA_DIR, `${slugArg}.script.json`);
  return null;
}

// --- ffmpeg resolution: prefer ffmpeg-static, fall back to system ffmpeg. ---
async function resolveFfmpeg() {
  // Arm 1: the npm-bundled static binary (keyless, self-contained).
  try {
    const mod = await import('ffmpeg-static');
    const bin = mod.default || mod;
    if (bin && existsSync(bin)) return { bin, arm: 'ffmpeg-static' };
  } catch {
    // not installed — fall through to the system arm
  }
  // Arm 2: a system ffmpeg on PATH.
  const probe = spawnSync('ffmpeg', ['-version'], { encoding: 'utf8' });
  if (probe.status === 0) return { bin: 'ffmpeg', arm: 'system' };
  // Arm 3: none available — the caller keeps the frames + timing.json.
  return { bin: null, arm: 'none' };
}

function runFfmpeg(bin, ffArgs) {
  const res = spawnSync(bin, ffArgs, { stdio: 'inherit' });
  if (res.status !== 0) {
    throw new Error(`ffmpeg exited with code ${res.status}`);
  }
}

async function main() {
  const path = resolveScriptPath();
  if (!path || !existsSync(path)) {
    console.log('Usage:');
    console.log('  npm run render -- <slug>                 Render data/<slug>.script.json');
    console.log('  npm run render -- --script <path.json>   Render an explicit script file');
    console.log('');
    console.log('Available fixtures in data/:');
    try {
      const { readdirSync } = await import('fs');
      readdirSync(DATA_DIR)
        .filter((f) => f.endsWith('.script.json'))
        .forEach((f) => console.log(`  ${f.replace('.script.json', '')}`));
    } catch { /* no data dir */ }
    process.exit(path ? 1 : 0);
  }

  const script = JSON.parse(readFileSync(path, 'utf8'));
  const slug = safeSlug(script.slug || slugArg);
  const fps = FPS;
  const timeline = buildTimeline(script, fps);
  const frameCount = totalFrames(script, fps);

  if (frameCount <= 0) {
    console.error('Script has no renderable beats.');
    process.exit(1);
  }

  const outDir = resolve(OUTPUT_DIR, slug);
  const framesDir = resolve(outDir, 'frames');
  // Fresh frames dir each run so a shorter re-render never leaves stale frames.
  rmSync(framesDir, { recursive: true, force: true });
  mkdirSync(framesDir, { recursive: true });

  console.log(`Rendering "${slug}" — ${frameCount} frames @ ${fps}fps (${(frameCount / fps).toFixed(1)}s), ${timeline.length} beats.`);
  console.log(`Dev server: ${DEV_SERVER}`);

  // --- Capture the frames deterministically over ?frame=0..frameCount-1. ---
  const size = script?.meta?.aspect === '9:16'
    ? { width: 1080, height: 1920 }
    : { width: 1920, height: 1080 };

  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: size.width + 400, height: size.height + 300, deviceScaleFactor: 1 });

  // Navigate ONCE (with ?slug + ?frame=0), then drive frames in-page via
  // window.__setFrame(f) rather than reloading per frame. Determinism is
  // preserved: each frame is set explicitly and we wait for window.__renderedReq
  // to reach the request id __setFrame returned (App.jsx publishes it in a
  // useLayoutEffect the instant the frame's DOM is committed). This is the
  // documented ?frame=N interface exposed as a function so the capture loop does
  // not pay a full page reload each step.
  const startUrl = `${DEV_SERVER}/?frame=0&slug=${encodeURIComponent(slug)}`;
  // Watch the logo request so a missing /logo.png can never fail silently: if it
  // 404s, the frames still render (the <img> just shows nothing) but we WARN so
  // the owner knows to run `python tools/sync-brand.py`. Never fails the render.
  page.on('response', (res) => {
    const url = res.url();
    if (url.endsWith('/logo.png') && res.status() === 404) {
      console.warn(
        `  WARNING: ${url} returned 404 — the brand logo will not paint. ` +
        'Run `python tools/sync-brand.py` from the BOS root to populate studio/video/public/.'
      );
    }
  });
  await page.goto(startUrl, { waitUntil: 'networkidle0', timeout: 20000 });
  await page.waitForSelector('.video-canvas', { timeout: 10000 });
  await page.waitForFunction('typeof window.__setFrame === "function"', { timeout: 10000 });
  await page.evaluate((s) => window.__selectSlug && window.__selectSlug(s), slug);

  // Pin the canvas to the top-left at its TRUE native size so we can screenshot a
  // fixed clip rect every frame (a fixed clip is far faster than re-resolving an
  // element handle + bounding box per frame). Neutralise the editor's
  // fit-to-window scale and lift the canvas out of the scaled preview wrapper.
  await page.evaluate(() => {
    const c = document.querySelector('.video-canvas');
    if (!c) return;
    const inner = c.parentElement;
    if (inner) { inner.style.transform = 'none'; inner.style.transformOrigin = 'top left'; }
    const outer = inner && inner.parentElement;
    if (outer) { outer.style.width = 'auto'; outer.style.height = 'auto'; outer.style.overflow = 'visible'; }
    // Fix the canvas to the viewport origin so clip {x:0,y:0,w,h} always lands on it.
    c.style.position = 'fixed';
    c.style.top = '0';
    c.style.left = '0';
    c.style.zIndex = '99999';
  });
  // Wait for web fonts ONCE before the first capture (not per frame), so the
  // serif on-screen text renders in the brand font from frame 0.
  await page.evaluate(() => (document.fonts ? document.fonts.ready : Promise.resolve()));

  const clip = { x: 0, y: 0, width: size.width, height: size.height };
  for (let f = 0; f < frameCount; f++) {
    // Request the frame; __setFrame returns a monotonic request id.
    const reqId = await page.evaluate((n) => window.__setFrame(n), f);
    // Wait until App.jsx signals THAT request has committed (deterministic
    // barrier — see the barrier design note in App.jsx).
    await page.waitForFunction((id) => window.__renderedReq === id, { timeout: 15000 }, reqId);

    const framePath = resolve(framesDir, frameName(f));
    await page.screenshot({
      path: framePath,
      type: 'png',
      clip,
      captureBeyondViewport: false,
      optimizeForSpeed: true,
    });
    if (f % 60 === 0 || f === frameCount - 1) {
      process.stdout.write(`\r  captured ${f + 1}/${frameCount} frames`);
    }
  }
  process.stdout.write('\n');
  await browser.close();

  // --- Write the timing sidecar (spec §3 / Pin 1) BEFORE stitching, so it is
  //     always produced even if ffmpeg is unavailable. ---
  const timing = timingSidecar(script, fps);
  const timingPath = resolve(outDir, `${slug}.timing.json`);
  writeFileSync(timingPath, JSON.stringify(timing, null, 2) + '\n', 'utf8');
  console.log(`  timing sidecar: ${timingPath}`);

  // --- Stitch to MP4 (+ GIF) with a silent stereo audio track. ---
  const { bin, arm } = await resolveFfmpeg();
  const mp4Path = resolve(outDir, `${slug}.mp4`);
  const gifPath = resolve(outDir, `${slug}.gif`);
  const framePattern = resolve(framesDir, 'frame-%06d.png');

  if (!bin) {
    // Keyless fallback: never hard-fail silently. Keep the frames + timing.json
    // and point the owner at a one-line, positive install path.
    console.log('');
    console.log('The frames and timing sidecar are ready. To stitch them into an MP4,');
    console.log('install ffmpeg once and re-run this render:');
    console.log('');
    console.log('  npm install            # brings in the bundled ffmpeg-static, no account needed');
    console.log('  # or install a system ffmpeg from https://ffmpeg.org/download.html');
    console.log('');
    console.log(`Frames: ${framesDir}`);
    console.log(`Timing: ${timingPath}`);
    return;
  }

  console.log(`  stitching with ffmpeg (${arm})...`);
  // MP4: H.264 video from the frame sequence + a silent STEREO audio track
  // (anullsrc, 2 channels). The -shortest flag trims the generated silence to the
  // video length. yuv420p keeps it broadly playable.
  //
  // ATOMIC WRITE: stitch to <slug>.part.mp4, then rename to <slug>.mp4 only after
  // ffmpeg returns 0. A mid-stitch failure therefore never leaves a truncated MP4
  // beside the valid timing.json — on error we unlink the partial and rethrow.
  // The temp name keeps the .mp4 extension (not <slug>.mp4.part) because ffmpeg
  // infers the output container from the extension; a .part suffix has no muxer.
  const mp4PartPath = resolve(outDir, `${slug}.part.mp4`);
  try {
    runFfmpeg(bin, [
      '-y',
      '-framerate', String(fps),
      '-i', framePattern,
      '-f', 'lavfi',
      '-i', 'anullsrc=channel_layout=stereo:sample_rate=48000',
      '-c:v', 'libx264',
      '-pix_fmt', 'yuv420p',
      '-c:a', 'aac',
      '-shortest',
      mp4PartPath,
    ]);
  } catch (err) {
    // Clean up the partial so no corrupt MP4 is ever left behind, then rethrow
    // (a failed MP4 IS a failed render; only the GIF is best-effort below).
    rmSync(mp4PartPath, { force: true });
    throw err;
  }
  renameSync(mp4PartPath, mp4Path);
  console.log(`  video: ${mp4Path}  (silent stereo audio track)`);

  if (!noGif) {
    // A lightweight preview GIF at a reduced rate/scale. The GIF is a PREVIEW
    // extra: the MP4 + timing.json are already complete, so a GIF-stitch failure
    // must NOT fail the whole run. Isolate it in its own try/catch and stay green.
    try {
      runFfmpeg(bin, [
        '-y',
        '-framerate', String(fps),
        '-i', framePattern,
        '-vf', 'fps=15,scale=640:-1:flags=lanczos',
        gifPath,
      ]);
      console.log(`  gif:   ${gifPath}`);
    } catch (err) {
      console.log(`  The MP4 and timing.json are ready; the preview GIF could not be generated (${err.message}).`);
    }
  }

  console.log('Done.');
}

main().catch((err) => {
  console.error('Render failed:', err);
  process.exit(1);
});
