---
description: Diagnose why a specific automation didn't do what you expected — disabled, never matched, conditions skipped it, an action failed, or it ran fine and the surprise is in the outcome. One reason, one fix.
---

Run the **why-didnt-it-fire** skill.

Invoke the skill at `skills/why-didnt-it-fire/SKILL.md`. Follow its instructions exactly — it pulls the automation and its run log via `trustpager` MCP read tools (`get_automation`, `list_automation_runs`, `get_automation_run`) for the given automation id/name, walks the run-log ladder, and gives the operator the single real reason plus the fix.
