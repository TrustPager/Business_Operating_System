// VideoBeats — THE video studio template.
//
// It renders ONE frame of a beat-structured video: given a <slug>.script.json
// and a global frame index N, it shows the beat that frame falls in, with the
// beat's `on_screen` text as branded text-on-screen motion graphics. This is the
// motion generalisation of the four still studios (Decision 4): instead of one
// static PNG, the same brand.json-driven React composition is captured at every
// frame across the timeline.
//
// FRAME-DRIVE INTERFACE (spec §5 Task 1.4 + Decision 4 is the owner):
//   The frame is read from the URL query param ?frame=N. scripts/render.js sets
//   ?frame=0, ?frame=1, ... deterministically over 0..duration*fps and captures
//   each. Animation is resolved AT a frame (never realtime) — the same idea as
//   studio/thumbnails/src/remotion-shim.jsx's "resolve animations at a frame".
//   Progress within a beat drives a deterministic fade/slide-in, so the motion is
//   reproducible: the same frame always paints identically.
//
// All colour flows from brand.json via src/brand.js. No hex literals here, and no
// TrustPager (or any owner-specific) literals — the copy is the script's, the
// palette is the owner's.

import React, { useMemo } from 'react';
import { buildTimeline, beatAtFrame, FPS } from '../timing.js';
import {
  NAME, GRADIENT, HERO_GRADIENT,
  PRIMARY, PRIMARY_DEEP, ACCENT, LIGHT, SLATE,
  TEXT, PANEL, CANVAS_BG,
  FONT_BODY, FONT_SERIF, LOGO_URL,
} from '../brand.js';

// Canvas sizes, one per aspect the script's meta.aspect can request.
const SIZES = {
  '16:9': { width: 1920, height: 1080 },
  '9:16': { width: 1080, height: 1920 },
};

export function sizeForAspect(aspect) {
  return SIZES[aspect] || SIZES['16:9'];
}

// A small deterministic ease for the intro of each beat: 0 at the beat's first
// frame, 1 after `rampFrames`. Pure function of frame position — reproducible.
function introProgress(framesIntoBeat, rampFrames) {
  if (rampFrames <= 0) return 1;
  const t = Math.min(1, Math.max(0, framesIntoBeat / rampFrames));
  // easeOutCubic
  return 1 - Math.pow(1 - t, 3);
}

// Human-friendly label for the beat role, shown as a small eyebrow.
// Only roles whose label is not simply their capitalised name need an entry here.
const ROLE_LABEL = {
  cta: 'Call to action',
};

/**
 * Label for any beat role, including one this studio has never heard of.
 *
 * The role set lives in the script schema (spec section 3 of
 * docs/architecture/2026-07-05-youtube-studio-design.md) and grows there:
 * `subscribe` was added on 2026-07-26, and a hardcoded map meant an unknown role
 * rendered a blank eyebrow until someone remembered to update this file. Deriving
 * the label removes that whole class of drift, so a role added tomorrow renders
 * sensibly here with no change.
 */
function roleLabelFor(role) {
  if (!role) return '';
  if (ROLE_LABEL[role]) return ROLE_LABEL[role];
  return String(role)
    .replace(/[-_]+/g, ' ')
    .replace(/^\s*(\w)/, (_, c) => c.toUpperCase());
}

/**
 * @param {object} props
 * @param {object} props.script  a parsed <slug>.script.json
 * @param {number} props.frame   the global frame index (from ?frame=N)
 * @param {number} [props.fps]   frames per second (defaults to the studio FPS)
 */
export function VideoBeats({ script, frame = 0, fps = FPS }) {
  const aspect = script?.meta?.aspect || '16:9';
  const size = sizeForAspect(aspect);
  // Memoise the timeline on [script, fps] (mirrors App.jsx) so it isn't rebuilt on
  // every frame during a render. The timing math + single source of truth stays in
  // timing.js — this only caches the result, it does not change it.
  const timeline = useMemo(() => buildTimeline(script, fps), [script, fps]);
  const active = beatAtFrame(timeline, frame);

  const framesIntoBeat = active ? Math.max(0, frame - active.startFrame) : 0;
  const rampFrames = Math.round(fps * 0.5); // half-second intro ramp
  const p = introProgress(framesIntoBeat, rampFrames);

  const isCta = active?.role === 'cta';
  const onScreen = active?.on_screen || '';
  const roleLabel = roleLabelFor(active?.role);

  // Beat counter (e.g. 3 / 8) so the scrubber and render both read as a timeline.
  const total = timeline.length;
  const index = active ? timeline.findIndex((t) => t === active) + 1 : 0;

  return (
    <div
      className="video-canvas"
      style={{
        width: size.width,
        height: size.height,
        position: 'relative',
        overflow: 'hidden',
        background: CANVAS_BG,
        fontFamily: FONT_BODY,
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {/* Soft brand colour blooms behind the text, masked to the corners. */}
      <div style={{
        position: 'absolute', inset: 0,
        backgroundImage:
          `radial-gradient(circle at 15% 12%, ${PRIMARY}22, transparent 42%),` +
          `radial-gradient(circle at 85% 88%, ${ACCENT}22, transparent 42%)`,
        pointerEvents: 'none',
      }} />

      {/* Top bar: logo + role eyebrow. */}
      <div style={{
        position: 'relative',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        padding: `${Math.round(size.height * 0.055)}px ${Math.round(size.width * 0.06)}px`,
      }}>
        <img src={LOGO_URL} alt={NAME} style={{ height: Math.round(size.height * 0.05), width: 'auto', display: 'block' }} />
        {roleLabel && (
          <span style={{
            fontSize: Math.round(size.height * 0.022),
            fontWeight: 700, letterSpacing: '0.14em', textTransform: 'uppercase',
            color: PRIMARY_DEEP,
            opacity: 0.55,
          }}>
            {roleLabel}
          </span>
        )}
      </div>

      {/* Centre: the on-screen line, faded/slid in by the deterministic ramp. */}
      <div style={{
        position: 'relative',
        flex: 1,
        display: 'flex', flexDirection: 'column',
        alignItems: 'center', justifyContent: 'center',
        padding: `0 ${Math.round(size.width * 0.09)}px`,
        textAlign: 'center',
      }}>
        <div style={{
          opacity: p,
          transform: `translateY(${(1 - p) * (size.height * 0.03)}px)`,
        }}>
          <div style={{
            fontFamily: FONT_SERIF,
            fontWeight: 700,
            lineHeight: 1.08,
            letterSpacing: '-0.01em',
            fontSize: Math.round(size.width * (aspect === '9:16' ? 0.075 : 0.058)),
            // The CTA beat gets the brand gradient fill; other beats stay in the
            // solid brand text colour so the ask is the visual peak.
            ...(isCta
              ? {
                  backgroundImage: HERO_GRADIENT,
                  WebkitBackgroundClip: 'text',
                  backgroundClip: 'text',
                  color: 'transparent',
                }
              : { color: TEXT }),
          }}>
            {onScreen}
          </div>
        </div>
      </div>

      {/* Footer: a progress rail + beat counter, so the timeline is legible. */}
      <div style={{
        position: 'relative',
        padding: `${Math.round(size.height * 0.045)}px ${Math.round(size.width * 0.06)}px`,
        display: 'flex', alignItems: 'center', gap: Math.round(size.width * 0.02),
      }}>
        <div style={{
          flex: 1, height: Math.max(4, Math.round(size.height * 0.006)),
          borderRadius: 999, background: LIGHT, overflow: 'hidden',
        }}>
          <div style={{
            height: '100%',
            width: `${total ? (index / total) * 100 : 0}%`,
            background: GRADIENT,
            borderRadius: 999,
          }} />
        </div>
        <span style={{
          fontSize: Math.round(size.height * 0.02),
          fontWeight: 600, color: SLATE, fontVariantNumeric: 'tabular-nums',
          whiteSpace: 'nowrap',
        }}>
          {index} / {total}
        </span>
      </div>
    </div>
  );
}

// Studio metadata mirrored from the still studios' templateMeta convention. The
// render size is resolved per-script from meta.aspect (sizeForAspect), so the
// default here is the 16:9 canvas.
VideoBeats.templateMeta = {
  id: 'video-beats',
  name: 'Text-on-screen video',
  size: SIZES['16:9'],
  sizes: SIZES,
};

export default VideoBeats;
