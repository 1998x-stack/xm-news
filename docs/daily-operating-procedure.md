# XM News 四大板块每日研究与发布 SOP

版本2.0 · Asia/Shanghai · 每天21:00交付。

## 每日交付物
- 门户：index.html
- 四专题：sections/YYYY-MM-DD/{politics,finance,economy,livelihood}/index.html
- 四份正文：content/YYYY-MM-DD/{politics,finance,economy,livelihood}.md
- 综合摘要：content/YYYY-MM-DD.md
- 结构化数据：data/YYYY-MM-DD.json
- 来源台账：sources/YYYY-MM-DD.md
- 长期信源目录：docs/source-directory.md、config/source-catalog.json
- 旧版posts/YYYY-MM-DD/index.html保留为历史金融日报。

## 执行时序
18:30–19:00 仓库检查与议程；19:00–19:40 多源采集；19:40–20:10 四板块证据台账和交叉核验；20:10–20:30 分析、反证和风险；20:30–20:45 生成HTML/Markdown/JSON；20:45–20:55 测试和浏览器QA；20:55–21:00 提交、Pages核验和邮件。21:00后发布的重要信息不倒填已截稿报告。

## 四大板块
政治：国内治理、外交、国际关系、安全、法律、监管和行政改革。
金融：A/H股、债券、利率、汇率、央行、银行、保险、基金、金融监管和资本流动。
经济：生产、消费、投资、贸易、房地产、财政、产业链、能源、企业和生产率。
民生：就业、收入、住房、教育、医疗、养老、托育、社保、公共安全、社区治理和消费者权益。

## 多元信源
详见 [信源目录](source-directory.md)。国内原始来源：新闻联播、人民日报、求是、新华社、中国政府网、部委、统计局、央行、交易所。欧美：Reuters、AP、AFP、Bloomberg、FT、The Economist、WSJ、BBC。区域：CNA、Straits Times、Nikkei Asia、SCMP、ISEAS、East Asia Forum、Lowy。国际组织：IMF、World Bank、OECD、WTO、ILO、WHO、UN、BIS、IEA。X/Twitter只作线索和观点。
重大claim优先组合“原始材料 + 独立报道/数据源 + 区域/专业视角”。无法满足时说明缺口；同一通讯社转载不算独立来源。

## HTML要求
每页包含核心结论、日期/截点、3–4个指标、时间线或原创SVG、事实与背景、来源比较、机制与反证、风险/限制、下一步观察和来源链接。独立可读、单一H1、语义化H2、移动端适配、键盘焦点、打印和减少动态效果样式。禁用外部JS、远程字体、分析脚本和第三方图表。

## 编辑边界
《求是》、人民日报评论作为官方思想/机构立场；付费文章只用公开摘要/授权转载/公开播客；不把草案写成生效法规，不把地方试点写成全国覆盖；不把期货当现货收盘，不把理论融资空间当实际资金流；事实、官方表述、媒体观点、推断和情景分开。

## QA与发布
```bash
python scripts/validate_news.py
python -m pytest -q
LATEST=$(python scripts/validate_news.py --print-latest-date)
for section in politics finance economy livelihood; do
  python .agent/skills/olah-style-paper-posts/scripts/validate.py "sections/$LATEST/$section/index.html"
  python .agent/skills/olah-style-paper-posts/scripts/browser_check.py "sections/$LATEST/$section/index.html" --output "/tmp/xm-news-qa/$section"
done
python scripts/build_site.py --output dist
```
Pages只发布dist/。分别核验validate、deploy-pages、head SHA、部署结论和公网URL。邮件包含四板块结论、风险、门户和四专题链接、commit/CI/Pages状态。收件人保存在自动化私有配置。失败/未执行/pending/成功严格区分。
