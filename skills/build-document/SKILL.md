---
name: Build Document
description: Design and create a reusable signing document template in TrustPager — sections, merge fields, and the signer inputs the recipient fills. Plans the structure in chat for approval, then creates the template via MCP. Does NOT send it (that's send-for-signing).
triggers:
  - build a document template
  - create a signing document
  - set up a contract template
  - make a proposal template
  - build a signing process
  - draft a service agreement template
  - turn this PDF into a signing template
---

# Build Document

You're building a reusable **document template** the operator will send for
signing again and again — a proposal, service agreement, contract, consent
form. You plan the structure with the operator first, then create it.

**This builds the template. It does NOT send it.** Sending a copy to a real
signer is `send-for-signing`. Stay in build mode here.

Source of truth: [`knowledge/document-method.md`](../../knowledge/document-method.md)
— read §1 (anatomy) and §5 (test-before-send) before starting.

## Step 1 — Understand the document

Ask the operator, unless they've already said:

1. **What is it?** (proposal / agreement / consent / quote-to-sign…) and what
   outcome it drives.
2. **Who signs, and in what order?** One signer, or several (e.g. client +
   guarantor)? Each signer needs their own signature block.
3. **What goes in it?** The fixed copy, plus which parts vary per deal (these
   become merge fields).
4. **Starting from a sample?** If they have an existing PDF/Word doc or a paste,
   read it and reverse-engineer the section structure rather than inventing one.

## Step 2 — Plan the structure in chat (for approval)

Present the planned template as a section list BEFORE creating anything:

```
Template: "Broker Partnership Agreement"

1. Heading        — "Partnership Agreement"
2. Text           — intro paragraph (merge: {{contact.full_name}}, {{company.name}})
3. Text           — terms (fixed copy)
4. Text           — fee schedule (merge: {{deal.value}})
5. Signer input   — Signature · signer 1 (the broker)
6. Signer input   — Date · signer 1
```

For every merge field, confirm the opportunity actually carries that data —
a `{{deal.value}}` that's usually blank should not go in a contract (method §6).
For every signer, confirm there's a signature input. Wait for the operator's
go before writing anything.

## Step 3 — Create the template

Once approved, build it via MCP, in order:

1. `mcp__trustpager__create_document_template(name=...)` → capture the
   `template_id`.
2. For each section, `mcp__trustpager__add_document_section(template_id, type=..., ...)`
   in document order. (Run `describe_resource("document")` first if you're
   unsure of a section `type`'s exact shape — don't guess section payloads.)
3. If sections landed out of order, `reorder_document_sections(template_id, section_ids=[...])`.

Narrate what you're adding as you go. If a section write fails, stop and show
the error — don't push the rest on top of a broken template.

## Step 4 — Read it back + preview

- `get_document_template(template_id)` and show the operator the final structure.
- Offer to **preview the resolved document** against a draft/test opportunity
  (never a real client) so they can see every merge field filled and every
  signer input present — method §5. `render_document_template` produces a PDF
  they can eyeball.

End with: *"Template's built. When you're ready to send a copy to a signer, run
`/send-for-signing`. Want me to run `/lint-document` on it first to catch broken
merge fields or missing signatures?"*

## Hard rules

- **Don't send from this skill.** Building ≠ sending. Redirect send requests to
  `send-for-signing`.
- **Confirm the plan before creating.** Template structure is cheap to discuss,
  annoying to unpick after sections exist.
- **Never wire a merge field the opportunity can't fill** (method §6). Blank
  fields in a contract are a real problem.
- **Every signer needs a signature input.** A signer with no input has nothing
  to sign — the envelope will stall.
- **Reuse over one-offs.** If they'll send this more than once, it's a template.

## Output shape

A clear section plan first, then (after approval) a running narration of the
create calls, then the read-back structure and the offer to preview + lint.
