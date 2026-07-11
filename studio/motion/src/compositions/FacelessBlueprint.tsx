// FacelessBlueprint.tsx — the Blueprint / how-it-works faceless composition.
//
// Same engine, same content (the tradie "quote in 60 seconds" plan) as Faceless,
// but the plan's direction.style = blueprint selects the schematic style set, so
// the two are directly comparable side by side in the studio.
import { buildFaceless } from "./facelessFactory";
import scenesPlan from "../../data/sample-blueprint.scenes.json";

const built = buildFaceless(scenesPlan);

export const FacelessBlueprint = built.Faceless;
export const BLUEPRINT_FPS = built.fps;
export const BLUEPRINT_DIMS = built.dims;
export const BLUEPRINT_DURATION_IN_FRAMES = built.durationInFrames;
