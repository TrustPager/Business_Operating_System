// Landing page — the seven-section conversion skeleton in order
// (web-design-method.md Part 1). This is the one-page degenerate case; a
// multi-page site reuses these same components per page plus the site layer.
//
// The skill replaces the placeholder copy with the real, positive-only,
// on-page-SEO-correct copy it derives, and wires the JSON-LD components with
// real business data. The FAQ JSON-LD below mirrors the Faq section's default
// questions so the schema matches what renders; keep them in sync when the
// copy is filled in.
import Hero from '../components/sections/Hero';
import TrustBar from '../components/sections/TrustBar';
import Benefits from '../components/sections/Benefits';
import HowItWorks from '../components/sections/HowItWorks';
import SocialProof from '../components/sections/SocialProof';
import Faq from '../components/sections/Faq';
import FinalCta from '../components/sections/FinalCta';
import LocalBusinessJsonLd from '../components/seo/LocalBusinessJsonLd';
import FaqJsonLd from '../components/seo/FaqJsonLd';

// FAQ content, defined once and passed to BOTH the visible section and the
// JSON-LD, so the schema always matches the page (a mismatch is a quality risk).
const faqItems = [
  {
    question: 'How soon can you come out?',
    answer:
      'Most local jobs get a same-day or next-day slot. Call and we will confirm a time that suits you.',
  },
  {
    question: 'Do you give a price before starting?',
    answer:
      'Yes. You get a clear quote up front, so the number is agreed before any work begins.',
  },
  {
    question: 'Is your work guaranteed?',
    answer:
      'Every job is done to standard and backed by our guarantee, so it stays fixed.',
  },
];

export default function Home() {
  return (
    <>
      {/* Structured data — LocalBusiness high on the page, FAQPage mirroring
          the visible FAQ. Real values are wired by the skill. */}
      <LocalBusinessJsonLd />
      <FaqJsonLd items={faqItems} />

      {/* The skeleton, in order. */}
      <Hero />
      <TrustBar />
      <Benefits />
      <HowItWorks />
      <SocialProof />
      <Faq items={faqItems} />
      <FinalCta />
    </>
  );
}
