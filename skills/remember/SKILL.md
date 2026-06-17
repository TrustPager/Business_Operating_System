---
name: Remember
description: Save, update, or forget a long-term memory about this business — how the operator likes things done, soft context the CRM doesn't hold, a recurring quirk — so Claude carries it into future sessions. Writes one fact per file into ./.bos-memory/ and keeps the MEMORY.md index current. Use when the operator says "remember that…", "from now on…", "note that I prefer…", or when you've just learned something durable worth keeping.
triggers:
  - remember that
  - remember this
  - from now on
  - note that I prefer
  - keep in mind
  - forget that
  - update what you know about
  - what do you remember
---

# Remember

The full model — where memory lives, how recall works, what's worth saving, and the rails — is in `knowledge/memory-and-feedback.md`. Read it if you haven't this session. This skill is the **write/update/delete** path; recall is automatic via the `CLAUDE.md` Memory section.

The store is `./.bos-memory/` in the operator's project folder: an index `MEMORY.md` plus one `<slug>.md` per fact.

## Step 1 — Decide if it belongs in memory at all

Apply the test from the knowledge doc: *would a sharp 2IC carry this into next week, and does the CRM not already hold it?*

- If it's a CRM fact (a phone number, deal value, due date, stage) → **put it on the record**, not in memory. Tell the operator that's where it went.
- If it's transient ("drafting the Jones email") → don't save it.
- If it's a secret (key, password, full bank/card number) → **refuse to store the secret**; offer to store a pointer to where it lives instead.
- Otherwise, classify it: `business`, `preference`, `workflow`, `contact`, or `reference`.

## Step 2 — Check for an existing memory first

Read `./.bos-memory/MEMORY.md` (create the folder + an empty index if neither exists). Scan the index for a line whose description already covers this fact.

- **Match found** → open that `<slug>.md` and **update it** rather than creating a near-duplicate.
- **No match** → you'll create a new file in Step 3.

## Step 3 — Write the memory

For a **new** memory, pick a short kebab-case slug and write `./.bos-memory/<slug>.md`:

```markdown
---
name: <slug>
description: <one line — what Claude reads on recall to decide relevance>
type: business | preference | workflow | contact | reference
---

<the fact, in a sentence or two. Link related memories with [[other-slug]] if useful.>
```

Then add a one-line pointer to `./.bos-memory/MEMORY.md`:

```
- [Title](<slug>.md) — short hook
```

For an **update**, edit the file's body (and its `description`/index line if the gist changed). For a **forget**, delete the `<slug>.md` and remove its index line.

## Step 4 — Confirm in one line

Tell the operator plainly what you did, so nothing accumulates behind their back:

- `🧠 Saved — "We never quote over the phone, always a written quote first" (business).`
- `🧠 Updated what I know about Dave at BuildCo.`
- `🧠 Forgotten — dropped the old after-hours rule.`
- `That belongs on the opportunity record, not memory — I've put it there instead.`

## Hard rules

- ❌ Never store secrets — store a pointer, never the credential itself.
- ❌ Never duplicate the CRM — TrustPager is the source of truth; memory is for what it doesn't hold.
- ❌ Never let the index hold content — `MEMORY.md` is one line per memory, full stop.
- ✅ One fact per file. Update the matching file instead of adding a twin. Delete what's proven wrong.
- ✅ The store is the operator's — local, plain Markdown, theirs to edit or wipe. Surface every save/update/delete in one line.
- ✅ Save proactively when you learn something durable — don't wait to be told "remember this".

## Output shape

A single confirmation line (saved / updated / forgotten / redirected-to-CRM). No essay. If you saved something the operator didn't explicitly ask you to, say so in the same line so they can correct it.
