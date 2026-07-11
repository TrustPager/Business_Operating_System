// FacelessPop.tsx — the Bold pop / social faceless composition.
//
// Same engine, same content (the tradie "quote in 60 seconds" plan) as Faceless,
// but the plan's direction.style = bold_pop selects the high-contrast kinetic
// style set, so the two are directly comparable side by side in the studio.
import { buildFaceless } from "./facelessFactory";
import scenesPlan from "../../data/sample-pop.scenes.json";

const built = buildFaceless(scenesPlan);

export const FacelessPop = built.Faceless;
export const POP_FPS = built.fps;
export const POP_DIMS = built.dims;
export const POP_DURATION_IN_FRAMES = built.durationInFrames;
