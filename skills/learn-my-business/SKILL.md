---
name: Learn My Business
description: Once a CRM is connected, read the operator's live TrustPager workspace and DEEPEN their CLAUDE.md profile from real data — company + brand, the real pipeline stages, products and prices, lead sources, opportunity types — folding in any industry gotchas from knowledge/industry-notes.md. This is the connected deepener, not the cold front door: brand-new or keyless owners start with /start-here (a 60-second brain-dump, no accounts needed); this runs once a workspace is connected, or re-runs when its shape changes.
triggers:
  - learn my business
  - set up my CLAUDE.md
  - build my workspace profile
  - configure claude for my business
  - onboard me
  - read my workspace and set me up
  - generate my context file
function_slot: strategy
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - mcp__list_pipelines
  - mcp__list_pipeline_stages
  - mcp__list_products
  - mcp__get_company_profile
  - mcp__get_crm_settings
status: active
---

# Learn My Business

**This is the connected deepener, not the cold front door.** Brand-new and keyless
owners start with `/start-here` — a 60-second brain-dump that fills the profile and
lands a real win with zero accounts. This skill picks up *after* a CRM is connected:
it reads the live workspace and replaces the inferred guesses in `CLAUDE.md` with
filled, accurate data — the real pipeline, products and prices, stages, lead
sources — with any industry-specific gotchas folded in. Run it once on connect, and
re-run it whenever the workspace shape changes.

## Step 1 — Read the workspace shape

```bash
python ~/.claude/bos-run.py learn-my-business
```

Returns the real shapes: company profile + brand, every pipeline with its
actual stage names, products with prices, lead sources, opportunity types,
lost/won reasons, and rough record counts. It's best-effort — check `warnings`
and `_sources`; for anything that came back `unavailable`, ask the operator one
short question rather than guessing (e.g. company-profile endpoints vary, so you
may need to ask "what's your business name and what do you do?").

**Fallback if the script can't run:** `list_pipelines` + `list_pipeline_stages`,
`list_products`, `get_company_profile`, `get_crm_settings`.

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

If the industry is ambiguous or `unavailable`, **ask one short question**
("what would you call your line of work?") rather than guessing the section.
Pull that section's **gotchas** and **comms style** into the file you write —
but treat them as industry patterns to confirm, never as facts read from the
workspace (see hard rules).

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
- ✅ Keep `templates/CLAUDE.md`'s structure (incl. the "About TrustPager" block) intact, and fold in the matched industry section's gotchas + comms style.
- ✅ Industry gotchas are *patterns to confirm*, not workspace facts — present them as defaults the operator can correct, and let real workspace data win where they conflict.
- ✅ Use the operator's exact stage and product names, spelled as the workspace
  spells them.

## Output shape

A one-line "wrote/updated CLAUDE.md" confirmation, a 4-6 line summary of what
was filled from real data, then the short list of guessed/blank items to
confirm. If you didn't write (because one existed), show the proposed content
and the ask instead.
