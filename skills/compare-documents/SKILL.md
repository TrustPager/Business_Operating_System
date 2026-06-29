---
name: Compare Documents
description: Compare two documents and show what actually changed. Converts both files (PDF, Word, etc.) to Markdown with the standard MarkItDown tool, then reports the meaningful differences in plain language — added, removed, changed — calling out moved figures and clauses. For contract versions, revised quotes, updated terms/policies. Built on knowledge/document-tools-method.md.
triggers:
  - compare these two documents
  - what changed between these
  - diff these contracts
  - compare v1 and v2
  - what's different in the new version
function_slot: documents
requires_driver: markitdown
requires_credential: none
data_path: local
status: active
---

# Compare Documents

"What changed between these two versions" is a constant question for anything
contractual. This converts both and reports the differences that matter, not a
character-level diff.

## Step 1 — Convert both files

```bash
python ~/.claude/bos-run.py tool markitdown_convert "<file-A>"
python ~/.claude/bos-run.py tool markitdown_convert "<file-B>"
```

(The `~/.claude/bos-run.py` launcher resolves the install location for you. If it is missing, run `python tools/setup.py` once from the BOS directory to create it.)

If either converts empty, say so and stop — you can't compare what you can't read.

## Step 2 — Compare meaningfully

Work from both Markdown versions. Report differences grouped as:
- **Added** — content in B that isn't in A.
- **Removed** — content in A that's gone in B.
- **Changed** — content present in both but different, especially **numbers,
  dates, names, and clauses** (e.g. "Fee: $2,000 → $2,500", "Term: 24 → 36
  months", "added a termination-for-convenience clause").

Lead with the changes that carry weight (money, obligations, dates, parties),
not formatting noise. Ignore pure layout/whitespace differences unless asked.

## Step 3 — Report in plain language

```
Comparing "Quote-v1.pdf" → "Quote-v2.pdf":

Changed
  • Total: $12,400 → $13,900
  • Delivery: 4 weeks → 6 weeks
Added
  • New clause: 20% deposit on acceptance
Removed
  • The "price held for 30 days" line is gone
```

End with one line on the net effect if it's clear ("v2 is $1,500 dearer, slower,
and adds a deposit"). Don't editorialise beyond what the documents show.

## Hard rules
- ❌ Don't compare unreadable conversions — flag and stop.
- ❌ Don't drown the real changes in formatting/whitespace noise.
- ❌ Don't misreport a figure — quote both sides (old → new) so it's checkable.
- ✅ Always convert through `tools/markitdown_convert.py`.
- ✅ Lead with money / dates / obligations / parties; those are what matter.

## Output shape
Grouped Added / Removed / Changed differences in plain language, figures shown
old → new, and a one-line net effect if clear.
