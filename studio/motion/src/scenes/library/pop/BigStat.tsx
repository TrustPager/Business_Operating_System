// BigStat (Pop) — the number blown up to fill the frame, counting up hard, set
// heavy over an oversized accent block that slams in behind it. The suffix rides
// as a badge, the kicker is a rotated stamp, the label lands in caps. Maximum
// impact, kinetic. Not a modest hero number.
//
// Structured props: value (+ prefix/suffix/label/kicker/cta/decimals).
import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Easing,
} from "remotion";
import { bg, text, panel, accent, primaryDeep } from "../../../tokens";
import { FONT_BODY } from "../../../fonts";
import { popIn } from "./_shared";

export interface BigStatProps {
  value: number;
  prefix?: string;
  suffix?: string;
  label?: string;
  kicker?: string;
  cta?: string;
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

  const t = interpolate(frame, [8, 40], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  const current = (value * t).toFixed(decimals);

  const numE = popIn(frame, fps, 6, 0.5, 30);
  const blockE = popIn(frame, fps, 2, 0.4, 0);
  const kickerE = popIn(frame, fps, 0, 0.5, 0);
  const suffixE = popIn(frame, fps, 22, 0.3, 0);
  const labelE = popIn(frame, fps, 30, 0.6, 30);
  const ctaE = popIn(frame, fps, 40, 0.6, 20);

  return (
    <AbsoluteFill
      style={{
        background: bg,
        fontFamily: FONT_BODY,
        alignItems: "center",
        justifyContent: "center",
        overflow: "hidden",
      }}
    >
      {/* Oversized accent block slamming in behind the number */}
      <div
        style={{
          position: "absolute",
          top: height * 0.34,
          left: "50%",
          width: width * 0.5,
          height: height * 0.32,
          background: accent,
          opacity: 0.9 * blockE.opacity,
          transform: `translateX(-50%) ${blockE.transform} rotate(-2deg)`,
        }}
      />

      <div
        style={{
          position: "relative",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: height * 0.015,
        }}
      >
        {/* Rotated stamp kicker */}
        {kicker ? (
          <div
            style={{
              opacity: kickerE.opacity,
              transform: `${kickerE.transform} rotate(-4deg)`,
              background: primaryDeep,
              color: panel,
              padding: "8px 20px",
              fontSize: height * 0.026,
              fontWeight: 800,
              letterSpacing: "0.08em",
              textTransform: "uppercase",
              marginBottom: height * 0.01,
            }}
          >
            {kicker}
          </div>
        ) : null}

        {/* The number, on the accent block, panel-coloured for contrast */}
        <div
          style={{
            display: "flex",
            alignItems: "flex-start",
            opacity: numE.opacity,
            transform: numE.transform,
            color: panel,
            lineHeight: 0.85,
          }}
        >
          {prefix ? (
            <span style={{ fontSize: height * 0.16, fontWeight: 900, marginRight: 4, marginTop: height * 0.02 }}>
              {prefix}
            </span>
          ) : null}
          <span
            style={{
              fontSize: height * 0.44,
              fontWeight: 900,
              letterSpacing: "-0.05em",
              fontVariantNumeric: "tabular-nums",
            }}
          >
            {current}
          </span>
        </div>

        {/* Suffix as a badge */}
        {suffix ? (
          <div
            style={{
              opacity: suffixE.opacity,
              transform: suffixE.transform,
              background: primaryDeep,
              color: panel,
              padding: "6px 18px",
              fontSize: height * 0.04,
              fontWeight: 900,
              letterSpacing: "0.02em",
              textTransform: "uppercase",
              marginTop: height * 0.01,
            }}
          >
            {suffix}
          </div>
        ) : null}

        {/* Supporting label in caps */}
        {label ? (
          <div
            style={{
              fontSize: height * 0.034,
              fontWeight: 800,
              textTransform: "uppercase",
              letterSpacing: "0.02em",
              color: text,
              opacity: labelE.opacity,
              transform: labelE.transform,
              marginTop: height * 0.02,
            }}
          >
            {label}
          </div>
        ) : null}

        {/* CTA line */}
        {cta ? (
          <div
            style={{
              fontSize: height * 0.024,
              fontWeight: 800,
              textTransform: "uppercase",
              letterSpacing: "0.06em",
              color: accent,
              opacity: ctaE.opacity,
              transform: ctaE.transform,
              marginTop: height * 0.02,
            }}
          >
            {cta}
          </div>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};
