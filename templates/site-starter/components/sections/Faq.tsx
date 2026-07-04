{/* @dsCard group="sections" */}
// Faq — section 6 of the conversion skeleton (web-design-method.md Part 1).
// Job: answer the last few hesitations at the decision point. The single
// richest section for question keywords, FAQPage schema (components/seo/
// FaqJsonLd), and "near me" voice intent. Each answer framed as a reason to
// go ahead. Placeholder, positive-only copy; reads design tokens as CSS vars.
// Uses native <details> so it works with zero JS (Core Web Vitals headroom).

type QaItem = { question: string; answer: string };

type FaqProps = {
  heading?: string;
  items?: QaItem[];
};

export default function Faq({
  heading = 'Questions, answered',
  // These defaults are a standalone-render fallback only. The SOURCE OF TRUTH
  // for the live page is the `faqItems` array in app/page.tsx, which is passed
  // to both this section and FaqJsonLd so the visible FAQ and its schema always
  // match. Edit the copy there, not here.
  items = [
    { question: 'How soon can you come out?', answer: 'Most local jobs get a same-day or next-day slot. Call and we will confirm a time that suits you.' },
    { question: 'Do you give a price before starting?', answer: 'Yes. You get a clear quote up front, so the number is agreed before any work begins.' },
    { question: 'Is your work guaranteed?', answer: 'Every job is done to standard and backed by our guarantee, so it stays fixed.' },
  ],
}: FaqProps) {
  return (
    <section className="bg-panel">
      <div className="mx-auto max-w-3xl px-6 py-20">
        <h2 className="text-center text-3xl font-bold">{heading}</h2>
        <div className="mt-10 divide-y divide-border">
          {items.map((item) => (
            <details key={item.question} className="group py-5">
              <summary className="cursor-pointer list-none text-lg font-semibold">
                {item.question}
              </summary>
              <p className="mt-3 text-text-muted">{item.answer}</p>
            </details>
          ))}
        </div>
      </div>
    </section>
  );
}
