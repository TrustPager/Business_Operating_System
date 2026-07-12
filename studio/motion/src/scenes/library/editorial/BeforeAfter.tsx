// BeforeAfter — a genuine two-state transformation diagram, not a captioned
// slide. Two panels sit either side of the frame: the "before" state reads
// muted and flat; a connector arrow draws across the negative space; the
// "after" state lands elevated and in brand colour. The eye travels left→right
// and reads the change without a sentence.
//
// Structured props: subject (shared noun) + before/after {tag, value}.
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
  primaryTint,
  accent,
  shadows,
} from "../../../tokens";
import { FONT_BODY, FONT_SERIF } from "../../../fonts";
import { ConnectorLine } from "../../../compositor";
import { riseIn } from "./_shared";

export interface BeforeAfterProps {
  /** Small shared noun labelling what changes, e.g. "Quote". */
  subject?: string;
  before: { tag: string; value: string };
  after: { tag: string; value: string };
}

const StatePanel: React.FC<{
  centerX: number;
  centerY: number;
  w: number;
  h: number;
  tag: string;
  value: string;
  entrance: ReturnType<typeof riseIn>;
  variant: "muted" | "brand";
}> = ({ centerX, centerY, w, h, tag, value, entrance, variant }) => {
  const brand = variant === "brand";
  return (
    <div
      style={{
        position: "absolute",
        left: centerX - w / 2,
        top: centerY - h / 2,
        width: w,
        height: h,
        opacity: entrance.opacity,
        transform: entrance.transform,
        background: brand ? primaryTint : panel,
        border: `1px solid ${brand ? "transparent" : border}`,
        borderRadius: 24,
        boxShadow: brand ? shadows.overlay : shadows.card,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "flex-start",
        gap: 18,
        padding: "0 44px",
        fontFamily: FONT_BODY,
        boxSizing: "border-box",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 12,
        }}
      >
        <div
          style={{
            width: 8,
            height: 8,
            borderRadius: "50%",
            background: brand ? accent : textMuted,
          }}
        />
        <span
          style={{
            fontSize: 20,
            fontWeight: 700,
            letterSpacing: "0.2em",
            textTransform: "uppercase",
            color: brand ? primaryDeep : textMuted,
          }}
        >
          {tag}
        </span>
      </div>
      <div
        style={{
          fontFamily: FONT_SERIF,
          fontSize: h * 0.2,
          lineHeight: 0.98,
          fontWeight: 700,
          letterSpacing: "-0.03em",
          color: brand ? primaryDeep : text,
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
  const { fps, width, height } = useVideoConfig();

  const panelW = width * 0.32;
  const panelH = height * 0.4;
  const cy = height * 0.54;
  const leftCx = width * 0.27;
  const rightCx = width * 0.73;

  const leftE = riseIn(frame, fps, 6, 24);
  const rightE = riseIn(frame, fps, 34, 24);
  const subjectE = riseIn(frame, fps, 0, 18);

  return (
    <AbsoluteFill style={{ background: bg, fontFamily: FONT_BODY }}>
      {/* Shared subject label, centred above the pair */}
      {subject ? (
        <div
          style={{
            position: "absolute",
            top: height * 0.2,
            width: "100%",
            textAlign: "center",
            opacity: subjectE.opacity,
            transform: subjectE.transform,
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
            {subject}
          </span>
        </div>
      ) : null}

      <StatePanel
        centerX={leftCx}
        centerY={cy}
        w={panelW}
        h={panelH}
        tag={before.tag}
        value={before.value}
        entrance={leftE}
        variant="muted"
      />

      {/* Transformation arrow across the negative space */}
      <ConnectorLine
        from={{ x: (leftCx + panelW / 2) / width + 0.01, y: cy / height }}
        to={{ x: (rightCx - panelW / 2) / width - 0.01, y: cy / height }}
        appearAt={26}
        drawDurationFrames={16}
        curve={0}
        strokeWidth={2}
        color={accent}
      />

      <StatePanel
        centerX={rightCx}
        centerY={cy}
        w={panelW}
        h={panelH}
        tag={after.tag}
        value={after.value}
        entrance={rightE}
        variant="brand"
      />
    </AbsoluteFill>
  );
};
