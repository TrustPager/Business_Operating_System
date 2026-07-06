---
description: Push a change to your team's standards out to everyone, with a per-person preview before it updates.
---

Run the **Sync Team Standards** skill.

Invoke the skill at `skills/sync-team-standards/SKILL.md`. Follow it exactly: read
the current `templates/team-standards.md`, find every existing pack under
`./team/<name>/`, regenerate each from the updated standards, show a per-person
diff, and update only after the operator confirms. Close with who changed and
what each person needs to re-pull.
