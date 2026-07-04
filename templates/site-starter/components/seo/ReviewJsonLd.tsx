// ReviewJsonLd — schema.org AggregateRating + Review structured data
// (web-design-method.md Part 3). Pairs with the TrustBar and SocialProof
// sections so real ratings and testimonials reinforce E-E-A-T. HARD RULE:
// only emit ratings and reviews that are genuinely the business's. Never
// fabricate a rating value, a review count, or a testimonial. If there is no
// real data yet, render nothing (the skill leaves the slot and tells the owner).

type Review = { author: string; body: string; rating?: number };

type ReviewJsonLdProps = {
  itemName?: string;
  ratingValue?: number;
  reviewCount?: number;
  reviews?: Review[];
};

export default function ReviewJsonLd({
  itemName = 'Your Business',
  ratingValue,
  reviewCount,
  reviews,
}: ReviewJsonLdProps) {
  const hasAggregate = typeof ratingValue === 'number' && typeof reviewCount === 'number';
  const hasReviews = reviews && reviews.length > 0;
  if (!hasAggregate && !hasReviews) return null;

  const data: Record<string, unknown> = {
    '@context': 'https://schema.org',
    '@type': 'LocalBusiness',
    name: itemName,
  };
  if (hasAggregate) {
    data.aggregateRating = {
      '@type': 'AggregateRating',
      ratingValue,
      reviewCount,
    };
  }
  if (hasReviews) {
    data.review = reviews!.map((r) => ({
      '@type': 'Review',
      author: { '@type': 'Person', name: r.author },
      reviewBody: r.body,
      ...(typeof r.rating === 'number'
        ? { reviewRating: { '@type': 'Rating', ratingValue: r.rating } }
        : {}),
    }));
  }

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  );
}
