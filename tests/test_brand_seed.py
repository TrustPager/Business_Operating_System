"""Tests for setup.py's _seed_brand — the brand-kit seeding that keeps updates clean.

The owner's live brand files (brand/brand.json, logo, favicons) are gitignored
user-data. A fresh clone ships only the neutral defaults under brand/defaults/, so
setup seeds any MISSING live file from there. The critical guarantee is that it
NEVER overwrites a brand the owner already set, because that is what lets a plain
`git pull` update never collide with someone's branding.

Offline-safe: pure filesystem, no network, no key.
"""

import importlib
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

setup = importlib.import_module("setup")


def _make_tree(root: Path, live: dict[str, str] | None = None,
               defaults: dict[str, str] | None = None) -> None:
    (root / "brand" / "defaults").mkdir(parents=True, exist_ok=True)
    for name, content in (defaults or {}).items():
        (root / "brand" / "defaults" / name).write_text(content, encoding="utf-8")
    for name, content in (live or {}).items():
        (root / "brand" / name).write_text(content, encoding="utf-8")


class TestSeedBrand(unittest.TestCase):
    def test_seeds_missing_live_files_from_defaults(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _make_tree(root, defaults={"brand.json": '{"name":"Your Business"}',
                                       "logo.png": "PNGDEFAULT"})
            setup._seed_brand(root)
            self.assertEqual((root / "brand" / "brand.json").read_text(encoding="utf-8"),
                             '{"name":"Your Business"}')
            self.assertEqual((root / "brand" / "logo.png").read_text(encoding="utf-8"),
                             "PNGDEFAULT")

    def test_never_overwrites_a_brand_the_owner_set(self):
        # The load-bearing guarantee: a live file the owner customised is left alone,
        # so `git pull` + setup never clobbers their branding.
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _make_tree(root,
                       live={"brand.json": '{"name":"Acme Plumbing"}'},
                       defaults={"brand.json": '{"name":"Your Business"}',
                                 "logo.png": "PNGDEFAULT"})
            setup._seed_brand(root)
            # Their brand is untouched...
            self.assertEqual((root / "brand" / "brand.json").read_text(encoding="utf-8"),
                             '{"name":"Acme Plumbing"}')
            # ...and the missing logo still gets seeded.
            self.assertTrue((root / "brand" / "logo.png").exists())

    def test_no_defaults_dir_is_a_noop(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "brand").mkdir(parents=True, exist_ok=True)
            setup._seed_brand(root)  # must not raise
            self.assertFalse((root / "brand" / "brand.json").exists())


if __name__ == "__main__":
    unittest.main()
