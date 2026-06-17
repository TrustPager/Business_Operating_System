---
description: Push an update to your team-standards out to everyone. After you edit team-standards.md, this regenerates each team member's pack (CLAUDE.md + memory) with a diff, so the whole team picks up the change instead of drifting.
---

Run the **Sync Team Standards** skill.

Invoke the skill at `skills/sync-team-standards/SKILL.md`. Follow it exactly: read
the current `templates/team-standards.md`, find every existing pack under
`./team/<name>/`, regenerate each from the updated standards, show a per-person
diff, and update only after the operator confirms. Close with who changed and
what each person needs to re-pull.
