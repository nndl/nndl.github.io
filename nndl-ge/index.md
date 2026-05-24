---
layout: book
title: 神经网络与深度学习（通识版）
book_key: ge
permalink: /nndl-ge/
---

{%- assign book = site.data.books | where: "key", page.book_key | first -%}

## 关于本书

《神经网络与深度学习（通识版）》面向更广泛的读者，以更直观的方式介绍神经网络与深度学习的核心思想，弱化数学推导，适合非专业读者、高校通识课与入门学习。

## 与"蒲公英书"的关系

- **蒲公英书（第 2 版）**：理论体系完整，适合系统学习与研究入门。
- **通识版**：聚焦核心思想与直观理解，作为先导读物或通识课教材。

读者可根据自身背景选择：偏直观选通识版，偏系统选第 2 版，二者主题与脉络一致。

## GitHub 仓库

<div class="resource-grid">
  <a class="resource-card" href="{{ book.repo }}/tree/main/{{ book.repo_path }}">
    <h3>{{ book.repo | replace: 'https://github.com/', '' }} <code>/{{ book.repo_path }}</code></h3>
    <p>通识版与理论书 v2 共享同一仓库，独立的 <code>{{ book.repo_path }}/</code> 子目录。</p>
  </a>
</div>

## 内容预告

> *（待补充：章节大纲、面向读者、配套教学资源。）*

## 反馈

本书目前为预告，欢迎通过 <a href="{{ book.repo }}/issues">{{ book.repo | replace: 'https://github.com/', '' }} Issues</a> 提出建议。
