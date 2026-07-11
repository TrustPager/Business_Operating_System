// AutomationLightningStrike — accent flash + ring pulse on an existing icon.
// No falling bolt — the icon already lives in the UI at the target position.
// This effect just lights it up: a quick accent glow flash on the icon itself,
// then a ring pulse expanding outward to signal the automation is now active.
import React from "react";
import {AbsoluteFill, useCurrentFrame, interpolate, Easing} from "remotion";
import {colors} from "../tokens";

export interface AutomationLightningStrikeProps {
  /** Target position in fractional canvas coords (0..1) — exact center of the icon. */
  target: {x: number; y: number};
  /** Frame at which the effect begins. */
  appearFrame: number;
  /** Total visible duration in frames. Default 60 (~2s). */
  durationFrames?: number;
  /** Brand colour override. Defaults to the brand accent. */
  color?: string;
}

export const AutomationLightningStrike: React.FC<AutomationLightningStrikeProps> = ({
  target,
  appearFrame,
  durationFrames = 60,
  color = colors.accentBrand,
}) => {
  const frame = useCurrentFrame();
  const local = frame - appearFrame;
  if (local < 0 || local > durationFrames) return null;

  const tx = target.x * 1920;
  const ty = target.y * 1080;

  const glowOpacity = interpolate(local, [0, 4, 28, 40], [0, 0.95, 0.55, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const glowScale = interpolate(local, [0, 40], [0.6, 1.4], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

  const discOpacity = interpolate(local, [0, 3, 22, 32], [0, 1, 0.6, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const ringOpacity = interpolate(local, [4, 12, 56], [0, 0.95, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const ringScale = interpolate(local, [4, 56], [0.7, 2.4], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

  const GLOW_SIZE = 64;
  const DISC_SIZE = 32;
  const RING_SIZE = 36;

  return (
    <AbsoluteFill style={{pointerEvents: "none", zIndex: 80}}>
      <div
        style={{
          position: "absolute",
          left: tx - GLOW_SIZE / 2,
          top: ty - GLOW_SIZE / 2,
          width: GLOW_SIZE,
          height: GLOW_SIZE,
          borderRadius: "50%",
          backgroundColor: color,
          opacity: glowOpacity,
          transform: `scale(${glowScale})`,
          filter: "blur(14px)",
        }}
      />
      <div
        style={{
          position: "absolute",
          left: tx - DISC_SIZE / 2,
          top: ty - DISC_SIZE / 2,
          width: DISC_SIZE,
          height: DISC_SIZE,
          borderRadius: "50%",
          backgroundColor: color,
          opacity: discOpacity,
          filter: "blur(2px)",
        }}
      />
      <div
        style={{
          position: "absolute",
          left: tx - RING_SIZE / 2,
          top: ty - RING_SIZE / 2,
          width: RING_SIZE,
          height: RING_SIZE,
          borderRadius: "50%",
          border: `3px solid ${color}`,
          opacity: ringOpacity,
          transform: `scale(${ringScale})`,
        }}
      />
    </AbsoluteFill>
  );
};
