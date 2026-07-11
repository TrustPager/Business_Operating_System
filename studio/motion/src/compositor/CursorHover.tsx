// CursorHover — mouse cursor flies in to a target position and holds there.
// Unlike CursorClick, there is no click ripple or highlight ring — purely a
// hovering cursor used to indicate the user is pointing at a UI element
// (e.g., to trigger a hover-state animation like a tooltip or popover).
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

export interface CursorHoverProps {
  /** Target position (proportional 0..1). Cursor lands here. */
  to: {x: number; y: number};
  /** Frame at which the cursor first appears (offscreen) and begins moving. */
  appearFrame: number;
  /** Frame at which the cursor reaches the target (lands). */
  landsAtFrame: number;
  /** Frame at which the cursor begins fading out. */
  fadeOutFrame: number;
  /** Frame at which the cursor is fully gone. */
  disappearFrame: number;
  /** Pixel offset from target where the cursor starts. */
  cursorFromX?: number;
  cursorFromY?: number;
  /** Cursor SVG size. */
  size?: number;
}

export const CursorHover: React.FC<CursorHoverProps> = ({
  to,
  appearFrame,
  landsAtFrame,
  fadeOutFrame,
  disappearFrame,
  cursorFromX = -340,
  cursorFromY = 220,
  size = 40,
}) => {
  const frame = useCurrentFrame();
  if (frame < appearFrame || frame > disappearFrame) return null;

  const ec = {extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const};

  const cursorX = interpolate(
    frame,
    [appearFrame, landsAtFrame],
    [cursorFromX, 0],
    {...ec, easing: easeInOut},
  );
  const cursorY = interpolate(
    frame,
    [appearFrame, landsAtFrame],
    [cursorFromY, 0],
    {...ec, easing: easeInOut},
  );
  const moveProgress =
    frame >= appearFrame && frame <= landsAtFrame
      ? (frame - appearFrame) / Math.max(1, landsAtFrame - appearFrame)
      : 1;
  const cursorArc =
    moveProgress > 0 && moveProgress < 1 ? Math.sin(moveProgress * Math.PI) * -36 : 0;

  const fadeIn = interpolate(frame, [appearFrame, appearFrame + 6], [0, 1], ec);
  const fadeOut = interpolate(
    frame,
    [fadeOutFrame, disappearFrame],
    [1, 0],
    ec,
  );
  const opacity = Math.min(fadeIn, fadeOut);

  const cx = to.x * FRAME_W;
  const cy = to.y * FRAME_H;

  return (
    <div
      style={{
        position: "absolute",
        left: cx + cursorX - 4,
        top: cy + cursorY + cursorArc - 2,
        opacity,
        pointerEvents: "none",
        zIndex: 85,
      }}
    >
      <CursorSVG size={size} />
    </div>
  );
};
