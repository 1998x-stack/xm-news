# XM News GitHub Pages 架构

## 1. 目标

将 Git 仓库作为研究数据的权威来源，将 GitHub Pages 作为只读发布层。Pages 不直接发布整个仓库，而由 `scripts/build_site.py` 生成最小公开站点目录。

## 2. 架构

```text
GitHub main
  ├── content/YYYY-MM-DD.md
  ├── data/YYYY-MM-DD.json
  ├── sources/YYYY-MM-DD.md
  └── posts/YYYY-MM-DD/index.html
            │
            ▼
  validate_news.py + pytest + Olah HTML QA
            │
            ▼
  scripts/build_site.py --output dist
            │
            ├── dist/index.html
            ├── dist/archive/index.html
            ├── dist/posts/YYYY-MM-DD/index.html
            ├── dist/latest.json
            ├── dist/sitemap.xml
            ├── dist/robots.txt
            └── dist/404.html
            │
            ▼
  upload-pages-artifact → deploy-pages
            │
            ▼
  https://1998x-stack.github.io/xm-news/
```

## 3. 路由约定

| 页面 | 路由 |
|---|---|
| 首页 | `/` |
| 历史归档 | `/archive/` |
| 最新日报 | `/posts/YYYY-MM-DD/` |
| 最新报告元数据 | `/latest.json` |
| 站点地图 | `/sitemap.xml` |

项目站点预期 URL：`https://1998x-stack.github.io/xm-news/`。

## 4. 发布工作流

工作流使用 GitHub 官方 Pages Actions：
1. checkout 默认分支；
2. 安装 Python；
3. 验证最新日报；
4. 运行测试；
5. 运行 Olah 静态 HTML 检查和 Chromium QA；
6. 运行站点构建脚本；
7. configure-pages；
8. upload-pages-artifact；
9. deploy-pages 到 `github-pages` 环境。

工作流需要 `contents: read`、`pages: write`、`id-token: write`。Pages artifact 只包含 `dist/` 内容，避免将 .agent/.pi Skills、脚本和开发文件发布到站点。

## 5. 首次启用

仓库管理员需在 GitHub 仓库 Settings → Pages → Build and deployment → Source 选择 **GitHub Actions**。添加 workflow 不会自动证明 Pages 已经启用。首次部署成功后，Actions job 的 environment URL 和 GitHub Pages 页面才是实际发布状态依据。

## 6. 安全和缓存

- 不在站点目录中放 API keys、个人资料、私有文件或运行日志。
- 不使用第三方统计、远程字体或非必要 JavaScript。
- 所有外部链接应标明发布方并使用安全的 target/rel 属性。
- sitemap 只登记首页、归档和真实存在的日报页面。
- 历史文章不可被新日报覆盖。
