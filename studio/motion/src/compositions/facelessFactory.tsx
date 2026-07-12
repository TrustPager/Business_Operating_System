// facelessFactory — the shared engine behind every scenes.json-driven faceless
// composition. Given a plan (a parsed <slug>.scenes.json), it resolves each
// scene's (style, visual_device) to a primitive via the registry and plays them
// in order through a TransitionSeries. The plan's `direction.style` selects the
// aesthetic; nothing is hardcoded per-video — swap the JSON, get a new video in a
// new style. Faceless / FacelessBlueprint / FacelessPop each bind one plan here.
import React from "react";
import { AbsoluteFill, Audio, staticFile } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { bg, text } from "../tokens";
import { FONT_BODY } from "../fonts";
import { resolveScene, DEFAULT_STYLE } from "../scenes/library/registry";

// ---- Types (loose — the JSON is the linted contract) ----
export interface SceneEntry {
  id: string;
  beat_ref?: string;
  visual_device: string;
  duration_s: number;
  visual: Record<string, unknown>;
  on_screen_label?: string;
}

// The per-beat voice manifest (data/<slug>.voice.json), inlined into the plan by
// scripts/render.js when the plan opts into voice. Each entry names a beat's MP3
// (under public/<dir>/) so the engine can layer it on that beat's scene. Silent by
// default — a plan with no `voice` renders exactly as before (spec §6, keyless floor).
export interface VoiceBeat {
  beat_ref: string;
  file: string;
  start_s?: number;
  duration_s?: number;
}
export interface VoiceManifest {
  dir: string; // path under public/ (e.g. "audio/<slug>")
  beats: VoiceBeat[];
}

export interface ScenesPlan {
  fps?: number;
  aspect?: string;
  direction?: { style?: string };
  transition?: { type?: string; duration_frames?: number };
  voice?: VoiceManifest | string | null;
  scenes: SceneEntry[];
}

// Build a beat_ref -> audio staticFile src lookup from the (inlined) voice manifest.
// A bare string `voice` is a dir hint that was never resolved to a manifest (render.js
// inlines it); treat that as silent rather than guessing filenames.
const buildVoiceLookup = (
  voice: ScenesPlan["voice"]
): Record<string, string> => {
  const lookup: Record<string, string> = {};
  if (!voice || typeof voice === "string") return lookup;
  const dir = (voice.dir || "").replace(/\/+$/, "");
  const beats = Array.isArray(voice.beats) ? voice.beats : [];
  for (const b of beats) {
    if (b && b.beat_ref && b.file) {
      lookup[b.beat_ref] = dir ? `${dir}/${b.file}` : b.file;
    }
  }
  return lookup;
};

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

// A scene must be strictly longer than the transition that overlaps it, or
// TransitionSeries throws. Clamp so a too-short duration can never crash a render,
// and use this everywhere scene frames are computed (metadata, render, timing) so
// the three never drift.
const sceneFrames = (
  durationS: number,
  fps: number,
  transitionFrames: number
): number => Math.max(Math.round((durationS ?? 0) * fps), transitionFrames + 1);

export interface FacelessMeta {
  fps: number;
  transitionFrames: number;
  dims: { width: number; height: number };
  durationInFrames: number;
  style: string;
}

/**
 * Pure metadata from a scenes plan — no React, no rendering. This is the ONE
 * place the timeline maths live, so `calculateMetadata` (for the props-driven
 * composition) and `buildFaceless` (for the static sample comps) can never
 * drift on how a plan maps to fps / dimensions / duration.
 */
export const computeFacelessMeta = (rawPlan: unknown): FacelessMeta => {
  const plan = (rawPlan ?? {}) as ScenesPlan;
  const fps = plan.fps ?? 30;
  const transitionFrames = plan.transition?.duration_frames ?? 12;
  const dims = ASPECT_DIMS[plan.aspect ?? "16:9"] ?? ASPECT_DIMS["16:9"];
  const style = plan.direction?.style ?? DEFAULT_STYLE;
  const scenes = Array.isArray(plan.scenes) ? plan.scenes : [];

  // TransitionSeries consumes `transitionFrames` of overlap per transition, so
  // the timeline length is Σ(scene frames) − Σ(transition frames).
  const total = scenes.reduce(
    (acc, s) => acc + sceneFrames(s.duration_s ?? 0, fps, transitionFrames),
    0
  );
  const transitions = Math.max(scenes.length - 1, 0);
  const durationInFrames = Math.max(total - transitions * transitionFrames, 1);

  return { fps, transitionFrames, dims, durationInFrames, style };
};

/** Build a faceless composition + its render metadata from a scenes plan. */
export const buildFaceless = (rawPlan: unknown): FacelessBuild => {
  const plan = rawPlan as ScenesPlan;

  const meta = computeFacelessMeta(plan);
  const { fps, transitionFrames, dims, durationInFrames, style } = meta;

  const frames = (s: SceneEntry): number =>
    sceneFrames(s.duration_s, fps, transitionFrames);

  // Silent by default. When the plan carries a resolved voice manifest, each beat's
  // MP3 is layered INSIDE that beat's scene Sequence, so it starts at the scene's
  // own start on the existing beat/scene timeline (no new timing maths — the
  // Sequence context is the beat's start). Audio longer than its scene is clipped by
  // the Sequence, so a too-long VO never bleeds into the next scene (voice.js warns
  // when that happens so the scene can be lengthened). Visual duration is unchanged.
  const voiceLookup = buildVoiceLookup(plan.voice);

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
    // Fail soft on an empty plan rather than mounting an empty TransitionSeries.
    if (!plan.scenes || plan.scenes.length === 0) {
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
          No scenes yet
        </AbsoluteFill>
      );
    }
    // TransitionSeries requires its children to be direct (fragments are not
    // flattened), so build a flat element array.
    const children: React.ReactNode[] = [];
    plan.scenes.forEach((scene, i) => {
      const voiceSrc = voiceLookup[scene.beat_ref ?? ""] ?? voiceLookup[scene.id];
      children.push(
        <TransitionSeries.Sequence
          key={scene.id}
          durationInFrames={frames(scene)}
        >
          <RenderedScene scene={scene} />
          {voiceSrc ? <Audio src={staticFile(voiceSrc)} /> : null}
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

/**
 * Plan-driven faceless component. Where `buildFaceless` closes over a plan known
 * at module scope (the static sample comps), this one takes the plan as its
 * React props — so a single registered composition can render ANY plan handed to
 * it at render time via Remotion input props (`--props`). The composition's
 * `calculateMetadata` uses `computeFacelessMeta` to set fps / dimensions /
 * duration from the same plan, so the timeline and the render always agree.
 */
export const FacelessFromPlan: React.FC<ScenesPlan> = (plan) => {
  const built = React.useMemo(() => buildFaceless(plan), [plan]);
  const Comp = built.Faceless;
  return <Comp />;
};
