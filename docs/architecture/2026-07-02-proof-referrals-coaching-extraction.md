# Proof, Referrals & Call-Coaching — three floor ports (Tier-1 extraction batch)

**Status:** Approved design (founder-approved 2026-07-02). Applies the
`trustpager-to-floor-extraction.md` recipe to the three highest-value capability
gaps found in the post-SEO audit. Names ruled by founder: `build-my-proof`,
`set-up-referrals`, `coach-my-calls`.

---

## 1. Why these three

Post-SEO reconciliation (the June-25 `skill-extraction-audit.md` vs the current
40-skill floor) found the remaining SEO-style ports — a paid TrustPager
capability whose *method is already in `business-method.md`* + a keyless slice +
**no floor front door** — cluster in word-of-mouth/proof and sales-motion:

- **Proof / reputation** (`request_reputation_review`, `get_reputation_stats`,
  `create_reputation_case_study`) — reviews are §10.5 tier-2, the top local
  growth lever; `get-found-online` can only flag it. No skill builds it.
- **Referrals** (`create_referral`, referral links/commissions/leaderboard) —
  §10.7 is fully-written doctrine; ~25%+ of a healthy business's new work; no
  floor skill.
- **Call coaching** (`ai_call_coaching`) — accepts raw `transcript_text`, so the
  analysis is pure reasoning (fully keyless). Rubric already exists (§12.5). No
  skill coaches a call you already had.

These three interlock: a captured win (proof) is the exact high-emotion moment to
ask for a referral (§10.7), and better sales calls (coaching) create more wins to
capture. Together they complete the floor's growth story:
**get found → prove results → turn results into referrals → sharpen the sale.**

## 2. The founder enrichment — proof is a *transformation story*, not a review

The centerpiece: a written 5-star review is weak proof; a **measured before→after
transformation in the client's own voice** is the strongest proof there is
(§7.2 Belief). So `build-my-proof` runs a **play across the whole engagement**,
not a one-time ask. This is doctrine-perfect: the value equation's Arrival made
provable (§6), the strongest likelihood signal (§7.2), proof-publishing (§10.5
tier 4), and it fires the referral moment (§10.7). The
`create_reputation_case_study` tool is literally `problem → solution → outcome →
key_metrics` — the same spine.

## 3. Skill 1 — `build-my-proof` (the transformation engine)

**Frontmatter:** `function_slot: strategy`, `requires_driver: none`,
`requires_credential: none`, `data_path: reasoning_only`, `status: active`.
Keyless: it produces scripts/docs from what the owner provides; an optional
`.docx` case study uses the document toolkit the way `write-a-proposal` does
(offered, not required). Baseline persistence keyless = a local file
`proof/<client-slug>-baseline.md`; connected = the CRM record.

**Three modes (detect from context or ask which):**

- **Kickoff (set up the win-story).**
  1. The owner states the **target outcome** — what winning looks like for this
     client, measurable where possible (the Arrival, §6). Prompt for it plainly.
  2. The skill **manufactures the baseline capture**: the specific "before" to
     record now — starting numbers, the situation, the pain in the client's own
     words, the goal — plus the exact questions to ask the client to get it.
  3. Write the baseline to `proof/<client-slug>-baseline.md` (or the record). This
     is what makes the story provable later; without it there is no delta.

- **Wrap (capture the win-story).**
  1. Load the baseline (file/record); if missing, reconstruct from the owner's
     memory and say so.
  2. Capture the **outcome** — the "after" numbers and the change.
  3. Compute the **before→after delta** (the transformation, with hard numbers).
  4. Produce two artifacts:
     - **Written case study** shaped `problem → solution → outcome →
       key_metrics` (the reputation-tool spine), positive/outcome-led.
     - **Video testimonial script** in the client's voice, the transformation arc:
       *"I'm [name] from [company], before working with [owner] I was [before /
       problem], we did [X, Y, Z], and now [after / result]."* Short (aim ~60-90s
       spoken), natural to read on camera, with a few filming tips (say the
       numbers, one take is fine, good light).

- **Quick review (velocity path).** The fast 5-star ask kit: the ask script sent
  at the moment of demonstrated satisfaction, by the person who did the work, with
  a direct link (§10.5 tier 2 timing), plus reply templates for each rating. For
  when the owner wants volume, not a full story.

**Deepener doorway (reactive, outcome-only):** tracked review-request sends, live
rating stats, case studies published on the reputation page, video hosting.

**Doctrine anchors:** §6 (Arrival), §7.2 (Belief/proof stack), §10.5 (tiers 2 &
4), §10.7 (the win moment feeds referrals), §11.3 (baseline is captured at
activation — the first-win moment).

## 4. Skill 2 — `set-up-referrals` (the referral engine)

**Frontmatter:** `function_slot: strategy`, `requires_driver: none`,
`requires_credential: none`, `data_path: reasoning_only`, `status: active`.

Installs the §10.7 referral engine as usable artifacts:
- The ask designed as an **introduction** (a three-way text / warm intro), never
  "got any names?" — the §10.7 rule.
- **Timing** at high-emotion moments (right after a win, at purchase, at job
  completion) — so it **hands off directly from `build-my-proof`'s captured win**.
- **Mutual reward**, one-click, tracked, fast-paid — recommend a structure that
  fits the shape (§15 adapters: no cash incentives where a regulated shape bars
  them).
- Produces: the ask scripts per moment/channel, the reward-structure
  recommendation, and a simple tracking sheet (who asked, who introduced, status).

**Deepener doorway:** live referral links, automated commission tracking, the
referral leaderboard.

**Doctrine anchors:** §10.7 (the referral engine), §10.5 tier 5, §10.9 (referrals
are an L4 lead-getter, not an L1 machine — keep it simple for small owners).

## 5. Skill 3 — `coach-my-calls`

**Frontmatter:** `function_slot: strategy`, `requires_driver: none`,
`requires_credential: none`, `data_path: reasoning_only`, `status: active`.

Paste a call / quote-visit / discovery transcript (or bring one from
`transcript-summary`, which owns the paste/local-file/transcribe path) → coaching
against the **discovery arc (§12.5)**:
- Score the six beats (hear it → name it → map what they tried → sell the arrival
  → settle the concerns → seal it) and the three objection costumes
  (circumstances / other people / self).
- Return **what went well**, the **1-2 highest-leverage fixes** (not a laundry
  list — §4 item 7), and a concrete **rehearsal line** for next time.
- Ethics line intact: coach to help the buyer decide, never to corner (§12.5).
- For a hire being coached, frame via the 3Ds (§12.1): feedback on the single
  lowest-scoring beat per round.

**Deepener doorway:** auto-pull transcripts per team member, coach across many
calls, track improvement over time, feed `team-review`.

**Doctrine anchors:** §12.5 (discovery arc — the rubric), §12.1 (3Ds coaching),
§3 constraint #2 (sales/conversion is what this attacks).

## 6. Shared knowledge — `knowledge/proof-and-referrals-method.md`

One home for the word-of-mouth how-to that `build-my-proof` and `set-up-referrals`
share: the transformation-story structure, the baseline-capture checklist, the
video-testimonial script template, the review-ask timing, and the
introduction-style referral ask. It **links to** §6/§7.2 (why transformation
proof beats a star review), §10.5 (review timing + proof publishing), §10.7
(referral engine), and §11.3 (baseline at activation) rather than restating them
(one home). Ends with the positive-only + no-em-dash output rule.

`coach-my-calls` references `business-method.md` §12.5 directly (it is already a
complete rubric) — no separate method file needed.

## 7. Wiring (per the extraction pattern's checklist)

- **`kernel/registry.json`** — three entries, `reasoning_only` / `none` / `none`
  (copy `grill-me-on-this-decision`'s shape; no `uses_tools`).
- **`knowledge/starter-projects.md`** — a row for each in the relevant group
  (🤝 Stay on top of customers / 🏆 Win work), add to the §2 keyless-core pool,
  and to the §4 relief→project mapping (proof/referrals under "finding leads /
  looking professional / staying on top of customers"; coaching under a
  sales/"win more of what I quote" relief).
- **Do NOT hand-edit `whats-possible`** (runtime registry reader).
- **`docs/CAPABILITIES.md`** — regenerate via `python tools/export-capabilities.py`.
- **`docs/architecture/trustpager-to-floor-extraction.md`** — move these three
  from "candidates" to built worked-examples (#2-#4), keep the rest as candidates.

## 8. Validation — dogfood each on Sonnet

- **`build-my-proof`:** a full kickoff→wrap round-trip for a real-ish client.
  Pass bar: kickoff produces a concrete measurable outcome + a baseline record
  with the right "before" data; wrap computes the before→after delta and produces
  BOTH a `problem→solution→outcome→metrics` case study AND a natural, short video
  script in the client's voice; positive-only, no em dash; deepener reactive.
- **`set-up-referrals`:** pass bar: the ask is an *introduction* not "any names?",
  timed to the win moment, mutual reward, and it references handing off from a
  captured win; shape-aware on incentives.
- **`coach-my-calls`:** paste a flawed discovery transcript. Pass bar: scores the
  six beats, names the 1-2 highest-leverage fixes (not a laundry list), gives a
  rehearsal line, keeps the ethics line, no invented transcript content.

## 9. Non-goals (YAGNI)

- No live review/referral sends or commission tracking on the floor (deepeners).
- No auto-transcription build in `coach-my-calls` — it consumes a transcript
  (`transcript-summary` owns getting one).
- No new video *production* (the script is text; filming is the owner's).
- No prospect-list / needs-analysis / pipeline-design skills this batch (Tier 2/3,
  later).
