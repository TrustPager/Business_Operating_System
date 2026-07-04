{/* @dsCard group="sections" */}
// FinalCta — section 7 of the conversion skeleton (web-design-method.md Part 1).
// Job: one most-wanted action, a short form (1-3 fields), one clear reassurance,
// at a 1:1 attention ratio. Restate the win and make the next step effortless.
// The conversion endpoint: kept fast and semantic. Placeholder, positive-only
// copy; reads design tokens as CSS variables. The form posts nowhere by default
// (no backend shipped); the skill wires it to the owner's capture on build.

type FinalCtaProps = {
  heading?: string;
  reassurance?: string;
  ctaLabel?: string;
};

export default function FinalCta({
  heading = 'Get your free quote today',
  reassurance = 'We usually reply within the hour.',
  ctaLabel = 'Request my quote',
}: FinalCtaProps) {
  return (
    <section id="final-cta" className="bg-primary">
      <div className="mx-auto max-w-xl px-6 py-20 text-center">
        <h2 className="text-3xl font-bold text-panel">{heading}</h2>
        <p className="mt-3 text-panel/80">{reassurance}</p>
        <form className="mx-auto mt-8 flex max-w-md flex-col gap-3" action="#" method="post">
          <label className="sr-only" htmlFor="name">Your name</label>
          <input
            id="name"
            name="name"
            type="text"
            placeholder="Your name"
            className="bg-panel px-4 py-3 text-text"
            style={{ borderRadius: 'var(--radius-md)' }}
            required
          />
          <label className="sr-only" htmlFor="phone">Your phone</label>
          <input
            id="phone"
            name="phone"
            type="tel"
            placeholder="Your phone"
            className="bg-panel px-4 py-3 text-text"
            style={{ borderRadius: 'var(--radius-md)' }}
            required
          />
          <button
            type="submit"
            className="bg-accent px-8 py-4 text-base font-semibold text-panel"
            style={{ borderRadius: 'var(--radius-md)' }}
          >
            {ctaLabel}
          </button>
        </form>
      </div>
    </section>
  );
}
