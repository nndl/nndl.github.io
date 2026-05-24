---
layout: default
title: 扩散模型
permalink: /viz/diffusion/
redirect_from:
  - /v/diffusion/
---

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 扩散模型

扩散模型分为前向加噪与反向去噪两个过程：前向把数据逐步变成纯噪声，反向学习从噪声中恢复出数据。

## 前向 / 反向过程

<figure class="viz-figure viz-figure--wide">
  <img src="https://lilianweng.github.io/posts/2021-07-11-diffusion-models/DDPM.png" alt="DDPM 前向与反向过程" loading="lazy">
  <figcaption>前向过程 q(xₜ|xₜ₋₁) 逐步加噪；反向过程 p_θ(xₜ₋₁|xₜ) 学习去噪。</figcaption>
  <small class="viz-figure__source">来源：Lilian Weng — <a href="https://lilianweng.github.io/posts/2021-07-11-diffusion-models/">What are Diffusion Models?</a></small>
</figure>

## 不同扩散模型对比

<figure class="viz-figure viz-figure--wide">
  <img src="https://lilianweng.github.io/posts/2021-07-11-diffusion-models/generative-overview.png" alt="生成模型对比" loading="lazy">
  <figcaption>扩散模型与 GAN、VAE、流模型在生成质量、训练稳定性、采样速度上的权衡。</figcaption>
  <small class="viz-figure__source">来源：Lilian Weng — <a href="https://lilianweng.github.io/posts/2021-07-11-diffusion-models/">What are Diffusion Models?</a></small>
</figure>

<p class="viz-attr">
  图片来源：Lilian Weng — <a href="https://lilianweng.github.io/posts/2021-07-11-diffusion-models/">What are Diffusion Models?</a>
</p>

## 交互式资源

<div class="resource-grid">
  <a class="resource-card" href="https://poloclub.github.io/diffusion-explainer/" target="_blank" rel="noopener">
    <h3>Diffusion Explainer ↗</h3>
    <p>交互式可视化文本到图像扩散模型（Stable Diffusion）的完整去噪过程。</p>
  </a>
  <a class="resource-card" href="https://github.com/lucidrains/denoising-diffusion-pytorch" target="_blank" rel="noopener">
    <h3>denoising-diffusion-pytorch ↗</h3>
    <p>开源 PyTorch 实现，README 含训练动图。</p>
  </a>
</div>
