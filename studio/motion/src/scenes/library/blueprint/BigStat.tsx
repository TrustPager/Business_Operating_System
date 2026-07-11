// BigStat (Blueprint) — the number as a measured dimension. It counts up in the
// mono face, a dimension line with end-ticks plots across its width beneath it
// (the value read off the sheet), and a crosshair registers the reading. A mono
// kicker and label frame it as a spec callout, not a hero caption.
//
// Structured props: value (+ prefix/suffix/label/kicker/cta/decimals).
import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Easing,
} from "remotion";
import { text, textMuted, primary, accent } from "../../../tokens";
import { FONT_MONO } from "../../../fonts";
import { GraphPaper } from "./GraphPaper";
import { measuredIn, drawIn, monoLabel } from "./_shared";

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
  const { width, height } = useVideoConfig();

  const t = interpolate(frame, [10, 46], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  const current = (value * t).toFixed(decimals);

  const numE = measuredIn(frame, 6, 16);
  const kickerE = measuredIn(frame, 0, 12);
  const dimGrow = drawIn(frame, 26, 22);
  const labelE = measuredIn(frame, 34, 14);
  const ctaE = measuredIn(frame, 44, 14);

  const dimW = width * 0.3;

  return (
    <GraphPaper>
      <div
        style={{
          position: "absolute",
          inset: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          gap: height * 0.02,
        }}
      >
        {/* Kicker between marker ticks */}
        {kicker ? (
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 14,
              opacity: kickerE.opacity,
              transform: kickerE.transform,
            }}
          >
            <div style={{ width: 8, height: 8, background: accent }} />
            <span style={monoLabel(height * 0.02)}>{kicker}</span>
            <div style={{ width: 8, height: 8, background: accent }} />
          </div>
        ) : null}

        {/* The measured number */}
        <div
          style={{
            position: "relative",
            display: "flex",
            alignItems: "flex-end",
            opacity: numE.opacity,
            transform: numE.transform,
            fontFamily: FONT_MONO,
            color: text,
            lineHeight: 0.9,
          }}
        >
          {prefix ? (
            <span style={{ fontSize: height * 0.14, fontWeight: 500, color: primary, marginRight: 6 }}>
              {prefix}
            </span>
          ) : null}
          <span
            style={{
              fontSize: height * 0.34,
              fontWeight: 600,
              letterSpacing: "-0.03em",
              fontVariantNumeric: "tabular-nums",
            }}
          >
            {current}
          </span>
          {suffix ? (
            <span
              style={{
                fontSize: height * 0.07,
                fontWeight: 500,
                color: primary,
                marginLeft: 12,
                marginBottom: height * 0.03,
              }}
            >
              {suffix}
            </span>
          ) : null}
          {/* registration crosshair top-right of the reading */}
          <div style={{ position: "absolute", right: -height * 0.05, top: -height * 0.02, opacity: dimGrow }}>
            <div style={{ position: "absolute", width: height * 0.03, height: 1, background: accent, top: 0, left: -height * 0.015 }} />
            <div style={{ position: "absolute", width: 1, height: height * 0.03, background: accent, top: -height * 0.015, left: 0 }} />
          </div>
        </div>

        {/* Dimension line with end-ticks under the reading */}
        <div style={{ position: "relative", width: dimW, height: 18, marginTop: height * 0.01 }}>
          <div style={{ position: "absolute", left: "50%", top: 0, transform: "translateX(-50%)", width: dimW * dimGrow, height: 1, background: primary }} />
          <div style={{ position: "absolute", left: `calc(50% - ${dimW / 2}px)`, top: -8, width: 1, height: 16, background: primary, opacity: dimGrow > 0 ? 1 : 0 }} />
          <div style={{ position: "absolute", left: `calc(50% + ${dimW / 2}px)`, top: -8, width: 1, height: 16, background: primary, opacity: dimGrow > 0.98 ? 1 : 0 }} />
        </div>

        {/* Supporting label */}
        {label ? (
          <div
            style={{
              ...monoLabel(height * 0.02, text),
              fontWeight: 500,
              opacity: labelE.opacity,
              transform: labelE.transform,
              marginTop: height * 0.012,
            }}
          >
            {label}
          </div>
        ) : null}

        {/* CTA note */}
        {cta ? (
          <div
            style={{
              ...monoLabel(height * 0.016, textMuted),
              opacity: ctaE.opacity,
              transform: ctaE.transform,
              marginTop: height * 0.025,
            }}
          >
            {cta}
          </div>
        ) : null}
      </div>
    </GraphPaper>
  );
};
