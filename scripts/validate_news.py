#!/usr/bin/env python3
"""Validate the daily research JSON, semantic HTML, and source register."""
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-11-23"


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
        self.title = False
        self.viewport = False
        self.main = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if tag == "h1": self.h1 += 1
        if tag == "h2": self.h2 += 1
        if tag == "svg": self.svg += 1
        if tag == "figure": self.figures += 1
        if tag == "figcaption": self.figcaptions += 1
        if tag == "button": self.buttons += 1
        if tag == "main": self.main = True
        if tag == "meta" and attrs_dict.get("name") == "viewport": self.viewport = True
        if tag == "a":
            parsed = urlparse(attrs_dict.get("href") or "")
            if parsed.scheme in {"https", "http"}: self.external_links += 1


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    data_path = root / "data" / f"{DATE}.json"
    html_path = root / "posts" / DATE / "index.html"
    source_path = root / "sources" / f"{DATE}.md"
    for path in (data_path, html_path, source_path):
        if not path.is_file():
            errors.append(f"missing required file: {path.relative_to(root)}")
    if errors:
        return errors

    try:
        data = json.loads(data_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid JSON: {exc}"]

    if data.get("date") != DATE:
        errors.append("JSON date does not match report directory")
    if data.get("timezone") != "Asia/Shanghai":
        errors.append("timezone must be Asia/Shanghai")
    if not data.get("as_of"):
        errors.append("missing as_of timestamp")
    if len(data.get("broadcast_headlines", [])) != 16:
        errors.append("expected 16 broadcast headline items")
    if len(data.get("source_ids", [])) < 10:
        errors.append("expected at least 10 registered source IDs")

    markets = data.get("market_data", {})
    a_indices = markets.get("a_share", {}).get("indices", [])
    hk_indices = markets.get("hong_kong", {}).get("indices", [])
    if len(a_indices) < 5:
        errors.append("A-share index series incomplete")
    if len(hk_indices) != 3:
        errors.append("expected 3 Hong Kong indices")
    if not any(x.get("name") == "创业板指" and x.get("change_pct") == 3.08 for x in a_indices):
        errors.append("ChiNext close/change mismatch")
    if not any(x.get("name") == "恒生指数" and x.get("change_pct") == -0.12 for x in hk_indices):
        errors.append("Hang Seng close/change mismatch")
    if data.get("macro_and_policy", {}).get("margin_rule_effective_date") != "2026-11-30":
        errors.append("margin rule effective date missing or incorrect")

    html = html_path.read_text(encoding="utf-8")
    parser = ArticleParser()
    parser.feed(html)
    if parser.h1 != 1: errors.append(f"expected exactly one h1, found {parser.h1}")
    if parser.h2 < 5: errors.append(f"expected at least 5 h2 sections, found {parser.h2}")
    if parser.svg < 3: errors.append(f"expected at least 3 SVG figures, found {parser.svg}")
    if parser.figures < 3: errors.append(f"expected at least 3 semantic figures, found {parser.figures}")
    if parser.figcaptions < parser.figures: errors.append("every figure must have a figcaption")
    if parser.buttons < 2: errors.append("expected at least two working filter buttons")
    if not parser.main: errors.append("missing semantic main")
    if not parser.viewport: errors.append("missing responsive viewport metadata")
    if parser.external_links < 8: errors.append("not enough external source links")
    if "<script src=" in html or '<link rel="stylesheet" href="http' in html:
        errors.append("external JS/CSS dependency found; daily article should be self-contained")

    sources = source_path.read_text(encoding="utf-8")
    source_links = re.findall(r"https?://[^)\s]+", sources)
    if len(source_links) < 10:
        errors.append("source register must contain at least 10 linked sources")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("PASS: daily JSON, semantic HTML, figures, interactions and source register")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
