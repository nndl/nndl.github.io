---
layout: default
title: 主页
description: 邱锡鹏《神经网络与深度学习》《大模型与智能体》系列图书主页
---

<section class="home-hero" aria-labelledby="home-title">
  <div class="home-hero__copy">
    <p class="eyebrow">系列丛书</p>
    <h1 id="home-title"><span class="accent">蒲公英</span>书系列</h1>
    <p class="home-hero__lede">从通识入门、理论主线、实践 notebook，到大模型与智能体前沿，把人工智能学习路径、配套代码和可视化资源汇集在同一入口。作者：<a href="https://xpqiu.github.io/">邱锡鹏</a>。</p>
    <div class="home-hero__actions" aria-label="主页快捷入口">
      <a class="btn btn-primary" href="{{ '/reading-path/' | relative_url }}">阅读路径</a>
      <a class="btn btn-secondary" href="{{ '/viz/' | relative_url }}">可视化资源</a>
    </div>
    <div class="home-hero__stats" aria-label="站点概览">
      <span><strong>{{ site.data.books | size }}</strong>本书</span>
      <span><strong>PDF</strong>开放下载</span>
      <span><strong>GitHub</strong>持续更新</span>
    </div>
  </div>
  <div class="home-hero__visual" aria-label="蒲公英书系列封面">
    <div class="home-hero__shelf">
      {%- for book in site.data.books -%}
        {%- assign cover_webp = book.cover_webp -%}
        {%- unless cover_webp -%}
          {%- assign guessed_cover_webp = book.cover | replace: '.png', '.webp' | replace: '.jpg', '.webp' | replace: '.jpeg', '.webp' -%}
          {%- assign cover_webp_file = site.static_files | where: "path", guessed_cover_webp | first -%}
          {%- if cover_webp_file -%}{%- assign cover_webp = guessed_cover_webp -%}{%- endif -%}
        {%- endunless -%}
        <a class="home-cover home-cover--{{ forloop.index }}" href="{{ book.url | relative_url }}" aria-label="{{ book.title }}">
          <picture>
            {%- if cover_webp -%}<source srcset="{{ cover_webp | relative_url }}" type="image/webp">{%- endif -%}
            <img src="{{ book.cover | relative_url }}" alt="{{ book.title }}" loading="{% if forloop.index <= 2 %}eager{% else %}lazy{% endif %}">
          </picture>
        </a>
      {%- endfor -%}
    </div>
  </div>
</section>

<div class="home-section-head">
  <p class="eyebrow">书目入口</p>
  <h2>按学习阶段选择</h2>
</div>
<section class="book-grid">
  {%- for book in site.data.books -%}
    {%- include book-card.html book=book -%}
  {%- endfor -%}
</section>

<aside class="reading-path-callout">
  <h2>不确定从哪本开始？</h2>
  <p>四本书分别面向不同读者：零基础读者可以从 <a href="{{ '/nndl-ge/' | relative_url }}">通识版</a> 入手；专业学生主修 <a href="{{ '/nndl-v2/' | relative_url }}">第二版</a> 并搭配 <a href="{{ '/nndl-practice/' | relative_url }}">案例与实践</a>；想深入大模型方向则进 <a href="{{ '/llm-agent/' | relative_url }}">大模型与智能体</a>。完整的选书路径与主题对照见 <a href="{{ '/reading-path/' | relative_url }}"><strong>阅读路径与选书建议</strong></a>。</p>
</aside>

## 配套资源

<div class="resource-grid">
  <div class="resource-card resource-card--list">
    <h3><a class="resource-card__heading-link" href="{{ '/viz/' | relative_url }}">可视化资源 <span class="resource-card__go" aria-hidden="true">→</span></a></h3>
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
