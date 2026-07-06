---
description: Surface the deals that have gone quiet and draft a re-engagement message for each, to approve.
---

Run the **Follow-up Radar** skill at `skills/follow-up-radar/SKILL.md`.

Default: top 10 silent opportunities, silence threshold 7 days. If the operator mentions a different threshold in their message (e.g. "two weeks", "month"), pass it through as `--silence-days N`. If they ask for a specific count, pass `--top N`.

For each opportunity surfaced, draft one personalised re-engagement message and present for approval one at a time. Never batch-send.
