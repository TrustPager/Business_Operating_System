// BeforeAfter (Blueprint) — a revision diagram. Two schematic component boxes:
// the "before" is drawn as an as-built outline (dashed, muted), the "after" is
// the specified solid part with an accent corner. A dimensioned connector plots
// across the gap carrying a delta callout, so the change reads like an
// engineering revision, not a captioned slide.
//
// Structured props: subject + before/after {tag, value}.
import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";
import { text, textMuted, panel, primary, accent } from "../../../tokens";
import { FONT_MONO } from "../../../fonts";
import { ConnectorLine } from "../../../compositor";
import { GraphPaper } from "./GraphPaper";
import { measuredIn, drawIn, monoLabel } from "./_shared";

export interface BeforeAfterProps {
  subject?: string;
  before: { tag: string; value: string };
  after: { tag: string; value: string };
}

const SchematicBox: React.FC<{
  cx: number;
  cy: number;
  w: number;
  h: number;
  tag: string;
  value: string;
  variant: "asbuilt" | "spec";
  opacity: number;
  transform: string;
}> = ({ cx, cy, w, h, tag, value, variant, opacity, transform }) => {
  const spec = variant === "spec";
  return (
    <div
      style={{
        position: "absolute",
        left: cx - w / 2,
        top: cy - h / 2,
        width: w,
        height: h,
        opacity,
        transform,
        background: spec ? panel : "transparent",
        border: `${spec ? 2 : 1}px ${spec ? "solid" : "dashed"} ${
          spec ? primary : textMuted
        }`,
        boxSizing: "border-box",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "flex-start",
        gap: 16,
        padding: "0 40px",
        fontFamily: FONT_MONO,
      }}
    >
      {/* accent corner marker on the spec part */}
      {spec ? (
        <>
          <div style={{ position: "absolute", left: -2, top: -2, width: 22, height: 2, background: accent }} />
          <div style={{ position: "absolute", left: -2, top: -2, width: 2, height: 22, background: accent }} />
        </>
      ) : null}
      <span style={monoLabel(h * 0.09, spec ? primary : textMuted)}>{tag}</span>
      <div
        style={{
          fontSize: h * 0.22,
          lineHeight: 0.98,
          fontWeight: 600,
          letterSpacing: "-0.01em",
          color: spec ? text : textMuted,
          width: "100%",
          overflowWrap: "break-word",
        }}
      >
        {value}
      </div>
    </div>
  );
};

export const BeforeAfter: React.FC<BeforeAfterProps> = ({
  subject,
  before,
  after,
}) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  const boxW = width * 0.3;
  const boxH = height * 0.36;
  const cy = height * 0.56;
  const leftCx = width * 0.28;
  const rightCx = width * 0.72;

  const leftE = measuredIn(frame, 6, 16);
  const rightE = measuredIn(frame, 30, 16);
  const subjectE = measuredIn(frame, 0, 14);

  return (
    <GraphPaper>
      {/* Subject label as a sheet heading */}
      {subject ? (
        <div
          style={{
            position: "absolute",
            top: height * 0.22,
            width: "100%",
            textAlign: "center",
            opacity: subjectE.opacity,
            transform: subjectE.transform,
          }}
        >
          <span style={monoLabel(height * 0.022)}>{subject}</span>
        </div>
      ) : null}

      <SchematicBox
        cx={leftCx}
        cy={cy}
        w={boxW}
        h={boxH}
        tag={before.tag}
        value={before.value}
        variant="asbuilt"
        opacity={leftE.opacity}
        transform={leftE.transform}
      />

      {/* Dimensioned revision arrow across the gap */}
      <ConnectorLine
        from={{ x: (leftCx + boxW / 2) / width + 0.01, y: cy / height }}
        to={{ x: (rightCx - boxW / 2) / width - 0.01, y: cy / height }}
        appearAt={22}
        drawDurationFrames={16}
        curve={0}
        strokeWidth={1.5}
        color={primary}
        glow={false}
      />

      {/* Delta callout above the connector */}
      <div
        style={{
          position: "absolute",
          left: 0,
          top: cy - height * 0.11,
          width: "100%",
          textAlign: "center",
          ...monoLabel(height * 0.018, accent),
          opacity: drawIn(frame, 40, 10),
        }}
      >
        {"△ Revised"}
      </div>

      <SchematicBox
        cx={rightCx}
        cy={cy}
        w={boxW}
        h={boxH}
        tag={after.tag}
        value={after.value}
        variant="spec"
        opacity={rightE.opacity}
        transform={rightE.transform}
      />
    </GraphPaper>
  );
};
