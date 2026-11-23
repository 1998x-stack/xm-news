# AGENTS.md｜XM News v4：每日优先、事件优先

## 不变的导航契约
首页 / 先按日期组织与筛选 → /issues/D/ 看当天主要事件与中国/欧美/新加坡亚洲不同观察 → /issues/D/{politics,finance,economy,livelihood}/ 进入对应日期专题。四个 /{pillar}/ 稳定路由只作为“最新专题”兼容链接，不是首页顶层分类。所有链接必须支持历史日期，不得错误跳转至另一日。

## 调研原则
- 《新闻联播》是众多中国官方信源之一，**绝不作为每日事件索引或研究主轴**。不要求每天必须有其文字稿或节目要闻。
- 先并行搜集不同地区候选重要事件：国内官方和专业媒体；欧美Reuters/AP/AFP/Bloomberg/FT/Economist/WSJ；新加坡CNA/Straits Times/新加坡政府、其他亚洲机构；国际组织和经核验的社交线索。
- 事件选择由公共影响、跨境关联、信息增量、可验证性、结构性重要程度决定，而不是媒体占比配额。
- 同一事件记录独立来源簇。多站转载Reuters或转述同一政府发布不算多个独立来源；媒体所在地不等于中立。
- 源头证据和媒体观点分离：事实/官方说法/媒体分析/我们的推断/假设情景。检索不到的消息坦白留白。
- 付费文章、授权转载、搜索摘要必须明确访问层次；不得声称读到未取得的全文。
- 政治: 各方官方表态与独立调查；金融: 时区、现货/期货、资金流/额度；经济: 统计期和名义/实际；民生: 草案/生效、目标/覆盖、地方样本/全国统计。

## 一期文件契约
- data/D.json 加 \`editorial\`：lead、三个实际观察地区的lenses、精选obs（id/pillar/title/summary/perspectives/source_ids/status/limitation）、跨栏目限制。
- sources/D.md 记录claim及source IDs、证据角色、发布时间、检索时间、独立性、冲突与访问范围。
- content/D.md 和 content/D/{pillar}.md、sections/D/{pillar}/index.html。
- scripts/build_site.py 从完整日期数据自动生成首页和日期Hub；不得手动维护网页日期列表。
- 旧版posts/D保留，档案不删除。必须使用最新远端SHA避免覆盖其他提交。
- .pi/skills/xm-news-daily-research 与.agent镜像一致，遵循vendored Olah的原创SVG、语义HTML、移动端和Chromium QA。

## 发布门槛
1. 先核验来源再写稿，不能编造来源、新闻、市场数据、引用或部署结果。
2. 四份文章均可单独阅读，包含日期返回、4+ H2、原始可访问SVG、来源对照及限制。
3. 首页日期过滤要能精确按日、年、月筛选，JS关闭仍能进入所有日期。日期Hub必须显示三个真实来源观察角度、核心事件和四模块链接。
4. 执行validate_news.py、pytest、四页Olah和Chromium、build_site.py；CI验证并不自动意味着公网部署成功。
5. Pages只上传dist/，仅GitHub main和现有XM News定时任务可改动；不修改cron-news、xm-posts或其他项目。
6. 发信前查Sent防重复，邮件应包括日期Hub与四个有日期的专题链接、风险、完整提交/CI/Pages状态；成功须以Gmail回执为证。

## 非完整交易日
若在北京时间21:00之前手动触发，必须标明PRELIMINARY，不能推断晚间新闻和当天收盘；可只检查、补全已完成上一个日期的资料。完整日报由晚间计划负责。
