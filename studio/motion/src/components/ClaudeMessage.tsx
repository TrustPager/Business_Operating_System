// ClaudeMessage — left-aligned assistant response in the active chat view.
// Vertical order (top to bottom):
//   1. Thought line (optional)  — muted single-line summary with chevron
//   2. Response body            — main content
//   3. Action bar (optional)    — copy + retry buttons
//   4. Assistant mark (optional)— small accent spark
import React from "react";
import { colors, fonts } from "../tokens";
import { AssistantMark } from "./chat-icons";

export interface ClaudeMessageProps {
  text?: string;
  thoughtLine?: string | null;
  showWordmark?: boolean;
  showActions?: boolean;
  opacity?: number;
  /** px translateY for slide-in animations */
  translateY?: number;
}

const ChevronDownIcon: React.FC<{ size?: number }> = ({ size = 12 }) => (
  <svg width={size} height={size} viewBox="0 0 20 20" fill="currentColor">
    <path d="M14.128 7.165a.502.502 0 0 1 .744.67l-4.5 5-.078.07a.5.5 0 0 1-.666-.07l-4.5-5-.06-.082a.501.501 0 0 1 .729-.656l.075.068L10 11.752z" />
  </svg>
);

const CopyIcon: React.FC<{ size?: number }> = ({ size = 20 }) => (
  <svg width={size} height={size} viewBox="0 0 20 20" fill="currentColor">
    <path d="M12.5 3A1.5 1.5 0 0 1 14 4.5V6h1.5A1.5 1.5 0 0 1 17 7.5v8a1.5 1.5 0 0 1-1.5 1.5h-8A1.5 1.5 0 0 1 6 15.5V14H4.5A1.5 1.5 0 0 1 3 12.5v-8A1.5 1.5 0 0 1 4.5 3zm1.5 9.5a1.5 1.5 0 0 1-1.5 1.5H7v1.5a.5.5 0 0 0 .5.5h8a.5.5 0 0 0 .5-.5v-8a.5.5 0 0 0-.5-.5H14zM4.5 4a.5.5 0 0 0-.5.5v8a.5.5 0 0 0 .5.5h8a.5.5 0 0 0 .5-.5v-8a.5.5 0 0 0-.5-.5z" />
  </svg>
);

const RetryIcon: React.FC<{ size?: number }> = ({ size = 20 }) => (
  <svg width={size} height={size} viewBox="0 0 20 20" fill="currentColor">
    <path d="M10.386 2.51A7.5 7.5 0 1 1 5.499 4H3a.5.5 0 0 1 0-1h3.5a.5.5 0 0 1 .49.402L7 3.5V7a.5.5 0 0 1-1 0V4.879a6.5 6.5 0 1 0 4.335-1.37L10 3.5l-.1-.01a.5.5 0 0 1 .1-.99z" />
  </svg>
);

const ActionButton: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div
    style={{
      width: 32,
      height: 32,
      borderRadius: 6,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      color: colors.text500,
    }}
  >
    {children}
  </div>
);

export const ClaudeMessage: React.FC<ClaudeMessageProps> = ({
  text = "",
  thoughtLine = null,
  showWordmark = true,
  showActions = true,
  opacity = 1,
  translateY = 0,
}) => {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        width: "100%",
        opacity,
        transform: `translateY(${translateY}px)`,
        paddingRight: 32,
      }}
    >
      {thoughtLine && (
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 6,
            paddingLeft: 8,
            paddingBottom: 6,
            color: colors.text500,
            fontFamily: fonts.ui,
            fontSize: 14,
            lineHeight: 1.4,
          }}
        >
          <span
            style={{
              overflow: "hidden",
              textOverflow: "ellipsis",
              whiteSpace: "nowrap",
              maxWidth: 520,
            }}
          >
            {thoughtLine}
          </span>
          <span style={{ transform: "rotate(-90deg)", display: "inline-flex" }}>
            <ChevronDownIcon size={12} />
          </span>
        </div>
      )}

      <div
        style={{
          paddingLeft: 8,
          fontFamily: fonts.ui,
          fontSize: 18,
          lineHeight: 1.7,
          color: colors.text100,
          whiteSpace: "pre-wrap",
          wordBreak: "break-word",
        }}
      >
        {text}
      </div>

      {showActions && (
        <div
          style={{
            display: "flex",
            justifyContent: "flex-start",
            alignItems: "center",
            marginTop: 4,
          }}
        >
          <ActionButton>
            <CopyIcon size={20} />
          </ActionButton>
          <ActionButton>
            <RetryIcon size={20} />
          </ActionButton>
        </div>
      )}

      {showWordmark && (
        <div
          style={{
            display: "flex",
            alignItems: "center",
            marginLeft: 4,
            marginTop: 24,
            color: colors.accentBrand,
          }}
        >
          <AssistantMark size={28} color={colors.accentBrand} />
        </div>
      )}
    </div>
  );
};
