// ComposerOverlay — overlays the chat composer card on top of any scene
// (typically one of the owner's own product screenshots) and types a prompt into
// it, then optionally points at the affected element and fades out.
//
// This is the building block for "prompt -> effect" moments in the product-demo
// add-on (Mode C):
//
//   <ComposerOverlay
//     prompt="Move all qualified leads to Won this quarter"
//     targetPoint={{x: 0.62, y: 0.50}}     // proportional 0-1
//     timing={{appearAt: 30, typeStart: 60, pointAt: 200, fadeAt: 240}}
//   >
//     <img src={staticFile('screens/pipeline.png')} />
//   </ComposerOverlay>
//
// The owner's screen renders full-frame underneath. The composer card floats over
// it at a position you choose (defaults to top-centre). After the prompt is typed,
// an optional ConnectorLine points to the element being affected. Colour flows
// from the token bridge (the "assistant" accent), never a baked literal.
import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from "remotion";
import { Composer } from "../components";
import { ConnectorLine, Point } from "./ConnectorLine";
import { accent } from "../tokens";

export interface ComposerOverlayTiming {
  /** Frame at which the composer card fades in. */
  appearAt: number;
  /** Frame at which typing begins. Should be >= appearAt + 6. */
  typeStart: number;
  /** Optional: frame at which the connector line draws to targetPoint. */
  pointAt?: number;
  /** Optional: frame at which the composer card fades out. */
  fadeAt?: number;
  /** Frames over which fade-in happens. Default 12. */
  fadeInFrames?: number;
  /** Frames over which fade-out happens. Default 18. */
  fadeOutFrames?: number;
}

export interface ComposerOverlayPosition {
  /** Center of the card, proportional 0-1. */
  x: number;
  y: number;
  /** Width of the card in pixels (matches the composer's 672px by default). */
  width?: number;
}

export interface ComposerOverlayProps {
  children: React.ReactNode;
  prompt: string;
  /** Where on the frame the prompt's effect lands. Used by ConnectorLine. */
  targetPoint?: Point;
  position?: ComposerOverlayPosition;
  timing: ComposerOverlayTiming;
  charsPerSecond?: number;
  /** Subtle dim on the background while the composer is up. */
  backgroundDim?: number; // 0-1; default 0.0 (none)
  /** Connector colour. Defaults to the brand "assistant" accent. */
  connectorColour?: string;
  /** Optional: keep cursor blinking after typing finishes. Default true. */
  showCursorAfterTyping?: boolean;
}

const FRAME_W = 1920;
const FRAME_H = 1080;

export const ComposerOverlay: React.FC<ComposerOverlayProps> = ({
  children,
  prompt,
  targetPoint,
  position = { x: 0.5, y: 0.32, width: 672 },
  timing,
  charsPerSecond = 26,
  backgroundDim = 0,
  connectorColour = accent,
  showCursorAfterTyping = true,
}) => {
  const frame = useCurrentFrame();
  const fps = 30;

  const fadeInFrames = timing.fadeInFrames ?? 12;
  const fadeOutFrames = timing.fadeOutFrames ?? 18;

  // Composer fade in/out
  const appearOpacity = interpolate(
    frame,
    [timing.appearAt, timing.appearAt + fadeInFrames],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.bezier(0.5, 0, 0.2, 1) }
  );
  const fadeOpacity = timing.fadeAt
    ? interpolate(
        frame,
        [timing.fadeAt, timing.fadeAt + fadeOutFrames],
        [1, 0],
        { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
      )
    : 1;
  const composerOpacity = Math.min(appearOpacity, fadeOpacity);

  // Subtle scale-up on appearance
  const appearScale = interpolate(
    frame,
    [timing.appearAt, timing.appearAt + fadeInFrames],
    [0.96, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.bezier(0.5, 0, 0.2, 1) }
  );

  // Typing logic
  const typeLocal = Math.max(0, frame - timing.typeStart);
  const charsToShow = Math.min(
    prompt.length,
    Math.floor((typeLocal / fps) * charsPerSecond)
  );
  const typedText = prompt.slice(0, charsToShow);
  const typingComplete = charsToShow >= prompt.length;
  const cursorVisible =
    frame < timing.typeStart
      ? false
      : typingComplete
        ? showCursorAfterTyping && Math.floor(frame / 15) % 2 === 0
        : true;
  const composerState = frame >= timing.typeStart ? "typing" : "empty";

  // Background dim
  const dim = composerOpacity * backgroundDim;

  // Composer card geometry
  const cardW = position.width ?? 672;
  const cardLeft = position.x * FRAME_W - cardW / 2;
  const cardTop = position.y * FRAME_H;
  const cardCenterX = position.x;
  const cardBottomY = (cardTop + 132) / FRAME_H; // 132 ~ composer card height
  const composerOrigin: Point = { x: cardCenterX, y: cardBottomY };

  return (
    <AbsoluteFill>
      {/* Owner screen underneath */}
      {children}

      {/* Optional dim layer */}
      {backgroundDim > 0 && (
        <AbsoluteFill style={{ background: "rgba(0,0,0,1)", opacity: dim, pointerEvents: "none" }} />
      )}

      {/* Composer card — only render when visible */}
      {composerOpacity > 0 && (
        <div
          style={{
            position: "absolute",
            left: cardLeft,
            top: cardTop,
            width: cardW,
            opacity: composerOpacity,
            transform: "scale(" + appearScale + ")",
            transformOrigin: "50% 0%",
            pointerEvents: "none",
            zIndex: 70,
          }}
        >
          <Composer
            composerState={composerState}
            typedText={typedText}
            cursorVisible={cursorVisible}
          />
        </div>
      )}

      {/* Connector line: composer -> target element */}
      {targetPoint && timing.pointAt !== undefined && (
        <ConnectorLine
          from={composerOrigin}
          to={targetPoint}
          appearAt={timing.pointAt}
          drawDurationFrames={22}
          curve={-60}
          color={connectorColour}
          arrowHead
          glow
        />
      )}
    </AbsoluteFill>
  );
};
