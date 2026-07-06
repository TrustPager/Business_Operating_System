import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import fs from 'fs';

// Plugin: Force .js files from the Remotion repo's src/ to be treated as JSX.
// Vite's import-analysis plugin fails on .js files containing JSX.
function remotionJsxPlugin() {
  const remotionSrc = path.resolve(__dirname, '../src').replace(/\\/g, '/');
  return {
    name: 'remotion-jsx-loader',
    enforce: 'pre',
    async load(id) {
      const normalized = id.replace(/\\/g, '/');
      if (normalized.startsWith(remotionSrc) && normalized.endsWith('.js')) {
        const code = fs.readFileSync(id, 'utf-8');
        return { code, map: null };
      }
    },
    async transform(code, id) {
      const normalized = id.replace(/\\/g, '/');
      if (normalized.startsWith(remotionSrc) && normalized.endsWith('.js')) {
        const esbuild = await import('esbuild');
        const result = await esbuild.transform(code, {
          loader: 'jsx',
          jsx: 'automatic',
          sourcefile: id,
        });
        return { code: result.code, map: result.map || null };
      }
    },
  };
}

// Dev-server port defaults to 3210; override with BOS_THUMBNAIL_PORT (render.js
// and shoot.js read the same var) when 3210 is already in use.
const DEV_PORT = Number(process.env.BOS_THUMBNAIL_PORT) || 3210;

export default defineConfig({
  plugins: [
    remotionJsxPlugin(),
    react(),
  ],
  resolve: {
    alias: [
      { find: 'remotion/no-react', replacement: path.resolve(__dirname, 'src/remotion-shim.jsx') },
      { find: 'remotion', replacement: path.resolve(__dirname, 'src/remotion-shim.jsx') },
      { find: /.*\/fonts\.js$/, replacement: path.resolve(__dirname, 'src/fonts-shim.js') },
      { find: /^@remotion\/google-fonts/, replacement: path.resolve(__dirname, 'src/fonts-shim.js') },
      { find: '@remotion-src', replacement: path.resolve(__dirname, '../src') },
      { find: '@scenes', replacement: path.resolve(__dirname, '../src/scenes') },
      { find: '@compositor', replacement: path.resolve(__dirname, '../src/compositor') },
      { find: '@data', replacement: path.resolve(__dirname, '../src/data') },
    ],
  },
  optimizeDeps: {
    esbuildOptions: {
      loader: { '.js': 'jsx' },
    },
  },
  server: {
    port: 3210,
    open: false,
    host: '0.0.0.0',
    allowedHosts: ['localhost'],
  },
});
