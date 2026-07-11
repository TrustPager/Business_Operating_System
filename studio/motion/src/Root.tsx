import React from "react";
import { Composition } from "remotion";
import { Scaffold } from "./compositions/Scaffold";
import { Showcase } from "./compositions/Showcase";
import {
  Faceless,
  FACELESS_FPS,
  FACELESS_DIMS,
  FACELESS_DURATION_IN_FRAMES,
} from "./compositions/Faceless";
import {
  FacelessBlueprint,
  BLUEPRINT_FPS,
  BLUEPRINT_DIMS,
  BLUEPRINT_DURATION_IN_FRAMES,
} from "./compositions/FacelessBlueprint";
import {
  FacelessPop,
  POP_FPS,
  POP_DIMS,
  POP_DURATION_IN_FRAMES,
} from "./compositions/FacelessPop";
import {
  FacelessFromPlan,
  computeFacelessMeta,
  type ScenesPlan,
} from "./compositions/facelessFactory";
import {
  Overlay,
  computeOverlayMeta,
  type OverlayPlan,
} from "./compositions/Overlay";
import samplePlan from "../data/sample.scenes.json";
import sampleOverlay from "../data/sample.overlay.json";

// Phase 1: a single brand-driven scaffold composition, to prove the engine + brand
// bridge render on the owner's brand.json with zero baked product tokens.
// Faceless / Overlay / ProductDemo compositions arrive in later phases.
export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="Scaffold"
        component={Scaffold}
        durationInFrames={90}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="Showcase"
        component={Showcase}
        durationInFrames={180}
        fps={30}
        width={1920}
        height={1080}
      />
      {/* Phase 2: the scenes.json-driven faceless renderer. Duration + fps +
          dimensions are derived from data/sample.scenes.json. */}
      <Composition
        id="Faceless"
        component={Faceless}
        durationInFrames={FACELESS_DURATION_IN_FRAMES}
        fps={FACELESS_FPS}
        width={FACELESS_DIMS.width}
        height={FACELESS_DIMS.height}
      />
      {/* Same content + engine, alternate scene styles selected by the plan's
          direction.style — directly comparable to Faceless. */}
      <Composition
        id="FacelessBlueprint"
        component={FacelessBlueprint}
        durationInFrames={BLUEPRINT_DURATION_IN_FRAMES}
        fps={BLUEPRINT_FPS}
        width={BLUEPRINT_DIMS.width}
        height={BLUEPRINT_DIMS.height}
      />
      <Composition
        id="FacelessPop"
        component={FacelessPop}
        durationInFrames={POP_DURATION_IN_FRAMES}
        fps={POP_FPS}
        width={POP_DIMS.width}
        height={POP_DIMS.height}
      />
      {/*
        Video — the ONE owner-facing composition. It renders an ARBITRARY
        <slug>.scenes.json chosen at render time: `make-my-video` (via
        scripts/render.js) hands the whole plan in as Remotion input props, and
        `calculateMetadata` derives fps + dimensions + duration from that plan.
        With no props it falls back to defaultProps (the bundled sample) so the
        Remotion Studio always has something to show. This is the composition the
        skill drives; the four above are fixed style samples.
      */}
      <Composition
        id="Video"
        component={FacelessFromPlan}
        defaultProps={samplePlan as unknown as ScenesPlan}
        calculateMetadata={({ props }) => {
          // `props` IS the scenes plan (input props merged over defaultProps).
          const meta = computeFacelessMeta(props);
          return {
            durationInFrames: meta.durationInFrames,
            fps: meta.fps,
            width: meta.dims.width,
            height: meta.dims.height,
          };
        }}
      />
      {/*
        Overlay — the ONE talking-head composition (Mode B). Like Video, it
        renders an ARBITRARY overlay plan handed in as input props:
        `make-my-video` (via scripts/render.js) ingests the owner recording,
        probes its real length, injects `durationInFrames`, and hands the whole
        plan in. `calculateMetadata` derives fps + dimensions + duration from the
        plan; the recording carries its own audio, graphics + captions layer over
        it, and any music bed is ducked underneath. No props => the bundled sample
        (placeholder until a recording is ingested).
      */}
      <Composition
        id="Overlay"
        component={Overlay}
        defaultProps={sampleOverlay as unknown as OverlayPlan}
        calculateMetadata={({ props }) => {
          const meta = computeOverlayMeta(props);
          return {
            durationInFrames: meta.durationInFrames,
            fps: meta.fps,
            width: meta.dims.width,
            height: meta.dims.height,
          };
        }}
      />
    </>
  );
};
