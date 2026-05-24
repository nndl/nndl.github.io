---
layout: book
title: 大模型与智能体
book_key: llm-agent
permalink: /llm-agent/
---

{%- assign book = site.data.books | where: "key", page.book_key | first -%}

## 关于本书

《大模型与智能体：从基础原理到系统构建与未来展望》围绕四条主线展开：**共用基础、大模型、智能体、边界与未来**，系统讲解大模型与智能体相关的原理、构建方法与前沿方向。

## GitHub 仓库

<div class="resource-grid">
  <a class="resource-card" href="{{ book.repo }}">
    <h3>{{ book.repo | replace: 'https://github.com/', '' }}</h3>
    <p>章节正文、案例代码、勘误。</p>
  </a>
</div>

## 章节目录

{% for part in book.parts %}
<h3>{{ part.title }}</h3>
<ol>
{% for ch in part.chapters %}  <li value="{{ ch.num }}">{{ ch.title }}</li>
{% endfor %}</ol>
{% endfor %}

## 反馈

本书目前为预告，欢迎通过 <a href="{{ book.repo }}/issues">{{ book.repo | replace: 'https://github.com/', '' }} Issues</a> 提出期待的内容与建议。
