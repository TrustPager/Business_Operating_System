/**
 * ApprovalPrompt — inline tool-use approval card the assistant renders in the
 * chat when a connected tool is invoked for the first time (Mode C add-on).
 */
import React from "react";
import { colors, fonts, accentRgb } from "../tokens";

const IconChevronRight = ({ size = 20, color = "currentColor" }: { size?: number; color?: string }) => (
  <svg width={size} height={size} viewBox="0 0 20 20" fill={color} xmlns="http://www.w3.org/2000/svg">
    <path d="M7.128 5.165a.5.5 0 0 1 .625-.097l.082.06 5 4.5a.5.5 0 0 1 .07.666l-.07.078-5 4.5a.501.501 0 0 1-.67-.744L11.752 10 7.165 5.872l-.068-.075a.5.5 0 0 1 .03-.632" />
  </svg>
);

const IconChevronDown = ({ size = 16, color = "currentColor" }: { size?: number; color?: string }) => (
  <svg width={size} height={size} viewBox="0 0 20 20" fill={color} xmlns="http://www.w3.org/2000/svg">
    <path d="M14.128 7.165a.502.502 0 0 1 .744.67l-4.5 5-.078.07a.5.5 0 0 1-.666-.07l-4.5-5-.06-.082a.501.501 0 0 1 .729-.656l.075.068L10 11.752z" />
  </svg>
);

export interface ApprovalPromptProps {
  toolName: string;
  serverName: string;
  logoSrc?: string;
  highlightAlwaysAllow?: boolean;
  highlightDeny?: boolean;
  maxWidth?: number;
  /**
   * Optional render-wrapper for the "Always allow" button (split-button group).
   * Use this to wrap the real rendered element in a ClickTarget so the cursor
   * lands on its true bounding box rather than a hand-measured coordinate.
   * Example:
   *   alwaysAllowWrapper={(btn) => <ClickTarget startFrame={N} color="primary">{btn}</ClickTarget>}
   */
  alwaysAllowWrapper?: (button: React.ReactNode) => React.ReactNode;
  /** Optional render-wrapper for the Deny button — same rationale as above. */
  denyWrapper?: (button: React.ReactNode) => React.ReactNode;
}

export function ApprovalPrompt({
  toolName,
  serverName,
  logoSrc,
  highlightAlwaysAllow = false,
  highlightDeny = false,
  maxWidth = 720,
  alwaysAllowWrapper,
  denyWrapper,
}: ApprovalPromptProps) {
  const highlightRing = `rgba(${accentRgb}, 0.30)`;
  return (
    <div style={{
      maxWidth,
      borderRadius: 12,
      border: `0.5px solid ${colors.border300}`,
      background: colors.bg000,
      padding: "8px 4px",
      fontFamily: fonts.ui,
      overflow: "hidden",
    }}>
      <div style={{
        display: "flex", alignItems: "center", gap: 16,
        padding: "8px 12px",
        borderRadius: 8,
        textAlign: "left",
        width: "100%",
      }}>
        <div style={{
          flexShrink: 0,
          width: 24, height: 24,
          borderRadius: 6.48,
          background: colors.bg000,
          border: `0.5px solid ${colors.border300}`,
          boxShadow: "0 1px 2px rgba(0,0,0,0.04)",
          display: "flex", alignItems: "center", justifyContent: "center",
          overflow: "hidden",
        }}>
          {logoSrc && <img src={logoSrc} width={16} height={16} alt="" style={{ objectFit: "contain" }} />}
        </div>

        <div style={{
          flex: 1, minWidth: 0,
          fontSize: 14, color: colors.text100,
        }}>
          Your assistant wants to use{" "}
          <span style={{ fontWeight: 600 }}>{toolName}</span>{" "}
          from{" "}
          <span style={{ fontWeight: 600 }}>{serverName}</span>
          <span style={{
            position: "relative", top: -1,
            marginLeft: 2, display: "inline-block", verticalAlign: "middle",
            color: colors.text500,
          }}>
            <IconChevronRight size={20} color={colors.text500} />
          </span>
        </div>
      </div>

      <div style={{ paddingLeft: 40, paddingTop: 8 }}>
        <div style={{ display: "flex", flexDirection: "column", gap: 12, padding: "0 12px 12px 12px" }}>
          <div style={{ display: "flex", gap: 8 }}>
            {(() => {
              const allowBtn = (
                <div style={{
                  display: "flex", height: 36, whiteSpace: "nowrap",
                  borderRadius: 8,
                  overflow: "hidden",
                  boxShadow: highlightAlwaysAllow
                    ? `0 0 0 3px ${highlightRing}, 0 1px 2px rgba(0,0,0,0.10)`
                    : "0 1px 2px rgba(0,0,0,0.10)",
                  transition: "box-shadow 0.2s ease",
                }}>
                  <div style={{
                    display: "flex", alignItems: "center", justifyContent: "center",
                    padding: "0 12px",
                    background: colors.text100, color: colors.bg100,
                    fontSize: 14, fontWeight: 600,
                    borderRight: "0.5px solid rgba(255,255,255,0.30)",
                  }}>
                    <span style={{ display: "flex", alignItems: "center" }}>
                      Always allow
                      <kbd style={{ marginLeft: 6, fontSize: 11, color: "rgba(255,255,255,0.55)", fontFamily: fonts.ui }}>⏎</kbd>
                    </span>
                  </div>
                  <div style={{
                    display: "flex", alignItems: "center", justifyContent: "center",
                    padding: "0 8px",
                    background: colors.text100, color: colors.bg100,
                  }}>
                    <IconChevronDown size={16} color={colors.bg100} />
                  </div>
                </div>
              );
              return alwaysAllowWrapper ? alwaysAllowWrapper(allowBtn) : allowBtn;
            })()}

            {(() => {
              const denyBtn = (
                <div style={{
                  display: "inline-flex", alignItems: "center", justifyContent: "center",
                  height: 36, padding: "0 16px",
                  borderRadius: 8,
                  border: `0.5px solid ${colors.border300}`,
                  background: colors.bg000,
                  color: colors.text100,
                  fontSize: 14, fontWeight: 600,
                  boxShadow: highlightDeny
                    ? `0 0 0 3px ${highlightRing}`
                    : "none",
                  transition: "box-shadow 0.2s ease",
                }}>
                  Deny
                  <kbd style={{ marginLeft: 6, fontSize: 11, color: colors.text500, fontFamily: fonts.ui }}>esc</kbd>
                </div>
              );
              return denyWrapper ? denyWrapper(denyBtn) : denyBtn;
            })()}
          </div>
        </div>
      </div>
    </div>
  );
}
