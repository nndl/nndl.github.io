---
layout: default
title: 主页
description: 邱锡鹏《神经网络与深度学习》《大模型与智能体》系列图书主页
---

<section class="home-hero">
  <p class="eyebrow">系列丛书</p>
  <h1><span class="accent">蒲公英</span>书系列</h1>
  <p class="home-hero__lede">一套面向不同读者的人工智能教材：从入门通识，到系统理论，到工程实践，再到大模型与智能体前沿。作者：<a href="https://xpqiu.github.io/">邱锡鹏</a>。</p>
</section>

<section class="book-grid">
  {%- for book in site.data.books -%}
    {%- include book-card.html book=book -%}
  {%- endfor -%}
</section>

## 配套资源

<div class="resource-grid">
  <a class="resource-card" href="{{ '/viz/' | relative_url }}">
    <h3>可视化资源</h3>
    <p>卷积、序列建模、注意力、扩散、优化等概念的动图与交互演示。</p>
  </a>
  <a class="resource-card" href="https://github.com/nndl">
    <h3>各书仓库</h3>
    <p>每本书的章节正文、习题、勘误托管在 nndl 组织下的独立仓库。</p>
  </a>
  <a class="resource-card" href="https://github.com/nndl/nndl/issues">
    <h3>反馈与勘误</h3>
    <p>请到对应书的仓库提交 Issue。理论书 v2 在 <code>nndl/nndl</code>。</p>
  </a>
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
