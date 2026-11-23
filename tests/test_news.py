from pathlib import Path
import json
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_site
import validate_news


class XMNewsFourPillarTests(unittest.TestCase):
    def setUp(self):
        self.latest = validate_news.report_dates(ROOT)[0]
        self.data = json.loads((ROOT / f"data/{self.latest}.json").read_text(encoding="utf-8"))

    def test_report_metadata_and_market_data(self):
        self.assertEqual(self.data["date"], self.latest)
        self.assertEqual(self.data["timezone"], "Asia/Shanghai")
        self.assertTrue(self.data["title"])
        self.assertTrue(self.data["summary"])
        self.assertGreaterEqual(len(self.data["source_ids"]), 10)
        self.assertGreaterEqual(len(self.data["market_data"]["a_share"]["indices"]), 1)
        self.assertGreaterEqual(len(self.data["market_data"]["hong_kong"]["indices"]), 1)

    def test_exactly_four_independent_pillars(self):
        expected = {"politics", "finance", "economy", "livelihood"}
        self.assertEqual(set(self.data["sections"]), expected)
        sources = (ROOT / f"sources/{self.latest}.md").read_text(encoding="utf-8")
        for slug, section in self.data["sections"].items():
            self.assertTrue((ROOT / section["path"]).is_file())
            self.assertTrue((ROOT / section["content_path"]).is_file())
            self.assertGreaterEqual(len(section["source_ids"]), 3)
            for source_id in section["source_ids"]:
                self.assertIn(source_id, sources)
            article = (ROOT / section["path"]).read_text(encoding="utf-8")
            self.assertIn("<h1>", article)
            self.assertIn("<svg", article)
            self.assertIn("来源与交叉核验", article)

    def test_source_catalog_has_diverse_groups(self):
        catalog = json.loads((ROOT / "config/source-catalog.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(catalog["groups"]), 5)
        sources = [source for group in catalog["groups"] for source in group["sources"]]
        self.assertGreaterEqual(len(sources), 35)
        self.assertTrue(any(source["name"] == "X / Twitter" for source in sources))

    def test_repository_validation(self):
        self.assertEqual(validate_news.validate(ROOT), [])


    def test_event_first_editorial_and_source_lineage(self):
        ed = self.data["editorial"]
        self.assertEqual(len(ed["lenses"]), 3)
        self.assertGreaterEqual(len(ed["observations"]), 4)
        ids = {v["id"] for v in ed["observations"]}
        self.assertEqual(len(ids), len(ed["observations"]))
        for event in ed["observations"]:
            self.assertIn(event["pillar"], {"politics", "finance", "economy", "livelihood"})
            self.assertTrue(event["source_ids"])
            self.assertTrue(event["limitation"])
            self.assertTrue(set(event["source_ids"]).issubset(self.data["source_ids"]))

    def test_curated_pages_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "site"
            result = build_site.write_site(ROOT, output)
            self.assertEqual(result["latest_date"], self.latest)
            self.assertEqual(set(result["pillars"]), {"politics", "finance", "economy", "livelihood"})
            for path in ("index.html", "archive/index.html", "source-guide/index.html", "source-catalog.json", "latest.json", "sitemap.xml"):
                self.assertTrue((output / path).is_file(), path)
            self.assertTrue((output / f"issues/{self.latest}/index.html").is_file())
            for slug in ("politics", "finance", "economy", "livelihood"):
                self.assertTrue((output / f"{slug}/index.html").is_file())
                self.assertTrue((output / f"issues/{self.latest}/{slug}/index.html").is_file())
            self.assertFalse((output / ".agent").exists())
            self.assertTrue((output / "assets/site.css").is_file())
            self.assertTrue((output / "assets/filters.js").is_file())
            self.assertTrue((output / "days.json").is_file())
            homepage = (output / "index.html").read_text(encoding="utf-8")
            self.assertIn('id="date-filter"', homepage)
            self.assertIn('id="year-filter"', homepage)
            self.assertIn('id="month-filter"', homepage)
            self.assertIn(f'issues/{self.latest}/', homepage)
            day_page = (output / f"issues/{self.latest}/index.html").read_text(encoding="utf-8")
            self.assertIn("同一天，三个观察角度", day_page)
            self.assertIn("当天最值得关注的事件", day_page)
            self.assertIn("四个领域，深入阅读", day_page)
            self.assertIn("S53", day_page)
            self.assertIn("S56", day_page)
            for slug in ("politics", "finance", "economy", "livelihood"):
                self.assertIn(f'href="{slug}/"', day_page)

            self.assertFalse((output / "scripts").exists())


if __name__ == "__main__":
    unittest.main()
