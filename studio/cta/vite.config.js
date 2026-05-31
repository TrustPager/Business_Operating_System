import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// CTA studio is a pure-Vite + React + Puppeteer pipeline. No Remotion
// dependencies — CTAs are static email images, not video frames. That's
// the deliberate divergence from the thumbnail studio (which inherits
// Remotion composition mirrors).
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3213,
    open: false,
    host: '0.0.0.0',
  },
});
