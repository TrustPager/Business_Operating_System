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

This is the catch-all skill. The operator describes the outcome they want — not which tool to call, not which page to visit. Your job is to figure out the right TrustPager operations and execute them, with approval at each destructive step.

## Step 1 — Warm the discovery surface (parallel MCP reads)

Before planning, pull the workspace's AI-facing reference data in one parallel batch off the `trustpager` MCP server, and keep it in memory for the rest of the conversation (re-referencing it costs nothing):

| Need | Tool | Args |
|---|---|---|
| Workspace workflow guidance + common mistakes | `get_ai_instructions` | — |
| Every automation trigger type + its `{{variable}}` tokens | `list_trigger_schemas` | — |
| Existing automations (to spot "you already have one of these") | `list_automations` | `limit: 100` |

These are all free reads. `list_trigger_schemas` returns the trigger types and the trigger-data shape each publishes; for one trigger's full payload use `get_trigger_schema(trigger_type: "<type>")`. There is **no client-side action-type catalog tool** — to learn an action's config, read the `config` field description on `add_automation_action` (it documents every `action_type`'s required fields), or check `using-trustpager-mcp.md` / `knowledge/automation-recipes.md`.

> Tool names use `deal` for legacy reasons — **always say "opportunity" to the operator**, never "deal".

## The pattern

1. **Restate the request** in your own words. ("So you want me to: find every contact from the Sept newsletter, tag them, and add them to the 'October re-engagement' auto-queue. Got it?")
2. **List the steps** before doing them. ("Three calls: find the contacts via search, bulk-update with the tag, enrol in auto-queue. That work?")
3. **Wait for go.**
4. **Execute, one step at a time**, showing progress.
5. **Stop and ask** before any destructive operation. "About to delete 14 contacts — confirm?"
6. **Report what happened** with a clear yes-no on whether the outcome matches the original request.

## Use the right discovery tools

Before guessing, use TrustPager's discovery surface on the `trustpager` MCP server:
- `get_ai_instructions` — workspace-specific guidance.
- `list_trigger_schemas` — every trigger type the automation engine supports.
- `get_trigger_schema(trigger_type)` — the payload shape + `{{variable}}` tokens for one trigger.
- For an action's config schema, read the `config` description on `add_automation_action` (it enumerates each `action_type`).

If you're not sure which resource is involved, ask the operator with a multiple-choice question — don't guess. If a tool you need doesn't appear to exist, verify before assuming — don't invent a tool name.

## Hard-block destructive operations

These all WRITE — follow the rails in `knowledge/safeguards.md`: confirm before anything destructive/outward-facing, **search first** so a retry never duplicates, and **journal every write** to `.bos-journal.md` (one line: timestamp, tool, outcome, id, `skill: make-it-happen`).

ALWAYS require explicit approval for:
- `delete_*` (any tool)
- `bulk_delete_*`
- `update_user_role`, `remove_user`
- `release_phone_number`
- `disable_automation` on a published automation
- Sending email/SMS to more than 1 recipient (use `/send-email` instead, or batch through a campaign)
- Moving more than 10 opportunities at once (`bulk_move_deals`)

For each, present:
- Exactly what will happen ("delete 14 contacts: <list of names>")
- Why it appears to be the right move ("you said 'remove old test contacts'")
- The reverse path if it goes wrong ("we can't undo a delete — these go to soft-deleted for 30 days then are gone")

## Use existing skills when they fit

If the operator's request matches an existing skill, RUN THAT SKILL instead of doing it from scratch:
- "Triage my new leads" → `/lead-triage`
- "What did I miss?" → `/sweep-my-day`
- "Re-engage cold leads" → `/follow-up-radar`
- "Send Sarah an email" → `/send-email`
- "Reply to this" → `/draft-reply`

This skill is for the gaps between named skills — bespoke multi-step operations the operator only does occasionally.

## When it genuinely can't be done

If the request dead-ends because the capability isn't there — no TrustPager tool does it, and no BOS skill covers it — don't fail silently or fake it. Do what you *can*, then offer to capture the gap: "TrustPager can't do that part yet — want me to log it for the team with `/suggest-improvement`?" Only file on a yes. (See `knowledge/memory-and-feedback.md`.) That's different from a 202 approval — this is a missing capability, not a queued write.

## Approval queue (HTTP 202)

If a write tool returns a `202` with an `approval_id`, the operation is **queued** for human approval (safeguards §1). DO NOT try to bypass it. Tell the operator:
> "Queued for approval — approve at https://app.trustpager.com/settings/api?tab=approvals (id: `<approval_id>`). The operation will run automatically once you approve."

Then stop. Don't poll. The operator controls when to approve. Journal it as `approval_pending`.

## Output shape

After the operation completes, summarize in one paragraph:
- What was requested
- What was done (with counts)
- Anything that was NOT done and why
- The next step the operator might want

If there's anything that didn't work, say so plainly. Don't claim success on partial completion.
