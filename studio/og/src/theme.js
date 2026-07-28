// OG Studio — local design tokens.
// Self-contained so the studio runs without depending on cross-folder aliases.
// The owner's real brand values live in the root brand/brand.json; keep these
// tokens in step with it when the brand changes.

export const colors = {
  primary: '#29c6c6',          // teal
  primaryDark: '#1a8a8a',
  secondary: '#2db87d',         // green
  accent: '#47a3d9',            // blue
  claudeOrange: '#d97757',      // Claude brand accent

  foreground: '#020817',
  mutedForeground: '#647086',

  background: '#f8fafc',
  card: '#ffffff',
  muted: '#f1f5f9',
  border: '#e2e8f0',

  success: '#1ee46f',
  warning: '#facc15',
  error: '#ef4444',
  white: '#ffffff',
  black: '#0f1117',
};

export const gradients = {
  // Hero — teal to blue, the brand wash
  hero: 'linear-gradient(135deg, #29c6c6 0%, #47a3d9 100%)',
  // Dark — for premium / tech feel
  dark: 'linear-gradient(135deg, #0f1117 0%, #1a2030 100%)',
  // Pastel — soft brand-tinted wash for editorial-style thumbnails
  pastel: 'linear-gradient(135deg, #fef3f2 0%, #f5f0ff 50%, #eaf5ff 100%)',
  // Claude — orange wash for Claude-related content
  claude: 'linear-gradient(135deg, #fff1eb 0%, #ffe0d1 100%)',
  // TP × Claude — split background
  tpClaude: 'linear-gradient(135deg, #e0f7f7 0%, #f5f0ff 50%, #ffe0d1 100%)',
};

export const fonts = {
  primary: '"Plus Jakarta Sans", -apple-system, BlinkMacSystemFont, sans-serif',
  serif: '"Playfair Display", "Times New Roman", Georgia, serif',
  mono: '"JetBrains Mono", "Fira Code", monospace',
};

// YouTube thumbnail dimensions (16:9). Locked at 1280x720.
export const THUMBNAIL_SIZE = { width: 1280, height: 720 };
