// BigStat — one number, made the whole composition. The metric counts up on
// entrance (a data device, not a static caption), the unit rides its baseline,
// a thin measuring rule draws under it, and a supporting label + optional CTA
// sit in generous negative space. The number dominates the frame.
//
// Structured props: value (number) + optional prefix/suffix/label/kicker/cta.
import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Easing,
} from "remotion";
import { bg, text, textMuted, primary, primaryDeep, accent } from "../../../tokens";
import { FONT_BODY, FONT_SERIF } from "../../../fonts";
import { riseIn, drawIn } from "./_shared";

export interface BigStatProps {
  /** The metric it counts up to. */
  value: number;
  /** e.g. "$" — sits before the number. */
  prefix?: string;
  /** e.g. "s" or "seconds" — rides the number's baseline. */
  suffix?: string;
  /** Supporting line under the rule, <=4 words. */
  label?: string;
  /** Uppercase eyebrow above the number. */
  kicker?: string;
  /** Optional closing line at the foot, <=4 words. */
  cta?: string;
  /** Decimal places for the count-up (default 0). */
  decimals?: number;
}

export const BigStat: React.FC<BigStatProps> = ({
  value,
  prefix,
  suffix,
  label,
  kicker,
  cta,
  decimals = 0,
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  // Count up 0 → value over a short eased window, then hold.
  const t = interpolate(frame, [8, 44], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  const current = (value * t).toFixed(decimals);

  const numE = riseIn(frame, fps, 6, 22);
  const kickerE = riseIn(frame, fps, 0, 16);
  const labelE = riseIn(frame, fps, 20, 18);
  const ctaE = riseIn(frame, fps, 30, 18);

  const ruleGrow = drawIn(frame, 18, 22);
  const ruleWidth = width * 0.26;

  return (
    <AbsoluteFill
      style={{
        background: bg,
        fontFamily: FONT_BODY,
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: height * 0.02,
        }}
      >
        {/* Kicker between two short rules */}
        {kicker ? (
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 16,
              opacity: kickerE.opacity,
              transform: kickerE.transform,
              marginBottom: height * 0.01,
            }}
          >
            <div style={{ width: 40, height: 2, background: accent }} />
            <span
              style={{
                fontSize: height * 0.022,
                fontWeight: 700,
                letterSpacing: "0.26em",
                textTransform: "uppercase",
                color: primary,
              }}
            >
              {kicker}
            </span>
            <div style={{ width: 40, height: 2, background: accent }} />
          </div>
        ) : null}

        {/* The number — dominant, brand serif, unit on its baseline */}
        <div
          style={{
            display: "flex",
            alignItems: "flex-end",
            opacity: numE.opacity,
            transform: numE.transform,
            fontFamily: FONT_SERIF,
            color: primaryDeep,
            lineHeight: 0.9,
          }}
        >
          {prefix ? (
            <span
              style={{
                fontSize: height * 0.16,
                fontWeight: 700,
                color: primary,
                marginRight: 6,
                letterSpacing: "-0.02em",
              }}
            >
              {prefix}
            </span>
          ) : null}
          <span
            style={{
              fontSize: height * 0.42,
              fontWeight: 700,
              letterSpacing: "-0.04em",
              fontVariantNumeric: "tabular-nums",
            }}
          >
            {current}
          </span>
          {suffix ? (
            <span
              style={{
                fontSize: height * 0.09,
                fontWeight: 700,
                color: primary,
                marginLeft: 14,
                marginBottom: height * 0.03,
                letterSpacing: "-0.01em",
              }}
            >
              {suffix}
            </span>
          ) : null}
        </div>

        {/* Thin measuring rule under the number */}
        <div
          style={{
            width: ruleWidth * ruleGrow,
            height: 2,
            background: accent,
            marginTop: height * 0.01,
          }}
        />

        {/* Supporting label */}
        {label ? (
          <div
            style={{
              fontSize: height * 0.03,
              fontWeight: 600,
              color: text,
              letterSpacing: "-0.01em",
              opacity: labelE.opacity,
              transform: labelE.transform,
              marginTop: height * 0.015,
            }}
          >
            {label}
          </div>
        ) : null}

        {/* Optional closing CTA line */}
        {cta ? (
          <div
            style={{
              fontSize: height * 0.02,
              fontWeight: 600,
              letterSpacing: "0.04em",
              color: textMuted,
              opacity: ctaE.opacity,
              transform: ctaE.transform,
              marginTop: height * 0.03,
            }}
          >
            {cta}
          </div>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};
