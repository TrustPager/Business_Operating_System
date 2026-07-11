// Faceless.tsx — the Clean-editorial faceless composition (Mode A, anchor style).
//
// Binds data/sample.scenes.json (direction.style = clean_editorial) to the shared
// faceless engine. Duration + fps + dimensions are derived from the plan. The
// Blueprint and Pop styles are separate compositions binding their own plans; all
// three share buildFaceless so the engine is written once.
import { buildFaceless } from "./facelessFactory";
import scenesPlan from "../../data/sample.scenes.json";

const built = buildFaceless(scenesPlan);

export const Faceless = built.Faceless;
export const FACELESS_FPS = built.fps;
export const FACELESS_TRANSITION_FRAMES = built.transitionFrames;
export const FACELESS_DIMS = built.dims;
export const FACELESS_DURATION_IN_FRAMES = built.durationInFrames;
