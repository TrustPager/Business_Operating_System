---
name: Onboard Team Member
description: Set up a new team member on Claude Code with your team's standards baked into their setup. Reads the team-standards file plus the live workspace, then generates the new person's CLAUDE.md, a memory pack, and a role-scoped command list into ./team/<name>/ to install, so the whole team follows one process. Re-run to refresh when standards change.
triggers:
  - onboard a team member
  - add someone to my team
  - set up a new hire on claude
  - onboard sarah
  - give my team the standards
  - generate a teammate's claude setup
function_slot: people
requires_driver: none
requires_credential: none
data_path: local
status: active
---

# Onboard Team Member

A team only runs well on Claude Code if everyone shares the same standards: one
customer voice, the same verify-before-it-ships discipline, and clear role
boundaries. Pasting those into a new hire's chat teaches them for one session,
then it evaporates. This skill instead **writes the standards into the new
person's own persistent setup** — their `CLAUDE.md` and a memory pack — so they
follow them by default from day one.

The single source of truth is **`templates/team-standards.md`** (the owner edits
it once). This skill generates each person's setup from it. When standards
change, re-run this skill for each person to refresh their pack (it shows a diff
before overwriting).

## Step 1 — Confirm who you're onboarding

You need three things. If the command didn't supply them, ask in one short
message:

- **Name** (e.g. "Sarah Lee").
- **Email** (their login / workspace email, if the team uses a connected CRM).
- **Role** — must match a role row in `templates/team-standards.md` section 3
  (e.g. `manager`, `ae`, `sdr`, `ops`). If they gave a role that isn't in the
  table, ask which existing role fits, or tell them to add the row to
  team-standards first.

## Step 2 — Read the standards and shared context

1. Read **`templates/team-standards.md`** in full: the team voice (section 1),
   the verify-before-customer gate (section 2), the role table (section 3),
   approval rules (section 4), escalation/handoffs (section 6), playbooks
   (section 7). This is the spec for what goes into the person's pack.
2. Read the owner's **`./CLAUDE.md`** (if present) for shared business context:
   business name, products, pipeline stages, lead sources, brand. The new
   person needs the same business context, not a blank one.
3. Read **`knowledge/communication-voice.md`** and **`knowledge/safeguards.md`**
   so the generated pack matches the canonical voice + verify-first wording.

If `templates/team-standards.md` doesn't exist yet, stop and tell the owner to
create it first (copy the starter), because there are no standards to propagate
without it.

## Step 3 — Generate the onboarding pack into `./team/<name>/`

Create a folder `./team/<slug>/` (slug = lowercased first name, e.g.
`./team/sarah/`) and write these files. If the folder already exists, do NOT
overwrite silently — show what changed and ask first (their pack may have
hand-tuned notes worth keeping).

**a) `./team/<slug>/CLAUDE.md`** — the person's context file. Build it from the
owner's `./CLAUDE.md` (shared business context: the owner's own business-context
block, i.e. business, products, pipeline, lead sources, copied as-is) PLUS a
role-specific section that states, in plain language:
- Their name and role.
- The team voice in one line + a pointer: "All customer messages follow the team
  voice — see `memory/team-voice.md`."
- The verify-before-customer rule in one line + pointer to `memory/verify-first.md`.
- Their role boundaries from the role table, written as explicit can / cannot
  bullets (e.g. for `sdr`: "You draft customer replies; a manager approves before
  they send. You do not change pipeline stages or disable automations.").
- Who they escalate to (from section 6).

**b) `./team/<slug>/memory/team-voice.md`** — the team voice, lifted from
`knowledge/communication-voice.md` and any business-specific voice rules from
team-standards section 1. Keep it short and instructive.

**c) `./team/<slug>/memory/verify-first.md`** — the verify-before-customer gate
from `knowledge/safeguards.md` section 4 + team-standards section 2, in the
"order, every time" form.

**d) `./team/<slug>/memory/role-and-approvals.md`** — their role's permissions
and the approval rules that apply to them (from sections 3 and 4). Include the
role's RESULT in one sentence at the top, from the role row in team-standards
(a handed-over role is defined by its result and standards, business-method.md
§12.4). If the role row has no result stated, ask the owner one short question
rather than omitting it.

**e) `./team/<slug>/commands.md`** — the list of slash commands this role gets,
and which are restricted, derived from the role's permissions. For example an
`sdr` gets `/sweep-my-day`, `/prep-for-call`, `/log-this-call`, `/draft-reply`
(draft only), `/follow-up-radar`; they do NOT get `/automate-this`,
`/audit-my-automations`, or send-without-approval. State the restricted ones
explicitly with one line on why.

Write every value explicitly — real business name, real role bullets, real
command names. Never leave a `<<< ... >>>` placeholder in a generated pack; if a
value is missing from team-standards, ask the owner one short question rather
than emitting a blank.

## Step 4 — Hand over install steps (so it persists on THEIR machine)

The pack only sticks if the new person installs it into their own project. Give
the owner a short, copy-paste set of steps to forward to the new hire:

```
1. Install Claude Code, and install the Business Operating System (see INSTALL.md).
2. If the owner uses a connected CRM, connect your workspace with your own key
   (run the setup wizard). Skip this if the team runs keyless.
3. Copy the CLAUDE.md and the memory/ folder from the pack you were sent into the
   root of your Claude Code project folder.
4. Tell your Claude, once: "Read CLAUDE.md and everything in memory/, and follow
   it as my standing instructions." Confirm it saved/loaded them.
```

This is the persistence step: the standards now live in the new person's own
`CLAUDE.md` + memory, not in a one-off chat.

Remind the owner: the pack covers standards; the first weeks still run the
delegation loop in person (business-method.md §12.1), and training sticks two
ways: watching the best, and doing it with feedback (§12.2).

## Step 5 — Confirm + close

Show the owner a tight summary:

```
✓ Generated onboarding pack for Sarah Lee (sdr) → ./team/sarah/
  • CLAUDE.md (business context + sdr boundaries + team voice + verify-first)
  • memory/: team-voice, verify-first, role-and-approvals
  • commands.md: 5 commands (draft-only on replies); automations restricted
  Next: forward ./team/sarah/ + the 4 install steps to Sarah.
```

If you didn't write (a pack already existed), show the proposed changes and the
ask instead.

## Hard rules
- ❌ Never grant a junior role more than its row in `team-standards.md` allows.
  An `sdr`'s pack must say drafts-only and exclude automation/delete commands.
- ❌ Never emit a `<<< ... >>>` placeholder in a generated pack — fill it from
  team-standards or the workspace, or ask one short question.
- ❌ Don't overwrite an existing `./team/<slug>/` pack without showing the diff
  and asking.
- ❌ Don't invent business facts (products, stages, brand) — copy them from the
  owner's `./CLAUDE.md`. If it's missing, run `/learn-my-business` first or ask.
- ✅ Standards come from ONE source (`team-standards.md`). This skill propagates;
  it never redefines the voice or rules itself.
- ✅ The generated pack is explicit and complete (the same bar every prompt
  meets): real values, real command names, real boundaries, no vague stand-ins.
- ✅ Re-running refreshes a person's pack from updated standards — always via a
  shown diff, never a silent clobber.

## Output shape
A one-line "generated/updated pack for <name> (<role>) → ./team/<slug>/"
confirmation, a 4-6 line summary of what the pack contains, and the handoff line
(forward the folder + the install steps). If a pack already existed, show the
proposed content + the ask instead.
