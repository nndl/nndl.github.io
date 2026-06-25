---
layout: default
title: 基于卷积的序列到序列模型
description: "WaveNet 与 fairseq 卷积 Seq2Seq：用卷积代替循环，可并行训练。"
permalink: /viz/sgm-seq2seq-cnn/
redirect_from:
  - /v/sgm-seq2seq-cnn/
---

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 基于卷积的序列到序列模型

使用卷积代替循环结构，可并行化训练、避免长依赖梯度消失。

## WaveNet（空洞因果卷积）

通过堆叠空洞因果卷积扩大感受野，逐点生成音频/序列。

<figure class="viz-figure viz-figure--wide">
  <img src="{{ '/viz/sgm-seq2seq-fnn-wavenet.gif' | relative_url }}" alt="WaveNet 空洞因果卷积" loading="lazy">
  <figcaption>WaveNet 的空洞因果卷积逐层扩大感受野。</figcaption>
  <small class="viz-figure__source">来源：<a href="https://deepmind.com/blog/wavenet-generative-model-raw-audio/">DeepMind Blog · WaveNet</a></small>
</figure>

<p class="viz-attr">图片来源：<a href="https://deepmind.com/blog/wavenet-generative-model-raw-audio/">DeepMind Blog</a></p>

## Facebook fairseq（卷积 Seq2Seq）

编码器和解码器均使用 CNN，加上注意力机制，在保持质量的同时获得 RNN 难以企及的并行速度。

<figure class="viz-figure viz-figure--wide">
  <img src="{{ '/viz/sgm-seq2seq-cnn-mt.gif' | relative_url }}" alt="基于 CNN 的 Seq2Seq" loading="lazy">
  <figcaption>fairseq 的卷积 Seq2Seq 模型工作过程。</figcaption>
  <small class="viz-figure__source">来源：<a href="https://github.com/facebookresearch/fairseq">facebookresearch/fairseq</a></small>
</figure>

<p class="viz-attr">图片来源：<a href="https://github.com/facebookresearch/fairseq">facebookresearch/fairseq</a></p>
