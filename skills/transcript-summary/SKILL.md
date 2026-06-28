---
name: Transcript Summary
description: Turn a recorded call or meeting into a usable write-up — a clean summary, the decisions, and the action list — from a transcript you paste or a local recording/transcript file. Reads the file the standard way (MarkItDown via tools/markitdown_convert.py), works on the text, and hands you something you can act on. Works day one with no accounts; once your CRM is connected I can also drop it straight onto the customer's record.
triggers:
  - transcript summary
  - summarise my last call
  - summarise that meeting
  - what did we agree on the call
  - turn the call into notes
  - write up the meeting
  - action items from the call
function_slot: comms
requires_driver: markitdown
requires_credential: none
data_path: local
status: active
---

# Transcript Summary

You recorded a call or meeting and want it turned into something useful: a short
summary, the decisions, and the action list, without re-listening to forty
minutes of audio. This skill takes the transcript you have on hand, reads it the
standard way, and produces a write-up you can act on. It runs day one with no
accounts connected.

## Step 1 — Get the transcript in front of you

There are two keyless ways in, and both stay on your own machine:

1. **You paste the transcript.** If you already have the text (a Notetaker
   export, a copied chat log, a voice-agent transcript you pasted in), work
   straight from it. Nothing to convert.
2. **You point at a local file.** A recording transcript saved as a `.txt`,
   `.docx`, `.pdf`, an exported meeting doc, or similar. Convert it to clean
   text first, the standard way:

   ```bash
   python tools/markitdown_convert.py "<path-to-file>"
   ```

   This handles PDF, Word, text, HTML, and more (the standard MarkItDown read
   path, same as `/extract-document`). If the wrapper reports the converter
   isn't installed, relay its one-line install hint (`pip install markitdown`)
   and stop until it's installed. If the file is an audio recording with no text
   track, say so plainly: there's no transcript to read, so the recording needs
   transcribing first before this skill can work on it.

If the converted file comes back empty, or the pasted text is just a few stray
lines with no real conversation in it, say so rather than inventing a call that
didn't happen.

## Step 2 — Read and write it up

Read the transcript end to end, then produce this, in your plain language (not
corporate meeting-minutes register):

```
## <Who the call was with>, <call type>, <date if known>

Summary: two or three sentences on what the call was about and where it landed.

Decisions
- the thing that got agreed

Action items
- [ ] <who>: <what> (by <when>, if a date was said)

Next step: the one concrete thing that moves this forward.

Notable lines (optional): one or two verbatim quotes if they capture a real point.
```

Pull only what is actually in the transcript. Do not invent decisions, and do
not add action items the parties did not agree to. If a date or owner wasn't
said, leave it open rather than guessing one.

## Step 3 — Hand it over and offer the connected upgrade

Give the write-up first. Then offer to put it where it's useful:

- **Save it as a file** you can keep or send. If they want a tidy document,
  draft it and offer to build one with `/build-document`.
- **Track the action items.** Lay the action list out clearly so it's easy to
  work through, and offer to turn it into a checklist.

Then, in plain language, offer the connected upgrade without naming any internal
machinery:

> This works right now on whatever transcript you hand me. Once your CRM is
> connected, I can also drop this write-up straight onto the customer's record
> and open the action items as tasks for you, so it's waiting there next time
> anyone opens the deal. No rush though, the write-up stands on its own today.

Keep that offer to plain words. The keyless write-up is the win; pushing it into
the CRM is the outcome you describe, not a thing you reach for here.

## Hard rules

- ❌ Only summarise what's in the transcript. No invented decisions, no action
  items nobody agreed to, no guessed owners or dates.
- ❌ Don't fabricate a summary for an empty file or a near-empty paste. "There's
  nothing in here to summarise" is a valid answer.
- ❌ Don't write bespoke per-format parsing. A file always goes through
  `tools/markitdown_convert.py`.
- ✅ Use the owner's own language, not boardroom minutes.
- ✅ Describe the connected upgrade in plain words only. Name no tools, scripts,
  or addresses for it.

## Output shape

The structured write-up first (summary, decisions, action items, next step),
then the offer to save it and, in plain language, the connected upgrade.
