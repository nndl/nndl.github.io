---
layout: default
title: t-SNE 与降维
permalink: /viz/tsne/
redirect_from:
  - /v/tsne/
---

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# t-SNE 与降维

t-SNE（t-distributed Stochastic Neighbor Embedding）是高维数据二维可视化的事实标准。但它的输出有不少容易被误读的"陷阱"——超参数、迭代步数、簇的大小都会改变最终图形的解读。

## 不同 perplexity 下的同一组数据

<figure class="viz-figure viz-figure--wide">
  <img src="https://distill.pub/2016/misread-tsne/thumbnail.jpg" alt="distill.pub How to Use t-SNE Effectively" loading="lazy" onerror="this.style.display='none'">
  <figcaption>原文给出十余组对照实验：同一份高维数据，只改 perplexity 或随机种子，输出的形状就可能截然不同。</figcaption>
  <small class="viz-figure__source">来源：Wattenberg 等 — <a href="https://distill.pub/2016/misread-tsne/">How to Use t-SNE Effectively</a></small>
</figure>

## 看的时候要小心

- **簇大小不代表密度** — t-SNE 会自动放大稀疏簇
- **簇间距离没有几何意义** — 只能看"邻近 / 不邻近"
- **必须看多组超参数** — 单张图容易被自欺欺人地解读

## 交互式资源

<div class="resource-grid">
  <a class="resource-card" href="https://distill.pub/2016/misread-tsne/" target="_blank" rel="noopener">
    <h3>How to Use t-SNE Effectively ↗</h3>
    <p>distill 经典互动文章：拖动 perplexity 与迭代步数，实时看 t-SNE 演化。</p>
  </a>
  <a class="resource-card" href="https://pair-code.github.io/understanding-umap/" target="_blank" rel="noopener">
    <h3>Understanding UMAP ↗</h3>
    <p>Google PAIR 团队对 UMAP 与 t-SNE 的对比与原理图解。</p>
  </a>
  <a class="resource-card" href="https://projector.tensorflow.org/" target="_blank" rel="noopener">
    <h3>TensorFlow Embedding Projector ↗</h3>
    <p>浏览器中加载自己的高维嵌入（如词向量），实时切换 PCA / t-SNE / UMAP。</p>
  </a>
</div>
