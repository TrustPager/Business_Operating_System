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
    </>
  );
};
