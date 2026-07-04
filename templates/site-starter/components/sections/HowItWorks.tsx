{/* @dsCard group="sections" */}
// HowItWorks — section 4 of the conversion skeleton (web-design-method.md
// Part 1). Job: 3-4 plain steps showing what happens after the customer acts.
// Lowers perceived risk by making the process known and simple. HowTo/step
// content captures "how does X work" intent. Each step framed as smooth and
// handled. Placeholder, positive-only copy; reads design tokens as CSS vars.

type Step = { title: string; body: string };

type HowItWorksProps = {
  heading?: string;
  steps?: Step[];
};

export default function HowItWorks({
  heading = 'How it works',
  steps = [
    { title: 'You call', body: 'Tell us what is going on. We listen and confirm we can help.' },
    { title: 'We confirm a time that suits you', body: 'Pick a slot that works. We turn up when we say we will.' },
    { title: 'We sort it', body: 'The job is done properly, tidied up, and guaranteed.' },
  ],
}: HowItWorksProps) {
  return (
    <section className="bg-panel">
      <div className="mx-auto max-w-content px-6 py-20">
        <h2 className="text-center text-3xl font-bold">{heading}</h2>
        <ol className="mt-12 grid gap-8 sm:grid-cols-3">
          {steps.map((step, i) => (
            <li key={step.title} className="text-center">
              <span
                className="mx-auto flex h-12 w-12 items-center justify-center bg-primary text-lg font-bold text-panel"
                style={{ borderRadius: 'var(--radius-full)' }}
              >
                {i + 1}
              </span>
              <h3 className="mt-4 text-lg font-semibold">{step.title}</h3>
              <p className="mt-2 text-text-muted">{step.body}</p>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}
