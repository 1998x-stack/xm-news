# XM News｜每日跨地区新闻观察

**研究单位是“日期中的重要事件”，不是《新闻联播》或任何一家媒体的栏目。**

每天把中国原始资料、欧美报道、新加坡及亚洲区域视角放进同一个候选事件池，先验证事实与独立来源关系，再提取核心事件，最后分为政治、金融、经济、民生四大专题。官方文件说明机构发布了什么；财经新闻和国际通讯社补充采访和机制；区域媒体带来不同议题权重，**不标榜任何来源绝对中立**。

## 入口与三级导航

| 层级 | 路由 | 用途 |
|---|---|---|
| ① 每日首页 | [首页](https://1998x-stack.github.io/xm-news/) | 时间倒序、精确日期、年份和月份筛选 |
| ② 某日总览 | [2026-11-23 示例](https://1998x-stack.github.io/xm-news/issues/2026-11-23/) | 当日核心事件、三个地区观察视角、四板块入口 |
| ③ 日期内专题 | [政治](https://1998x-stack.github.io/xm-news/issues/2026-11-23/politics/) · [金融](https://1998x-stack.github.io/xm-news/issues/2026-11-23/finance/) · [经济](https://1998x-stack.github.io/xm-news/issues/2026-11-23/economy/) · [民生](https://1998x-stack.github.io/xm-news/issues/2026-11-23/livelihood/) | 有独立证据链与可视化解释的专题文章 |

兼容：[归档](https://1998x-stack.github.io/xm-news/archive/)、[信源体系](https://1998x-stack.github.io/xm-news/source-guide/)、[最新政治](https://1998x-stack.github.io/xm-news/politics/)、[最新金融](https://1998x-stack.github.io/xm-news/finance/)、[最新经济](https://1998x-stack.github.io/xm-news/economy/)、[最新民生](https://1998x-stack.github.io/xm-news/livelihood/)。

## 事件驱动流程

\`\`\`text
中国官方及专业报道 ─┐
欧美通讯社、Bloomberg、FT、Economist等 ─┼→ 事件池 → 转载去重 → 证据台账
新加坡CNA、Straits Times、ISEAS及亚洲媒体 ─┤       ↓           ↓
IMF/WTO/ILO等国际数据与核验后的社交线索 ──┘       重要性筛选 → 多方框架对照
                                                           ↓
                       日期索引 → 日期综合总览 → 4个专题深度研究
                                                           ↓
                                   CI + Chromium → Pages → Gmail
\`\`\`

首期2026-11-23事件补强：中新29项合作成果与自贸协定升级谈判、亚洲AI市场调整、德国及欧洲媒体关注的经济与金融风险、中瑞外交、中欧/中墨贸易沟通、A/H股、宏观生产与需求结构、养老托育。对于文章付费墙、市场跨时区和通讯社转载问题保留明确的限制说明。

## 仓库结构

\`\`\`text
index.html                             # GitHub中的每日首页预览
assets/site.css / filters.js           # 本地样式与渐进式时间筛选
scripts/build_site.py                  # 从所有data/YYYY-MM-DD.json构建时间索引
scripts/site_views.py                  # 每日首页/日期总览渲染器
scripts/validate_news.py               # 证据/专题结构检查
data/YYYY-MM-DD.json                   # 结构化每日观察 + editorial事件列表
sources/YYYY-MM-DD.md                  # 独立来源链、局限、冲突
content/YYYY-MM-DD.md                  # 综合提要
content/YYYY-MM-DD/{pillar}.md         # 四份Markdown
sections/YYYY-MM-DD/{pillar}/index.html# 四份HTML正文
posts/YYYY-MM-DD/index.html            # 旧版金融页面，作为存档保留
docs/                                   # 来源政策、SOP、Pages架构
.agent/skills/xm-news-daily-research/  # 研究Skill
.pi/skills/xm-news-daily-research/     # 与.agent字节相同的镜像
\`\`\`

## 构建的 Pages 目录

\`\`\`text
dist/
├── index.html                           # 全部日期（自动更新）
├── archive/index.html                   # 同步的完整日期索引
├── days.json                            # 每日清单
├── issues/YYYY-MM-DD/index.html         # 日期综合总览
├── issues/YYYY-MM-DD/{pillar}/index.html# 日期专题
├── politics/ finance/ economy/ livelihood/ # 最新专题兼容路由
├── source-guide/index.html
├── source-catalog.json
├── assets/site.css, assets/filters.js
└── latest.json, sitemap.xml, robots.txt
\`\`\`

## 验证与发布

\`\`\`bash
python -m pip install -r requirements-dev.txt
python scripts/validate_news.py
python -m pytest -q
LATEST=$(python scripts/validate_news.py --print-latest-date)
for section in politics finance economy livelihood; do
  python .agent/skills/olah-style-paper-posts/scripts/validate.py "sections/$LATEST/$section/index.html"
  python .agent/skills/olah-style-paper-posts/scripts/browser_check.py "sections/$LATEST/$section/index.html" --output "/tmp/xm-news-qa/$section"
done
python scripts/build_site.py --output dist
\`\`\`

只部署 \`dist/\`。不公开邮件地址、账号密钥、自动化配置或代理内部文件。每日北京时间21:00的原定时任务根据[SOP](docs/daily-operating-procedure.md)运行；如果是深夜或早晨人工运行，必须标记非最终日报，不能声称当日市场收盘已经发生。

详细方法：[信源目录](docs/source-directory.md) · [信源证据政策](docs/source-policy.md) · [事件驱动方法](docs/event-first-editorial-policy.md) · [发布架构](docs/github-pages-architecture.md)。

本项目仅为公开信息研究，不构成投资、法律或个人政策执行建议。
