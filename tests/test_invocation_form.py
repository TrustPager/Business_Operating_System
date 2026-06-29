#!/usr/bin/env python3
"""Guard: every tool invocation in skills and commands must use the portable
${CLAUDE_PLUGIN_ROOT}/tools/ form, never a bare 'python tools/' call.

This test greps all skills/**/SKILL.md and commands/*.md for the pattern
'python tools/' and asserts none are found without the CLAUDE_PLUGIN_ROOT
prefix. It is careful not to false-positive on the correct form itself.
"""
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Pattern that matches a bare 'python tools/' NOT preceded by CLAUDE_PLUGIN_ROOT
# We look for lines that contain 'python tools/' but NOT '${CLAUDE_PLUGIN_ROOT}/tools/'
BARE_INVOCATION = re.compile(r'python tools/')
PORTABLE_FORM = re.compile(r'\$\{CLAUDE_PLUGIN_ROOT\}/tools/')


def _skill_and_command_files():
    files = []
    for path in REPO_ROOT.glob("skills/**/SKILL.md"):
        files.append(path)
    for path in REPO_ROOT.glob("commands/*.md"):
        files.append(path)
    return files


class TestInvocationForm(unittest.TestCase):
    """Assert no skill or command body contains a bare 'python tools/' invocation."""

    def test_no_bare_python_tools_invocations(self):
        violations = []
        for filepath in _skill_and_command_files():
            content = filepath.read_text(encoding="utf-8")
            for lineno, line in enumerate(content.splitlines(), start=1):
                if BARE_INVOCATION.search(line) and not PORTABLE_FORM.search(line):
                    violations.append(
                        f"{filepath.relative_to(REPO_ROOT)}:{lineno}: {line.strip()}"
                    )

        if violations:
            self.fail(
                "Found bare 'python tools/' invocations (must use"
                " ${CLAUDE_PLUGIN_ROOT}/tools/ instead):\n"
                + "\n".join(violations)
            )

    def test_portable_form_present_in_expected_files(self):
        """Sanity check: the portable form exists somewhere (catches accidental blanket removal)."""
        found = False
        for filepath in _skill_and_command_files():
            content = filepath.read_text(encoding="utf-8")
            if PORTABLE_FORM.search(content):
                found = True
                break
        self.assertTrue(
            found,
            "Expected to find at least one ${CLAUDE_PLUGIN_ROOT}/tools/ invocation "
            "in skills or commands, but found none. Was the fix accidentally reverted?",
        )


if __name__ == "__main__":
    unittest.main()
