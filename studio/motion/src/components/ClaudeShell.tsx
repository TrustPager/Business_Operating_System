// ClaudeShell — sidebar + content slot + floating top-right button.
// Every chat composition wraps its content in this. Pass children for the screen.
// Part of the product-demo chat kit (Mode C add-on).
import React from "react";
import { useCurrentFrame, interpolate, staticFile } from "remotion";
import { colors, fonts } from "../tokens";
import { Sidebar, type SidebarUser, type SidebarNavItem } from "./Sidebar";
import { IncognitoIcon } from "./chat-icons";

export const ClaudeShell = ({
  children,
  sidebarProgress = 0,
  user,
  navItems = [],
  recents = [],
  showRecents = false,
  highlightProfile = false,
  activeConnector,
  connectorLogo,
}: {
  children: React.ReactNode;
  sidebarProgress?: number;
  user?: SidebarUser;
  navItems?: SidebarNavItem[];
  recents?: string[];
  showRecents?: boolean;
  highlightProfile?: boolean;
  activeConnector?: string | null;
  /** staticFile path (under public/) for the connected-tool logo shown in the pill.
   *  Brand-neutral: the owner supplies their own; no product favicon is baked. */
  connectorLogo?: string | null;
}) => {
  const frame = useCurrentFrame();
  // 60-frame pulse: 0.5 -> 1.0 -> 0.5
  const pulseT = frame % 60;
  const pulseOpacity = interpolate(pulseT, [0, 30, 60], [0.5, 1.0, 0.5], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const avatarSize = 36;
  const avatarPad = 12;
  const ringInset = 4;
  const ringSize = avatarSize + ringInset * 2;

  return (
    <div style={{
      width: "100%", height: "100%", backgroundColor: colors.bg100,
      display: "flex", flexDirection: "row", overflow: "hidden", position: "relative",
    }}>
      <Sidebar
        sidebarProgress={sidebarProgress}
        user={user}
        navItems={navItems}
        recents={recents}
        showRecents={showRecents}
      />

      {/* Active connector pill - between Recents and profile footer */}
      {activeConnector && sidebarProgress > 0.7 && (
        <div style={{
          position: "absolute",
          left: 12,
          bottom: avatarPad + avatarSize + 12 + 16,
          opacity: (sidebarProgress - 0.7) / 0.3,
          zIndex: 5,
        }}>
          <div style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 8,
            padding: "6px 12px",
            borderRadius: 9999,
            backgroundColor: colors.bg200,
            color: colors.text200,
            fontFamily: fonts.ui,
            fontSize: 13,
            fontWeight: 500,
            whiteSpace: "nowrap",
          }}>
            {connectorLogo && (
              <img
                src={staticFile(connectorLogo)}
                width={16}
                height={16}
                alt=""
                style={{ objectFit: "contain", display: "block" }}
              />
            )}
            <span>{activeConnector}</span>
          </div>
        </div>
      )}

      {/* Profile chip pulse ring (bottom-left of sidebar) */}
      {highlightProfile && (
        <div style={{
          position: "absolute",
          left: avatarPad - ringInset,
          bottom: avatarPad - ringInset,
          width: ringSize,
          height: ringSize,
          borderRadius: 9999,
          border: `2px solid ${colors.accentBrand}`,
          opacity: pulseOpacity,
          pointerEvents: "none",
          zIndex: 10,
        }} />
      )}

      <div style={{ flex: 1, position: "relative", overflow: "hidden" }}>
        {children}
        <div style={{
          position: "absolute", top: 14, right: 14,
          width: 32, height: 32, display: "flex", alignItems: "center", justifyContent: "center",
          borderRadius: 8, color: colors.text400,
        }}>
          <IncognitoIcon size={20} />
        </div>
      </div>
    </div>
  );
};
