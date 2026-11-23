# XM News｜每日新闻与全球市场研究档案

**把新闻联播、A股/港股、宏观数据与国际主流媒体放进同一套可追溯的研究流程。**

本仓库不是新闻转载站，也不是自动荐股工具。它是一个每日更新的研究档案：先记录事实和来源，再解释市场如何定价，最后用可视化页面呈现证据链。

## 今日入口

- **2026-11-23 可视化日报：** [HTML 页面文件](posts/2026-11-23/index.html)（下载后可直接用浏览器打开；在线 Pages 地址需先完成 Pages 配置）
- **结构化数据：** [data/2026-11-23.json](data/2026-11-23.json)
- **文字研究：** [content/2026-11-23.md](content/2026-11-23.md)
- **来源登记：** [sources/2026-11-23.md](sources/2026-11-23.md)

## 仓库结构

```text
xm-news/
├── AGENTS.md                         # 所有 Agent 必须遵守的研究与发布规则
├── README.md                         # 项目说明、目录和工作流
├── THIRD_PARTY_NOTICES.md            # Skill 来源与版权说明
├── index.html                        # GitHub Pages 首页 / 最新日报入口
├── .agent/skills/olah-style-paper-posts/
│   └── ...                           # Agent 运行时使用的完整 Skill
├── .pi/skills/olah-style-paper-posts/
│   └── ...                           # Pi 运行时使用的完整 Skill
├── content/YYYY-MM-DD.md             # 每日研究正文（事实、解释、判断、风险）
├── data/YYYY-MM-DD.json              # 可供程序读取的结构化市场与新闻数据
├── sources/YYYY-MM-DD.md             # 来源登记、交叉验证、口径与限制
├── posts/YYYY-MM-DD/index.html       # 独立可阅读的可视化日报
├── docs/source-policy.md             # 信源分级、核验、引用和版权规则
├── scripts/validate_news.py          # JSON / HTML / 来源链接静态校验
├── tests/test_news.py                # 回归测试
├── requirements-dev.txt              # 本地开发与 Skill QA 依赖
└── .github/workflows/validate.yml    # PR / push 自动验证
```

## 研究范围

1. **中国政策与新闻联播**：政策发布、经济运行、产业、科技、民生和国际新闻。
2. **中国权益市场**：上证、深证、创业板、科创板、北交所、行业板块、A股成交额。
3. **香港市场**：恒生指数、恒生科技、国企指数、港股成交额及重要公司。
4. **宏观与跨资产**：央行操作、利率、汇率、国债、黄金、能源、工业金属。
5. **国际媒体**：The Economist、Bloomberg、Reuters、AP、FT 等；优先使用可核验的原文或授权转载。
6. **解释与情景**：把政策、基本面、市场结构和投资者行为联系起来，但明确区分事实、推断和情景。

## 每日工作流

```text
搜集原始来源
   ↓
核验日期、时区、市场时段和统计口径
   ↓
建立 evidence ledger（主张—来源—定位—状态）
   ↓
写作：事实 → 背景 → 机制 → 影响 → 不确定性
   ↓
生成 JSON、Markdown 和独立 HTML
   ↓
静态校验 + 浏览器 QA + 人工检查
   ↓
提交 GitHub，核验远端文件与 CI
```

## 快速开始

要求 Python 3.11+：

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_news.py
python -m pytest -q
python .agent/skills/olah-style-paper-posts/scripts/validate.py posts/2026-11-23/index.html
python .agent/skills/olah-style-paper-posts/scripts/browser_check.py posts/2026-11-23/index.html --output /tmp/xm-news-qa
```

Skill 采用离线优先的语义 HTML、内嵌 CSS、原创 SVG、清晰图注和渐进式交互。新闻文章不是学术论文；复用的是其叙事、证据、图示和 QA 方法，不会伪造论文式实验或引用。

## GitHub Pages

仓库根目录已有 `index.html`，可作为 Pages 发布入口。若希望公开网站可访问，请在 GitHub 仓库 Settings → Pages 中选择 GitHub Actions，并检查部署工作流状态。**仅有 HTML 文件或 workflow 不代表 Pages 已经上线。**

## 数据与投资免责声明

- 市场数据必须标注交易日期、时区、盘中/收盘/期货属性和币种。
- 不同媒体的涨跌家数、成交额和板块分类可能有统计口径差异；冲突必须显式说明。
- 不把政策预期写成已经发生的资金流入，不把单日涨跌写成趋势。
- 本仓库内容仅用于信息整理和研究，不构成投资建议、证券推荐或收益承诺。

## 来源与版权

优先链接原始新闻、官方公告和原始数据，不复制付费文章全文。对 Bloomberg、The Economist 等内容只做有限摘要、观点归纳和必要引用，并保留原文链接。Skill 来源和许可状态见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
