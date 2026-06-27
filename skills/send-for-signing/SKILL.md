---
name: Send For Signing
description: Send a copy of a document template to one or more signers on an opportunity — with the safeguards (confirm signers, preview merges, one real send at a time). Creates a tracked signing envelope.
triggers:
  - send for signing
  - send the contract to the client
  - send this proposal to sign
  - get this signed
  - email the agreement for signature
  - send the document to the signers
function_slot: documents
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - mcp__trustpager__send_for_signing
  - mcp__trustpager__list_document_templates
  - mcp__trustpager__search_opportunities
status: active
---

# Send For Signing

You're sending a real document to real signers. Every send creates a tracked
**envelope** and emails the recipient a hosted signing page. This is a live,
customer-facing action — get the signer or the merge data wrong and a client
receives a broken or wrong contract.

Source of truth: [`knowledge/document-method.md`](../../knowledge/document-method.md)
— read §2, §5 (test-before-send) and §6 (safety rails) before sending.

## Hard prerequisites

Before any `send_for_signing` call, you need all three:

1. **The template** — its `template_id`. List with
   `mcp__trustpager__list_document_templates` if the operator named it by title.
   If the template doesn't exist yet, redirect to `/build-document`.
2. **The opportunity** — the `deal_id` the document attaches to. Search with
   `mcp__trustpager__search_opportunities` if you only have a name. The envelope
   and all tracking thread onto this opportunity.
3. **The signers** — an array of `{name, email}`. Confirm spelling and order
   out loud with the operator. For multi-signer documents, confirm who's signer
   1 vs 2 (it drives signing order + which signature block they fill).

## Step 1 — Confirm, out loud, before sending

Read the send back to the operator and wait for a yes:

```
About to send for signing:
  Document : "Broker Partnership Agreement"
  To       : Jane Broker <jane@realbrokerage.com.au>
  On deal  : "Real Brokerage — Partnership"
  Subject  : Your partnership agreement to sign
```

If the template has merge fields, offer to **preview the resolved document
first** (render against this opportunity) so they see the filled contract
before a client does. For a brand-new or just-edited template, strongly
recommend it — method §5.

## Step 2 — Send

```
mcp__trustpager__send_for_signing(
  template_id=...,
  deal_id=...,
  signers=[{name, email}, ...],
  subject=...,        # optional but recommended
  message=...,        # optional cover note
)
```

One send at a time. Capture the returned `envelope_id`.

## Step 3 — Confirm + hand off to tracking

- Confirm the send landed (envelope created, recipients `sent: true`).
- Tell the operator the envelope now tracks itself: they'll get the
  `signature_opened` signal when the recipient opens it, and
  `signature_completed` when it's signed.
- Point them at the follow-on: *"Run `/signing-radar` any time to see who's
  opened, who's stuck, and who still hasn't looked. Want me to set up an
  automation that pings you the moment they open it? — that's `/automate-this`
  on the `signature_opened` trigger."*

## Hard rules

- **Real signers only.** Never send to an invented or `@example.com` address to
  "test" — it pollutes the envelope list permanently. To test delivery, send to
  the operator's own address on a draft opportunity.
- **Never to a real client without explicit confirmation** of the exact signer
  list and the deal. Read it back; get a yes.
- **One real send at a time** for a new template until it's proven.
- **Don't invent merge data.** If a field would render blank in the contract,
  flag it before sending — don't send a half-filled legal document.
- **If it returns an approval gate (202 / approval required), stop and tell the
  operator to approve it** — don't try to route around it.

## Output shape

The confirmation block, the (optional) preview offer, then — after the yes —
the send result and the hand-off to `/signing-radar` + the open-notification
automation tip.
