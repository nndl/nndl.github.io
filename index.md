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

<aside class="reading-path-callout">
  <h2>不确定从哪本开始？</h2>
  <p>四本书分别面向不同读者：零基础读者可以从 <a href="{{ '/nndl-ge/' | relative_url }}">通识版</a> 入手；专业学生主修 <a href="{{ '/nndl-v2/' | relative_url }}">第 2 版</a> 并搭配 <a href="{{ '/nndl-practice/' | relative_url }}">案例与实践</a>；想深入大模型方向则进 <a href="{{ '/llm-agent/' | relative_url }}">大模型与智能体</a>。完整的选书路径与主题对照见 <a href="{{ '/reading-path/' | relative_url }}"><strong>阅读路径与选书建议</strong></a>。</p>
</aside>

## 配套资源

<div class="resource-grid">
  <div class="resource-card resource-card--list">
    <h3>可视化资源</h3>
    <p>书中关键概念的动图与交互演示：</p>
    <div class="repo-chip-grid">
      <a class="repo-chip" href="{{ '/viz/#第-5-章--卷积神经网络' | relative_url }}">
        <span class="repo-chip__title">卷积</span>
        <code class="repo-chip__repo">第 5 章</code>
      </a>
      <a class="repo-chip" href="{{ '/viz/#第-6-章--循环神经网络' | relative_url }}">
        <span class="repo-chip__title">序列建模</span>
        <code class="repo-chip__repo">第 6 章</code>
      </a>
      <a class="repo-chip" href="{{ '/viz/#第-7-章--网络优化与正则化' | relative_url }}">
        <span class="repo-chip__title">网络优化</span>
        <code class="repo-chip__repo">第 7 章</code>
      </a>
      <a class="repo-chip" href="{{ '/viz/#第-8-章--注意力机制与-transformer' | relative_url }}">
        <span class="repo-chip__title">注意力 / Transformer</span>
        <code class="repo-chip__repo">第 8 章</code>
      </a>
      <a class="repo-chip repo-chip--more" href="{{ '/viz/' | relative_url }}">
        <span class="repo-chip__title">查看全部</span>
        <code class="repo-chip__repo">→</code>
      </a>
    </div>
  </div>
  <div class="resource-card resource-card--list">
    <h3>各书仓库</h3>
    <p>每本书的章节正文、习题、勘误托管在独立仓库：</p>
    <div class="repo-chip-grid">
      {%- for book in site.data.books -%}
        {%- assign repo_slug = book.repo | remove: 'https://github.com/' | remove: 'http://github.com/' | replace: '.git', '' -%}
        <a class="repo-chip" href="{{ book.repo }}" title="到 {{ repo_slug }} 仓库主页">
          <span class="repo-chip__title">{{ book.short_title }}</span>
          <code class="repo-chip__repo">{{ repo_slug }}</code>
        </a>
      {%- endfor -%}
    </div>
  </div>
  <div class="resource-card resource-card--list">
    <h3>反馈与勘误</h3>
    <p>请到对应书的仓库提交 Issue：</p>
    <div class="repo-chip-grid">
      {%- for book in site.data.books -%}
        {%- assign repo_slug = book.repo | remove: 'https://github.com/' | remove: 'http://github.com/' | replace: '.git', '' -%}
        <a class="repo-chip" href="{{ book.repo }}/issues" title="提交 Issue 到 {{ repo_slug }}">
          <span class="repo-chip__title">{{ book.short_title }}</span>
          <code class="repo-chip__repo">{{ repo_slug }}</code>
        </a>
      {%- endfor -%}
    </div>
  </div>
</div>

## 引用

```
邱锡鹏，神经网络与深度学习（第二版），机械工业出版社，https://nndl.ai/, 2026.
```

```bibtex
@book{qiu2026nndl,
  title     = {神经网络与深度学习（第二版）},
  publisher = {机械工业出版社},
  year      = {2026},
  author    = {邱锡鹏},
  address   = {北京},
  url       = {https://nndl.ai/},
}
```
