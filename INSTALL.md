# Install Business Operating System

Total time: about 5 minutes. No coding required, and **no Python** — everything runs through Claude Code and your TrustPager MCP connection.

---

## Before you start

You need:

1. **A TrustPager workspace.** Sign up at [trustpager.com](https://trustpager.com) — you'll get one free.
2. **Claude Code installed.** Get it from [claude.com/claude-code](https://claude.com/claude-code) (works on Mac, Windows, and Linux).
3. **Your TrustPager API key.** Find it under your workspace settings → API. It starts with `tp_live_`.

---

## Install in 2 steps

### Step 1 — Connect TrustPager, then install the pack

**1a — Connect your TrustPager workspace to Claude Code.** This is what gives the skills their `trustpager` tools. Add the TrustPager MCP server to Claude Code — either with the `/mcp` command, or by adding it to your `.mcp.json`:

```json
{
  "mcpServers": {
    "trustpager": {
      "type": "http",
      "url": "https://mcp.trustpager.com/<your-workspace-slug>/mcp",
      "headers": { "Authorization": "Bearer tp_live_..." }
    }
  }
}
```

Replace `<your-workspace-slug>` and the `tp_live_...` key with yours. The exact connection details for your setup are at [docs.trustpager.com](https://docs.trustpager.com). The server **must** be named `trustpager` — the skills look for it by that name.

> The MCP connection holds your API key. There's nothing else to store — no key file, no setup script.

**1b — Install the Business Operating System pack.** This registers every command, skill, and subagent. In Claude Code:

```
/plugin marketplace add TrustPager/Business_Operating_System
/plugin install business-operating-system@trustpager
```

(Prefer to clone? `git clone https://github.com/TrustPager/Business_Operating_System.git` into your home folder and point Claude Code at it. Either way there's no build step.)

### Step 2 — Teach Claude your business (run `/learn-my-business`)

**Restart Claude Code** so the new commands and MCP connection load, then type:

```
/learn-my-business
```

It reads your live TrustPager workspace and writes a `CLAUDE.md` into your project folder for you — your real pipeline, products, and brand — and folds in the gotchas for your line of work. That file tells Claude the shape of your business so it doesn't have to ask every time. Re-run it whenever your pipeline, products, or brand change.

It also creates a local memory store (`.bos-memory/` in your project folder) that loads automatically each session. As you work, tell Claude to remember things with `/remember` — preferences, how you like things done, context the CRM doesn't hold — and it carries them forward. (If your project folder is a git repo, you may want to add `.bos-memory/` and `.bos-journal.md` to `.gitignore` — they're your private working notes and change log.)

**Prefer to do it by hand?** Copy `templates/CLAUDE.md` into your project folder as `CLAUDE.md` and fill in the `<<< ... >>>` blanks. Industry-specific gotchas live in `knowledge/industry-notes.md` (one section per vertical: mortgage/finance, trades, insurance, consulting, allied health, manufacturing).

---

## Try it

With your `CLAUDE.md` written (Step 2), type:

```
/sweep-my-day
```

You should see Claude pull up everything that needs your attention today — quotes overdue, hot leads, missed calls, follow-ups due. If you see that, you're done.

---

## Troubleshooting

**"trustpager mcp not found" / the skills can't reach your data**
The `trustpager` MCP server isn't connected. Run `/mcp` in Claude Code to check it's listed and connected, re-check the URL + key in your `.mcp.json` (Step 1a), then restart Claude Code.

**"Authorization: Bearer invalid"**
The API key is wrong or expired. Generate a new one in your TrustPager workspace settings → API → Create new key, and update it in your MCP connection.

**"command /sweep-my-day not found"**
The pack didn't install, or Claude Code needs a restart. Re-run the `/plugin install` step (Step 1b) and restart.

**"Claude doesn't know about my products / pipeline / brand"**
You skipped Step 2. Run `/learn-my-business` and it'll write your `CLAUDE.md` from your live workspace (or copy `templates/CLAUDE.md` in by hand). Claude picks it up next session.

---

## Updating

When new skills ship, update the plugin:

```
/plugin update business-operating-system@trustpager
```

(Cloned instead? `cd ~/Business_Operating_System && git pull`.) There's no build step and nothing to re-run — the skills are Markdown that Claude reads directly, and your MCP connection and `CLAUDE.md` are untouched.

---

## Uninstall

```
/plugin uninstall business-operating-system@trustpager
```

(Or delete the cloned folder.) Optionally remove the `trustpager` entry from your `.mcp.json` to disconnect the workspace.

Your memory store and change log live in your project folder, not in the pack — if you want to wipe them too, delete `.bos-memory/` and `.bos-journal.md` from that folder.

(None of these steps touch your TrustPager workspace — your data is unaffected.)

---

## Help

If something's not working, the fastest path is:
1. Check [docs.trustpager.com](https://docs.trustpager.com) — most questions are answered there
2. Email support and we'll get back to you the same day (Australian business hours)
