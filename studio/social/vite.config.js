import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Social studio is a pure-Vite + React + Puppeteer pipeline. No Remotion
// dependencies — social posts are static images, not video frames. Same
// clean base as the CTA studio; only the templates + canvas sizes differ.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3216,
    open: false,
    host: '0.0.0.0',
  },
});
