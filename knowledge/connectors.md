# Connector library

This is the catalog `connect-a-tool` reads to walk an owner through connecting a
tool, and to help them find connectors that fit their business. It is the "what
can I plug in, and what does it unlock" library.

**The honest boundary.** Connecting a tool is an authorization the OWNER performs
in their Claude app (it is an OAuth sign-in, so only they can click it). The
system does everything else: it explains the value, gives the exact steps for
their app, does the token-frugal and privacy thinking for them, verifies the
connection worked, and then puts it to use. This is the one "you do this bit"
step in an otherwise done-for-you setup, and the job is to make it stress-free.

**Token-frugality (always mention).** Connecting a tool loads its actions into
every future turn. Keep it lean: connect only what the owner needs now, and where
the connector offers scopes, enable only the groups in use. A brand-new owner on
a lighter plan should not have their context filled with tools they are not using.

---

## How an entry is shaped (the schema)

Every connector below follows the same shape, so adding a new one is drop-in and
the catalog stays searchable:

- **What it is**: one plain line.
- **Fits businesses that**: the business-need tags, so an owner can find it by
  "what do I want to do" rather than by product name.
- **Unlocks**: the concrete routines and skills it switches on.
- **Connect it**: the steps, per Claude app (the label may differ slightly by
  app version; guide to the Connectors area and adapt).
- **Keep it lean**: the scopes/groups to enable, and what to leave off.
- **Heads-up**: any credit, cost, or privacy note to say out loud first.
- **Verify**: the one lightweight read that proves it worked.

---

## Google Calendar

- **What it is:** the owner's calendar, readable and writable by their system.
- **Fits businesses that:** book appointments, run their day around a schedule,
  juggle jobs or meetings, want a morning brief of what's on.
- **Unlocks:** a morning brief that reads the day ahead; scheduling help;
  routines that key off upcoming events (prep for the next call, remind a client).
- **Connect it:** in the Claude app, open Settings, then Connectors (in Claude
  Code, run `/mcp`). Find the Google Calendar connector, choose Connect, and sign
  in with the Google account that holds their work calendar. Approve the access it
  asks for. Only they can complete this sign-in.
- **Keep it lean:** if asked which calendars, connect the one work calendar they
  actually run the business on, not every personal calendar.
- **Heads-up:** it can read event details and, if they allow it, create or change
  events. Nothing is created without asking. No credit cost to connect.
- **Verify:** ask the system to list their next few calendar events. If it can
  see them, the connection is live.

## Gmail

- **What it is:** the owner's email, so the system can read threads and draft
  replies for them to send.
- **Fits businesses that:** live in their inbox, chase quotes and follow-ups,
  answer the same kinds of enquiries all day, want drafts ready to send.
- **Unlocks:** drafting replies in the owner's voice; a routine that turns the
  morning's calendar into follow-up drafts; catching enquiries that went quiet.
- **Connect it:** in the Claude app, open Settings, then Connectors (in Claude
  Code, run `/mcp`). Find the Google / Gmail connector, choose Connect, and sign
  in with their work email account, approving the access it requests. Only they
  can complete this sign-in.
- **Keep it lean:** connect the one email account they run the business from.
  Where the connector separates reading from sending, start with drafting (read +
  compose drafts) and leave automatic sending off until they trust it.
- **Heads-up:** this lets the system read email content, so name that plainly and
  keep it to their business account. Drafts are prepared for them to review; it
  does not send on its own unless they set that up on purpose.
- **Verify:** ask the system to summarize the latest email in their inbox. If it
  can, the connection is live.

---

## The growing library (add by asking)

Gmail and Calendar are the starting pair because they power the Day-5 routine and
suit almost any business. Beyond them, the right connectors depend on the
business, and finding them is a great activity AFTER the challenge. Common next
ones owners ask for, by need:

- **Accounting (e.g. Xero):** live numbers, invoices, and reconciled cash flow.
- **Team chat (e.g. Slack):** route alerts and updates to where the team talks.
- **File storage (e.g. Google Drive):** read and organize documents in bulk.
- **A CRM:** the deepest one, it turns many keyless drafts into live, tracked
  actions (send the follow-up, move the deal, run the sequence).

When an owner wants one that is not written up here yet, treat it as a new catalog
entry: find its Connectors listing, learn the connect steps and the scopes, and
walk them through it with the same shape above. The point of this library is that
adding a connector is always the same friendly, verified walkthrough, never a
technical chore handed to the owner.
