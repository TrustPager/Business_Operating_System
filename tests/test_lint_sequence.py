"""Offline unit tests for the nurture-sequence linter (tools/lint-sequence.py).

Pure logic, no network, no API key. Run:
    python -m unittest tests.test_lint_sequence
    python -m unittest discover -s tests
"""

import importlib.util
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("lint_sequence", REPO / "tools" / "lint-sequence.py")
ls = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ls)  # type: ignore[union-attr]

GOOD = {
    "label": "Day 0",
    "subject": "Streamline your week",
    "body": ('<p>Hi {{contact.first_name}},</p><p>Here is the idea.</p>'
             '<p><a href="https://x"><strong>Watch it here:</strong></a></p>'
             '<p><a href="https://x"><img src="y.png"></a></p>'
             '<p>Warmest regards,<br>Simon</p>'),
}
# Same email but the ONLY anchor wraps the image — no text CTA above it.
IMG_ONLY = {
    "label": "Day 7",
    "subject": "See how it works",
    "body": ('<p>Hi {{contact.first_name}},</p><p>See it:</p>'
             '<p><a href="https://x"><img src="y.png"></a></p>'
             '<p>Warmest regards,<br>Simon</p>'),
}


def _check(email, name):
    report = ls.lint([email], signoff="Warmest regards", allow_em_dash=False)
    return next(c for c in report["emails"][0]["checks"] if c["check"] == name)


class TestPerEmail(unittest.TestCase):
    def test_good_email_overall_pass(self):
        report = ls.lint([GOOD], signoff="Warmest regards", allow_em_dash=False)
        self.assertEqual(report["overall"], ls.PASS, report)

    def test_text_cta_above_image_passes_for_good(self):
        self.assertEqual(_check(GOOD, "cta_above_image")["level"], ls.PASS)

    def test_image_wrapping_anchor_is_not_a_text_cta(self):
        # The bug we fixed: an anchor that only wraps the <img> must NOT count.
        c = _check(IMG_ONLY, "cta_above_image")
        self.assertEqual(c["level"], ls.FAIL, c)

    def test_negative_subject_warns(self):
        email = dict(GOOD, subject="Don't miss out")
        self.assertEqual(_check(email, "positive_subject")["level"], ls.WARN)

    def test_em_dash_warns_by_default(self):
        email = dict(GOOD, subject="Streamline — your week")
        self.assertEqual(_check(email, "no_em_dash")["level"], ls.WARN)

    def test_em_dash_allowed_with_flag(self):
        email = dict(GOOD, subject="Streamline — your week")
        report = ls.lint([email], signoff="Warmest regards", allow_em_dash=True)
        c = next(x for x in report["emails"][0]["checks"] if x["check"] == "no_em_dash")
        self.assertEqual(c["level"], ls.PASS)

    def test_missing_link_fails(self):
        email = {"label": "x", "subject": "Hello there",
                 "body": "<p>Hi {{contact.first_name}},</p><p>No link here.</p>"}
        self.assertEqual(_check(email, "link")["level"], ls.FAIL)


class TestConsistency(unittest.TestCase):
    def test_mixed_cta_above_image_is_a_failure(self):
        report = ls.lint([GOOD, IMG_ONLY], signoff="Warmest regards", allow_em_dash=False)
        self.assertEqual(report["overall"], ls.FAIL)
        mixed = [c for c in report["consistency"] if "MIXED" in c["message"]]
        self.assertTrue(mixed, "expected a MIXED cta_above_image finding")
        self.assertEqual(mixed[0]["level"], ls.FAIL)

    def test_uniform_good_set_has_no_mixed_finding(self):
        report = ls.lint([GOOD, dict(GOOD, label="Day 2")],
                         signoff="Warmest regards", allow_em_dash=False)
        mixed = [c for c in report["consistency"] if "MIXED" in c["message"]]
        self.assertFalse(mixed)


if __name__ == "__main__":
    unittest.main()
