// DebugOverlay — toggleable pixel grid + named bounding boxes for positioning work.
// Drop into ANY composition during iteration; remove the prop (or set show={false})
// before shipping. NEVER ship with `show` enabled.
//
// Usage:
//   <DebugOverlay
//     show
//     grid={{step: 100, minor: 50}}
//     boxes={[
//       {label: "header", tl: {x: 282, y: 164}, w: 284, h: 67, color: "#ff00ff"},
//       {label: "bolt target", tl: {x: 506, y: 178}, w: 24, h: 24, color: "#00ff88"},
//     ]}
//   />
import React from "react";
import {AbsoluteFill} from "remotion";

const FRAME_W = 1920;
const FRAME_H = 1080;

export interface DebugBox {
  label?: string;
  /** Top-left in composition pixels (1920x1080 space). */
  tl: {x: number; y: number};
  /** Width in composition pixels. */
  w: number;
  /** Height in composition pixels. */
  h: number;
  /** Outline color. Default magenta. */
  color?: string;
}

export interface DebugOverlayProps {
  show?: boolean;
  /** Pixel-grid settings. Pass false to disable grid. */
  grid?: false | {step?: number; minor?: number; color?: string; opacity?: number};
  /** Named boxes to draw. */
  boxes?: DebugBox[];
}

const buildGridLines = (
  axis: "v" | "h",
  step: number,
  total: number,
  color: string,
  width: number,
  opacity: number,
) => {
  const lines: React.ReactNode[] = [];
  for (let n = step; n < total; n += step) {
    if (axis === "v") {
      lines.push(
        <line key={`${axis}${n}`} x1={n} y1={0} x2={n} y2={FRAME_H} stroke={color} strokeWidth={width} opacity={opacity} />,
      );
    } else {
      lines.push(
        <line key={`${axis}${n}`} x1={0} y1={n} x2={FRAME_W} y2={n} stroke={color} strokeWidth={width} opacity={opacity} />,
      );
    }
  }
  return lines;
};

export const DebugOverlay: React.FC<DebugOverlayProps> = ({
  show = false,
  grid = {step: 100, minor: 50, color: "#00ffff", opacity: 0.45},
  boxes = [],
}) => {
  if (!show) return null;

  const gridConfig = !grid ? null : {
    step: grid?.step ?? 100,
    minor: grid?.minor ?? 50,
    color: grid?.color ?? "#00ffff",
    opacity: grid?.opacity ?? 0.45,
  };

  return (
    <AbsoluteFill style={{pointerEvents: "none", zIndex: 999}}>
      {gridConfig && (
        <>
          <svg width={FRAME_W} height={FRAME_H} viewBox={`0 0 ${FRAME_W} ${FRAME_H}`} style={{position: "absolute", inset: 0, opacity: gridConfig.opacity}}>
            {buildGridLines("v", gridConfig.step, FRAME_W, gridConfig.color, 1, 1)}
            {buildGridLines("h", gridConfig.step, FRAME_H, gridConfig.color, 1, 1)}
            {buildGridLines("v", gridConfig.minor, FRAME_W, gridConfig.color, 0.5, 0.4)}
            {buildGridLines("h", gridConfig.minor, FRAME_H, gridConfig.color, 0.5, 0.4)}
          </svg>
          {Array.from({length: Math.floor(FRAME_W / gridConfig.step) - 1}, (_, i) => (i + 1) * gridConfig.step).map((x) => (
            <div
              key={`lx${x}`}
              style={{
                position: "absolute",
                left: x - 12,
                top: 4,
                color: gridConfig.color,
                fontFamily: "monospace",
                fontSize: 10,
                background: "rgba(0,0,0,0.7)",
                padding: "1px 3px",
                borderRadius: 2,
              }}
            >
              {x}
            </div>
          ))}
          {Array.from({length: Math.floor(FRAME_H / gridConfig.step)}, (_, i) => (i + 1) * gridConfig.step).map((y) => (
            <div
              key={`ly${y}`}
              style={{
                position: "absolute",
                left: 4,
                top: y - 6,
                color: gridConfig.color,
                fontFamily: "monospace",
                fontSize: 10,
                background: "rgba(0,0,0,0.7)",
                padding: "1px 3px",
                borderRadius: 2,
              }}
            >
              {y}
            </div>
          ))}
        </>
      )}

      {boxes.map((b, i) => {
        const color = b.color ?? "#ff00ff";
        return (
          <React.Fragment key={i}>
            <div
              style={{
                position: "absolute",
                left: b.tl.x,
                top: b.tl.y,
                width: b.w,
                height: b.h,
                border: `3px solid ${color}`,
                boxSizing: "border-box",
                boxShadow: `0 0 8px ${color}`,
              }}
            />
            {b.label && (
              <div
                style={{
                  position: "absolute",
                  left: b.tl.x,
                  top: b.tl.y + b.h + 4,
                  color,
                  fontFamily: "monospace",
                  fontSize: 12,
                  background: "rgba(0,0,0,0.7)",
                  padding: "2px 6px",
                  borderRadius: 3,
                  whiteSpace: "nowrap",
                }}
              >
                {b.label}: TL({b.tl.x},{b.tl.y}) W={b.w} H={b.h}
              </div>
            )}
          </React.Fragment>
        );
      })}
    </AbsoluteFill>
  );
};
