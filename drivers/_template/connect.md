# Connect <Display Name> (<plain parenthetical>)

<!-- TEMPLATE — documentation only. Copy this file to drivers/<your-id>/connect.md,
     fill every <placeholder>, and keep this as the single home for the connect
     steps. No other surface restates them; the connectors.md card and the spec
     only point here. Worked example: drivers/meta-ads/connect.md. -->

## What this unlocks
Once connected, I can <the win, in the owner's own terms — what I can now do for
them against their live account>, built to your plan, created safe and ready for
you to review. Reads are free; I never <spend / deploy / do the irreversible
thing> without showing you first.

## The honest boundary
There's one sign-in only you can do (it's your account). I do everything else: the
exact steps, the safety thinking, the check that it worked, and the setup. I'll
never ask for a password or a code. This loads the <tool> tools, but Claude Code
keeps them out of the way until I actually use one, so it won't slow your other
work.

<!-- If the connect mechanism differs from the usual in-app /mcp (Connectors)
     flow, name it as a LABELLED exception here and in skills/connect-a-tool, so
     the two never silently diverge. Delete this note if the default flow applies. -->
(For the builder: this connector is added via <the add mechanism, e.g. the
`claude mcp` CLI>, which is a deliberate, labelled exception to connect-a-tool's
usual "/mcp in the app" flow. The owner still performs the sign-in themselves; BOS
only runs the add/login commands.)

## Step 1: I add the connection for you (permission first)
"To set up your <capability> I need to add the <Display Name> connection. It's a
one-time, free sign-in with your <account> account. Want me to get it ready?"
On yes, I run (on your machine, from your workspace folder, so I do it, not you):

    <the add command, e.g. claude mcp add --transport http --scope local <id> <server_url>>

I connect it to this workspace, so your other projects stay nice and fast.

<!-- Scope is LOCAL (this-folder) by default — the CLI default, kept explicit so
     it's self-documenting — run from the owner's BOS workspace folder. Local
     scope is private to the owner (~/.claude.json), never a git-tracked file.
     That rule is owned by the Connection Scoping Doctrine in
     docs/architecture/tier-1-addon-kit.md (the keyless firecrawl server is the
     one labelled user-scope exception). Follow it here; don't restate it. -->

## Step 2: You sign in (the one step that's yours)
I run:

    <the login command, e.g. claude mcp login <id>>

This opens <the provider>'s sign-in in your browser. Sign in with the account that
manages your <capability> and approve the access.
- Grant the read-only access first. We start read-only so nothing can <spend /
  deploy> by accident; we widen it only when you're ready to actually <act>.
- <Any known fallback, e.g. if the browser sign-in seems to hang, I re-add it on a
  fixed port and we try again — keep or delete per your provider.>

## Step 3: Restart so it loads
The connection only wakes up when Claude Code starts fresh. So: close and reopen
Claude Code once. (Before the restart it won't show in /mcp yet. That's expected,
not a problem.)

## Step 4: I verify it worked
Back after the restart, I do one small read to prove it's live: I <the one
lightweight read, e.g. list your accounts>. If I can see them, you're connected. If
not, we check you signed into the right account and try the sign-in once more.

## Step 5: Make it yours, then put it to use
The moment it verifies, I run the quick "make it yours" setup (I read your brand
and business, take a look at your account, and ask a couple of <capability>
questions), then we're ready to <put the connected skill to work on your plan,
safely, for your review>.
