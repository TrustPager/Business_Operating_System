// ProductDemo — the "watch it get built" composition (Mode C, design spec §5.3).
//
// FOUNDER/SAAS ADD-ON. This is NOT on the default owner flow. A service-business
// owner has no software to demo; this composition serves a founder or a SaaS
// client whose product has a screen worth showing. The reusable value is the
// interaction + storytelling layer (a fake-assistant chat surface driving a
// cursor/click/build sequence over the OWNER'S OWN screenshots), never any
// product UI of ours.
//
// Props-driven exactly like `Video`/`Overlay`: a ProductDemo plan arrives as
// Remotion input props (scripts/render.js hands it in inline) and
// `computeProductDemoMeta(plan)` owns fps/dimensions/duration so the timeline and
// the render never disagree.
//
// Compositing model (all in Remotion):
//   * A background STAGE (solid brand bg by default; transparent when the plan
//     sets `transparent: true` — the alpha "hand to my editor" export, spec §5.4).
//   * A series of timed BEATS laid end to end. A beat is one of:
//       - "chat"   — the ClaudeShell + ActiveChatScreen surface, with messages
//         REVEALED IN ORDER over the beat (this is where the build story lives).
//       - "screen" — one of the owner's screenshots (staticFile under public/),
//         with an optional cursor/click (ClickTarget) landing on a real element
//         box, and an optional ComposerOverlay typing a prompt over it.
//   * A PersistentProgressPanel overlay spanning the whole clip, ticking tasks.
//
// THE HARD RULE — "never cut from submit straight to done" (spec §5.3, CLAUDE.md
// §5). A `build` chat beat is validated to show the working sequence
// (thinking -> tool rows -> result) before any final assistant answer. A beat
// that skips it renders a loud in-studio warning frame rather than a misleading
// cut — the rule is baked into the engine, not left to the plan author.
import React from "react";
import {
  AbsoluteFill,
  Sequence,
  useCurrentFrame,
  interpolate,
  staticFile,
} from "remotion";
import { ClaudeShell } from "../components/ClaudeShell";
import {
  ActiveChatScreen,
  type ChatMessage,
} from "../components/ActiveChatScreen";
import { ComposerOverlay } from "../compositor/ComposerOverlay";
import { ClickTarget } from "../scenes/shared/ClickIndicator";
import { PersistentProgressPanel } from "../overlays/PersistentProgressPanel";
import type { ProgressTask } from "../components/ProgressPanel";
import { bg, text } from "../tokens";
import { FONT_BODY } from "../fonts";

const ASPECT_DIMS: Record<string, { width: number; height: number }> = {
  "16:9": { width: 1920, height: 1080 },
  "9:16": { width: 1080, height: 1920 },
  "1:1": { width: 1080, height: 1080 },
};

// ---- Plan types (loose — the JSON is the contract, mirrored by the skill) ----

/** A revealed chat message: a ChatMessage plus WHEN it appears within the beat. */
export interface DemoChatMessage extends ChatMessage {
  /** Frames from the beat's start at which this message appears. Defaults to an
   *  even spread across the beat when omitted. */
  appearAtOffset?: number;
}

export interface DemoClick {
  /** Proportional (0-1) element box on the screen to ring + click. */
  x: number;
  y: number;
  w: number;
  h: number;
  /** Frames from the beat's start at which the cursor lands. Default 12. */
  startOffset?: number;
  color?: "primary" | "assistant" | string;
  borderRadius?: number;
}

export interface DemoComposerOverlay {
  prompt: string;
  targetPoint?: { x: number; y: number };
  position?: { x: number; y: number; width?: number };
  timing?: {
    appearAt: number;
    typeStart: number;
    pointAt?: number;
    fadeAt?: number;
  };
}

export interface DemoBeat {
  id: string;
  kind: "chat" | "screen";
  duration_s: number;
  // chat beat:
  messages?: DemoChatMessage[];
  composer?: { placeholder?: string; model?: string; modelMode?: string };
  /** Flags a "watch it get built" beat — enforces thinking -> tool -> result. */
  build?: boolean;
  // shell chrome for a chat beat:
  sidebarProgress?: number;
  connector?: string | null;
  connectorLogo?: string | null;
  user?: { initial: string; name: string; workspace: string };
  navItems?: { icon: string; label: string }[];
  // screen beat:
  screen?: string | null; // staticFile path under public/ (e.g. "screens/x.png")
  clicks?: DemoClick[];
  composerOverlay?: DemoComposerOverlay;
}

export interface ProgressPlan {
  title?: string;
  tasks: ProgressTask[];
  appearFrame?: number;
  checkoffFrames?: number[];
  disappearFrame?: number;
  rightOffset?: number;
}

export interface ProductDemoPlan {
  slug?: string;
  aspect?: string;
  fps?: number;
  /** Alpha export: drop the solid stage so the canvas is transparent (spec §5.4). */
  transparent?: boolean;
  progress?: ProgressPlan | null;
  beats: DemoBeat[];
}

export interface ProductDemoMeta {
  fps: number;
  durationInFrames: number;
  dims: { width: number; height: number };
}

// ---- Metadata owner (the ONE place duration/dims/fps are computed) ----
const beatFrames = (b: DemoBeat, fps: number): number =>
  Math.max(Math.round((b.duration_s ?? 0) * fps), 1);

export const computeProductDemoMeta = (rawPlan: unknown): ProductDemoMeta => {
  const plan = (rawPlan ?? {}) as ProductDemoPlan;
  const fps = plan.fps ?? 30;
  const dims = ASPECT_DIMS[plan.aspect ?? "16:9"] ?? ASPECT_DIMS["16:9"];
  const beats = Array.isArray(plan.beats) ? plan.beats : [];
  const total = beats.reduce((acc, b) => acc + beatFrames(b, fps), 0);
  return { fps, durationInFrames: Math.max(total, 1), dims };
};

// ---- "never cut submit -> done" — the baked build-sequence invariant ----
// A build beat must show a working sequence (a thinking row AND at least one tool
// row) BEFORE the RESULT — the last assistant answer. An early acknowledgement
// ("On it.") before the working rows is fine; what the rule forbids is jumping
// from the request straight to a "done" with no visible work between. Returns
// null when valid, else a human-readable reason to surface in a warning frame.
const buildRuleViolation = (b: DemoBeat): string | null => {
  if (!b.build) return null;
  const msgs = b.messages ?? [];
  // The result is the LAST non-empty assistant text message.
  let lastAnswerIdx = -1;
  msgs.forEach((m, i) => {
    if (m.role === "assistant" && (m.text ?? "").trim().length > 0) lastAnswerIdx = i;
  });
  if (lastAnswerIdx < 0) return null; // no result yet — nothing to cut TO
  const before = msgs.slice(0, lastAnswerIdx);
  const hasThinking = before.some((m) => m.role === "assistant-thinking");
  const hasTool = before.some((m) => m.role === "assistant-tool");
  if (!hasThinking || !hasTool) {
    return 'build beat cuts straight to the answer — show thinking + tool rows before the result ("never cut from submit to done")';
  }
  return null;
};

const WarningFrame: React.FC<{ reason: string }> = ({ reason }) => (
  <AbsoluteFill
    style={{
      background: bg,
      color: text,
      fontFamily: FONT_BODY,
      fontSize: 26,
      alignItems: "center",
      justifyContent: "center",
      textAlign: "center",
      padding: 60,
    }}
  >
    ProductDemo build-rule check: {reason}
  </AbsoluteFill>
);

// ---- Chat beat: reveal messages IN ORDER over the beat ----
const ChatBeat: React.FC<{ beat: DemoBeat }> = ({ beat }) => {
  const frame = useCurrentFrame(); // relative to the beat's Sequence
  const msgs = beat.messages ?? [];

  // Default reveal schedule: spread evenly across the beat if offsets are absent.
  const revealAt = (i: number): number => {
    const m = msgs[i];
    if (typeof m.appearAtOffset === "number") return m.appearAtOffset;
    return Math.round((i / Math.max(msgs.length, 1)) * 18); // gentle cascade
  };

  const visible = msgs
    .map((m, i) => ({ m, at: revealAt(i) }))
    .filter(({ at }) => frame >= at)
    .map(({ m, at }) => {
      // Fade each message in over ~8 frames as it appears.
      const opacity = interpolate(frame, [at, at + 8], [0, 1], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      });
      const translateY = interpolate(frame, [at, at + 8], [8, 0], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      });
      return { ...m, opacity: (m.opacity ?? 1) * opacity, translateY };
    });

  return (
    <ClaudeShell
      sidebarProgress={beat.sidebarProgress ?? 0}
      user={beat.user}
      navItems={beat.navItems ?? []}
      activeConnector={beat.connector ?? undefined}
      connectorLogo={beat.connectorLogo ?? undefined}
    >
      <ActiveChatScreen messages={visible} composer={beat.composer} />
    </ClaudeShell>
  );
};

// ---- Screen beat: owner screenshot + cursor/click + optional composer overlay ----
const ScreenLayer: React.FC<{ beat: DemoBeat }> = ({ beat }) => {
  if (!beat.screen) {
    // No screenshot — used for a pure-overlay / transparent alpha frame.
    return null;
  }
  return (
    <img
      src={staticFile(beat.screen)}
      alt=""
      style={{ width: "100%", height: "100%", objectFit: "cover", display: "block" }}
    />
  );
};

const ClickLayer: React.FC<{ clicks?: DemoClick[] }> = ({ clicks }) => {
  if (!clicks || clicks.length === 0) return null;
  return (
    <>
      {clicks.map((c, i) => (
        // A transparent box positioned on the real element, wrapped in ClickTarget
        // so the ring + cursor land on its true bounding box — never a guessed x/y.
        <div
          key={i}
          style={{
            position: "absolute",
            left: `${c.x * 100}%`,
            top: `${c.y * 100}%`,
            width: `${c.w * 100}%`,
            height: `${c.h * 100}%`,
          }}
        >
          <ClickTarget
            startFrame={c.startOffset ?? 12}
            color={c.color ?? "assistant"}
            borderRadius={c.borderRadius ?? 12}
            fit
          >
            <div style={{ width: "100%", height: "100%" }} />
          </ClickTarget>
        </div>
      ))}
    </>
  );
};

const ScreenBeat: React.FC<{ beat: DemoBeat }> = ({ beat }) => {
  const inner = (
    <AbsoluteFill>
      <ScreenLayer beat={beat} />
      <ClickLayer clicks={beat.clicks} />
    </AbsoluteFill>
  );

  if (beat.composerOverlay) {
    const co = beat.composerOverlay;
    return (
      <ComposerOverlay
        prompt={co.prompt}
        targetPoint={co.targetPoint}
        position={co.position}
        timing={co.timing ?? { appearAt: 6, typeStart: 18, pointAt: 60 }}
      >
        {inner}
      </ComposerOverlay>
    );
  }
  return inner;
};

const Beat: React.FC<{ beat: DemoBeat }> = ({ beat }) => {
  const violation = buildRuleViolation(beat);
  if (violation) return <WarningFrame reason={violation} />;
  return beat.kind === "chat" ? <ChatBeat beat={beat} /> : <ScreenBeat beat={beat} />;
};

/** Props-driven "watch it get built" composition. */
export const ProductDemo: React.FC<ProductDemoPlan> = (plan) => {
  const fps = plan.fps ?? 30;
  const beats = Array.isArray(plan.beats) ? plan.beats : [];
  const transparent = plan.transparent === true;

  // Lay beats end to end as absolute Sequences (cumulative start frames).
  let cursor = 0;
  const beatSequences: React.ReactNode[] = [];
  beats.forEach((b) => {
    const frames = beatFrames(b, fps);
    beatSequences.push(
      <Sequence key={b.id} from={cursor} durationInFrames={frames} name={b.id}>
        <Beat beat={b} />
      </Sequence>
    );
    cursor += frames;
  });

  return (
    <AbsoluteFill style={{ background: transparent ? "transparent" : bg }}>
      {beats.length === 0 ? (
        <AbsoluteFill
          style={{
            fontFamily: FONT_BODY,
            color: text,
            fontSize: 28,
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          No beats yet
        </AbsoluteFill>
      ) : (
        beatSequences
      )}

      {/* Persistent task-progress overlay across the whole clip. */}
      {plan.progress && plan.progress.tasks.length > 0 ? (
        <PersistentProgressPanel
          tasks={plan.progress.tasks}
          appearFrame={plan.progress.appearFrame ?? 0}
          checkoffFrames={plan.progress.checkoffFrames ?? []}
          disappearFrame={plan.progress.disappearFrame}
          rightOffset={plan.progress.rightOffset ?? 48}
        />
      ) : null}
    </AbsoluteFill>
  );
};
