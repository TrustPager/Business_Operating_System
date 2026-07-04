{/* @dsCard group="sections" */}
// TrustBar — section 2 of the conversion skeleton (web-design-method.md Part 1).
// Job: rating + review count + licences/insured + years + logos, high on the
// page. Earns trust before asking for anything. Carries E-E-A-T signals and
// Review/AggregateRating schema (see components/seo). Placeholder, positive-only
// copy; never fabricate a rating or a count — the skill fills real values or
// leaves the slot and says so to the owner.

type TrustItem = { label: string };

type TrustBarProps = {
  items?: TrustItem[];
};

export default function TrustBar({
  items = [
    { label: 'Fully licensed and insured' },
    { label: '4.9 stars from local jobs' },
    { label: '10+ years in the trade' },
    { label: 'Same-day response' },
  ],
}: TrustBarProps) {
  return (
    <section className="border-y border-border bg-panel">
      <div className="mx-auto flex max-w-content flex-wrap items-center justify-center gap-x-10 gap-y-3 px-6 py-6">
        {items.map((item) => (
          <span key={item.label} className="text-sm font-medium text-text-muted">
            {item.label}
          </span>
        ))}
      </div>
    </section>
  );
}
