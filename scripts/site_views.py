"""Editorial page renderers for date-first XM News Pages.

All outward-facing strings are escaped, all links are stable date URLs, and
the archive works without JavaScript. Only local assets are loaded.
"""
from __future__ import annotations

import html
from datetime import date
from pathlib import Path

BASE = "https://1998x-stack.github.io/xm-news"
PILLARS = {
    "politics": ("政治与公共治理", "POLITICS", "01"),
    "finance": ("金融与资本市场", "FINANCE", "02"),
    "economy": ("宏观经济与产业", "ECONOMY", "03"),
    "livelihood": ("民生与公共服务", "LIVELIHOOD", "04"),
}


def e(value: object) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


def head(title: str, description: str, style_prefix: str = "assets/") -> str:
    return (
        '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<meta name="description" content="{e(description)[:300]}">'
        f'<title>{e(title)}｜XM News</title>'
        f'<link rel="stylesheet" href="{e(style_prefix)}site.css">'
        '</head><body><a href="#main" class="skip">跳转正文</a>'
    )


def header(active: str = "") -> str:
    home = f"{BASE}/"
    nav = [
        ("首页 · 每日", home, "home"),
        ("历史档案", f"{BASE}/archive/", "archive"),
        ("信源体系", f"{BASE}/source-guide/", "sources"),
    ]
    links = "".join(
        '<a href="' + e(url) + '"' +
        (' aria-current="page"' if active == key else '') +
        '>' + e(label) + '</a>'
        for label, url, key in nav
    )
    return (
        '<header class="site-head"><div class="head-in">'
        f'<a class="logo" href="{home}">XM <span>NEWS</span></a>'
        f'<nav class="global-nav" aria-label="主导航">{links}</nav>'
        '</div></header>'
    )


def footer() -> str:
    return (
        '<footer class="footer"><strong>XM News</strong> · 每日多源新闻观察与证据研究。'
        '<p>日期以 Asia/Shanghai 为准。历史档案保持固定URL，来源与立场有别，'
        '研究推断不等于事实或投资建议。</p>'
        f'<a href="{BASE}/">每日首页</a><a href="{BASE}/source-guide/">来源与方法</a>'
        '<a href="https://github.com/1998x-stack/xm-news">研究仓库</a></footer>'
    )


def _label_date(value: str) -> tuple[str, str]:
    d = date.fromisoformat(value)
    return f"{d.year} / {d.month:02d}", f"{d.day:02d}"


def _day_card(report: dict, prefix: str = "") -> str:
    day = report["date"]
    date_prefix, day_number = _label_date(day)
    has_pillars = bool(report["sections"])
    target = f"{prefix}issues/{day}/" if has_pillars else f"{prefix}posts/{day}/"
    tags = (
        ["政治", "金融", "经济", "民生"]
        if has_pillars else ["旧版金融档案", "尚未补齐四板块"]
    )
    tag_html = "".join(f'<span class="topic-tag">{e(t)}</span>' for t in tags)
    label = "四大板块 · 综合研究" if has_pillars else "历史存档 · 金融专题"
    return (
        f'<a class="day-card" href="{e(target)}" data-date="{e(day)}">'
        f'<div class="day-date"><strong>{day_number}</strong><small>{date_prefix}</small></div>'
        '<div class="day-body">'
        f'<span class="issue-label">{label}</span><h3>{e(report["title"])}</h3>'
        f'<p>{e(report["summary"])}</p><div class="topic-tags">{tag_html}</div>'
        '</div><span class="day-arrow">阅读当日 →</span></a>'
    )


def render_home(reports: list[dict], archive: bool = False) -> str:
    if not reports:
        raise ValueError("daily home needs at least one dated record")
    latest_complete = next((r for r in reports if r["sections"]), None)
    newest = latest_complete or reports[0]
    years = sorted({r["date"][:4] for r in reports}, reverse=True)
    year_options = "".join(f'<option value="{y}">{y} 年</option>' for y in years)
    cards = "".join(_day_card(r, "../" if archive else "") for r in reports)
    prefix = "../assets/" if archive else "assets/"
    intro = (
        "按日期浏览，每个完整日报先呈现当日跨地区核心事件，"
        "再分政治、金融、经济、民生四个独立研究模块。"
    )
    path_prefix = "../" if archive else ""
    latest_target = (
        f"{path_prefix}issues/{newest['date']}/" if newest["sections"]
        else f"{path_prefix}posts/{newest['date']}/"
    )
    latest_block = (
        f'<aside class="hero-side"><span class="eyebrow">LATEST COMPLETE ISSUE</span>'
        f'<time datetime="{e(newest["date"])}">最新完整日期 · {e(newest["date"])}</time>'
        f'<strong>{e(newest["title"])}</strong>'
        f'<p>{e(newest["summary"])}</p>'
        f'<a href="{e(latest_target)}">进入当日研究总览 →</a></aside>'
    )
    title = "全部日期档案" if archive else "每天，都值得重新理解。"
    return (
        head("全部日期" if archive else "每日观察", intro, style_prefix=prefix)
        + header("archive" if archive else "home")
        + '<main class="wrap" id="main">'
        + '<div class="hero"><div><span class="eyebrow">DAILY ARCHIVE / MULTI-SOURCE INTELLIGENCE</span>'
        f'<h1>{title}</h1><p class="intro">{intro}</p>'
        '<p class="small">先选择日期 → 进入当天总览 → 阅读四个专题。'
        '不以任何单一媒体的栏目排序代替事件重要性判断。</p></div>'
        + latest_block + '</div>'
        + '<div class="stat-row"><div class="stat"><b>'
        + str(len(reports)) + '</b><small>已归档日期</small></div>'
        + '<div class="stat"><b>' + str(sum(bool(r["sections"]) for r in reports))
        + '</b><small>四模块完整日报</small></div>'
        + '<div class="stat"><b>3+</b><small>地区观察：中 / 欧美 / 亚洲</small></div></div>'
        + '<section id="daily-archive" aria-labelledby="daily-heading">'
        '<div class="section-title"><h2 id="daily-heading">每日研究时间轴</h2>'
        '<small>从新到旧 · 以报告日期归档</small></div>'
        '<div class="filter-panel"><div class="filter-bar">'
        '<div class="filter-control"><label for="date-filter">精确日期</label>'
        '<input type="date" id="date-filter" autocomplete="off"></div>'
        '<div class="filter-control"><label for="year-filter">年份</label>'
        f'<select id="year-filter"><option value="">全部年份</option>{year_options}</select></div>'
        '<div class="filter-control"><label for="month-filter">月份</label>'
        '<select id="month-filter"><option value="">全部月份</option>'
        + ''.join(f'<option value="{i:02d}">{i}月</option>' for i in range(1, 13))
        + '</select></div><button type="button" class="clear" id="reset-filter">清除筛选</button>'
        '</div><p id="filter-status" class="result-status" role="status" aria-live="polite">'
        f'共 {len(reports)} 个可访问日期</p></div>'
        f'<div class="timeline" id="daily-list">{cards}</div>'
        '<div id="filter-empty" class="empty" hidden><strong>此日期暂无已发布日报。</strong>'
        '<p>可以更改日期或清除筛选。未发布的日期不会生成空页面。</p></div></section>'
        '<section class="method"><h2>我们的研究对象是事件，而不是媒体的目录</h2>'
        '<p>中国原始文件与专业报道、欧美独立媒体、新加坡和其他亚洲地区报道共同进入候选事件池。'
        '再根据重要性、可验证程度和视角差异进行取舍；同一通讯社稿件的转载不重复计算。'
        '每天的日期页展示各地区观察、事件叙事差异和四个专题入口。</p>'
        f'<a href="{BASE}/source-guide/">阅读信源与交叉核验规则 →</a></section>'
        + footer() + '</main>'
        f'<script src="{e(prefix)}filters.js" defer></script>'
        '</body></html>'
    )


def _lens_cards(editorial: dict) -> str:
    lenses = editorial.get("lenses", [])
    if not lenses:
        lenses = [
            {"label": "中国 · 原始信息", "outlets": "待核验", "summary": "本期未记录独立的地区观察摘要。"},
            {"label": "欧美 · 报道与分析", "outlets": "待核验", "summary": "不以媒体名称替代具体来源。"},
            {"label": "新加坡与亚洲 · 区域视角", "outlets": "待核验", "summary": "区域媒体转载须核查稿件来源。"},
        ]
    out = []
    for i, lens in enumerate(lenses[:3], 1):
        out.append(
            f'<div class="lens"><span class="symbol">0{i}</span>'
            f'<h3>{e(lens.get("label", ""))}</h3>'
            f'<span class="outlet">{e(lens.get("outlets", ""))}</span>'
            f'<p>{e(lens.get("summary", ""))}</p></div>'
        )
    return "".join(out)


def _observation_cards(report: dict, editorial: dict) -> str:
    observations = editorial.get("observations") or []
    if not observations:
        return (
            '<div class="event"><div class="meta">存档说明</div>'
            '<h3>本期尚未制作独立事件索引</h3>'
            '<p>四个专题仍可独立阅读。后续日期将按事件归档并提供多地区交叉核验。</p></div>'
        )
    out = []
    for obs in observations[:12]:
        slug = obs.get("pillar", "")
        if slug not in PILLARS:
            continue
        label = PILLARS[slug][0]
        sources = " · ".join(obs.get("source_ids", []))
        out.append(
            '<article class="event">'
            f'<div class="meta"><span>{e(label)}</span>'
            f'<span>{e(obs.get("status", "来源待复核"))}</span></div>'
            f'<h3>{e(obs.get("title", ""))}</h3>'
            f'<p>{e(obs.get("summary", ""))}</p>'
            f'<p>{e(obs.get("perspectives", ""))}</p>'
            f'<div class="sources">证据来源：{e(sources) or "未登记"}'
            f' · {e(obs.get("limitation", ""))}</div>'
            f'<a href="{e(slug)}/">进入{e(label)}专题 →</a>'
            '</article>'
        )
    return "".join(out)


def render_issue(report: dict, reports: list[dict]) -> str:
    if not report["sections"]:
        raise ValueError("legacy report cannot render four-pillar issue hub")
    day = report["date"]
    editorial = report.get("data", {}).get("editorial") or {}
    modules = []
    for slug, (label, en, number) in PILLARS.items():
        section = report["sections"][slug]
        modules.append(
            f'<a class="pillar {slug}" href="{slug}/">'
            f'<span class="num">{number} / {en}</span>'
            f'<h3>{e(label)}</h3>'
            f'<strong>{e(section.get("title", ""))}</strong>'
            f'<p>{e(section.get("summary", ""))}</p>'
            f'<span class="go">查看这一天的专题分析 →</span></a>'
        )
    available = [r["date"] for r in reports if r["sections"]]
    idx = available.index(day)
    previous = available[idx + 1] if idx + 1 < len(available) else None
    following = available[idx - 1] if idx > 0 else None
    adjacent = ""
    if previous:
        adjacent += f'<a href="../{previous}/">← {previous} 较早日报</a>　'
    if following:
        adjacent += f'<a href="../{following}/">{following} 较新日报 →</a>'
    limitations = editorial.get("limitations") or []
    limit_html = "".join(f'<li>{e(item)}</li>' for item in limitations[:6])
    if not limit_html:
        limit_html = '<li>请在各专题页查阅来源证据与数据限制。</li>'
    asof = report.get("data", {}).get("as_of") or "未记录"
    intro = editorial.get("lead") or report["summary"]
    return (
        head(f"{day} 每日综合观察", intro, "../../assets/")
        + header()
        + '<main id="main" class="wrap">'
        f'<div class="breadcrumb"><a href="{BASE}/">每日首页</a><span>/</span>'
        f'<span>{e(day)}</span><span>/</span><span>当日总览</span></div>'
        '<header class="issue-hero"><span class="eyebrow">ONE DAY · MANY PERSPECTIVES</span>'
        f'<div class="issue-date">{e(day)}</div>'
        f'<div class="issue-kicker">这一天，中国、欧美和新加坡等亚洲视角看到了什么？</div>'
        f'<h1>每日核心观察</h1><p class="intro">{e(intro)}</p>'
        f'<p class="asof">报告时区 Asia/Shanghai · 资料截点：{e(asof)} · '
        '已完成日期的档案快照</p></header>'
        '<section aria-labelledby="lenses"><div class="section-title">'
        '<h2 id="lenses">同一天，三个观察角度</h2>'
        '<small>各方报道角色不等于立场排名</small></div>'
        f'<div class="lens-grid">{_lens_cards(editorial)}</div>'
        '<p class="disclosure">来源分布仅展示本期真实采用的证据；转载、翻译与同一官方材料的重复转述不可视作独立验证。</p></section>'
        '<figure class="flow-figure"><svg viewBox="0 0 920 176" role="img" aria-labelledby="flow-title flow-desc" '
        'xmlns="http://www.w3.org/2000/svg">'
        '<title id="flow-title">跨地区事件研究流程</title>'
        '<desc id="flow-desc">中国、欧美与新加坡亚洲三种信息来源，先汇入同一事件池，再分流为政治、金融、经济与民生四个主题。是逻辑示意，不表示数量大小。</desc>'
        '<rect x="6" y="10" width="222" height="45" rx="11" fill="#e6ebe7" stroke="#b6c9bd"/>'
        '<rect x="6" y="65" width="222" height="45" rx="11" fill="#e6ebe7" stroke="#b6c9bd"/>'
        '<rect x="6" y="120" width="222" height="45" rx="11" fill="#e6ebe7" stroke="#b6c9bd"/>'
        '<g font-size="17" fill="#204941" font-weight="700" text-anchor="middle">'
        '<text x="117" y="40">中国原始资料</text><text x="117" y="95">欧美独立报道</text>'
        '<text x="117" y="150">新加坡及亚洲</text></g>'
        '<path d="M228 33 L310 86 M228 88 L310 88 M228 142 L310 90" stroke="#6b9790" stroke-width="2.5" fill="none"/>'
        '<rect x="310" y="56" width="215" height="62" rx="14" fill="#235f5a"/>'
        '<text x="417" y="94" text-anchor="middle" font-weight="800" font-size="20" fill="#fff">可核验事件池</text>'
        '<path d="M525 87 L617 87" stroke="#6b9790" stroke-width="3"/>'
        '<g fill="#f0f3ef" stroke="#b4cac2">'
        '<rect x="617" y="10" width="135" height="66" rx="12"/><rect x="764" y="10" width="135" height="66" rx="12"/>'
        '<rect x="617" y="88" width="135" height="66" rx="12"/><rect x="764" y="88" width="135" height="66" rx="12"/></g>'
        '<g fill="#1c4e47" font-size="18" font-weight="800" text-anchor="middle">'
        '<text x="684" y="51">政治</text><text x="831" y="51">金融</text>'
        '<text x="684" y="129">经济</text><text x="831" y="129">民生</text></g></svg>'
        '<figcaption>研究分流示意：先围绕事件核验各来源，再确定栏目；不是把《新闻联播》或任一媒体的目录照搬为日报目录。</figcaption></figure>'
        '<section aria-labelledby="events-heading"><div class="section-title"><h2 id="events-heading">当天最值得关注的事件</h2>'
        '<small>按议题重要性与核验价值整理</small></div>'
        f'<div class="events">{_observation_cards(report, editorial)}</div></section>'
        '<section aria-labelledby="pillars-heading"><div class="section-title">'
        '<h2 id="pillars-heading">四个领域，深入阅读</h2>'
        '<small>每篇文章有独立证据与反证</small></div>'
        f'<div class="pillar-grid">{"".join(modules)}</div></section>'
        '<section class="method"><h2>阅读提示与证据边界</h2>'
        '<p>日期是事件检索窗口；公布日期、实际发生日期、统计期和交易日分别标明。'
        '国际专业媒体的意见不是事实，官方新闻稿也不是独立结果评估。'
        '没有独立核验的内容标注限制。</p><ul>'
        f'{limit_html}</ul><a href="{BASE}/source-guide/">完整信源体系 →</a>'
        f' · <a href="https://github.com/1998x-stack/xm-news/blob/main/sources/{day}.md">当日证据台账 →</a>'
        '</section><p class="note">'
        + adjacent + '</p>' + footer() + '</main></body></html>'
    )
