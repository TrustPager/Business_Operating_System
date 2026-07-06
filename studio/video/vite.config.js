import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Video studio is the fifth studio in the family and copies the proven
// Vite + React + Puppeteer stack exactly (Decision 4 of the YouTube Studio
// design doc). It renders MOTION by frame-capture, not realtime: the template
// reads its frame from a ?frame=N URL query param, and scripts/render.js steps
// N over 0..duration*fps deterministically. No Remotion dependency lives here
// (the workspace hard-rule reserves the Remotion render engine for the separate
// Remotion-VideoStudio repo); this studio reuses the still studios' pattern.
export default defineConfig({
  plugins: [react()],
  server: {
    // thumbnails 3210, cta 3213, social 3216, og 3217 are taken; site-starter
    // uses 3220. The plan assigns the video studio port 3218.
    port: 3218,
    open: false,
    host: '0.0.0.0',
  },
});
