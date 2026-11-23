#!/usr/bin/env python3
"""Build a curated, offline-first GitHub Pages artifact from XM News records."""
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
from datetime import date
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
SITE_URL = "https://1998x-stack.github.io/xm-news"


def _read_reports(root: Path) -> list[dict]:
    reports: list[dict] = []
    data_dir = root / "data"
    if not data_dir.is_dir():
        raise FileNotFoundError(f"missing data directory: {data_dir}")
    for path in sorted(data_dir.glob("*.json")):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", path.stem):
            continue
        date.fromisoformat(path.stem)
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("date") != path.stem:
            raise ValueError(f"date mismatch in {path.relative_to(root)}")
        article = root / "posts" / path.stem / "index.html"
        if not article.is_file():
            raise FileNotFoundError(f"missing article for {path.stem}: {article}")
        markdown = root / "content" / f"{path.stem}.md"
        if not markdown.is_file():
            raise FileNotFoundError(f"missing research note for {path.stem}: {markdown}")
        title = data.get("title") or _markdown_title(markdown)
        summary = data.get("summary") or _markdown_summary(markdown)
        reports.append({"date": path.stem, "data": data, "title": title, "summary": summary})
    if not reports:
        raise ValueError("no valid daily report JSON files found")
    return sorted(reports, key=lambda item: item["date"], reverse=True)


def _markdown_title(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return f"XM News {path.stem}"


def _markdown_summary(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith(">") and len(line) > 2:
            return line.lstrip("> ").strip()
    return "当日新闻、市场数据与国际媒体研究摘要。"


def _metric_cards(report: dict) -> str:
    data = report["data"]
    markets = data.get("market_data", {})
    a_indices = markets.get("a_share", {}).get("indices", [])
    hk_indices = markets.get("hong_kong", {}).get("indices", [])
    selected = []
    for name in ("创业板指", "上证指数"):
        row = next((item for item in a_indices if item.get("name") == name), None)
        if row:
            selected.append((name, row.get("change_pct"), f'{row.get("close", "—")}点'))
    for name in ("恒生指数", "恒生科技指数"):
        row = next((item for item in hk_indices if item.get("name") == name), None)
        if row:
            selected.append((name, row.get("change_pct"), f'{row.get("close", "—")}点'))
    turnover = markets.get("a_share", {}).get("turnover_cny_100m")
    if turnover is not None:
        selected.append(("沪深成交额", None, f'{turnover / 10000:.2f}万亿元'))
    cards = []
    for name, change, detail in selected[:5]:
        if change is None:
            value = detail
            cls = ""
        else:
            value = f'{change:+.2f}%'
            cls = "up" if change > 0 else ("down" if change < 0 else "")
        cards.append(
            f'<div class="metric"><span>{html.escape(name)}</span>'
            f'<strong class="{cls}">{html.escape(value)}</strong>'
            f'<small>{html.escape(detail) if change is not None else "当日市场数据"}</small></div>'
        )
    return "\n".join(cards)


def _homepage(latest: dict, reports: list[dict]) -> str:
    report = latest["data"]
    report_date = latest["date"]
    title = html.escape(latest["title"])
    summary = html.escape(latest["summary"])
    as_of = html.escape(str(report.get("as_of", "")))
    top_articles = report.get("international_articles", [])[:3]
    article_items = "".join(
        f'<li><span>{html.escape(str(item.get("publisher", "媒体")))}</span>'
        f'<a href="{html.escape(str(item.get("url", "#")), quote=True)}" rel="noopener">'
        f'{html.escape(str(item.get("title", "未命名文章")))}</a></li>'
        for item in top_articles
    )
    issue_count = len(reports)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{summary}">
<meta property="og:type" content="website"><meta property="og:title" content="XM News｜{title}">
<meta property="og:description" content="{summary}">
<meta property="og:url" content="{SITE_URL}/">
<meta name="theme-color" content="#f8faf8">
<link rel="canonical" href="{SITE_URL}/">
<title>XM News｜每日新闻与全球市场研究</title>
<style>
:root{{--ink:#1e3035;--muted:#607176;--teal:#147f80;--red:#b85b47;--line:#dbe5e1;--paper:#f8faf8;--card:#fff;--wash:#edf5f1}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.75 system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif}}
a{{color:var(--teal);text-underline-offset:.2em}}a:focus-visible{{outline:3px solid var(--teal);outline-offset:3px}}
header{{border-bottom:1px solid var(--line);background:rgba(255,255,255,.88)}}
.topbar{{max-width:1160px;margin:auto;padding:1rem 1.5rem;display:flex;align-items:center;justify-content:space-between;gap:1rem}}
.brand{{font-weight:850;letter-spacing:.12em;color:var(--ink);text-decoration:none}}
.nav{{display:flex;gap:1.1rem;font-size:.9rem}}.nav a{{text-decoration:none}}
main{{max-width:1160px;margin:auto;padding:4rem 1.5rem 6rem}}
.eyebrow{{color:var(--teal);font-size:.76rem;font-weight:800;letter-spacing:.17em}}
.hero{{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(260px,.8fr);gap:2rem;align-items:end}}
h1{{font-size:clamp(2.8rem,7vw,5.6rem);line-height:1.04;letter-spacing:-.055em;margin:.7rem 0 1.2rem;max-width:820px}}
.deck{{font-size:1.12rem;color:var(--muted);max-width:760px}}
.asof{{font-size:.82rem;color:var(--muted)}}
.feature{{border:1px solid var(--line);background:var(--card);border-radius:1.2rem;padding:1.5rem;box-shadow:0 12px 32px rgba(32,48,53,.04)}}
.feature h2{{font-size:1.45rem;line-height:1.4;margin:.4rem 0}}.feature p{{color:var(--muted);font-size:.93rem}}
.actions{{display:flex;gap:.7rem;flex-wrap:wrap;margin-top:1.2rem}}
.link{{display:inline-flex;align-items:center;padding:.65rem .95rem;border-radius:999px;background:var(--teal);color:white;text-decoration:none;font-weight:700;font-size:.9rem}}
.link.secondary{{background:white;color:var(--ink);border:1px solid var(--line)}}
.metrics{{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:.75rem;margin:2.2rem 0}}
.metric{{background:white;border:1px solid var(--line);border-radius:.85rem;padding:.9rem;min-width:0}}
.metric span,.metric small{{display:block;color:var(--muted);font-size:.78rem}}.metric strong{{display:block;font-size:1.45rem;line-height:1.4;overflow-wrap:anywhere}}
.up{{color:var(--teal)}}.down{{color:var(--red)}}
.section-head{{display:flex;align-items:end;justify-content:space-between;gap:1rem;margin:3.6rem 0 1rem}}
h2{{font-size:1.55rem;margin:0;letter-spacing:-.025em}}.section-head p{{margin:0;color:var(--muted);font-size:.85rem}}
.columns{{display:grid;grid-template-columns:1fr 1fr;gap:1rem}}
.card{{background:white;border:1px solid var(--line);border-radius:1rem;padding:1.2rem}}
.card h3{{margin:.1rem 0 .55rem;font-size:1.05rem}}.card p{{margin:.4rem 0;color:var(--muted);font-size:.9rem}}
.list{{padding-left:1.1rem;margin:.6rem 0}}.list li{{margin:.65rem 0}}.list span{{display:block;color:var(--muted);font-size:.74rem}}
.archive{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.7rem}}
.issue{{padding:1rem;border:1px solid var(--line);border-radius:.85rem;background:white;text-decoration:none;color:var(--ink)}}
.issue time{{font-size:.76rem;color:var(--muted)}}.issue strong{{display:block;margin:.25rem 0}}.issue small{{color:var(--muted)}}
footer{{border-top:1px solid var(--line);margin-top:4rem;padding-top:1.2rem;color:var(--muted);font-size:.82rem}}
@media(max-width:760px){{main{{padding:2.5rem 1rem 4rem}}.hero{{grid-template-columns:1fr}}.metrics{{grid-template-columns:repeat(2,minmax(0,1fr))}}.columns,.archive{{grid-template-columns:1fr}}.topbar{{padding:1rem}}}}
@media(prefers-reduced-motion:reduce){{*{{scroll-behavior:auto!important;transition:none!important}}}}
@media print{{header .nav,.actions{{display:none}}main{{padding:0}}.feature,.card,.issue{{break-inside:avoid}}}}
</style>
</head>
<body>
<header><div class="topbar"><a class="brand" href="./">XM NEWS</a><nav class="nav" aria-label="主导航"><a href="archive/">历史日报</a><a href="posts/{report_date}/">最新文章</a><a href="https://github.com/1998x-stack/xm-news">GitHub</a></nav></div></header>
<main>
<div class="hero">
<div><div class="eyebrow">DAILY RESEARCH · CHINA / GLOBAL MARKETS</div>
<h1>把新闻放进证据链，<br>把市场放进长期观察。</h1>
<p class="deck">每日新闻联播、中国与香港权益市场、宏观数据、全球资产和国际媒体的交叉研究。先核验事实，再解释价格，最后记录尚待验证的判断。</p>
<p class="asof">最新一期：{report_date} · 数据截点：{as_of} · 历史日报：{issue_count} 期</p></div>
<section class="feature"><div class="eyebrow">LATEST BRIEFING / {report_date}</div>
<h2>{title}</h2><p>{summary}</p>
<div class="actions"><a class="link" href="posts/{report_date}/">阅读今日研究 →</a><a class="link secondary" href="archive/">浏览历史档案</a></div>
</section></div>
<div class="metrics">{_metric_cards(latest)}</div>
<div class="section-head"><h2>国际媒体观察</h2><p>精选报道 · 原文链接</p></div>
<section class="card"><ul class="list">{article_items or '<li>今日暂无已核验的国际媒体条目。</li>'}</ul></section>
<div class="section-head"><h2>研究方法</h2><p>Evidence first · No fabricated facts</p></div>
<div class="columns">
<section class="card"><h3>信源分层与交叉核验</h3><p>优先政府、监管机构、交易所和原始公告；再用Bloomberg、The Economist、Reuters等独立报道补充背景。付费全文不可见时，明确标注访问范围。</p></section>
<section class="card"><h3>事实与判断分离</h3><p>每个重要结论都保留来源、时间、口径和反证。区分盘中、收盘、期货、官方数据、分析师估算与情景推演。</p></section>
</div>
<div class="section-head"><h2>最近日报</h2><p><a href="archive/">完整归档 →</a></p></div>
<div class="archive">
{''.join(f'<a class="issue" href="posts/{item["date"]}/"><time>{item["date"]}</time><strong>{html.escape(item["title"])}</strong><small>{html.escape(item["summary"][:110])}</small></a>' for item in reports[:6])}
</div>
<footer>XM News · 每日新闻与全球市场研究档案。信息研究用途，不构成投资建议。<br>所有市场数据均需结合交易日期、交易时段、币种与统计口径理解。</footer>
</main>
</body></html>"""


def _archive(reports: list[dict]) -> str:
    items = "".join(
        f'<a class="issue" href="../posts/{item["date"]}/"><time>{item["date"]}</time>'
        f'<strong>{html.escape(item["title"])}</strong><small>{html.escape(item["summary"])}</small></a>'
        for item in reports
    )
    return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="XM News 历史日报归档"><title>历史日报｜XM News</title>
<style>:root{{--ink:#203035;--muted:#607176;--teal:#147f80;--line:#dbe5e1;--paper:#f8faf8}}*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.75 system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif}}main{{max-width:960px;margin:auto;padding:3rem 1.25rem 5rem}}a{{color:var(--teal)}}.brand{{font-weight:800;letter-spacing:.12em;text-decoration:none}}h1{{font-size:clamp(2.4rem,6vw,4rem);line-height:1.1;letter-spacing:-.04em}}p{{color:var(--muted)}}.archive{{display:grid;grid-template-columns:1fr 1fr;gap:.8rem}}.issue{{display:block;background:white;border:1px solid var(--line);border-radius:.9rem;padding:1rem;text-decoration:none;color:var(--ink)}}.issue time,.issue small{{display:block;color:var(--muted);font-size:.82rem}}.issue strong{{display:block;margin:.35rem 0}}@media(max-width:640px){{.archive{{grid-template-columns:1fr}}}}</style></head>
<body><main><a class="brand" href="../">XM NEWS</a><h1>历史日报</h1><p>按发布日期倒序排列。每期报告保留独立正文、结构化数据与来源登记。</p><div class="archive">{items}</div></main></body></html>"""


def _write_site(root: Path, output: Path) -> dict:
    reports = _read_reports(root)
    output.mkdir(parents=True, exist_ok=True)
    (output / "archive").mkdir(parents=True, exist_ok=True)
    (output / "posts").mkdir(parents=True, exist_ok=True)

    for report in reports:
        dest = output / "posts" / report["date"]
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / "posts" / report["date"] / "index.html", dest / "index.html")

    latest = reports[0]
    (output / "index.html").write_text(_homepage(latest, reports), encoding="utf-8")
    (output / "archive" / "index.html").write_text(_archive(reports), encoding="utf-8")
    (output / "404.html").write_text(
        '<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>页面不存在｜XM News</title><body style="font:16px/1.8 system-ui;max-width:720px;margin:12vh auto;padding:1rem;color:#203035"><h1>这期日报暂时不存在</h1><p>请返回首页或查看历史归档。</p><p><a href="./">XM News 首页</a> · <a href="./archive/">历史日报</a></p></body></html>',
        encoding="utf-8",
    )
    (output / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: " + SITE_URL + "/sitemap.xml\n", encoding="utf-8")
    (output / ".nojekyll").write_text("", encoding="utf-8")

    urls = [f"{SITE_URL}/", f"{SITE_URL}/archive/"] + [
        f'{SITE_URL}/posts/{item["date"]}/' for item in reports
    ]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n' + '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += "".join(f"<url><loc>{html.escape(url)}</loc></url>\n" for url in urls)
    sitemap += "</urlset>\n"
    (output / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    latest_payload = {
        "date": latest["date"],
        "title": latest["title"],
        "summary": latest["summary"],
        "homepage": SITE_URL + "/",
        "article": f'{SITE_URL}/posts/{latest["date"]}/',
    }
    (output / "latest.json").write_text(json.dumps(latest_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"latest_date": latest["date"], "reports": len(reports), "output": str(output)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    result = _write_site(args.root.resolve(), args.output.resolve())
    print(f'PASS: built {result["reports"]} reports; latest={result["latest_date"]}; output={result["output"]}')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
