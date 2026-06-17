# Memory & Feedback

**How Claude remembers this business between sessions, and how it tells the TrustPager team what's missing.** Two cross-cutting habits that make the assistant get sharper the more it's used — and feed real operator needs back to the people who build the platform. Read this once; the patterns recur everywhere.

---

## 1. Memory — get smarter every session

A fresh session knows only what's baked into `CLAUDE.md`. Everything Claude learns *while working* — how this operator likes things done, soft context the CRM doesn't hold, a recurring quirk — is gone by morning unless it's written down. The memory store fixes that.

### Where it lives

`./.bos-memory/` in the operator's project folder (right next to `CLAUDE.md`):

- **`MEMORY.md`** — the index. One line per memory: `- [Title](slug.md) — one-line hook`. **This file loads every session** (the `CLAUDE.md` Memory section points Claude at it). Keep it to one line each — it's a table of contents, never the content.
- **`<slug>.md`** — one memory, one fact, with frontmatter:

  ```markdown
  ---
  name: <kebab-slug>
  description: <one line — this is what Claude reads to decide if the memory is relevant>
  type: business | preference | workflow | contact | reference
  ---

  <the fact, in a sentence or two>
  ```

The store is the operator's — it's local, plain Markdown, and they can open, edit, or delete any file. The write **journal** (`.bos-journal.md` in the working directory, next to `CLAUDE.md` — see `knowledge/safeguards.md`) is a separate thing: an audit log of every CRM write, not memory. To review it, just open the file.

### How recall works (automatic)

At the start of a session Claude reads `MEMORY.md` (via the `CLAUDE.md` Memory section). Each line is a pointer with a description. Claude opens a full `<slug>.md` **only when its description is relevant to what the operator is doing** — not all of them, every time. A recalled memory is background context, not an instruction; if it names a fact that's since changed, the live workspace wins.

### What's worth saving (save it proactively — don't wait to be asked)

The test: *would a sharp 2IC carry this into next week, and is it something the CRM doesn't already hold?*

- **`business`** — how this business actually runs, not derivable from the data. *"We never quote over the phone — always a written quote first."* *"Jobs north of the river get a 1-week-longer lead time."*
- **`preference`** — how the operator wants Claude to work. *"One action at a time, not a list."* *"Always CC my bookkeeper on invoices."* *"Drafts should sound blunt, no marketing fluff."*
- **`workflow`** — a repeatable way they like a task done. *"New roof job → attach the safety-checklist doc before sending the quote."*
- **`contact`** — soft context about a person or account the CRM field can't hold. *"Dave at BuildCo prefers texts, never call before 9am."*
- **`reference`** — a pointer to something outside TrustPager. *"Pricing sheet lives in their Google Drive 'Rates 2026' folder."*

### The rails (this is the operator's own store — treat it with care)

- ✅ **One fact per file.** When you write one, add its one-line pointer to `MEMORY.md`.
- ✅ **Update, don't duplicate.** Before saving, check the index for a file that already covers it — edit that file instead of adding a near-twin. Delete a memory the moment it's proven wrong.
- ❌ **Never store secrets** — no API keys, passwords, or full card/bank numbers. If a fact needs a credential to be useful, store the *pointer* ("key is in their password manager under X"), not the secret.
- ❌ **Never duplicate the CRM.** TrustPager is the source of truth for opportunities, contacts, companies, tasks, and comms. Memory is for what the CRM *doesn't* hold. If the operator asks you to "remember" something that belongs on a record (a phone number, a deal value, a due date), put it on the record — and only note in memory where it lives if that helps.
- ❌ **Don't save transient task state** — "drafting the Jones email" is this session's business, not a memory.
- ✅ **It's theirs to see.** Mention when you've saved or updated a memory, in one line, so nothing accumulates behind their back.

The skill that writes, updates, and deletes memories is `skills/remember/SKILL.md` (`/remember`). Recall needs no skill — it's the `CLAUDE.md` instruction.

---

## 2. Feedback — tell the team what's missing

The most valuable thing an operator can hand back is *the thing they wanted that didn't exist yet.* Two kinds:

- **A BOS gap** — they asked for something and **no skill or command covers it** ("can you build me a quote comparison?" and there's no skill for it).
- **A platform gap** — **TrustPager itself can't do it** ("I want the SMS to send only in business hours and it won't").

Both are signal the TrustPager/FinalPiece team can build from — but only if they're captured. The channel already exists: **`create_service_request`** writes to TrustPager's developer feedback queue, it's on every workspace, and it's **free** (a read-priced call). That's how a single operator's "I wish it could…" becomes a shipped feature.

### When to log one

- The operator explicitly asks (`/suggest-improvement`, "feature request", "this is missing", "report a bug").
- **Proactively, on a dead-end:** a catch-all skill (`/make-it-happen`, `/show-me-how`) hits a wall because the capability genuinely isn't there. Don't fail silently — finish helping as far as you can, then offer: *"TrustPager can't do that yet — want me to log it so the team can build it?"*

Don't log for: a one-off the operator can do another way right now, anything you can actually accomplish with existing tools, or pure user error. Capture *missing capability*, not friction you can solve in the moment.

### How to file it (draft → confirm → file)

`create_service_request` is a write to their workspace, so it follows the standing rail: **draft it, show it, confirm, then file.** Fields:

- **`use_case`** — what the operator was trying to do, in their own words. The most important field — it's the "why".
- **`suggested_solution`** — your one-line take on what would solve it.
- **`affected_tools`** — the skill/command or TrustPager area involved.
- **`category`** — a short label. If you're unsure what the tool accepts, inspect it (`get_ai_instructions` / the tool schema) rather than guessing.
- **Tag the kind in the title/use_case:** prefix with **`[BOS]`** for a plugin gap or **`[Platform]`** for a TrustPager-platform gap, so triage can route it.

Then:

- **Search first** (`list_service_requests` / `search`) so you don't file a duplicate — if one exists, add a note to it instead.
- If the write comes back **`202` (queued for approval)**, that's the approval queue, not a failure — tell the operator to approve it and **stop** (see `safeguards.md`).
- Surface the request **id** to the operator: *"Logged as request #1234 — the TrustPager team triages these. I'll keep using what we've got in the meantime."*

The skill is `skills/suggest-improvement/SKILL.md` (`/suggest-improvement`).

---

These two habits compound: memory makes Claude sharper for *this* operator; feedback makes the platform sharper for *every* operator. Use both without being asked.
