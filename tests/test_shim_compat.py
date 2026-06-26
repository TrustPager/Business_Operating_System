"""Compatibility-shim contract tests for tools/trustpager_api.py.

trustpager_api.py is a thin re-export shim: the real homes are kernel/runtime/
(vendor-neutral) and drivers/trustpager/ (TrustPager). The 22 skills/*/fetch.py
scripts — plus several tools/*.py — import their whole public surface from it.
These tests lock that surface so slimming the shim can never silently drop a
name or break a signature.

Imports trustpager_api exactly the way a skill fetch.py does: put tools/ on
sys.path, then `import trustpager_api`.

Run:
    python -m unittest tests.test_shim_compat
"""

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import trustpager_api as t  # noqa: E402

# The full public surface the shim guarantees. Every name here must keep
# resolving with an identical signature for skills/*/fetch.py + tools/*.py to
# keep importing them unchanged. Sourced from the task spec's minimum list plus
# every name actually imported across skills/ + tools/.
PUBLIC_FUNCTIONS = [
    # transport / driver writes + reads
    "api_get", "api_post", "api_patch", "idempotent_post",
    "parallel_get", "paginate", "bulk_apply",
    # catalog-driven path resolution
    "resolve_path", "get_catalog", "inspect_endpoint", "api_call_by_resource",
    "get_api_key",
    # kernel helpers
    "now_utc", "parse_iso", "days_since", "group_count", "top_n_by",
    "log", "emit_json", "emit_error_and_exit", "force_utf8_stdout",
]

PUBLIC_CLASSES = ["ApprovalPending", "BOSError"]

PUBLIC_CONSTANTS = ["API_BASE", "CATALOG_URL"]


class TestPublicSurfacePresent(unittest.TestCase):
    def test_functions_present_and_callable(self):
        for name in PUBLIC_FUNCTIONS:
            self.assertTrue(hasattr(t, name), f"shim is missing public name: {name}")
            self.assertTrue(callable(getattr(t, name)), f"{name} should be callable")

    def test_classes_present(self):
        for name in PUBLIC_CLASSES:
            self.assertTrue(hasattr(t, name), f"shim is missing public class: {name}")
            self.assertTrue(isinstance(getattr(t, name), type), f"{name} should be a class")

    def test_constants_present(self):
        for name in PUBLIC_CONSTANTS:
            self.assertTrue(hasattr(t, name), f"shim is missing public constant: {name}")

    def test_approvalpending_is_the_trustpager_subclass(self):
        # The re-exported ApprovalPending must be the TrustPager subclass (with
        # poll()/executed), not the bare kernel base — skills rely on isinstance.
        self.assertTrue(hasattr(t.ApprovalPending, "poll"))
        self.assertTrue(hasattr(t.ApprovalPending, "executed"))


class TestRebindingSeam(unittest.TestCase):
    """tools/test-skill.py reassigns trustpager_api.api_get to a fixture mock.

    parallel_get / paginate exported from the shim must observe that rebinding
    at call time (they look api_get up via the shim's globals), or fixture-based
    skill testing breaks. This mirrors that seam without touching the network.
    """

    def test_parallel_get_observes_rebound_api_get(self):
        real = t.api_get
        calls = []

        def fake_api_get(path, **params):
            calls.append((path, params))
            return {"data": [{"id": path}], "pagination": {"has_more": False}}

        t.api_get = fake_api_get
        try:
            out = t.parallel_get([("opportunities", {"limit": 1}),
                                  ("tasks", {})])
        finally:
            t.api_get = real
        self.assertEqual(set(out.keys()), {"opportunities", "tasks"})
        self.assertEqual(out["opportunities"], {"data": [{"id": "opportunities"}],
                                                "pagination": {"has_more": False}})
        self.assertEqual({c[0] for c in calls}, {"opportunities", "tasks"})

    def test_paginate_observes_rebound_api_get(self):
        real = t.api_get
        # paginate auto-follows pagination.next_cursor until has_more is false.
        pages = [
            {"data": [{"id": 1}, {"id": 2}],
             "pagination": {"has_more": True, "next_cursor": "c1"}},
            {"data": [{"id": 3}], "pagination": {"has_more": False}},
        ]
        seq = iter(pages)

        def fake_api_get(path, **params):
            return next(seq)

        t.api_get = fake_api_get
        try:
            rows = list(t.paginate("opportunities", limit=2))
        finally:
            t.api_get = real
        self.assertEqual([r["id"] for r in rows], [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
