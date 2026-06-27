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
function_slot: comms
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
status: active
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

## Step 1 — Pick the source

Two ways in:

- **A live auto queue** — lint what's actually deployed:
  ```bash
  python tools/lint-sequence.py --queue <auto_queue_id> --json
  ```
  (Get the queue id from `/nurture-health` or `python tools/dump-crm-bundle.py --resources auto_queues`.)

- **Local drafts** — lint before shipping, e.g. the drafts from
  `design-nurture-sequence`:
  ```bash
  python tools/lint-sequence.py --drafts drafts.json --json
  ```
  Drafts file: `[{"label": "Day 0", "subject": "...", "body": "<p>...</p>"}, ...]`.

Useful flags: `--signoff "Warmest regards, Sam"` to match the operator's locked
closer; `--allow-em-dash` if the operator is fine with em dashes (default flags
them, because the house style avoids them).

## Step 2 — What each check means

Per email:

| Check | Fails when | Why it matters |
|---|---|---|
| `subject` | missing / very long | no subject = no open; long = the hook gets truncated |
| `greeting` | no "Hi {{contact.first_name}}" up top | a cold open reads like a blast, not a note |
| `html` | body isn't `<p>` HTML | plain text renders badly in Gmail |
| `link` | **no link at all** | nothing to click — the email does no work |
| `cta_above_image` | there's an image but **no text link above it** | image-blocked clients see no CTA — the exact gap that silently kills clicks |
| `signoff` | the sign-off block is missing | inconsistent closers make the set feel unfinished |
| `positive_subject` | subject leads with negation | positive, forward-looking subjects outperform |
| `no_em_dash` | contains `—` | house style (relax with `--allow-em-dash`) |

Across the set:
- **MIXED cta_above_image** is a FAIL on purpose — some emails following the
  pattern and others not is the single biggest "half-built" tell.
- Inconsistent sign-offs or P.S. presence are WARNs — align them unless the
  variation is deliberate.

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
- ❌ Don't treat `--allow-em-dash` as the default — only pass it if the operator
  has said em dashes are fine in their voice.

## Output shape

Open with the one-line verdict (N emails, X fail, Y warn). List failing emails
with the concrete fix, then warnings, then the set-wide consistency findings.
Close with the fix path (rewrite → re-wire → re-lint) and offer to kick it off.
