// BeforeAfter (Pop) — a head-to-head slam. The "before" crashes in from the left
// as a muted, struck-through block; the "after" crashes in from the right as a
// bigger, accent-filled stamp; a heavy arrow pops between them. Kinetic, high
// contrast, unmistakably a versus. Not two tidy captioned cards.
//
// Structured props: subject + before/after {tag, value}.
import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { bg, text, textMuted, panel, primaryTint, accent, primaryDeep } from "../../../tokens";
import { FONT_BODY } from "../../../fonts";
import { popIn, slamIn } from "./_shared";

export interface BeforeAfterProps {
  subject?: string;
  before: { tag: string; value: string };
  after: { tag: string; value: string };
}

const Block: React.FC<{
  cx: number;
  cy: number;
  w: number;
  h: number;
  tag: string;
  value: string;
  variant: "before" | "after";
  opacity: number;
  transform: string;
}> = ({ cx, cy, w, h, tag, value, variant, opacity, transform }) => {
  const after = variant === "after";
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
        background: after ? accent : primaryTint,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        gap: 14,
        fontFamily: FONT_BODY,
        boxSizing: "border-box",
        padding: "0 24px",
      }}
    >
      <span
        style={{
          fontSize: h * 0.12,
          fontWeight: 800,
          letterSpacing: "0.1em",
          textTransform: "uppercase",
          color: after ? panel : textMuted,
        }}
      >
        {tag}
      </span>
      <div
        style={{
          fontSize: h * 0.26,
          lineHeight: 0.95,
          fontWeight: 900,
          letterSpacing: "-0.03em",
          textTransform: "uppercase",
          textAlign: "center",
          color: after ? panel : text,
          textDecoration: after ? "none" : "line-through",
          textDecorationThickness: after ? undefined : "3px",
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
  const { fps, width, height } = useVideoConfig();

  const beforeW = width * 0.3;
  const beforeH = height * 0.36;
  const afterW = width * 0.34;
  const afterH = height * 0.44;
  const cy = height * 0.56;
  const leftCx = width * 0.27;
  const rightCx = width * 0.73;

  const leftE = slamIn(frame, fps, 4, -width * 0.5);
  const rightE = slamIn(frame, fps, 18, width * 0.5);
  const arrowE = popIn(frame, fps, 30, 0.3, 0);
  const subjectE = popIn(frame, fps, 0, 0.5, 0);

  return (
    <AbsoluteFill style={{ background: bg, fontFamily: FONT_BODY, overflow: "hidden" }}>
      {/* Subject stamp */}
      {subject ? (
        <div
          style={{
            position: "absolute",
            top: height * 0.18,
            width: "100%",
            textAlign: "center",
            opacity: subjectE.opacity,
            transform: subjectE.transform,
          }}
        >
          <span
            style={{
              display: "inline-block",
              background: primaryDeep,
              color: panel,
              padding: "8px 22px",
              fontSize: height * 0.03,
              fontWeight: 800,
              letterSpacing: "0.08em",
              textTransform: "uppercase",
            }}
          >
            {subject}
          </span>
        </div>
      ) : null}

      <Block
        cx={leftCx}
        cy={cy}
        w={beforeW}
        h={beforeH}
        tag={before.tag}
        value={before.value}
        variant="before"
        opacity={leftE.opacity}
        transform={leftE.transform}
      />

      {/* Heavy arrow popping between */}
      <div
        style={{
          position: "absolute",
          left: width * 0.5,
          top: cy,
          transform: `translate(-50%, -50%) ${arrowE.transform}`,
          opacity: arrowE.opacity,
          fontSize: height * 0.13,
          fontWeight: 900,
          color: primaryDeep,
          lineHeight: 1,
        }}
      >
        →
      </div>

      <Block
        cx={rightCx}
        cy={cy}
        w={afterW}
        h={afterH}
        tag={after.tag}
        value={after.value}
        variant="after"
        opacity={rightE.opacity}
        transform={rightE.transform}
      />
    </AbsoluteFill>
  );
};
