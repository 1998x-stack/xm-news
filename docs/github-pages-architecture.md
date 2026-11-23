# XM News GitHub Pages 四大板块架构

源仓库按日期保存四个独立专题；构建器将最新日期复制到稳定根路由，并把每期专题归档到issues/YYYY-MM-DD。

```text
GitHub main
├── index.html
├── sections/YYYY-MM-DD/{politics,finance,economy,livelihood}/index.html
├── content/YYYY-MM-DD/{four pillar markdown}.md
├── data/YYYY-MM-DD.json
├── sources/YYYY-MM-DD.md
├── docs/source-directory.md
├── config/source-catalog.json
└── scripts/build_site.py
       ↓ validation + pytest + Olah static QA + Chromium QA
dist/
├── index.html
├── politics/index.html
├── finance/index.html
├── economy/index.html
├── livelihood/index.html
├── issues/YYYY-MM-DD/{index.html,pillar/index.html}
├── source-guide/index.html
├── source-catalog.json
├── archive/index.html
├── latest.json / sitemap.xml / robots.txt / 404.html
└── posts/YYYY-MM-DD/index.html (legacy finance archive)
       ↓
GitHub Pages Actions
```

## 路由
`/`；`/politics/`；`/finance/`；`/economy/`；`/livelihood/`；`/issues/YYYY-MM-DD/`；`/issues/YYYY-MM-DD/{pillar}/`；`/source-guide/`；`/source-catalog.json`；`/archive/`；`/latest.json`。

## 安全
Pages只上传dist/；不发布.agent/.pi、脚本、测试缓存、个人邮箱、API key和内部配置。页面为自包含HTML/CSS/SVG，不依赖远程字体、外部JS、分析服务或第三方图表API。
