# The Content-Doctrine Layer

> **SCOPE UPDATE 2026-07-06 (founder ruling; read this first, it changes the doc below).**
> The four content rules are NOT all universal, and the client-facing product must not
> impose FinalPiece's brand taste on a client's marketing. Corrected scope:
> - **positive-only is STRIPPED from the client BOS.** It is FinalPiece house style, not a
>   client rule. Clients choose their own marketing psychology (pain-led, fear-led, whatever).
>   positive-only stays only in FinalPiece's own settings (global CLAUDE.md +
>   settings/recommended-global-claude.md). The "clients don't receive the doctrine = gap"
>   framing below is WRONG for positive-only; that was the correct boundary.
> - **no-em-dash, never-invent-evidence, no-vendor-leak, plain-language are KEPT for
>   clients** and consolidated into a shipped `knowledge/content-rules.md` home + one anchor.
>   The em-dash mechanical guard (`tools/_content_rules.py`) STAYS.
> - The BOS already writes in the CLIENT's own voice (build-my-voice / build-brand-strategy);
>   the fix is removing the house-style override, not adding one.
>
> Sections below that treat positive-only as a shipped/consolidated client rule are
> superseded by this note. The current plan is
> [`plans/2026-07-06-content-doctrine-layer.md`](plans/2026-07-06-content-doctrine-layer.md).

**The question (Vic, 2026-07-06, from a team session):** the ~92 skills each restate the same rules (no em dashes, reactive-TrustPager, plain language, positive-only). That is a maintenance tax and a per-invocation token cost. The `knowledge/*-method.md` files are the right move (skills reference the method instead of restating it). How do we push more of the repeated rules down into shared knowledge so skill bodies get leaner?

**One-line answer:** the *safety rails* are already homed correctly in `safeguards.md` and should stay reference-only. The *content-generation doctrine* (positive-only, no em dashes, never-invent-evidence, no-vendor-names) has **no home that ships inside the pack** because its canonical statement lives in Vic's private global `~/.claude/CLAUDE.md`, which clients never receive. So skills paste it. The fix is one shipped home (`knowledge/content-rules.md`) plus a single one-line inline anchor per content skill, not pure extraction. The anchor matters because a rule that is only referenced can be silently missed on Sonnet, and there is a field incident proving it.

This doc was produced by an 18-agent audit workflow (map + 12 skill-audit batches + synthesis + 3 adversarial verifiers) and the verifier corrections are folded in. See the appendix for what changed.

---

## 1. Why the restatement exists (the root cause)

Two different rule-types get lumped together under "repeated rules," and they have different fixes.

**Rails and service-voice are already homed and mostly referenced.** `knowledge/safeguards.md` owns the five write rails (202-means-queued, ask-before-destructive, verify-before-customer, one-workspace, journaled-writes). `knowledge/communication-voice.md` owns operational-message tone (plain, warm, short). `knowledge/connectors.md` owns the reactive keyless-to-connected "connect-doorway articulation" and labels itself the single home. `business-method.md` §12.5 and §18 own the discovery arc and the pain-is-a-diagnostic-input boundary. These are the pattern to emulate. Where skills still restate the rails inline (see §7), that is a discipline problem, not a homing problem: the home exists, skills just do not point at it.

**The content-generation doctrine has no home that ships.** Verified against the repo:

- **positive-only:** `business-method.md` §18 is a *bridge*. It asserts "The BOS ships a hard rule: customer-facing copy is outcome-led, never pain-led" and applies it to offer mechanics (hooks, guarantees, magnets). It does **not** carry the full "don't write / do write" list or the "the brain remembers what you describe" rationale. That teaching lives **only** in the maintainer's global `~/.claude/CLAUDE.md`.
- **no em dashes:** ships as a *mechanism* (`tools/_content_rules.py` `assert_no_em_dash()`, exit code 3) but not as an explained principle. The rationale is global-CLAUDE.md-only.
- **never-invent-evidence:** genuinely cross-cutting and consistently stated, but fragmented across 8+ method files with no declared owning section.
- **no-vendor-names** (the customer-facing half of reactive-TrustPager): fragmented across banned-framings lists in several files with no single home.

**The one-sentence diagnosis:** rails have a home and mostly get referenced; content-doctrine has no shipped home, so it gets pasted. Vic's private global CLAUDE.md is doing a job the plugin should do.

---

## 2. The load-bearing tension (why NOT pure extraction)

`skills/write-post-copy/SKILL.md` references `communication-voice.md` (line 73) **and still restates** positive-only and no-em-dash in its Hard rules (lines 153-169), with this comment:

> "A field test shipped a quote with an em dash because nothing reminded the model; this is the reminder."

The target runtime is Claude Sonnet on a Pro plan. A rule that is only referenced in another file can be skipped by the model mid-generation, and the failure mode is a rule violation reaching a customer. The author of write-post-copy already discovered this and defended against it by restating. Several other skills (`design-my-site`, `plan-my-ads`, `describe-a-product`) do the same: reference the home AND restate. That is the authors telling us a bare pointer did not feel safe.

**So the design keeps a firing reminder inline for the load-bearing rules, and moves only the teaching and examples to the home.** This is deliberately not the "just reference it" answer.

---

## 3. Recommended architecture

### 3.1 The home: a new `knowledge/content-rules.md`, peer to `communication-voice.md`

Not `communication-voice.md` (it owns operational *message tone*, a different concern; merging bloats a file loaded for a narrower purpose). Not `business-method.md` §18 (it is the *discovery-boundary* owner and the *applications* catalogue; it should point at the rule, not become its home). Not `kernel/runtime/` (that is Python-only, vendor-literal-banned, CI-enforced; behaviour-rich copy policy does not belong there). Plain `knowledge/`, read at runtime via `Read` exactly as 40 skills already read `knowledge/`.

`content-rules.md` owns four things, promoted verbatim from the global CLAUDE.md so clients finally receive them:
1. positive-only: the "don't write / do write" list + the "describe the win" rationale.
2. no em dashes: the rule + rationale + the comma/colon/parentheses substitution recipe.
3. never-invent-evidence: one cross-cutting statement.
4. no-vendor-names: one statement.

Plus a **labelled scope note** (mirroring `communication-voice.md` lines 5-10): these bind customer-facing OUTPUT only; internal/dev/discovery voice is exempt (per the `em-dash-scope` and `pain-language-ok-in-discovery` doctrine), and the discovery-vs-shipped boundary points to `business-method.md` §18/§12.5.

**Draw the §18 line explicitly** or the refactor relocates duplication instead of removing it: `content-rules.md` owns the do/don't *examples and rationale*; §18 keeps the *applications* catalogue (hooks, guarantees, magnets) and links out for the examples.

### 3.2 The mechanism: per-rule ruling on demote vs load-bearing-anchor

| Rule | Ruling | Why |
|---|---|---|
| positive-only | **Anchor + pointer** | Field incident proves a bare reference is unsafe on Sonnet. Keep a firing reminder; move the teaching to the home. |
| no em dashes | **Anchor + pointer** (has a partial mechanical backstop) | Same incident. `_content_rules.py` only catches em dashes at the *write-tool* boundary (docx/xlsx/pdf). Copy that ships as chat text (posts, SMS drafts) never hits that guard, so the inline reminder is doing real work. |
| never-invent-evidence | **Anchor + keep the one domain-specific line** | A fabricated testimonial is unrecoverable. Demote the generic statement; keep the regulatory/high-stakes domain line inline (BAS figures, proof quotes, medical shapes). Blanket demotion is not safe here. |
| no-vendor-names | **Anchor + pointer**, enforced via the existing doctrine-voice gate (see §4) | Vendor leak is a real client-facing failure; keep it firing. |
| safeguards rails | **Demote to reference** (`safeguards.md`) | These fire at the *tool* boundary (a 202 is a 202 regardless of prose). The home exists and works; the fix is to make skills point at it, not paste it. |
| plain language | **Demote to reference** (`communication-voice.md`) | Low-stakes, complementary, already well-referenced. |
| keyless-then-connected | **Demote to reference** (`connectors.md` + `starter-projects.md`) | Structural design property, not a per-line QA rule. |
| discovery arc | **Demote to reference** (`business-method.md` §12.5/§18) | Already the best-homed rule in the pack. |

### 3.3 The standard anchor line (single, greppable, lintable)

For any customer-facing content skill:

```
Customer-facing copy is positive-only and outcome-led, uses no em dashes, invents no
facts/quotes/numbers, and names no third-party vendor. The rules and examples are in
knowledge/content-rules.md. Follow them; do not restate them here.
```

One line, not a paragraph. It keeps the four load-bearing rules firing inline (the Sonnet reminder) while pointing at the home for the teaching (kills the drift surface).

### 3.4 Before / after: `write-post-copy`

**Before** (Hard rules, ~10 lines: positive-only stated twice, no-em-dash stated twice, plus never-invent, no-vendor, plain-language, each inline):

```
- positive/outcome-led... Every word that ships names the win, never the pain.
- Positive-only, outcome-led, always... Not "stop losing leads", but "every enquiry answered same day".
- NO em dashes (use colons, commas, parentheses)... A field test shipped a quote with an em dash.
- No em dashes in the copy. Use a comma, a colon, parentheses, or two sentences.
- No invented proof. Don't put a fake stat or a made-up testimonial into a post.
- No third-party vendor or tool names anywhere a follower would see them.
- Sound like a person. Short sentences. No jargon, no system-internals.
```

**After** (1 anchor + 1 pointer; the skill keeps only genuinely skill-specific craft, e.g. its hook doctrine):

```
- Customer-facing copy is positive-only, no em dashes, invents no facts/quotes, names no
  vendor. Rules + examples: knowledge/content-rules.md. Follow them; don't restate.
- Voice/tone: knowledge/communication-voice.md. Hook doctrine: business-method.md §7.5/§10.6.
```

Net ~10 lines to 2. The "describe the win" example pair and the field-test anecdote move into `content-rules.md` once (where the anecdote belongs, as the reason the rule exists) and every skill inherits it.

---

## 4. Enforcement

Three checks, but two hosts, and a hard prerequisite the first synthesis missed.

**Step 0 prerequisite (blocking): amend `tools/manifest.py` first.** The manifest schema is *closed*. `KNOWN_KEYS` (line 80) is an exhaustive allowlist and `validate_manifest` appends `"unknown key: ..."` (lines 327-328), which `lint-skill.py` treats as **FAIL** (lines 118-119). So writing a new `produces_customer_facing_copy: true` field into any skill **FAILs CI immediately**. The field must be added to a key tuple (`PASSTHROUGH_KEYS` or a new `OPTIONAL_SCALAR_KEYS` entry) in `manifest.py` before any skill carries it. Only then does "WARN so CI stays green" hold.

**Check (i) FAIL on the pasted boilerplate**, added to `lint-skill.py` after the existing `_MCP_TOOL_RE` body scan (line 57 / 121-138 is the exact template; `body` is already in hand at line 100). Fingerprint the phrases that only appear when the doctrine is *restated* rather than linked (the "use a comma, a colon, parentheses" substitution recipe is the highest-signal one). **Honest framing:** this is a denylist of known strings, so it catches copy-paste regressions, not novel paraphrase. A skill that paraphrases the rule slips through. It makes *known* boilerplate lintable, not all restatement.

**Check (ii) require the anchor+pointer** in any skill with `produces_customer_facing_copy: true` that does not contain `knowledge/content-rules.md`. WARN during migration, FAIL once the pack is green.

**The no-vendor-names half belongs in `tools/check-doctrine-voice.py`, not `lint-skill.py`.** That gate already exists and already models exactly this shape: a banned-literal scan across tracked files with allowed-location carve-outs and its own test. Extend its banned list / carve-outs to cover "TrustPager" outside the maintainer-only paths. Do not build a second mechanism.

**Coverage gap to know about:** `tests/test_kernel_vendor_neutral.py` scans **only `kernel/`** for the `trustpager` literal. The drift files below are in `knowledge/` and `skills/`, so they pass CI today. Nothing currently catches a leaked "TrustPager" outside the kernel.

**How this differs from the manifest/registry lint the kernel re-arch plans:** those checks validate the *capability contract* (what a skill declares it can do, which tools/drivers it may call). This validates *output policy* (how emitted copy must behave). Different concern, same file, same `body` string in hand. This is the "voice/comms rules" single owning file the re-arch review's open question explicitly asked for (`bos-rearchitecture-review.md` line 242).

---

## 5. The client-doesn't-have-global-CLAUDE.md fix (highest-value single move)

This is the root cause and the highest-leverage change, and it lands value even before any skill is edited.

Today a client installs the plugin and gets `templates/CLAUDE.md` + `knowledge/*.md` + skill bodies. They receive the *obligation* to obey the content rules (scattered across the restatements) but never the rules' actual teaching or rationale, because that lives on Vic's machine only. That absence is *why* every content skill re-invents its own do/don't list.

The fix is the promotion the anti-drift doctrine already prescribes ("session-memory that has held 2+ weeks gets promoted into the owning repo doc; the repo is the shared contract"):

1. **Lift** the positive-only "don't write / do write" block and the no-em-dash rationale from global `~/.claude/CLAUDE.md` into the shipped `knowledge/content-rules.md`. The global file keeps its copy (it governs Vic's non-BOS work) and adds a labelled note: "the BOS ships its own copy at knowledge/content-rules.md; that is the client-facing home."
2. **Link it from `templates/CLAUDE.md`.** That file already links `communication-voice.md` and `safeguards.md` under "How to draft customer comms" (around lines 100-114). Add one line pointing at `content-rules.md`.
3. **Carry the labelled scope note** in `content-rules.md` (customer-facing output only; internal/dev/discovery exempt; discovery boundary points to §18).

After this, a client's assistant drafting their customer copy reads the doctrine from a file that ships, not from a maintainer machine it never sees.

---

## 6. Migration plan

Sequenced to dovetail with the kernel/driver/app split, low-risk, each step a separate revertible commit.

- **Step 0 (mechanical, prerequisite):** add `produces_customer_facing_copy` to `manifest.py`'s key schema. Without this, everything downstream FAILs CI.
- **Step 1 (mechanical, ~1 hr, no skill edits):** write `knowledge/content-rules.md` by promoting the global-CLAUDE.md doctrine. Add the one-line link to `templates/CLAUDE.md`. This step alone closes the client-gap because `templates/CLAUDE.md` loads every session. Nothing can regress because no skill changed.
- **Step 2 (mechanical):** add lint checks (i)/(ii) to `lint-skill.py` (WARN) and extend `check-doctrine-voice.py` for the vendor literal. Run across all skills to get the baseline offender list.
- **Step 3 (judgement, batched, worst-first):** migrate the content-authoring restaters (write-a-proposal, write-a-policy, the youtube trio, build-brand-strategy, write-post-copy, ...). Replace pasted do/don't blocks with the anchor+pointer, keeping skill-specific craft. **Do not delete labelled exceptions** (e.g. write-a-letter's "firm about the facts, positive about the destination" carve-out); they stay and cite the scope note instead of re-explaining it.
- **Step 4 (judgement):** the safeguards restaters (make-it-happen, run-my-ads, the radars, the build-* skills). Replace inline 202/destructive-write prose with `safeguards.md` section pointers. Leave genuinely load-bearing domain safety gates inline (run-my-ads spend ceiling, estimate-my-bas never-lodge).
- **Step 5 (mechanical):** flip check (ii) to FAIL once the pack is green. Drift cannot re-enter.
- **Step 6:** fold into the re-arch's de-branding / `about.md` pass so knowledge homes land as one coherent change.

**Rollback:** Step 1 is purely additive (new file + one link line); reverting is a one-file delete. Steps 3/4 are per-skill; `git checkout -- skills/<name>/SKILL.md` restores the inline version instantly and the home stays. No step touches the kernel or any Python runtime, so no capability contract is at risk.

---

## 7. Risks and open decisions for Vic

**D1 (scope, blocking) - the three TrustPager-branded content files.** These hardcode "TrustPager" as the product and require the vendor name verbatim in customer-facing examples, the opposite of the no-vendor rule. Verified file list (corrected from the first synthesis, which wrongly named `make-social-post` - that file is clean and correctly enforces the rule):
- `knowledge/platform-guide.md` (~34 hits) - a FinalPiece/TrustPager-internal support artifact.
- `knowledge/youtube-thumbnail-method.md` (~9 hits).
- `skills/make-thumbnail/SKILL.md` line 108 (`"headline": "Forms That Auto-Fill Your CRM"`) - a leftover; the skill already carries a "supersedes the earlier TrustPager-tutorial framing" note, so it is half-genericised.

Decision needed: segregate these as maintainer-only (not shipped to generic clients), or genericise to the owner's brand as the flip-set work already started? Until you rule, do NOT migrate these in the same batch as the client floor skills, and the vendor-name lint would falsely flag them.

**D2 - is one anchor sentence a strong enough Sonnet reminder?** Today some skills belt-and-braces the em-dash rule twice. The design bets that one clear anchor + the `_content_rules.py` write-guard backstop is enough for the docx/xlsx/pdf paths. I am less confident for chat-text output (posts, ad hooks, SMS drafts), which never hits the write-guard. If after migration any author re-adds prose, treat that as signal the anchor is too weak, not as a lint nuisance.

**D3 - the chat-text em-dash gap (follow-up, out of scope for this layer).** `_content_rules.py` guards only written files. Several skills that produce customer-facing *chat* drafts (follow-up-radar, lead-triage, missed-call-recovery, run-my-ads' checklist) state the em-dash rule *zero times today* and bypass the guard entirely. The migration should *add* the anchor to these gap skills, not just dedupe the restaters, which makes the layer a net coverage gain. Optionally, extend a text-level em-dash guard to the chat path later.

**D4 - the scorecard is directional, not measured.** The audit produced per-rule counts (roughly: positive-only restated in ~24 skills, never-invent in ~34, safeguards in ~30, ~560 lines / 7-9k tokens pack-wide). A verifier cross-checked against live grep and found the counts are estimates, not a committed measurement: em-dash is *mentioned* in ~39 skill files and never-invent language in ~51, so some rows are likely under-counted, while safeguards may be over-counted. **The architecture does not depend on the exact numbers** (every file-level claim held up), but per your own anti-drift doctrine ("no live counts in prose, they rot"), regenerate a committed audit and recompute the table before quoting any number as fact.

---

## Appendix: what the adversarial verifiers corrected in the first synthesis

Kept for transparency; all corrections are folded into the body above.

1. **The `produces_customer_facing_copy` field is a blocking prerequisite** (closed manifest schema), not a free add. The original "WARN so CI stays green" sequencing was wrong until `manifest.py` is amended. **Confirmed in repo.**
2. **`check-doctrine-voice.py` already exists** as the vendor-name enforcement precedent; the original proposed building it fresh in `lint-skill.py`. **Confirmed in repo.**
3. **`make-social-post` is clean** (0 TrustPager hits) and was wrongly listed as a drift file; the real strongest offenders are `platform-guide.md`, `youtube-thumbnail-method.md`, and `make-thumbnail/SKILL.md:108`. **Confirmed in repo.**
4. **`test_kernel_vendor_neutral.py` only scans `kernel/`**, so the `knowledge/`+`skills/` drift passes CI today.
5. **§18 carries an applications catalogue**, not just a thin bridge; `content-rules.md` must own examples+rationale while §18 keeps applications, or the refactor relocates duplication.
6. **The lint is a denylist** (catches copy-paste, not paraphrase); framing it as making "drift a lintable property" overstates it.
7. **The scorecard is estimate, not measurement** (raw audit truncated; grep contradicts several rows). Regenerate before citing.
