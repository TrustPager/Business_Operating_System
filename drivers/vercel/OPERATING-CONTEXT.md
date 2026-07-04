# Vercel operating context (loaded on connect)

> This file is loaded into an owner's `CLAUDE.md` profile only once they connect
> their Vercel account. It is the canonical source for how the assistant behaves
> when the Vercel connection is live. Until an account is connected, none of this
> applies. The assistant works from the owner's profile, their built site, and
> what they share. (`launch-my-site`'s Step 1 init is what folds this block into
> the profile, with its own no-clobber merge, and only when the connection has
> been verified with `vercel whoami`.)

## How the connection works

When Vercel is connected, you work inside the owner's own Vercel account, over
their own sign-in. Theirs, never anyone else's. It is a keyed local CLI: the
owner installs the `vercel` CLI and authorizes it once (a browser sign-in via
`vercel login`, or a token they create), and you shell that CLI via Bash. Reads
are free, so look around freely: `vercel whoami` to confirm who is signed in,
`vercel ls` to see their projects and past deployments. You deploy a preview
first, always, and ship to production only on the owner's explicit go. There is
no password or code for you to hold; the sign-in is the one step the owner does
themselves.

## What lives in the account (so you know what's possible when they ask)

- **Projects** are the deployable units: each built site the owner links is a
  Vercel project, with its own settings and deployment history.
- **Deployments** are every build Vercel has hosted, each on its own URL. A
  preview deployment is a private-ish URL for review; a production deployment is
  the one on the project's main URL.
- **Domains** are the addresses a project answers on, the default `*.vercel.app`
  URL and any custom domain the owner has added.
- **Past deployments and their URLs** are everything the account has shipped
  before, useful for rolling back to a known-good build or sharing an earlier
  preview.

## Things that change how you behave (deploy safety)

- **Preview first, always.** Every deploy starts as a preview (`vercel`), handed
  back for review on its own URL. You stop there until the owner has looked.
- **Production only on an explicit yes.** A production deploy (`vercel --prod`) is
  the single live switch, and it belongs to the owner. Never ship to production
  without their clear go, and never treat "looks good" on a preview as that go
  unless they say to make it live.
- **Report the real outcome.** Report exactly what the CLI returned, including
  failures. Never claim the site is live until `vercel` confirms the production
  URL back to you.
- **The URL comes from Vercel, not from you.** Read the deployed URL from the
  CLI's own output; never guess or construct it.
- **The owner owns going live.** Your job ends at a clean preview the owner has
  reviewed, then a production deploy they approved. You hand back the real URL
  Vercel gave you.

## Tools you lean on

Plain operating reference for the common moves when the connection is live:

- **`vercel whoami`** confirms the account is signed in; the first read before
  anything else.
- **`vercel ls`** lists the account's projects and recent deployments.
- **`vercel`** (no flag) deploys a PREVIEW and returns its URL; the default,
  review-first deploy.
- **`vercel --prod`** promotes to PRODUCTION and returns the live URL — the single
  explicit switch, run only on the owner's go.
