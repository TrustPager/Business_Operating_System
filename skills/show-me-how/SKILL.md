---
name: show-me-how
description: Describe what you want to do in plain English, get a step-by-step walkthrough using TrustPager — links to the right pages, the exact tool calls, the gotchas.
triggers:
  - show me how
  - how do I
  - how do you
  - where do I
  - walk me through
  - I want to learn
  - teach me how
  - help me understand
  - tutorial for
function_slot: strategy
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - mcp__trustpager__search_help_center
  - mcp__trustpager__describe_resource
  - mcp__trustpager__describe_action_type
  - mcp__trustpager__create_service_request
status: active
---

# /show-me-how

Customers want to learn by doing, not by reading documentation. This skill turns "how do I X?" into a hands-on walkthrough — searches the TrustPager help center, summarizes the answer, links to the specific page in their workspace, and offers to drive the steps if they want.

## Step 1 — Pre-fetch + search the help center

First, run:

```
python ~/.claude/bos-run.py show-me-how --query "<the user's question>"
```

This pre-fetches the workspace's AI instructions (which sometimes contain workflow guidance that supersedes the generic answer) and any matching custom training canvases the customer's team has built (Learning Hub).

Then, in the same turn, call `mcp__trustpager__search_help_center` for the canonical published articles. This returns matching published tutorial articles. Always do BOTH — the platform team writes the canonical answer, the workspace may have its own overlay, and our job is to surface both.

If 0 results:
> "No published article on that exact topic. Let me figure it out from first principles — give me 30 seconds…"
> Then use `mcp__trustpager__describe_resource` and `mcp__trustpager__describe_action_type` to construct an answer.

If multiple results, pick the most relevant (best title match) and offer the rest as "related":
> "Closest article: '[title]'. Also possibly relevant: '[a]', '[b]'. Want me to walk through the closest, or one of the others?"

## Step 2 — Summarize, don't dump

Don't paste the whole article. Distill it to:
- **The steps** (numbered, ≤ 8 of them)
- **The URL to the actual workspace page** they need (e.g. `https://app.trustpager.com/settings/pipelines`)
- **One gotcha** they'll hit (the one footnote in the article that everyone misses)

Format example:
```
**How to add a new lead source**

1. Go to **Settings → CRM** ([link](https://app.trustpager.com/settings/crm)).
2. Scroll to the "Lead sources" section.
3. Click "+ Add source" and enter the name.
4. Save.

Heads up: the source name is case-sensitive in automations — if you have an automation that fires on "Facebook" leads, calling the new source "facebook" won't trigger it.

Want me to add it for you now? (Just say the source name.)
```

## Step 3 — Offer to drive

End with a single offer:
- For configuration tasks → "Want me to do this for you?" → if yes, execute via the appropriate `mcp__trustpager__*` tool.
- For navigation ("show me where my opps are") → just give the URL and explain what they'll see.
- For analysis tasks → "Want me to run `/audit-pipeline` (or relevant tool) to show you what's there now?"

NEVER drive without explicit yes. The offer is the offer — the user opts in.

## Important behaviours

- **One URL per answer.** If you mention "/settings/crm" twice, both must be live links to the same workspace path.
- **Workspace URLs only.** Not docs.trustpager.com URLs (those are for developers). Customer-facing links go to `app.trustpager.com/...`.
- **No code blocks.** This skill is for non-developers. Show steps as bulleted prose.
- **Acknowledge what you DON'T know.** If a question is outside TrustPager ("how do I export to QuickBooks?" but only Xero is integrated), say so plainly. Don't pretend.
- **Recency.** The help center is the source of truth — if your knowledge contradicts the help center, the help center wins.

## Edge cases

- **"How do I delete my account?"** → Don't answer with a how-to. Say "I can help you understand what's in your workspace first — want me to summarize that? If you still want to delete, reach the team directly." Deletion is a deliberate decision, not a CLI fact.
- **"Where do I find X?"** with an obvious answer → just give the URL + one line. No 8-step walkthrough for "where's my contacts list".
- **"How do I [feature that doesn't exist]?"** → "TrustPager doesn't have [feature X] yet — the closest thing is [Y]. Want me to file a feature request with the team?" Offer `mcp__trustpager__create_service_request`.

## Output shape

The final response IS the walkthrough — no separate summary line.
