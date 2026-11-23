from pathlib import Path
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_news
import build_site


class DailyNewsTests(unittest.TestCase):
    def setUp(self):
        self.latest = validate_news.report_dates(ROOT)[0]
        self.data = json.loads((ROOT / f"data/{self.latest}.json").read_text(encoding="utf-8"))

    def test_daily_record_has_headlines_and_sources(self):
        self.assertGreater(len(self.data["broadcast_headlines"]), 0)
        self.assertGreaterEqual(len(self.data["source_ids"]), 5)

    def test_market_values_are_explicit_and_separate(self):
        a_share = self.data["market_data"]["a_share"]["indices"]
        hk = self.data["market_data"]["hong_kong"]["indices"]
        self.assertGreaterEqual(len(a_share), 1)
        self.assertGreaterEqual(len(hk), 1)
        self.assertIn("change_pct", a_share[0])
        self.assertIn("change_pct", hk[0])

    def test_report_metadata_and_date(self):
        self.assertEqual(self.data["date"], self.latest)
        self.assertTrue(self.data["title"])
        self.assertTrue(self.data["summary"])
        self.assertEqual(self.data["timezone"], "Asia/Shanghai")

    def test_source_conflict_is_preserved_when_present(self):
        breadth = self.data.get("market_data", {}).get("a_share", {}).get("advancers", {})
        if breadth:
            self.assertIn("口径", breadth.get("note", ""))

    def test_repository_validation(self):
        self.assertEqual(validate_news.validate(ROOT), [])

    def test_site_build_is_curated_and_complete(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "site"
            result = build_site._write_site(ROOT, out)
            self.assertEqual(result["latest_date"], self.latest)
            self.assertTrue((out / "index.html").is_file())
            self.assertTrue((out / "archive/index.html").is_file())
            self.assertTrue((out / f"posts/{self.latest}/index.html").is_file())
            self.assertTrue((out / "sitemap.xml").is_file())
            self.assertFalse((out / ".agent").exists())
            self.assertFalse((out / "scripts").exists())


if __name__ == "__main__":
    unittest.main()
