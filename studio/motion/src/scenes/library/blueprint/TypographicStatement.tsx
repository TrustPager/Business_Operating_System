// TypographicStatement (Blueprint) — the statement treated as the part-name on a
// drawing sheet. It is NOT centred text: a mono kicker sits on a marker rule
// top-left, a faint figure reference is plotted like a drawing number, the line
// sets in the technical mono face, and a dimension line with end-ticks draws
// across its measured width beneath it. The schematic frame does the styling.
//
// Structured props: kicker, statement (<=4 words), index.
import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";
import { text, textMuted, accent, primary } from "../../../tokens";
import { FONT_MONO } from "../../../fonts";
import { GraphPaper } from "./GraphPaper";
import { measuredIn, drawIn, monoLabel } from "./_shared";

export interface TypographicStatementProps {
  kicker?: string;
  statement: string;
  index?: string;
}

export const TypographicStatement: React.FC<TypographicStatementProps> = ({
  kicker,
  statement,
  index,
}) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  const marginLeft = width * 0.13;
  const words = statement.split(/\s+/).filter(Boolean);

  const kickerE = measuredIn(frame, 8, 14);
  const dimGrow = drawIn(frame, 30, 22);
  const dimTop = height * 0.62;
  const dimW = width * 0.42;

  return (
    <GraphPaper>
      {/* Faint figure reference, plotted like a drawing number */}
      {index ? (
        <div
          style={{
            position: "absolute",
            left: marginLeft,
            top: height * 0.2,
            ...monoLabel(height * 0.02, textMuted),
            opacity: 0.6 * measuredIn(frame, 2, 12).opacity,
          }}
        >
          {`FIG ${index}`}
        </div>
      ) : null}

      {/* Kicker on a marker rule */}
      {kicker ? (
        <div
          style={{
            position: "absolute",
            left: marginLeft,
            top: height * 0.32,
            display: "flex",
            alignItems: "center",
            gap: 14,
            opacity: kickerE.opacity,
            transform: kickerE.transform,
          }}
        >
          <div style={{ width: 10, height: 10, background: accent }} />
          <div style={{ width: 54, height: 1, background: primary }} />
          <span style={monoLabel(height * 0.019)}>{kicker}</span>
        </div>
      ) : null}

      {/* The statement — technical mono, plotted word by word */}
      <div
        style={{
          position: "absolute",
          left: marginLeft,
          top: height * 0.4,
          right: width * 0.1,
          fontFamily: FONT_MONO,
          fontSize: height * 0.088,
          lineHeight: 1.08,
          fontWeight: 500,
          letterSpacing: "-0.01em",
          color: text,
        }}
      >
        {words.map((w, i) => {
          const e = measuredIn(frame, 16 + i * 5, 16);
          return (
            <span
              key={i}
              style={{
                display: "inline-block",
                marginRight: "0.35em",
                opacity: e.opacity,
                transform: e.transform,
              }}
            >
              {w}
            </span>
          );
        })}
      </div>

      {/* Dimension line beneath, end-ticks + measured caption */}
      <div style={{ position: "absolute", left: marginLeft, top: dimTop }}>
        {/* left end tick */}
        <div style={{ position: "absolute", left: 0, top: -8, width: 1, height: 16, background: primary, opacity: dimGrow > 0 ? 1 : 0 }} />
        {/* the measuring rule */}
        <div style={{ position: "absolute", left: 0, top: 0, width: dimW * dimGrow, height: 1, background: primary }} />
        {/* right end tick */}
        <div
          style={{
            position: "absolute",
            left: dimW,
            top: -8,
            width: 1,
            height: 16,
            background: primary,
            opacity: dimGrow > 0.98 ? 1 : 0,
          }}
        />
        {/* caption under the rule */}
        <div
          style={{
            position: "absolute",
            left: 0,
            top: 14,
            width: dimW,
            textAlign: "center",
            ...monoLabel(height * 0.016, textMuted),
            opacity: drawIn(frame, 48, 10),
          }}
        >
          {"To scale"}
        </div>
      </div>
    </GraphPaper>
  );
};
