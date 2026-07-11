// facelessFactory — the shared engine behind every scenes.json-driven faceless
// composition. Given a plan (a parsed <slug>.scenes.json), it resolves each
// scene's (style, visual_device) to a primitive via the registry and plays them
// in order through a TransitionSeries. The plan's `direction.style` selects the
// aesthetic; nothing is hardcoded per-video — swap the JSON, get a new video in a
// new style. Faceless / FacelessBlueprint / FacelessPop each bind one plan here.
import React from "react";
import { AbsoluteFill } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { bg, text } from "../tokens";
import { FONT_BODY } from "../fonts";
import { resolveScene, DEFAULT_STYLE } from "../scenes/library/registry";

// ---- Types (loose — the JSON is the linted contract) ----
export interface SceneEntry {
  id: string;
  visual_device: string;
  duration_s: number;
  visual: Record<string, unknown>;
  on_screen_label?: string;
}
export interface ScenesPlan {
  fps?: number;
  aspect?: string;
  direction?: { style?: string };
  transition?: { type?: string; duration_frames?: number };
  scenes: SceneEntry[];
}

export interface FacelessBuild {
  Faceless: React.FC;
  fps: number;
  transitionFrames: number;
  dims: { width: number; height: number };
  durationInFrames: number;
}

const ASPECT_DIMS: Record<string, { width: number; height: number }> = {
  "16:9": { width: 1920, height: 1080 },
  "9:16": { width: 1080, height: 1920 },
  "1:1": { width: 1080, height: 1080 },
};

/** Build a faceless composition + its render metadata from a scenes plan. */
export const buildFaceless = (rawPlan: unknown): FacelessBuild => {
  const plan = rawPlan as ScenesPlan;

  const fps = plan.fps ?? 30;
  const transitionFrames = plan.transition?.duration_frames ?? 12;
  const dims = ASPECT_DIMS[plan.aspect ?? "16:9"] ?? ASPECT_DIMS["16:9"];
  const style = plan.direction?.style ?? DEFAULT_STYLE;

  const sceneFrames = (s: SceneEntry): number =>
    Math.round(s.duration_s * fps);

  // TransitionSeries consumes `transitionFrames` of overlap per transition, so
  // the timeline length is Σ(scene frames) − Σ(transition frames).
  const durationInFrames: number = (() => {
    const total = plan.scenes.reduce((acc, s) => acc + sceneFrames(s), 0);
    const transitions = Math.max(plan.scenes.length - 1, 0);
    return Math.max(total - transitions * transitionFrames, 1);
  })();

  const RenderedScene: React.FC<{ scene: SceneEntry }> = ({ scene }) => {
    const Component = resolveScene(scene.visual_device, style);
    if (!Component) {
      // Unknown device: fail loud in the studio, but never crash a render.
      return (
        <AbsoluteFill
          style={{
            background: bg,
            fontFamily: FONT_BODY,
            alignItems: "center",
            justifyContent: "center",
            color: text,
            fontSize: 28,
          }}
        >
          Unknown visual_device: {scene.visual_device}
        </AbsoluteFill>
      );
    }
    return <Component {...scene.visual} />;
  };

  const Faceless: React.FC = () => {
    // TransitionSeries requires its children to be direct (fragments are not
    // flattened), so build a flat element array.
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
            timing={linearTiming({ durationInFrames: transitionFrames })}
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

  return { Faceless, fps, transitionFrames, dims, durationInFrames };
};
