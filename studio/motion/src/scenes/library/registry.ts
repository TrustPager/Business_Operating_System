// Scene-primitive registry — maps a `visual_device` string (from a
// <slug>.scenes.json entry) to the React component that renders it.
//
// This is the seam that makes the studio data-driven: `design-my-scenes`
// writes a device name + structured `visual` props per beat, and the Faceless
// composition looks the component up here and renders `<Component {...visual} />`.
// Adding a new device = add a primitive + one line here. No composition edits.
import React from "react";
import {
  TypographicStatement,
  BeforeAfter,
  ProcessFlow,
  BigStat,
} from "./editorial";

// Each primitive reads its own structured props off the scene's `visual` object,
// so the registry types them loosely (the JSON is the contract, linted upstream).
export type SceneComponent = React.FC<any>;

export const SCENE_REGISTRY: Record<string, SceneComponent> = {
  // Clean editorial style — the anchor set.
  typographic_statement: TypographicStatement,
  before_after: BeforeAfter,
  process_flow: ProcessFlow,
  big_stat: BigStat,
};

/** Resolve a visual_device to its component, or undefined if unknown. */
export const resolveScene = (device: string): SceneComponent | undefined =>
  SCENE_REGISTRY[device];

/** All registered device names (for lint / tooling). */
export const KNOWN_DEVICES: string[] = Object.keys(SCENE_REGISTRY);
