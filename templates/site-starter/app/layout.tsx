// Root layout — the app shell for every page.
//
// Carries four things the method (web-design-method.md) requires at the shell:
//   1. Metadata API defaults (title + meta, per-page overridable) — Part 3.
//   2. The font <link> wiring, done so the font ACTUALLY loads (Part 4, lever 3:
//      a named-but-unloaded font silently falls back to system-sans and the
//      design reverts to generic). The neutral starter loads Inter via a real
//      preconnect + stylesheet link; the skill swaps in the owner's typeface and
//      confirms the same wiring loads it.
//   3. The design-system token layer (styles/tokens.css) imported before the
//      Tailwind entry, so every component reads the owner's tokens as CSS vars.
//   4. The shared Nav + Footer, so the multi-page site case shares one chrome.
//
// tokens.css is imported first so its :root variables are defined before the
// Tailwind utilities that read them.
import '../styles/tokens.css';
import '../styles/globals.css';
import type { Metadata } from 'next';
import Nav from '../components/sections/Nav';
import Footer from '../components/sections/Footer';

// Metadata API defaults. Per-page files override title/description for
// SERP message-match; the skill writes the real, keyword-in-benefit values.
export const metadata: Metadata = {
  title: 'Your Business',
  description:
    'A bespoke, high-converting page built from the sites you admire and your own taste.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        {/* Font wiring — confirm-loading pattern (Part 4, lever 3). Preconnect
            then load the stylesheet so the named font renders, never silently
            falling back to system-sans. Swap Inter for the owner's typeface and
            keep this same preconnect + <link> shape so it still loads. */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="anonymous"
        />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
        />
      </head>
      <body>
        <Nav />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
