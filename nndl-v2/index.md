---
layout: book
title: 神经网络与深度学习
book_key: theory
permalink: /nndl-v2/
---

{%- assign book = site.data.books | where: "key", page.book_key | first -%}

## 关于本书

《神经网络与深度学习》（即"蒲公英书"）系统介绍了神经网络与深度学习的基础理论、典型模型和应用方法。第 2 版相对第一版进行了全面更新，新增 Transformer、扩散模型、大语言模型等近年来的关键内容。

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
    <p>配套实战教程，含 PyTorch 实现。</p>
  </a>
  <a class="resource-card" href="{{ '/nndl-ge/' | relative_url }}">
    <h3>通识版</h3>
    <p>面向更广读者的入门读本，弱化数学推导。</p>
  </a>
</div>

## 第一版归档

<div class="archive-note">
  <p>第一版 PDF 与勘误保留在 <a href="{{ book.repo }}/tree/main/legacy/nndl-v1">legacy/nndl-v1</a> 目录。</p>
</div>

## 引用

```
邱锡鹏，神经网络与深度学习（第二版），机械工业出版社，https://nndl.github.io/, 2025.
```

```bibtex
@book{qiu2025nndl,
  title     = {神经网络与深度学习（第二版）},
  publisher = {机械工业出版社},
  year      = {2025},
  author    = {邱锡鹏},
  address   = {北京},
  url       = {https://nndl.github.io/},
}
```
