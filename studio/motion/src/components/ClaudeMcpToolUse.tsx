// ClaudeMcpToolUse — the active "assistant is using a tool" row that appears in
// the chat while a connected-tool call is in progress (Mode C add-on).
//
// Pattern:  [16px tool logo] [shimmer-animated verb text], with an accent
// spinner ring while active. When isActive=false the verb holds at a static
// muted colour (a "done" indicator paired with a status icon).
import React from "react";
import { useCurrentFrame, interpolate } from "remotion";
import { colors, fonts, accent } from "../tokens";

export interface ClaudeMcpToolUseProps {
  verb: string;
  logoSrc: string;
  isActive?: boolean;
  opacity?: number;
}

export const ClaudeMcpToolUse: React.FC<ClaudeMcpToolUseProps> = ({
  verb,
  logoSrc,
  isActive = true,
  opacity = 1,
}) => {
  const frame = useCurrentFrame();
  // Animate the gradient position to create a shimmering sweep.
  // 2.25s cycle (~67 frames @ 30fps).
  const CYCLE = 67;
  const t = (frame % CYCLE) / CYCLE;
  const bgPos = interpolate(t, [0, 1], [200, -100]); // moves the highlight left-to-right

  const textBaseColor = colors.text400; // muted neutral (token-driven)
  const textHighlight = colors.white;   // bright sweep peak

  const shimmerStyle: React.CSSProperties = isActive
    ? {
        backgroundImage: `linear-gradient(90deg, ${textBaseColor} 0%, ${textBaseColor} 30%, ${textHighlight} 50%, ${textBaseColor} 70%, ${textBaseColor} 100%)`,
        backgroundSize: "300% 100%",
        backgroundPosition: `${bgPos}% 50%`,
        WebkitBackgroundClip: "text",
        backgroundClip: "text",
        WebkitTextFillColor: "transparent",
        color: "transparent",
      }
    : { color: textBaseColor };

  return (
    <div style={{
      display: "flex",
      flexDirection: "row",
      alignItems: "center",
      gap: 10,
      padding: "6px 0",
      opacity,
    }}>
      <div style={{
        width: 24,
        height: 24,
        position: "relative",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        flexShrink: 0,
      }}>
        {isActive && (
          <div style={{
            position: "absolute",
            width: 22, height: 22,
            borderRadius: 999,
            border: "1.5px solid transparent",
            borderTopColor: accent,
            borderRightColor: accent,
            transform: `rotate(${(frame * 6) % 360}deg)`,
          }} />
        )}
        <img
          src={logoSrc}
          width={16}
          height={16}
          alt=""
          style={{ objectFit: "contain", display: "block", borderRadius: 3 }}
        />
      </div>
      <div style={{
        flex: 1,
        minWidth: 0,
        paddingLeft: 6,
      }}>
        <span
          style={{
            fontFamily: fonts.ui,
            fontSize: 14,
            fontWeight: 500,
            textAlign: "left",
            ...shimmerStyle,
          }}
        >
          {verb}
        </span>
      </div>
    </div>
  );
};
