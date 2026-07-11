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
    </>
  );
};
