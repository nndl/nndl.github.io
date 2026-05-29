---
layout: book
title: 神经网络与深度学习
book_key: theory
permalink: /nndl-v2/
redirect_from:
  - /nndl2/
---

{%- assign book = site.data.books | where: "key", page.book_key | first -%}

## 关于本书

《神经网络与深度学习》（即"蒲公英书"）系统介绍了神经网络与深度学习的基础理论、典型模型和应用方法。第二版相对第一版进行了全面更新，新增 Transformer、扩散模型、大语言模型等近年来的关键内容。

## GitHub 仓库

<div class="resource-grid">
  <a class="resource-card" href="{{ book.repo }}">
    <h3>{{ book.repo | replace: 'https://github.com/', '' }}</h3>
    <p>章节正文、习题、勘误。第二版（v2）内容在 <code>{{ book.repo_path }}/</code> 子目录。</p>
  </a>
  <a class="resource-card" href="{{ book.repo }}/issues">
    <h3>勘误与反馈</h3>
    <p>通过 GitHub Issues 提交意见与勘误。</p>
  </a>
</div>

## 章节目录

{% for part in book.parts %}
<h3>{{ part.title }}</h3>
<ol>
{% for ch in part.chapters %}  <li value="{{ ch.num }}">{{ ch.title }}</li>
{% endfor %}</ol>
{% endfor %}
{% if book.appendix %}
<h3>附录</h3>
<ul>
{% for ap in book.appendix %}  <li>{{ ap.title }}</li>
{% endfor %}</ul>
{% endif %}

## 配套资源

<div class="resource-grid">
  <a class="resource-card" href="{{ '/nndl-practice/' | relative_url }}">
    <h3>案例与实践</h3>
    <p>配套实战教程，含 PyTorch 实现。想边读边写代码可以搭配它。</p>
  </a>
  <a class="resource-card" href="{{ '/nndl-ge/' | relative_url }}">
    <h3>通识版</h3>
    <p>面向更广读者的入门读本，弱化数学推导。预习或科普可从它入手。</p>
  </a>
  <a class="resource-card" href="{{ '/llm-agent/' | relative_url }}">
    <h3>大模型与智能体</h3>
    <p>专门讲大模型与智能体的姊妹书。学完本书第 8 章（注意力机制与 Transformer）和第 13 章（大语言模型与智能体）后可深入这本。</p>
  </a>
</div>

> 想了解本书与系列内其他几本的差别、判断哪本更适合自己？参考 [**阅读路径与选书建议**]({{ '/reading-path/' | relative_url }})。

## 第一版归档

<div class="archive-note">
  <p>第一版 PDF 与勘误保留在 <a href="{{ book.repo }}/tree/main/legacy/nndl-v1">legacy/nndl-v1</a> 目录。</p>
</div>
