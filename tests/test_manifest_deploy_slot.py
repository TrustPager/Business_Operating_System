"""Offline-safe: no network, no key. Run: BOS_OFFLINE=1 python -m unittest tests.test_manifest_deploy_slot"""
import sys, unittest
from pathlib import Path
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import manifest

class TestDeploySlot(unittest.TestCase):
    def test_deploy_is_a_valid_function_slot(self):
        self.assertIn("deploy", manifest.FUNCTION_SLOTS)
    def test_deploy_manifest_validates(self):
        meta = {"function_slot": "deploy", "requires_driver": "vercel",
                "requires_credential": "key", "data_path": "local", "status": "active"}
        errors = manifest.validate_manifest(meta)
        self.assertEqual(errors, [])
