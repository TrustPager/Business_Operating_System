---
name: Lint Document
description: Pre-flight a document/signing template before it goes to a client — every signer has a signature input, no broken or always-blank merge fields, required sections present, disclaimers in place. Read-only; reports fails first, then warnings.
triggers:
  - lint my document
  - check my signing template
  - is this contract template ready
  - review my document template
  - check this document before I send it
  - pre-flight my signing document
---

# Lint Document

Catch the embarrassing, client-facing mistakes in a document template BEFORE
the first send: a signer with nothing to sign, a `{{merge_field}}` that always
renders blank, a missing signature block, a stray placeholder. Read-only — this
skill never edits the template; it routes each fix to `/build-document`.

Source of truth: [`knowledge/document-method.md`](../../knowledge/document-method.md)
— the checks map to §1 (anatomy) and §6 (merge-field honesty).

## Step 1 — Load the template

If the operator named it by title, find it with `mcp__trustpager__list_document_templates`,
then `mcp__trustpager__get_document_template(template_id)` to read its full
section structure. If they didn't say which, ask.

## Step 2 — Run the checks

Work through every section and signer:

**FAILS (block the send):**
- **Signer with no input** — a named signer who has no signature/initials input
  section. They'd have nothing to sign; the envelope stalls.
- **Signature input with no signer** — an orphan signature block assigned to a
  signer that isn't in the signer set.
- **Broken merge token** — a `{{ }}` that isn't a real field path (typo'd
  `{{contact.fullname}}`, unclosed `{{deal.value`, unknown namespace).
- **Empty template** — no body sections, or no signature input at all.

**WARNINGS (worth a look):**
- **Likely-blank merge field** — a field the opportunity usually doesn't carry
  (e.g. `{{deal.value}}` on a workspace that leaves value empty). Flag for the
  operator to confirm it'll be filled at send time.
- **Placeholder text left in** — "Lorem ipsum", "TODO", "[INSERT…]", "XXXX",
  a draft date.
- **No dated signature** — a signature input with no accompanying date field
  (most agreements want the signing date captured).
- **Missing disclaimer/terms** for an agreement-type document, if the operator's
  `CLAUDE.md` or brand notes say one is required.

## Step 3 — Report, fails first

```
📄 "Broker Partnership Agreement" — 1 fail, 2 warnings

❌ FAILS (fix before sending)
  → Signer "Guarantor" has no signature input. Add one, or remove the signer. → /build-document
  → Merge token {{contact.fulname}} is misspelled (should be {{contact.full_name}}). → /build-document

⚠️ WORTH A LOOK
  → {{deal.value}} is used in the fee schedule but is often blank on your deals — confirm it'll be filled.
  → No date field next to the broker's signature — most agreements capture the signing date.
```

End with the single most important fix, and route every fix to `/build-document`
(this skill doesn't edit). If it's clean: *"Clean — every signer has an input,
all merge fields resolve, no placeholders. Ready for `/send-for-signing`."*

## Hard rules

- **Read-only.** Never edit the template here. Diagnose, route to `/build-document`.
- **Fails before warnings.** Lead with what would actually break or embarrass.
- **Don't invent required disclaimers** — only flag a missing one if the
  operator's own notes/brand say it's required.
- **A likely-blank merge field is a warning, not a fail** — the operator may
  fill it per-deal; surface it, don't block on it.

## Output shape

Headline tally, then FAILS, then WARNINGS, then the one fix to make first — or
a clean bill of health with the hand-off to `/send-for-signing`.
