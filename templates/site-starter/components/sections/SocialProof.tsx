{/* @dsCard group="sections" */}
// SocialProof — section 5 of the conversion skeleton (web-design-method.md
// Part 1). Job: named testimonials, before/after, short case studies, placed
// where doubt peaks. Verbatim customer language adds long-tail coverage; review
// schema reinforces trust (see components/seo/ReviewJsonLd). HARD RULE: never
// fabricate a testimonial, a name, or a number. These are clearly-marked
// placeholders; the skill fills real proof or leaves the slot and tells the owner.

type Testimonial = { quote: string; name: string; detail: string };

type SocialProofProps = {
  heading?: string;
  testimonials?: Testimonial[];
};

export default function SocialProof({
  heading = 'What local customers say',
  testimonials = [
    { quote: 'Placeholder for a real customer quote. Replace with genuine words from a real review.', name: 'Customer name', detail: 'Suburb, job type' },
    { quote: 'Placeholder for a real customer quote. Replace with genuine words from a real review.', name: 'Customer name', detail: 'Suburb, job type' },
  ],
}: SocialProofProps) {
  return (
    <section className="bg-page-bg">
      <div className="mx-auto max-w-content px-6 py-20">
        <h2 className="text-center text-3xl font-bold">{heading}</h2>
        <div className="mt-12 grid gap-8 sm:grid-cols-2">
          {testimonials.map((t, i) => (
            <figure
              key={i}
              className="bg-panel p-8"
              style={{ borderRadius: 'var(--radius-lg)', boxShadow: 'var(--shadow-sm)' }}
            >
              <blockquote className="text-lg">&ldquo;{t.quote}&rdquo;</blockquote>
              <figcaption className="mt-4 text-sm font-medium text-text-muted">
                {t.name} &middot; {t.detail}
              </figcaption>
            </figure>
          ))}
        </div>
      </div>
    </section>
  );
}
