/** @type {import('tailwindcss').Config} */
// Tailwind is the utility layer; the design system lives in styles/tokens.css
// as CSS variables (the layer Claude Design attaches to via /design-sync).
// Tailwind's theme maps its scales onto those variables, so a token change in
// tokens.css reskins every utility at once, and inline_design_system.py only
// ever has to rewrite tokens.css per project.
module.exports = {
  content: [
    './app/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: 'var(--color-primary)',
        'primary-deep': 'var(--color-primary-deep)',
        accent: 'var(--color-accent)',
        text: 'var(--color-text)',
        'text-muted': 'var(--color-text-muted)',
        panel: 'var(--color-panel)',
        border: 'var(--color-border)',
        'page-bg': 'var(--color-page-bg)',
      },
      fontFamily: {
        sans: 'var(--font-sans)',
        serif: 'var(--font-serif)',
      },
      borderRadius: {
        sm: 'var(--radius-sm)',
        DEFAULT: 'var(--radius-md)',
        md: 'var(--radius-md)',
        lg: 'var(--radius-lg)',
        full: 'var(--radius-full)',
      },
      maxWidth: {
        content: 'var(--layout-max-width)',
      },
    },
  },
  plugins: [],
};
