---
name: Set Up A Routine
description: Turn a recurring job into something your system runs on its own. Once you've connected a tool like Gmail or Google Calendar, this builds a real routine on top of it (for example a morning brief that reads your day and drafts your follow-ups), sets it on a schedule, shows it working once, and hands you plain-language controls to pause or change it.
triggers:
  - set up a routine
  - make it run itself
  - automate my mornings
  - build me a morning brief
  - run this every day
  - run this every week
  - take this off my plate for good
  - have it do this automatically
function_slot: comms
requires_driver: none
requires_credential: mcp
data_path: mcp_tools
status: active
---

# Set Up A Routine

This is the operator moment: the owner stops doing a recurring job by hand and
their system starts doing it on a schedule. The feeling to deliver is "it runs
the work now, I just operate." Keep it concrete and safe, and always end with the
routine actually running, not just described.

The flagship routine is a **morning brief**: each morning the system reads the
day's calendar and drafts the follow-up emails the owner would otherwise write by
hand, ready for them to glance at and send. It is the clearest proof that the
system takes work off their plate.

## Prerequisite: a connected tool

A routine runs on something. The good ones here run on the owner's connected
tools (Gmail, Google Calendar). If nothing useful is connected yet, do not stall:
hand off to `connect-a-tool` to connect Gmail and Calendar first (that is the
Day-5 pairing), then come back here. If they only want a routine over a keyless
app they already use (say a weekly review of their own numbers), that is fine too,
you just schedule that instead.

## Step 1: Pick the job to automate

Start from what actually eats their week. Pick ONE to start; a single routine that
runs beats three they never trust.

**Suggest a candidate first (diagnose, don't just ask).** Before asking them to
name a task, read `./CLAUDE.md`: the "what would you most love to hand off" note,
the diagnosed constraint, and anything about how they spend their week. Look for a
**repeatable by-hand task they do the same way every time** (chasing quiet leads,
the morning follow-ups, a weekly numbers check, the same recap sent again and
again) and propose the single best one in plain words, matched to a routine shape
below: *"You mentioned you chase quotes by hand every week. That's exactly the
kind of thing I can run for you. Want me to set that up?"* Proposing a concrete
candidate beats a blank "what do you want to automate?", the owner often cannot
name it cold. If the profile gives you nothing to go on, then ask in one line.
This is the diagnose-then-build path Day 5 of the challenge uses; it works the
same standalone.

## Step 2: Design it concretely, and safely

Say back exactly what the routine will do, when it will run, and what it will
produce, in plain language. Hold two safety lines:

- **It prepares, it does not fire.** Routines produce drafts and summaries for the
  owner to review. Nothing gets sent to a customer, and nothing gets changed,
  without the owner's say-so. Auto-send stays off unless they explicitly turn it
  on later, once they trust it.
- **One clear cadence.** Daily first thing, or weekly on a chosen morning. Do not
  over-engineer the timing.

## Step 3: Set it up for them

Do the setup yourself, with permission, never hand them a command to run. Ask
"want me to set this to run every weekday at 7am?" and on yes, create the
scheduled routine using the scheduling the owner's app provides. Give it a plain,
recognizable name ("Morning brief"). If the app cannot schedule unattended runs,
say so honestly and set it up as a one-tap routine they trigger, rather than
pretending it runs on its own.

## Step 4: Run it once now (the wow)

Do not leave them imagining it. Run the routine a single time immediately so they
see the real output: today's brief, today's drafts. This is the moment it becomes
real. If a draft is off, tune it and note the preference so the routine improves.

## Step 5: Hand them the controls

Close by telling them, in plain words:
- what it will do and when ("every weekday at 7am, you'll have your day and your
  follow-up drafts waiting"),
- that nothing sends without them,
- and how to pause or change it ("just tell me to pause the morning brief, or
  change the time, any time").

## Routine shapes (starter set)

- **Morning brief (flagship, calendar + email):** reads today's calendar, drafts
  the follow-ups and prep the day calls for, leaves them ready to review.
- **Weekly review:** a set morning each week, a short digest of what happened and
  what needs attention (works over connected tools, or over the owner's own
  numbers keylessly).
- **Weekly numbers check-in, kept as plain text (phone-first, no spreadsheet):**
  for an owner who does not use spreadsheets or works mostly from their phone,
  keep the same small set of weekly numbers (a five-number cut of the
  `business-method.md` §12.6 scoreboard, e.g. leads, conversations, jobs won, cash
  collected, plus the one metric that matters most this quarter) as a plain dated log
  in the `## My weekly numbers` section of `./CLAUDE.md` (the single home for this
  log, newest first). Each week they bring the numbers, you read
  the last few weeks back with the one thing to work on, then append the new week
  below the last. Same weekly rhythm as the scoreboard, held as text they never
  open a spreadsheet to use. Be honest about the shape: it is a check-in you run
  together each week, not something running on its own.
- **Quiet-lead follow-up:** spots enquiries or threads that went quiet and drafts
  a warm nudge for each, for the owner to approve.

When the routine is a customer-contact or cadence routine (regular check-ins on
active customers), follow the retention cadence spec (`business-method.md`
§11.4): a named owner for each relationship, a weekly checkbox so it can't
quietly decay, contact that is genuinely specific to that customer, and never
a blast.

## Hard rules

- **Permission first, then you do it.** Never tell a non-technical owner to run a
  command or a file. You set the routine up; they only say yes.
- **Nothing sends or changes without the owner.** Routines draft and summarize;
  auto-send is off unless they deliberately enable it later.
- **Always run it once so they see it work.** A routine they have not seen is not
  a win yet.
- **Reversible and clear.** Pause, change the time, or stop, all in plain language.
- **Plain language only.** They never hear "cron", "job", "MCP", or "scheduler
  token". They hear "routine", "runs every morning", "I'll set it up".
- **Positive, outcome-led, no em dashes** in anything the owner reads.
