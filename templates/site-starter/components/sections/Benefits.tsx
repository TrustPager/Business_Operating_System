{/* @dsCard group="sections" */}
// Benefits — section 3 of the conversion skeleton (web-design-method.md Part 1).
// Job: benefit-led, feature-supported, 3-4 scannable items for F-pattern reading.
// Home for H2s carrying secondary and long-tail service keywords. Each item
// leads with what the customer gets, then the feature that delivers it.
// Placeholder, positive-only copy; reads design tokens as CSS variables.

type Benefit = { title: string; body: string };

type BenefitsProps = {
  heading?: string;
  benefits?: Benefit[];
};

export default function Benefits({
  heading = 'What you get',
  benefits = [
    { title: 'Back up and running the same day', body: 'We carry the common parts on the van, so most jobs are sorted in one visit.' },
    { title: 'A price you know up front', body: 'A clear quote before we start, so the number never moves on you.' },
    { title: 'Work that lasts', body: 'Done to standard and guaranteed, so you call once and it stays fixed.' },
  ],
}: BenefitsProps) {
  return (
    <section className="bg-page-bg">
      <div className="mx-auto max-w-content px-6 py-20">
        <h2 className="text-center text-3xl font-bold">{heading}</h2>
        <div className="mt-12 grid gap-8 sm:grid-cols-3">
          {benefits.map((b) => (
            <div
              key={b.title}
              className="bg-panel p-6"
              style={{ borderRadius: 'var(--radius-lg)', boxShadow: 'var(--shadow-sm)' }}
            >
              <h3 className="text-lg font-semibold">{b.title}</h3>
              <p className="mt-2 text-text-muted">{b.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
