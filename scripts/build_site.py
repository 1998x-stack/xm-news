#!/usr/bin/env python3
"""Build the curated XM News four-pillar GitHub Pages site."""
from __future__ import annotations
import argparse
import html
import json
import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE_URL = "https://1998x-stack.github.io/xm-news"
PILLARS = ("politics", "finance", "economy", "livelihood")


def safe_path(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if root.resolve() not in path.parents:
        raise ValueError(f"unsafe path: {relative}")
    return path


def read_reports(root: Path) -> list[dict]:
    reports = []
    for path in sorted((root / "data").glob("*.json")):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", path.stem):
            continue
        date.fromisoformat(path.stem)
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("date") != path.stem:
            raise ValueError(f"date mismatch in {path}")
        if not (root / "posts" / path.stem / "index.html").is_file():
            raise FileNotFoundError(f"legacy article missing: {path.stem}")
        if not (root / "content" / f"{path.stem}.md").is_file():
            raise FileNotFoundError(f"executive summary missing: {path.stem}")
        sections = data.get("sections") or {}
        if sections:
            if set(sections) != set(PILLARS):
                raise ValueError(f"{path.stem} must contain exactly four pillars")
            for section in sections.values():
                if not safe_path(root, section["path"]).is_file():
                    raise FileNotFoundError(section["path"])
                if not safe_path(root, section["content_path"]).is_file():
                    raise FileNotFoundError(section["content_path"])
        reports.append({"date": path.stem, "title": data.get("title", path.stem), "summary": data.get("summary", ""), "sections": sections})
    if not reports:
        raise ValueError("no dated reports found")
    return sorted(reports, key=lambda x: x["date"], reverse=True)


def issue_index(report: dict) -> str:
    cards = []
    for i, slug in enumerate(PILLARS, 1):
        section = report["sections"][slug]
        cards.append(f'<a href="{slug}/"><b>0{i} / {slug.upper()}</b><h2>{html.escape(section["title"])}</h2><p>{html.escape(section["summary"])}</p></a>')
    return f"""<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{report['date']}四大专题｜XM News</title><style>body{{margin:0;background:#f7f8f6;color:#1c292d;font:16px/1.7 system-ui;padding:3rem 1rem}}main{{max-width:960px;margin:auto}}a{{color:#356d66}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:1rem}}.grid a{{background:white;border:1px solid #dce4e0;border-radius:1rem;padding:1rem;text-decoration:none;color:#1c292d}}@media(max-width:650px){{.grid{{grid-template-columns:1fr}}}}</style><main><a href="../../">XM NEWS</a><p>{report['date']} · FOUR PILLARS</p><h1>本期四大专题</h1><div class="grid">{"".join(cards)}</div></main></html>"""


def archive_page(reports: list[dict]) -> str:
    items = []
    for report in reports:
        href = f'../issues/{report["date"]}/' if report["sections"] else f'../posts/{report["date"]}/'
        label = "四大专题" if report["sections"] else "历史金融日报"
        items.append(f'<a href="{href}"><time>{report["date"]}</time><strong>{html.escape(report["title"])}</strong><small>{html.escape(report["summary"])} · {label}</small></a>')
    return f"""<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>历史报告｜XM News</title><style>body{{margin:0;background:#f7f8f6;color:#1c292d;font:16px/1.7 system-ui;padding:3rem 1rem}}main{{max-width:960px;margin:auto}}a{{color:#356d66}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:1rem}}.grid a{{background:white;border:1px solid #dce4e0;border-radius:1rem;padding:1rem;text-decoration:none;color:#1c292d}}time,small{{display:block;color:#617176;font-size:.8rem}}@media(max-width:650px){{.grid{{grid-template-columns:1fr}}}}</style><main><a href="../">XM NEWS</a><h1>历史报告</h1><div class="grid">{"".join(items)}</div></main></html>"""


def write_site(root: Path, output: Path) -> dict:
    reports = read_reports(root)
    latest = reports[0]
    for required in (root / "index.html", root / "source-guide" / "index.html", root / "config" / "source-catalog.json"):
        if not required.is_file():
            raise FileNotFoundError(required)
    output.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root / "index.html", output / "index.html")
    urls = [f"{SITE_URL}/", f"{SITE_URL}/archive/", f"{SITE_URL}/source-guide/", f"{SITE_URL}/source-catalog.json"]
    urls += [f"{SITE_URL}/{slug}/" for slug in PILLARS]
    for report in reports:
        day = report["date"]
        old = output / "posts" / day
        old.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / "posts" / day / "index.html", old / "index.html")
        urls.append(f"{SITE_URL}/posts/{day}/")
        if report["sections"]:
            issue = output / "issues" / day
            issue.mkdir(parents=True, exist_ok=True)
            (issue / "index.html").write_text(issue_index(report), encoding="utf-8")
            urls.append(f"{SITE_URL}/issues/{day}/")
            for slug, section in report["sections"].items():
                dest = issue / slug
                dest.mkdir(parents=True, exist_ok=True)
                shutil.copy2(safe_path(root, section["path"]), dest / "index.html")
                urls.append(f"{SITE_URL}/issues/{day}/{slug}/")
                if day == latest["date"]:
                    current = output / slug
                    current.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(safe_path(root, section["path"]), current / "index.html")
    (output / "archive").mkdir(parents=True, exist_ok=True)
    (output / "archive" / "index.html").write_text(archive_page(reports), encoding="utf-8")
    (output / "source-guide").mkdir(parents=True, exist_ok=True)
    shutil.copy2(root / "source-guide" / "index.html", output / "source-guide" / "index.html")
    shutil.copy2(root / "config" / "source-catalog.json", output / "source-catalog.json")
    (output / ".nojekyll").write_text("", encoding="utf-8")
    (output / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    (output / "404.html").write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>404｜XM News</title><body><h1>页面不存在</h1><a href="./">返回首页</a></body></html>', encoding="utf-8")
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += "".join(f"<url><loc>{html.escape(url)}</loc></url>\n" for url in sorted(set(urls)))
    (output / "sitemap.xml").write_text(sitemap + "</urlset>\n", encoding="utf-8")
    latest_json = {"date": latest["date"], "title": latest["title"], "summary": latest["summary"], "homepage": SITE_URL + "/", "issue": f'{SITE_URL}/issues/{latest["date"]}/', "sections": {slug: f"{SITE_URL}/{slug}/" for slug in PILLARS}, "source_guide": SITE_URL + "/source-guide/", "source_catalog": SITE_URL + "/source-catalog.json", "report_count": len(reports)}
    (output / "latest.json").write_text(json.dumps(latest_json, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"latest_date": latest["date"], "reports": len(reports), "pillars": list(latest["sections"]), "output": str(output)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    result = write_site(args.root.resolve(), args.output.resolve())
    print(f'PASS: built {result["reports"]} reports; latest={result["latest_date"]}; pillars={",".join(result["pillars"])}; output={result["output"]}')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
