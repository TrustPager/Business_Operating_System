---
description: Design and create a reusable signing document template — sections, merge fields, and signer inputs. Plans the structure in chat for approval, then creates it via MCP. Does not send it.
---

Run the **Build Document** skill.

Invoke the skill at `skills/build-document/SKILL.md`. Understand the document
(what it is, who signs, what varies per deal) first, plan the section structure
in chat for approval, then create the template via MCP (`create_document_template`
→ `add_document_section` ×N → read back). Confirm every merge field is one the
opportunity can fill and every signer has a signature input before creating.

This skill BUILDS the template. It does not send it — that's `/send-for-signing`.
Offer `/lint-document` before the first send.

If the operator wants to start from an existing PDF/doc, read it and reverse-
engineer the sections rather than inventing a structure.
