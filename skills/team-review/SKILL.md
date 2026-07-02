---
name: Team Review
description: A team-aware weekly rollup for managers. Pulls the week's activity grouped by team member (tasks completed, opportunities moved and who moved them, calls logged, messages sent), surfaces pipeline moves and bottlenecks (overdue, gone quiet), and presents a tight manager-facing summary. The team version of /weekly-review, which is solo-only. Read-only.
triggers:
  - team review
  - how did the team do this week
  - team weekly rollup
  - what did the team ship
  - team retrospective
function_slot: people
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - mcp__list_tasks
  - mcp__list_activities
status: active
---

# Team Review

`/weekly-review` answers "how did *I* do". A manager needs "how did the *team*
do": who shipped what, which deals moved and through whose hands, and where work
is stuck. This skill is read-only — visibility, not changes.

## Step 1 — Resolve the team + the window

Read the team members from `templates/team-standards.md` section 5 (names →
user ids). Default window is the last 7 days; honour a different range if the
operator asks ("this month", "since Monday").

## Step 2 — Pull the week's activity, grouped by person

Use the workspace data (a `bos-run.py team-review` fetcher if present, else the
APIs below) to gather, per team member:

- **Tasks completed** (and how many still overdue) — `list_tasks` filtered by
  `assigned_to` + completion/ due dates.
- **Opportunities moved** — stage changes in the window and who made them
  (`list_activities` / opportunity activity, grouped by user).
- **Calls logged + meetings** — `list_activities` of type call/meeting per user.
- **Messages sent** — outbound email/SMS counts per user where available.

Also pull, team-wide:
- **Pipeline moves** worth narrating (a deal that went rep → AE → won, with the
  hands it passed through and how long each held it).
- **Bottlenecks** — people with overdue tasks, opportunities gone quiet 7+ days,
  anyone with no activity in the last 2 days.
- **Close-gap flag** — where the data shows conversion or win-rate by person, a
  large founder-vs-team gap is a motion problem, not a market problem
  (business-method.md §3): flag it as a motion-transfer candidate (record,
  review, the delegation loop with a rubric, §12.1) rather than a performance
  mark. If per-person conversion isn't derivable, skip silently.

For anything `unavailable`, note it rather than guessing.

## Step 3 — Present the manager rollup

Tight, scannable, names first:

```
🏆 Team week — 10-16 Jun

Shipped
  Sarah (sdr): 8 proposals, 12 calls, 6 opps qualified  (2 tasks overdue)
  Bob (ae): 3 deals won ($45k), 24 customer emails
  Ops: 2 automations built, 30 import errors cleared

Pipeline moves
  "Acme 50k": Sarah qualified → Bob pitched → in negotiation
  "XYZ 12k": Sarah → Bob → won (7 days end to end)

Watch
  Sarah: 2 tasks overdue
  Bob: no logged activity in 2 days
  "Beckers 20k": gone quiet 9 days, owner Bob
```

End with one line: the single thing the manager should action this week (the
biggest bottleneck or the deal most at risk).

Per person, the same discipline: if someone's numbers lag, name ONE thing, the
lowest item, not a list (business-method.md §12.1). The rollup is the input to
the weekly 1:1 where the manager mostly listens (§12.6).

## Hard rules
- ❌ Read-only — this skill never writes. (If the manager wants to act on a
  bottleneck, point them at `/delegate-this-work`; for quality-shaped
  bottlenecks, `/review-team-draft`.)
- ❌ Don't guess numbers for `unavailable` sources — say what couldn't be read.
- ✅ Group by person, names first; managers scan by who.
- ✅ Surface bottlenecks plainly; that's the value, not the vanity metrics.

## Output shape
A grouped weekly rollup: shipped-by-person, notable pipeline moves, a "watch"
list of bottlenecks, and one recommended action. No raw data dumps.
