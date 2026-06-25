---
layout: default
title: GAN Lab
description: "PoloClub 互动玩具：在浏览器中训练一个 2D GAN，逐步可视化判别器与生成器的对抗。"
permalink: /viz/gan-lab/
redirect_from:
  - /v/gan-lab/
---

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# GAN Lab

由 Georgia Tech PoloClub 与 Google Brain 合作开发的浏览器内 GAN 训练演示：选一个 2D 数据分布，实时看判别器与生成器如何在博弈中收敛——或者崩坏。

<figure class="viz-figure viz-figure--wide">
  <img src="https://raw.githubusercontent.com/poloclub/ganlab/master/ganlab-teaser.png" alt="GAN Lab 主界面" loading="lazy" onerror="this.style.display='none'">
  <figcaption>左侧是真实数据与生成样本的分布对比，右侧是判别器输出的"真伪概率"热图。</figcaption>
  <small class="viz-figure__source">来源：PoloClub — <a href="https://poloclub.github.io/ganlab/">GAN Lab</a></small>
</figure>

## 适合用来直观感受

- 判别器 / 生成器的目标函数是如何相互拉扯的
- **模式崩塌（mode collapse）** 长什么样：生成器把所有真实模式都坍缩到一个点上
- 学习率、噪声维度、网络容量对训练稳定性的影响

## 交互式资源

<div class="resource-grid">
  <a class="resource-card" href="https://poloclub.github.io/ganlab/" target="_blank" rel="noopener">
    <h3>GAN Lab ↗</h3>
    <p>纯浏览器训练 2D GAN，逐步可视化对抗过程。</p>
  </a>
  <a class="resource-card" href="https://github.com/poloclub/ganlab" target="_blank" rel="noopener">
    <h3>源码仓库 ↗</h3>
    <p>TensorFlow.js 实现，可本地运行或二次开发。</p>
  </a>
  <a class="resource-card" href="https://lilianweng.github.io/posts/2017-08-20-gan/" target="_blank" rel="noopener">
    <h3>From GAN to WGAN ↗</h3>
    <p>Lilian Weng 系统梳理 GAN 各变体的损失函数与稳定性技巧。</p>
  </a>
</div>
