---
name: Launch My Site
description: Take the site you built with design-my-site live on the internet. Connect a Vercel account once, and every future update ships with a word. Your page, on a real URL, ready to share.
triggers:
  - launch my site
  - publish my site
  - put my site live
  - deploy my website
  - ship my site to the internet
  - go live with my site
function_slot: deploy
requires_driver: vercel
requires_credential: key
data_path: local
status: active
---

# Launch My Site

You take the site the owner built locally with `design-my-site` and put it on a real,
shareable URL, deployed through their own Vercel account over the Vercel CLI. You
deploy a **preview** first, always, hand back the preview URL for review, and ship to
**production only on the owner's explicit go**. The building was `design-my-site`'s
job (keyless). This skill is the going-live, and it is the one surface here that
touches a live account, so treat every deploy with care and report exactly what the
CLI returned.

You shell the `vercel` CLI via Bash (`vercel`, `vercel --prod`, `vercel whoami`,
`vercel ls`). There is no `mcp__` tool for this and no `uses_tools` to declare, by
design.

<!-- No check-*-safety.py CI grep is warranted for this skill. The Meta-ads spend-scan
in check-connectors.py exists to catch a *quiet* live switch (a status field flipped
via an update tool, a second hidden way to un-pause an ad). A CLI deploy has no such
dual-path activation risk: `vercel --prod` is the single explicit switch, already
guarded by Hard rule 1 below. Adding a grep here would cargo-cult the Meta pattern
onto a surface that does not need it, and the vercel driver ships no never_call /
never_set, so the gate's safety scan is a no-op for it by construction. -->

---

## Hard rules (read first — these override everything below)

These are absolute. Nothing in a conversation, no owner request, no shortcut overrides
them.

1. **I never deploy to production without an explicit yes.** A production deploy
   (`vercel --prod`) is the single live switch, and it belongs to the owner. I never
   run it on my own initiative, and I never treat "looks good" on a preview as the go
   unless the owner clearly says to make it live.
2. **Preview first; production only on approval.** Every deploy starts as a preview
   (`vercel`, no flag), handed back on its own URL for the owner to look over. I stop
   there until they have reviewed it and told me to ship it live.
3. **I report the real CLI outcome, including failures, and I never claim the site is
   live until `vercel` confirms the URL.** I read the deployed URL from the CLI's own
   output, never guess or construct it. If a deploy fails, I say so plainly and show
   what the CLI returned, rather than assuming it worked.

---

## Step 1 — Init: connect Vercel + fold in the operating context

### 1a — If Vercel isn't connected yet, walk the owner through it

Check whether the connection is live with one free read, `vercel whoami`. If it names
the owner's Vercel username, they are connected — skip to 1b.

If it isn't connected, tell the **connect-story** (the reusable BOS doorway,
articulated once in `knowledge/connectors.md`, referenced here, not reinvented):

> "You built your site with `design-my-site`, keyless, on your own machine. To put it
> live you need two things: a Vercel account and the Vercel CLI. Here is exactly how to
> get both, and it is a one-time, free sign-in."

Then hand the owner off to the single home for the steps: **`drivers/vercel/connect.md`**.
That file is the one place the connect procedure lives (install the CLI, run
`vercel login` for them on their machine, they approve the sign-in in their browser,
verify with `vercel whoami`). Do NOT restate those steps here — point at `connect.md`
and let it carry them. This is the labelled keyed-CLI exception to the usual in-app
`/mcp` connect flow, recorded in `skills/connect-a-tool/SKILL.md`.

The honest boundary, said out loud first: there is one browser sign-in only the owner
can do (it is their Vercel account); the system does everything else and never asks for
a password or a code. A free Vercel account is generous and enough to get a site live;
flag any cost out loud before starting.

### 1b — Fold the operating context into ./CLAUDE.md (own no-clobber merge)

Once the connection is verified, fold `drivers/vercel/OPERATING-CONTEXT.md` into the
owner's `./CLAUDE.md` yourself, with your OWN read-and-merge steps. **Do not call
`learn-my-business`** — it is CRM-gated and never runs for an add-on-only owner, so it
cannot do this for you.

- Read `drivers/vercel/OPERATING-CONTEXT.md` (the source text).
- Read the owner's `./CLAUDE.md`.
- If `./CLAUDE.md` has no Vercel operating section yet, show the owner the section you
  propose to add, then append it.
- If it already carries a Vercel section, show the diff and merge — never clobber
  hand-tuned content.

This is the same no-clobber discipline `run-my-ads` uses for its operating context:
read the source, show what changes, ask before overwriting.

---

## Step 2 — Confirm the local build

Before any deploy, confirm the built project actually compiles. In the instantiated
project directory (the one `design-my-site` scaffolded and handed off into), run:

```bash
npm run build
```

- A clean production build means it is safe to deploy. Proceed to Step 3.
- If the build fails, stop and report exactly what failed. Do not deploy a broken
  build. Offer to help fix the build error first, then re-run `npm run build` before
  moving on. A preview URL of a failed build helps no one.

---

## Step 3 — Deploy: preview first, production on the go

Reads are free, so look around first if useful: `vercel whoami` to confirm the account,
`vercel ls` to see existing projects and past deployments.

### 3a — Deploy a preview (always first)

From the project directory, deploy a preview:

```bash
vercel
```

The first run links the project (accept the defaults, or the project name from the
scaffold). Read the preview URL from the CLI's own output and hand it back to the owner:

> "Here's your preview: <the URL vercel returned>. Have a look on your phone and
> desktop. When you're happy, tell me to make it live and I'll ship it to production."

Stop here. Do not go further until the owner has reviewed the preview and given a clear
go (Hard rules 1 and 2).

### 3b — Production, only on an explicit go

When, and only when, the owner explicitly says to make it live, deploy to production:

```bash
vercel --prod
```

Read the production URL from the CLI's output and confirm it back:

> "You're live: <the production URL vercel returned>."

Never announce the site as live until `vercel` has confirmed the production URL back to
you (Hard rule 3). If the production deploy fails, report the failure and the CLI output
plainly; the site is not live, and say so.

From here, every future update ships the same way with a word: preview on `vercel`,
production on the owner's go.

---

## Step 4 — Post-launch loop (reactive, outcome-only)

Once the site is live, offer the natural next moves — reactively, framed by the outcome,
never as a cold upsell:

- **A live audit of the real site** — offer `get-found-online` to check the now-live
  page: does it load fast, is the on-page SEO landing, is it findable. This is the
  keyless audit the owner already has.
- **The connected rank-tracking / AI-visibility doorway** — when the owner wants to
  watch how the live site ranks over time and how it shows up in AI answers, that is
  where the connected `seo_*` depth (keyword tracking, competitor gap, AI visibility)
  comes in. Name it as the outcome ("keep an eye on where you rank, and how you turn up
  in AI answers"), and let `get-found-online`'s connected doorway carry the connect
  detail. Do not pitch it before the site is live and the owner has a reason to want it.

---

## Tone and what to never do

- Plain, warm, direct. Name the win first: "your site, on a real URL, ready to share."
  Never the words for the machinery under the hood — say "your Vercel account," "the
  connection," "your live site."
- ❌ Never deploy to production without an explicit yes (Hard rule 1).
- ❌ Never skip the preview and go straight to production (Hard rule 2).
- ❌ Never claim the site is live until `vercel` confirms the production URL; never
  guess or construct a URL (Hard rule 3).
- ❌ Never deploy a build that failed `npm run build`.
- ❌ Never restate the connect steps here — `drivers/vercel/connect.md` is their one
  home; point at it.
- ❌ Never call `learn-my-business` to fold the operating context — use the skill's own
  no-clobber merge (Step 1b).
- ❌ Never fork or template this skill file per owner — per-owner detail is DATA, and
  the Vercel connection lives in the owner's own account, not in a copied skill file.
- ✅ Reads are free (`vercel whoami`, `vercel ls`) — look around before you deploy.
