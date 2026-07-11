# ADR 0002 — TrustPager stays reactive and off the acquisition pages (with one labelled Day 5 exception)

**Status:** Accepted (2026-07-11).
**Context owner:** the operative rule lives in [`knowledge/connectors.md`](../../knowledge/connectors.md) (the single home for the connect-doorway articulation) and founder-decision D3 in [`docs/architecture/founder-decisions.md`](../architecture/founder-decisions.md). This ADR records the decision and the one intentional exception; it does not restate the rule.

## Context

TrustPager is the CRM/platform BOS ships a full driver for, and the AI BOS is the top of a warm funnel into it. The standing doctrine is that TrustPager is **reactive**: the keyless floor stands alone and is complete on its own, and TrustPager is named only when the owner reaches for it (asks what else the system can do, or asks about connecting a CRM). It is kept **off the acquisition surfaces** (the AI BOS About and Community pages) and out of the cold onboarding path in `start-here`, so the first experience is never a pitch. This protects trust and keeps the floor honest.

The tension the doctrine already anticipates: TrustPager "surfaces when a member reaches connecting a CRM." Day 5 of the 5-day challenge is exactly that moment, deep inside the product, not an acquisition page: the owner has built their whole floor and explicitly asked what to connect next (`plan-my-roadmap`).

## Decision

1. **Keep the reactive rule everywhere it already applies.** `start-here`, the floor skills, and the acquisition pages never name TrustPager cold. This is unchanged.
2. **Day 5's `plan-my-roadmap` is a single, labelled exception (Option 2, "named where it fits").** In the roadmap, TrustPager may be named as an **earned recommendation among options**, only where it genuinely fits the owner's goal and their Day 4 constraint (a sales, retention, or customer-ops constraint where a connected CRM is the direct lever). It is presented honestly: it needs a paid subscription, other CRMs they already use are welcome, and it is never the only option and never a hard sell. Where the constraint points elsewhere (accounting, ads, publishing), the roadmap names the generic connector that fits instead.

Options considered: (1) generic connectors only, (2) named where it genuinely fits, (3) TrustPager as the default recommended CRM. Founder chose **Option 2** on 2026-07-11.

## Consequences

- The AI BOS → TrustPager funnel warms at its designed point, without diluting the reactive doctrine elsewhere.
- `plan-my-roadmap`'s SKILL.md carries the naming rule inline and points here, so the exception is labelled and traceable, not silent drift.
- If the challenge ever adds another surface that names TrustPager, it must be added here as an explicit exception too, or it is drift.
- The operative "how to articulate a connect doorway" rule remains owned by `knowledge/connectors.md`; this ADR only governs *whether TrustPager is named by product name* and *where*.
