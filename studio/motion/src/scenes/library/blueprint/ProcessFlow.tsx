// ProcessFlow (Blueprint) — the flagship schematic. Rectangular spec-nodes carry
// a mono STEP code and a label; thin connectors plot between them with arrowheads
// and junction dots, each drawing only after its nodes land. Reads like a system
// diagram on a drawing sheet, following left→right like a signal path.
//
// Structured props: kicker + ordered {label} steps (2–4). Positions are
// proportional so the layout survives aspect changes.
import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";
import { text, panel, primary, accent } from "../../../tokens";
import { FONT_MONO } from "../../../fonts";
import { ConnectorLine } from "../../../compositor";
import { GraphPaper } from "./GraphPaper";
import { measuredIn, monoLabel } from "./_shared";

export interface ProcessStep {
  label: string;
}
export interface ProcessFlowProps {
  kicker?: string;
  steps: ProcessStep[];
}

const NODE_DELAY = 12;

const SpecNode: React.FC<{
  cx: number;
  cy: number;
  w: number;
  h: number;
  code: string;
  label: string;
  opacity: number;
  transform: string;
}> = ({ cx, cy, w, h, code, label, opacity, transform }) => (
  <div
    style={{
      position: "absolute",
      left: cx - w / 2,
      top: cy - h / 2,
      width: w,
      height: h,
      opacity,
      transform,
      background: panel,
      border: `1.5px solid ${primary}`,
      boxSizing: "border-box",
      display: "flex",
      flexDirection: "column",
      justifyContent: "center",
      gap: h * 0.14,
      padding: `0 ${w * 0.1}px`,
      fontFamily: FONT_MONO,
    }}
  >
    {/* accent index tab on the top edge */}
    <div style={{ position: "absolute", left: -1.5, top: -1.5, width: w * 0.32, height: 3, background: accent }} />
    <span style={monoLabel(h * 0.16, accent)}>{code}</span>
    <div
      style={{
        fontSize: h * 0.19,
        lineHeight: 1.05,
        fontWeight: 500,
        letterSpacing: "-0.01em",
        color: text,
      }}
    >
      {label}
    </div>
  </div>
);

export const ProcessFlow: React.FC<ProcessFlowProps> = ({ kicker, steps }) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  const n = Math.max(steps.length, 1);
  const nodeW = width * 0.19;
  const nodeH = height * 0.2;
  const cy = height * 0.54;

  const bandL = width * 0.16;
  const bandR = width * 0.84;
  const step = n > 1 ? (bandR - bandL) / (n - 1) : 0;
  const centres = steps.map((_, i) => bandL + step * i);

  const kickerE = measuredIn(frame, 2, 14);

  return (
    <GraphPaper>
      {kicker ? (
        <div
          style={{
            position: "absolute",
            top: height * 0.24,
            width: "100%",
            textAlign: "center",
            opacity: kickerE.opacity,
            transform: kickerE.transform,
          }}
        >
          <span style={monoLabel(height * 0.022)}>{kicker}</span>
        </div>
      ) : null}

      {/* Connectors — drawn after both endpoint nodes have landed */}
      {centres.slice(0, -1).map((cxA, i) => {
        const cxB = centres[i + 1];
        const gapHalf = nodeW / 2;
        const appearAt = 8 + (i + 1) * NODE_DELAY + 10;
        const y = cy / height;
        return (
          <React.Fragment key={`c-${i}`}>
            <ConnectorLine
              from={{ x: (cxA + gapHalf) / width + 0.004, y }}
              to={{ x: (cxB - gapHalf) / width - 0.004, y }}
              appearAt={appearAt}
              drawDurationFrames={10}
              curve={0}
              strokeWidth={1.5}
              color={primary}
              glow={false}
            />
            {/* junction dot at the outgoing edge */}
            <div
              style={{
                position: "absolute",
                left: cxA + gapHalf - 3,
                top: cy - 3,
                width: 6,
                height: 6,
                borderRadius: "50%",
                background: accent,
                opacity: frame > appearAt ? 1 : 0,
              }}
            />
          </React.Fragment>
        );
      })}

      {steps.map((s, i) => {
        const e = measuredIn(frame, 8 + i * NODE_DELAY, 16);
        return (
          <SpecNode
            key={`n-${i}`}
            cx={centres[i]}
            cy={cy}
            w={nodeW}
            h={nodeH}
            code={`STEP ${String(i + 1).padStart(2, "0")}`}
            label={s.label}
            opacity={e.opacity}
            transform={e.transform}
          />
        );
      })}
    </GraphPaper>
  );
};
