// ProcessFlow — labelled steps joined by drawn connectors. A real flow diagram:
// numbered nodes rise in left→right, each connector draws only after its two
// nodes have landed, so the eye follows the sequence like a path. Not a bullet
// list with icons.
//
// Structured props: kicker + an ordered list of {label} steps (2–4 works best;
// each label <=4 words). Node positions are computed proportionally so the
// layout survives aspect-ratio changes.
import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import {
  bg,
  text,
  textMuted,
  panel,
  border,
  primary,
  primaryDeep,
  accent,
  shadows,
} from "../../../tokens";
import { FONT_BODY, FONT_SERIF } from "../../../fonts";
import { ConnectorLine } from "../../../compositor";
import { riseIn } from "./_shared";

export interface ProcessStep {
  label: string;
}

export interface ProcessFlowProps {
  kicker?: string;
  steps: ProcessStep[];
}

const NODE_DELAY = 10; // frames between successive node entrances

const StepNode: React.FC<{
  cx: number; // px
  cy: number; // px
  size: number;
  ordinal: string;
  label: string;
  delay: number;
}> = ({ cx, cy, size, ordinal, label, delay }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const e = riseIn(frame, fps, delay, 22);

  return (
    <div
      style={{
        position: "absolute",
        left: cx - size / 2,
        top: cy - size / 2,
        width: size,
        opacity: e.opacity,
        transform: e.transform,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 22,
        fontFamily: FONT_BODY,
      }}
    >
      {/* Numbered chip */}
      <div
        style={{
          width: size,
          height: size,
          borderRadius: "50%",
          background: panel,
          border: `2px solid ${border}`,
          boxShadow: shadows.card,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          position: "relative",
        }}
      >
        <span
          style={{
            fontFamily: FONT_SERIF,
            fontSize: size * 0.42,
            fontWeight: 700,
            color: primaryDeep,
            letterSpacing: "-0.02em",
          }}
        >
          {ordinal}
        </span>
        {/* thin accent ring segment at the top for a touch of brand */}
        <div
          style={{
            position: "absolute",
            top: -2,
            left: -2,
            right: -2,
            bottom: -2,
            borderRadius: "50%",
            border: `2px solid ${accent}`,
            clipPath: "polygon(0 0, 100% 0, 100% 32%, 0 32%)",
            opacity: 0.9,
          }}
        />
      </div>
      {/* Label under the node */}
      <div
        style={{
          textAlign: "center",
          fontSize: size * 0.3,
          fontWeight: 600,
          color: text,
          letterSpacing: "-0.01em",
          maxWidth: size * 2.1,
          lineHeight: 1.1,
        }}
      >
        {label}
      </div>
    </div>
  );
};

export const ProcessFlow: React.FC<ProcessFlowProps> = ({ kicker, steps }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const n = Math.max(steps.length, 1);
  const size = height * 0.15;
  const cy = height * 0.52;

  // Evenly space node centres inside a comfortable horizontal band.
  const bandL = width * 0.18;
  const bandR = width * 0.82;
  const step = n > 1 ? (bandR - bandL) / (n - 1) : 0;
  const centres = steps.map((_, i) => bandL + step * i);

  const kickerE = riseIn(frame, fps, 2, 16);

  return (
    <AbsoluteFill style={{ background: bg, fontFamily: FONT_BODY }}>
      {kicker ? (
        <div
          style={{
            position: "absolute",
            top: height * 0.22,
            width: "100%",
            textAlign: "center",
            opacity: kickerE.opacity,
            transform: kickerE.transform,
          }}
        >
          <span
            style={{
              fontSize: height * 0.026,
              fontWeight: 700,
              letterSpacing: "0.26em",
              textTransform: "uppercase",
              color: primary,
            }}
          >
            {kicker}
          </span>
        </div>
      ) : null}

      {/* Connectors between consecutive nodes — each draws after both land */}
      {centres.slice(0, -1).map((cxA, i) => {
        const cxB = centres[i + 1];
        const gapHalf = size * 0.62;
        const appearAt = 8 + (i + 1) * NODE_DELAY + 12;
        return (
          <ConnectorLine
            key={`c-${i}`}
            from={{ x: (cxA + gapHalf) / width, y: cy / height }}
            to={{ x: (cxB - gapHalf) / width, y: cy / height }}
            appearAt={appearAt}
            drawDurationFrames={12}
            curve={0}
            strokeWidth={2}
            color={accent}
          />
        );
      })}

      {/* Nodes */}
      {steps.map((s, i) => (
        <StepNode
          key={`n-${i}`}
          cx={centres[i]}
          cy={cy}
          size={size}
          ordinal={String(i + 1).padStart(2, "0")}
          label={s.label}
          delay={8 + i * NODE_DELAY}
        />
      ))}
    </AbsoluteFill>
  );
};
