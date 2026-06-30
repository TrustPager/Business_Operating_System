# Install Business Operating System

No accounts. No API keys. Real wins from minute one.

Total time: about 5 minutes. All you need is [Claude Code](https://claude.com/claude-code), `git`, and `python` (3.10 or later).

---

## The easy path: let Claude do it

Open Claude Code and say:

```
Go get the Business Operating System from TrustPager on GitHub.
```

Claude clones the public repo, installs the small document helper libraries (Word, Excel, PDF support), writes a signpost at `~/.claude/bos-run.py` so every skill can find its tools from any folder, and copies the skills and commands into `~/.claude/skills/` and `~/.claude/commands/` so Claude Code discovers them automatically. No key required. No account needed.

**The one thing Claude cannot do for you:** trigger a Claude Code restart. After the setup finishes, fully close and reopen Claude Code so the new skills load (they load at startup, not mid-session). Then type:

```
/start-here
```

You're running.

---

## Manual install (step by step)

Works identically on Mac, Windows, and Linux. You need `git` and `python` (3.10+) already installed.

### Step 1. Clone the repo

```
git clone https://github.com/TrustPager/Business_Operating_System
cd Business_Operating_System
```

### Step 2. Run setup

```
python tools/setup.py
```

Setup does four things automatically:

1. Installs the document libraries (Word, Excel, PDF read and write). One-time. Uses the same Python interpreter you ran it with, so there's no version mismatch on Windows.
2. Writes `~/.claude/bos.json` recording this clone's location.
3. Writes `~/.claude/bos-run.py`, the signpost that lets every skill call its tools from any working directory.
4. Copies the skills and commands into `~/.claude/skills/` and `~/.claude/commands/` so Claude Code discovers them without a plugin store or marketplace.

**At the key prompt, press Enter to skip.** The keyless floor installs completely. You can connect TrustPager later without re-running setup from scratch.

### Step 3. Verify

```
python tools/check-install.py
```

You'll see a `[OK]` / `[FAIL]` list. The keyless floor checks come first (document libraries, a real write-then-read round trip). The connected tier checks only run if you have a TrustPager key configured. "All checks passed" means you're ready.

If a document library is missing, run:

```
python tools/check-install.py --fix
```

It installs the missing pieces for you.

### Step 4. Restart, then start

Fully close and reopen Claude Code so the new skills load. Then:

```
/start-here
```

---

## Try it (keyless, right now)

No account needed. No key. Just type one of these after setup:

```
/start-here
```

Your assistant introduces itself, learns your business from a 60-second brain-dump, and hands you a first real win: a priced quote, a proposal draft, a competitor read. One short conversation and you're operating.

Or go straight to a specific win:

```
/price-my-work
```

Tell it the job, your costs, and the margin you want. It shows the price, the margin in dollars, and the rate you'd need to hit your target.

Run `/whats-possible` to see the full keyless capability list.

---

## Going deeper: connect TrustPager (optional)

TrustPager is a CRM, automation, and client portal platform built for service businesses. Connecting it switches on the always-on workflows: live pipeline briefings, follow-up radar, missed call recovery, nurture sequences, automations, reports, and more. It requires a TrustPager subscription.

**The primary connection path is the OAuth connector.** In Claude Code, say:

```
Connect my TrustPager workspace.
```

Claude walks you through the connector flow. Once connected, the TrustPager MCP server authenticates via OAuth and no key is needed.

**The API key path is an advanced alternative.** If you prefer a direct key (for scripting or a shared team setup), get one from your TrustPager workspace under Settings, then API, then Create new key. It starts with `tp_live_`. Re-run setup and paste it at the prompt:

```
python tools/setup.py --force
```

Once connected (either path), run:

```
/learn-my-business
```

This reads your live TrustPager workspace and writes a `CLAUDE.md` for your project: your real pipeline, products, and brand, with the gotchas for your line of work. Re-run it whenever your workspace changes. (If you already ran `/start-here`, it wrote a first profile from your brain-dump. This enriches it from live data.)

Prefer to do it by hand? Copy `templates/CLAUDE.md` into your project folder as `CLAUDE.md` and fill in the blanks. Industry-specific notes live in `knowledge/industry-notes.md`.

Sign up at [trustpager.com](https://trustpager.com).

---

## Updating

When new skills ship:

```
cd Business_Operating_System
git pull
python tools/setup.py
```

Setup is idempotent. It refreshes BOS-owned skills and commands in `~/.claude/`, updates the signpost if the clone moved, and prints a `[refresh]` line for each skill it updates. It never touches your TrustPager key or any skill you placed there yourself.

Run `python tools/check-install.py` afterward to confirm the floor is still green.

---

## Uninstall

Delete the cloned folder:

```
rm -rf ~/Business_Operating_System
```

To remove the skills and commands BOS copied into `~/.claude/`, delete the entries listed in `~/.claude/bos.json` under `installed_skills` and `installed_commands`. You can also delete `~/.claude/bos.json` and `~/.claude/bos-run.py`. None of this touches a TrustPager workspace. Your data stays where it is.

---

## Troubleshooting

**Skills don't appear after setup**
Restart Claude Code. Skills load at startup, not mid-session. If restarting doesn't help, check that `~/.claude/skills/` contains the BOS skill folders and `~/.claude/commands/` contains the command files. If they're missing, re-run `python tools/setup.py`.

**"A tool says a library is missing"**
Your assistant will offer to install it for you. Say yes and it runs `check-install.py --fix` on your behalf. Or run it yourself:

```
python tools/check-install.py --fix
```

**"The launcher is missing" or skills error with bos-run.py not found**
The signpost `~/.claude/bos-run.py` was not written or was deleted. Re-run:

```
python tools/setup.py
```

**Skills appear but TrustPager commands return "no key configured"**
You're using a connected-tier skill without a key. Either press Enter to skip (keyless skills will still work), or add your TrustPager key by running `python tools/setup.py --force`.

**TrustPager connection issues (connected tier)**
Confirm your subscription is active at [trustpager.com](https://trustpager.com). If using the OAuth connector, try reconnecting from [app.trustpager.com/auto/ai-access](https://app.trustpager.com/auto/ai-access). If using an API key, check it starts with `tp_live_` and regenerate if needed.

---

## Help

If something is not working:

1. Check [docs.trustpager.com](https://docs.trustpager.com). Most questions are answered there.
2. Email support and we'll get back to you the same day (Australian business hours).
