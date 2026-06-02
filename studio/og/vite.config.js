import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// OG Image studio is a pure-Vite + React + Puppeteer pipeline. No Remotion
// dependencies — OG images are static, not video frames. Same clean base as
// the social + CTA studios; only the template (OgImage, 1200×630) + canvas
// size differ. Port 3217 keeps it clear of the other studios (thumbnails
// 3210, social 3216).
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3217,
    open: false,
    host: '0.0.0.0',
  },
});
