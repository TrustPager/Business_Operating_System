// ActiveChatScreen — post-prompt-submission state (Mode C add-on).
// Greeting gone; composer moved to sticky bottom; conversation lives in a
// scrollable column above. Messages prop format:
//   [
//     {role: "user", text: "..."},
//     {role: "assistant", text: "...", thoughtLine?: "...", showWordmark?: true},
//   ]
// Roles are brand-neutral: "user" and the "assistant" family
// ("assistant" / "assistant-thinking" / "assistant-tool").
import React from "react";
import { colors, fonts } from "../tokens";
import { Composer } from "./Composer";
import { UserMessageBubble } from "./UserMessageBubble";
import { ClaudeMessage } from "./ClaudeMessage";
import { ClaudeThinking } from "./ClaudeThinking";
import { ApprovalPrompt } from "./ApprovalPrompt";
import { ClaudeMcpToolUse } from "./ClaudeMcpToolUse";

const MAX_WIDTH = 768; // max-w-3xl
const MESSAGE_GAP = 96; // gap when speaker changes
const SAME_ROLE_GAP = 12; // tight gap for consecutive same-role messages

export interface ChatMessage {
  role: "user" | "assistant" | "assistant-thinking" | "assistant-tool";
  text?: string;
  thoughtLine?: string | null;
  showWordmark?: boolean;
  showActions?: boolean;
  opacity?: number;
  translateY?: number;
  thinkingLabel?: string;
  thinkingSize?: number;
  // For role: "assistant-tool" — connected-tool-use shimmer row.
  toolVerb?: string;
  toolLogoSrc?: string;
  toolActive?: boolean;
}

export interface ActiveChatScreenProps {
  messages?: ChatMessage[];
  composerState?: "empty" | "typing" | "submitted";
  typedText?: string;
  cursorVisible?: boolean;
  composer?: {
    placeholder?: string;
    model?: string;
    modelMode?: string;
  };
  highlightedTarget?: string | null;
  pendingApproval?: {
    toolName: string;
    serverName: string;
    logoSrc?: string;
    /** Slot wrapper for the Always allow button — use to ClickTarget-wrap it. */
    alwaysAllowWrapper?: (button: React.ReactNode) => React.ReactNode;
    /** Slot wrapper for the Deny button — same rationale. */
    denyWrapper?: (button: React.ReactNode) => React.ReactNode;
  };
  /**
   * Where to insert the ApprovalPrompt card in the rendered message list.
   * - 'after-user' (default): inserts right after the last user message —
   *   matches the real approval-before-reply pattern.
   * - 'after-last': inserts after the last message of any role. Use this when
   *   the narrative needs the working sequence (thinking -> tool-use) visible
   *   BEFORE the approval card appears.
   */
  approvalAfter?: "after-user" | "after-last";
  highlightAlwaysAllow?: boolean;
  toolCompletion?: { text: string; logoSrc?: string };
}

export const ActiveChatScreen: React.FC<ActiveChatScreenProps> = ({
  messages = [],
  composerState = "empty",
  typedText = "",
  cursorVisible = true,
  composer = { placeholder: "Reply...", model: "Assistant", modelMode: "Adaptive" },
  highlightedTarget = null,
  pendingApproval,
  approvalAfter = "after-user",
  highlightAlwaysAllow = false,
  toolCompletion,
}) => {
  // Choose the splice index for the approval card based on approvalAfter.
  let approvalIdx = -1;
  if (approvalAfter === "after-last") {
    approvalIdx = messages.length - 1;
  } else {
    for (let i = messages.length - 1; i >= 0; i--) {
      if (messages[i].role === "user") {
        approvalIdx = i;
        break;
      }
    }
  }

  const renderMessage = (m: ChatMessage, i: number, prev: ChatMessage | undefined) => {
    const family = (r: ChatMessage["role"]) => (r === "user" ? "user" : "assistant");
    const sameFamilyAsPrev = prev !== undefined && family(prev.role) === family(m.role);
    const marginTop = prev === undefined ? 0 : sameFamilyAsPrev ? SAME_ROLE_GAP : MESSAGE_GAP;

    if (m.role === "user") {
      return (
        <div key={`msg-${i}`} style={{ marginTop }}>
          <UserMessageBubble
            text={m.text ?? ""}
            opacity={m.opacity ?? 1}
            translateY={m.translateY ?? 0}
          />
        </div>
      );
    }
    if (m.role === "assistant") {
      return (
        <div key={`msg-${i}`} style={{ marginTop }}>
          <ClaudeMessage
            text={m.text ?? ""}
            thoughtLine={m.thoughtLine}
            showWordmark={m.showWordmark ?? true}
            showActions={m.showActions ?? true}
            opacity={m.opacity ?? 1}
            translateY={m.translateY ?? 0}
          />
        </div>
      );
    }
    if (m.role === "assistant-thinking") {
      return (
        <div key={`msg-${i}`} style={{ marginTop, paddingLeft: 8 }}>
          <ClaudeThinking
            size={m.thinkingSize ?? 24}
            opacity={m.opacity ?? 1}
            label={m.thinkingLabel ?? "Working..."}
          />
        </div>
      );
    }
    if (m.role === "assistant-tool") {
      // Tighter spacing for tool rows — they cluster as a unit
      const tightMarginTop = prev === undefined ? 0 : (prev.role === "assistant-tool" || prev.role === "assistant-thinking") ? 2 : 12;
      return (
        <div key={`msg-${i}`} style={{ marginTop: tightMarginTop, paddingLeft: 8 }}>
          <ClaudeMcpToolUse
            verb={m.toolVerb ?? ""}
            logoSrc={m.toolLogoSrc ?? ""}
            isActive={m.toolActive ?? true}
            opacity={m.opacity ?? 1}
          />
        </div>
      );
    }
    return null;
  };

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        backgroundColor: colors.bg100,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Messages column */}
      <div
        style={{
          flex: 1,
          width: "100%",
          maxWidth: MAX_WIDTH,
          padding: "40px 24px 0 24px",
          display: "flex",
          flexDirection: "column",
          overflow: "hidden",
        }}
      >
        {messages.map((m, i) => {
          const prev = i > 0 ? messages[i - 1] : undefined;
          const node = renderMessage(m, i, prev);

          // Insert approval card at the chosen splice index
          if (pendingApproval && i === approvalIdx) {
            return (
              <React.Fragment key={`frag-${i}`}>
                {node}
                <div style={{ marginTop: MESSAGE_GAP }}>
                  <ApprovalPrompt
                    toolName={pendingApproval.toolName}
                    serverName={pendingApproval.serverName}
                    logoSrc={pendingApproval.logoSrc}
                    highlightAlwaysAllow={highlightAlwaysAllow}
                    alwaysAllowWrapper={pendingApproval.alwaysAllowWrapper}
                    denyWrapper={pendingApproval.denyWrapper}
                  />
                </div>
              </React.Fragment>
            );
          }
          return node;
        })}

        {/* Tool completion row (system-style: small tool logo + muted text) */}
        {toolCompletion && (
          <div style={{
            marginTop: MESSAGE_GAP,
            display: "flex",
            alignItems: "center",
            gap: 10,
            paddingLeft: 4,
          }}>
            {toolCompletion.logoSrc && (
              <img
                src={toolCompletion.logoSrc}
                width={24}
                height={24}
                alt=""
                style={{ objectFit: "contain", display: "block", borderRadius: 6 }}
              />
            )}
            <span style={{
              fontFamily: fonts.ui,
              fontSize: 13,
              color: colors.text400,
            }}>
              {toolCompletion.text}
            </span>
          </div>
        )}
      </div>

      {/* Sticky composer area */}
      <div
        style={{
          width: "100%",
          maxWidth: MAX_WIDTH,
          padding: "24px 24px 8px 24px",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          background: `linear-gradient(to bottom, ${colors.bg100}00 0%, ${colors.bg100} 24px)`,
        }}
      >
        <Composer
          composerState={composerState}
          typedText={typedText}
          cursorVisible={cursorVisible}
          placeholder={composer.placeholder}
          modelLabel={composer.model}
          modelMode={composer.modelMode}
          highlightedTarget={highlightedTarget}
        />
      </div>
    </div>
  );
};
