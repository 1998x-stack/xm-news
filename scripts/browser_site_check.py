#!/usr/bin/env python3
"""Browser QA for dynamic date-first homepage and date-hub routing."""
from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright


def check(root: Path, output: Path) -> None:
    latest = root / "latest.json"
    if not latest.is_file():
        raise AssertionError("latest.json missing")
    import json
    day = json.loads(latest.read_text(encoding="utf-8"))["date"]
    output.mkdir(parents=True, exist_ok=True)
    handler = partial(SimpleHTTPRequestHandler, directory=str(root))
    server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
    Thread(target=server.serve_forever, daemon=True).start()
    origin = f'http://127.0.0.1:{server.server_port}'
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for width in (1440, 390, 360):
            page = browser.new_page(viewport={"width": width, "height": 900}, device_scale_factor=1)
            errors = []
            page.on("pageerror", lambda err: errors.append(str(err)))
            page.goto(origin + "/index.html")
            page.wait_for_load_state("domcontentloaded")
            assert page.locator("h1").count() == 1, "home needs single h1"
            assert page.locator("#daily-list [data-date]").count() >= 1, "home must list dates"
            assert page.locator("#date-filter").count() == 1
            assert page.locator("#year-filter").count() == 1
            assert page.locator("#month-filter").count() == 1
            assert page.locator(f'[data-date="{day}"]').count() == 1
            page.screenshot(path=str(output / f"home-{width}.png"), full_page=True)
            if width == 1440:
                page.locator("#date-filter").fill("2033-01-01")
                assert page.locator("#filter-empty").is_visible(), "unknown date needs empty state"
                assert page.locator("#daily-list .day-card:visible").count() == 0, "invalid filter did not hide cards"
                page.locator("#reset-filter").click()
                assert page.locator("#filter-empty").is_hidden(), "reset must restore list"
                page.locator(f'[data-date="{day}"]').click()
                page.wait_for_load_state("domcontentloaded")
                assert page.locator("h1").count() == 1
                assert page.locator("#lenses").count() == 1, "day hub must compare regions"
                assert page.locator(".lens").count() == 3, "three truthful source lenses required"
                assert page.locator(".event").count() >= 4, "day events missing"
                for slug in ("politics", "finance", "economy", "livelihood"):
                    assert page.locator(f'.pillar[href="{slug}/"]').count() == 1, f"{slug} detail link missing"
                page.screenshot(path=str(output / "day-hub-1440.png"), full_page=True)
                page.locator('.pillar[href="politics/"]').click()
                page.wait_for_load_state("domcontentloaded")
                assert page.locator("h1").count() == 1, "detail article needs one h1"
                assert "来源与交叉核验" in page.locator("body").inner_text(), "detail article missing cross-check"
            else:
                issue = browser.new_page(viewport={"width": width, "height": 820})
                issue.goto(f"{origin}/issues/{day}/")
                assert issue.locator(".lens").count() == 3
                assert issue.locator(".pillar").count() == 4
                issue.screenshot(path=str(output / f"day-hub-{width}.png"), full_page=True)
                assert issue.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 2"), f"day hub horizontal overflow at {width}px"
                issue.close()
            assert not errors, f"JavaScript errors at {width}px: {errors}"
            assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 2"), f"horizontal overflow at {width}px"
            page.close()
        browser.close()
    server.shutdown()
    server.server_close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, default=Path("dist"))
    parser.add_argument("--output", type=Path, default=Path("artifacts/site"))
    args = parser.parse_args()
    check(args.site.resolve(), args.output.resolve())
    print("PASS: daily-home exact date filtering, reset, day hub, four pillar routing, 1440/390/360 responsive QA")


if __name__ == "__main__":
    main()
