{/* @dsCard group="sections" */}
// Footer — shared site chrome (web-design-method.md Part 2). Full NAP identical
// to the Google Business Profile, hours, service-area list, links to every
// service and location page (the footer as secondary sitemap), map embed. The
// skill fills the real NAP; never invent an address, phone, or hours. Reads
// design tokens as CSS variables.

type FooterProps = {
  businessName?: string;
  address?: string;
  phone?: string;
  hours?: string;
  serviceAreas?: string[];
};

export default function Footer({
  businessName = 'Your Business',
  address = '',
  phone = '',
  hours = '',
  serviceAreas = [],
}: FooterProps) {
  const year = new Date().getFullYear();
  return (
    <footer className="border-t border-border bg-panel">
      <div className="mx-auto grid max-w-content gap-8 px-6 py-14 sm:grid-cols-3">
        <div>
          <p className="text-lg font-bold">{businessName}</p>
          {address ? <p className="mt-2 text-sm text-text-muted">{address}</p> : null}
          {phone ? (
            <a href={`tel:${phone}`} className="mt-2 block text-sm font-semibold text-primary">
              {phone}
            </a>
          ) : null}
          {hours ? <p className="mt-2 text-sm text-text-muted">{hours}</p> : null}
        </div>
        <div>
          <p className="text-sm font-semibold">Areas we serve</p>
          <ul className="mt-2 space-y-1 text-sm text-text-muted">
            {serviceAreas.length
              ? serviceAreas.map((area) => <li key={area}>{area}</li>)
              : <li>Your service areas here</li>}
          </ul>
        </div>
        <div>
          <p className="text-sm font-semibold">Get in touch</p>
          <a
            href="#final-cta"
            className="mt-2 inline-block text-sm font-semibold text-primary"
          >
            Request a quote
          </a>
        </div>
      </div>
      <div className="border-t border-border">
        <p className="mx-auto max-w-content px-6 py-6 text-xs text-text-muted">
          &copy; {year} {businessName}. All rights reserved.
        </p>
      </div>
    </footer>
  );
}
