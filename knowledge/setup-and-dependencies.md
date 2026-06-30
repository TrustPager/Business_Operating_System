# Setup and dependencies (plain language)

This page is for you, the owner. No jargon. Here's the whole story in three lines:

1. **Almost everything is already built in.** When you first set up your system, it
   quietly installs the tools it needs to read and write documents (Word, Excel, PDF).
   You don't run anything.
2. **If it ever needs one more thing, it asks you first.** One plain question, one "yes."
   Then it sets it up itself and carries on. It will never hand you a command to run.
3. **There's a manual fallback you'll almost never need** (right at the bottom), in case
   you're ever offline or something odd happens.

That's it. You can stop reading here unless you're curious.

---

## What "a tool it needs" actually means

Your assistant can already think, plan, research, and write. A few jobs also need a small
helper on your computer. One example: turning your words into a real Word document you can
send, or reading a PDF a client emailed you. Those helpers are standard, free, and safe.
They run entirely on your machine. Nothing is uploaded, no account is needed.

When you first ran setup, your assistant installed the common ones for you. So most of the
time everything just works and you never think about this.

Setup also switches on **web research** so your assistant can look up a business from just
its name or website (handy the very first time it meets your business). It's free, needs no
account, and loads the next time you open Claude Code. If it's ever not available, your
assistant uses the built-in web search instead, so the "it already knew my business" moment
still lands.

## What happens if one is missing

Occasionally, usually on a brand-new computer, a specific helper isn't there yet. When
that happens you'll see something like:

> "To do this I need to add the document reader. It's a one-time, free setup on your
> machine and takes a few seconds. Want me to go ahead?"

You say **yes**, it installs it itself, checks it worked, and finishes the job. You say
**not now**, and it stops there with no harm done. **You are never asked to type a command.**
That is a promise: the system does the setup, you just give it the nod.

## The one-button health check

If anything ever feels off, you can ask your assistant to "check my setup" and it runs a
quick health check:

- It writes a tiny test Word file and Excel file, then reads them back. That proves the
  document tools work end to end.
- It tells you, in green and red, what's working and what (if anything) is missing.
- If something's missing, it can fix it for you on the spot (the same one-yes flow above).

Under the hood that's `python tools/check-install.py` (and `--fix` to install anything
missing). You don't need to remember that. Just ask your assistant to check your setup.

## The rare manual fallback

You should almost never need this. But if you're ever fully offline, or you'd simply rather
do it yourself, every document tool can be installed in one go from the project folder:

```
python -m pip install -r requirements.txt
```

That installs the whole document tool-kit at once. (Always `python -m pip`, not a bare
`pip`. On a computer with more than one Python that's what makes sure it lands in the
right place.) After that, "check my setup" should come back all green.

---

*Companion reading: `knowledge/document-tools-method.md` explains, for the assistant, exactly
how the read/write document tools work and how the "ask first, then do it" loop is wired.*
