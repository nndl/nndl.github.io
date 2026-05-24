---
layout: default
title: CNN Explainer
permalink: /viz/cnn-explainer/
---

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# CNN Explainer

由 Georgia Tech PoloClub 出品的交互式 CNN 解释器：在浏览器中加载一个真实的 Tiny VGG，逐层查看卷积、激活、池化、全连接的每一步张量流动。

<figure class="viz-figure viz-figure--wide">
  <img src="https://poloclub.github.io/cnn-explainer/assets/figures/preview.png" alt="CNN Explainer 主界面" loading="lazy" onerror="this.style.display='none'">
  <figcaption>从输入图像到 softmax 输出的全部中间张量都可滚动浏览，点击任一像素可看到对应的感受野与卷积运算细节。</figcaption>
  <small class="viz-figure__source">来源：PoloClub — <a href="https://poloclub.github.io/cnn-explainer/">CNN Explainer</a></small>
</figure>

## 适合用来理解

- 卷积层的"滑动窗口 + 通道求和"为什么会形成新的特征图
- ReLU / 池化为什么不会改变张量的语义层级
- 全连接层如何把空间特征汇聚为类别 logit

## 交互式资源

<div class="resource-grid">
  <a class="resource-card" href="https://poloclub.github.io/cnn-explainer/" target="_blank" rel="noopener">
    <h3>CNN Explainer ↗</h3>
    <p>原始交互式网页，支持上传图片或选择内置样本。</p>
  </a>
  <a class="resource-card" href="https://github.com/poloclub/cnn-explainer" target="_blank" rel="noopener">
    <h3>源码仓库 ↗</h3>
    <p>Svelte + TensorFlow.js 实现，可本地部署或二次开发。</p>
  </a>
</div>
