---
name: Build Knowledge Base From Docs
description: Turn the business's policy / FAQ / product / process documents into answerable AI Knowledge in TrustPager. Converts each file (PDF, Word, slides, etc.) to Markdown with the standard MarkItDown tool, splits it into clean knowledge entries, and loads them into TrustPager AI Knowledge so the in-app assistant and voice agents answer from the client's real documents. Built on knowledge/document-tools-method.md.
triggers:
  - build a knowledge base from these docs
  - load my policies into ai knowledge
  - turn these documents into faqs
  - make my docs answerable
  - ingest these into knowledge
function_slot: documents
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - mcp__trustpager__create_knowledge
  - mcp__trustpager__ingest_knowledge_base_text
status: active
---

# Build Knowledge Base From Docs

A business's real answers live in documents (policies, product sheets, FAQs,
process guides). This skill makes them answerable everywhere TrustPager AI runs
— the in-app assistant and voice agents — by loading them into AI Knowledge.

## Step 1 — Convert each document to Markdown

For every file the operator points at:

```bash
python ~/.claude/bos-run.py tool markitdown_convert "<path>"
```

Handles PDF, Word, PowerPoint, Excel, HTML. If MarkItDown isn't installed, relay
its install hint and stop. If a file converts empty (e.g. an image-only scan with
no OCR text), flag it rather than loading a blank entry.

## Step 2 — Split into clean knowledge entries + show the plan

AI Knowledge works best as focused entries, not one giant dump. From the
Markdown, propose a split: one entry per topic / policy / FAQ, each with a clear
title and the relevant content. Show the operator the proposed entries before
writing:

```
From "Lending-policy-2026.pdf" I'd create 6 knowledge entries:
  • "Minimum deposit requirements"
  • "Acceptable income types"
  • "Self-employed applicants" ...
From "Product-sheet.docx": 3 entries. Total: 9 entries.
OK to load these into AI Knowledge?
```

Keep titles in the customer's own words. Don't invent content that isn't in the
documents; don't merge unrelated topics into one entry.

## Step 3 — Load into AI Knowledge (after confirmation)

Create the entries in TrustPager AI Knowledge (`create_knowledge` /
`ingest_knowledge_base_text`, per the platform's knowledge tools). Batch them;
stream progress. Respect the approval queue (202 = queued, surface it —
`knowledge/safeguards.md`). Tag the source document on each entry so it's
traceable and easy to refresh later.

## Step 4 — Confirm + point at where it's used

```
✓ Loaded 9 entries into AI Knowledge from 2 documents.
  Your in-app assistant and voice agents will now answer from these.
  Re-run this when a policy changes to refresh the entries.
```

## Hard rules
- ❌ Don't load empty or image-only conversions — flag them instead.
- ❌ Don't invent or merge content — entries reflect what the documents say.
- ❌ Don't write to AI Knowledge without showing the proposed entries first.
- ✅ Always convert through `tools/markitdown_convert.py` — no bespoke parsing.
- ✅ One focused entry per topic; titles in the customer's words; source tagged.

## Output shape
The proposed entry list per document for confirmation, then a one-line load
confirmation (how many entries, from how many docs) and where they're now used.
