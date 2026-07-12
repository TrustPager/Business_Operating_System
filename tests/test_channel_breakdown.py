"""Tests for tools/channel_breakdown.py -- the breakout engine.

Offline, deterministic, no network, no CRM key. Mirrors the tools-import pattern
used by test_finance_calc.py (sys.path.insert + bare import; there is no
tools/__init__.py).

Run:
    BOS_OFFLINE=1 python -m unittest tests.test_channel_breakdown
"""
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TOOLS = REPO / "tools"
sys.path.insert(0, str(TOOLS))

import channel_breakdown  # noqa: E402


class TestParse(unittest.TestCase):
    def test_skips_null_views_and_orders_oldest_first(self):
        # yt-dlp flat dump: playlist_index 1 = most recent (reverse-chron)
        entries = [
            {"playlist_index": 1, "title": "newest", "view_count": 50000},
            {"playlist_index": 2, "title": "shorts", "view_count": None},   # skipped
            {"playlist_index": 3, "title": "oldest", "view_count": 10000},
        ]
        vids = channel_breakdown.parse_flat_dump(entries)
        self.assertEqual([v["title"] for v in vids], ["oldest", "newest"])
        self.assertTrue(all(v["view_count"] is not None for v in vids))

    def test_accepts_entries_wrapper(self):
        vids = channel_breakdown.parse_flat_dump(
            {"entries": [{"playlist_index": 1, "title": "a", "view_count": 100}]})
        self.assertEqual(len(vids), 1)

    def test_load_entries_handles_jsonl(self):
        # yt-dlp --dump-json emits one JSON object per line; each starts with '{'
        jsonl = '{"playlist_index": 1, "title": "a", "view_count": 5}\n' \
                '{"playlist_index": 2, "title": "b", "view_count": 6}'
        entries = channel_breakdown._load_entries(jsonl)
        self.assertEqual(len(entries), 2)

    def test_load_entries_handles_single_array(self):
        entries = channel_breakdown._load_entries('[{"view_count": 1}, {"view_count": 2}]')
        self.assertEqual(len(entries), 2)


class TestRollingOutlier(unittest.TestCase):
    def test_steady_channel_reads_near_1x(self):
        vids = [{"title": f"v{i}", "view_count": 10000} for i in range(20)]
        out = channel_breakdown.rolling_outlier(vids, window=5)
        scored = [v for v in out if v.get("outlier") is not None]
        self.assertTrue(scored)
        for v in scored:
            self.assertAlmostEqual(v["outlier"], 1.0, delta=0.01)

    def test_early_videos_have_no_baseline(self):
        vids = [{"title": f"v{i}", "view_count": 10000} for i in range(10)]
        out = channel_breakdown.rolling_outlier(vids, window=5)
        self.assertIsNone(out[0]["outlier"])
        self.assertIsNone(out[2]["outlier"])   # < 3 prior
        self.assertIsNotNone(out[3]["outlier"])  # 3 prior -> scored


class TestDetect(unittest.TestCase):
    def test_finds_a_real_step(self):
        vids = [{"title": f"v{i}", "view_count": 10000} for i in range(12)] + \
               [{"title": f"v{i}", "view_count": 50000} for i in range(12, 24)]
        out = channel_breakdown.rolling_outlier(vids, window=5)
        res = channel_breakdown.detect_breakout(out, min_segment=5)
        self.assertEqual(res["status"], "ok")
        self.assertGreaterEqual(res["trigger_index"], 11)
        self.assertLessEqual(res["trigger_index"], 15)

    def test_lone_spike_is_not_a_durable_step(self):
        vids = [{"title": f"v{i}", "view_count": 10000} for i in range(24)]
        vids[12]["view_count"] = 200000
        out = channel_breakdown.rolling_outlier(vids, window=5)
        res = channel_breakdown.detect_breakout(out, min_segment=5)
        self.assertEqual(res["status"], "no_upward_inflection")


if __name__ == "__main__":
    unittest.main()
