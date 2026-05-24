---
layout: default
title: 基于 RNN 的序列到序列模型
permalink: /viz/sgm-seq2seq-rnn/
---

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 基于 RNN 的序列到序列模型

编码器—解码器结构的循环神经网络 Seq2Seq，常用于机器翻译。编码器读完整个输入序列后，解码器逐步生成输出。

<figure class="viz-figure viz-figure--wide">
  <img src="{{ '/viz/sgm-seq2seq-rnn-mt.gif' | relative_url }}" alt="基于 RNN 的 Seq2Seq" loading="lazy">
  <figcaption>RNN 编码器—解码器在机器翻译中的工作过程。</figcaption>
  <small class="viz-figure__source">来源：<a href="https://github.com/google/seq2seq">google/seq2seq</a></small>
</figure>

<p class="viz-attr">图片来源：<a href="https://github.com/google/seq2seq">google/seq2seq</a></p>
