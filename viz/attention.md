---
layout: default
title: 注意力机制
description: "编码—解码注意力、自注意力与多头注意力的可视化。"
permalink: /viz/attention/
redirect_from:
  - /v/attention/
---

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 注意力机制

从 Encoder-Decoder Attention 到 Self-Attention 与 Multi-Head Attention 的可视化。

## 编码器—解码器注意力

<figure class="viz-figure viz-figure--wide">
  <img src="https://jalammar.github.io/images/t/transformer_decoding_2.gif" alt="解码器逐步生成时的注意力流动" loading="lazy">
  <figcaption>解码器每生成一个 token，都对编码器输出进行一次加权聚合（注意力）。</figcaption>
  <small class="viz-figure__source">来源：Jay Alammar — <a href="https://jalammar.github.io/illustrated-transformer/">The Illustrated Transformer</a></small>
</figure>

## 自注意力（Self-Attention）

<figure class="viz-figure viz-figure--wide">
  <img src="https://jalammar.github.io/images/t/self-attention-output.png" alt="自注意力计算流程" loading="lazy">
  <figcaption>序列中每个位置作为 Query，与所有位置的 Key 计算相似度，再加权 Value 求和。</figcaption>
  <small class="viz-figure__source">来源：Jay Alammar — <a href="https://jalammar.github.io/illustrated-transformer/">The Illustrated Transformer</a></small>
</figure>

## 多头注意力（Multi-Head Attention）

<figure class="viz-figure viz-figure--wide">
  <img src="https://jalammar.github.io/images/t/transformer_multi-headed_self-attention-recap.png" alt="多头注意力" loading="lazy">
  <figcaption>多个独立的注意力"头"分别建模不同子空间，拼接后线性投影。</figcaption>
  <small class="viz-figure__source">来源：Jay Alammar — <a href="https://jalammar.github.io/illustrated-transformer/">The Illustrated Transformer</a></small>
</figure>

<p class="viz-attr">
  图片来源：Jay Alammar — <a href="https://jalammar.github.io/illustrated-transformer/">The Illustrated Transformer</a>
</p>

## 交互式资源

<div class="resource-grid">
  <a class="resource-card" href="https://bbycroft.net/llm" target="_blank" rel="noopener">
    <h3>LLM Visualization ↗</h3>
    <p>3D 交互式 GPT/Transformer 可视化，按步骤展示每个张量在网络中的流动。</p>
  </a>
  <a class="resource-card" href="https://poloclub.github.io/transformer-explainer/" target="_blank" rel="noopener">
    <h3>Transformer Explainer ↗</h3>
    <p>Polo Club 出品的交互式 Transformer 解释器，可输入文本观察注意力分布。</p>
  </a>
</div>
