# Publication and email delivery

## 1. Repository bundle

The canonical source of truth is GitHub main:
- `content/YYYY-MM-DD.md`
- `data/YYYY-MM-DD.json`
- `sources/YYYY-MM-DD.md`
- `posts/YYYY-MM-DD/index.html`

Do not overwrite previous dates. For same-day corrections, inspect the current SHA and update the existing bundle. Keep source IDs stable within the report.

## 2. Static Pages build

Run:
```bash
python scripts/build_site.py --output dist
```

The build should create a curated artifact containing:
- `index.html` (latest issue homepage)
- `archive/index.html`
- `posts/YYYY-MM-DD/index.html` (all available articles)
- `404.html`
- `robots.txt`, `sitemap.xml`, `.nojekyll`

Do not publish `.agent/`, `.pi/`, credentials, test caches or source-generation scripts in the Pages artifact. The repository itself may remain public; the Pages artifact is deliberately curated.

## 3. GitHub Pages deployment

- Source: GitHub Actions.
- Trigger: push to main when daily content, site builder, or deployment workflow changes; plus manual workflow dispatch.
- Permissions: contents read, pages write, id-token write.
- Jobs: checkout → install minimal Python → validate daily bundle → build static artifact → configure Pages → upload artifact → deploy.
- Use the `github-pages` environment and expose the real `page_url` output.
- A successful research CI run is not a successful Pages deployment. Verify the deploy workflow run and public URL separately.
- If Pages is not enabled for the repository, a maintainer must select Settings → Pages → Build and deployment → Source → GitHub Actions once.

Expected project URL: `https://1998x-stack.github.io/xm-news/`.
Daily article URL: `https://1998x-stack.github.io/xm-news/posts/YYYY-MM-DD/`.

## 4. Email contract

Recipient: `the recipient configured privately in the automation`.

Subject format: `XM News｜YYYY-MM-DD 核心新闻与市场研究`.

Required body:
1. Date and report cut-off time.
2. Three to five key conclusions, each with a concise evidence/caveat.
3. A-share and Hong Kong close snapshot, explicitly labeled as close/holiday/latest session.
4. One to three important global media items with links.
5. Material risks, conflicts and unavailable data.
6. Latest verified Pages URL and the GitHub HTML fallback.

Send only after the repository commit and deployment state have been checked. If Pages is pending/failed, state that explicitly and link to the GitHub article file. Never send a guessed URL as a verified live page.
