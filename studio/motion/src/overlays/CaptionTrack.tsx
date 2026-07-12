// CaptionTrack — the talking-head caption renderer.
//
// Drives off useCurrentFrame(): given a Caption[] (the exact shape
// @remotion/install-whisper-cpp's toCaptions() emits, and what scripts/caption.js
// writes), it shows the caption active at the current time as a phone-legible
// lower band. Colour + type flow from the brand token bridge; there is NO hex
// literal here beyond neutral black/white scrim values.
//
// Captions are DATA (studio CLAUDE.md §5): sized for a phone (~110-150px cap on a
// 1920-tall portrait comp), one line at a time, high-contrast scrim so it stays
// legible over any footage. Timing is in milliseconds so it maps 1:1 to whisper
// output; we convert to the current frame's millisecond position via fps.
import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, AbsoluteFill } from "remotion";
import { text as brandText } from "../tokens";
import { FONT_BODY } from "../fonts";

// The @remotion/captions / toCaptions() Caption shape (inlined so we do not add a
// dependency just for a 4-field type).
export interface Caption {
  text: string;
  startMs: number;
  endMs: number;
  timestampMs?: number | null;
  confidence?: number | null;
}

export interface CaptionTrackProps {
  captions?: Caption[];
  // Vertical anchor of the caption band, 0..1 of frame height (default low third).
  y?: number;
  // Cap font size in px on the reference 1920-tall comp; scaled to the real comp.
  fontSizePx?: number;
}

export const CaptionTrack: React.FC<CaptionTrackProps> = ({
  captions = [],
  y = 0.82,
  fontSizePx = 64,
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  if (!captions || captions.length === 0) return null;

  const nowMs = (frame / fps) * 1000;
  // The active caption is the last one whose window contains `nowMs`.
  const active = captions.find((c) => nowMs >= c.startMs && nowMs < c.endMs);
  if (!active || !active.text || !active.text.trim()) return null;

  // Scale the cap size to the real comp height (reference is a 1920-tall frame).
  const scale = height / 1920;
  const fontSize = fontSizePx * scale;

  // Short fade in/out at the caption's own edges (150ms), never a hard pop.
  const fadeMs = 150;
  const opacity = interpolate(
    nowMs,
    [active.startMs, active.startMs + fadeMs, active.endMs - fadeMs, active.endMs],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div
        style={{
          position: "absolute",
          left: "50%",
          top: y * height,
          transform: "translate(-50%, -50%)",
          maxWidth: width * 0.86,
          textAlign: "center",
          background: "rgba(0,0,0,0.62)",
          color: "#ffffff",
          borderRadius: 12 * scale,
          padding: `${14 * scale}px ${28 * scale}px`,
          fontFamily: FONT_BODY,
          fontSize,
          fontWeight: 700,
          lineHeight: 1.15,
          letterSpacing: "-0.01em",
          opacity,
          // A subtle brand-tinted underline keeps captions on-brand without
          // baking a colour literal (brandText is the owner's text token).
          borderBottom: `${3 * scale}px solid ${brandText}`,
          textShadow: "0 2px 8px rgba(0,0,0,0.45)",
          whiteSpace: "pre-wrap",
        }}
      >
        {active.text.trim()}
      </div>
    </AbsoluteFill>
  );
};
