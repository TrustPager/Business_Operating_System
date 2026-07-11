// The product-demo chat kit barrel (Mode C add-on).
//
// Brand-neutral: every colour/type flows from ../tokens; no product logo or
// third-party vendor mark ships. The legacy ChatBubble and the pixel-matched
// settings-replica screens are intentionally NOT ported/exported — they are
// product-specific chrome outside this add-on's scope.
export { ClaudeShell } from "./ClaudeShell";
export { Sidebar } from "./Sidebar";
export type { SidebarUser, SidebarNavItem } from "./Sidebar";
export { Composer } from "./Composer";
export { NewChatScreen } from "./NewChatScreen";
export { ActiveChatScreen } from "./ActiveChatScreen";
export type { ChatMessage, ActiveChatScreenProps } from "./ActiveChatScreen";
export { ClaudeMessage } from "./ClaudeMessage";
export type { ClaudeMessageProps } from "./ClaudeMessage";
export { ClaudeThinking } from "./ClaudeThinking";
export type { ClaudeThinkingProps } from "./ClaudeThinking";
export { UserMessageBubble } from "./UserMessageBubble";
export type { UserMessageBubbleProps } from "./UserMessageBubble";
export { ClaudeMcpToolUse } from "./ClaudeMcpToolUse";
export type { ClaudeMcpToolUseProps } from "./ClaudeMcpToolUse";
export { ApprovalPrompt } from "./ApprovalPrompt";
export type { ApprovalPromptProps } from "./ApprovalPrompt";
export { ProgressPanel } from "./ProgressPanel";
export type { ProgressPanelProps, ProgressTask } from "./ProgressPanel";

// Chat-kit atoms + icon set (exported so ProductDemo and any future add-on
// composition can compose them without reaching into individual files).
export {
  Avatar,
  IconButton,
  Pill,
  PromptChip,
  WorkspaceBadge,
} from "./chat-primitives";
export * as ChatIcons from "./chat-icons";
