import React from "react";
import { Composition } from "remotion";
import { Scaffold } from "./compositions/Scaffold";

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
    </>
  );
};
