// ServiceJsonLd — schema.org Service structured data (web-design-method.md
// Part 3). One per service page, so search engines understand the offer and
// the area it covers. The skill passes real values; never emit invented data.

type ServiceJsonLdProps = {
  name?: string;
  description?: string;
  providerName?: string;
  areaServed?: string[];
  serviceType?: string;
};

export default function ServiceJsonLd({
  name = 'Your Service',
  description,
  providerName,
  areaServed,
  serviceType,
}: ServiceJsonLdProps) {
  const data: Record<string, unknown> = {
    '@context': 'https://schema.org',
    '@type': 'Service',
    name,
  };
  if (description) data.description = description;
  if (serviceType) data.serviceType = serviceType;
  if (providerName) {
    data.provider = { '@type': 'LocalBusiness', name: providerName };
  }
  if (areaServed && areaServed.length) data.areaServed = areaServed;

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  );
}
