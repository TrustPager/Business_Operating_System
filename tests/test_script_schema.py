#!/usr/bin/env python3
"""Offline schema check for script-my-video's `<slug>.script.json` contract.

script-my-video is a reasoning-only, keyless skill: it has no fetch.py to drive
with tools/test-skill.py. Its testable artifact is the beat schema it emits (spec
§3, docs/architecture/2026-07-05-youtube-studio-design.md). This test validates a
committed sample script output against that contract, so an implementer can never
drift the schema, and confirms the committed topic-payload input fixture is
well-formed. No network, no key: pure JSON-shape assertions.

Run: BOS_OFFLINE=1 python -m unittest tests.test_script_schema
"""
import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO / "skills" / "script-my-video"
INPUT_FIXTURE = SKILL_DIR / "test-fixture.json"
SAMPLE_SCRIPT = SKILL_DIR / "sample.script.json"

# The beat roles the schema allows (spec §3). `subscribe` was added 2026-07-26: the
# subscribe ask is its own beat in youtube-script-method.md, and without a role of its
# own it was being smuggled in as a `reset`, which mislabels it for anything reading
# roles (chapter labels, the scenes plan, the timing file).
VALID_ROLES = {"hook", "promise", "point", "reset", "proof", "subscribe", "cta"}
# The minimum roles a conforming script must reach (Task 1.1 Step 4).
REQUIRED_ROLES = {"hook", "promise", "point", "cta"}
# Every beat must carry these keys.
REQUIRED_BEAT_KEYS = {"id", "role", "spoken", "on_screen", "b_roll"}
# Owner-facing beat text where the no-em-dash rule applies.
EM_DASH = "—"


def _validate_script(doc: dict) -> list[str]:
    """Return a list of contract violations for a script doc (empty == valid)."""
    errors: list[str] = []

    # Top-level required keys.
    for key in ("slug", "working_title", "packaging", "meta", "beats"):
        if key not in doc:
            errors.append(f"missing top-level key: {key}")

    meta = doc.get("meta", {})
    if not isinstance(meta, dict):
        errors.append("meta: must be an object")
        meta = {}
    for key in ("duration_target_s", "aspect", "hook_window_s"):
        if key not in meta:
            errors.append(f"meta missing key: {key}")

    packaging = doc.get("packaging", {})
    if not isinstance(packaging, dict):
        errors.append("packaging: must be an object")
        packaging = {}
    if not isinstance(packaging.get("title_options"), list) or not packaging.get("title_options"):
        errors.append("packaging.title_options: must be a non-empty array")
    for key in ("thumbnail_concept", "angle"):
        if key not in packaging:
            errors.append(f"packaging missing key: {key}")

    beats = doc.get("beats")
    if not isinstance(beats, list) or not beats:
        errors.append("beats: must be a non-empty array")
        return errors

    seen_ids = set()
    seen_roles = set()
    for i, beat in enumerate(beats):
        if not isinstance(beat, dict):
            errors.append(f"beat[{i}]: must be an object")
            continue
        missing = REQUIRED_BEAT_KEYS - set(beat)
        for k in sorted(missing):
            errors.append(f"beat[{i}] missing key: {k}")
        role = beat.get("role")
        if role not in VALID_ROLES:
            errors.append(f"beat[{i}] role '{role}' not in {sorted(VALID_ROLES)}")
        else:
            seen_roles.add(role)
        bid = beat.get("id")
        if bid in seen_ids:
            errors.append(f"beat[{i}] duplicate id: {bid}")
        seen_ids.add(bid)
        # duration_s is optional, but if present must be a positive number.
        if "duration_s" in beat:
            d = beat["duration_s"]
            if not isinstance(d, (int, float)) or isinstance(d, bool) or d <= 0:
                errors.append(f"beat[{i}] duration_s must be a positive number")
        # No em dashes in owner-facing beat text.
        for field in ("spoken", "on_screen"):
            val = beat.get(field, "")
            if isinstance(val, str) and EM_DASH in val:
                errors.append(f"beat[{i}] {field} contains an em dash")

    missing_roles = REQUIRED_ROLES - seen_roles
    if missing_roles:
        errors.append(f"required beat roles not reached: {sorted(missing_roles)}")

    # The hook must be the first beat and land inside the hook window.
    first = beats[0]
    if first.get("role") != "hook":
        errors.append("first beat must be the hook")
    hook_window = meta.get("hook_window_s")
    if isinstance(hook_window, (int, float)) and "duration_s" in first:
        if first["duration_s"] > hook_window:
            errors.append(
                f"hook duration_s ({first['duration_s']}) exceeds hook_window_s ({hook_window})"
            )

    # Exactly one call to action.
    cta_count = sum(1 for b in beats if isinstance(b, dict) and b.get("role") == "cta")
    if cta_count != 1:
        errors.append(f"expected exactly one cta beat, found {cta_count}")

    return errors


class TestInputFixture(unittest.TestCase):
    def test_input_fixture_present_and_wellformed(self):
        self.assertTrue(INPUT_FIXTURE.exists(), f"missing input fixture {INPUT_FIXTURE}")
        payload = json.loads(INPUT_FIXTURE.read_text(encoding="utf-8"))
        # A topic payload the skill can script from: a topic and the one action.
        self.assertIn("topic", payload)
        self.assertIn("one_action", payload)
        self.assertIn("target_length_s", payload)


class TestSampleScriptConformsToSchema(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SAMPLE_SCRIPT.exists(), f"missing sample script {SAMPLE_SCRIPT}")
        self.doc = json.loads(SAMPLE_SCRIPT.read_text(encoding="utf-8"))

    def test_sample_is_schema_valid(self):
        errors = _validate_script(self.doc)
        self.assertEqual(errors, [], f"sample script violates the schema: {errors}")

    def test_slug_is_kebab_case(self):
        slug = self.doc.get("slug", "")
        self.assertRegex(slug, r"^[a-z0-9]+(-[a-z0-9]+)*$", "slug must be kebab-case")


class TestValidatorCatchesBadScripts(unittest.TestCase):
    """Guard the validator itself: it must reject a script that breaks the contract."""

    def _base(self) -> dict:
        return {
            "slug": "x",
            "working_title": "X",
            "packaging": {"title_options": ["A"], "thumbnail_concept": "t", "angle": "a"},
            "meta": {"duration_target_s": 60, "aspect": "16:9", "hook_window_s": 5},
            "beats": [
                {"id": "hook", "role": "hook", "spoken": "s", "on_screen": "o", "b_roll": "b", "duration_s": 4},
                {"id": "promise", "role": "promise", "spoken": "s", "on_screen": "o", "b_roll": "b"},
                {"id": "point-1", "role": "point", "spoken": "s", "on_screen": "o", "b_roll": "b"},
                {"id": "cta", "role": "cta", "spoken": "s", "on_screen": "o", "b_roll": "b"},
            ],
        }

    def test_base_is_valid(self):
        self.assertEqual(_validate_script(self._base()), [])

    def test_missing_required_role_is_caught(self):
        doc = self._base()
        doc["beats"] = [b for b in doc["beats"] if b["role"] != "promise"]
        self.assertTrue(any("promise" in e for e in _validate_script(doc)))

    def test_two_ctas_is_caught(self):
        doc = self._base()
        doc["beats"].append({"id": "cta-2", "role": "cta", "spoken": "s", "on_screen": "o", "b_roll": "b"})
        self.assertTrue(any("cta" in e for e in _validate_script(doc)))

    def test_subscribe_is_a_valid_role_and_may_repeat(self):
        """The subscribe ask is its own beat, and a channel may ask twice.

        Before `subscribe` existed, this beat was authored as a `reset`, which
        mislabelled it for anything reading roles. A channel that asks mid-roll and
        again at the end has two of them, alongside exactly one terminal cta.
        """
        doc = self._base()
        doc["beats"][3:3] = [
            {"id": "subscribe-midroll", "role": "subscribe", "spoken": "s", "on_screen": "o", "b_roll": "b"},
            {"id": "subscribe-close", "role": "subscribe", "spoken": "s", "on_screen": "o", "b_roll": "b"},
        ]
        self.assertEqual(_validate_script(doc), [])

    def test_em_dash_is_caught(self):
        doc = self._base()
        doc["beats"][0]["on_screen"] = "win " + EM_DASH + " today"
        self.assertTrue(any("em dash" in e for e in _validate_script(doc)))

    def test_hook_outside_window_is_caught(self):
        doc = self._base()
        doc["beats"][0]["duration_s"] = 12
        self.assertTrue(any("hook" in e and "window" in e for e in _validate_script(doc)))


if __name__ == "__main__":
    unittest.main()
