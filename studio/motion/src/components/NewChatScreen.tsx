// NewChatScreen — the "new chat" landing screen: workspace badge + greeting +
// composer + prompt chips (Mode C add-on). All copy + chip data come from props.
import React from "react";
import { useCurrentFrame, interpolate } from "remotion";
import { colors, fonts, app } from "../tokens";
import {
  AssistantMark,
  WorkspaceIcon,
  PencilIcon,
  GraduationIcon,
  CodeBracketsIcon,
  BriefcaseIcon,
} from "./chat-icons";
import { WorkspaceBadge, PromptChip } from "./chat-primitives";
import { Composer } from "./Composer";

const CHIP_ICONS: Record<string, React.ComponentType<{ size?: number; style?: React.CSSProperties }>> = {
  pencil: PencilIcon,
  graduation: GraduationIcon,
  "code-brackets": CodeBracketsIcon,
  briefcase: BriefcaseIcon,
};

interface AttachedFile {
  name: string;
  meta?: string;
}

// File-chip row rendered ABOVE the composer when files are attached to a draft.
// Colours are token-driven (the "app / primary" family for the file glyph).
const AttachmentRow = ({ files }: { files: AttachedFile[] }) => (
  <div style={{
    display: "flex", flexWrap: "wrap", gap: 8,
    marginBottom: 10, paddingLeft: 4,
    width: 672, maxWidth: "100%",
  }}>
    {files.map((f, i) => (
      <div key={i} style={{
        display: "inline-flex", alignItems: "center", gap: 8,
        padding: "7px 12px",
        borderRadius: 10,
        background: colors.bg200,
        border: `1px solid ${colors.border200}`,
        fontFamily: fonts.ui,
        fontSize: 12.5,
        color: colors.text100,
      }}>
        {/* Tiny file glyph, tinted from the owner's primary colour */}
        <div style={{
          width: 18, height: 22, borderRadius: 3,
          background: colors.bg200, border: `1px solid ${app}`,
          color: app,
          display: "inline-flex", alignItems: "center", justifyContent: "center",
          fontSize: 7.5, fontWeight: 700, letterSpacing: 0.3,
        }}>CSV</div>
        <span style={{ fontWeight: 500 }}>{f.name}</span>
        {f.meta ? (
          <span style={{ color: colors.text500, fontVariantNumeric: "tabular-nums" }}>{f.meta}</span>
        ) : null}
      </div>
    ))}
  </div>
);

interface NewChatUser {
  name: string;
  workspace: string;
}

export const NewChatScreen = ({
  user = { name: "You", workspace: "Your workspace" },
  greeting = { prefix: "Back at it,", name: "you" },
  composer = { placeholder: "How can I help you today?", model: "Assistant", modelMode: "Adaptive" },
  promptChips = [],
  composerState,
  typedText,
  cursorVisible,
  highlightedTarget,
  composerValue,
  highlightSend = false,
  attachedFiles = null,
}: {
  user?: NewChatUser;
  greeting?: { prefix: string; name: string };
  composer?: { placeholder?: string; model?: string; modelMode?: string };
  promptChips?: { id: string; label: string; icon?: string }[];
  composerState?: "empty" | "typing" | "submitted";
  typedText?: string;
  cursorVisible?: boolean;
  highlightedTarget?: string | null;
  composerValue?: string;
  highlightSend?: boolean;
  attachedFiles?: AttachedFile[] | null;
}) => {
  const frame = useCurrentFrame();
  const pulseT = frame % 60;
  const pulseOpacity = interpolate(pulseT, [0, 30, 60], [0.5, 1.0, 0.5], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const effectiveState = composerValue !== undefined ? "typing" : composerState;
  const effectiveTyped = composerValue !== undefined ? composerValue : typedText;
  const effectiveCursorVisible = composerValue !== undefined ? true : cursorVisible;

  const btnSize = 32;
  const ringInset = 4;
  const ringSize = btnSize + ringInset * 2;

  return (
    <div style={{
      width: "100%", height: "100%", backgroundColor: colors.bg100,
      display: "flex", flexDirection: "column", alignItems: "center",
      paddingTop: "20vh", gap: 28, position: "relative",
    }}>
      <WorkspaceBadge label={user.workspace} icon={WorkspaceIcon} />

      <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
        <AssistantMark size={40} color={colors.accentBrand} />
        <span style={{
          fontFamily: fonts.display,
          fontSize: 40,
          fontWeight: 400,
          color: colors.text200,
          lineHeight: 1.2,
        }}>
          {greeting.prefix} {greeting.name}
        </span>
      </div>

      <div style={{ position: "relative", display: "flex", flexDirection: "column", alignItems: "center", width: "100%" }}>
        {attachedFiles && attachedFiles.length > 0 ? (
          <AttachmentRow files={attachedFiles} />
        ) : null}
        <Composer
          composerState={effectiveState}
          typedText={effectiveTyped}
          cursorVisible={effectiveCursorVisible}
          placeholder={composer.placeholder}
          modelLabel={composer.model}
          modelMode={composer.modelMode}
          highlightedTarget={highlightedTarget}
        />
        {highlightSend && (
          <div style={{
            position: "absolute",
            top: 0,
            left: "calc(50% + 336px - 14px - 16px - 4px)",
            marginTop: 96 - ringSize / 2,
            width: ringSize,
            height: ringSize,
            borderRadius: 9999,
            border: `2px solid ${colors.accentBrand}`,
            opacity: pulseOpacity,
            pointerEvents: "none",
            zIndex: 10,
          }} />
        )}
      </div>

      <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap: 8, paddingTop: 16, maxWidth: 700 }}>
        {promptChips.map((chip) => {
          const Icon = chip.icon ? CHIP_ICONS[chip.icon] : undefined;
          return <PromptChip key={chip.id} label={chip.label} icon={Icon} />;
        })}
      </div>
    </div>
  );
};
