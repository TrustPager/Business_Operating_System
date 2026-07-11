// Scene-primitive registry — maps a `direction.style` + a `visual_device` string
// (both from a <slug>.scenes.json plan) to the React component that renders it.
//
// This is the seam that makes the studio data-driven: `design-my-scenes` writes a
// style + device name + structured `visual` props per beat, and the Faceless
// composition looks the component up here and renders `<Component {...visual} />`.
// Adding a new device = add a primitive to each style set + one key. Adding a new
// STYLE = add a primitive set + one entry in STYLE_REGISTRY. No composition edits.
import React from "react";
import * as Editorial from "./editorial";
import * as Blueprint from "./blueprint";
import * as Pop from "./pop";

// Each primitive reads its own structured props off the scene's `visual` object,
// so the registry types them loosely (the JSON is the contract, linted upstream).
export type SceneComponent = React.FC<any>;

// A style set implements the SAME four visual devices, each in its own aesthetic.
type DeviceSet = Record<string, SceneComponent>;

const asSet = (m: {
  TypographicStatement: SceneComponent;
  BeforeAfter: SceneComponent;
  ProcessFlow: SceneComponent;
  BigStat: SceneComponent;
}): DeviceSet => ({
  typographic_statement: m.TypographicStatement,
  before_after: m.BeforeAfter,
  process_flow: m.ProcessFlow,
  big_stat: m.BigStat,
});

// style name (matches scenes.json `direction.style`) → device → component.
export const STYLE_REGISTRY: Record<string, DeviceSet> = {
  clean_editorial: asSet(Editorial),
  blueprint: asSet(Blueprint),
  bold_pop: asSet(Pop),
};

export const DEFAULT_STYLE = "clean_editorial";

// Flat editorial map kept for back-compat with anything importing the anchor set.
export const SCENE_REGISTRY: DeviceSet = STYLE_REGISTRY[DEFAULT_STYLE];

/**
 * Resolve a (style, device) pair to its component. Falls back to the editorial
 * implementation of the device if the style is unknown, and returns undefined
 * only if the device itself is unknown (so the renderer can fail loud).
 */
export const resolveScene = (
  device: string,
  style: string = DEFAULT_STYLE
): SceneComponent | undefined => {
  const set = STYLE_REGISTRY[style] ?? STYLE_REGISTRY[DEFAULT_STYLE];
  return set[device] ?? STYLE_REGISTRY[DEFAULT_STYLE][device];
};

/** All registered device names (for lint / tooling). */
export const KNOWN_DEVICES: string[] = Object.keys(SCENE_REGISTRY);

/** All registered style names (for lint / tooling). */
export const KNOWN_STYLES: string[] = Object.keys(STYLE_REGISTRY);
