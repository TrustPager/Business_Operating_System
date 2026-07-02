---
name: Design Nurture Sequence
description: Design a multi-step email nurture sequence in the operator's voice — pick the help-center video for each stage, draft the subject + body per email, anchor each to a verbatim customer pain. Drafts in chat for review. Does NOT touch the live auto queue (that's wire-nurture-sequence).
triggers:
  - design a nurture sequence
  - draft the welcome sequence
  - draft a drip campaign
  - design a trial onboarding sequence
  - write the auto queue emails
  - design the post-signup sequence
function_slot: comms
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
status: active
---

# Design Nurture Sequence

You're drafting a multi-step email sequence in the operator's voice. Each
email is anchored to a verbatim customer pain from the synthesis, picks
the help-center video that most directly addresses the concern at that
point in the journey, and follows the canonical email shape.

**This is a DESIGN skill, not a deploy skill.** It produces drafts the
operator reviews in chat. To push the drafts into a live auto queue, the
operator then runs `wire-nurture-sequence`.

The source of truth for the method is
[`knowledge/marketing-strategy-method.md`](../../knowledge/marketing-strategy-method.md)
— read its "Layer 4 — Designing a nurture sequence" section before
starting.

## Prerequisites

The operator must have already authored:
- `voice.md` (how to write — built by `build-brand-strategy`)
- `value-props.yaml` (what to claim)
- `content-pillars.yaml` (themes)
- A customer-voice synthesis (verbatim pain to anchor each email)

If any of these are missing, STOP and ask the operator to run the prior
skill. Don't invent the brand voice on the fly.

## Step 1 — Confirm the sequence shape

Ask the operator:

1. **Which auto queue?** (Name or ID — they should already have it set up
   with stages, even if the email actions are empty.) Confirm the queue
   exists by running `python ~/.claude/bos-run.py tool dump-crm-bundle --resources auto_queues`
   and reading the result.
2. **Audience + trigger.** Who's enrolled and when (e.g. trial signups
   moving into a "Welcome" stage, Facebook leads via form submission).
3. **Goal of the sequence.** Drive conversion, drive activation, drive
   referral, etc. Map the goal to its doctrine before drafting:
   - **Activation** → the activation protocol (business-method.md §11.3):
     a felt first win inside the first days, plus a personal re-sell
     touch inside 48 hours (directional) — which may be a task for the
     operator rather than an email.
   - **Conversion** → the next-win timing (§9.4): each email sells the
     solution to the problem the previous win just revealed; the line
     the reader sees names the next win.
   - **Retention** → the retention cadence (§11.4): personal and
     specific, never a newsletter blast — a mass sequence may be the
     wrong tool here; say so.
4. **The stages and their delays.** Default to whatever the auto queue
   already has. Common shape: Day 0 (immediate) → Day 2 → 4 → 6 → 8 → 10
   → 12.

## Step 2 — Map a help video to each stage

The TrustPager help center is the canonical library. List articles via:

```bash
curl -s "https://api.trustpager.com/functions/v1/help-center-public?action=list" \
  | python -c "import sys, json; [print(f\"{a['slug']} | {a['title']}\") for a in json.load(sys.stdin)['articles']]"
```

For each stage:

1. **Identify the customer concern that's MOST ACUTE by that point** in
   the trial — i.e. the strongest unaddressed pain from synthesis §2
   given what earlier emails have already covered. Every solved problem
   reveals the next one; the stage order follows the problem chain, not
   the feature list (business-method.md §9.4).
2. **Find the help video whose title most directly addresses that concern.**
3. **Cross-reference against the canonical pain themes** in synthesis §2.
4. **If the chosen video is feature-led** (e.g. "AI Needs Analysis"),
   check whether it actually cuts a real customer concern. Feature-
   showcase ≠ concern-cutting. If it doesn't, pick a different video.

Present the mapping as a table:

| Day | Stage | Video | Why this lands (synthesis anchor) |
|---|---|---|---|
| 0 | Welcome | (link) | (anchor) |
| 2 | First Win | (link) | (anchor) |
| ... | ... | ... | ... |

Wait for the operator to approve the mapping before drafting bodies.
They'll often swap one or two videos based on knowledge you don't have.

## Step 3 — Draft each email

For each step, follow the canonical shape:

```
Subject: <forward-looking, action-oriented verb the reader can agree to>

<HTML body with <p> tags>

<warm human opener — "Hi {{contact.first_name}}" or "Great to meet you ..." for Day 0>

<one paragraph: the core idea — the anchor (ONE verbatim pain or outcome from synthesis) informs it; the copy states the outcome>

<one paragraph: what the video shows, why it matters>

<the link — raw URL as both href and visible text>

<warmest regards sign-off block>
```

Hard rules per email:

- **Subject = a verb.** "Let's streamline your operations" beats "Thanks
  for your enquiry". Don't lead with receipts of past actions.
- **One core idea per paragraph.** Don't stuff three customer pains into
  one sentence.
- **Customer phrases are seasoning, not the meal.** Use ONE verbatim
  pain anchor per email at most. Use the founder's voice for everything
  else.
- **No banned register.** No VC-bro, no Salesforce-enterprise speak, no
  AI-as-hero framing, no copywriter abstractions. See voice.md's "Watch
  out for" section.
- **Words that are FINE.** *Streamline*, *facilitate growth*,
  *operations*, *strategy*. These are normal business English.
- **One soft CTA.** The help video. No aggressive funnel pushes.
- **Sign-off block, verbatim.** Whatever voice.md says is the locked
  closer.
- **Raw URL as href + visible text.** Never breadcrumbs.
- **HTML with `<p>` tags.** Plain-text `\n` doesn't render right in
  Gmail.

## Step 4 — Present all drafts in chat

Present the full set in chat, scannable. Per-email format:

```
### Day X — <stage name>

**Subject:** ...

<HTML body in a code block>

*Anchor: <synthesis quote + speaker + reason it lands>*
```

Two notes at the bottom of your output:

1. **Open variables** — anything you used a `{{template_var}}` for that
   isn't standard (e.g. `{{assignee.first_name}}` for the assigned team
   member). Flag for the operator to verify in TrustPager's automation
   builder.
2. **Cross-references between emails** — if Day 4's email references
   Day 2's video ("If you got Claude connected on Tuesday..."), flag it.
   Soft language is better than hard branching.

End with: *"Edits welcome on any of these. When you give the green
light, I'll run `wire-nurture-sequence` to push them into the auto
queue via MCP."*

## Hard rules

- **NO em dashes in any email copy.** The emails are customer-facing output: em
  dashes never appear (use commas, colons, parentheses, or separate sentences).
  Check every draft before presenting it.
- **The pain anchor is internal rationale** (it picks the video and the
  idea); the shipped sentence leads and closes on the outcome
  (business-method.md §18). The anchor citation under each draft names the
  pain; the email body names the win.
- **Don't write to the auto queue from this skill.** That's the next
  skill (`wire-nurture-sequence`). Stay in design mode.
- **Iterate in chat, not in MCP.** Voice corrections take 2-3 rounds.
  Cheaper to do them in markdown than in live automation actions.
- **Quote the synthesis for every anchor.** If you can't cite a specific
  quote for why an email lands, you're inventing pain.
- **Default to fewer emails over more.** A 4-step sequence done well
  beats a 7-step sequence with two filler emails. Almost all conversion
  and churn is decided early (business-method.md §11.3), so front-load
  the first-win emails.
- **The convert-day email is special.** It's the strongest "concern-
  cutting" video + the conversion close + an explicit out for "if it's
  not working, tell me what's missing". Don't soften this.
