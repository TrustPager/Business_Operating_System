// Composer — the input box card in the chat kit (Mode C add-on).
// State: 'empty' | 'typing' | 'submitted'. Reads typedText + cursorVisible when typing.
import React from "react";
import { colors, fonts, sizing, shadows } from "../tokens";
import { PlusIcon, ChevronDownIcon, VoiceWaveIcon } from "./chat-icons";
import { Pill } from "./chat-primitives";

export const Composer = ({
  composerState = "empty",
  typedText = "",
  cursorVisible = true,
  placeholder = "How can I help you today?",
  modelLabel = "Assistant",
  modelMode = "Adaptive",
  highlightedTarget = null,
}: {
  composerState?: string;
  typedText?: string;
  cursorVisible?: boolean;
  placeholder?: string;
  modelLabel?: string;
  modelMode?: string;
  highlightedTarget?: string | null;
}) => {
  const isHighlighted = highlightedTarget === "composer";
  const showText = composerState === "typing" && typedText.length > 0;
  return (
    <div style={{
      width: sizing.composerMaxWidth,
      maxWidth: "95%",
      backgroundColor: colors.bg000,
      borderRadius: sizing.composerRadius,
      boxShadow: isHighlighted
        ? "0 0 0 3px " + colors.accentBrand + ", " + shadows.composer
        : shadows.composer,
      padding: 14,
      display: "flex",
      flexDirection: "column",
      gap: 12,
      transition: "box-shadow 200ms ease",
    }}>
      <div style={{
        minHeight: 48,
        padding: "6px 6px",
        fontFamily: fonts.ui,
        fontSize: 18,
        lineHeight: 1.4,
        color: showText ? colors.text100 : colors.text500,
        position: "relative",
      }}>
        {showText ? (
          <>
            {typedText}
            <span style={{
              display: "inline-block",
              width: 2,
              height: 22,
              backgroundColor: colors.text100,
              verticalAlign: "text-bottom",
              marginLeft: 1,
              opacity: cursorVisible ? 1 : 0,
            }} />
          </>
        ) : (
          placeholder
        )}
      </div>

      <div style={{ display: "flex", alignItems: "center", gap: 8, width: "100%" }}>
        <div style={{
          width: 32, height: 32, display: "flex", alignItems: "center", justifyContent: "center",
          borderRadius: 8, color: colors.text400,
        }}>
          <PlusIcon size={20} />
        </div>
        <div style={{ flex: 1 }} />
        <Pill bg="transparent" color={colors.text400} trailingIcon={ChevronDownIcon}>
          <span style={{ color: colors.text100, fontWeight: 500 }}>{modelLabel}</span>
          <span style={{ color: colors.text500, marginLeft: 6 }}>{modelMode}</span>
        </Pill>
        <div style={{
          width: 32, height: 32, display: "flex", alignItems: "center", justifyContent: "center",
          borderRadius: 8, color: colors.text400,
        }}>
          <VoiceWaveIcon size={20} />
        </div>
      </div>
    </div>
  );
};
