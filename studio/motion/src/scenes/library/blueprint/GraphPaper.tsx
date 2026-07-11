// GraphPaper — the faint engineering-grid ground shared by every blueprint
// scene, plus corner registration ticks and a thin sheet border. It is what
// makes the style read as "drawn on a spec sheet" before a single label lands.
//
// Colours come only from tokens (grid = border, ticks = primary). The grid
// itself fades in first so the sheet feels like it is being laid out, then the
// scene's device plots on top.
import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { bg, primary } from "../../../tokens";
import { GRID_COLOR, drawIn } from "./_shared";

export const GraphPaper: React.FC<{ children?: React.ReactNode }> = ({
  children,
}) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  const cell = Math.round(height / 18); // minor grid pitch
  const gridIn = drawIn(frame, 0, 16);
  const frameIn = drawIn(frame, 4, 18);

  const inset = Math.round(height * 0.06);
  const tick = Math.round(height * 0.03);

  return (
    <AbsoluteFill style={{ background: bg }}>
      {/* Minor + major graph grid, faint, fading in first */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          opacity: 0.5 * gridIn,
          backgroundImage: `
            linear-gradient(${GRID_COLOR} 1px, transparent 1px),
            linear-gradient(90deg, ${GRID_COLOR} 1px, transparent 1px)
          `,
          backgroundSize: `${cell}px ${cell}px, ${cell}px ${cell}px`,
        }}
      />
      <div
        style={{
          position: "absolute",
          inset: 0,
          opacity: 0.5 * gridIn,
          backgroundImage: `
            linear-gradient(${GRID_COLOR} 1px, transparent 1px),
            linear-gradient(90deg, ${GRID_COLOR} 1px, transparent 1px)
          `,
          backgroundSize: `${cell * 5}px ${cell * 5}px, ${cell * 5}px ${cell * 5}px`,
        }}
      />

      {/* Thin sheet border */}
      <div
        style={{
          position: "absolute",
          left: inset,
          top: inset,
          right: inset,
          bottom: inset,
          border: `1px solid ${GRID_COLOR}`,
          opacity: frameIn,
        }}
      />

      {/* Corner registration ticks */}
      {[
        { left: inset, top: inset, sx: 1, sy: 1 },
        { left: width - inset, top: inset, sx: -1, sy: 1 },
        { left: inset, top: height - inset, sx: 1, sy: -1 },
        { left: width - inset, top: height - inset, sx: -1, sy: -1 },
      ].map((c, i) => (
        <div key={i} style={{ position: "absolute", left: c.left, top: c.top, opacity: frameIn }}>
          <div
            style={{
              position: "absolute",
              width: tick * c.sx,
              height: 1,
              background: primary,
            }}
          />
          <div
            style={{
              position: "absolute",
              width: 1,
              height: tick * c.sy,
              background: primary,
            }}
          />
        </div>
      ))}

      {children}
    </AbsoluteFill>
  );
};
