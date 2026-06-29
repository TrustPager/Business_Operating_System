---
description: Set up a new team member to run on Claude Code with your team's standards baked in. Generates their CLAUDE.md + a memory pack + a role-scoped command list from your team-standards file and live workspace, so they sound like the team and follow the same process from day one.
---

Run the **Onboard Team Member** skill.

Invoke the skill at `skills/onboard-team-member/SKILL.md`. Follow it exactly: read
`templates/team-standards.md` (and the owner's `./CLAUDE.md` for shared business
context), confirm the new person's name / email / role, then generate their
onboarding pack into `./team/<name>/`: a filled `CLAUDE.md`, a small memory pack
(team voice, verify-before-customer, their role's boundaries), and the list of
slash commands their role gets. Never overwrite an existing pack without showing
the diff. Close with what was generated, where, and the exact steps the new
person follows to install it on their machine.
