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

Clone this repo to your home folder:

```
cd ~
git clone https://github.com/TrustPager/Business_Operating_System.git
```

Then run the installer for your operating system:

**Mac / Linux:**
```
cd Business_Operating_System
./scripts/install.sh
```

**Windows (PowerShell):**
```
cd Business_Operating_System
./scripts/install.ps1
```

The installer copies the skills, slash commands, and templates into Claude Code's settings directory.

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
Step 1 didn't complete. Re-run the installer and restart Claude Code.

**"Claude doesn't know about my products / pipeline / brand"**
You skipped Step 2. Drop one of the industry templates into your project folder as `CLAUDE.md` and Claude will pick it up next session.

---

## Updating

When new skills ship, pull the latest:

```
cd ~/Business_Operating_System
git pull
./scripts/install.sh   # (or install.ps1 on Windows)
```

---

## Uninstall

```
cd ~/Business_Operating_System
./scripts/uninstall.sh
```

(Removes the skills + commands from Claude Code. Doesn't touch your TrustPager workspace.)

---

## Help

If something's not working, the fastest path is:
1. Check [docs.trustpager.com](https://docs.trustpager.com) — most questions are answered there
2. Email support and we'll get back to you the same day (Australian business hours)
