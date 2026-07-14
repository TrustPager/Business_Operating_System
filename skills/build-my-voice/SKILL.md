---
name: Build My Voice
description: Lock in how YOU sound so every content app writes as you, forever. Reads a file of your real emails, posts, and messages, then runs a short "this, not that" session and writes it to the voice files the rest of your system already loads. Builds both your company voice and your personal voice, same process for each. Keyless, works from your own words.
triggers:
  - build my voice
  - lock in my voice
  - capture how I write
  - make it sound like me
  - teach it my voice
  - my personal voice
  - my brand voice
  - write like me
function_slot: strategy
requires_driver: markitdown
requires_credential: none
data_path: local
status: active
produces_customer_facing_copy: true
---

# Build My Voice

You are capturing how the owner actually sounds and locking it in so every
content app in their system writes as them, without being asked again. This is
the operator's signature: once it's set, `write-post-copy`, `plan-my-content`,
`build-social-strategy`, `write-a-proposal`, `draft-reply`, and `write-a-letter`
all read it and produce work in the owner's real voice.

**This is the owner's OWN voice, not the customer's.** It is the mirror image of
`build-customer-voice` (which captures the words *customers* use). Do not confuse
them: this skill is about how the *business* and the *owner* speak.

## Two voices, one process

You build up to two voices, using the same three steps for each:

| Voice | What it is | Where it's written | Who loads it |
|---|---|---|---|
| **Company voice** | How the business speaks: posts, captions, proposals, emails that go out under the brand | `marketing-strategy/<BrandName>/voice.md` | every content app already reads this file |
| **Personal voice** | How the owner writes as themselves: their own LinkedIn/founder posts, personal notes | `marketing-strategy/<BrandName>/personal-voice.md` | content apps when the owner writes as themselves |

Start with the company voice (it unlocks the most). Offer the personal voice
after, as a second pass. Building only one is a perfectly good outcome; never
force both in one sitting.

**Relationship to `build-brand-strategy`:** that skill *infers* a light
`voice.md` from a brain-dump. This skill is the deep, evidence-grounded version,
built from the owner's real writing plus a conscious lock-in. It produces the
**same `voice.md` file in the same shape**, so everything downstream keeps
working. If a `voice.md` already exists, you are deepening it: read it first, and
show what changed before you overwrite (see Step 3).

The method reference for tone and register is
[`knowledge/communication-voice.md`](../../knowledge/communication-voice.md),
read it if you haven't.

---

## Step 1: Read the owner's real writing

Voice is captured from real words the owner already wrote, never invented for
them. Ask for the richest evidence they can hand you, in this order:

1. **A file or folder they point you at**, a batch of sent emails, exported
   posts, a doc of past captions, saved messages, anything they have written.
   Convert each to clean text first:

   ```bash
   python ~/.claude/bos-run.py tool markitdown_convert "<path-to-file>"
   ```

   (The `~/.claude/bos-run.py` launcher resolves the install location for you.
   If it is missing, run `python tools/setup.py` once from the BOS directory to
   create it.) This handles PDF, Word, Excel, PowerPoint, images (OCR), HTML,
   CSV, JSON. If the converter reports it is not installed, relay its one-line
   install hint and continue with whatever was pasted.
2. **Anything they paste**, a few emails, posts, or texts dropped straight in.
3. **One good prompt when the well is shallow**, *"Paste me 3-4 emails or posts
   you wrote and were happy with, and I'll pull out how you sound."* A voice
   built from a handful of genuine samples beats a guessed one.

**Read every sample end-to-end.** Do not skim. In email threads and message
logs, keep the OWNER's lines and drop the other person's, so you capture how
*they* write, not their correspondent.

As you read, gather **candidate traits, each with a real example** from the
samples: typical sentence length and rhythm, vocabulary they reach for, signature
moves, greetings and sign-offs, punctuation habits, emoji use, contractions,
level of formality, humour, and the registers they never touch. Hold these as
observations to confirm, not conclusions to assert.

If there is genuinely almost nothing to read, you can still run Step 2 from how
they describe themselves. Say so plainly rather than inventing a voice.

---

## Step 2: The "this, not that" lock-in

This is what makes the voice *theirs*: a short, targeted session that turns your
observations into conscious choices. Draw each contrast from what you actually
saw in Step 1, and present concrete either/or options rather than open questions.

- **One or two contrasts at a time.** Never a wall of questions.
- **Smart-default-then-confirm.** Lead with what the samples suggest: *"Your
  emails open warm and personal, like 'Hope you're having a cracker of a week.'
  Lock that in as your default open, or do you want something crisper for
  business notes?"*
- **Tag why you're asking** when it isn't obvious, and always leave an escape
  (*"or skip and I'll use what I saw"*).
- **Make them choose the boundaries**, not just the preferences: which words or
  registers are off-limits (hype, jargon, corporate filler), and which normal
  words are absolutely fine so nothing gets over-restricted later.

Contrasts worth locking (pick the ones the samples make live):

- Warm and conversational **vs** crisp and professional (and whether that shifts
  by channel)
- Short and punchy **vs** fuller, more explanatory
- Contractions on **vs** off; emoji on **vs** off
- How you open a post: outcome-first **vs** question/curiosity-first
- Preferred greeting and sign-off
- Signature phrases they own **vs** phrases they never want put in their mouth
- Jargon tolerance: what's welcome, what's banned

Keep it tight: aim for the fewest contrasts that pin the voice down. Every sample
you write during this session follows the content guardrails in the Hard rules
below.

---

## Step 3: Write the voice file

Write the company voice to `marketing-strategy/<BrandName>/voice.md` and the
personal voice (if built) to `marketing-strategy/<BrandName>/personal-voice.md`.
Tell the owner exactly where each file is.

Use the same section shape the rest of the system expects, so every content app
reads it cleanly:

- **Meta-rule (open with it):** *The owner's voice IS the voice. Everything here
  is reference for writing in that voice when the owner isn't writing personally.
  When this doc and the owner disagree, the owner wins, and the doc gets updated
  to match what they actually shipped.*
- **Tone, 5 adjectives**, each backed by a real quote from the samples.
- **Signature moves**, the recurring patterns that make them sound like them,
  with examples.
- **Vocabulary to reach for**, phrases lifted verbatim from the samples, in a
  table with a source tag. Available, never mandatory.
- **Watch out for**, the registers and words the owner chose to avoid in Step 2,
  framed as defaults not absolute bans.
- **Words that are fine**, normal words the owner uses, listed so nothing gets
  over-restricted.
- **Mechanical preferences**, greeting, sign-off, emoji, punctuation.
- **Canonical examples**, at least one real sample the owner approved, with a
  short "why this works" note.
- **Change log**, dated entries whenever the owner corrects the voice later.

**Never clobber a hand-tuned file.** If `voice.md` already exists, read it, and
show the owner a short before/after of what you are changing before you write.
The personal-voice file is framed the same way, in the first person: how the
owner writes as themselves.

**Leave a pointer in the profile so a later session finds the voice.** Once a
voice is locked, add one dated line to the `## How the business is running` block
in `./CLAUDE.md` so a returning session (Day 4 of the 5-day challenge reads this
block) knows the voice exists and where it lives. This touches only the profile,
never the voice files themselves, and follows the same never-clobber discipline:

1. **Append, never overwrite.** Add the line to the `## How the business is
   running` block (create that heading at the end of the file only if it is
   missing). Leave every existing line in place. If a pointer line for this voice
   already exists from a prior run, update it in place rather than adding a
   duplicate.
2. **Use the session's current date.** Read today's date at runtime; never
   hardcode it.
3. **Line format:**
   `Voice locked (<date>): <short characterisation>, see <voice file path>`
   Example:
   `Voice locked (2026-01-15): direct, warm, short sentences, see marketing-strategy/<BrandName>/voice.md`
4. **One line per voice.** If the personal voice is also locked, add its own
   pointer line the same way, pointing at `personal-voice.md`.

---

## Step 4: Prove it, then hand it off

Show the voice working immediately:

- Draft one short sample in each voice you built (for example a post opener and
  an email line). Let the owner correct it. A correction is not a failure: fold
  it straight into the file and add a change-log line, so the voice gets truer
  every time they touch it.
- Then tell them plainly: *"That's locked in. From now on, whenever I write a
  post, a caption, a proposal, or an email, it comes out in this voice. Want me
  to plan a week of content or draft a post now to see it in action?"* Offer the
  natural next app (`write-post-copy`, `plan-my-content`), never push.

Keep your spoken report short: the voice files are the deliverable.

---

## Hard rules

- **Ground every trait in real evidence.** Do not invent how the owner sounds.
  If a trait has one supporting sample, say so; if there is no evidence for
  something, leave it out rather than guessing.
- **The owner always wins over the doc**, and their correction updates the file
  (with a change-log entry).
- **Content guardrails.** Customer-facing copy uses no em dashes, invents no
  facts, quotes, or numbers, and names no third-party vendor. Write it in the
  owner's brand voice; the framing and the marketing psychology are the owner's
  choice. The rules are in `knowledge/content-rules.md`. The voice files
  themselves are internal reference.
- **Private content stays internal.** Real names, private email content, and
  anything sensitive from the samples belong only in the owner's own files, never
  carried into public copy.
- **Do not clobber an existing voice file** without showing the diff first.
- **This is the owner's voice, not the customer's.** For the words customers use,
  that is `build-customer-voice`, a separate input.
