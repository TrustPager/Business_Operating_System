---
name: Learn My Business
description: Read the operator's live TrustPager workspace and WRITE their CLAUDE.md profile for them — company + brand, the real pipeline stages, products and prices, lead sources, opportunity types — folding in any industry gotchas from knowledge/industry-notes.md. The single front door to setup; replaces hand-filling a template. Run once at setup, or re-run when the workspace shape changes.
triggers:
  - learn my business
  - set up my CLAUDE.md
  - build my workspace profile
  - configure claude for my business
  - onboard me
  - read my workspace and set me up
  - generate my context file
---

# Learn My Business

Hand-filling a template means picking the right one and completing a dozen
`<<< ... >>>` blanks. Most operators never do — so Claude starts every session
not knowing their pipeline, products, or stages. This skill is the front door
that removes that step: it reads the live workspace and writes a filled,
accurate `CLAUDE.md` for them, with any industry-specific gotchas folded in.

## Step 1 — Read the workspace shape (MCP calls)

Use the `trustpager` MCP server. Everything here is a read — free, nothing journaled, no approval. Fire what you can in parallel.

| Need | Tool | Args / notes |
|---|---|---|
| Company profile + brand | `get_company` | Returns name, industry, website, city/country, branding/primary colour, description, timezone. (Note: `get_company_profile` is a *different* tool — the public reputation page — don't use it for this.) |
| Pipelines | `list_pipelines` | `limit: 100` |
| Stages for each pipeline | `list_pipeline_stages` | one call per pipeline id — stages are **not** inline on the pipeline list; fetch them per pipeline (in parallel) and order by `position` |
| Products + prices | `list_products` | `limit: 100` — capture name, price/unit_price, currency, billing interval |
| Lead sources, opportunity types, lost/won reasons | `get_crm_settings` | read `lead_sources`, `opportunity_type_options`, `lost_reasons`, `won_reasons` |
| Rough record counts | `list_deals`, `list_contacts`, `list_customers`, `list_automations` | `limit: 100` each — report the page count, or "100+" if the response indicates more pages |

> Tool names use `deal` for legacy reasons — **always say "opportunity" to the operator**, never "deal". (`list_deals` = opportunities, `list_customers` = companies/accounts.)

This is best-effort. If any call errors or comes back empty (company-profile and crm-settings shapes vary by workspace), don't guess — note it and ask the operator one short question instead (e.g. "what's your business name and what do you do?").

## Step 2 — Load the structure + the industry gotchas

There is one base template: **`templates/CLAUDE.md`** — read it so the file you
write keeps its structure (including the fixed "About TrustPager" block) and you
fill it from real data rather than inventing a new format.

Then match the operator's industry to a section in **`knowledge/industry-notes.md`**
using `company.industry` and the pipeline shape:

- mortgage / finance, trades, insurance, consultant / professional services,
  allied health, manufacturing → read that section.
- nothing fits → use the generic template as-is and ask one or two short
  questions about their pipeline quirks and comms style.

If the industry is ambiguous or couldn't be read, **ask one short question**
("what would you call your line of work?") rather than guessing the section.
Pull that section's **gotchas** and **comms style** into the file you write —
but treat them as industry patterns to confirm, never as facts read from the
workspace (see hard rules).

## Step 3 — Write the CLAUDE.md

Fill every `<<< ... >>>` from the data you pulled:

- **My business** — name, city/country, description from the company profile. If industry
  is known, say it.
- **Products / services** — real product names + prices from `list_products`.
- **Pipeline** — the actual stages of the default pipeline, in order. If there
  are several pipelines, list the primary one's stages and name the others.
- **Lead sources** — tick the boxes that match `crm_settings.lead_sources`.
- **Ideal customer / tone** — leave as a short prompt for the operator to
  confirm; you can draft a first guess from the industry, but flag it as a guess.

Then **write it to `./CLAUDE.md` in the operator's project folder.**

- If `./CLAUDE.md` does NOT exist → write it, then show a summary of what you filled.
- If it DOES exist → do NOT overwrite silently. Show the proposed file, point out
  what differs from the current one, and ask before replacing. (Their existing
  file may have hand-tuned voice/rules worth keeping — merge, don't clobber.)

## Step 3b — Create the memory store

So Claude can remember things about this business from the next session on, make
sure the memory store exists. If `./.bos-memory/MEMORY.md` does NOT exist, create
the folder and write a starter index:

```markdown
# Memory Index

One line per memory. Files live alongside this one (`<slug>.md`), one fact each.
Claude reads this index at the start of every session and recalls a file when
its description is relevant. Add memories with `/remember`.
```

Don't seed it with guesses — leave it empty. The model is in
`knowledge/memory-and-feedback.md`. (If `./.bos-memory/MEMORY.md` already exists,
leave it untouched.)

## Step 4 — Confirm + close gaps

Show the operator a tight summary:

```
✓ Wrote CLAUDE.md from your workspace:
  • Business: <name> — <industry>, <city>
  • Pipeline "Sales": New lead → Qualified → Quote sent → Negotiation → Won
  • 4 products (CRM Suite $129/mo, AI Audit $499, ...)
  • Lead sources: Website form, Meta ads, Referrals

Two things I couldn't read and guessed — please confirm:
  • Your ideal customer (I drafted a line from your industry)
  • Your tone preferences (left as a prompt)
```

End by telling them: "Claude will use this from your next session. Re-run
`/learn-my-business` whenever your pipeline, products, or brand change. I'll also
remember things as we work — tell me to remember anything with `/remember`."

## Hard rules

- ❌ Don't overwrite an existing `CLAUDE.md` without showing the diff and asking.
- ❌ Don't invent products, prices, or stages — use the real ones from the
  workspace. If a section couldn't be read, ask one question; don't fabricate.
- ❌ Don't fill the "ideal customer" / "tone" sections as if they were read from
  data — they're your guess; label them for confirmation.
- ✅ Keep `templates/CLAUDE.md`'s structure (incl. the "About TrustPager" block) intact, and fold in the matched industry section's gotchas + comms style.
- ✅ Industry gotchas are *patterns to confirm*, not workspace facts — present them as defaults the operator can correct, and let real workspace data win where they conflict.
- ✅ Use the operator's exact stage and product names, spelled as the workspace
  spells them.

## Output shape

A one-line "wrote/updated CLAUDE.md" confirmation, a 4-6 line summary of what
was filled from real data, then the short list of guessed/blank items to
confirm. If you didn't write (because one existed), show the proposed content
and the ask instead.
