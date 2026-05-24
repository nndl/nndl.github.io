---
layout: default
title: 基于 Transformer 的序列到序列模型
permalink: /v/sgm-seq2seq-transformer/
---

<a class="viz-back" href="{{ '/v/' | relative_url }}">可视化资源</a>

# 基于 Transformer 的序列到序列模型

完全基于自注意力机制，抛弃循环与卷积，可并行处理整个序列。是当前大模型的基础架构。

<figure class="viz-figure viz-figure--wide">
  <img src="{{ '/v/sgm-seq2seq-transformer.gif' | relative_url }}" alt="Transformer 编码器—解码器" loading="lazy">
  <figcaption>Transformer 编码器与解码器并行处理序列。</figcaption>
  <small class="viz-figure__source">来源：<a href="https://ai.googleblog.com/2017/08/transformer-novel-neural-network.html">Google AI Blog · Transformer</a></small>
</figure>

<p class="viz-attr">图片来源：<a href="https://ai.googleblog.com/2017/08/transformer-novel-neural-network.html">Google AI Blog</a></p>
