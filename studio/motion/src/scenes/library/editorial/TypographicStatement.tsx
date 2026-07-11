// TypographicStatement — one emphatic line, built as an editorial page, not
// centred text on a background.
//
// Devices that make it a composition rather than a caption:
//   - a large muted index numeral anchored top-left (the "01" of a spread)
//   - a small uppercase kicker on a thin rule
//   - the statement set BIG in the brand serif, left-aligned, word-by-word
//     staggered reveal, hung on a generous left margin
//   - a thin ~2px accent bar that draws down the left edge
// Brand palette + type only. Structured props: kicker, statement, index.
import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { bg, text, textMuted, accent, primary } from "../../../tokens";
import { FONT_BODY, FONT_SERIF } from "../../../fonts";
import { riseIn, drawIn } from "./_shared";

export interface TypographicStatementProps {
  /** Small uppercase eyebrow, e.g. "FOR TRADIES". <=3 words. */
  kicker?: string;
  /** The one emphatic line, <=4 words. Split on spaces for the stagger. */
  statement: string;
  /** Optional two-char index numeral, e.g. "01". Purely a graphic anchor. */
  index?: string;
}

export const TypographicStatement: React.FC<TypographicStatementProps> = ({
  kicker,
  statement,
  index,
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const marginLeft = width * 0.12;
  const words = statement.split(/\s+/).filter(Boolean);

  // Thin accent bar draws down the left margin.
  const barGrow = drawIn(frame, 4, 20);

  // Kicker + rule rise together, then the words stagger in after.
  const kickerE = riseIn(frame, fps, 8, 18);

  return (
    <AbsoluteFill style={{ background: bg, fontFamily: FONT_BODY }}>
      {/* Index numeral — oversized, faint, anchors the top-left like a spread */}
      {index ? (
        <div
          style={{
            position: "absolute",
            left: marginLeft,
            top: height * 0.16,
            fontFamily: FONT_SERIF,
            fontSize: height * 0.12,
            lineHeight: 1,
            fontWeight: 400,
            color: textMuted,
            opacity: 0.16 * riseIn(frame, fps, 0, 0).opacity,
            letterSpacing: "-0.03em",
          }}
        >
          {index}
        </div>
      ) : null}

      {/* Thin accent bar down the left margin */}
      <div
        style={{
          position: "absolute",
          left: marginLeft - 28,
          top: height * 0.34,
          width: 2,
          height: height * 0.32 * barGrow,
          background: accent,
          transformOrigin: "top",
        }}
      />

      {/* Kicker on a thin rule */}
      {kicker ? (
        <div
          style={{
            position: "absolute",
            left: marginLeft,
            top: height * 0.31,
            display: "flex",
            alignItems: "center",
            gap: 16,
            opacity: kickerE.opacity,
            transform: kickerE.transform,
          }}
        >
          <div style={{ width: 46, height: 2, background: primary }} />
          <span
            style={{
              fontSize: height * 0.019,
              fontWeight: 700,
              letterSpacing: "0.22em",
              textTransform: "uppercase",
              color: primary,
            }}
          >
            {kicker}
          </span>
        </div>
      ) : null}

      {/* The statement — big serif, left-aligned, word-by-word stagger */}
      <div
        style={{
          position: "absolute",
          left: marginLeft,
          top: height * 0.4,
          right: width * 0.1,
          fontFamily: FONT_SERIF,
          fontSize: height * 0.135,
          lineHeight: 1.02,
          fontWeight: 700,
          letterSpacing: "-0.03em",
          color: text,
        }}
      >
        {words.map((w, i) => {
          const e = riseIn(frame, fps, 16 + i * 6, 34);
          return (
            <span
              key={i}
              style={{
                display: "inline-block",
                marginRight: "0.28em",
                opacity: e.opacity,
                transform: e.transform,
              }}
            >
              {w}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
