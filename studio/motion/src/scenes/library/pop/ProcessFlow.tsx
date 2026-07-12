// ProcessFlow (Pop) — big accent-filled number chips that BOUNCE in one after
// another, heavy uppercase labels beneath, joined by chunky dashes that pop
// between them. Energetic, staggered, thumb-stopping. Not a quiet node diagram.
//
// Structured props: kicker + ordered {label} steps (2–4). Positions proportional.
import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { bg, text, panel, accent, primaryDeep } from "../../../tokens";
import { FONT_BODY } from "../../../fonts";
import { popIn } from "./_shared";

export interface ProcessStep {
  label: string;
}
export interface ProcessFlowProps {
  kicker?: string;
  steps: ProcessStep[];
}

const NODE_DELAY = 9;

const Chip: React.FC<{
  cx: number;
  cy: number;
  size: number;
  ordinal: string;
  label: string;
  opacity: number;
  transform: string;
}> = ({ cx, cy, size, ordinal, label, opacity, transform }) => (
  <div
    style={{
      position: "absolute",
      left: cx - size / 2,
      top: cy - size / 2,
      width: size,
      opacity,
      transform,
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      gap: 20,
      fontFamily: FONT_BODY,
    }}
  >
    <div
      style={{
        width: size,
        height: size,
        borderRadius: "50%",
        background: accent,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <span
        style={{
          fontSize: size * 0.48,
          fontWeight: 900,
          color: panel,
          letterSpacing: "-0.03em",
        }}
      >
        {ordinal}
      </span>
    </div>
    <div
      style={{
        textAlign: "center",
        fontSize: size * 0.28,
        fontWeight: 800,
        textTransform: "uppercase",
        letterSpacing: "-0.01em",
        color: text,
        maxWidth: size * 2.3,
        lineHeight: 1.05,
      }}
    >
      {label}
    </div>
  </div>
);

export const ProcessFlow: React.FC<ProcessFlowProps> = ({ kicker, steps }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const n = Math.max(steps.length, 1);
  const size = height * 0.19;
  const cy = height * 0.52;

  const bandL = width * 0.19;
  const bandR = width * 0.81;
  const step = n > 1 ? (bandR - bandL) / (n - 1) : 0;
  const centres = steps.map((_, i) => bandL + step * i);

  const kickerE = popIn(frame, fps, 0, 0.5, 0);

  return (
    <AbsoluteFill style={{ background: bg, fontFamily: FONT_BODY, overflow: "hidden" }}>
      {kicker ? (
        <div
          style={{
            position: "absolute",
            top: height * 0.2,
            width: "100%",
            textAlign: "center",
            opacity: kickerE.opacity,
            transform: kickerE.transform,
          }}
        >
          <span
            style={{
              display: "inline-block",
              background: primaryDeep,
              color: panel,
              padding: "8px 22px",
              fontSize: height * 0.028,
              fontWeight: 800,
              letterSpacing: "0.08em",
              textTransform: "uppercase",
            }}
          >
            {kicker}
          </span>
        </div>
      ) : null}

      {/* Chunky connector dashes popping between chips */}
      {centres.slice(0, -1).map((cxA, i) => {
        const cxB = centres[i + 1];
        const mid = (cxA + cxB) / 2;
        const e = popIn(frame, fps, 8 + (i + 1) * NODE_DELAY - 3, 0.4, 0);
        return (
          <div
            key={`c-${i}`}
            style={{
              position: "absolute",
              left: mid - size * 0.35,
              top: cy - 5,
              width: size * 0.7,
              height: 10,
              background: primaryDeep,
              borderRadius: 6,
              opacity: e.opacity,
              transform: e.transform,
            }}
          />
        );
      })}

      {steps.map((s, i) => {
        const e = popIn(frame, fps, 8 + i * NODE_DELAY, 0.5, 44);
        return (
          <Chip
            key={`n-${i}`}
            cx={centres[i]}
            cy={cy}
            size={size}
            ordinal={String(i + 1)}
            label={s.label}
            opacity={e.opacity}
            transform={e.transform}
          />
        );
      })}
    </AbsoluteFill>
  );
};
