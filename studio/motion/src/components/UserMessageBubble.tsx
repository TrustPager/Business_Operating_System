// UserMessageBubble — right-aligned user message in the active chat view.
import React from "react";
import { colors, fonts } from "../tokens";

export interface UserMessageBubbleProps {
  text: string;
  opacity?: number;
  translateY?: number;
}

export const UserMessageBubble: React.FC<UserMessageBubbleProps> = ({
  text,
  opacity = 1,
  translateY = 0,
}) => {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "flex-end",
        width: "100%",
        opacity,
        transform: `translateY(${translateY}px)`,
      }}
    >
      <div
        style={{
          backgroundColor: colors.bg300,
          color: colors.text100,
          borderRadius: 12,
          padding: "10px 16px",
          maxWidth: "85%",
          fontFamily: fonts.ui,
          fontSize: 17,
          lineHeight: 1.55,
          whiteSpace: "pre-wrap",
          wordBreak: "break-word",
        }}
      >
        {text}
      </div>
    </div>
  );
};
