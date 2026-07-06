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
