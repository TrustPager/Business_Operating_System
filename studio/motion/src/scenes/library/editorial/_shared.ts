// Shared entrance helpers for the Clean-editorial scene primitives.
//
// One place for the restrained spring language every editorial scene uses:
// a staggered rise-in (opacity + small lift + micro-scale) driven by the
// scene-local frame. Keeps motion discipline consistent across the library so
// scenes read as one system, not four different animation styles.
import { spring, interpolate } from "remotion";

export interface Entrance {
  opacity: number;
  lift: number; // px to translate up from
  scale: number;
  /** Ready-made transform combining lift + scale. */
  transform: string;
}

/**
 * riseIn — the house entrance. Springs a value in starting at `delay` frames
 * (scene-local), rising `lift` px with a gentle scale settle. `damping: 200`
 * gives a calm, overshoot-free settle — editorial, not bouncy.
 */
export const riseIn = (
  frame: number,
  fps: number,
  delay = 0,
  lift = 26
): Entrance => {
  const s = spring({
    frame: frame - delay,
    fps,
    config: { damping: 200, mass: 0.9 },
  });
  const opacity = interpolate(s, [0, 1], [0, 1]);
  const y = interpolate(s, [0, 1], [lift, 0]);
  const scale = interpolate(s, [0, 1], [0.965, 1]);
  return {
    opacity,
    lift: y,
    scale,
    transform: `translateY(${y}px) scale(${scale})`,
  };
};

/**
 * drawIn — 0→1 progress for a stroke/rule drawing itself in, eased. Used for
 * the thin editorial rules and dividers.
 */
export const drawIn = (
  frame: number,
  start: number,
  duration: number
): number =>
  interpolate(frame, [start, start + duration], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
