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

## 阅读前提

第一篇"共用基础"（第 1–3 章）会从神经网络与 Transformer 基础讲起，没有深度学习背景的读者也可以直接入门。如果想要更系统的理论铺垫，建议先读 [《神经网络与深度学习》第 2 版]({{ '/nndl-v2/' | relative_url }}) 第 4–8 章。

## 配套资源

<div class="resource-grid">
  <a class="resource-card" href="{{ '/nndl-v2/' | relative_url }}">
    <h3>蒲公英书（第 2 版）</h3>
    <p>系列理论主干，本书第一篇的扩展版本。第 8 章 Transformer、第 13 章大语言模型与智能体两节与本书直接呼应。</p>
  </a>
  <a class="resource-card" href="{{ '/nndl-ge/' | relative_url }}">
    <h3>通识版</h3>
    <p>面向更广读者的入门读本，含独立的大模型与智能体章节。想先建立直观理解再深入本书可以从它入手。</p>
  </a>
  <a class="resource-card" href="{{ '/nndl-practice/' | relative_url }}">
    <h3>案例与实践</h3>
    <p>动手实战教程（PyTorch / PaddlePaddle）。Transformer 实现、训练流程、对齐等部分可以在这里练手。</p>
  </a>
</div>

不确定从哪本入手？看 [**阅读路径与选书建议**]({{ '/reading-path/' | relative_url }})。

## 反馈

本书目前为预告，欢迎通过 <a href="{{ book.repo }}/issues">{{ book.repo | replace: 'https://github.com/', '' }} Issues</a> 提出期待的章节内容、案例或前沿主题。
