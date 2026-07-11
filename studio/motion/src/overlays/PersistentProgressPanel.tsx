// PersistentProgressPanel — frame-driven ProgressPanel overlay.
// Renders above other Sequences in a composition; uses useCurrentFrame() to
// track which tasks have been checked off based on a per-task frame schedule.
import React from "react";
import {AbsoluteFill, useCurrentFrame, interpolate} from "remotion";
import {ProgressPanel, ProgressTask} from "../components/ProgressPanel";

const FPS = 30;

export interface PersistentProgressPanelProps {
  tasks: ProgressTask[];
  appearFrame: number;
  /** One frame per task — when that task gets checked off. Length should be ≤ tasks.length. */
  checkoffFrames: number[];
  /** Optional frame at which the panel fades out (e.g., when scene ends). */
  disappearFrame?: number;
  rightOffset?: number;
}

export const PersistentProgressPanel: React.FC<PersistentProgressPanelProps> = ({
  tasks,
  appearFrame,
  checkoffFrames,
  disappearFrame,
  rightOffset = 48,
}) => {
  const frame = useCurrentFrame();

  if (frame < appearFrame) return null;
  if (disappearFrame !== undefined && frame > disappearFrame) return null;

  const fadeIn = interpolate(
    frame,
    [appearFrame, appearFrame + Math.round(FPS * 0.4)],
    [0, 1],
    {extrapolateLeft: "clamp", extrapolateRight: "clamp"},
  );
  const fadeOut = disappearFrame !== undefined
    ? interpolate(
        frame,
        [disappearFrame - Math.round(FPS * 0.4), disappearFrame],
        [1, 0],
        {extrapolateLeft: "clamp", extrapolateRight: "clamp"},
      )
    : 1;
  const opacity = Math.min(fadeIn, fadeOut);

  const completedCount = checkoffFrames.filter((f) => frame >= f).length;
  const activeIndex = completedCount < tasks.length ? completedCount : tasks.length - 1;

  return (
    <AbsoluteFill style={{pointerEvents: "none", zIndex: 100}}>
      <div
        style={{
          position: "absolute",
          right: rightOffset,
          top: "50%",
          transform: "translateY(-50%)",
        }}
      >
        <ProgressPanel
          tasks={tasks}
          completedCount={completedCount}
          activeIndex={activeIndex}
          opacity={opacity}
        />
      </div>
    </AbsoluteFill>
  );
};
