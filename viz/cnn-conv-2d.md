---
layout: default
title: 二维卷积演示
permalink: /viz/cnn-conv-2d/
redirect_from:
  - /v/cnn-conv-2d/
---

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 二维卷积

不同卷积核大小 `m`、零填充 `p`、步长 `s` 下二维卷积的滑动过程。

<div class="figure-grid figure-grid--2col">
  <figure class="viz-figure">
    <img src="{{ '/viz/cnn-in_5_out_3_p_0_s_0.gif' | relative_url }}" alt="二维卷积 m=3, p=0, s=1" loading="lazy">
    <figcaption><code>m = 3</code> · <code>p = 0</code> · <code>s = 1</code></figcaption>
    <small class="viz-figure__source">来源：<a href="https://github.com/vdumoulin/conv_arithmetic">vdumoulin/conv_arithmetic</a>（MIT）</small>
  </figure>
  <figure class="viz-figure">
    <img src="{{ '/viz/cnn-in_5_out_4_p_2_s_2.gif' | relative_url }}" alt="二维卷积 m=3, p=2, s=2" loading="lazy">
    <figcaption><code>m = 3</code> · <code>p = 2</code> · <code>s = 2</code></figcaption>
    <small class="viz-figure__source">来源：<a href="https://github.com/vdumoulin/conv_arithmetic">vdumoulin/conv_arithmetic</a>（MIT）</small>
  </figure>
  <figure class="viz-figure">
    <img src="{{ '/viz/cnn-in_3_out_5.gif' | relative_url }}" alt="二维卷积 m=3, p=2, s=1" loading="lazy">
    <figcaption><code>m = 3</code> · <code>p = 2</code> · <code>s = 1</code></figcaption>
    <small class="viz-figure__source">来源：<a href="https://github.com/vdumoulin/conv_arithmetic">vdumoulin/conv_arithmetic</a>（MIT）</small>
  </figure>
  <figure class="viz-figure">
    <img src="{{ '/viz/cnn-in_9_out_5.gif' | relative_url }}" alt="二维卷积 m=5, p=2, s=2" loading="lazy">
    <figcaption><code>m = 5</code> · <code>p = 2</code> · <code>s = 2</code></figcaption>
    <small class="viz-figure__source">来源：<a href="https://github.com/vdumoulin/conv_arithmetic">vdumoulin/conv_arithmetic</a>（MIT）</small>
  </figure>
</div>

<div class="viz-legend">
  <span><code>m</code> 卷积核大小</span>
  <span><code>p</code> 零填充（zero-padding）</span>
  <span><code>s</code> 步长（stride）</span>
</div>

<p class="viz-attr">
  图片修改自：Vincent Dumoulin, Francesco Visin — <a href="https://arxiv.org/abs/1603.07285">A guide to convolution arithmetic for deep learning</a>
</p>
