// chat-primitives.tsx — atoms for the product-demo chat kit (Mode C add-on).
// Ported from the RVS Claude chat kit; every colour/size flows from the token
// bridge (../tokens), never a baked literal.
import React from "react";
import { colors, fonts, sizing, motion } from "../tokens";

// ---------- Avatar ----------
export const Avatar = ({
  initial,
  size = sizing.avatarSize,
  bg,
  color,
}: {
  initial: string;
  size?: number;
  bg?: string;
  color?: string;
}) => (
  <div
    style={{
      width: size,
      height: size,
      borderRadius: sizing.pillRadius,
      backgroundColor: bg || colors.text200,
      color: color || colors.bg100,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontFamily: fonts.ui,
      fontWeight: 700,
      fontSize: Math.round(size * 0.44),
      lineHeight: 1,
      flexShrink: 0,
      userSelect: "none",
    }}
  >
    {initial}
  </div>
);

// ---------- IconButton ----------
export const IconButton = ({
  icon: Icon,
  iconSize = sizing.iconSize,
  size = 32,
  color = colors.text400,
  bg = "transparent",
  rounded = sizing.buttonRadius,
  ariaLabel,
  style: extraStyle,
}: {
  icon: React.ComponentType<{ size?: number }>;
  iconSize?: number;
  size?: number;
  color?: string;
  bg?: string;
  rounded?: number;
  ariaLabel?: string;
  style?: React.CSSProperties;
}) => (
  <div
    aria-label={ariaLabel}
    style={{
      width: size,
      height: size,
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      borderRadius: rounded,
      backgroundColor: bg,
      color,
      flexShrink: 0,
      transition: `all ${motion.durationBase}ms ${motion.ease}`,
      ...extraStyle,
    }}
  >
    <Icon size={iconSize} />
  </div>
);

// ---------- Pill ----------
// The composer's model pill, and any chip-shaped label.
export const Pill = ({
  children,
  color = colors.text200,
  bg = "transparent",
  icon: Icon,
  trailingIcon: TrailingIcon,
}: {
  children: React.ReactNode;
  color?: string;
  bg?: string;
  icon?: React.ComponentType<{ size?: number }>;
  trailingIcon?: React.ComponentType<{ size?: number; style?: React.CSSProperties }>;
}) => (
  <div
    style={{
      display: "inline-flex",
      alignItems: "center",
      gap: 6,
      height: 32,
      paddingLeft: 10,
      paddingRight: TrailingIcon ? 8 : 10,
      borderRadius: sizing.buttonRadius,
      backgroundColor: bg,
      color,
      fontFamily: fonts.ui,
      fontSize: 14,
      fontWeight: 500,
      lineHeight: 1,
      whiteSpace: "nowrap",
      userSelect: "none",
    }}
  >
    {Icon && <Icon size={16} />}
    <span>{children}</span>
    {TrailingIcon && <TrailingIcon size={12} style={{ opacity: 0.75 }} />}
  </div>
);

// ---------- PromptChip ----------
export const PromptChip: React.FC<{
  label: string;
  icon?: React.ComponentType<{ size?: number; style?: React.CSSProperties }>;
  iconColor?: string;
}> = ({ label, icon: Icon, iconColor }) => (
  <button
    style={{
      display: "inline-flex",
      alignItems: "center",
      gap: 6,
      height: 32,
      paddingLeft: 10,
      paddingRight: 10,
      borderRadius: sizing.chipRadius,
      backgroundColor: colors.bg000,
      border: `0.5px solid ${colors.border200}`,
      color: colors.text200,
      fontFamily: fonts.ui,
      fontSize: 14,
      fontWeight: 400,
      lineHeight: 1,
      whiteSpace: "nowrap",
      cursor: "default",
      transition: `all ${motion.durationBase}ms ${motion.ease}`,
    }}
  >
    {Icon && <Icon size={20} style={{ color: iconColor || colors.text400, marginLeft: -2 }} />}
    <span>{label}</span>
  </button>
);

// ---------- WorkspaceBadge ----------
export const WorkspaceBadge = ({
  label,
  icon: Icon,
}: {
  label: string;
  icon?: React.ComponentType<{ size?: number; style?: React.CSSProperties }>;
}) => (
  <div
    style={{
      display: "inline-flex",
      alignItems: "center",
      gap: 6,
      height: 32,
      paddingLeft: 8,
      paddingRight: 10,
      borderRadius: sizing.buttonRadius,
      backgroundColor: colors.bg300,
      color: colors.text500,
      fontFamily: fonts.ui,
      fontSize: 14,
      fontWeight: 400,
      lineHeight: 1,
      whiteSpace: "nowrap",
      userSelect: "none",
    }}
  >
    {Icon && <Icon size={20} style={{ margin: "0 -2px" }} />}
    <span>{label}</span>
  </div>
);
