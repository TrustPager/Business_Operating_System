// NoAutomationsCard — minimal popover shown when hovering an icon BEFORE any
// automations exist there. Just a single line: "No automations". Used to set up
// the "empty state" beat before the first automation is built.
import React from "react";
import {useCurrentFrame, interpolate, Easing} from "remotion";
import {colors, fonts, shadows} from "../tokens";

export interface NoAutomationsCardProps {
  /** Top-left position (fractional 0..1). */
  position: {x: number; y: number};
  appearFrame: number;
  disappearFrame: number;
  /** Card width (px). Default 180. */
  width?: number;
  /** Text to show. Default "No automations". */
  label?: string;
}

export const NoAutomationsCard: React.FC<NoAutomationsCardProps> = ({
  position,
  appearFrame,
  disappearFrame,
  width = 180,
  label = "No automations",
}) => {
  const frame = useCurrentFrame();
  if (frame < appearFrame || frame > disappearFrame) return null;

  const ec = {extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const};
  const local = frame - appearFrame;
  const fadeIn = interpolate(local, [0, 12], [0, 1], ec);
  const slideY = interpolate(local, [0, 18], [10, 0], {
    ...ec,
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });
  const fadeOut = interpolate(frame, [disappearFrame - 12, disappearFrame], [1, 0], ec);
  const opacity = Math.min(fadeIn, fadeOut);

  const x = position.x * 1920;
  const y = position.y * 1080;

  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        width,
        backgroundColor: colors.bg000,
        borderRadius: 10,
        boxShadow: `${shadows.overlay}, 0 0 0 1px ${colors.border300}`,
        padding: "12px 16px",
        opacity,
        transform: `translateY(${slideY}px)`,
        zIndex: 90,
        pointerEvents: "none",
        textAlign: "center",
      }}
    >
      <span
        style={{
          fontFamily: fonts.ui,
          fontSize: 14,
          fontWeight: 500,
          color: colors.text200,
        }}
      >
        {label}
      </span>
    </div>
  );
};
