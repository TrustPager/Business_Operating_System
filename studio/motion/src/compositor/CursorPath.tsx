// CursorPath — single cursor that travels through multiple targets in sequence.
// Used when chaining hover interactions. The cursor enters from off-screen,
// lands on the first stop, then slides directly between subsequent stops without
// leaving the frame. Use in place of multiple CursorHover instances when you want
// a single persistent mouse trail.
import React from "react";
import {useCurrentFrame, interpolate, Easing} from "remotion";

const FRAME_W = 1920;
const FRAME_H = 1080;
const easeInOut = Easing.inOut(Easing.quad);

const CursorSVG: React.FC<{size?: number}> = ({size = 40}) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    style={{
      filter:
        "drop-shadow(0 0 8px rgba(255,255,255,0.8)) drop-shadow(0 2px 6px rgba(0,0,0,0.5))",
    }}
  >
    <path
      d="M4 1L4 17.5L8.5 13.5L12.5 21L15.5 19.5L11.5 12L17 11.5L4 1Z"
      fill="#ffffff"
      stroke="#0f1117"
      strokeWidth="1.5"
      strokeLinejoin="round"
    />
  </svg>
);

export interface CursorPathStop {
  /** Target position (fractional 0..1). */
  to: {x: number; y: number};
  /** Frame at which the cursor finishes arriving at this stop. */
  arriveFrame: number;
}

export interface CursorPathProps {
  stops: CursorPathStop[];
  /** Frame at which the cursor first appears (offscreen) and starts flying in. */
  entryStartFrame: number;
  /** Frame at which the cursor begins fading out (after final stop). */
  exitStartFrame: number;
  /** Frame at which the cursor is fully gone. */
  exitDoneFrame: number;
  /** Cursor SVG size (px). Default 30. */
  size?: number;
  /** Pixel offset (from first stop) where the cursor enters from. Default {-340, 220}. */
  entryFromX?: number;
  entryFromY?: number;
  /** Frames before each arriveFrame the cursor starts moving from the previous stop. Default 30. */
  travelDuration?: number;
}

export const CursorPath: React.FC<CursorPathProps> = ({
  stops,
  entryStartFrame,
  exitStartFrame,
  exitDoneFrame,
  size = 30,
  entryFromX = -340,
  entryFromY = 220,
  travelDuration = 30,
}) => {
  const frame = useCurrentFrame();
  if (frame < entryStartFrame || frame > exitDoneFrame || stops.length === 0) return null;

  const ec = {extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const};
  const first = stops[0];

  let cx = 0;
  let cy = 0;
  let arc = 0;

  if (frame < first.arriveFrame) {
    const span = Math.max(1, first.arriveFrame - entryStartFrame);
    const t = (frame - entryStartFrame) / span;
    const eased = easeInOut(Math.max(0, Math.min(1, t)));
    cx = first.to.x * FRAME_W + entryFromX * (1 - eased);
    cy = first.to.y * FRAME_H + entryFromY * (1 - eased);
    arc = t > 0 && t < 1 ? Math.sin(t * Math.PI) * -36 : 0;
  } else {
    let placed = false;
    for (let i = 0; i < stops.length - 1; i++) {
      const cur = stops[i];
      const next = stops[i + 1];
      if (frame >= cur.arriveFrame && frame < next.arriveFrame) {
        const travelStart = next.arriveFrame - travelDuration;
        if (frame < travelStart) {
          cx = cur.to.x * FRAME_W;
          cy = cur.to.y * FRAME_H;
        } else {
          const t = (frame - travelStart) / travelDuration;
          const eased = easeInOut(Math.max(0, Math.min(1, t)));
          cx = (cur.to.x + (next.to.x - cur.to.x) * eased) * FRAME_W;
          cy = (cur.to.y + (next.to.y - cur.to.y) * eased) * FRAME_H;
        }
        placed = true;
        break;
      }
    }
    if (!placed) {
      const last = stops[stops.length - 1];
      cx = last.to.x * FRAME_W;
      cy = last.to.y * FRAME_H;
    }
  }

  const fadeIn = interpolate(frame, [entryStartFrame, entryStartFrame + 6], [0, 1], ec);
  const fadeOut = interpolate(frame, [exitStartFrame, exitDoneFrame], [1, 0], ec);
  const opacity = Math.min(fadeIn, fadeOut);

  return (
    <div
      style={{
        position: "absolute",
        left: cx - 4,
        top: cy + arc - 2,
        opacity,
        pointerEvents: "none",
        zIndex: 85,
      }}
    >
      <CursorSVG size={size} />
    </div>
  );
};
