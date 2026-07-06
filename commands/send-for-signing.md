---
description: Send a document to signers with the safeguards: confirm signers, preview the merge, track signs.
---

Run the **Send For Signing** skill.

Invoke the skill at `skills/send-for-signing/SKILL.md`. You need three things
first: the template (`template_id`), the opportunity (`deal_id`), and the signer
list (`{name, email}` each). Read the send back to the operator (document, to
whom, on which deal) and get an explicit yes before calling `send_for_signing`.
Offer to preview the resolved document for a new or just-edited template.

Real signers only. Never a test/`@example.com` address. One real send at a time.
If the operator hasn't built the template yet, redirect to `/build-document`.
After sending, hand off to `/signing-radar` and mention the `signature_opened`
automation for instant open alerts.
