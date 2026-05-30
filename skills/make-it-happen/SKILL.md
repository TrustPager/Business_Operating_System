---
name: make-it-happen
description: Describe what you want done in plain English. The skill figures out which TrustPager tools to call, in what order, and gets your approval at each destructive step.
triggers:
  - make it happen
  - just do it
  - sort this out
  - handle this for me
  - fix this
  - clean up
  - take care of
  - I need you to
---

# /make-it-happen

This is the catch-all skill. The user describes the outcome they want — not which tool to call, not which page to visit. Your job is to figure out the right TrustPager operations and execute them, with approval at each destructive step.

## The pattern

1. **Restate the request** in your own words. ("So you want me to: find every contact from the Sept newsletter, tag them, and add them to the 'October re-engagement' auto-queue. Got it?")
2. **List the steps** before doing them. ("Three calls: find the contacts via search, bulk-update with the tag, enrol in auto-queue. That work?")
3. **Wait for go.**
4. **Execute, one step at a time**, showing progress.
5. **Stop and ask** before any destructive operation. "About to delete 14 contacts — confirm?"
6. **Report what happened** with a clear yes-no on whether the outcome matches the original request.

## Use the right discovery tools

Before guessing, use TrustPager's discovery surface:
- `mcp__trustpager__get_ai_instructions` — workspace-specific guidance
- `mcp__trustpager__describe_resource(resource)` — what tools exist for an entity
- `mcp__trustpager__describe_action_type(action_type)` — config schema for one automation action
- `mcp__trustpager__get_trigger_schema(trigger)` — payload shape for a trigger
- `mcp__trustpager__list_action_types` — full action catalog

If you're not sure which resource is involved, ask the user with a multiple-choice question — don't guess.

## Hard-block destructive operations

ALWAYS require explicit approval for:
- `delete_*` (any tool)
- `bulk_delete_*`
- `update_user_role`, `remove_user`
- `release_phone_number`
- `disable_automation` on a published automation
- Sending email/SMS to more than 1 recipient (use `/send-email` instead, or batch through a campaign)
- Moving more than 10 opportunities at once

For each, present:
- Exactly what will happen ("delete 14 contacts: <list of names>")
- Why it appears to be the right move ("you said 'remove old test contacts'")
- The reverse path if it goes wrong ("we can't undo a delete — these go to soft-deleted for 30 days then are gone")

## Use existing skills when they fit

If the user's request matches an existing skill, RUN THAT SKILL instead of doing it from scratch:
- "Triage my new leads" → `/lead-triage`
- "What did I miss?" → `/sweep-my-day`
- "Re-engage cold leads" → `/follow-up-radar`
- "Send Sarah an email" → `/send-email`
- "Reply to this" → `/draft-reply`

This skill is for the gaps between named skills — bespoke multi-step operations the user only does occasionally.

## Approval queue (HTTP 202)

If a tool call returns HTTP 202 with an `approval_id`, the operation is queued for human approval. DO NOT try to bypass it. Tell the user:
> "Queued for approval — approve at https://app.trustpager.com/settings/api?tab=approvals (id: `<approval_id>`). The operation will run automatically once you approve."

Then stop. Don't poll. The user controls when to approve.

## Output shape

After the operation completes, summarize in one paragraph:
- What was requested
- What was done (with counts)
- Anything that was NOT done and why
- The next step the user might want

If there's anything that didn't work, say so plainly. Don't claim success on partial completion.
