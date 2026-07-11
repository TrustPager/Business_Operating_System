// Shared primitives for the Bold pop / social scene style.
//
// Register: high-contrast, heavy, oversized, kinetic. Elements SLAM in with an
// overshoot spring and settle; accent blocks and rotated stamps carry the brand;
// scale is deliberately too big for the frame. Built for thumb-stopping
// short-form. The opposite of the blueprint's calm.
//
// This module is the one home for the pop motion language so the four primitives
// read as one energetic system.
import { spring, interpolate } from "remotion";

export interface Pop {
  opacity: number;
  scale: number;
  transform: string;
}

/**
 * popIn — the house pop entrance. A punchy overshoot spring: the element
 * overshoots its scale then settles, with a small upward slam. Low damping =
 * visible bounce (kinetic, on-brand for social), unlike the editorial/blueprint
 * calm settles.
 */
export const popIn = (
  frame: number,
  fps: number,
  delay = 0,
  fromScale = 0.6,
  lift = 40
): Pop => {
  const s = spring({
    frame: frame - delay,
    fps,
    config: { damping: 11, mass: 0.7, stiffness: 140 },
  });
  const opacity = interpolate(s, [0, 0.4], [0, 1], {
    extrapolateRight: "clamp",
  });
  const scale = interpolate(s, [0, 1], [fromScale, 1]);
  const y = interpolate(s, [0, 1], [lift, 0]);
  return { opacity, scale, transform: `translateY(${y}px) scale(${scale})` };
};

/**
 * slamIn — a horizontal overshoot slam from a direction. Used for the pop
 * before/after panels so they crash in from opposite sides.
 */
export const slamIn = (
  frame: number,
  fps: number,
  delay: number,
  fromX: number
): Pop => {
  const s = spring({
    frame: frame - delay,
    fps,
    config: { damping: 12, mass: 0.8, stiffness: 130 },
  });
  const opacity = interpolate(s, [0, 0.35], [0, 1], {
    extrapolateRight: "clamp",
  });
  const x = interpolate(s, [0, 1], [fromX, 0]);
  const scale = interpolate(s, [0, 1], [0.85, 1]);
  return { opacity, scale, transform: `translateX(${x}px) scale(${scale})` };
};
