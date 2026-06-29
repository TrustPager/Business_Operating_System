#!/usr/bin/env python3
"""Guard: tool invocations in skills and commands must use the signpost form.

Checks all skills/**/SKILL.md and commands/*.md and asserts:

  (a) No bare 'python tools/' invocation (no path-relative call).
  (b) No '${CLAUDE_PLUGIN_ROOT}/tools/' invocation (the old portable form
      that does not expand in PowerShell: the primary platform).
  (c) Every tool invocation uses the cross-OS signpost form:
          python ~/.claude/bos-run.py tool <toolname> [args...]

The connected-skill form 'python ~/.claude/bos-run.py <skill>' (without the
'tool' sub-command) is intentional and must NOT be flagged: only the literal
string '~/.claude/bos-run.py tool ' is the pattern for tool invocations.
"""
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# (a) Bare relative path: never acceptable
BARE_PYTHON_TOOLS = re.compile(r'python tools/')

# (b) Old CLAUDE_PLUGIN_ROOT form: superseded by signpost
PLUGIN_ROOT_FORM = re.compile(r'\$\{CLAUDE_PLUGIN_ROOT\}/tools/')

# (c) Correct signpost form for tool invocations
SIGNPOST_TOOL_FORM = re.compile(r'python\s+~/.claude/bos-run\.py\s+tool\s+\S')

# Connected-skill form (without 'tool'): intentional, must not be flagged
CONNECTED_SKILL_FORM = re.compile(r'python\s+~/.claude/bos-run\.py\s+(?!tool\s)\S')


def _skill_and_command_files():
    files = []
    for path in REPO_ROOT.glob("skills/**/SKILL.md"):
        files.append(path)
    for path in REPO_ROOT.glob("commands/*.md"):
        files.append(path)
    return sorted(files)


class TestInvocationForm(unittest.TestCase):
    """Assert that tool invocations use the ~/.claude/bos-run.py signpost form."""

    def test_no_bare_python_tools_invocations(self):
        """(a) No bare 'python tools/' path-relative invocations.

        Exception: 'python tools/setup.py' is the one-time bootstrap command that
        CREATES the launcher shim. It cannot itself use the launcher (the launcher
        doesn't exist yet), so it is explicitly excluded from this check.
        """
        violations = []
        for filepath in _skill_and_command_files():
            content = filepath.read_text(encoding="utf-8")
            for lineno, line in enumerate(content.splitlines(), start=1):
                if BARE_PYTHON_TOOLS.search(line) and "tools/setup.py" not in line:
                    violations.append(
                        f"{filepath.relative_to(REPO_ROOT)}:{lineno}: {line.strip()}"
                    )
        if violations:
            self.fail(
                "Found bare 'python tools/' invocations (must use the signpost form"
                " 'python ~/.claude/bos-run.py tool <name>' instead):\n"
                + "\n".join(violations)
            )

    def test_no_plugin_root_tool_invocations(self):
        """(b) No ${CLAUDE_PLUGIN_ROOT}/tools/ invocations: does not expand in PowerShell."""
        violations = []
        for filepath in _skill_and_command_files():
            content = filepath.read_text(encoding="utf-8")
            for lineno, line in enumerate(content.splitlines(), start=1):
                if PLUGIN_ROOT_FORM.search(line):
                    violations.append(
                        f"{filepath.relative_to(REPO_ROOT)}:{lineno}: {line.strip()}"
                    )
        if violations:
            self.fail(
                "Found '${CLAUDE_PLUGIN_ROOT}/tools/' invocations (superseded by"
                " 'python ~/.claude/bos-run.py tool <name>': the old form does not"
                " expand in PowerShell):\n"
                + "\n".join(violations)
            )

    def test_signpost_tool_form_present(self):
        """(c) Sanity check: the signpost tool form exists somewhere (catches accidental blanket removal)."""
        found = False
        for filepath in _skill_and_command_files():
            content = filepath.read_text(encoding="utf-8")
            if SIGNPOST_TOOL_FORM.search(content):
                found = True
                break
        self.assertTrue(
            found,
            "Expected to find at least one 'python ~/.claude/bos-run.py tool <name>'"
            " invocation in skills or commands, but found none. Was the migration"
            " accidentally reverted?",
        )

    def test_connected_skill_form_not_flagged(self):
        """The connected-skill form 'python ~/.claude/bos-run.py <skill>' (no 'tool') must not be confused with tool calls."""
        # This test verifies that SIGNPOST_TOOL_FORM does NOT match connected-skill invocations.
        connected_examples = [
            "python ~/.claude/bos-run.py sweep-my-day",
            "python ~/.claude/bos-run.py weekly-review",
            "python ~/.claude/bos-run.py draft-reply --hours 48",
        ]
        for example in connected_examples:
            self.assertFalse(
                SIGNPOST_TOOL_FORM.search(example),
                f"SIGNPOST_TOOL_FORM incorrectly matched connected-skill invocation: {example!r}",
            )
        # And confirm it DOES match the tool form
        tool_examples = [
            "python ~/.claude/bos-run.py tool write_xlsx --out foo.xlsx",
            "python ~/.claude/bos-run.py tool finance_calc pmt --rate 0.006",
        ]
        for example in tool_examples:
            self.assertTrue(
                SIGNPOST_TOOL_FORM.search(example),
                f"SIGNPOST_TOOL_FORM failed to match tool invocation: {example!r}",
            )


if __name__ == "__main__":
    unittest.main()
