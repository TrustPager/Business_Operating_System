# Install Business Operating System

Total time: about 10 minutes. No coding required.

---

## Before you start

You need:

1. **A TrustPager workspace.** Sign up at [trustpager.com](https://trustpager.com) — you'll get one free.
2. **TrustPager already connected to Claude.** If you're on Claude in the browser, connect TrustPager from the [TrustPager AI access page](https://app.trustpager.com/auto/ai-access). Once it's connected there, Claude Code picks it up automatically.
3. **Claude Code installed.** Get it from [claude.com/claude-code](https://claude.com/claude-code) (works on Mac, Windows, and Linux).
4. **Your TrustPager API key.** Find it under your workspace settings → API. It starts with `tp_live_`.

---

## Install in 2 steps

### Step 1 — Install the Business Operating System pack

You have two ways to get the skills + commands. **Either way you still run the
Python setup** in 1b, because that's what stores your API key for the tools.

**Option A — as a Claude Code plugin (recommended).** This registers every
command, skill, and subagent with Claude Code automatically. In Claude Code:

```
/plugin marketplace add TrustPager/Business_Operating_System
/plugin install business-operating-system@trustpager
```

Then clone the repo too (the Python tools and the installer live in it):

```
cd ~
git clone https://github.com/TrustPager/Business_Operating_System.git
```

**Option B — clone only.** Clone to your home folder and point Claude Code at
the directory (or run from inside it):

```
cd ~
git clone https://github.com/TrustPager/Business_Operating_System.git
```

#### 1b — Run setup (both options, same on Mac, Linux, and Windows)

```
cd Business_Operating_System
python tools/setup.py
python tools/check-install.py
```

`setup.py` writes your TrustPager API key to `~/.claude/bos.json`. If you've already connected TrustPager to Claude in the browser, it'll detect that key and offer to reuse it (no copy-paste needed).

`check-install.py` runs 7 quick health checks and prints a green / red list. If you see "All checks passed", you're ready.

### Step 2 — Pick your industry template (optional but recommended)

Open the `templates/industries/` folder and copy the one that fits your business into your project folder as `CLAUDE.md`. Options:

- **Mortgage / finance broker** — `templates/industries/mortgage-broker/CLAUDE.md`
- **Trades** — `templates/industries/trades/CLAUDE.md`
- **Insurance broker** — `templates/industries/insurance/CLAUDE.md`
- **Consultant / professional services** — `templates/industries/consultant/CLAUDE.md`
- **Allied health** — `templates/industries/allied-health/CLAUDE.md`
- **Manufacturing** — `templates/industries/manufacturing/CLAUDE.md`
- **None of the above** — use `templates/CLAUDE.md`

This file tells Claude the shape of your business so it doesn't have to ask every time.

---

## Try it

Restart Claude Code. Then type:

```
/sweep-my-day
```

You should see Claude pull up everything that needs your attention today — quotes overdue, hot leads, missed calls, follow-ups due. If you see that, you're done.

---

## Troubleshooting

**"trustpager mcp not found"**
The TrustPager connector isn't connected to Claude. Connect it at [app.trustpager.com/auto/ai-access](https://app.trustpager.com/auto/ai-access), then restart Claude Code.

**"Authorization: Bearer invalid"**
The API key didn't paste correctly. Generate a new one in your TrustPager workspace settings → API → Create new key.

**"command /sweep-my-day not found"**
Step 1 didn't complete. Make sure you ran `python tools/setup.py` from inside the `Business_Operating_System` folder and restart Claude Code.

**"Claude doesn't know about my products / pipeline / brand"**
You skipped Step 2. Drop one of the industry templates into your project folder as `CLAUDE.md` and Claude will pick it up next session.

---

## Updating

When new skills ship, pull the latest:

```
cd ~/Business_Operating_System
git pull
python tools/check-install.py
```

No re-install step needed — Claude Code reads the skills directly from this folder.

---

## Uninstall

To remove BOS, just delete the folder:

```
rm -rf ~/Business_Operating_System
```

Optionally clear the stored API key + cache:

```
python tools/config.py --clear-all
```

(Neither step touches your TrustPager workspace — your data is unaffected.)

---

## Help

If something's not working, the fastest path is:
1. Check [docs.trustpager.com](https://docs.trustpager.com) — most questions are answered there
2. Email support and we'll get back to you the same day (Australian business hours)
