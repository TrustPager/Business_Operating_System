---
description: Combine a record's filled forms and files into one ordered PDF pack, ready to send onward.
---

Run the **Assemble Pack** skill.

Invoke the skill at `skills/assemble-pack/SKILL.md`. Follow it exactly: list the
opportunity's files and completed-form PDFs, show the operator the candidate list
and let them choose which to include and in what order, confirm, then call
`bundle_files` (check its exact inputs with `describe_resource("file")` first) to
produce ONE combined PDF saved back to the opportunity. Never bundle without
showing the file list and order for a yes, and never send the pack anywhere.
assembling is not sending. If an expected document is missing, flag it (offer to
run `/outstanding-documents`) rather than shipping an incomplete pack.
