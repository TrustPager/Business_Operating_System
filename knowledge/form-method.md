# Form Method

How to build a form process in TrustPager and run it end to end — template →
fields wired to CRM → sent/intake → opened → completed → PDF on the timeline —
without orphan fields or stalled submissions.

Source-of-truth method behind `build-form`, `wire-form`, `lint-form`, and
`form-radar`. Read the section a skill points you at before you act.

## The one-sentence model

A **form template** is a reusable set of **fields**; each field is **wired** to
a CRM variable so answers land on the right record; you **send** it to a
recipient (or wire it to an intake), and each send is a **submission** that
moves *sent → opened → in-progress → completed*, auto-archiving a PDF when done.

Build the template + wiring once. Send/collect many times.

## 1. Anatomy of a form template

- **Fields** (`add_form_field`, each needs `type` + `label`) — text, email,
  phone, number, date, select, checkbox, file upload, signature, etc. Order is
  set by `reorder_form_fields`.
- **Field wiring** — the high-leverage part. Each field maps to a CRM variable
  (`contact.email`, `deal.value`, a custom field…) via
  `bulk_update_form_field_wiring`. A wired field writes the answer onto the
  record automatically. An **unwired field is an orphan** — the answer is
  captured on the submission but never lands on the contact/opportunity, so it's
  invisible to the rest of the CRM.
- **PIN** — internal forms are PIN-protected; the recipient gets a code to open
  their copy. Built in; you don't manage it per-send.

Tools: `create_form_template` (needs `name`) → `add_form_field` (needs `type`,
`label`) ×N → `bulk_update_form_field_wiring(template_id, wiring)` →
`reorder_form_fields`. `get_form_template` + `list_form_fields` read it back.

## 2. The label rule (don't skip this)

**Every field's label must match what the answer means on the CRM record it
wires to.** A field labelled "Phone" wired to `contact.mobile` is fine; a field
labelled "Summary" wired to a freetext note that an AI then dumps three
paragraphs into is the classic mismatch. If a field collects a specific piece of
data, its label and its wiring target must agree. Mislabelled→miswired fields
are the #1 source of "the data went in but I can't find it".

## 3. The three ways a form gets filled

1. **Sent to a named recipient** (`send_form`, scope `forms:send`, costs credits)
   — outbound link emailed to a contact for them to fill. Requires `template_id`,
   `recipient_email`, `recipient_name`. Fires `form_sent` → `form_opened` →
   `form_completed`.
   - **Shared submissions (Scope 3 / co-applicants):** pass `additional_recipients`
     (array of `{ email, name, contact_id? }`) to send joint applicants their own
     link + PIN -- all share ONE submission, all write to the same answer fields,
     any can finalize. Use for joint mortgage applicants, guarantors, co-account
     holders. `get_form_submission` returns the `form_submission_participants`
     array showing viewed/completed state per co-applicant.
   - **Automation `recipient_source: "all_contacts"`:** resolves every contact
     linked to the opportunity and fans out as above (primary owns the submission,
     the rest become participants). Use for deal-triggered multi-party sends.
2. **Internal fill** (`create_internal_form_submission`, needs `template_id` +
   `deal_id`) — staff enters the data themselves; no email, PIN pre-cleared.
3. **Intake / website** — the form is wired to an automation trigger so inbound
   submissions create or update records. NOTE: a public *website* contact form
   is NOT this internal-form system — that's a webhook trigger
   (`generic_webhook`). `form_completed`/`form_opened`/`form_sent` are for
   PIN-protected form templates we send, not website visitors.

## 4. The submission lifecycle (what you track)

`list_form_submissions` (optionally `?template_id=`) is the board. Each
submission carries a status:

| State | Meaning | Signal |
|---|---|---|
| `pending` / `sent` | sent, not opened | `form_sent` fired |
| `viewed` | recipient opened the form | `form_opened` fired, `viewed_at` set |
| `in_progress` | started, not finished | partial answers saved |
| `completed` | submitted | `form_completed` fired; PDF auto-archived |
| `expired` | link lapsed unfilled | — |

**Follow-up gold:** `viewed`/`in_progress` but not `completed` — they started and
stalled. And `sent` but never `viewed` past N days — chase or resend
(`resend_form_submission`). `convert_form_submission_to_pdf` / the auto-archive
puts the completed form on the opportunity's document library.

## 5. Automating the lifecycle

Wire these in `/automate-this`:
- `form_opened` — they opened it; nudge if they don't finish, or notify the owner.
- `form_completed` — submitted; route the data, move the stage, trigger the next step.

Tokens: `{{recipient_name}}`, `{{template_name}}`, `{{deal_id}}`, `{{opened_at}}`,
plus the wired field answers.

## 6. Safety rails

- **No orphan fields in a shipped form.** Every field that collects real data is
  wired, or you've consciously decided it's display-only.
- **Real recipients only** for `send_form` — never a test/`@example.com` address
  (pollutes the submission list, costs credits).
- **Don't delete a template with live submissions** without flagging that the
  submissions stay but the template's gone.
- **Voiding/deleting a submission is destructive** — name it, get a yes;
  `delete_form_submission` can also wipe the archived PDF.

## 7. Discovery protocol

- `describe_resource("form")` — canonical tool surface + field hints.
- `get_form_template(template_id)` + `list_form_fields(template_id)` — read the
  real field + wiring shape before editing.
- `get_trigger_schema("form_completed")` — exact trigger_data tokens.

## House rules

- **Wire every field to its CRM home.** A form whose answers don't land on the
  record is a survey, not a CRM process.
- **Label = meaning = wiring target.** Keep all three in agreement (§2).
- **Send path for outbound, intake path for inbound, webhook for website forms.**
  Don't reach for `form_completed` on a public website form.
- **Chase stalled submissions** — `form-radar` is the check-up; opened-not-
  completed and sent-never-opened are both follow-up gold.
