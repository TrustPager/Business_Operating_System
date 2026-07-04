// FaqJsonLd — schema.org FAQPage structured data (web-design-method.md Part 3).
// Pairs with the Faq section so the same questions that clear doubt also earn
// FAQ rich results. Pass the SAME questions and answers rendered on the page;
// mismatched schema is a quality risk. The skill supplies real Q&A.

type QaItem = { question: string; answer: string };

type FaqJsonLdProps = {
  items?: QaItem[];
};

export default function FaqJsonLd({ items = [] }: FaqJsonLdProps) {
  if (!items.length) return null;

  const data = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: items.map((item) => ({
      '@type': 'Question',
      name: item.question,
      acceptedAnswer: {
        '@type': 'Answer',
        text: item.answer,
      },
    })),
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  );
}
