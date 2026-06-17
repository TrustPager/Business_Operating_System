---
name: Lint Nurture Sequence
description: Check a nurture sequence against the house style before it ships, or catch drift in a live auto queue — every email needs a clickable text CTA above the image, a consistent sign-off, a positively framed subject, a greeting, and HTML structure. Flags per-email problems AND set-wide inconsistency (the thing that makes a drip feel half-built).
triggers:
  - lint the nurture sequence
  - check my sequence style
  - is my drip consistent
  - review the sequence emails
  - check the auto queue emails
  - are these emails on-brand
  - sequence quality check
---

# Lint Nurture Sequence

A nurture sequence underperforms when its emails drift apart — one has a bold
clickable link above the image, the next only has the image (so anyone who
blocks images has nothing to click); one signs off warmly, another just stops.
This skill runs a deterministic check over the whole set and tells the operator
exactly what's off, per email and across the set.

It's the quality gate between `design-nurture-sequence` (draft) and
`wire-nurture-sequence` (ship) — and it works on a live queue too, to catch
drift in something already running.

## Step 1 — Gather the emails (subject + body, in order)

Two ways in. Either way, you end up with an **ordered list of `{label, subject, body}`** that you reason over in Step 2. Use the `trustpager` MCP server.

> Tool names use `deal`/`event_queue` for legacy reasons — **always say "opportunity" / "sequence" to the operator**.

- **A live auto queue** — lint what's actually deployed. Two read calls (free):
  1. `get_auto_queue(id: <auto_queue_id>)` → returns the queue with its **steps**, each carrying a `step_order` and a linked `automation_id`. Sort the steps by `step_order`. (Get the queue id from `/nurture-health` or `list_auto_queues`.)
  2. For each step's `automation_id`, call `list_automation_actions(automation_id: <id>)` and find the send action (`action_type` of `send_gmail_email` / `send_custom_email` / `send_marketing_email`). Its `config.subject` and `config.body` are the email. Label each from the step's `description` (take the part before any "—") or "Step N". If a step has no linked automation or no send action, keep it in the list with empty subject/body and note it ("no send action on this step").

- **Local drafts** — lint before shipping, e.g. the drafts from `design-nurture-sequence`. If the operator hands you a drafts JSON file, `Read` it. Shape is either `[{"label": "Day 0", "subject": "...", "body": "<p>...</p>"}, ...]` or `{"emails": [ {...}, ... ]}` (body may be under `body` or `html`, label under `label` or `day`).

Two settings to confirm before you start: the **expected sign-off** (default `Warmest regards`; the operator may have a locked closer like "Warmest regards, Sam") and whether **em dashes** are allowed (default: flag them, because the house style avoids them — only permit if the operator has said em dashes are fine in their voice).

All reads — nothing here is journaled or needs approval. This skill **never writes** (see Step 3).

## Step 2 — Apply the lint rules (reason over each email)

For each email, evaluate every check below and record PASS / WARN / FAIL. An email's verdict is its worst check; the set's verdict is the worst email or consistency finding.

**Per email:**

| Check | Level when it fails | How to test | Why it matters |
|---|---|---|---|
| `subject` | FAIL if empty; WARN if > 90 chars | look at the subject | no subject = no open; long = the hook gets truncated |
| `greeting` | WARN if absent | first ~240 chars of body contain a `{{contact.*}}` token OR a word like "hi"/"hello"/"hey" | a cold open reads like a blast, not a note |
| `html` | WARN if body has text but no `<p` tag | check for `<p` in the body | plain text renders badly in Gmail |
| `link` | FAIL if **no `<a ... href=` at all** | any anchor with an href | nothing to click — the email does no work |
| `cta_above_image` | FAIL if there's an `<img>` but **no clickable TEXT link before it** | find the first `<img`; before that point there must be an `<a href>` whose visible inner text is non-empty AND is not just a wrapped image. An anchor that only wraps the image doesn't count. If there's no image, this passes (n/a). | image-blocked clients see no CTA — the exact gap that silently kills clicks |
| `signoff` | WARN if the expected sign-off string isn't in the body | case-insensitive substring match on the confirmed sign-off | inconsistent closers make the set feel unfinished |
| `positive_subject` | WARN if subject leads with negation | subject starts with / contains negative framing: `don't`, `do not`, `stop`, `never`, `no`, `isn't`, `won't`, `can't` | positive, forward-looking subjects outperform |
| `no_em_dash` | WARN if subject or body contains `—` (skip if em dashes permitted) | look for the em-dash character | house style avoids them |

**Across the set:**
- **MIXED `cta_above_image`** is a **FAIL** on purpose — if some emails (that have images) have a text CTA above the image and others don't, that inconsistency is the single biggest "half-built" tell. Don't soften it to a warning.
- **Inconsistent sign-offs** — WARN if the sign-off passes on some emails and not others; every email should close the same way.
- **Inconsistent P.S.** — WARN (informational) if a "P.S." line appears on some emails but not all; fine if deliberate.

## Step 3 — Present and route the fixes

Lead with the verdict and the fails, then the warnings, then "the rest are
clean". Translate each flag into the concrete fix.

```
Sequence lint — 7 emails: 2 fail, 3 warn

✗ Day 7  — Want AI to build your CRM for you?
     ✗ cta_above_image: image has no text link above it — add a bold "Connect Claude here:" link before the image
✗ Day 14 — Watch Claude wire up your pipeline
     ✗ cta_above_image: same issue
⚠ Day 21 — An automation that runs forever
     ⚠ signoff: 'Warmest regards' not found

Across the set:
  ✗ MIXED: Days 0/49 have a text CTA above the image, Days 7/14/21/28/38 don't — make it consistent.

Fix path: hand the failing emails to /design-nurture-sequence to rewrite, then
/wire-nurture-sequence to push the corrected copy. Re-run this lint to confirm green.
```

For live-queue fails, the fix is to rewrite the copy (`design-nurture-sequence`)
and re-wire it (`wire-nurture-sequence`) — **this skill never edits the queue
itself.** It only reports.

## What to never do

- ❌ Don't edit emails or the queue from this skill — diagnose and route only.
- ❌ Don't soften a MIXED `cta_above_image` to a warning — inconsistency across
  the set is the failure that matters most.
- ❌ Don't treat em dashes as allowed by default — only relax that check if the
  operator has said em dashes are fine in their voice.

## Output shape

Open with the one-line verdict (N emails, X fail, Y warn). List failing emails
with the concrete fix, then warnings, then the set-wide consistency findings.
Close with the fix path (rewrite → re-wire → re-lint) and offer to kick it off.
