{/* @dsCard group="sections" */}
// Nav — shared site chrome (web-design-method.md Part 2). 5-7 plainly-labelled
// top items, one persistent primary CTA plus a sticky click-to-call, shallow
// mobile-first structure. Placeholder links; the skill wires the real page set
// (Home, Services hub, Service pages, Areas, About, Reviews, Contact). Reads
// design tokens as CSS variables.

type NavLink = { label: string; href: string };

type NavProps = {
  businessName?: string;
  links?: NavLink[];
  ctaLabel?: string;
  ctaHref?: string;
  phone?: string;
};

export default function Nav({
  businessName = 'Your Business',
  links = [
    { label: 'Services', href: '#' },
    { label: 'About', href: '#' },
    { label: 'Reviews', href: '#' },
    { label: 'Contact', href: '#final-cta' },
  ],
  ctaLabel = 'Get a quote',
  ctaHref = '#final-cta',
  phone = '',
}: NavProps) {
  return (
    <header className="sticky top-0 z-50 border-b border-border bg-panel">
      <nav className="mx-auto flex max-w-content items-center justify-between px-6 py-4">
        <a href="/" className="text-lg font-bold">
          {businessName}
        </a>
        <div className="hidden items-center gap-8 sm:flex">
          {links.map((link) => (
            <a key={link.label} href={link.href} className="text-sm font-medium text-text-muted hover:text-text">
              {link.label}
            </a>
          ))}
        </div>
        <div className="flex items-center gap-3">
          {phone ? (
            <a href={`tel:${phone}`} className="hidden text-sm font-semibold text-primary sm:inline">
              {phone}
            </a>
          ) : null}
          <a
            href={ctaHref}
            className="bg-primary px-5 py-2.5 text-sm font-semibold text-panel"
            style={{ borderRadius: 'var(--radius-md)' }}
          >
            {ctaLabel}
          </a>
        </div>
      </nav>
    </header>
  );
}
