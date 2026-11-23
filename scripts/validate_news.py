#!/usr/bin/env python3
"""Validate the latest (or explicitly selected) XM News daily bundle."""
from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]


class ArticleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.h1 = 0
        self.h2 = 0
        self.svg = 0
        self.figures = 0
        self.figcaptions = 0
        self.buttons = 0
        self.external_links = 0
        self.main = 0
        self.viewport = False
        self.meta_description = False
        self.svg_titles = 0
        self.svg_descriptions = 0
        self.ids: set[str] = set()
        self.href_targets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if tag == "h1": self.h1 += 1
        if tag == "h2": self.h2 += 1
        if tag == "svg": self.svg += 1
        if tag == "figure": self.figures += 1
        if tag == "figcaption": self.figcaptions += 1
        if tag == "button": self.buttons += 1
        if tag == "main": self.main += 1
        if tag == "title": pass
        if tag == "meta" and attrs_dict.get("name") == "viewport": self.viewport = True
        if tag == "meta" and attrs_dict.get("name") == "description": self.meta_description = True
        if tag == "svg" and attrs_dict.get("aria-labelledby"): self.svg_titles += 1
        if tag == "a":
            href = attrs_dict.get("href") or ""
            parsed = urlparse(href)
            if parsed.scheme in {"https", "http"}: self.external_links += 1
            if href.startswith("#"): self.href_targets.append(href[1:])
        if attrs_dict.get("id"): self.ids.add(str(attrs_dict["id"]))


def report_dates(root: Path = ROOT) -> list[str]:
    data_dir = root / "data"
    if not data_dir.is_dir():
        return []
    return sorted(
        (path.stem for path in data_dir.glob("*.json") if re.fullmatch(r"\d{4}-\d{2}-\d{2}", path.stem)),
        reverse=True,
    )


def validate(root: Path = ROOT, report_date: str | None = None) -> list[str]:
    errors: list[str] = []
    dates = report_dates(root)
    if not dates:
        return ["no daily JSON files found"]
    selected = report_date or dates[0]
    if selected not in dates:
        return [f"report date not found: {selected}"]
    data_path = root / "data" / f"{selected}.json"
    html_path = root / "posts" / selected / "index.html"
    source_path = root / "sources" / f"{selected}.md"
    content_path = root / "content" / f"{selected}.md"
    for path in (data_path, html_path, source_path, content_path):
        if not path.is_file():
            errors.append(f"missing required file: {path.relative_to(root)}")
    if errors:
        return errors

    try:
        data = json.loads(data_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid JSON: {exc}"]

    if data.get("date") != selected:
        errors.append("JSON date does not match report directory")
    if data.get("timezone") != "Asia/Shanghai":
        errors.append("timezone must be Asia/Shanghai")
    if not data.get("as_of"):
        errors.append("missing as_of timestamp")
    if len(data.get("broadcast_headlines", [])) < 1:
        errors.append("broadcast headlines missing")
    source_ids = data.get("source_ids", [])
    if len(source_ids) < 5 or len(source_ids) != len(set(source_ids)):
        errors.append("source IDs missing or duplicated")

    markets = data.get("market_data", {})
    a_indices = markets.get("a_share", {}).get("indices", [])
    hk_indices = markets.get("hong_kong", {}).get("indices", [])
    if len(a_indices) < 1:
        errors.append("A-share index data missing; use explicit nulls with a documented gap if unavailable")
    if len(hk_indices) < 1:
        errors.append("Hong Kong index data missing; use explicit nulls with a documented gap if unavailable")

    for group_name, rows in (("A-share", a_indices), ("Hong Kong", hk_indices)):
        for row in rows:
            if "change_pct" not in row or "close" not in row:
                errors.append(f"{group_name} index row missing close/change_pct keys: {row.get('name', 'unknown')}")
    for required in ("title", "summary"):
        if not data.get(required):
            errors.append(f"missing report metadata: {required}")

    html_text = html_path.read_text(encoding="utf-8")
    parser = ArticleParser()
    parser.feed(html_text)
    if parser.h1 != 1: errors.append(f"expected exactly one h1, found {parser.h1}")
    if parser.h2 < 4: errors.append(f"expected at least 4 h2 sections, found {parser.h2}")
    if parser.svg < 1: errors.append("expected at least one original SVG figure")
    if parser.figures < 1: errors.append("expected at least one semantic figure")
    if parser.figcaptions < parser.figures: errors.append("every figure must have a figcaption")
    if parser.buttons < 1: errors.append("expected at least one keyboard-operable control")
    if parser.main != 1: errors.append(f"expected exactly one main, found {parser.main}")
    if not parser.viewport: errors.append("missing responsive viewport metadata")
    if not parser.meta_description: errors.append("missing meta description")
    if parser.external_links < 5: errors.append("not enough external source links")
    if "<script src=" in html_text or '<link rel="stylesheet" href="http' in html_text:
        errors.append("external JS/CSS dependency found; daily article should be self-contained")
    missing_targets = sorted(set(parser.href_targets) - parser.ids)
    if missing_targets:
        errors.append(f"broken local anchor targets: {missing_targets}")

    sources = source_path.read_text(encoding="utf-8")
    source_links = re.findall(r"https?://[^)\s]+", sources)
    if len(source_links) < 5:
        errors.append("source register must contain at least 5 linked sources")
    for source_id in source_ids:
        if source_id not in sources:
            errors.append(f"source ID not found in source register: {source_id}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", help="report date YYYY-MM-DD; defaults to latest report")
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
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {args.date or report_dates()[0]} daily bundle, metadata, sources and semantic HTML")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
