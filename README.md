# XM News｜每日新闻与全球市场研究档案

**把新闻联播、A股/港股、宏观数据与国际主流媒体放进一套可追溯、可验证、可持续发布的研究流程。**

XM News 不是新闻转载站，也不是自动荐股工具。它将每日信息流沉淀为结构化研究资产：原始事实、来源证据、市场数据、分析判断、反证和下一交易日观察条件。

## 在线入口

- **GitHub Pages 首页：** https://1998x-stack.github.io/xm-news/
- **历史日报：** https://1998x-stack.github.io/xm-news/archive/
- **最新文章：** 进入首页查看最新一期；单期路径为 `/posts/YYYY-MM-DD/`
- **GitHub 仓库：** https://github.com/1998x-stack/xm-news

> 首次启用 Pages 时，仓库管理员需要在 Settings → Pages → Build and deployment → Source 中选择 **GitHub Actions**。Pages workflow 成功部署前，预期 URL 不等于已上线 URL。

## 项目结构

```text
xm-news/
├── AGENTS.md
├── README.md
├── THIRD_PARTY_NOTICES.md
├── .agent/skills/
│   ├── olah-style-paper-posts/       # 上游视觉叙事 Skill，原样 vendored
│   └── xm-news-daily-research/       # 新闻研究项目专用 Skill
├── .pi/skills/                       # 与 .agent 对应副本保持一致
├── content/YYYY-MM-DD.md             # 完整中文研究正文
├── data/YYYY-MM-DD.json              # 结构化事实、市场数据、文章与 source IDs
├── sources/YYYY-MM-DD.md             # 证据台账、来源定位、访问限制
├── posts/YYYY-MM-DD/index.html       # 单期可视化文章
├── docs/
│   ├── source-policy.md
│   ├── daily-operating-procedure.md
│   └── github-pages-architecture.md
├── scripts/
│   ├── validate_news.py              # 动态日期日报校验
│   └── build_site.py                 # 构建 curated Pages artifact
├── tests/
│   └── test_news.py
├── .github/workflows/
│   ├── validate.yml
│   └── deploy-pages.yml
├── index.html                        # 仓库内预览入口
└── dist/                             # 本地/CI生成，gitignored，不提交
```

## 研究覆盖

1. **新闻联播与中国政策：** 央视新闻、国务院、部委、央行、外汇局、国家统计局、能源局及监管机构。
2. **A股：** 上证、深证、创业板、沪深300、科创板、北交所、成交额、涨跌广度和行业结构。
3. **港股：** 恒生、恒生科技、国企指数、主板成交及重要公司。
4. **宏观与跨资产：** 公开市场操作、Shibor、国债收益率、人民币汇率、黄金、原油和工业金属。
5. **国际媒体：** The Economist、Bloomberg、Reuters、AP、FT 等。
6. **综合分析：** 政策—产业—盈利—估值—市场结构传导，明确区分事实、媒体观点、推断与情景。

## 每日研究流程

```text
读取仓库现状 / 去重
        ↓
新闻、政策、市场与国际媒体搜索
        ↓
来源分层、发布时间与市场时段核验
        ↓
Evidence Ledger：主张—来源—定位—状态—限制
        ↓
事实 → 背景 → 机制 → 影响 → 反证 → 观察条件
        ↓
Markdown + JSON + Sources + HTML/SVG
        ↓
动态校验 + 单元测试 + Chromium 多视口 QA
        ↓
构建 curated Pages artifact
        ↓
GitHub Actions 部署 + 公网访问核验
        ↓
邮件发送核心结论与最新可验证网页链接
```

详细门禁见 [每日研究与发布 SOP](docs/daily-operating-procedure.md)，视觉/研究规范见 `.agent/skills/xm-news-daily-research/SKILL.md`。

## 本地开发与验证

要求 Python 3.11+：

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_news.py
python -m pytest -q
LATEST=$(python scripts/validate_news.py --print-latest-date)
python .agent/skills/olah-style-paper-posts/scripts/validate.py "posts/$LATEST/index.html"
python .agent/skills/olah-style-paper-posts/scripts/browser_check.py "posts/$LATEST/index.html" --output "/tmp/xm-news-qa/$LATEST"
python scripts/build_site.py --output dist
```

## GitHub Pages 发布

Pages 使用 GitHub Actions，不直接发布整个仓库。构建器从 `data/`、`content/`、`sources/` 和 `posts/` 读取数据，生成首页、历史归档、日报、404、robots、sitemap 和 latest.json 到 `dist/`。Skills、测试脚本、开发文档和仓库配置不会被打包进网站。

- 架构说明：[docs/github-pages-architecture.md](docs/github-pages-architecture.md)
- 部署工作流：[.github/workflows/deploy-pages.yml](.github/workflows/deploy-pages.yml)
- 站点预期 URL： https://1998x-stack.github.io/xm-news/

## 质量与版权

- 每个重要事实都要有来源 ID；市场数据必须带日期、时区、币种、单位和交易时段。
- 数据冲突要保留口径差异，不得用平均值制造确定性。
- 期货不是现金市场收盘；融资空间不是实际资金流入；单日涨跌不是趋势。
- 不复制付费文章全文，不复制第三方图表；使用原创中文摘要与原创 SVG。
- 不把个人邮箱、API key、令牌或私有运行配置写入公开仓库。
- 所有内容仅用于信息研究，不构成投资建议。
