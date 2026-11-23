# XM News Source Policy

适用范围：政治、金融、经济、民生。目录见 [source-directory.md](source-directory.md) 和 [source-catalog.json](../config/source-catalog.json)。

- P0：原始文件、官方声明、监管公告、原始统计、法院判决和公司公告。
- P1：国际通讯社和独立新闻报道。
- P2：专业财经、区域媒体、学术研究和智库。
- P3：社交媒体、个人账号、聚合转载和新闻线索。

P0代表直接性，不代表对争议事实的独立裁定；P1/P2也不代表天然中立。解释来源角色、机构立场和局限。

## 独立性
- 多个平台转载同一Reuters/AP/Xinhua稿件只计一条证据链。
- 同一官方稿件的中英文版不算两份独立证据。
- 多家媒体引用同一官方通报，不代表独立验证通报之外的推断。
- 对外交争议尽量收集当事方公开表态和独立报道。
- 对民生问题区分政策目标、地方试点、典型案例和全国统计。

## 证据记录
每个关键claim记录claim_id、source_id、URL、publisher、published_at、retrieved_at、locator、source_type、institutional_position、independence_cluster、status、caveat、access_note、counter_evidence和confidence。

## 社交媒体
X/Twitter、微博、微信公众号、短视频和论坛只作为线索或观点层。账号身份从机构官网反向核验；图片视频检查原始素材、时间、地点和上下文；未经独立核验的帖子不得成为重大事实唯一依据。

## 版权与访问限制
付费文章只总结公开可见摘要、授权转载或公开播客说明。搜索摘要不等于阅读全文，不复制文章全文和第三方图表。
