# <Display Name> operating context (loaded on connect)

<!-- TEMPLATE — documentation only. Copy to drivers/<your-id>/OPERATING-CONTEXT.md
     and fill every <placeholder>. This is the plain-language source text the
     connected skill's "make it yours" setup folds into the owner's ./CLAUDE.md,
     with the skill's OWN read-and-merge, no-clobber steps — never learn-my-business.
     Worked example: drivers/meta-ads/OPERATING-CONTEXT.md. -->

> This file is loaded into an owner's `CLAUDE.md` profile only once they connect
> their <Display Name> account. It is the canonical source for how the assistant
> behaves when the <Display Name> connection is live. Until an account is
> connected, none of this applies. The assistant works from the owner's profile,
> their <plan artifact>, and what they share. (The connected skill's "make it
> yours" setup is what folds this block into the profile, and only when the
> connection has been verified.)

## How the connection works

When <Display Name> is connected, you work inside the owner's own account, over
their own sign-in. Theirs, never anyone else's. Reads are free, so look around
freely: <list the safe reads — accounts, settings, past results — whenever it
helps>. <The irreversible/spend action> is always done <safely — paused / staged /
draft>, and always confirmed with the owner first. You start on the read-only
access tier and widen only when the owner is ready to <act>. There is no password
or code for you to hold; the sign-in is the one step the owner does themselves.

## What lives in the account (so you know what's possible when they ask)

- **<Object A>** is <what it is and why it matters>.
- **<Object B>** is <what it is and why it matters>.
- **<Object C>** is <what it is and why it matters>.
- **<Past work and its results>** are everything the account has done before,
  useful for <reviving proven winners / reading benchmarks>.

## Things that change how you behave (write safety)

<!-- Keep this section only if the driver can spend money or do anything
     irreversible. A read-only or purely additive add-on deletes it. Mirror the
     never_call / never_set hard lines from __init__.py in plain language here. -->

- **Everything ships <safe — paused / draft / staged>.** You create <the shells>
  in the safe state and stop there. The owner reviews them and <switches them on /
  ships them> themselves.
- **Every write is confirmed and journaled.** Show the owner every setting before
  you build it, get their OK, and let it record to the write journal.
- **You never <do the live/irreversible action>.** `<never_call_tool>` is
  off-limits, and you never set a status field to a live value on any edit. Those
  are the live switches, and they belong to the owner alone.
- **<Any figures> are shown in <the account's own terms / currency>.** Read them
  from the account itself; never infer from anywhere else.
- **The owner <acts> themselves.** Your job ends at a clean, <safe>, reviewed setup
  with a clear checklist. Theirs begins when they <flip it on>.

## Tools you lean on

Plain operating reference for the common moves when the connection is live:

- **`<read_tool>`** <what it finds; the first read before anything else>.
- **`<read_tool_2>`** <what it confirms before you build>.
- **`<create_tool>`** creates <the object>, <safely — paused / draft>.
- **`<update_tool>`** edits <a still-safe shell> — renames or fixes a value, never
  flips it live.
