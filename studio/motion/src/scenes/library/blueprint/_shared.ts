// Shared primitives for the Blueprint / how-it-works scene style.
//
// Register: schematic technical drawing. Everything reads like a spec sheet —
// faint graph-paper ground, thin precise strokes that DRAW themselves in (never
// bounce), mono uppercase labels, dimension lines and connectors doing the
// explaining. Calm, measured, engineered. The opposite of kinetic.
//
// This module is the one home for the blueprint motion + drawing language so the
// four primitives read as a single technical system.
import { interpolate, Easing } from "remotion";
import { border, primary } from "../../../tokens";
import { FONT_MONO } from "../../../fonts";

/**
 * measuredIn — the house blueprint entrance. A calm fade with a hair of settle
 * (0.6px is imperceptible as motion; it just softens the pop). Deliberately NOT
 * a spring: schematic elements appear as if plotted, not thrown.
 */
export const measuredIn = (
  frame: number,
  start = 0,
  duration = 14
): { opacity: number; transform: string } => {
  const t = interpolate(frame, [start, start + duration], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.33, 0, 0.15, 1),
  });
  const y = interpolate(t, [0, 1], [6, 0]);
  return { opacity: t, transform: `translateY(${y}px)` };
};

/**
 * drawIn — 0→1 progress for a stroke plotting itself in, eased like a pen. Used
 * for dimension lines, rules and the schematic frame.
 */
export const drawIn = (frame: number, start: number, duration: number): number =>
  interpolate(frame, [start, start + duration], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.5, 0, 0.2, 1),
  });

/** The mono uppercase micro-label used for every schematic annotation. */
export const monoLabel = (size: number, color: string = primary) =>
  ({
    fontFamily: FONT_MONO,
    fontSize: size,
    fontWeight: 600,
    letterSpacing: "0.22em",
    textTransform: "uppercase",
    color,
  }) as const;

/** Faint grid rule colour, used by GraphPaper and the schematic frame. */
export const GRID_COLOR = border;
export const STROKE_COLOR = primary;
