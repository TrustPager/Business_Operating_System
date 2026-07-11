// Sidebar — collapsible vertical nav rail for the product-demo chat kit.
// Renders icons-only by default; expands to show labels when sidebarProgress > 0.
// All nav items are driven by data, not hardcoded — safe to swap order/items.
import React from "react";
import { colors, fonts, sizing } from "../tokens";
import {
  PlusIcon,
  SearchIcon,
  ChatsIcon,
  ProjectsIcon,
  CodeIcon,
  CustomizeIcon,
  DesignIcon,
  ChevronDownIcon,
  SidebarToggleIcon,
  DownloadIcon,
} from "./chat-icons";
import { Avatar } from "./chat-primitives";

const ICON_MAP: Record<string, React.ComponentType<{ size?: number }>> = {
  plus: PlusIcon, search: SearchIcon, chats: ChatsIcon, projects: ProjectsIcon,
  code: CodeIcon, customize: CustomizeIcon, design: DesignIcon, download: DownloadIcon,
};

const SidebarItem: React.FC<{
  icon: string;
  label?: string;
  sidebarProgress?: number;
  hasPing?: boolean;
  isPrimary?: boolean;
}> = ({ icon, label, sidebarProgress = 0, hasPing = false, isPrimary = false }) => {
  const Icon = ICON_MAP[icon];
  if (!Icon) return null;
  const labelOpacity = sidebarProgress > 0.4 ? (sidebarProgress - 0.4) / 0.6 : 0;
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 12, height: 32, padding: "0 8px", margin: "0 8px", borderRadius: 8, color: colors.text100, position: "relative" }}>
      <div style={{ width: 28, height: 28, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, ...(isPrimary ? { backgroundColor: "rgba(120, 120, 130, 0.15)", borderRadius: 9999, width: 22, height: 22, marginLeft: 3 } : {}) }}>
        <Icon size={isPrimary ? 16 : 20} />
      </div>
      {label && <span style={{ fontFamily: fonts.ui, fontSize: 14, fontWeight: 400, color: colors.text100, opacity: labelOpacity, whiteSpace: "nowrap", overflow: "hidden" }}>{label}</span>}
      {hasPing && <span style={{ position: "absolute", top: 2, right: 4, width: 8, height: 8, borderRadius: 9999, backgroundColor: colors.accentBrand }} />}
    </div>
  );
};

export interface SidebarUser {
  initial: string;
  name: string;
  workspace: string;
}

export interface SidebarNavItem {
  icon: string;
  label: string;
}

export const Sidebar = ({
  sidebarProgress = 0,
  user = { initial: "A", name: "Your assistant", workspace: "Your workspace" },
  navItems = [],
  showRecents = false,
  recents = [],
}: {
  sidebarProgress?: number;
  user?: SidebarUser;
  navItems?: SidebarNavItem[];
  showRecents?: boolean;
  recents?: string[];
}) => {
  const width = sizing.sidebarCollapsedWidth + (sizing.sidebarExpandedWidth - sizing.sidebarCollapsedWidth) * sidebarProgress;
  const showLabels = sidebarProgress > 0.2;
  return (
    <div style={{ width, height: "100%", backgroundColor: colors.bg100, borderRight: "0.5px solid " + colors.border200, display: "flex", flexDirection: "column", flexShrink: 0, overflow: "hidden" }}>
      <div style={{ padding: 8, display: "flex", alignItems: "center", justifyContent: "flex-end", height: 48 }}>
        <div style={{ width: 32, height: 32, display: "flex", alignItems: "center", justifyContent: "center", color: colors.text400 }}>
          <SidebarToggleIcon size={20} />
        </div>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 1 }}>
        {navItems.map((item, i) => (
          <SidebarItem key={i} icon={item.icon} label={showLabels ? item.label : ""} sidebarProgress={sidebarProgress} isPrimary={item.icon === "plus"} />
        ))}
      </div>
      <div style={{ flexGrow: 1 }} />
      {showRecents && sidebarProgress > 0.7 && recents.length > 0 && (
        <div style={{ padding: "0 8px", opacity: (sidebarProgress - 0.7) / 0.3 }}>
          <h2 style={{ fontFamily: fonts.ui, fontSize: 12, fontWeight: 400, color: colors.text500, padding: "8px 8px 4px 8px", margin: 0 }}>Recents</h2>
          {recents.slice(0, 6).map((r, i) => (
            <div key={i} style={{ fontFamily: fonts.ui, fontSize: 14, color: colors.text200, padding: "6px 8px", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis", borderRadius: 8 }}>{r}</div>
          ))}
        </div>
      )}
      <div style={{ padding: 8, position: "relative" }}>
        <SidebarItem icon="download" label="" sidebarProgress={sidebarProgress} hasPing />
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 8, padding: 12, borderTop: "0.5px solid " + colors.border100 }}>
        <Avatar initial={user.initial} size={36} />
        {showLabels && (
          <div style={{ flex: 1, minWidth: 0, opacity: (sidebarProgress - 0.2) / 0.8 }}>
            <div style={{ fontFamily: fonts.ui, fontSize: 14, fontWeight: 500, color: colors.text100, lineHeight: 1.2, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{user.name}</div>
            <div style={{ fontFamily: fonts.ui, fontSize: 12, color: colors.text500, lineHeight: 1.2, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{user.workspace}</div>
          </div>
        )}
        {showLabels && (
          <div style={{ color: colors.text400, opacity: (sidebarProgress - 0.2) / 0.8 }}>
            <ChevronDownIcon size={14} />
          </div>
        )}
      </div>
    </div>
  );
};
