#!/usr/bin/env python3
"""Validate the latest XM News four-pillar daily bundle."""
from __future__ import annotations
import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PILLARS = {"politics", "finance", "economy", "livelihood"}


class ArticleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = self.h2 = self.svg = self.figures = self.figcaptions = 0
        self.main = self.links = self.external_links = self.svg_titles = 0
        self.viewport = self.meta_description = False
        self.ids = set()
        self.href_targets = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "h1": self.h1 += 1
        if tag == "h2": self.h2 += 1
        if tag == "svg":
            self.svg += 1
            if a.get("aria-labelledby"): self.svg_titles += 1
        if tag == "figure": self.figures += 1
        if tag == "figcaption": self.figcaptions += 1
        if tag == "main": self.main += 1
        if tag == "meta" and a.get("name") == "viewport": self.viewport = True
        if tag == "meta" and a.get("name") == "description": self.meta_description = True
        if tag == "a":
            self.links += 1
            href = a.get("href") or ""
            if urlparse(href).scheme in {"http", "https"}: self.external_links += 1
            if href.startswith("#"): self.href_targets.append(href[1:])
        if a.get("id"): self.ids.add(str(a["id"]))


def report_dates(root=ROOT):
    folder = root / "data"
    if not folder.is_dir(): return []
    return sorted((p.stem for p in folder.glob("*.json") if re.fullmatch(r"\d{4}-\d{2}-\d{2}", p.stem)), reverse=True)


def check_html(path, label, errors, minimum_links=8, require_focus=True):
    text = path.read_text(encoding="utf-8")
    parser = ArticleParser()
    parser.feed(text)
    if parser.h1 != 1: errors.append(f"{label}: expected exactly one h1, found {parser.h1}")
    if parser.h2 < 4: errors.append(f"{label}: expected at least four h2 sections, found {parser.h2}")
    if parser.main != 1: errors.append(f"{label}: expected exactly one main, found {parser.main}")
    if parser.svg < 1 or parser.svg_titles < 1: errors.append(f"{label}: accessible SVG missing")
    if parser.figures < 1 or parser.figcaptions < parser.figures: errors.append(f"{label}: figure/figcaption incomplete")
    if not parser.viewport or not parser.meta_description: errors.append(f"{label}: viewport/description metadata missing")
    if parser.external_links < 4: errors.append(f"{label}: insufficient evidence links")
    if parser.links < minimum_links: errors.append(f"{label}: insufficient navigation/source links")
    if require_focus and ":focus-visible" not in text: errors.append(f"{label}: keyboard focus styling missing")
    if "<script src=" in text or '<link rel="stylesheet" href="http' in text: errors.append(f"{label}: external JS/CSS dependency found")
    missing = sorted(set(parser.href_targets) - parser.ids)
    if missing: errors.append(f"{label}: broken local anchors {missing}")


def validate(root=ROOT, selected_date=None):
    errors = []
    dates = report_dates(root)
    if not dates: return ["no daily JSON files found"]
    day = selected_date or dates[0]
    if day not in dates: return [f"report date not found: {day}"]
    data_path = root / "data" / f"{day}.json"
    legacy_html = root / "posts" / day / "index.html"
    legacy_md = root / "content" / f"{day}.md"
    source_path = root / "sources" / f"{day}.md"
    for path in (data_path, legacy_md, source_path):
        if not path.is_file(): errors.append(f"missing required file: {path.relative_to(root)}")
    if errors: return errors
    try:
        data = json.loads(data_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid report JSON: {exc}"]
    if data.get("date") != day: errors.append("JSON date mismatch")
    if data.get("timezone") != "Asia/Shanghai": errors.append("timezone must be Asia/Shanghai")
    if not data.get("as_of"): errors.append("missing as_of cut-off")
    if not data.get("title") or not data.get("summary"): errors.append("title/summary missing")
    if not data.get("broadcast_headlines"): errors.append("broadcast headlines missing")
    source_ids = data.get("source_ids", [])
    if len(source_ids) < 10 or len(source_ids) != len(set(source_ids)): errors.append("source IDs missing or duplicated")
    market = data.get("market_data", {})
    if not market.get("a_share", {}).get("indices"): errors.append("A-share index data missing")
    if not market.get("hong_kong", {}).get("indices"): errors.append("Hong Kong index data missing")
    for group in ("a_share", "hong_kong"):
        for row in market.get(group, {}).get("indices", []):
            if "close" not in row or "change_pct" not in row: errors.append(f"{group} missing close/change_pct")
    sources = source_path.read_text(encoding="utf-8")
    if len(re.findall(r"https?://[^)\s]+", sources)) < 10: errors.append("source register needs at least 10 linked sources")
    for sid in source_ids:
        if sid not in sources: errors.append(f"source ID missing from register: {sid}")
    sections = data.get("sections") or {}
    if legacy_html.is_file():
        check_html(legacy_html, "legacy finance article", errors, minimum_links=6, require_focus=False)
    elif not sections:
        errors.append("non-pillar legacy report is missing its HTML article")
    if sections:
        if set(sections) != PILLARS: errors.append(f"expected four pillars, found {sorted(sections)}")
        for slug in sorted(PILLARS & set(sections)):
            section = sections[slug]
            html_path = root / section.get("path", "")
            md_path = root / section.get("content_path", "")
            if not html_path.is_file():
                errors.append(f"{slug}: missing HTML {section.get('path')}")
                continue
            if not md_path.is_file(): errors.append(f"{slug}: missing Markdown {section.get('content_path')}")
            ids = section.get("source_ids", [])
            if len(ids) < 3: errors.append(f"{slug}: needs at least three source IDs")
            for sid in ids:
                if sid not in sources: errors.append(f"{slug}: source ID missing from register: {sid}")
            check_html(html_path, slug, errors)
            page = html_path.read_text(encoding="utf-8")
            for sid in ids:
                if sid not in page: errors.append(f"{slug}: source ID not visible in HTML: {sid}")

    catalog_path = root / "config" / "source-catalog.json"
    if not catalog_path.is_file(): errors.append("missing source-catalog.json")
    else:
        try:
            catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
            groups = catalog.get("groups", [])
            entries = [s for group in groups for s in group.get("sources", [])]
            if len(groups) < 5: errors.append("source catalog needs five groups")
            if len(entries) < 35: errors.append("source catalog needs at least 35 sources")
            for source in entries:
                for field in ("name", "url", "tier", "caveat"):
                    if not source.get(field): errors.append(f"source catalog missing {field}: {source.get('name')}")
        except (json.JSONDecodeError, TypeError) as exc:
            errors.append(f"invalid source catalog: {exc}")

    portal = root / "index.html"
    guide = root / "source-guide" / "index.html"
    if not portal.is_file(): errors.append("main portal index.html missing")
    else:
        portal_text = portal.read_text(encoding="utf-8")
        for slug in PILLARS:
            if f"/{slug}/" not in portal_text: errors.append(f"portal missing {slug} link")
    if not guide.is_file(): errors.append("source guide page missing")
    else:
        guide_text = guide.read_text(encoding="utf-8")
        for word in ("X / Twitter", "Reuters", "求是", "CNA", "Bloomberg"):
            if word not in guide_text: errors.append(f"source guide missing {word}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date")
    parser.add_argument("--print-latest-date", action="store_true")
    args = parser.parse_args()
    if args.print_latest_date:
        dates = report_dates()
        if not dates:
            print("No report dates found", file=sys.stderr)
            return 1
        print(dates[0])
        return 0
    errors = validate(ROOT, args.date)
    if errors:
        for error in errors: print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {args.date or report_dates()[0]} four-pillar bundle, sources, portal and HTML")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
