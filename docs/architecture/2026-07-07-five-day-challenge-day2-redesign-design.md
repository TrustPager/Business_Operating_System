# Five-Day Challenge — Day 2 redesign: the capability tree

**Status:** Implemented. `skills/five-day-challenge/SKILL.md` carries the new Day
2-5 shape. The Day 2 visual shipped as `skills/five-day-challenge/assets/
capability-tree.png`, one static aspirational image (not per-member progress
states — see §6, revised after founder direction on 2026-07-07 to keep this
simple: "one aspirational image... let them dive in wherever they want").
A separate, premium version of the same content is a follow-up task in
`AI-BOS/skool-studio/` (its own `THUMBNAIL-RECIPE.md` "system-diagram mode"),
not part of this design. Day 1 is live with real members and unchanged by this
design. No member has reached Day 2 yet, so there was no in-flight behavior to
preserve there. Outstanding: Vic's own read-through/dogfood before release.

**One-line:** Day 2 stops being a fixed content-production day and becomes "the map":
a tour of the apps that make up the member's floor, a visual build map showing what's
built and what's next, and a pick of which floor app to tackle first. Days 3-4 loosen
from a fixed script into flexible completion of the same floor apps. Day 5 (graduation)
is unchanged except for explicitly naming the add-ons that open up once the floor is filled.

## 1. Why

Day 1 (`start-here`) ends on a consultation and one recommended first build. Members
who finish Day 1 have no sense of the rest of what their system can do beyond that one
build — the challenge has no moment that shows the shape of the whole floor before
asking them to keep building on it one conversation at a time.

The existing `whats-possible` skill already does a capability tour, but only at Day 5
graduation. Pulling a version of that tour forward to Day 2, paired with something
visual members can hold onto, closes the gap without duplicating `whats-possible`'s job
(Day 5 still shows the full menu; Day 2 shows the map of what's ahead specifically
inside the challenge).

## 2. Current Day 2 (being replaced)

Today: `build-my-voice` → `build-social-strategy` → `plan-my-content` →
`write-post-copy`. A real, tangible day with a strong kept win (voice locked in +
social strategy + content calendar + drafted posts). This content is not being
deleted — it becomes part of "filling in the floor" across the new looser Days 3-4.

## 3. Terminology (on-brand, not gaming)

The product already has the right vocabulary; this design reuses it rather than
inventing an RPG metaphor that risks alienating members who aren't into games:

| Instead of (gaming) | Use (already canonical in this codebase) |
|---|---|
| Skill tree | **Build map** (or "floor plan") |
| Base level / minor spells | **The floor** — already means the keyless tier everywhere else in the docs (`docs/CAPABILITIES.md`, `floor-roster.md`) |
| Higher level / fireball | **Add-ons** — already the term for Meta Ads, site builder/launch-my-site, etc. |
| "You must unlock X before Y" | "We recommend filling in your floor first, so everything stays aligned to your business — but nothing's locked, jump ahead if you want to." Never a hard gate; a strong recommendation. |

Owner-facing framing line: *"Here's the shape of your system: the apps that make up
your floor, and the add-ons you can build on top once it's filled in."*

## 4. The tree content (floor, add-ons, scaling, summit)

The base tier reuses the six categories already generated in `docs/CAPABILITIES.md`
from `kernel/registry.json` via `tools/export-capabilities.py`. This keeps that
tier CI-bound to the real registry instead of creating a second, hand-maintained
taxonomy that drifts (see the anti-drift doctrine — one rule, one home):

- 🏆 Win work
- 💰 Get paid
- 🤝 Stay on top of customers
- 🎨 Look professional & market
- 🗂️ Handle paperwork
- 🧭 Plan & decide

Day 2 copy re-skins these as "apps" in the member-facing tour without renaming them
in `CAPABILITIES.md` itself — the registry-generated file stays the single source of
truth; the skill just narrates it warmly.

Above the floor, the tree adds two more tiers (founder-directed 2026-07-07, not
derived from the registry, since these are partly aspirational/roadmap rather than
all shipped today):

- **Add-ons** (one tier up): Value Equation/Offer Tune-Up (off Win Work), Xero/
  Invoicing Sync (off Get Paid), Automations & Follow-Up Engine (off Stay on Top
  of Customers), Social & Video Studio + Meta Ads (both off Look Professional &
  Market), E-Signing & Document Workflows (off Handle Paperwork), Team &
  Reporting (off Plan & Decide).
- **Scaling** (deeper still, only this one branch goes here for now): Advanced
  Money Models (off Value Equation/Offer Tune-Up) — the advanced
  upsell/downsell/continuity systems, once the base offer is priced right via the
  Value Equation.
- **Summit**: a single highlight-box node, "Operate Your Business and Watch It
  Scale," that every leaf branch (the add-ons with no further child, plus Advanced
  Money Models) visually converges into — the tree literally builds up from the
  floor to the goal.

The Website/site-builder node was deliberately left out (those skills are being
pulled from the repo for now, per Vic, 2026-07-07).

## 5. The new daily shape

### Day 2 — "the map"
1. Recap Day 1's win, place them in the arc.
2. Tour the six floor branches from `CAPABILITIES.md`, in plain "apps" language,
   naming what's already done (their Day 1 build) and what's still open.
3. Show the capability tree image (see §6) — one static picture of the whole
   system, the same for every member every time, not tied to their progress.
4. Name the recommendation plainly: fill in the floor before reaching for add-ons
   (Meta Ads, site builder), but say explicitly it's not a lock.
5. They pick which floor app to tackle first. This sets ordering for Day 3, not an
   exclusive path — every member is still working toward a filled-in floor.
6. Kept win: they see the whole map and start their pick.
7. Operator move: *you can see the whole system now, not just the last thing you built.*
8. Tease: "Tomorrow we start filling it in for real."

### Days 3-4 — "fill in the floor" (loosened from a fixed script)
Same underlying apps as today's Day 2/3/4 content (brand/voice, offer + pricing +
proposal, content, money), but run as a flexible continuation rather than a rigid
Day-3-is-X, Day-4-is-Y script. Each session:
1. Pick up wherever they are (their Day 2 choice, or whatever's next).
2. Run the floor apps that fit, in their real business, same "always their business"
   rule as every other day.
3. End on a real kept win, same as always — never end on "you learned about X."
4. Update `challenge_floor_apps_done` for the resume logic (§7) — this no longer
   drives any image, the picture stays static; it's purely so a resumed Day 3/4
   session knows what's left without re-deriving it.

By end of Day 4, the floor is filled in for every member: voice/positioning, a priced
job + proposal, content, and a money basic. This is the fix for the original tension —
personalization is in ordering and pacing, not in which parts of the floor get skipped.

### Day 5 — graduation (mostly unchanged)
Same as today: walk back through the week, build the first routine
(`set-up-a-routine` / `connect-a-tool`), run `whats-possible`. The one addition: name
the add-ons explicitly as what's now open, tying back to the Day 2 map — "your floor's
filled in, here's what building on top looks like."

## 6. Capability tree image mechanics (as built, revised 2026-07-07)

**History (for context, not the current mechanism):** the first pass built an
architectural-blueprint floor plan with 8 pre-rendered PNGs tracking every
combination of the three floor clusters being done or not — see git history /
prior revisions of this doc if that's ever relevant again. Founder direction
on 2026-07-07 replaced that with a single static "aspirational" image: show
the whole system once, let the member choose where to dive in, don't try to
track their real progress in the picture. That simplification is what's built.

**Two separate deliverables, don't conflate them:**

1. **The session version (this repo, what SKILL.md actually shows):**
   `skills/five-day-challenge/assets/capability-tree.png`, generated by
   `assets/build_tree.py` (Pillow + numpy, no AI image generation). A radial
   near-black-teal background, hexagon nodes for floor/add-on/scaling tiers, a
   highlight-box summit, glowing connector lines — wireframe-simple by design,
   so it's trivial to regenerate if the content changes. Colors are TrustPager's
   teal tokens (ACCENT `#29c6c6` and friends), hardcoded in the script, not
   pulled from this repo's `brand/brand.json` (that file is the neutral
   customer-facing placeholder; this asset is AI BOS's own course material).
2. **The premium version (a separate, not-yet-started task):** built in
   `AI-BOS/skool-studio/` using its real production pipeline (`theme.js`,
   `THUMBNAIL-RECIPE.md`, `DESIGN-LOG.md`'s hard rules, `scripts/render.js`),
   as the "system-diagram mode: glowing core + skills radiating" variant that
   doc already earmarks. Same content/structure as #1, full production polish
   (real hex energy field, possibly generated hero art). For posting in Skool.
   Out of scope for this design; tracked here only so the connection is on record.

**Runtime lookup:** the skill always shows `capability-tree.png` — no marker
read, no per-member state, no image generation during a session. If the file
is ever missing, describe the map in words instead of stalling or erroring.

## 7. Marker changes (`./CLAUDE.md` profile)

Today's marker only tracks `challenge=day<N>`. This design adds (both for the
Day 3/4 resume flow, per §5 — neither drives the image, per §6):

- `challenge_floor_apps_done`: list of which floor clusters (Brand & Voice, Win
  the Work, Money & Paperwork) are complete, so a resumed Day 3/4 session knows
  what's left without re-deriving it.
- `challenge_first_pick`: which floor cluster they chose first on Day 2, for
  ordering and for later doorway copy ("you started with X, here's Y next").

Existing fields (`challenge_wins`, `doorways_open`) are unchanged.

## 8. Non-goals

- Not building per-member-generated or per-progress art. One static image (§6).
- Not making the floor-before-add-ons recommendation a hard gate — members can jump
  to a connected add-on early if they ask; the skill just states the recommendation
  once, plainly, per §3.
- Not touching `whats-possible` or the add-on skills themselves — this design only
  changes `skills/five-day-challenge/SKILL.md` and adds the `assets/` folder.
- Not using gaming-style icons (padlocks, etc.) anywhere on the tree — add-ons and
  the scaling tier render as open, inviting nodes, not locked doors, matching the
  "recommendation, never a lock" rule.
- Not building the premium `AI-BOS/skool-studio/` version as part of this design
  (§6) — that's a separate task in a separate repo.

## 9. Open items (need Vic, not code)

- Read-through / dogfood of the actual Day 2-5 flow in `SKILL.md` before release.
- The premium skool-studio "system-diagram mode" build (§6, deliverable #2) —
  not started.
- `AI-BOS/skool-studio`'s own `theme.js`/`DESIGN-LOG.md` still describe the
  pre-pivot blue+orange house kit; the teal pivot is only logged in the
  Remotion-VideoStudio spec doc so far. Worth reconciling those docs at some
  point, flagged here since it surfaced during this work, not actioned.

## 10. Addendum — goal lock-in (added after first dogfood)

A dogfood run of Day 2 surfaced a real gap: the profile template had a goal
field, but it was buried under "labelled guesses," merged with revenue into one
throwaway line, and only ever filled "if volunteered." Nothing instructed any
skill to actually reason against it. Founder-directed fix, same day:

- **`templates/CLAUDE.md`** gets a first-class `## My goal` section (own
  heading, not a buried bullet), paired with a standing instruction: once
  filled in, every recommendation in every skill should be reasoned against it,
  and roadblocks get treated as things to clear in service of it, not detours.
  The resume marker's `pending=[…]` gained `goal` alongside the existing
  `identity, customers, relief, voice` fields.
- **`start-here` (Day 1)** already surfaces a goal conversationally in its
  Step 6b consultation; it just never landed anywhere durable. Step 9 now
  writes a real stated goal into `## My goal` and drops it from `pending`. If
  the owner took the fast-win path instead and no goal was ever stated, it
  stays blank and pending, deliberately, rather than inventing one.
- **`five-day-challenge` Day 2** is the backstop, not the first ask: it opens
  by reading `## My goal`. If Day 1 already got it, Day 2 reflects it back and
  confirms in one exchange ("still the target?"), rather than re-interrogating.
  If it's still blank, Day 2 asks directly before running the tour. Either way
  it's locked in before the capability-tree tour runs, and the tour's
  recommendation is now reasoned from the goal explicitly ("given you're aiming
  at X, I'd suggest starting with Y, because...") before handing the actual
  choice back to the owner.

This also fixed a related dogfood note: the original recommendation-then-pick
transition read as an abrupt cold menu. Reasoning from the goal first, then
explicitly handing the choice back ("you know your business better than I do,
it's your call"), fixed both problems in the same edit.

## 11. Addendum — Day 2's closing beat (fixed same day)

The goal-lock rewrite in §10 accidentally dropped Day 2's closing beat, no
"tease tomorrow" line, breaking the daily-flow template every other day
follows. Also surfaced: Day 2 no longer ends on a built artifact (it locks a
goal, shows the tree, gets a pick), so unlike other days a member is often
primed to keep going rather than stop. Fixed in two parts:

1. **Continue-or-stop fork after the pick:** ask plainly whether to jump
   straight into the picked cluster's Day 3 content in the same sitting, or
   stop and pick it up next time. If they continue, the marker is set to
   `challenge=day3` (not `day2`), since that work is genuinely done. Never
   assumed either way, always asked, consistent with the "one day at a time is
   the default... unless they ask for more" hard rule.
2. **A goal-anchored close (when they stop), founder-directed:** a three-beat
   wrap rather than a one-line tease, (a) wrap what today gave them (goal
   locked, system mapped, pick made), (b) name what it leads to and what's still
   on the table (the rest of the floor, then the add-ons/scaling tier above it),
   (c) point at next session as a recommendation aimed at their goal, held
   loosely ("based on where you're headed, I'd have us [X] next, but we'll take
   it as it comes"). The general daily-flow step 7 was also lightly updated so
   every day from Day 2 on inherits this goal-anchored close, with Day 2 as the
   fullest worked example (one home for the pattern).
