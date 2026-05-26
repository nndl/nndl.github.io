# nndl.github.io

[蒲公英书系列](https://nndl.github.io) 的导航门户。

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
