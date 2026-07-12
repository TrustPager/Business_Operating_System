// ClaudeThinking — animated assistant mark + pulse, indicating "working".
// Shown after the assistant's first reply and before its result.
import React from "react";
import { useCurrentFrame } from "remotion";
import { AssistantMark } from "./chat-icons";
import { colors, fonts } from "../tokens";

export interface ClaudeThinkingProps {
  /** size of the mark in px. Default 24 */
  size?: number;
  /** Opacity multiplier (for fade-in/out from parent) */
  opacity?: number;
  /** Optional label next to the spinner. Default "Working..." */
  label?: string;
}

export const ClaudeThinking: React.FC<ClaudeThinkingProps> = ({
  size = 24,
  opacity = 1,
  label = "Working...",
}) => {
  const frame = useCurrentFrame();
  // Continuous rotation — one full turn every 1.6s (48 frames @ 30fps)
  const rotation = (frame / 48) * 360;
  // Subtle opacity pulse — 0.65 -> 1 -> 0.65 every 1s
  const pulse = 0.65 + 0.35 * (0.5 + 0.5 * Math.sin((frame / 15) * Math.PI));

  return (
    <div style={{
      display: "flex",
      alignItems: "center",
      gap: 10,
      opacity,
      paddingTop: 4,
      paddingBottom: 4,
    }}>
      <div style={{
        width: size,
        height: size,
        transform: "rotate(" + rotation + "deg)",
        opacity: pulse,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}>
        <AssistantMark size={size} color={colors.accentBrand} />
      </div>
      <span style={{
        fontFamily: fonts.ui,
        fontSize: 15,
        color: colors.text400,
        fontStyle: "italic",
        opacity: pulse,
      }}>
        {label}
      </span>
    </div>
  );
};
