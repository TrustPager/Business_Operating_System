// Faceless.tsx — the scenes.json-driven faceless renderer (Mode A).
//
// Reads a <slug>.scenes.json plan, resolves each scene's `visual_device` to a
// primitive via the registry, and plays them in order through a TransitionSeries
// with a tasteful fade between scenes. Every entrance is spring-driven off the
// scene-local frame; nothing is hardcoded per-video — swap the JSON, get a new
// video. Duration is computed from the scenes' own durations, not fixed here.
import React from "react";
import { AbsoluteFill } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { bg } from "../tokens";
import { FONT_BODY } from "../fonts";
import { resolveScene } from "../scenes/library/registry";
import scenesPlan from "../../data/sample.scenes.json";

// ---- Types (loose — the JSON is the linted contract) ----
interface SceneEntry {
  id: string;
  visual_device: string;
  duration_s: number;
  visual: Record<string, unknown>;
  on_screen_label?: string;
}
interface ScenesPlan {
  fps?: number;
  aspect?: string;
  transition?: { type?: string; duration_frames?: number };
  scenes: SceneEntry[];
}

const plan = scenesPlan as unknown as ScenesPlan;

// ---- Exported render metadata (Root.tsx uses these to size the Composition) ----
export const FACELESS_FPS = plan.fps ?? 30;
export const FACELESS_TRANSITION_FRAMES = plan.transition?.duration_frames ?? 12;

const ASPECT_DIMS: Record<string, { width: number; height: number }> = {
  "16:9": { width: 1920, height: 1080 },
  "9:16": { width: 1080, height: 1920 },
  "1:1": { width: 1080, height: 1080 },
};
export const FACELESS_DIMS =
  ASPECT_DIMS[plan.aspect ?? "16:9"] ?? ASPECT_DIMS["16:9"];

const sceneFrames = (s: SceneEntry): number =>
  Math.round(s.duration_s * FACELESS_FPS);

// TransitionSeries consumes `transitionFrames` of overlap per transition, so the
// timeline length is Σ(scene frames) − Σ(transition frames).
export const FACELESS_DURATION_IN_FRAMES: number = (() => {
  const total = plan.scenes.reduce((acc, s) => acc + sceneFrames(s), 0);
  const transitions = Math.max(plan.scenes.length - 1, 0);
  return Math.max(total - transitions * FACELESS_TRANSITION_FRAMES, 1);
})();

// ---- A single scene, resolved through the registry ----
const RenderedScene: React.FC<{ scene: SceneEntry }> = ({ scene }) => {
  const Component = resolveScene(scene.visual_device);
  if (!Component) {
    // Unknown device: fail loud in the studio, but never crash a render.
    return (
      <AbsoluteFill
        style={{
          background: bg,
          fontFamily: FONT_BODY,
          alignItems: "center",
          justifyContent: "center",
          color: "#020817",
          fontSize: 28,
        }}
      >
        Unknown visual_device: {scene.visual_device}
      </AbsoluteFill>
    );
  }
  return <Component {...scene.visual} />;
};

export const Faceless: React.FC = () => {
  // TransitionSeries requires its Sequence/Transition children to be direct
  // (fragments are not flattened), so build a flat element array.
  const children: React.ReactNode[] = [];
  plan.scenes.forEach((scene, i) => {
    children.push(
      <TransitionSeries.Sequence
        key={scene.id}
        durationInFrames={sceneFrames(scene)}
      >
        <RenderedScene scene={scene} />
      </TransitionSeries.Sequence>
    );
    if (i < plan.scenes.length - 1) {
      children.push(
        <TransitionSeries.Transition
          key={`t-${scene.id}`}
          presentation={fade()}
          timing={linearTiming({ durationInFrames: FACELESS_TRANSITION_FRAMES })}
        />
      );
    }
  });

  return (
    <AbsoluteFill style={{ background: bg }}>
      <TransitionSeries>{children}</TransitionSeries>
    </AbsoluteFill>
  );
};
