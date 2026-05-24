---
layout: default
title: 优化算法对比
permalink: /v/optimizers/
---

<a class="viz-back" href="{{ '/v/' | relative_url }}">可视化资源</a>

# 优化算法对比

不同优化器在损失面上的轨迹差异：SGD / Momentum / NAG / Adagrad / RMSprop / Adam。

## 三维损失面上的优化轨迹

<figure class="viz-figure viz-figure--wide">
  <img src="{{ '/v/opt-3d.gif' | relative_url }}" alt="三维损失面上的优化器对比" loading="lazy">
  <figcaption>不同优化器在三维损失面上的轨迹对比。</figcaption>
  <small class="viz-figure__source">来源：邱锡鹏 · 原创动画（视频版本：<a href="{{ '/v/opt-3d.mov' | relative_url }}">opt-3d.mov</a>）</small>
</figure>

<p class="viz-attr">
  本页 GIF 由作者制作，原始视频版本：<a href="{{ '/v/opt-3d.mov' | relative_url }}">opt-3d.mov</a>
</p>

## 交互式资源

<div class="resource-grid">
  <a class="resource-card" href="https://distill.pub/2017/momentum/" target="_blank" rel="noopener">
    <h3>Why Momentum Really Works ↗</h3>
    <p>distill.pub 的交互式文章，从凸优化的角度解释动量为什么有效。</p>
  </a>
  <a class="resource-card" href="https://www.ruder.io/optimizing-gradient-descent/" target="_blank" rel="noopener">
    <h3>Sebastian Ruder：梯度下降综述 ↗</h3>
    <p>系统综述 SGD 各变种的数学形式与适用场景。</p>
  </a>
</div>

<p class="viz-attr">
  <em>TODO：可补充鞍点对比、长峡谷损失面等经典场景的二维动图（Alec Radford 等社区版本）。</em>
</p>
