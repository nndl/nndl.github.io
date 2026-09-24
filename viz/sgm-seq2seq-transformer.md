---
layout: default
title: 基于 Transformer 的序列到序列模型
description: "以自注意力为核心、结合编码器—解码器交叉注意力，可并行处理训练序列；Transformer 是许多大模型的基础架构。"
permalink: /viz/sgm-seq2seq-transformer/
redirect_from:
  - /v/sgm-seq2seq-transformer/
---

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 基于 Transformer 的序列到序列模型

原始 Transformer 以自注意力为核心，编码器—解码器之间还通过交叉注意力传递信息，并抛弃了循环与卷积。训练阶段可以并行处理整个序列；生成式解码仍需按位置逐步生成。它也成为许多大模型架构的基础。

<figure class="viz-figure viz-figure--wide">
  <img src="{{ '/viz/sgm-seq2seq-transformer.gif' | relative_url }}" alt="Transformer 编码器—解码器" loading="lazy">
  <figcaption>Transformer 编码器与解码器并行处理序列。</figcaption>
  <small class="viz-figure__source">来源：<a href="https://ai.googleblog.com/2017/08/transformer-novel-neural-network.html">Google AI Blog · Transformer</a></small>
</figure>

<p class="viz-attr">图片来源：<a href="https://ai.googleblog.com/2017/08/transformer-novel-neural-network.html">Google AI Blog</a></p>
