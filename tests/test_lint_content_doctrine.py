"""Content-doctrine lint checks in tools/lint-skill.py (flag-gated).

The three checks fire ONLY on skills flagged produces_customer_facing_copy (the
client's published marketing). The assistant's own voice and operator-facing
analysis are intentionally exempt (founder ruling: "client marketing only").

  (i)   flagged skill missing the content-rules.md anchor -> FAIL
  (ii)  flagged skill enforcing positive-only framing -> FAIL
  (iii) flagged skill pasting the em-dash-recipe boilerplate -> FAIL
  (iv)  UNflagged skill with positive-only framing -> clean (assistant voice / operator)

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
           "and names no third-party vendor. Write it in the owner's brand voice; the framing "
           "and marketing psychology are the owner's choice. The rules are in knowledge/content-rules.md.")


def _write(root, fm, body):
    d = root / "synth-skill"
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(f"---\n{fm}---\n{body}", encoding="utf-8")
    return d


def _sev(issues):
    return [s for s, _ in issues]


class TestFlaggedSkillIsPoliced(unittest.TestCase):
    def test_missing_anchor_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = _write(Path(tmp), _CF_FM, "\n# S\n\nWrite a caption.\n")
            self.assertTrue(any(s == "FAIL" and "content-rules.md" in m
                                for s, m in lint_skill.lint_skill(d)))

    def test_positive_only_mandate_fails(self):
        for body in [f"\n# S\n\n{_ANCHOR}\nCopy must be positive-only.\n",
                     f"\n# S\n\n{_ANCHOR}\nName the win, never the pain.\n"]:
            with tempfile.TemporaryDirectory() as tmp:
                d = _write(Path(tmp), _CF_FM, body)
                self.assertIn("FAIL", _sev(lint_skill.lint_skill(d)), body)

    def test_em_dash_recipe_paste_fails(self):
        for body in [f"\n# S\n\n{_ANCHOR}\nNo em dashes: use a comma, a colon, parentheses.\n",
                     f"\n# S\n\n{_ANCHOR}\nuse commas, colons, parentheses.\n"]:
            with tempfile.TemporaryDirectory() as tmp:
                d = _write(Path(tmp), _CF_FM, body)
                self.assertIn("FAIL", _sev(lint_skill.lint_skill(d)), body)

    def test_flagged_with_clean_anchor_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = _write(Path(tmp), _CF_FM, f"\n# S\n\n{_ANCHOR}\nThe marketing angle is the owner's call.\n")
            self.assertNotIn("FAIL", _sev(lint_skill.lint_skill(d)), lint_skill.lint_skill(d))


class TestContentSkillContract(unittest.TestCase):
    """The two-half contract in knowledge/content-rules.md.

    voice half: a customer-facing skill names its voice source inline (WARN, because
    which register applies is the author's judgement). attention half: a skill that
    declares engagement_copy routes storytelling-method.md (FAIL, opt-in by flag).
    """

    def _msgs(self, issues):
        return " ".join(m for _, m in issues)

    def test_flagged_without_voice_source_warns(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = _write(Path(tmp), _CF_FM, f"\n# S\n\n{_ANCHOR}\n")
            issues = lint_skill.lint_skill(d)
            self.assertTrue(any(s == "WARN" and "no voice source" in m for s, m in issues), issues)
            self.assertNotIn("FAIL", _sev(issues), issues)

    def test_marketing_voice_source_satisfies_it(self):
        body = f"\n# S\n\n{_ANCHOR}\nVoice: `marketing-strategy/<BrandName>/voice.md`.\n"
        with tempfile.TemporaryDirectory() as tmp:
            d = _write(Path(tmp), _CF_FM, body)
            self.assertNotIn("no voice source", self._msgs(lint_skill.lint_skill(d)))

    def test_service_register_also_satisfies_it(self):
        body = f"\n# S\n\n{_ANCHOR}\nRegister: knowledge/communication-voice.md.\n"
        with tempfile.TemporaryDirectory() as tmp:
            d = _write(Path(tmp), _CF_FM, body)
            self.assertNotIn("no voice source", self._msgs(lint_skill.lint_skill(d)))

    def test_unflagged_skill_needs_no_voice_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = _write(Path(tmp), _FLOOR_FM, "\n# S\n\nSummarise the week.\n")
            self.assertNotIn("no voice source", self._msgs(lint_skill.lint_skill(d)))

    def test_engagement_copy_without_storytelling_fails(self):
        fm = _CF_FM + "engagement_copy: true\n"
        body = f"\n# S\n\n{_ANCHOR}\nVoice: `marketing-strategy/<BrandName>/voice.md`.\n"
        with tempfile.TemporaryDirectory() as tmp:
            d = _write(Path(tmp), fm, body)
            issues = lint_skill.lint_skill(d)
            self.assertTrue(any(s == "FAIL" and "storytelling-method.md" in m
                                for s, m in issues), issues)

    def test_engagement_copy_with_storytelling_passes(self):
        fm = _CF_FM + "engagement_copy: true\n"
        body = (f"\n# S\n\n{_ANCHOR}\nVoice: `marketing-strategy/<BrandName>/voice.md`.\n"
                "Hook craft: knowledge/storytelling-method.md.\n")
        with tempfile.TemporaryDirectory() as tmp:
            d = _write(Path(tmp), fm, body)
            self.assertNotIn("FAIL", _sev(lint_skill.lint_skill(d)), lint_skill.lint_skill(d))

    def test_engagement_copy_alone_still_owes_a_voice_source(self):
        """Engagement copy is customer-facing by definition, flag or no flag."""
        fm = _FLOOR_FM + "engagement_copy: true\n"  # no produces_customer_facing_copy
        body = "\n# S\n\nHook craft: knowledge/storytelling-method.md.\n"
        with tempfile.TemporaryDirectory() as tmp:
            d = _write(Path(tmp), fm, body)
            issues = lint_skill.lint_skill(d)
            self.assertTrue(any(s == "WARN" and "no voice source" in m for s, m in issues), issues)

    def test_engagement_copy_is_a_known_manifest_key(self):
        """A new frontmatter key FAILs the closed manifest schema until it is declared."""
        fm = _CF_FM + "engagement_copy: true\n"
        body = (f"\n# S\n\n{_ANCHOR}\nVoice: `marketing-strategy/<BrandName>/voice.md`.\n"
                "Hook craft: knowledge/storytelling-method.md.\n")
        with tempfile.TemporaryDirectory() as tmp:
            d = _write(Path(tmp), fm, body)
            self.assertNotIn("unknown key", self._msgs(lint_skill.lint_skill(d)))


class TestUnflaggedSkillIsExempt(unittest.TestCase):
    """The assistant's own voice / operator analysis keeps positive framing without failing."""

    def test_unflagged_positive_only_is_clean(self):
        # e.g. start-here framing a recommendation on the win, or a forecast "where to plan".
        body = "\n# S\n\nFrame the recommendation positive-only: name the win, never the pain.\n"
        with tempfile.TemporaryDirectory() as tmp:
            d = _write(Path(tmp), _FLOOR_FM, body)  # no produces_customer_facing_copy
            issues = lint_skill.lint_skill(d)
            self.assertFalse(any("content-rules.md" in m or "positive-only" in m
                                 for _, m in issues), issues)


if __name__ == "__main__":
    unittest.main()
