// ffmpeg.js — the shared ffmpeg resolver + probe for the motion studio.
//
// This is the SAME three-arm resolution the video studio uses
// (studio/video/scripts/render.js): the bundled `ffmpeg-static` binary is
// preferred (keyless, self-contained), a system `ffmpeg` on PATH is the
// fallback, and if NEITHER is available the caller gets `{bin:null}` and prints a
// positive install pointer — never a hard-fail. Both ingest.js (normalise a
// recording) and render.js (probe a recording's real duration for the Overlay
// composition's calculateMetadata) share it, so the resolution lives in one place.

import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";

/**
 * Resolve an ffmpeg binary, in order:
 *   1. `ffmpeg-static` (bundled npm binary — keyless, self-contained).
 *   2. a system `ffmpeg` on PATH.
 *   3. neither → { bin: null } (the caller degrades gracefully; never crashes).
 */
export async function resolveFfmpeg() {
  // Arm 1: the npm-bundled static binary.
  try {
    const mod = await import("ffmpeg-static");
    const bin = mod.default || mod;
    if (bin && existsSync(bin)) return { bin, arm: "ffmpeg-static" };
  } catch {
    // not installed — fall through to the system arm
  }
  // Arm 2: a system ffmpeg on PATH.
  const probe = spawnSync("ffmpeg", ["-version"], { encoding: "utf8" });
  if (probe.status === 0) return { bin: "ffmpeg", arm: "system" };
  // Arm 3: none available.
  return { bin: null, arm: "none" };
}

/**
 * Probe a media file's duration in seconds by parsing ffmpeg's own stderr
 * banner (`Duration: HH:MM:SS.ms`). This needs only `ffmpeg` (not `ffprobe`,
 * which ffmpeg-static does not bundle), so it works keyless off the resolver
 * above. `ffmpeg -i <file>` with no output map exits non-zero by design, so we
 * read stderr regardless of exit code. Returns null if the banner is unreadable.
 */
export function probeDurationSeconds(bin, file) {
  const res = spawnSync(bin, ["-i", file], { encoding: "utf8" });
  const out = (res.stderr || "") + (res.stdout || "");
  const m = out.match(/Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)/);
  if (!m) return null;
  return Number(m[1]) * 3600 + Number(m[2]) * 60 + parseFloat(m[3]);
}

/** Probe a video stream's pixel dimensions (post-rotation display size). */
export function probeDimensions(bin, file) {
  const res = spawnSync(bin, ["-i", file], { encoding: "utf8" });
  const out = (res.stderr || "") + (res.stdout || "");
  // e.g. "Stream #0:0 ... 1080x1920 [SAR 1:1 DAR 9:16] ..."
  const m = out.match(/,\s*(\d{2,5})x(\d{2,5})/);
  if (!m) return null;
  return { width: Number(m[1]), height: Number(m[2]) };
}
