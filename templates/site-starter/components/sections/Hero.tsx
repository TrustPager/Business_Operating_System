{/* @dsCard group="sections" */}
// Hero — section 1 of the conversion skeleton (web-design-method.md Part 1).
// Job: headline + subhead + one real hero visual + one primary CTA, inside the
// ~10s window. Holds the single H1 as the primary keyword in benefit form.
// Copy is placeholder and positive-only; the skill replaces it with the real,
// on-page-SEO-correct copy it derives. Reads design tokens as CSS variables.

type HeroProps = {
  headline?: string;
  subhead?: string;
  ctaLabel?: string;
  ctaHref?: string;
};

export default function Hero({
  headline = 'The outcome your customers want, delivered',
  subhead = 'Say what you do, who it is for, and the next step, right here above the fold.',
  ctaLabel = 'Get your free quote',
  ctaHref = '#final-cta',
}: HeroProps) {
  return (
    <section className="bg-page-bg">
      <div className="mx-auto max-w-content px-6 py-24 text-center">
        {/* The single H1 — the primary keyword written as the human benefit. */}
        <h1 className="mx-auto max-w-3xl text-4xl font-bold sm:text-5xl">
          {headline}
        </h1>
        <p className="mx-auto mt-6 max-w-2xl text-lg text-text-muted">
          {subhead}
        </p>
        <div className="mt-10">
          <a
            href={ctaHref}
            className="inline-block bg-primary px-8 py-4 text-base font-semibold text-panel"
            style={{ borderRadius: 'var(--radius-md)' }}
          >
            {ctaLabel}
          </a>
        </div>
      </div>
    </section>
  );
}
