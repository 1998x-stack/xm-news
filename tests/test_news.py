from pathlib import Path
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_news


class DailyNewsTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "data/2026-11-23.json").read_text(encoding="utf-8"))

    def test_daily_record_has_all_sixteen_headlines(self):
        self.assertEqual(len(self.data["broadcast_headlines"]), 16)

    def test_market_values_are_explicit_and_separate(self):
        a_share = self.data["market_data"]["a_share"]["indices"]
        hk = self.data["market_data"]["hong_kong"]["indices"]
        self.assertEqual(next(x for x in a_share if x["name"] == "创业板指")["change_pct"], 3.08)
        self.assertEqual(next(x for x in hk if x["name"] == "恒生指数")["change_pct"], -0.12)

    def test_margin_rule_is_not_effective_yet(self):
        self.assertEqual(self.data["macro_and_policy"]["margin_rule_effective_date"], "2026-11-30")

    def test_source_conflict_is_preserved(self):
        breadth = self.data["market_data"]["a_share"]["advancers"]
        self.assertNotEqual(breadth["reported"], breadth["alternate_report"])
        self.assertIn("口径", breadth["note"])

    def test_repository_validation(self):
        self.assertEqual(validate_news.validate(ROOT), [])


if __name__ == "__main__":
    unittest.main()
