// AutomationPreviewCard — small popover card showing a just-built automation.
// Appears near the element it belongs to (positioned by parent).
// Format: bolt icon + title row, then "When ..." trigger and "Then ..." action rows.
import React from "react";
import {useCurrentFrame, interpolate, Easing} from "remotion";
import {colors, fonts, shadows} from "../tokens";

export interface AutomationPreviewCardProps {
  title: string;
  trigger: string;
  action: string;
  /** Top-left position in fractional canvas coords (0..1). */
  position: {x: number; y: number};
  appearFrame: number;
  /** Optional fade-out frame. */
  disappearFrame?: number;
  width?: number;
}

// Lucide "zap" icon — matches a typical automation button glyph.
const MiniBolt: React.FC<{color: string}> = ({color}) => (
  <svg
    width={16}
    height={16}
    viewBox="0 0 24 24"
    fill="none"
    stroke={color}
    strokeWidth={2}
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z" />
  </svg>
);

export const AutomationPreviewCard: React.FC<AutomationPreviewCardProps> = ({
  title,
  trigger,
  action,
  position,
  appearFrame,
  disappearFrame,
  width = 320,
}) => {
  const frame = useCurrentFrame();
  if (frame < appearFrame) return null;
  if (disappearFrame !== undefined && frame > disappearFrame) return null;

  const local = frame - appearFrame;
  const fadeIn = interpolate(local, [0, 12], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const slideY = interpolate(local, [0, 18], [14, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });
  const fadeOut =
    disappearFrame !== undefined
      ? interpolate(frame, [disappearFrame - 12, disappearFrame], [1, 0], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        })
      : 1;
  const opacity = Math.min(fadeIn, fadeOut);

  const x = position.x * 1920;
  const y = position.y * 1080;

  const labelStyle: React.CSSProperties = {
    fontFamily: fonts.ui,
    fontSize: 11,
    fontWeight: 600,
    color: colors.text400,
    textTransform: "uppercase",
    letterSpacing: "0.05em",
    marginBottom: 3,
  };
  const valueStyle: React.CSSProperties = {
    fontFamily: fonts.ui,
    fontSize: 13.5,
    color: colors.text200,
    lineHeight: 1.45,
  };

  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        width,
        backgroundColor: colors.bg000,
        borderRadius: 12,
        boxShadow: `${shadows.overlay}, 0 0 0 1px ${colors.border300}`,
        padding: "10px 14px",
        opacity,
        transform: `translateY(${slideY}px)`,
        zIndex: 90,
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 8,
          paddingBottom: 8,
          borderBottom: `1px solid ${colors.border100}`,
          marginBottom: 8,
        }}
      >
        <MiniBolt color={colors.accentBrand} />
        <span
          style={{
            fontFamily: fonts.ui,
            fontSize: 15,
            fontWeight: 600,
            color: colors.text100,
          }}
        >
          {title}
        </span>
      </div>

      <div style={{marginBottom: 8}}>
        <div style={labelStyle}>When</div>
        <div style={valueStyle}>{trigger}</div>
      </div>

      <div>
        <div style={labelStyle}>Then</div>
        <div style={valueStyle}>{action}</div>
      </div>
    </div>
  );
};
