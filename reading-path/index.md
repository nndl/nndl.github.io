---
layout: default
title: 阅读路径
description: 蒲公英书系列四本书的阅读顺序、读者画像与组合建议
permalink: /reading-path/
redirect_from:
  - /how-to-read/
  - /roadmap/
---

{%- assign book_theory = site.data.books | where: "key", "theory" | first -%}
{%- assign book_practice = site.data.books | where: "key", "practice" | first -%}
{%- assign book_ge = site.data.books | where: "key", "ge" | first -%}
{%- assign book_llm = site.data.books | where: "key", "llm-agent" | first -%}

<article class="reading-page">
  <section class="reading-hero" aria-labelledby="reading-title">
    <div class="reading-hero__copy">
      <p class="eyebrow">阅读路径</p>
      <h1 id="reading-title">先选对入口，<br><span class="nobreak">再决定深度</span></h1>
      <p class="reading-hero__lede">蒲公英书系列覆盖通识入门、系统理论、动手实践和大模型与智能体专题。四本书不是线性先后关系，而是面向不同读者的四个入口：先看自己要解决什么问题，再选择主线和搭配。</p>
      <div class="reading-hero__actions" aria-label="快速跳转">
        <a class="btn btn-primary" href="#reader-paths">按读者画像选择</a>
        <a class="btn btn-secondary" href="#topic-map">按主题查书</a>
      </div>
      <div class="reading-hero__metrics" aria-label="阅读路径概览">
        <span><strong>4</strong>本书</span>
        <span><strong>5</strong>类读者路径</span>
        <span><strong>2</strong>组核心搭配</span>
      </div>
    </div>

    <div class="reading-hero__visual" aria-label="蒲公英书系列封面">
      <div class="reading-cover-map">
        <a class="reading-cover reading-cover--ge" href="{{ book_ge.url | relative_url }}" aria-label="{{ book_ge.title }}">
          <img src="{{ book_ge.cover | relative_url }}" alt="{{ book_ge.title }}" loading="eager">
          <span>通识入口</span>
        </a>
        <a class="reading-cover reading-cover--theory" href="{{ book_theory.url | relative_url }}" aria-label="{{ book_theory.title }}">
          <img src="{{ book_theory.cover | relative_url }}" alt="{{ book_theory.title }}" loading="eager">
          <span>理论主线</span>
        </a>
        <a class="reading-cover reading-cover--practice" href="{{ book_practice.url | relative_url }}" aria-label="{{ book_practice.title }}">
          <img src="{{ book_practice.cover | relative_url }}" alt="{{ book_practice.title }}" loading="lazy">
          <span>实践篇（第二版）</span>
        </a>
        <a class="reading-cover reading-cover--llm" href="{{ book_llm.url | relative_url }}" aria-label="{{ book_llm.title }}">
          <img src="{{ book_llm.cover | relative_url }}" alt="{{ book_llm.title }}" loading="lazy">
          <span>大模型专题</span>
        </a>
      </div>
    </div>
  </section>

  <section class="reading-section reading-section--tight" aria-labelledby="quick-start">
    <div class="reading-section-head">
      <p class="eyebrow">快速选择</p>
      <h2 id="quick-start">你现在最需要哪一种读法？</h2>
    </div>
    <div class="reading-choice-grid">
      <a class="reading-choice-card" href="{{ book_ge.url | relative_url }}" style="--choice-accent: var(--color-forest);">
        <span class="reading-choice-card__label">理解 AI 全貌</span>
        <strong>从通识版开始</strong>
        <p>适合零基础、跨专业读者、管理者和希望先建立整体版图的学习者。</p>
      </a>
      <a class="reading-choice-card reading-choice-card--primary" href="{{ book_theory.url | relative_url }}" style="--choice-accent: var(--color-accent);">
        <span class="reading-choice-card__label">系统学深度学习</span>
        <strong>以第二版为主线</strong>
        <p>适合专业学生和需要完整理论框架的读者，是系列中最核心的教材。</p>
      </a>
      <a class="reading-choice-card" href="{{ book_practice.url | relative_url }}" style="--choice-accent: var(--color-gold);">
        <span class="reading-choice-card__label">边学边写代码</span>
        <strong>第二版 + 实践篇</strong>
        <p>先读理论，再运行 notebook，用最小实验把模型、训练和调试串起来。</p>
      </a>
      <a class="reading-choice-card" href="{{ book_llm.url | relative_url }}" style="--choice-accent: var(--color-accent-light);">
        <span class="reading-choice-card__label">进入大模型方向</span>
        <strong>转入大模型与智能体</strong>
        <p>适合已经具备神经网络基础，想系统学习预训练、对齐、工具、记忆与治理的人。</p>
      </a>
    </div>
  </section>

  <section class="reading-section" id="reader-paths" aria-labelledby="reader-paths-title">
    <div class="reading-section-head">
      <p class="eyebrow">读者画像</p>
      <h2 id="reader-paths-title">按背景选择主线</h2>
    </div>
    <div class="reading-route-grid">
      <article class="reading-route-card">
        <div class="reading-route-card__head">
          <span class="reading-route-card__tag">A</span>
          <h3>零基础或非专业读者</h3>
          <p>先获得概念地图，不急着进入公式和代码。</p>
        </div>
        <dl class="reading-route-steps">
          <div><dt>先读</dt><dd><a href="{{ book_ge.url | relative_url }}">通识版</a></dd></div>
          <div><dt>再选</dt><dd>想看数学进第二版；想动手进实践篇；想了解前沿进大模型与智能体。</dd></div>
          <div><dt>目标</dt><dd>读完后能说清神经网络、Transformer、扩散模型、智能体和 AI 风险的大致位置。</dd></div>
        </dl>
      </article>

      <article class="reading-route-card reading-route-card--focus">
        <div class="reading-route-card__head">
          <span class="reading-route-card__tag">B</span>
          <h3>计算机或人工智能专业学生</h3>
          <p>以第二版建立体系，用实践篇把抽象模型落到代码。</p>
        </div>
        <dl class="reading-route-steps">
          <div><dt>主线</dt><dd><a href="{{ book_theory.url | relative_url }}">第二版</a>第 1–13 章。</dd></div>
          <div><dt>配套</dt><dd><a href="{{ book_practice.url | relative_url }}">实践篇（第二版）</a>对应章节，重点跑通前 10 章 notebook。</dd></div>
          <div><dt>进阶</dt><dd>读完第 13 章后，转入大模型与智能体做专题学习。</dd></div>
        </dl>
      </article>

      <article class="reading-route-card">
        <div class="reading-route-card__head">
          <span class="reading-route-card__tag">C</span>
          <h3>工程师或已有机器学习基础</h3>
          <p>从能运行、能改动、能复现的材料切入。</p>
        </div>
        <dl class="reading-route-steps">
          <div><dt>先做</dt><dd>实践篇的 PyTorch notebook 和测试。</dd></div>
          <div><dt>再查</dt><dd>遇到推导、优化或模型机制问题，再回第二版对应章节。</dd></div>
          <div><dt>侧重</dt><dd>把线性模型、前馈网络、卷积网络、循环网络、注意力、图神经网络和大模型示例跑通。</dd></div>
        </dl>
      </article>

      <article class="reading-route-card">
        <div class="reading-route-card__head">
          <span class="reading-route-card__tag">D</span>
          <h3>研究生或大模型方向入门</h3>
          <p>先补 Transformer 和训练基础，再主攻大模型与智能体。</p>
        </div>
        <dl class="reading-route-steps">
          <div><dt>补基础</dt><dd>第二版第 1、4、7、8 章，或通识版相关章节。</dd></div>
          <div><dt>主攻</dt><dd><a href="{{ book_llm.url | relative_url }}">大模型与智能体</a>全本。</dd></div>
          <div><dt>回查</dt><dd>需要优化、生成模型、图神经网络等经典基础时，回到第二版。</dd></div>
        </dl>
      </article>

      <article class="reading-route-card reading-route-card--wide">
        <div class="reading-route-card__head">
          <span class="reading-route-card__tag">E</span>
          <h3>高校教师或课程设计者</h3>
          <p>按课程目标组合教材、实验和可视化资源。</p>
        </div>
        <dl class="reading-route-steps reading-route-steps--three">
          <div><dt>通识课</dt><dd>通识版为主，配合<a href="{{ '/viz/' | relative_url }}">可视化资源</a>。</dd></div>
          <div><dt>专业课</dt><dd>第二版第 1–9 章 + 第 13 章，实践篇作为实验环节。</dd></div>
          <div><dt>专题课</dt><dd>大模型与智能体全本，前置补第二版第 8 章或专题书第 2–3 章。</dd></div>
        </dl>
      </article>
    </div>
  </section>

  <section class="reading-section" aria-labelledby="books-position-title">
    <div class="reading-section-head">
      <p class="eyebrow">四本书定位</p>
      <h2 id="books-position-title">同一版图里的不同入口</h2>
    </div>
    <div class="reading-book-map">
      <a class="reading-book-card" href="{{ book_ge.url | relative_url }}">
        <img src="{{ book_ge.cover | relative_url }}" alt="{{ book_ge.title }}" loading="lazy">
        <span>通识版</span>
        <strong>先建立直观图景</strong>
        <p>弱化数学推导，用故事和现象解释 AI 的主要概念。</p>
      </a>
      <a class="reading-book-card reading-book-card--main" href="{{ book_theory.url | relative_url }}">
        <img src="{{ book_theory.cover | relative_url }}" alt="{{ book_theory.title }}" loading="lazy">
        <span>神经网络与深度学习</span>
        <strong>系列理论主线</strong>
        <p>从机器学习基础到 Transformer、强化学习、生成模型，适合系统学习。</p>
      </a>
      <a class="reading-book-card" href="{{ book_practice.url | relative_url }}">
        <img src="{{ book_practice.cover | relative_url }}" alt="{{ book_practice.title }}" loading="lazy">
        <span>实践篇（第二版）</span>
        <strong>把理论变成实验</strong>
        <p>以可运行 notebook 和 sanity test 串联经典模型与大模型示例。</p>
      </a>
      <a class="reading-book-card" href="{{ book_llm.url | relative_url }}">
        <img src="{{ book_llm.cover | relative_url }}" alt="{{ book_llm.title }}" loading="lazy">
        <span>大模型与智能体</span>
        <strong>面向前沿专题</strong>
        <p>系统展开预训练、后训练、对齐、多模态、工具、记忆、规划与治理。</p>
      </a>
    </div>
  </section>

  <section class="reading-section" id="topic-map" aria-labelledby="topic-map-title">
    <div class="reading-section-head">
      <p class="eyebrow">主题索引</p>
      <h2 id="topic-map-title">一个主题该去哪本书找？</h2>
    </div>
    <div class="reading-matrix-wrap">
      <table class="reading-matrix">
        <thead>
          <tr>
            <th>主题</th>
            <th>通识版</th>
            <th>第二版</th>
            <th>实践篇</th>
            <th>大模型与智能体</th>
          </tr>
        </thead>
        <tbody>
          <tr><th>神经网络基础</th><td>直观概念</td><td><strong>完整理论</strong></td><td>代码实现</td><td>简要复习</td></tr>
          <tr><th>前馈、卷积、循环网络</th><td>概念</td><td><strong>完整理论</strong></td><td>代码实现</td><td>按需补充</td></tr>
          <tr><th>Transformer</th><td>直观解释</td><td>推导与机制</td><td>注意力实现</td><td><strong>完整章节</strong></td></tr>
          <tr><th>优化与正则化</th><td>直观理解</td><td><strong>完整理论</strong></td><td>训练实验</td><td>训练系统视角</td></tr>
          <tr><th>大语言模型</th><td>概览</td><td>概览</td><td>入门示例</td><td><strong>核心主题</strong></td></tr>
          <tr><th>预训练、后训练、对齐</th><td>概念</td><td>背景</td><td>少量示例</td><td><strong>核心主题</strong></td></tr>
          <tr><th>工具、记忆、规划、智能体</th><td>概念</td><td>概览</td><td>入门示例</td><td><strong>核心主题</strong></td></tr>
          <tr><th>生成模型、扩散模型</th><td>概念</td><td><strong>完整理论</strong></td><td>按需扩展</td><td>相关背景</td></tr>
          <tr><th>图神经网络</th><td>少量背景</td><td><strong>完整理论</strong></td><td>代码实现</td><td>按需补充</td></tr>
          <tr><th>安全、治理、未来智能系统</th><td>概念</td><td>少量背景</td><td>按需扩展</td><td><strong>完整章节</strong></td></tr>
        </tbody>
      </table>
    </div>
  </section>

  <section class="reading-section" aria-labelledby="combo-title">
    <div class="reading-section-head">
      <p class="eyebrow">组合读法</p>
      <h2 id="combo-title">最常用的三种搭配</h2>
    </div>
    <div class="reading-combo-grid">
      <article class="reading-combo-card">
        <span>理论 + 实战</span>
        <h3>第二版 + 实践篇（第二版）</h3>
        <p>每读完一章理论，就运行对应 notebook。先把模型跑通，再回头看推导和细节。</p>
        <a href="{{ book_theory.url | relative_url }}">进入第二版</a>
      </article>
      <article class="reading-combo-card">
        <span>入门 + 前沿</span>
        <h3>通识版 + 大模型与智能体</h3>
        <p>先用通识版建立全局图景，再用专题书深入大模型、智能体和未来系统。</p>
        <a href="{{ book_ge.url | relative_url }}">进入通识版</a>
      </article>
      <article class="reading-combo-card">
        <span>课程 + 资源</span>
        <h3>教材章节 + 可视化资源</h3>
        <p>讲到卷积、循环网络、注意力、扩散或强化学习时，配合交互演示降低理解门槛。</p>
        <a href="{{ '/viz/' | relative_url }}">查看可视化资源</a>
      </article>
    </div>
  </section>

  <section class="reading-section reading-section--final" aria-labelledby="study-advice-title">
    <div class="reading-section-head">
      <p class="eyebrow">学习建议</p>
      <h2 id="study-advice-title">把阅读变成可持续的学习节奏</h2>
    </div>
    <div class="reading-principles">
      <div>
        <strong>先有脉络</strong>
        <p>先扫目录、章首和章末小结，知道每块知识放在哪里，再回头精读。</p>
      </div>
      <div>
        <strong>理论和代码交替</strong>
        <p>推导看不懂时，先跑一个最小实验；代码跑通后，再回来看公式更容易。</p>
      </div>
      <div>
        <strong>按问题回查</strong>
        <p>不要把四本书当作必须顺序读完的清单。遇到问题时，按主题回到对应书。</p>
      </div>
      <div>
        <strong>及时反馈</strong>
        <p>错别字、推导疑问和代码问题可到对应仓库提交 Issue，或到 <a href="https://github.com/nndl/nndl-discussion/discussions">nndl-discussion</a> 讨论。</p>
      </div>
    </div>
  </section>
</article>
