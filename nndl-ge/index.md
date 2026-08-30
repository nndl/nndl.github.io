---
layout: book
title: 神经网络与深度学习（通识版）
book_key: ge
permalink: /nndl-ge/
redirect_from:
  - /ge/
  - /intro/
---

{%- assign book = site.data.books | where: "key", page.book_key | first -%}

## 关于本书

《神经网络与深度学习（通识版）》面向更广泛的读者，以更直观的方式介绍神经网络与深度学习的核心思想，弱化数学推导，适合非专业读者、高校通识课与入门学习。

本书纸质版即将出版，当前已开放[完整的出版前电子稿]({{ book.pdf }})供读者试读和勘误。

## 与"蒲公英书"的关系

- **蒲公英书（第二版）**：理论体系完整，适合系统学习与研究入门。
- **通识版**：聚焦核心思想与直观理解，作为先导读物或通识课教材。

读者可根据自身背景选择：偏直观选通识版，偏系统选第二版。两本书在机器学习和神经网络基础上相互衔接，通识版的后半部分进一步扩展到大模型、智能体、多模态、科学智能、具身智能与AI治理。完整系列（含案例与实践、大模型与智能体）的选书建议见 [**阅读路径**]({{ '/reading-path/' | relative_url }})。

## GitHub 仓库

<div class="resource-grid">
  <a class="resource-card" href="{{ book.repo }}/tree/main/{{ book.repo_path }}">
    <h3>{{ book.repo | replace: 'https://github.com/', '' }} <code>/{{ book.repo_path }}</code></h3>
    <p>通识版与理论书 v2 共享同一仓库，独立的 <code>{{ book.repo_path }}/</code> 子目录。</p>
  </a>
</div>

## 章节目录

<ol>
{% for ch in book.chapters %}  <li value="{{ ch.num }}">{{ ch.title }}</li>
{% endfor %}</ol>

## 配套资源

<div class="resource-grid">
  <a class="resource-card" href="{{ '/nndl-v2/' | relative_url }}">
    <h3>蒲公英书（第二版）</h3>
    <p>理论体系完整版，含完整数学推导与系统化的模型族谱。学完通识版可直接进阶。</p>
  </a>
  <a class="resource-card" href="{{ '/llm-agent/' | relative_url }}">
    <h3>大模型与智能体</h3>
    <p>专门讲大模型与智能体的姊妹书，主题与通识版后半部分（大语言模型 / 智能体 / 具身智能）衔接。</p>
  </a>
  <a class="resource-card" href="{{ '/nndl-practice/' | relative_url }}">
    <h3>案例与实践</h3>
    <p>动手实战教程。想边读边写代码可以搭配它。</p>
  </a>
</div>

不确定从哪本入手？看 [**阅读路径与选书建议**]({{ '/reading-path/' | relative_url }})。

## 反馈

本书已开放出版前电子稿，欢迎通过 <a href="{{ book.repo }}/issues">{{ book.repo | replace: 'https://github.com/', '' }} Issues</a> 提交勘误，以及对内容和表达方式的改进建议。
