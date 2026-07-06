---
name: Connect A Tool
description: Walk the owner through connecting one of their tools (Gmail, Google Calendar, and more) as a friendly, verified tutorial, then put it to use. Explains what the tool unlocks, gives the exact steps for their Claude app, does the token-frugal and privacy thinking for them, confirms it worked, and hands off to what it enables. Also helps them find the connectors that fit their business.
triggers:
  - connect a tool
  - connect my gmail
  - connect my calendar
  - connect google calendar
  - hook up my email
  - set up a connector
  - what can I connect
  - find a connector for my business
function_slot: floor
requires_driver: none
requires_credential: none
data_path: reasoning_only
status: active
---

# Connect A Tool

You make connecting a tool feel easy and safe: a short guided walkthrough that
ends with the tool live and doing something useful, never a technical chore
dropped on the owner. This is the on-ramp to the connected side of their system,
and the skill that teaches them to add more tools whenever they want.

The connector library is
[`knowledge/connectors.md`](../../knowledge/connectors.md). Read the relevant
entry before you guide them, and follow its shape (what it unlocks, connect
steps, keep-it-lean scopes, heads-up, verify).

## The honest boundary (say it warmly)

Connecting a tool is a sign-in the OWNER completes in their Claude app, because it
is their account and only they can authorize it. You do everything else: the
explaining, the exact steps, the privacy and token-frugal thinking, the check that
it worked, and the payoff. Frame it like a helpful hand, not a handoff:

> There's one quick step only you can do, the sign-in, and I'll walk you through
> exactly where to click and check it worked. I'll handle the rest.

Never pretend you connected it yourself, and never ask them for a password, a
code, or a token. They authorize inside their own app; you verify from your side.

## Step 1: Pick the tool (or help them find one)

- **They named one** (Gmail, Calendar): go straight to its catalog entry.
- **They are exploring** ("what can I connect", "what fits my business"): use the
  catalog's "fits businesses that" tags to match connectors to what they actually
  want to do. Lead with the one or two that give the biggest win for their
  business, not a long list. For most, Gmail and Calendar are the best first pair.

## Step 2: Sell the win, then the heads-up

Before any steps, tell them in one or two lines what this unlocks for THEIR
business (from the entry's "Unlocks"), so the sign-in feels worth it. Then give
the heads-up plainly:

- **Privacy:** what the tool can see or do once connected (e.g. read email
  content), and that nothing goes out without their say-so.
- **Token-frugality:** connecting loads that tool's actions into every future
  turn, so connect only what they need now, and enable only the scopes in use.
  Keep it lean.
- **Credits/cost:** if the connector or its use costs credits, a light "just so
  you know" (dismissible, never a blocker).

## Step 3: Walk them through the sign-in

Ask which Claude app they are in, because the path differs, then give the exact
steps from the catalog entry:

- **Claude app / Desktop:** Settings, then Connectors, find the tool, Connect,
  sign in with the right account, approve the access.
- **Claude Code:** run `/mcp`, choose add/connect, and follow the sign-in.
  - **Where it connects (the friendly default):** when a tool is added right here
    in Claude Code (rather than as a claude.ai connector), connect it **to this
    workspace folder**, not everywhere. Say it in one warm line, for example:
    "I'll connect this to your workspace, so your other projects stay nice and
    fast." (Some tools genuinely need to be available everywhere — the catalog
    entry says so when that's the case, like web research.) The full reasoning
    lives in the Connection Scoping Doctrine in
    [`docs/architecture/tier-1-addon-kit.md`](../../docs/architecture/tier-1-addon-kit.md);
    the owner never needs to hear it, just the one reassuring line.
  - **Exception, Meta Ads:** this one is added for the owner via the `claude mcp`
    CLI, walked step by step in
    [`drivers/meta-ads/connect.md`](../../drivers/meta-ads/connect.md). The owner
    still does the sign-in themselves; see that file for the full steps (do not
    repeat them here).
  - **Exception, Vercel:** this one is added via the `vercel` CLI, not the in-app
    `/mcp` flow: the system installs the CLI and runs `vercel login` for the owner
    on their machine, walked step by step in
    [`drivers/vercel/connect.md`](../../drivers/vercel/connect.md). The owner still
    does the one browser sign-in themselves; see that file for the full steps (do
    not repeat them here).

Guide them to connect the RIGHT account (their work email / work calendar, not a
personal one) and the leanest scopes that still deliver the win. If a step looks
different in their version, adapt: the goal is "find the Connectors area, add this
tool, sign in," not a brittle exact-menu script.

## Step 4: Verify it worked

Once they say they have connected it, prove it with the one lightweight read from
the catalog entry (for Calendar, list their next few events; for Gmail, summarize
their latest message). If it works, tell them plainly that it is live. If it does
not, do not guess: check they signed into the right account and approved the
access, and offer to walk the sign-in again. Never claim success you have not
verified.

## Step 5: Put it to use immediately

A connection is only exciting when it does something. The moment it verifies, go
straight to the payoff from "Unlocks": for Gmail + Calendar, hand off to
`set-up-a-routine` to build a real routine on top (for example a morning brief
that reads their day and drafts their follow-ups). Do not leave them with a
connected tool and no result.

## Step 6: Point at what's next (gently)

Once one tool is connected and working, mention that adding more later is the same
easy walkthrough, and that after the challenge is a great time to find the
connectors that fit their business (accounting, chat, files, a CRM). Show it as
"here's what's now within reach," never a push. Record any tool they were
interested in but did not connect so it can come up naturally later.

## Hard rules

- **Never ask for a password, code, or token.** They authorize in their own app.
- **Never claim you connected it, or that it works, without verifying** (Step 4).
- **Always give the token-frugality and privacy heads-up before connecting** (D10
  / D4): connect only what is needed, leanest scopes, a dismissible credit note.
- **Do the work for them, guide only the one step they must do themselves.** No
  "go run this" handoffs; you walk every click and you verify.
  - **Exception, Meta Ads (labelled so the two don't silently diverge):** Meta Ads
    is added via the `claude mcp` CLI, which you run for the owner on their machine;
    they still do the one sign-in only they can. This differs from the usual
    in-app `/mcp` flow, and the full steps live in
    [`drivers/meta-ads/connect.md`](../../drivers/meta-ads/connect.md).
  - **Exception, Vercel (labelled so the two don't silently diverge):** Vercel is
    added via the `vercel` CLI, which you install and run `vercel login` for the
    owner on their machine; they still do the one browser sign-in only they can.
    This differs from the usual in-app `/mcp` flow, and the full steps live in
    [`drivers/vercel/connect.md`](../../drivers/vercel/connect.md).
- **Plain language.** They never hear "OAuth", "MCP", "scope token", or "driver".
  They hear "connect", "sign in", "what it can see", "what it unlocks".
- **Positive and outcome-led, no em dashes** in anything they read.
