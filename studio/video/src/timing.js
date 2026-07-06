// Shared timing math for the video studio.
//
// This is the ONE place that turns a <slug>.script.json into a per-beat
// timeline (start_s / end_s per beat) at a fixed fps. Both surfaces read it so
// they can never drift:
//   - the template (VideoBeats.jsx) uses it to decide which beat a given frame
//     falls in, so ?frame=N shows the right beat;
//   - scripts/render.js uses it to know how many frames to capture and to write
//     the <slug>.timing.json sidecar.
//
// TIMING CONTRACT OWNER: spec §3 of docs/architecture/2026-07-05-youtube-studio-design.md
// ("the script is the spec"). The *planned* per-beat duration is the beat's
// duration_s when present, else it is computed from the spoken word count at the
// words-per-minute the script used (script-my-video states 150 wpm; we default to
// the same so a script that omitted duration_s still renders to a sane length).
// script-my-video writes the planned duration_s; studio/video writes the ACTUAL
// rendered per-beat times to <slug>.timing.json after the frame loop. Because the
// floor render is deterministic (no realtime drift), the actual times equal the
// planned windows quantised to the frame grid — see render.js.
//
// This module is framework-free ESM so Node (render.js) and the browser
// (VideoBeats.jsx) both import it unchanged.

// Studio constant. 30 fps is the floor default; a script never sets fps (fps is
// a render property, not a script property), so it lives here.
export const FPS = 30;

// The words-per-minute fallback, matching skills/script-my-video (150 wpm). Only
// used when a beat is missing an explicit duration_s. Kept in step with the
// script-my-video skill body so planned == rendered length for a fixture script.
export const DEFAULT_WPM = 150;

// A floor so a beat with almost no spoken text still gets a readable on-screen
// moment. Applied only to the word-count fallback, never to an explicit
// duration_s (the script author's intent wins).
const MIN_BEAT_S = 1.5;

function wordCount(str) {
  if (!str || typeof str !== 'string') return 0;
  return str.trim().split(/\s+/).filter(Boolean).length;
}

// The PLANNED duration of one beat in seconds. Explicit duration_s wins; else
// spoken word count / wpm * 60, floored so it stays readable.
export function plannedBeatSeconds(beat, wpm = DEFAULT_WPM) {
  if (beat && typeof beat.duration_s === 'number' && beat.duration_s > 0) {
    return beat.duration_s;
  }
  const words = wordCount(beat && beat.spoken);
  const s = (words / wpm) * 60;
  return Math.max(s, MIN_BEAT_S);
}

// Turn a script's beats into a timeline. Returns an array in render order, each:
//   { id, role, on_screen, start_s, end_s, startFrame, endFrame }
// where [startFrame, endFrame) is a half-open frame window at `fps`.
// start_s / end_s are the ACTUAL rendered seconds: because stepping is
// deterministic on the frame grid, they are the frame boundaries converted back
// to seconds (frame / fps), which is exactly what render.js captured. This is the
// shape <slug>.timing.json is keyed on (spec §3 timing contract).
export function buildTimeline(script, fps = FPS, wpm = DEFAULT_WPM) {
  const beats = (script && Array.isArray(script.beats)) ? script.beats : [];
  const timeline = [];
  let cursorFrame = 0;
  for (const beat of beats) {
    const planned = plannedBeatSeconds(beat, wpm);
    // Quantise the planned duration to whole frames (at least 1 frame) so the
    // capture loop and the timing sidecar agree to the frame.
    const frames = Math.max(1, Math.round(planned * fps));
    const startFrame = cursorFrame;
    const endFrame = cursorFrame + frames;
    timeline.push({
      id: beat.id,
      role: beat.role,
      on_screen: beat.on_screen,
      start_s: +(startFrame / fps).toFixed(3),
      end_s: +(endFrame / fps).toFixed(3),
      startFrame,
      endFrame,
    });
    cursorFrame = endFrame;
  }
  return timeline;
}

// Total frame count for a script at `fps` (the render loop iterates 0..this).
export function totalFrames(script, fps = FPS, wpm = DEFAULT_WPM) {
  const timeline = buildTimeline(script, fps, wpm);
  return timeline.length ? timeline[timeline.length - 1].endFrame : 0;
}

// Which timeline entry a given global frame falls in (or null past the end).
export function beatAtFrame(timeline, frame) {
  for (const t of timeline) {
    if (frame >= t.startFrame && frame < t.endFrame) return t;
  }
  // Clamp to the last beat on the final frame so the closing card holds.
  return timeline.length ? timeline[timeline.length - 1] : null;
}

// The <slug>.timing.json payload (spec §3 / Pin 1 shape): keyed by beat id,
// seconds as floats, array in render order.
export function timingSidecar(script, fps = FPS, wpm = DEFAULT_WPM) {
  const timeline = buildTimeline(script, fps, wpm);
  return {
    slug: script && script.slug,
    fps,
    beats: timeline.map((t) => ({
      id: t.id,
      start_s: t.start_s,
      end_s: t.end_s,
    })),
  };
}
