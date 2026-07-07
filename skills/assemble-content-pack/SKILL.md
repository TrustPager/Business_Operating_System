---
name: Assemble Content Pack
description: Gather the pieces of one finished social post (the brief, the caption, the rendered graphic) into a single clean, named, ready-to-publish folder with a short readme of what's inside. No generation, no network: it just collects, names, and labels what you already have. Pairs with write-post-copy (the words) and make-social-post (the picture).
triggers:
  - assemble the content pack
  - put this post together
  - collate the post pieces
  - bundle this social post
  - gather the caption and graphic
  - package this post for publishing
  - make a publish-ready folder for this post
  - put the caption and image in one place
  - build the content pack
function_slot: social
requires_driver: none
requires_credential: none
data_path: local
status: active
---

# Assemble Content Pack

This is the tidy-up step that comes after the words and the picture exist. The
caption was written (that's `write-post-copy`), the graphic was rendered (that's
`make-social-post`), and the idea came from a brief or a planned row (often
`plan-my-content`). This collates those three into ONE clean, clearly named
folder with a short readme, so when it's time to publish, the whole post sits in
one place instead of scattered across downloads and chat scrollback.

It collects; it does not create. No new caption, no new graphic, no network
call. Everything that goes in the pack already exists. One pack per run.

## Step 1 — Find the three pieces

Confirm what you're packing. A complete pack has three parts, and you only ever
collate what's already been made:

| Piece | Where it usually comes from |
|---|---|
| The brief / idea | a planned row from `plan-my-content`, or a one-line brief the owner gave you |
| The caption / post copy | already drafted by `write-post-copy` (paste, or a saved `.md`/`.txt`) |
| The rendered graphic | already rendered by `make-social-post` (the PNG, usually in `studio/social/output/`) |

Ask for whatever you don't already have in front of you: the path to the
rendered image, the caption text (or its file), and the brief. If a piece is
genuinely missing, say which one and point at the app that makes it, rather than
inventing it here:

- No caption yet? That's `write-post-copy`.
- No graphic yet? That's `make-social-post`.
- No brief or idea at all? That's `plan-my-content`, or just one line from the owner.

Don't generate the missing piece inside this app. Collating is not writing.

## Step 2 — Name the pack

Pick one clear, human folder name for this post so the owner can find it later.
Build it from the platform and the idea, kept short and tidy, for example
`instagram-same-day-quotes` or `linkedin-one-place-launch`. Confirm the name
with the owner if it isn't obvious from the brief. The folder lands wherever the
owner keeps their content (default to a `content-packs/<pack-name>/` folder in
the working directory, and say where you put it).

## Step 3 — Collate the files into the folder

Make the folder, then copy each piece in under a clear, predictable name. Copy,
never move: the originals stay where they are.

```bash
mkdir -p "content-packs/<pack-name>"
cp "<path-to-rendered-graphic>" "content-packs/<pack-name>/graphic.png"
cp "<path-to-caption-file>"     "content-packs/<pack-name>/caption.txt"   # if the caption is a file
```

If the caption was pasted as text rather than handed over as a file, write it
straight into `caption.txt` exactly as the owner approved it, word for word. Do
not reword, trim, or "improve" it here: this step preserves the approved copy,
it does not edit it. Same for the brief: drop the planned idea or the one-line
brief into `brief.txt` (or `brief.md`) as-is.

A finished pack folder looks like this:

```
content-packs/instagram-same-day-quotes/
  README.md       — what's in the pack, the platform, and how to publish it
  caption.txt     — the approved post copy, ready to paste
  graphic.png     — the rendered image, ready to upload
  brief.txt       — the idea this post fills (for context)
```

## Step 4 — Write the readme

Write a short `README.md` inside the folder that says, in plain language, what
the pack is and how to use it. Keep it to the essentials so a person glancing at
it months later knows exactly what they're holding:

```markdown
# Instagram post: same-day quotes

**Platform:** Instagram (Square)
**Status:** ready to publish

## What's in here
- `graphic.png`: the image to upload
- `caption.txt`: the words to paste (already in your voice, approved)
- `brief.txt`: the idea this post came from, for context

## How to publish
1. Upload `graphic.png` as the image.
2. Paste the text from `caption.txt` as the caption.
3. Post it.

Assembled on <date>. The caption and graphic are exactly as approved, so give
them one last read before posting.
```

Match the readme's facts to the actual pieces in the pack: name the real
platform, list only the files that are actually there, and if a piece was left
out (say there's no separate brief), just leave that line off rather than
referencing a file that isn't there.

## Step 5 — Hand it over

Show the owner the finished pack: where it lives, what's in it, and the one
remaining human step (a last read before it goes out).

```
✓ Packed "instagram-same-day-quotes": caption, graphic, and the brief, all in one folder:
  content-packs/instagram-same-day-quotes/
  Open it, give the caption and image one last look, and it's ready to post.
```

This pack is ready for the owner to publish by hand: upload the graphic, paste
the caption, post. Once your CRM is connected, I can also file a pack like this
straight into your workspace's images and content area for you, so it's stored
with everything else and ready to schedule, instead of living only on your
desktop. That's the upgrade; the folder on its own is the win today, and it
ships with zero accounts connected.

## Hard rules

- **Collate only, never create.** No new caption, no new graphic, no rewritten
  copy. Every piece in the pack already exists and goes in exactly as approved.
  If a piece is missing, name the app that makes it (`write-post-copy`,
  `make-social-post`, `plan-my-content`) — don't fabricate it here.
- **Keyless and local.** This runs with zero accounts connected. It reads files
  the owner already has and writes a folder on disk. No network, no lookups.
- **Copy, don't move.** The originals stay put; the pack holds copies, so
  nothing the owner already has gets disturbed.
- **Preserve the approved copy word for word.** The caption goes in exactly as
  the owner signed off on it. This step does not edit, trim, or re-voice it.
- **Clear, plain hand-off.** The readme and the hand-off say what's in the pack
  and how to use it, in plain language. This is operator-facing status text:
  keep it factual and easy to scan.
- **One pack per run.** One post, one folder. A batch of posts is a series of
  runs, not one giant folder.
- **Don't publish.** Assembling is not posting. The pack is ready for the owner
  to publish by hand; sending it anywhere is a separate, deliberate step.

## Output shape

A short confirmation naming the pack folder, where it lives, and what's inside
(caption, graphic, brief), then the one human step left: a last read before it
goes out. The deliverable is the clean, named, publish-ready folder itself.
