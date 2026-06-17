---
name: Suggest Improvement
description: Log something the operator wanted that doesn't exist yet — a missing BOS skill/command, or a TrustPager platform capability that isn't there — into TrustPager's developer feedback queue via a service request, so the team can build it. Use when the operator says "I wish it could…", "this is missing", "feature request", "report a bug", or whenever a task dead-ends because the capability genuinely isn't there.
triggers:
  - suggest an improvement
  - feature request
  - I wish it could
  - this is missing
  - report a bug
  - log this for the team
  - request a feature
  - that should be possible
---

# Suggest Improvement

The full model — what's worth logging and how the feedback loop fits with memory — is in `knowledge/memory-and-feedback.md`. Read it if you haven't this session.

This is how a single operator's "I wish it could…" becomes a shipped feature. The channel already exists: **`create_service_request`** writes to TrustPager's developer feedback queue, it's on every workspace, and it's free.

## Step 1 — Classify the gap

- **`[BOS]` — plugin gap:** they asked for something and no BOS skill/command covers it.
- **`[Platform]` — platform gap:** TrustPager itself can't do it.

If it's neither — you can actually do it with existing tools, it's a one-off they can do another way right now, or it's user error — **don't log it.** Help them in the moment instead. Capture *missing capability*, not friction you can already solve.

## Step 2 — Check for a duplicate

Search the existing queue first (`list_service_requests`, or `search`) for the same gap. If one already exists, **add a note to it** (`add_service_request_note`) — "+1, another operator hit this doing X" — rather than filing a duplicate. A second voice on an existing request is more useful than a near-twin.

## Step 3 — Draft it, show it, confirm

`create_service_request` is a write, so it follows the standing rail: **draft → show → confirm → file.** Compose:

- **`use_case`** — what the operator was trying to do, in their own words. The most important field; it's the "why". Prefix it with `[BOS]` or `[Platform]`.
- **`suggested_solution`** — your one-line take on what would solve it.
- **`affected_tools`** — the skill/command or TrustPager area involved.
- **`category`** — a short label. If unsure what the tool accepts, inspect it (`get_ai_instructions` / the tool schema) rather than guessing.

Show the operator the draft and get a yes before filing.

## Step 4 — File it and surface the id

- If it returns **`202` (queued for approval)** — that's the approval queue, not a failure. Tell the operator to approve it at `app.trustpager.com/settings/api?tab=approvals` and **stop** (see `safeguards.md`). Don't retry.
- Otherwise surface the request **id**: *"Logged as request #1234 — the TrustPager team triages these. I'll keep using what we've got in the meantime."*

Then carry on helping with whatever the operator can do today.

## Proactive use (don't wait to be asked)

When a catch-all skill (`/make-it-happen`, `/show-me-how`) dead-ends because the capability genuinely isn't there, don't fail silently. Finish helping as far as you can, then offer: *"TrustPager can't do that yet — want me to log it so the team can build it?"* Only file on a yes.

## Hard rules

- ❌ Don't log friction you can solve right now, one-offs with a workaround, or user error — only missing capability.
- ❌ Don't file a duplicate — search first; +1 an existing request instead.
- ❌ Don't retry a `202` — it's queued for a human; surface it and stop.
- ✅ Always draft → confirm before filing (it's a write to their workspace).
- ✅ Tag `[BOS]` vs `[Platform]` so triage can route it, and surface the request id.

## Output shape

A one-line confirmation with the request id (or the approval-queue hand-off), then back to helping. If you +1'd an existing request, say which one.
