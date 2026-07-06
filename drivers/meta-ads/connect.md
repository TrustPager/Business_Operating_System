# Connect Meta Ads (Facebook & Instagram ads)

## What this unlocks
Once connected, I can set up your Facebook and Instagram ad campaigns for you,
built to your plan, created paused and safe, ready for you to review and switch
on yourself. Reads are free; I never spend a cent without showing you first.

## The honest boundary
There's one sign-in only you can do (it's your ad account). I do everything
else: the exact steps, the safety thinking, the check that it worked, and the
setup. I'll never ask for a password or a code. This loads the ad tools, but
Claude Code keeps them out of the way until I actually use one, so it won't slow
your other work.

(For the builder: this connector is added via the `claude mcp` CLI, which is a
deliberate, labelled exception to connect-a-tool's usual "/mcp in the app" flow.
The owner still performs the sign-in themselves; BOS only runs the add/login
commands. See spec §3d. The registration is **project scope, run from the
owner's BOS workspace folder** — that choice is owned by the Connection Scoping
Doctrine in
[docs/architecture/tier-1-addon-kit.md](../../docs/architecture/tier-1-addon-kit.md);
this file follows it, never restates it.)

## Step 1: I add the connection for you (permission first)
"To set up your ads I need to add the Meta Ads connection. It's a one-time,
free sign-in with your Facebook account. Want me to get it ready?"
On yes, I run (on your machine, from your workspace folder, so I do it, not you):

    claude mcp add --transport http --scope project meta-ads https://mcp.facebook.com/ads

I connect it to this workspace, so your other projects stay nice and fast.

## Step 2: You sign in (the one step that's yours)
I run:

    claude mcp login meta-ads

This opens Meta's sign-in in your browser. Sign in with the Facebook account
that manages your ads and approve the access.
- Grant the read-only access first. We start read-only so nothing can spend by
  accident; we widen it only when you're ready to actually launch.
- If the browser sign-in seems to hang (the little local page never returns), no
  problem, I re-add it on a fixed port and we try again:

      claude mcp add --transport http --scope project meta-ads https://mcp.facebook.com/ads --callback-port 8080

## Step 3: Restart so it loads
The connection only wakes up when Claude Code starts fresh. So: close and reopen
Claude Code once. (Before the restart it won't show in /mcp yet. That's
expected, not a problem.)

## Step 4: I verify it worked
Back after the restart, I do one small read to prove it's live: I list your ad
accounts. If I can see them, you're connected. If not, we check you signed into
the right Facebook account and try the sign-in once more.

## Step 5: Make it yours, then put it to use
The moment it verifies, I run the quick "make it yours" setup (I read your brand
and business, take a look at your account, and ask a couple of ads questions),
then we're ready to launch your plan, created paused, for your review.
