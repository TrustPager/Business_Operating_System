// TypographicStatement (Pop) — oversized heavy type that slams in word by word,
// stacked left-aligned and filling the frame. The final word lands inside an
// accent block (a caption-style highlight), and the kicker rides in as a rotated
// stamp badge. Kinetic overshoot, brand-heavy. Not a tidy centred line.
//
// Structured props: kicker, statement (<=4 words), index.
import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { bg, text, primaryDeep, accent, panel } from "../../../tokens";
import { FONT_BODY } from "../../../fonts";
import { popIn } from "./_shared";

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
  const { fps, width, height } = useVideoConfig();

  const words = statement.split(/\s+/).filter(Boolean);
  const marginLeft = width * 0.1;
  const lastIdx = words.length - 1;

  const kickerE = popIn(frame, fps, 0, 0.5, 0);
  const kickerRot = -4;

  return (
    <AbsoluteFill style={{ background: bg, fontFamily: FONT_BODY, overflow: "hidden" }}>
      {/* Oversized faint index digit, bottom-right, purely graphic energy */}
      {index ? (
        <div
          style={{
            position: "absolute",
            right: -width * 0.02,
            bottom: -height * 0.14,
            fontSize: height * 0.5,
            fontWeight: 900,
            color: accent,
            opacity: 0.1 * popIn(frame, fps, 2, 0.8, 0).opacity,
            letterSpacing: "-0.05em",
          }}
        >
          {index}
        </div>
      ) : null}

      {/* Rotated stamp kicker */}
      {kicker ? (
        <div
          style={{
            position: "absolute",
            left: marginLeft,
            top: height * 0.2,
            transform: `${kickerE.transform} rotate(${kickerRot}deg)`,
            opacity: kickerE.opacity,
            background: accent,
            color: panel,
            padding: "10px 20px",
            fontSize: height * 0.028,
            fontWeight: 800,
            letterSpacing: "0.08em",
            textTransform: "uppercase",
          }}
        >
          {kicker}
        </div>
      ) : null}

      {/* Stacked heavy words, last one in an accent block */}
      <div
        style={{
          position: "absolute",
          left: marginLeft,
          top: height * 0.32,
          right: width * 0.06,
          display: "flex",
          flexDirection: "column",
          alignItems: "flex-start",
          gap: height * 0.005,
        }}
      >
        {words.map((w, i) => {
          const e = popIn(frame, fps, 8 + i * 5, 0.55, 46);
          const highlight = i === lastIdx && words.length > 1;
          return (
            <div
              key={i}
              style={{
                opacity: e.opacity,
                transform: e.transform,
                transformOrigin: "left center",
                fontSize: height * 0.16,
                lineHeight: 0.98,
                fontWeight: 900,
                letterSpacing: "-0.03em",
                textTransform: "uppercase",
                color: highlight ? panel : primaryDeep,
                background: highlight ? accent : "transparent",
                padding: highlight ? "0 0.12em" : 0,
              }}
            >
              {w}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
