# Content-Doctrine Layer Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Strip FinalPiece's positive-only house rule out of the client-facing BOS (clients choose their own marketing psychology), and consolidate the rules that DO stay for clients (no em dashes, never invent evidence, no vendor leak, plain-language) into one shipped home plus a single inline anchor.

**Architecture:** Two moves in one skill-editing pass. (1) REMOVE every positive-only / outcome-led restatement from the client pack; positive-only lives only in FinalPiece's own settings, never shipped. (2) Create `knowledge/content-rules.md` as the shipped home for the rules that stay, and replace their scattered restatements with one anchor line + pointer. The em-dash mechanical guard is unchanged. A denylist lint (added last) bans the pasted boilerplate, requires the anchor, and guards against positive-only creeping back into the client pack. The BOS already writes in the client's own voice (`build-my-voice`, `build-brand-strategy`); this removes the house-style override sitting on top of it.

**Tech Stack:** Python 3 (`tools/manifest.py`, `tools/lint-skill.py`), `unittest` suite (`python -m unittest tests.<name>`), Markdown knowledge read at runtime via `Read`. No hooks, no new runtime capability. Target runtime model: Claude Sonnet (Pro).

**Design doc (the spec):** [`docs/architecture/content-doctrine-layer.md`](../content-doctrine-layer.md) — read its SCOPE UPDATE banner first; this plan executes the corrected scope.

---

## The rule split (the whole plan hinges on this)

| Rule | Client-facing BOS? | Home / mechanism |
|---|---|---|
| **positive-only / outcome-led** | **STRIP.** FinalPiece house style, not a client rule. Clients pick their own psychology. | Stays only in `~/.claude/CLAUDE.md` + `settings/recommended-global-claude.md`. Never shipped. |
| **no em dashes** | **KEEP** (strong, on any output — the AI-writing tell). | `content-rules.md` + anchor. Existing guard `tools/_content_rules.py` unchanged. |
| **never invent evidence** | **KEEP** (integrity / fraud protection for the client). | `content-rules.md` + anchor. |
| **no third-party vendor leak** | **KEEP** (do not inject our stack into their copy; they may name their own vendors). | `content-rules.md` + anchor. |
| **plain-language service voice** | **KEEP** as guidance. | Already homed in `communication-voice.md`; content-rules.md cross-links it. |

---

## CRITICAL: execution order and the CI constraint

**CI runs `set -e; for d in skills/*/; do python tools/lint-skill.py "$d"; done`** (`.github/workflows/test.yml:50-55`). `lint-skill.py main()` returns exit **1 on WARN** and **2 on FAIL**, and `set -e` aborts the job on **any** non-zero exit.

> **The enforcing lint must land LAST, only after every skill it would flag is already clean.** There is no safe "WARN during migration" window: a WARN (exit 1) fails CI exactly like a FAIL. Adding the check before the skills are migrated turns CI red for the whole window.

Three PR-sized groups, each independently green:

- **PR 1 (Tasks 0-3): additive foundation.** manifest key, the home file, the client-template link, and confirming positive-only stays FinalPiece-only. No lint change, no skill edit.
- **PR 2 (Tasks 4-6): the skill + method pass.** Strip positive-only AND swap the kept-rule restatements for the anchor, in one edit per skill; reframe the method files and §18; point the rail restaters at `safeguards.md`. Still no new lint, so CI stays green.
- **PR 3 (Task 7): land the enforcing lint at FAIL,** only after a local dry-run confirms the pack is clean.

(Alternative if you want to enforce sooner: change the CI loop to tolerate WARN with `|| test $? -eq 1` — the repo already uses `|| test $? -eq 2` at line 72. That is a CI-policy change and is Vic's call; this plan does not assume it.)

---

## The standard anchor line (canonical, greppable) — note: NO positive-only

Every customer-facing content skill carries exactly this, once, at its output gate:

```
Customer-facing copy uses no em dashes, invents no facts, quotes, or numbers, and names
no third-party vendor. Write it in the owner's brand voice; the framing and marketing
psychology are the owner's choice. The rules are in knowledge/content-rules.md.
```

The clause "the framing and marketing psychology are the owner's choice" is deliberate: it is what stops a client's assistant from arguing positive-only at them.

---

## Design decisions locked

- **Home = a NEW `knowledge/content-rules.md`**, peer to `communication-voice.md`. It holds no-em-dash + never-invent + no-vendor, and cross-links communication-voice.md for plain-language. It does NOT contain positive-only.
- **positive-only is removed, not relocated into the pack.** It already lives in the two FinalPiece settings files; those keep it. The pack ships without it.
- **`business-method.md` §18 gets reframed, not deleted.** Today it reconciles the diagnostic doctrine with a "customer-facing copy is outcome-led, never pain-led" hard rule. That hard rule is FinalPiece-only now, so §18 becomes: pain is a diagnostic and discovery input; how the owner frames their shipped copy is the owner's choice. The discovery-arc content (§12.5) is unaffected.
- **`produces_customer_facing_copy`** goes in `PASSTHROUGH_KEYS` (allowed, not manifest-validated; lint owns it). Verified it needs no enum domain or generator default.
- **The em-dash guard `tools/_content_rules.py` is untouched.** no-em-dash stays; the guard is its enforcement on the docx/xlsx/pdf write path.

---

## File structure

| File | Change | Responsibility |
|---|---|---|
| `knowledge/content-rules.md` | **Create** (PR1) | Shipped home: no-em-dash + never-invent + no-vendor + plain-language pointer + "framing is the owner's choice" note. |
| `tools/manifest.py` | Modify line 77 (PR1) | Add `produces_customer_facing_copy` to `PASSTHROUGH_KEYS`. |
| `templates/CLAUDE.md` | Modify ~line 100-114 (PR1) | One line pointing client assistants at `content-rules.md` (no positive-only mention). |
| `settings/recommended-global-claude.md` | Modify (PR1) | Note that positive-only is FinalPiece-only and intentionally NOT in the shipped pack. |
| `skills/<content skills>/SKILL.md` | Modify (PR2) | Remove positive-only; swap kept-rule restatements for the anchor; add the flag. |
| `knowledge/<method files>.md`, `business-method.md` §18, `starter-projects.md` | Modify (PR2) | Drop the positive-only half of boilerplate tails; reframe §18; keep em-dash half. |
| `skills/<rail restaters>/SKILL.md` | Modify (PR2) | Replace inline rails with `safeguards.md` pointers. |
| `tools/lint-skill.py` | Modify after line 138 (PR3) | Three FAIL checks: pasted kept-rule boilerplate, missing anchor, positive-only regression. |
| `tests/test_lint_content_doctrine.py` | **Create** (PR3) | Tests for the three lint checks. |
| `tests/test_content_rules_home.py` | **Create** (PR1) | Home exists, is em-dash-clean, has no positive-only, template links it. |

---

# PR 1 — Additive foundation (every commit green)

## Task 0: Allow the `produces_customer_facing_copy` frontmatter key

**Why first:** the manifest schema is closed. `validate_manifest` FAILs on any unknown key (`manifest.py:328`); `lint-skill.py` turns that into a FAIL. Adding the key to a skill before this lands bricks CI.

**Files:** Modify `tools/manifest.py:77`; test in `tests/test_lint_manifest.py`.

- [ ] **Step 1: Failing test** — add to `tests/test_lint_manifest.py`:

```python
class TestCustomerFacingCopyKeyAllowed(unittest.TestCase):
    def test_produces_customer_facing_copy_is_a_known_key(self):
        fm = _VALID_FLOOR_FM + "produces_customer_facing_copy: true\n"
        with tempfile.TemporaryDirectory() as tmp:
            d = _write_skill(Path(tmp), fm)
            issues = lint_skill.lint_skill(d)
            self.assertFalse(any("unknown key" in m for _, m in issues), issues)
```

- [ ] **Step 2: Run, verify FAIL** — `python -m unittest tests.test_lint_manifest.TestCustomerFacingCopyKeyAllowed -v` (unknown key).
- [ ] **Step 3: Add the key** — `tools/manifest.py:77`:

```python
PASSTHROUGH_KEYS: tuple[str, ...] = (
    "name", "description", "triggers", "produces_customer_facing_copy",
)
```

- [ ] **Step 4: Run, verify PASS** — same command.
- [ ] **Step 5: Suite** — `python -m unittest tests.test_lint_manifest tests.test_manifest -v` (all PASS).
- [ ] **Step 6: Commit** — `git commit -m "feat(manifest): allow produces_customer_facing_copy passthrough key"`

---

## Task 1: Create the home `knowledge/content-rules.md` (kept rules only)

**Files:** Create `knowledge/content-rules.md`. Additive.

- [ ] **Step 1: Write the file exactly** (zero em dashes; it is the em-dash rule's home; no positive-only anywhere):

```markdown
# Content rules

**The small set of quality and integrity guardrails for any copy this system generates
that a customer or end-user will read or hear.** Emails, SMS, captions, ad copy, web
copy, headlines, scripts, proposals, letters. One home: every content skill points here
instead of restating it.

**Whose voice:** the copy is written in the OWNER's brand voice (see build-my-voice and
build-brand-strategy). These rules are universal quality and integrity guardrails, not a
house style. The framing and the marketing psychology are the owner's choice.

**Scope (labelled boundary):** these rules bind customer-facing OUTPUT only. Internal
worksheets, operator coaching, discovery conversations, and dev notes are exempt.

## 1. No em dashes
Never use an em dash in customer-facing copy. Em dashes read as machine-written and are
one of the clearest tells of AI-generated text, which weakens the copy. Break the thought
into separate sentences, or use a comma, a colon, or parentheses. Hyphens in compound
words are fine; the ban is the em dash used as a sentence connector.

## 2. Never invent evidence
Never fabricate a number, statistic, testimonial, customer quote, or metric. Use only real
figures the owner supplied and real customer words. A missing number is a finding, not a
gap to fill with a plausible one. Where the stakes are regulatory (tax, financial,
medical), a made-up figure is never acceptable.

## 3. No third-party vendor leak
Do not inject the tools or platforms behind the work (the CRM, the ad platform, the site
host) into the owner's customer-facing copy unprompted. The copy is the owner's brand. The
owner naming vendors THEY choose is their call; this rule is about not leaking our stack
into their output.

## Service-message voice
For the owner's operational messages to their own customers (fix confirmations, updates),
keep it plain, warm, and clear: see knowledge/communication-voice.md.

## Marketing framing is the owner's choice
How the owner frames their marketing (positive, pain-led, or any psychology they choose)
is the owner's decision. This system writes in the owner's voice and does not impose a
house style on their copy.
```

- [ ] **Step 2: Verify no em dash** — `python -c "import pathlib,sys; t=pathlib.Path('knowledge/content-rules.md').read_text(encoding='utf-8'); sys.exit(1 if chr(8212) in t else 0)"` (exit 0).
- [ ] **Step 3: Commit** — `git commit -m "feat(knowledge): add content-rules.md (kept client rules; no positive-only)"`

---

## Task 2: Wire the home into the client front door (`templates/CLAUDE.md`)

**Files:** Modify `templates/CLAUDE.md` (the "How to draft customer comms" block, ~line 100-114); create `tests/test_content_rules_home.py`.

- [ ] **Step 1: Failing test** — create `tests/test_content_rules_home.py`:

```python
"""The content-doctrine home ships, carries no positive-only, and is linked.

Run:  python -m unittest tests.test_content_rules_home
"""
import pathlib
import unittest

REPO = pathlib.Path(__file__).resolve().parent.parent
HOME = REPO / "knowledge" / "content-rules.md"


class TestContentRulesHome(unittest.TestCase):
    def test_home_exists(self):
        self.assertTrue(HOME.exists())

    def test_home_has_no_em_dash(self):
        self.assertNotIn(chr(8212), HOME.read_text(encoding="utf-8"))

    def test_home_does_not_impose_positive_only(self):
        # The client home must not carry FinalPiece's positive-only house rule as a mandate.
        t = HOME.read_text(encoding="utf-8").lower()
        self.assertNotIn("positive-only rule", t)
        self.assertNotIn("never pain-led", t)

    def test_client_template_points_at_the_home(self):
        t = (REPO / "templates" / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("content-rules.md", t)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run, verify the template test FAILS** — `python -m unittest tests.test_content_rules_home -v`.
- [ ] **Step 3: Add the pointer** — in `templates/CLAUDE.md`, next to the `communication-voice.md` / `safeguards.md` links:

```markdown
- The quality guardrails for any content I generate that a customer will read (no em
  dashes, never invent facts or quotes, no third-party vendor names) are in
  `knowledge/content-rules.md`. I write in the owner's brand voice; their marketing
  framing is their choice, I do not impose a house style.
```

- [ ] **Step 4: Run, verify PASS** — same command.
- [ ] **Step 5: Commit** — `git commit -m "feat(templates): point client assistants at content-rules.md"`

**After Task 2 the kept rules have a shipped home and the client front door is honest about not imposing a framing. Natural first PR / safe stopping point.**

---

## Task 3: Remove positive-only from the client-facing global template

**Files:** `settings/recommended-global-claude.md` (tracked, CLIENT-facing — installed into the client's global config by `tools/setup_claude_config.py`).

Corrected understanding: that file already offered positive-only and no-em-dash as OPTIONAL, off-by-default "house style" recommendations. Per the founder ruling, positive-only should not be offered to clients at all (it is FinalPiece-only; its homes are OUTSIDE this repo — the maintainer's personal global CLAUDE.md and the FinalPiece marketing skills). no-em-dash stays.

- [x] **Step 1:** Removed the "Optional: Positive-only copy" block; reframed the section so marketing framing is explicitly the owner's choice; kept the "Optional: No em dashes" block.
- [x] **Step 2:** Did NOT touch `~/.claude/CLAUDE.md` (the maintainer's personal file already holds positive-only for FinalPiece's own work; no repo action needed, and the pack must not carry it).
- [x] **Step 3:** Verified full suite (399 tests) + all CI gates green after the change; committed with PR 1.

---

# PR 2 — The skill + method pass (strip positive-only AND consolidate kept rules)

## Task 4: Migrate the content-authoring skills

**Seeded by the audit's per-skill classification, NOT by a grep.** The lint does not exist yet in PR2. Use the design-doc audit to find every skill that (a) restates positive-only or (b) restates a kept rule.

**Method (repeatable per skill; parallelisable via subagent-driven-development, one skill per subagent).**

**Worst-first order (from the audit):** `write-a-proposal`, `write-a-policy`, `write-post-copy`, `build-brand-strategy`, `plan-my-youtube`, `research-my-channel`, `script-my-video`, `package-my-video`, `make-social-post`, `describe-a-product`, `write-a-letter`, `write-a-job-ad`, `plan-my-ads`, `run-my-ads` (copy sections only), `design-my-site`, `launch-my-site`, `get-found-online`, `build-my-proof`, `build-social-strategy`, `build-customer-voice`, `plan-my-content`, `research-a-competitor`, `quote-from-photo`, then any remaining customer-facing skill the audit flags.

**Per-skill steps (one coordinated edit):**

- [ ] **Step 1:** Add `produces_customer_facing_copy: true` to the frontmatter AND insert the standard anchor line (no positive-only) at the output gate, in the same edit.
- [ ] **Step 2: REMOVE all positive-only / outcome-led restatements.** Delete lines like "positive-only, outcome-led, always", "names the win, never the pain", "❌ don't write pain-led". Do NOT replace them with anything: framing is now the owner's choice. Preserve any genuinely useful, brand-neutral copy craft, just not framed as a positive-only mandate.
- [ ] **Step 3: Remove the kept-rule restatements** (no-em-dash, never-invent, no-vendor, plain-language) since the anchor + `content-rules.md` now carry them. **Keep load-bearing domain nuance inline** where stakes are regulatory (e.g. `estimate-my-bas` "a made-up figure on a tax form is never acceptable" stays, citing content-rules.md rule 2).
- [ ] **Step 4:** Add the voice/craft pointers the skill needs (`communication-voice.md`, `business-method.md` sections other than the old positive-only mandate).
- [ ] **Step 5:** `python tools/lint-skill.py skills/<name>` (exit 0 — no new checks yet; confirms frontmatter still valid). `python tools/test-skill.py <name>` if it has a fixture.
- [ ] **Step 6:** Commit per batch (3-5 skills): `git commit -m "refactor(<names>): drop positive-only house rule; kept rules to content-rules.md anchor"`

**Also add the anchor to the audit's gap skills that emit customer-facing chat drafts and state no rule today:** `follow-up-radar`, `lead-triage`, `missed-call-recovery`, `draft-reply`, `send-email`, `prep-for-call`. Net coverage gain for the KEPT rules (no em dashes especially, which bypasses the write-tool guard on chat text).

---

## Task 5: Reframe the method files and business-method.md §18

**Files:** the `knowledge/*-method.md` files carrying the positive-only boilerplate tail (per the audit: `web-design-method.md`, `seo-method.md`, `proof-and-referrals-method.md`, `research-method.md`, `youtube-packaging-method.md`, `youtube-script-method.md`, `social-post-method.md`), plus `business-method.md` §18 and `starter-projects.md`.

- [ ] **Step 1: Rewrite each combined boilerplate tail** to drop the positive-only half and keep the em-dash half, pointing at the home. Example, change:
  > "Everything the owner reads follows the positive-only rule and uses no em dashes (use commas, colons, parentheses)."
  to:
  > "Customer-facing output follows knowledge/content-rules.md (no em dashes, no invented evidence, no vendor leak). The owner's marketing framing is their own choice."
- [ ] **Step 2: Remove the per-section positive-only mandates** in `web-design-method.md` (the "Copy guidance (positive-only)" x7) and the "banned: negative / fear-led framing" lines in `social-post-method.md`, `youtube-*-method.md`. Keep any genuinely useful, brand-neutral copy craft as optional guidance; delete the positive-only requirement.
- [ ] **Step 3: Reframe `business-method.md` §18.** Keep "pain is a diagnostic input and a discovery-conversation tool". Remove the client mandate "the BOS ships a hard rule: customer-facing copy is outcome-led, never pain-led". Replace with: how the owner frames their shipped copy (positive, pain-led, whatever psychology) is the owner's choice; the diagnostic use of pain in analysis and discovery is unchanged. Update the §18 heading if it still says "coexists with positive-only copy".
- [ ] **Step 4:** Remove positive-only notes from `starter-projects.md` (the "Note for builders" + Planned note).
- [ ] **Step 5:** Run the doc-dependency tests: `python -m unittest tests.test_doc_deps tests.test_doc_lib_set -v` (adjust any that asserted the old boilerplate). Commit per file or small batch.

---

## Task 6: Point the safeguards restaters at `safeguards.md`

**Files:** `make-it-happen` (the `## Hard-block destructive operations` + `## Approval queue (HTTP 202)` sections, zero links today), `run-my-ads`, `sweep-my-day`, the radar skills, and build-* skills that restate write rails.

- [ ] **Step 1:** Replace inline 202 / destructive-write / verify-before-customer prose with a `safeguards.md` pointer.
- [ ] **Step 2:** Leave load-bearing domain safety gates inline (`run-my-ads` spend ceiling, `estimate-my-bas` never-auto-lodge).
- [ ] **Step 3:** `python tools/lint-skill.py skills/<name>` (exit 0) + fixture test; commit per batch.

---

# PR 3 — Land the enforcing lint LAST (at FAIL, once the pack is clean)

## Task 7: Add the three content-doctrine lint checks

**Files:** Modify `tools/lint-skill.py` (pattern near line 57; checks after line 138, inside the `else:` where `fm` and `body` are in scope); create `tests/test_lint_content_doctrine.py`.

**Do NOT start until Tasks 4-6 are merged.** Step 1 is a dry-run that must come back clean.

- [ ] **Step 1: Dry-run gate** — implement on a branch, then run the CI-equivalent loop:

Run (bash): `set +e; for d in skills/*/; do python tools/lint-skill.py "$d" >/dev/null 2>&1 || echo "TRIPS: $d"; done`
Expected: **no `TRIPS:` output.** Any skill that trips was missed in PR2 — fix it here before proceeding.

- [ ] **Step 2: Write the tests** — create `tests/test_lint_content_doctrine.py`:

```python
"""Content-doctrine lint checks in tools/lint-skill.py.

  (i)   pasted KEPT-rule boilerplate (em-dash / never-invent / vendor) -> FAIL.
  (ii)  produces_customer_facing_copy without the content-rules.md pointer -> FAIL.
  (iii) positive-only ENFORCEMENT language in a client skill -> FAIL (it is FinalPiece-only).

Run:  python -m unittest tests.test_lint_content_doctrine
"""
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
_spec = importlib.util.spec_from_file_location("lint_skill", REPO / "tools" / "lint-skill.py")
lint_skill = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lint_skill)

_FLOOR_FM = """\
name: Synth Content
description: A synthetic content skill for tests.
triggers:
  - write the synthetic thing
  - draft synth copy
  - make synth content
function_slot: floor
requires_driver: none
requires_credential: none
data_path: reasoning_only
status: active
"""
_CF_FM = _FLOOR_FM + "produces_customer_facing_copy: true\n"
_ANCHOR = ("Customer-facing copy uses no em dashes, invents no facts, quotes, or numbers, "
           "and names no third-party vendor. The rules are in knowledge/content-rules.md.")


def _write(root, fm, body):
    d = root / "synth-skill"
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(f"---\n{fm}---\n{body}", encoding="utf-8")
    return d


def _sev(issues):
    return [s for s, _ in issues]


class TestKeptRuleBoilerplateFails(unittest.TestCase):
    def test_em_dash_substitution_recipe_paste_fails(self):
        for body in ["\n# S\n\nuse a comma, a colon, parentheses.\n",
                     "\n# S\n\nuse commas, colons, parentheses.\n"]:
            with tempfile.TemporaryDirectory() as tmp:
                d = _write(Path(tmp), _CF_FM, body)
                self.assertIn("FAIL", _sev(lint_skill.lint_skill(d)), body)


class TestAnchorRequiredFails(unittest.TestCase):
    def test_customer_facing_without_pointer_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = _write(Path(tmp), _CF_FM, "\n# S\n\nWrite a caption.\n")
            self.assertTrue(any(s == "FAIL" and "content-rules.md" in m
                                for s, m in lint_skill.lint_skill(d)))

    def test_customer_facing_with_anchor_is_clean(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = _write(Path(tmp), _CF_FM, f"\n# S\n\n{_ANCHOR}\n")
            self.assertNotIn("FAIL", _sev(lint_skill.lint_skill(d)))

    def test_non_customer_facing_not_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = _write(Path(tmp), _FLOOR_FM, "\n# S\n\nInternal ops.\n")
            self.assertFalse(any("content-rules.md" in m for _, m in lint_skill.lint_skill(d)))


class TestPositiveOnlyRegressionFails(unittest.TestCase):
    """positive-only is FinalPiece-only; it must not re-enter a client skill body."""
    def test_positive_only_mandate_fails(self):
        for body in ["\n# S\n\nCopy must be positive-only, outcome-led.\n",
                     "\n# S\n\nName the win, never the pain.\n",
                     "\n# S\n\nNever define value by absence.\n"]:
            with tempfile.TemporaryDirectory() as tmp:
                d = _write(Path(tmp), _CF_FM, body)
                self.assertIn("FAIL", _sev(lint_skill.lint_skill(d)), body)

    def test_owner_choice_language_is_clean(self):
        # Saying the framing is the owner's choice must NOT trip the guard.
        body = f"\n# S\n\n{_ANCHOR}\nThe marketing psychology is the owner's choice.\n"
        with tempfile.TemporaryDirectory() as tmp:
            d = _write(Path(tmp), _CF_FM, body)
            self.assertNotIn("FAIL", _sev(lint_skill.lint_skill(d)))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run, verify FAIL** — `python -m unittest tests.test_lint_content_doctrine -v`.
- [ ] **Step 4: Implement** — in `tools/lint-skill.py`, add near line 57:

```python
# Content-doctrine fingerprints. See docs/architecture/content-doctrine-layer.md.
# KEPT-rule boilerplate (em-dash substitution recipe, singular AND plural) that belongs
# in knowledge/content-rules.md, not restated inline. Denylist of KNOWN boilerplate:
# catches copy-paste regressions, not novel paraphrase.
_KEPT_RULE_PASTE_RE = re.compile(
    r"use (?:a )?comma[s]?,?\s*(?:a )?colon[s]?,?\s*(?:or )?parentheses",
    re.IGNORECASE,
)
# positive-only ENFORCEMENT language. positive-only is FinalPiece-only; it must not ship
# in a client skill. Precise mandate phrasings only, so ordinary prose does not trip.
_POSITIVE_ONLY_RE = re.compile(
    r"positive[- ]only|outcome-led, always|names the win, never the pain|"
    r"never define value by absence|never pain-led",
    re.IGNORECASE,
)
_CONTENT_RULES_HOME = "knowledge/content-rules.md"
```

Then insert after the undeclared-`mcp__`-tool loop (after line 138, inside `else:`, 12-space indent):

```python
            # KEPT-rule boilerplate belongs in the home, not inline.
            if _KEPT_RULE_PASTE_RE.search(body):
                issues.append((
                    "FAIL",
                    f"SKILL.md restates content-rule boilerplate that lives in "
                    f"{_CONTENT_RULES_HOME} — replace it with the standard anchor + pointer",
                ))
            # A customer-facing skill must point at the home.
            if fm.get("produces_customer_facing_copy") and _CONTENT_RULES_HOME not in body:
                issues.append((
                    "FAIL",
                    f"skill declares produces_customer_facing_copy but does not "
                    f"reference {_CONTENT_RULES_HOME} — add the standard anchor line",
                ))
            # positive-only is FinalPiece-only; it must not re-enter a client skill.
            if _POSITIVE_ONLY_RE.search(body):
                issues.append((
                    "FAIL",
                    "SKILL.md enforces positive-only framing — that is FinalPiece house "
                    "style, not a client rule. Remove it; the owner chooses their framing.",
                ))
```

- [ ] **Step 5: Run unit tests, verify PASS** — `python -m unittest tests.test_lint_content_doctrine -v`.
- [ ] **Step 6: Full CI-equivalent green gate before committing:**

Run: `python -m unittest discover -s tests -v`
Run (bash): `set -e; for d in skills/*/; do python tools/lint-skill.py "$d"; done && echo ALL_GREEN`
Expected: `ALL_GREEN`. If it aborts, a skill still trips a check — fix it here.

- [ ] **Step 7: Commit** — `git commit -m "feat(lint): enforce content-rules anchor, ban kept-rule boilerplate + positive-only regression (FAIL)"`

Now drift cannot re-enter: pasted boilerplate, a missing anchor, OR a positive-only mandate creeping into a client skill all fail CI.

---

## GATED FOLLOW-UP (not in the launch path): vendor-file segregation

**Blocked on Vic's confirmation.** The three TrustPager-branded files (`knowledge/platform-guide.md`, `knowledge/youtube-thumbnail-method.md`, `skills/make-thumbnail:108`) hardcode the vendor name in client-shipped content. D1 decision was "segregate as maintainer-only." This is separate because it reverses just-shipped YouTube-studio work and "maintainer-only" has no mechanism until the registry layer exists (`bos-rearchitecture-review.md` P0/P1). The anchor's no-vendor-leak reminder is the live control until then.

---

## Risks

- **R1 (Sonnet missed read):** mitigated by design (kept rules keep an inline anchor). If a migrated skill re-adds prose, that is signal the anchor is too weak, not a lint nuisance.
- **R2 (chat-text em-dash gap):** `_content_rules.py` guards only the docx/xlsx/pdf write path. Task 4 adds the anchor to the chat-draft gap skills, a net coverage gain for no-em-dash.
- **R3 (denylist, not structural):** the boilerplate and positive-only checks catch known phrasings, not every paraphrase. Acceptable; the anchor-required FAIL is the structural half. The migration set is audit-seeded, not regex-seeded.
- **R4 (positive-only regex false-positive):** `_POSITIVE_ONLY_RE` matches mandate phrasings, but "positive" appears in ordinary prose. The test `test_owner_choice_language_is_clean` guards the common safe case; tune the regex if a legitimate skill trips it (prefer narrowing over dropping the check).
- **Rollback:** every task is a separate commit. Tasks 0-2 are additive. Tasks 4-6 are per-file; `git checkout -- <path>` restores the prior version and the home stays. No task touches the kernel or any runtime.

---

## Execution notes

- **PR 1 (Tasks 0-3)** is mechanical and additive: the home, the link, the FinalPiece-only boundary. Ship first.
- **PR 2 (Tasks 4-6)** is the bulk and ideal for subagent-driven-development: one skill/file per subagent, batch-commit, in a worktree. No new lint yet, so CI stays green.
- **PR 3 (Task 7)** lands the enforcing lint only after PR 2 merges and the local dry-run is clean.
- Regenerate a committed skill-by-skill audit before quoting any duplication count as fact (anti-drift "no live counts in prose"); the design doc scorecard is directional.
```
