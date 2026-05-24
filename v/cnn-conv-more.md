---
layout: default
title: 转置卷积与空洞卷积演示
permalink: /v/cnn-conv-more/
---

<a class="viz-back" href="{{ '/v/' | relative_url }}">可视化资源</a>

# 转置卷积与空洞卷积

## 转置卷积

将卷积过程"反过来"的运算，常用于上采样。同一参数下，标准卷积与转置卷积的对比：

<div class="figure-grid figure-grid--2col">
  <figure class="viz-figure">
    <img src="{{ '/v/cnn-no_padding_no_strides.gif' | relative_url }}" alt="标准卷积 s=1" loading="lazy">
    <figcaption>标准卷积 · <code>m = 3</code> · <code>p = 0</code> · <code>s = 1</code></figcaption>
    <small class="viz-figure__source">来源：<a href="https://github.com/vdumoulin/conv_arithmetic">vdumoulin/conv_arithmetic</a>（MIT）</small>
  </figure>
  <figure class="viz-figure">
    <img src="{{ '/v/cnn-no_padding_strides.gif' | relative_url }}" alt="标准卷积 s=2" loading="lazy">
    <figcaption>标准卷积 · <code>m = 3</code> · <code>p = 0</code> · <code>s = 2</code></figcaption>
    <small class="viz-figure__source">来源：<a href="https://github.com/vdumoulin/conv_arithmetic">vdumoulin/conv_arithmetic</a>（MIT）</small>
  </figure>
  <figure class="viz-figure">
    <img src="{{ '/v/cnn-no_padding_no_strides_transposed.gif' | relative_url }}" alt="转置卷积 s=1" loading="lazy">
    <figcaption>转置卷积 · <code>m = 3</code> · <code>p = 0</code> · <code>s = 1</code></figcaption>
    <small class="viz-figure__source">来源：<a href="https://github.com/vdumoulin/conv_arithmetic">vdumoulin/conv_arithmetic</a>（MIT）</small>
  </figure>
  <figure class="viz-figure">
    <img src="{{ '/v/cnn-no_padding_strides_transposed.gif' | relative_url }}" alt="转置卷积 s=2" loading="lazy">
    <figcaption>转置卷积 · <code>m = 3</code> · <code>p = 0</code> · <code>s = 2</code></figcaption>
    <small class="viz-figure__source">来源：<a href="https://github.com/vdumoulin/conv_arithmetic">vdumoulin/conv_arithmetic</a>（MIT）</small>
  </figure>
</div>

## 空洞卷积

在卷积核元素之间插入"空洞"，扩大感受野而不增加参数量：

<div class="figure-grid figure-grid--2col">
  <figure class="viz-figure">
    <img src="{{ '/v/cnn-dilation-in_7_out_3.gif' | relative_url }}" alt="d=1 标准卷积" loading="lazy">
    <figcaption><code>d = 1</code>（等价于标准卷积）</figcaption>
    <small class="viz-figure__source">来源：<a href="https://github.com/vdumoulin/conv_arithmetic">vdumoulin/conv_arithmetic</a>（MIT）</small>
  </figure>
  <figure class="viz-figure">
    <img src="{{ '/v/cnn-dilation.gif' | relative_url }}" alt="d=2 空洞卷积" loading="lazy">
    <figcaption><code>d = 2</code>（感受野扩大）</figcaption>
    <small class="viz-figure__source">来源：<a href="https://github.com/vdumoulin/conv_arithmetic">vdumoulin/conv_arithmetic</a>（MIT）</small>
  </figure>
</div>

<div class="viz-legend">
  <span><code>m</code> 卷积核大小</span>
  <span><code>p</code> 零填充（zero-padding）</span>
  <span><code>s</code> 步长（stride）</span>
  <span><code>d</code> 膨胀率（dilation）</span>
</div>

<p class="viz-attr">
  图片修改自：Vincent Dumoulin, Francesco Visin — <a href="https://arxiv.org/abs/1603.07285">A guide to convolution arithmetic for deep learning</a>
</p>
