---
name: Learn My Business
description: Read the operator's live TrustPager workspace and WRITE their CLAUDE.md profile for them — company + brand, the real pipeline stages, products and prices, lead sources, opportunity types. Replaces hand-copying an industry template and filling in the blanks. Run once at setup, or re-run when the workspace shape changes.
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

The industry templates ask the operator to pick the right one and hand-fill a
dozen `<<< ... >>>` blanks. Most never do — so Claude starts every session not
knowing their pipeline, products, or stages. This skill removes that step: it
reads the live workspace and writes a filled, accurate `CLAUDE.md` for them.

## Step 1 — Read the workspace shape

```bash
python skills/learn-my-business/fetch.py
```

Returns the real shapes: company profile + brand, every pipeline with its
actual stage names, products with prices, lead sources, opportunity types,
lost/won reasons, and rough record counts. It's best-effort — check `warnings`
and `_sources`; for anything that came back `unavailable`, ask the operator one
short question rather than guessing (e.g. company-profile endpoints vary, so you
may need to ask "what's your business name and what do you do?").

**Fallback if the script can't run:** `list_pipelines` + `list_pipeline_stages`,
`list_products`, `get_company_profile`, `get_crm_settings`.

## Step 2 — Choose the base template

Look at `company.industry` and the pipeline shape, then pick the closest base:

- mortgage / finance → `templates/industries/mortgage-broker/CLAUDE.md`
- trades / on-the-tools → `templates/industries/trades/CLAUDE.md`
- insurance → `templates/industries/insurance/CLAUDE.md`
- consultant / professional services → `templates/industries/consultant/CLAUDE.md`
- allied health → `templates/industries/allied-health/CLAUDE.md`
- manufacturing → `templates/industries/manufacturing/CLAUDE.md`
- anything else → `templates/CLAUDE.md` (generic)

Read the chosen template so the file you write keeps its structure and its
industry-specific gotchas — you're filling it in from real data, not inventing
a new format.

## Step 3 — Write the CLAUDE.md

Fill every `<<< ... >>>` from the digest:

- **My business** — name, city/country, description from `company`. If industry
  is known, say it.
- **Products / services** — real product names + prices from `products`.
- **Pipeline** — the actual `stages` of the default pipeline, in order. If there
  are several pipelines, list the primary one's stages and name the others.
- **Lead sources** — tick the boxes that match `settings.lead_sources`.
- **Ideal customer / tone** — leave as a short prompt for the operator to
  confirm; you can draft a first guess from the industry, but flag it as a guess.

Then **write it to `./CLAUDE.md` in the operator's project folder.**

- If `./CLAUDE.md` does NOT exist → write it, then show a summary of what you filled.
- If it DOES exist → do NOT overwrite silently. Show the proposed file, point out
  what differs from the current one, and ask before replacing. (Their existing
  file may have hand-tuned voice/rules worth keeping — merge, don't clobber.)

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
`/learn-my-business` whenever your pipeline, products, or brand change."

## Hard rules

- ❌ Don't overwrite an existing `CLAUDE.md` without showing the diff and asking.
- ❌ Don't invent products, prices, or stages — use the real ones from the
  workspace. If a section is `unavailable`, ask one question; don't fabricate.
- ❌ Don't fill the "ideal customer" / "tone" sections as if they were read from
  data — they're your guess; label them for confirmation.
- ✅ Keep the chosen template's structure and industry gotchas intact.
- ✅ Use the operator's exact stage and product names, spelled as the workspace
  spells them.

## Output shape

A one-line "wrote/updated CLAUDE.md" confirmation, a 4-6 line summary of what
was filled from real data, then the short list of guessed/blank items to
confirm. If you didn't write (because one existed), show the proposed content
and the ask instead.
