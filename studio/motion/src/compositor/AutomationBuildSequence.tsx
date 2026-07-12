// AutomationBuildSequence — the canonical "the assistant builds an automation" beat.
//
// Composes three primitives in a fixed rhythm:
//
//   +0         AutomationLightningStrike  — accent bolt flash on the empty icon
//                                            ("this is being built")
//   +70        CursorHover                — mouse cursor appears off-screen, arcs in
//   +88        CursorHover                — cursor lands on the bolt
//   +90        AutomationPreviewCard      — preview card slides in above the column
//   +90+hold   AutomationPreviewCard      — preview card fades out
//   +110+hold  CursorHover                — cursor fades out (20 frames after preview)
//
// To synchronise a progress panel: set that automation's task checkoff to
// roughly `startFrame + 120` (i.e., ~30 frames after the preview opens).
//
// All offsets are RELATIVE to the Sequence the component is rendered in,
// matching Remotion's useCurrentFrame contract.
import React from "react";
import {AutomationLightningStrike} from "./AutomationLightningStrike";
import {AutomationPreviewCard} from "./AutomationPreviewCard";
import {CursorHover} from "./CursorHover";

export interface AutomationBuildSequenceProps {
  /** Bolt target position (fractional 0..1). Cursor lands here, lightning strikes here. */
  boltTarget: {x: number; y: number};
  /** Top-left position of the preview card (fractional 0..1). */
  cardPosition: {x: number; y: number};
  /** Preview card content. */
  title: string;
  trigger: string;
  action: string;
  /** Frame at which the bolt flash begins — i.e., "this gets built". */
  startFrame: number;
  /** How long the preview card stays visible after opening. Default 75 frames (~2.5s). */
  previewHoldFrames?: number;
  /** Optional preview card width (px). Default 320. */
  cardWidth?: number;
  /** Cursor SVG size (px). Default 30. */
  cursorSize?: number;
  /** Cursor entry offset from the bolt target (px). Default {-340, 220} (off-screen below-left). */
  cursorFromX?: number;
  cursorFromY?: number;
  /** Skip the per-automation CursorHover (use when a higher-level CursorPath manages the cursor). */
  disableCursor?: boolean;
}

const OFFSETS = {
  cursorEnter: 70,
  cursorLand: 88,
  previewOpen: 90,
  cursorExitMargin: 20,
};

export const AutomationBuildSequence: React.FC<AutomationBuildSequenceProps> = ({
  boltTarget,
  cardPosition,
  title,
  trigger,
  action,
  startFrame,
  previewHoldFrames = 75,
  cardWidth,
  cursorSize = 30,
  cursorFromX,
  cursorFromY,
  disableCursor = false,
}) => {
  const cursorEnter = startFrame + OFFSETS.cursorEnter;
  const cursorLand = startFrame + OFFSETS.cursorLand;
  const previewOpen = startFrame + OFFSETS.previewOpen;
  const previewClose = previewOpen + previewHoldFrames;
  const cursorExit = previewClose + OFFSETS.cursorExitMargin;

  return (
    <>
      <AutomationLightningStrike target={boltTarget} appearFrame={startFrame} />
      {!disableCursor && (
        <CursorHover
        to={boltTarget}
        appearFrame={cursorEnter}
        landsAtFrame={cursorLand}
        fadeOutFrame={previewClose}
        disappearFrame={cursorExit}
        size={cursorSize}
        cursorFromX={cursorFromX}
        cursorFromY={cursorFromY}
      />
      )}
      <AutomationPreviewCard
        title={title}
        trigger={trigger}
        action={action}
        position={cardPosition}
        appearFrame={previewOpen}
        disappearFrame={previewClose}
        width={cardWidth}
      />
    </>
  );
};
