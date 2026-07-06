import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Video studio is the fifth studio in the family and copies the proven
// Vite + React + Puppeteer stack exactly (Decision 4 of the YouTube Studio
// design doc). It renders MOTION by frame-capture, not realtime: the template
// reads its frame from a ?frame=N URL query param, and scripts/render.js steps
// N over 0..duration*fps deterministically. No Remotion dependency lives here
// (the workspace hard-rule reserves the Remotion render engine for the separate
// Remotion-VideoStudio repo); this studio reuses the still studios' pattern.
// The dev-server port defaults to 3218 but can be overridden with the
// BOS_VIDEO_PORT env var. render.js and shoot.js read the SAME variable, so
// setting it once (e.g. BOS_VIDEO_PORT=3219) moves the dev server AND the place
// the render scripts look, keeping them in lockstep. Handy when 3218 is already
// in use by a concurrent session or a leftover dev server.
const DEV_PORT = Number(process.env.BOS_VIDEO_PORT) || 3218;

export default defineConfig({
  plugins: [react()],
  server: {
    // thumbnails 3210, cta 3213, social 3216, og 3217 are taken; site-starter
    // uses 3220. The plan assigns the video studio port 3218 (override: BOS_VIDEO_PORT).
    port: DEV_PORT,
    open: false,
    host: '0.0.0.0',
  },
});
