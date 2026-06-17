---
name: Sync Team Standards
description: Propagate an update to the team's standards out to everyone. After the owner edits templates/team-standards.md (voice, verify rule, roles, approval rules), this regenerates each existing team member's pack (their CLAUDE.md + memory) from the new standards, shows a per-person diff, and updates only on confirmation. Closes the loop so a standards change reaches the whole team instead of only new hires. Run whenever team-standards.md changes.
triggers:
  - sync team standards
  - push the standards update
  - update everyone's setup
  - i changed team-standards, roll it out
  - refresh the team packs
---

# Sync Team Standards

`/onboard-team-member` propagates standards to a *new* hire. When the owner
changes the standards later, the existing team would otherwise drift. This skill
re-generates everyone's pack from the updated `templates/team-standards.md`, so
one edit reaches the whole team.

## Step 1 — Read the current standards + find existing packs

1. Read `templates/team-standards.md` in full (the new source of truth) and
   `knowledge/communication-voice.md` + `knowledge/safeguards.md` for the
   canonical wording.
2. List the existing packs: every folder under `./team/<slug>/`. Each maps to a
   person in section 5. If a person in section 5 has no pack yet, note them as
   "needs onboarding" (point to `/onboard-team-member`); if a pack exists for
   someone no longer in section 5, flag it for removal.

## Step 2 — Regenerate each pack (in memory) and diff

For each existing pack, regenerate its files exactly as `/onboard-team-member`
Step 3 would from the *current* standards + the owner's `./CLAUDE.md` + that
person's role: their `CLAUDE.md`, `memory/team-voice.md`,
`memory/verify-first.md`, `memory/role-and-approvals.md`, and `commands.md`.

Then show a **per-person diff**: what changed for each member (e.g. "Sarah: team
voice updated; approval threshold $5k → $3k; no role change"). Don't write yet.

## Step 3 — Confirm, then write

After the operator confirms, write the regenerated files into each
`./team/<slug>/`. Never clobber a pack that has hand-tuned local notes without
showing those specific lines and asking — preserve per-person customisations
that don't conflict with the standards.

## Step 4 — Tell people what to re-pull

The packs live in the owner's project; each person installed a copy on their
machine. So updating the packs here isn't enough on its own. Produce a short
note the owner forwards to whoever changed:

```
Standards updated. Re-pull your pack: copy the refreshed CLAUDE.md + memory/
from ./team/<your-name>/ into your project folder, then tell your Claude:
"Re-read CLAUDE.md and memory/ and follow them." (Changed for you: <one line>.)
```

Only message the people whose pack actually changed.

## Step 5 — Confirm

```
✓ Synced standards to 3 packs (1 unchanged):
  • Sarah (sdr): voice update + approval threshold change → re-pull
  • Bob (ae): voice update → re-pull
  • Ops: no change
  ⚠ Priya is in team-standards but has no pack → run /onboard-team-member
```

## Hard rules
- ❌ Don't write any pack before showing its diff and getting confirmation.
- ❌ Don't clobber hand-tuned per-person notes that don't conflict — surface and ask.
- ❌ Never widen a role's permissions beyond its row in team-standards.
- ✅ Standards flow ONE way: from `team-standards.md` into the packs. This skill never edits the standards themselves.
- ✅ Only ask people whose pack actually changed to re-pull.

## Output shape
A per-person summary of what changed (or "no change"), any members missing a pack
or packs with no member, and the re-pull note for those affected.
