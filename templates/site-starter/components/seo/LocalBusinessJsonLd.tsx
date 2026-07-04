// LocalBusinessJsonLd — schema.org LocalBusiness structured data
// (web-design-method.md Part 3). Emits a JSON-LD <script> so search engines
// read the business's NAP, hours, and rating. The skill passes real values;
// never emit invented data. Empty/omitted fields are simply left out.

type LocalBusinessJsonLdProps = {
  name?: string;
  url?: string;
  telephone?: string;
  streetAddress?: string;
  addressLocality?: string;
  addressRegion?: string;
  postalCode?: string;
  areaServed?: string[];
  priceRange?: string;
};

export default function LocalBusinessJsonLd({
  name = 'Your Business',
  url,
  telephone,
  streetAddress,
  addressLocality,
  addressRegion,
  postalCode,
  areaServed,
  priceRange,
}: LocalBusinessJsonLdProps) {
  const data: Record<string, unknown> = {
    '@context': 'https://schema.org',
    '@type': 'LocalBusiness',
    name,
  };
  if (url) data.url = url;
  if (telephone) data.telephone = telephone;
  if (streetAddress || addressLocality || addressRegion || postalCode) {
    data.address = {
      '@type': 'PostalAddress',
      ...(streetAddress ? { streetAddress } : {}),
      ...(addressLocality ? { addressLocality } : {}),
      ...(addressRegion ? { addressRegion } : {}),
      ...(postalCode ? { postalCode } : {}),
    };
  }
  if (areaServed && areaServed.length) data.areaServed = areaServed;
  if (priceRange) data.priceRange = priceRange;

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  );
}
