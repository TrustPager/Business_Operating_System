#!/usr/bin/env python3
"""Tests for the mechanical no-em-dash content guard on the doc-write tools.

The guard runs after the library import but before any write, so an em-dash payload
never reaches a file. These tests run with the doc libraries present (the normal
case), so an em-dash payload exits with EXIT_CONTENT_RULE (3) rather than the
missing-dependency code (2).
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import _content_rules  # noqa: E402
import write_docx  # noqa: E402
import write_xlsx  # noqa: E402
import make_pdf  # noqa: E402

EM = "—"  # em dash


class TestFindEmDashes(unittest.TestCase):
    def test_clean_text_has_no_offenders(self):
        self.assertEqual(
            _content_rules.find_em_dashes(["all good, no dashes", "ranges 9-5 are fine"]),
            [],
        )

    def test_em_dash_is_found_with_snippet(self):
        offenders = _content_rules.find_em_dashes([f"we deliver{EM}fast"])
        self.assertEqual(len(offenders), 1)
        self.assertIn(EM, offenders[0])

    def test_non_strings_are_ignored(self):
        self.assertEqual(_content_rules.find_em_dashes([1, None, True, 3.5]), [])


class TestAssertNoEmDash(unittest.TestCase):
    def test_clean_passes(self):
        _content_rules.assert_no_em_dash(["fine, really", "also fine: yes"])  # no raise

    def test_em_dash_exits_with_content_rule_code(self):
        with self.assertRaises(SystemExit) as cm:
            _content_rules.assert_no_em_dash([f"bad{EM}copy"])
        self.assertEqual(cm.exception.code, _content_rules.EXIT_CONTENT_RULE)


class TestDocToolsRejectEmDash(unittest.TestCase):
    """Each write tool rejects an em-dash payload (exit 3) before writing the file."""

    def test_write_docx_rejects_em_dash_paragraph(self):
        with self.assertRaises(SystemExit) as cm:
            write_docx.write_docx("unused.docx", [{"type": "paragraph", "text": f"a{EM}b"}])
        self.assertEqual(cm.exception.code, _content_rules.EXIT_CONTENT_RULE)

    def test_write_docx_rejects_em_dash_in_table_cell(self):
        with self.assertRaises(SystemExit) as cm:
            write_docx.write_docx(
                "unused.docx",
                [{"type": "table", "header": ["Item", "Price"], "rows": [[f"Labour{EM}8h", "$760"]]}],
            )
        self.assertEqual(cm.exception.code, _content_rules.EXIT_CONTENT_RULE)

    def test_write_xlsx_rejects_em_dash_cell(self):
        with self.assertRaises(SystemExit) as cm:
            write_xlsx.write_xlsx("unused.xlsx", [["Item", "Price"], [f"Parts{EM}misc", 450]])
        self.assertEqual(cm.exception.code, _content_rules.EXIT_CONTENT_RULE)

    def test_make_pdf_rejects_em_dash_paragraph(self):
        with self.assertRaises(SystemExit) as cm:
            make_pdf.make_pdf("unused.pdf", [{"type": "paragraph", "text": f"x{EM}y"}])
        self.assertEqual(cm.exception.code, _content_rules.EXIT_CONTENT_RULE)


if __name__ == "__main__":
    unittest.main()
