# nndl.github.io

[蒲公英书系列](https://nndl.ai) 的导航门户（旧域 `nndl.github.io` 会自动 301 到 `nndl.ai`；备用域 `nndl.tech` 整域转发至此）。

本仓库是 [nndl 组织](https://github.com/nndl) 下系列图书的总入口。每本书的章节正文、习题、勘误托管在各自的仓库：

| 书 | 仓库 |
|---|---|
| 神经网络与深度学习（v2） | [nndl/nndl](https://github.com/nndl/nndl) `v2/` |
| 通识版 | [nndl/nndl](https://github.com/nndl/nndl) `ge/` |
| 案例与实践 | [nndl/nndl-practice](https://github.com/nndl/nndl-practice) |
| 大模型与智能体 | [nndl/llm-agent](https://github.com/nndl/llm-agent) |

## 本地开发

```sh
bundle install
bundle exec jekyll serve
# 或：pwsh -File scripts/dev.ps1
```

## 更新书目元数据

`_data/books.yml` 由 `scripts/aggregate-books.py` 从各书仓库的 `_meta.yml` 聚合生成：

```sh
python scripts/aggregate-books.py
```

工作流：编辑某本书的 `_meta.yml`（在它自己的仓库里）→ 跑脚本 → commit 主站的 `_data/books.yml` 变更。

> 当前阶段：per-book 仓库的 `_meta.yml` 尚未建立，`_data/books.yml` 为手工维护初始版本。脚本运行时若所有 `_meta.yml` 缺失，会跳过覆写。

## GitHub Star 计数

书卡和导航上的 star 数从 `_data/gh_stars.yml` 静态渲染，浏览器端不再依赖 `api.github.com`（国内访客经常被 60 req/h 限流挡掉）。

`_data/gh_stars.yml` 已被 gitignore，不进 git history。`.github/workflows/pages.yml` 在每次部署时临时拉取 stars 并 `jekyll build`，产物部署到 Pages：

- 每次 push 到 `main` 触发
- 每天北京时间中午 12:00 定时刷新（cron `0 4 * * *`）
- Actions 页面可手动 `Run workflow`

> **一次性配置**：仓库 Settings → Pages → Source 改为 `GitHub Actions`（默认是 `Deploy from branch`，必须切换否则这个 workflow 不会被 Pages 当部署来源）。Workflow permissions 不用改，默认就够。

### 本地预览要带 star 数？

`_data/gh_stars.yml` 默认不存在，本地 `jekyll serve` 看到的徽章是 `—`。要本地预渲染：

```sh
python scripts/fetch-gh-stars.py                # 60 req/IP/h，可能被限流
GITHUB_TOKEN=ghp_xxx python scripts/fetch-gh-stars.py    # 5000 req/h，必走通
```

脚本读 `_data/books.yml` 收集仓库 slug + `nndl/nndl`（导航），写入 `_data/gh_stars.yml`；fetch 失败保留旧值。生成的文件不会被 commit。
