import React from "react";
import {
  AbsoluteFill,
  Sequence,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from "remotion";
import {
  bg,
  panel,
  border,
  primary,
  primaryTint,
  text,
  textMuted,
  accent,
  shadows,
  gradients,
} from "../tokens";
import { FONT_BODY } from "../fonts";
import { ConnectorLine, CursorClick, CrossHighlight } from "../compositor";
import { Annotations } from "../overlays/Annotations";
import { PersistentProgressPanel } from "../overlays/PersistentProgressPanel";
import { ProgressTask } from "../components/ProgressPanel";

// Showcase — a calm, editorial demonstration that exercises several ported
// primitives end-to-end so a viewer sees what the studio can do, all on the
// owner's brand.json. Every colour + type traces to the token bridge; no hex
// literals, no product names. 1920x1080, 30fps, 180 frames.

// --- Two labelled nodes the connector links (proportional centres) ---
const LEFT_NODE = { x: 0.3, y: 0.54 };
const RIGHT_NODE = { x: 0.585, y: 0.54 };

// A single labelled node card. Springs in on its own Sequence-local frame.
const NodeCard: React.FC<{
  center: { x: number; y: number };
  eyebrow: string;
  label: string;
  glyph: string;
}> = ({ center, eyebrow, label, glyph }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const enter = spring({ frame, fps, config: { damping: 200, mass: 0.9 } });
  const opacity = interpolate(enter, [0, 1], [0, 1]);
  const lift = interpolate(enter, [0, 1], [28, 0]);
  const scale = interpolate(enter, [0, 1], [0.94, 1]);

  const cardW = 260;
  const cardH = 132;

  return (
    <div
      style={{
        position: "absolute",
        left: center.x * width - cardW / 2,
        top: center.y * height - cardH / 2,
        width: cardW,
        height: cardH,
        opacity,
        transform: `translateY(${lift}px) scale(${scale})`,
        background: panel,
        border: `1px solid ${border}`,
        borderRadius: 20,
        boxShadow: shadows.card,
        padding: "22px 24px",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        gap: 12,
        fontFamily: FONT_BODY,
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
        <div
          style={{
            width: 44,
            height: 44,
            borderRadius: 12,
            background: primaryTint,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: 22,
            color: primary,
            fontWeight: 700,
          }}
        >
          {glyph}
        </div>
        <div>
          <div
            style={{
              fontSize: 12,
              fontWeight: 600,
              letterSpacing: "0.12em",
              textTransform: "uppercase",
              color: textMuted,
            }}
          >
            {eyebrow}
          </div>
          <div
            style={{
              fontSize: 26,
              fontWeight: 700,
              color: text,
              letterSpacing: "-0.01em",
              marginTop: 3,
            }}
          >
            {label}
          </div>
        </div>
      </div>
    </div>
  );
};

export const Showcase: React.FC = () => {
  const tasks: ProgressTask[] = [
    { id: "draft", label: "Draft the outline" },
    { id: "design", label: "Design the frames" },
    { id: "render", label: "Render to video" },
  ];

  const headlineAnnotations = [
    {
      type: "headline",
      target: { x: 0.42, y: 0.16 },
      text: "One idea, all the way to published",
      style: "emphasis",
      timing: { start_offset_seconds: 0.2, duration_seconds: 5.6 },
    },
    {
      type: "caption",
      target: { x: 0.42, y: 0.27 },
      text: "The studio carries it the whole way",
      timing: { start_offset_seconds: 0.9, duration_seconds: 4.9 },
    },
  ];

  return (
    <AbsoluteFill style={{ background: bg, fontFamily: FONT_BODY }}>
      {/* Soft brand-tinted top band for editorial warmth (from token gradient) */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          height: 6,
          background: gradients.hero,
        }}
      />

      {/* Two labelled nodes — spring in one after the other */}
      <Sequence from={6} name="left-node">
        <NodeCard
          center={LEFT_NODE}
          eyebrow="Start"
          label="Idea"
          glyph="✱"
        />
      </Sequence>
      <Sequence from={30} name="right-node">
        <NodeCard
          center={RIGHT_NODE}
          eyebrow="Finish"
          label="Published"
          glyph="◆"
        />
      </Sequence>

      {/* Connector links the two nodes (cause -> effect) */}
      <ConnectorLine
        from={{ x: LEFT_NODE.x + 0.07, y: LEFT_NODE.y }}
        to={{ x: RIGHT_NODE.x - 0.07, y: RIGHT_NODE.y }}
        appearAt={50}
        drawDurationFrames={22}
        curve={70}
      />

      {/* Cursor flies in and clicks the finished node */}
      <CursorClick
        to={RIGHT_NODE}
        targetW={0.135}
        targetH={0.122}
        appearAt={82}
        duration={52}
      />

      {/* Both nodes pulse together to close the loop */}
      <CrossHighlight
        regions={[
          { x: LEFT_NODE.x, y: LEFT_NODE.y, w: 0.15, h: 0.14 },
          { x: RIGHT_NODE.x, y: RIGHT_NODE.y, w: 0.15, h: 0.14 },
        ]}
        appearAt={140}
        durationFrames={40}
      />

      {/* Headline + caption overlay (absolute composition frames) */}
      <Annotations annotations={headlineAnnotations} />

      {/* Progress panel ticking three tasks down the right edge */}
      <PersistentProgressPanel
        tasks={tasks}
        appearFrame={18}
        checkoffFrames={[70, 108, 150]}
      />
    </AbsoluteFill>
  );
};
