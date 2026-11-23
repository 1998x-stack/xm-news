# XM News｜政治、金融、经济、民生综合研究平台

从金融市场日报升级为四大板块、多元信源、交叉验证和独立专题页面的每日研究平台。

## 在线入口
- 门户：https://1998x-stack.github.io/xm-news/
- 政治：https://1998x-stack.github.io/xm-news/politics/
- 金融：https://1998x-stack.github.io/xm-news/finance/
- 经济：https://1998x-stack.github.io/xm-news/economy/
- 民生：https://1998x-stack.github.io/xm-news/livelihood/
- 信源体系：https://1998x-stack.github.io/xm-news/source-guide/
- 历史归档：https://1998x-stack.github.io/xm-news/archive/

## 四大板块
| 板块 | 研究范围 |
|---|---|
| 政治 | 国内治理、外交、国际关系、安全、法律、监管和公共行政 |
| 金融 | A股、港股、债券、利率、汇率、央行、银行、保险、金融监管和资本流动 |
| 经济 | 生产、消费、投资、贸易、房地产、财政、产业链、能源、企业和生产率 |
| 民生 | 就业、收入、住房、教育、医疗、养老、托育、社保、社区和消费者权益 |

## 信源体系
国内官方：新闻联播、人民日报、求是、新华社、中国政府网、部委、国家统计局、人民银行和交易所。国内专业媒体：财新、第一财经、21世纪经济报道、经济观察报、南方周末、澎湃新闻。欧美：Reuters、AP、AFP、Bloomberg、FT、The Economist、WSJ、BBC、NYT、DW。亚洲：CNA、The Straits Times、Nikkei Asia、SCMP、ISEAS、Fulcrum、East Asia Forum、Lowy。国际组织：IMF、World Bank、OECD、WTO、ILO、WHO、UN、BIS、IEA。X/Twitter只作线索和观点，需核验身份、时间、地点、原始素材和独立来源。

没有任何媒体在所有议题上绝对中立。来源按证据角色、机构属性、独立性和访问限制使用；转载同一通讯社不计多个独立信源。

详细目录：[docs/source-directory.md](docs/source-directory.md) · [机器可读目录](config/source-catalog.json)。

## 仓库结构
```text
xm-news/
├── index.html
├── sections/YYYY-MM-DD/{politics,finance,economy,livelihood}/index.html
├── content/YYYY-MM-DD.md
├── content/YYYY-MM-DD/{politics,finance,economy,livelihood}.md
├── data/YYYY-MM-DD.json
├── sources/YYYY-MM-DD.md
├── docs/source-directory.md / source-policy.md / daily-operating-procedure.md
├── config/source-catalog.json
├── scripts/validate_news.py / build_site.py
├── tests/test_news.py
└── posts/YYYY-MM-DD/index.html  # 旧版金融日报历史档案
```

## 工作流
仓库去重 → 四大板块多源采集 → 证据台账 → 转载去重与交叉验证 → 事实/观点/推断分层 → 四份HTML与Markdown → Olah静态校验与Chromium QA → 构建dist → Pages部署核验 → 邮件交付。

## 本地验证
```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_news.py
python -m pytest -q
LATEST=$(python scripts/validate_news.py --print-latest-date)
for section in politics finance economy livelihood; do
  python .agent/skills/olah-style-paper-posts/scripts/validate.py "sections/$LATEST/$section/index.html"
  python .agent/skills/olah-style-paper-posts/scripts/browser_check.py "sections/$LATEST/$section/index.html" --output "/tmp/xm-news-qa/$section"
done
python scripts/build_site.py --output dist
```

Pages只发布dist/。内容仅供信息研究，不构成投资建议、法律意见或政策执行解释。
