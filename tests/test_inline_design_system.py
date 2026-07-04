"""Offline-safe: no network, no key. Run: BOS_OFFLINE=1 python -m unittest tests.test_inline_design_system

Task 1.3 of the Site Builder plan. The helper makes an instantiated copy of
templates/site-starter/ SELF-CONTAINED: it reads the owner's brand/brand.json
plus the skill's derived per-project token overrides and writes a standalone
styles/tokens.css + design-system.json into the project, so nothing depends on
the in-repo ../../../brand path once copied out.

Var-name alignment (the load-bearing contract): the generated tokens.css MUST
use the SAME CSS-variable names that templates/site-starter/styles/tokens.css
declares and templates/site-starter/tailwind.config.js reads, or an instantiated
copy's components will not pick up the tokens. brand.json uses camelCase keys
(primaryDeep, pageBg, textMuted); the starter's CSS vars are kebab-case
(--color-primary-deep, --color-page-bg, --color-text-muted). The helper maps
camelCase brand keys to those exact kebab-case var names.
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "skills" / "design-my-site"))
import inline_design_system as ids


class TestInline(unittest.TestCase):
    def test_writes_self_contained_tokens(self):
        with tempfile.TemporaryDirectory() as d:
            proj = Path(d)
            (proj / "styles").mkdir()
            brand = {"colors": {"primary": "#1A2B6D", "accent": "#E84545", "pageBg": "#F8F8F6", "text": "#111111"},
                     "fonts": {"primary": "DM Sans", "serif": "Syne"}}
            overrides = {"radius": {"sm": "2px", "md": "4px", "full": "0px"}, "colors": {"accent": "#0EA5A0"}}
            ds = ids.inline(proj, brand=brand, overrides=overrides)
            css = (proj / "styles" / "tokens.css").read_text()
            self.assertIn("--color-primary: #1A2B6D", css)          # brand token carried through
            self.assertIn("--color-accent: #0EA5A0", css)           # override wins over brand
            self.assertIn("--radius-full: 0px", css)                # radius pinned (anti-sameness)
            self.assertNotIn("../../../brand", css)                 # self-contained, no repo path
            self.assertEqual(ds["colors"]["accent"], "#0EA5A0")     # returns the merged system
            self.assertTrue((proj / "design-system.json").exists()) # machine copy for /design-sync

    def test_camelcase_brand_keys_map_to_kebab_css_var_names(self):
        # The starter's tokens.css + tailwind.config.js read kebab-case var names,
        # while brand/defaults/brand.json uses camelCase keys. If this mapping
        # drifts, an instantiated copy's components silently stop reading tokens.
        with tempfile.TemporaryDirectory() as d:
            proj = Path(d)
            (proj / "styles").mkdir()
            brand = {"colors": {"primaryDeep": "#0B1B4D", "pageBg": "#FAFAFA", "textMuted": "#556677"},
                     "fonts": {"primary": "Inter", "serif": "Fraunces"}}
            ids.inline(proj, brand=brand, overrides={})
            css = (proj / "styles" / "tokens.css").read_text()
            self.assertIn("--color-primary-deep: #0B1B4D", css)
            self.assertIn("--color-page-bg: #FAFAFA", css)
            self.assertIn("--color-text-muted: #556677", css)
            # Fonts land on the starter's --font-sans / --font-serif names.
            self.assertIn("--font-sans: Inter", css)
            self.assertIn("--font-serif: Fraunces", css)

    def test_full_radius_scale_is_written(self):
        # The starter declares --radius-sm/md/lg/full; the helper writes the full
        # scale, taking overrides where given and falling back to sensible defaults.
        with tempfile.TemporaryDirectory() as d:
            proj = Path(d)
            (proj / "styles").mkdir()
            brand = {"colors": {"primary": "#123456"}, "fonts": {"primary": "Arial"}}
            overrides = {"radius": {"lg": "24px"}}
            ids.inline(proj, brand=brand, overrides=overrides)
            css = (proj / "styles" / "tokens.css").read_text()
            for var in ("--radius-sm", "--radius-md", "--radius-lg", "--radius-full"):
                self.assertIn(var + ":", css)
            self.assertIn("--radius-lg: 24px", css)                 # override honoured

    def test_deep_merge_does_not_mutate_inputs(self):
        # A pure function must not mutate the brand/overrides dicts it is handed.
        with tempfile.TemporaryDirectory() as d:
            proj = Path(d)
            (proj / "styles").mkdir()
            brand = {"colors": {"primary": "#111111", "accent": "#222222"}, "fonts": {"primary": "Arial"}}
            overrides = {"colors": {"accent": "#333333"}}
            ids.inline(proj, brand=brand, overrides=overrides)
            self.assertEqual(brand["colors"]["accent"], "#222222")  # brand untouched
            self.assertEqual(overrides["colors"], {"accent": "#333333"})

    def test_design_system_json_reflects_the_merge(self):
        with tempfile.TemporaryDirectory() as d:
            proj = Path(d)
            (proj / "styles").mkdir()
            brand = {"colors": {"primary": "#111111", "accent": "#222222"}, "fonts": {"primary": "Arial"}}
            overrides = {"colors": {"accent": "#333333"}, "radius": {"full": "0px"}}
            ds = ids.inline(proj, brand=brand, overrides=overrides)
            written = json.loads((proj / "design-system.json").read_text())
            self.assertEqual(written["colors"]["primary"], "#111111")
            self.assertEqual(written["colors"]["accent"], "#333333")
            self.assertEqual(written["radius"]["full"], "0px")
            self.assertEqual(written, ds)                           # returned dict == file

    def test_creates_styles_dir_if_absent(self):
        # A freshly copied project may not have styles/ yet; the helper creates it.
        with tempfile.TemporaryDirectory() as d:
            proj = Path(d)
            ids.inline(proj, brand={"colors": {"primary": "#abcdef"}, "fonts": {}}, overrides={})
            self.assertTrue((proj / "styles" / "tokens.css").exists())


if __name__ == "__main__":
    unittest.main()
