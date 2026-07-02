# Automation Recipes

**A catalogue of battle-tested TrustPager automations.** The hard part of automation isn't building one — it's knowing *what* to automate. This is the answer key.

`/automate-this` reads this file. When an operator says "what should I automate?" or describes a problem that matches a recipe, pull the recipe, adapt the names/values to their workspace, show the plain-English spec, and build it through the normal `/automate-this` flow (discover → spec → approve → **test** → enable). Read [`automation-method.md`](automation-method.md) first — these recipes assume that model.

Every recipe is written as **WHEN → ONLY IF → THEN**, plus the trigger/action primitives and the safety dials to set. Values (pipeline names, dollar thresholds, templates) are examples — always swap in the operator's real ones, pulled from their workspace.

> **Read first, then adapt — never paste literally.** Discover the live trigger and action types (`list_trigger_schemas`, `list_action_types`) and confirm each action's config with `describe_action_type` before writing. Recipes name the *shape*; the workspace supplies the specifics.

---

## Universal — every business should have these

### R1 · Missed-call recovery 🌐
The highest-ROI automation there is. A missed call is a warm lead you can still save with a 30-second text. The standard is a response inside 5 minutes in business hours; the 60-second automated first touch is the aspiration (business-method.md §10.3, directional). For a local business, R1 + R5 are the hard gate before any lead-generation spend (§10.5).
- **WHEN:** `call_voicemail` (voice agent) — or an inbound missed-call event if the workspace logs them.
- **ONLY IF:** caller has a contact record (skip unknown spam numbers if the operator prefers).
- **THEN:** 1) `send_sms` to the caller — *"Hi {{contact.first_name}}, sorry we missed you just now — what can we help with? Reply here and we'll jump straight on it."* 2) `add_tasks`: "Call back {{contact.first_name}}" due today. 3) `notify_assigned_staff`.
- **Dials:** dedup ON (15 min) so a double-ring doesn't double-text.

### R2 · New lead intake → acknowledge + organise 🌐  *(multi-trigger showcase)*
Leads arrive two ways and both deserve the same instant response. **One automation, two triggers** (§1.1 of the method doc) — don't build two. The 2-minute acknowledgement is what keeps every doorway inside the 5-minute response standard (business-method.md §10.3, directional).
- **WHEN (trigger 1):** `form_completed` — your TrustPager intake form.
- **WHEN (trigger 2):** `webhook_received` — the contact form on your website.
- **THEN:** 1) `create_opportunity` in the "Inbound" pipeline, "New" stage. 2) `apply_tags` "new-lead" + the source. 3) `send_custom_email` acknowledgement within 2 min. 4) `add_tasks`: "Qualify {{contact.first_name}}" due today.
- **Dials:** dedup ON (60 min). **Why multi-trigger:** identical actions, different doorways — if you'd copy-paste the chain, it's one automation with two triggers.

### R3 · Hot lead → notify the owner instantly 🌐
Big leads shouldn't wait in a queue to be noticed.
- **WHEN:** `deal_created` (any source).
- **ONLY IF:** `{ "deal.value": { "gte": 10000 } }` (use the operator's "this one matters" number).
- **THEN:** 1) `slack_send_message` (or `notify_assigned_staff`): "🔥 Hot lead: {{contact.first_name}} — ${{deal.value}}." 2) `apply_tags` "hot".
- **Dials:** none needed — it's notify-only.

### R4 · Quote/proposal sent → follow-up nudge 🌐
Most quotes die from silence, not rejection.
- **WHEN:** `stage_changed` into "Quote Sent" — or `document_sent` if quotes go out as documents.
- **THEN (single nudge):** `add_tasks` "Follow up on quote" due +3 days, **and** a `send_sms`/`send_custom_email` chase scheduled with a delay.
- **→ Better as a queue** if you want Day 3 / Day 7 / Day 14 touches — that's a drip, hand off to `/design-nurture-sequence`. Single chase = automation; sequence = queue.

### R5 · Invoice paid → ask for a review 🌐
The moment money lands is the warmest moment to ask for a review.
- **WHEN:** `xero_invoice_paid` (or your accounting integration's paid event).
- **ONLY IF:** not already reviewed (tag check `{ "tags": { "not_contains": "review-requested" } }`).
- **THEN:** 1) `request_review` (or `send_custom_email` with the review link). 2) `apply_tags` "review-requested".
- **Dials:** dedup ON; tag-guard prevents re-asking.

### R6 · Deal Won → kick off onboarding 🌐
- **WHEN:** `stage_changed` into "Won".
- **THEN:** 1) `attach_to_event_queue` → the onboarding auto queue (welcome, what-happens-next, first-deliverable). 2) `send_custom_email` welcome. 3) `add_tasks` "Set up {{customer.name}}".
- **Note:** the multi-step welcome lives in the **queue**; the automation just enrols them. Build the queue with the nurture-sequence skills. Doctrine shape: engineer a felt first win inside 7 days and a personal re-sell of the decision inside 48 hours (directional) — the queue carries the sequence, the personal touch stays personal (business-method.md §11.3).

### R7 · No-show / cancellation → reschedule 🌐
- **WHEN:** booking cancelled / no-show event (discover the exact `trigger_type` for the operator's scheduler — e.g. `calcom_*`, `booking_*`).
- **THEN:** 1) `send_sms`: "No worries — grab a new time here: {{booking_link}}." 2) `add_tasks` to chase if they don't rebook.
- **Dials:** dedup ON.

### R8 · Inbound message → never-miss triage 🌐
- **WHEN (multi-trigger):** `sms_received` **or** `email_received`.
- **ONLY IF:** from a known contact (optional).
- **THEN:** 1) `notify_assigned_staff`. 2) `add_tasks` "Reply to {{contact.first_name}}" due today.
- **Note:** notify + task only — don't auto-reply to inbound humans unless the operator explicitly wants an autoresponder.

---

## Trades & on-the-tools 🔧

### R9 · Job complete → review + rebook
- **WHEN:** `stage_changed` into "Job Complete" (or work-order closed).
- **THEN:** 1) `request_review`. 2) `send_sms`: "Thanks {{contact.first_name}}! If you ever need us again, just text this number." 3) `apply_tags` "past-customer" (feeds a future re-engagement queue).

### R10 · Site-visit booked → prep + reminder
- **WHEN:** `booking_created`.
- **THEN:** 1) `add_tasks` "Load van for {{contact.first_name}} — {{booking_address}}". 2) `send_sms` reminder the day before (delay). 3) attach to a "day-of" queue if you run reminders.

---

## Mortgage & finance broking 💰

### R11 · Pre-approval expiry → re-engage before it lapses
- **WHEN:** `scheduled` (date-based) — N days before `pre_approval_expiry` custom field.
- **ONLY IF:** opportunity still open.
- **THEN:** 1) `send_custom_email`: "Your pre-approval expires soon — let's keep it live." 2) `add_tasks` for the broker.
- **Dials:** `max_executions_per_day` cap as a backstop on date sweeps.

### R12 · Document collection chase
- **WHEN:** `stage_changed` into "Docs Outstanding".
- **THEN:** 1) `send_form` (the doc-checklist form) or `send_custom_email` listing what's needed. 2) `add_tasks` "Chase docs" +2 days.
- **→ Queue** if you want escalating reminders (Day 2 / 5 / 8).

---

## Insurance broking 🛡️

### R13 · Referral intake → quoting engine  *(multi-trigger showcase)*
The InsureHQ pattern. A referral lands via the TrustPager intake form **or** the broker's website, and either way the client's data must hit the external quoting API.
- **WHEN (trigger 1):** `form_completed` (intake form).
- **WHEN (trigger 2):** `webhook_received` (website form).
- **THEN:** 1) `create_opportunity` in "Life Insurance", "Referral Received". 2) `call_webhook` → the quoting engine with the mapped fields. 3) `notify_assigned_staff`.
- **Dials:** dedup ON (60 min); **set `max_executions_per_day`** — a `call_webhook` to an external API is exactly the kind of action you cap as a seatbelt.

### R14 · Policy renewal reminder
- **WHEN:** `scheduled` — N days before `renewal_date`.
- **THEN:** `send_custom_email` renewal nudge + `add_tasks` for the broker.

---

## Allied health 🩺

### R15 · Appointment reminder + no-show recovery
- **WHEN:** `booking_created` → reminder the day before (delay). Plus a **second automation**: no-show event → `send_sms` rebook link. (Different actions per event = separate automations.)
- **THEN (reminder):** `send_sms`: "Reminder: your appt with {{practice_name}} is tomorrow at {{booking_time}}."
- **Compliance note:** keep clinical detail out of SMS — time + practice name only.

### R16 · Recare / recall
- **WHEN:** `scheduled` — N months after last visit (date field).
- **THEN:** `send_custom_email` "time for your check-up" + `add_tasks`.
- **→ Queue** for a gentle 2-3 touch recall rather than a single email.

---

## Consultancy & professional services 📊

### R17 · Discovery call booked → prep + brief
- **WHEN:** `booking_created` for the discovery event type.
- **THEN:** 1) `add_tasks` "Prep brief for {{contact.first_name}}". 2) optionally schedule the notetaker for the booking. 3) `send_custom_email` "looking forward — here's what we'll cover."

### R18 · Proposal follow-up
- **WHEN:** `document_sent` (the proposal) or `stage_changed` into "Proposal Sent".
- **THEN:** single chase task + delayed email. Escalating cadence → queue.

---

## Retention & saves 🤝

### R21 · Retention cadence — the personal-touch sweep
The retention cadence (business-method.md §11.4) runs on scheduled personal contact — so this recipe creates TASKS, never auto-sends.
- **WHEN:** `scheduled` — a sweep of active customers whose last personal touch is older than the cadence (default ~14 days, directional; use the operator's number).
- **ONLY IF:** active customer; no open task of this kind already on them.
- **THEN:** 1) `add_tasks`: "Personal check-in with {{contact.first_name}} — something specific to them, not a blast", assigned to the named relationship owner. 2) `notify_assigned_staff`.
- **Dials:** `max_executions_per_day` cap; a tag/condition guard so the same customer doesn't re-enter the sweep every day.
- **Never** convert this to a `send_custom_email` — a blast is exactly what the cadence is not.

### R22 · Cancellation → the save conversation
No silent cancellations — every cancel gets a real conversation within 24 hours (business-method.md §11.5). The automation guarantees the conversation happens; it never makes the save offer itself (safeguards.md §5).
- **WHEN:** the workspace's cancellation/churn event (discover the exact trigger — a subscription cancelled, a membership ended, a stage change into "Cancelled").
- **THEN:** 1) `add_tasks`: "Save call with {{contact.first_name}} — within 24 hours" (run it as a discovery conversation: why they joined, what changed, what result they still want). 2) `notify_assigned_staff`. 3) `apply_tags` "cancel-save-open".
- **After the call:** log the exit in three buckets — never activated / product failed them / life happened — the distribution picks the fix (business-method.md §11.5).
- **Dials:** dedup ON.

---

## Re-engagement & reawakening ♻️

Old leads you already quoted are the cheapest pipeline you'll ever work — they
know you, you have their details, and someone already did the qualifying. The
trap is treating "send them some emails" as the whole job. The real unit is a
**multi-channel enrolment machine**: pipeline stages + the two automations that
enrol and un-enrol + the email queue + a backing SMS. Build the machine, not
the mailing list.

### R19 · Aged-lead reawakening campaign  *(the full machine — multi-channel)*
A time-boxed push to reactivate leads you quoted but never closed. Owner makes
the call; the machine backs every call with an SMS and a drip so nobody goes
cold between attempts.

**The pieces (build in this order):**

1. **A pipeline** with the campaign's own stages, e.g.
   `To Call → No Answer — Nurturing → Call Back → Booked → Subscribed → Remove from Nurturing → Not Interested`.
   Load the aged leads into `To Call` (filter by age + ownership — see the
   ownership rule below).
2. **Stage automation A — enrol on entering "No Answer — Nurturing":**
   - **WHEN:** `stage_changed` into `No Answer — Nurturing`.
   - **THEN:** 1) `attach_to_event_queue` → the reawakening queue (enrols them
     in the drip). 2) `send_sms` — the backing text, sent as the owner, that
     reminds them who you are and gives two easy paths (call back **or** book):
     *"Hi {{contact.first_name}}, {{owner.first_name}} from {{company.name}}
     here — tried to reach you and sent an email. We automate your sales + ops
     into one system, and there's a free trial on right now. Worth a quick
     call? Ring me back, or book here: {{booking_link}}."*
   - **Dials:** dedup ON so re-entering the stage doesn't double-enrol/text.
3. **Stage automation B — un-enrol on entering "Remove from Nurturing":**
   - **WHEN:** `stage_changed` into `Remove from Nurturing` (and/or `Booked` /
     `Subscribed` / `Not Interested`).
   - **THEN:** remove them from the queue so a booked or dead lead stops
     getting drip emails. This is the half everyone forgets — without it, leads
     who already replied keep getting "haven't started yet?" emails.
4. **The email queue** — the drip itself (Day 0 / 7 / 14 / 21 / 28 / 38 / 49,
   or whatever cadence). Build it with `/design-nurture-sequence` then
   `/wire-nurture-sequence`. It only fires for leads who are enrolled (i.e.
   who hit `No Answer — Nurturing`), so a lead you reach on the first call
   never gets a single drip email.

**Channels working together:** the call is the spearhead; the SMS lands the
moment the call misses (familiar name → higher pickup next time); the email
drip carries the offer and the deadline. Three channels, one machine.

**Ownership rule (adapt to the operator's):** many teams hand a fresh lead to a
setter for its first N days, then it reverts to the closer. Reassign the
campaign's leads to whoever's actually working them before you start, so calls,
SMS, and "from" lines all come from the right person.

**Time-box it.** A reawakening push that reuses your onboarding email assets
should have a hard close date, so it doesn't overlap with people who later
sign up and get those same emails fresh. Set the deadline, and disable the
queue when it passes.

### R20 · Past-customer win-back  *(evergreen)*
Lighter, always-on cousin of R19 for customers who bought once and went quiet.
- **WHEN:** `scheduled` — N months after last activity / last invoice.
- **ONLY IF:** no open opportunity already, not unsubscribed.
- **THEN:** 1) `apply_tags` "win-back". 2) `attach_to_event_queue` → a short
  2-3 touch win-back queue (we miss you / what's new / a reason to come back).
- **Dials:** dedup ON; tag-guard so they don't re-enter every sweep.
- **→ Queue, not a single email** — a gentle multi-touch beats one "we miss
  you" that's easy to ignore.

> Health-check any live re-engagement machine with `/nurture-health` — it
> shows which step is leaking and whether the un-enrol side is actually firing.

---

## How to choose & adapt a recipe

1. **Match the problem, not the label.** "Leads slip through" → R2/R8. "Quotes go cold" → R4. "We forget to ask for reviews" → R5/R9.
2. **Swap in their real names** — pipelines, stages, templates, dollar thresholds. Pull them from the workspace; don't invent.
3. **Decide automation vs queue** (method §4): one-shot reaction = automation; timed series = queue → hand off.
4. **Same actions from two doorways?** One automation, multiple triggers (R2, R13). Different actions? Separate automations (R15).
5. **Set the dials** — dedup on anything that sends; `max_executions_per_day` on anything with a `call_webhook` or a feedback path.
6. **Spec → approve → test → enable.** Recipes don't skip the rails.

> If the operator wants something no recipe and no existing action covers, that's a feature request — `/make-it-happen file a feature request`, don't fake it with a fragile `call_webhook` workaround unless they explicitly want one.
