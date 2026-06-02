# Document & Signing Method

How to build a document/signing process in TrustPager and run it end to end —
template → send → opened → signed — without anything stalling silently.

This is the source-of-truth method behind `build-document`, `send-for-signing`,
`lint-document`, and `signing-radar`. Read the section a skill points you at
before you act.

## The one-sentence model

A **document template** is a reusable, merge-fielded document; you **send** a
copy of it to one or more **signers** attached to an opportunity; each signer
gets a private hosted page; TrustPager tracks that copy (an **envelope**)
through *sent → opened → signed → completed*.

You build the template once. You send it many times. Every send is an envelope
with its own lifecycle.

## 1. Anatomy of a document template

A template is an ordered list of **sections**, plus merge fields and signer
inputs.

- **Sections** (`add_document_section`, each has a `type`): text/HTML blocks,
  headings, signature blocks, signer-input fields, page breaks, images. Order
  matters and is set by `reorder_document_sections`.
- **Merge fields** — `{{contact.full_name}}`, `{{deal.name}}`,
  `{{company.name}}`, etc. — resolve at send time from the linked opportunity.
  A merge field with no backing data renders blank, so only use fields the
  opportunity actually carries.
- **Signer inputs** — fields the *recipient* fills/signs on their hosted page
  (signature, initials, date, text). Every signature a process needs MUST exist
  as a signer-input section, or the recipient has nothing to sign.

Tools: `create_document_template` (needs `name`) → `add_document_section`
(needs `type`) ×N → `reorder_document_sections` → `get_document_template` to
read it back. `render_document_template` renders a filled PDF into the file
library (useful for a non-signing "generate + send as attachment" path).

## 2. The two ways a document leaves the building

1. **For signing** (`send_for_signing`, scope `signing:send`) — the recipient
   lands on a TrustPager-hosted signing page, enters a PIN, views, and signs.
   This is the path that gives you open + sign tracking. Requires
   `template_id`, `signers` (array of `{name, email}`), and `deal_id`.
2. **As a generated PDF** (`render_document_template` → attach to an email) —
   a flat document, no signing, no per-recipient tracking beyond the email. Use
   only when nothing needs signing.

If the owner wants to "know when they open it / chase until signed", it has to
go via **send_for_signing** — that's the only path with a hosted page we can
track.

## 3. The envelope lifecycle (what you track)

Every `send_for_signing` creates an **envelope** with per-recipient state:

| State | Meaning | The signal |
|---|---|---|
| `sent` | emailed, not yet opened | `signature_sent` fired |
| `viewed` | recipient opened the signing page | `signature_opened` fired, `viewed_at` set |
| `signed` | that recipient signed | — |
| `completed` | all recipients signed | `signature_completed` fired |
| `declined` | a recipient declined | `signature_declined` fired |
| `voided` | cancelled by the sender | — |

`list_signing_envelopes` (optionally `?deal_id=`) is the board. `get_signing_envelope`
is the detail. `resend_signing_envelope` re-emails a stuck one;
`void_signing_envelope` kills one that's wrong or superseded.

**The money signal is `viewed` but not `signed`.** That recipient is engaged and
holding — the highest-value moment to follow up. `signing-radar` surfaces exactly
this set.

## 4. Automating the lifecycle (the four triggers)

These automation triggers fire off the lifecycle — wire them in `/automate-this`:

- `signature_sent` — the moment you send. Rarely needs an automation.
- `signature_opened` — **they opened it.** Notify the owner / create a "call now
  while it's hot" task. Or branch: if NOT opened in 48h, send a nudge.
- `signature_completed` — all signed. Kick off onboarding, move the stage, ask
  for a review.
- `signature_declined` — they declined. Alert the owner with the reason.

Available tokens in those automations: `{{recipient_name}}`, `{{document_title}}`,
`{{deal_id}}`, `{{opened_at}}`. (See `knowledge/automation-method.md` for how to
wire a trigger.)

## 5. The test-before-send discipline (non-negotiable)

A signing document goes to a real customer and is, often, a legal artefact. Get
it wrong and you've sent a broken or wrong contract to a client.

- **Always preview the resolved document before the first real send.** Use a
  draft/test opportunity (never a real client's) and confirm every merge field
  resolves and every signer input is present.
- **Confirm the signer list out loud** — names, emails, and order — before
  `send_for_signing`. A typo'd signer email means the contract goes nowhere or
  to the wrong person.
- **One real send at a time** until the template is proven. Don't batch-send a
  brand-new template to twelve clients.

## 6. The safety rails every signing skill carries

- **Never send to anyone but the confirmed signers.** No "test" sends to invented
  or `@example.com` addresses — they pollute the envelope list forever. Use a
  real draft opportunity with the owner's own address if you must test delivery.
- **Voiding is destructive-ish** — a voided envelope can't be un-voided; you
  re-send a fresh one. Always name the envelope before voiding and get a yes.
- **Don't delete a template that has live envelopes against it** without
  flagging that the historical envelopes stay but the template is gone.
- **Merge-field honesty** — never wire a merge field the opportunity can't fill.
  A blank `{{deal.value}}` in a signed contract is a real problem.

## 7. The discovery protocol (do this, don't memorise)

When you're unsure of a tool's exact shape, ask the workspace, don't guess:

- `describe_resource("document")` and `describe_resource("signing_envelope")` —
  the canonical tool surface + field hints.
- `get_document_template(template_id)` — read a real template's section shape
  before editing it.
- `get_trigger_schema("signature_opened")` — the exact trigger_data tokens.

## House rules (carry these into every document skill)

- **Build in the template, send from the opportunity.** The template is reusable;
  the envelope is per-deal. Don't hand-build one-off documents when a template
  will be reused.
- **Signing path for anything that needs a signature or open-tracking.** PDF-
  attachment path only for flat, untracked documents.
- **The hosted page is the only place an open is detectable.** "Did they read
  it?" is answerable only for `send_for_signing`, never for an emailed PDF.
- **Confirm signers + preview merges before the first send.** Every time a
  template is new or changed.
- **Surface stuck envelopes, don't let them rot.** Opened-not-signed and
  sent-never-opened are both follow-up gold; `signing-radar` is the check-up.
