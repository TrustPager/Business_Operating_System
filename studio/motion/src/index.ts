import { registerRoot } from "remotion";
import { RemotionRoot } from "./Root";

// MUST be called or the studio shows a black "waiting for registerRoot" screen.
registerRoot(RemotionRoot);
