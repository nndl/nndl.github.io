---
layout: default
title: 循环神经网络与门控机制
permalink: /v/rnn-lstm/
---

<a class="viz-back" href="{{ '/v/' | relative_url }}">可视化资源</a>

# 循环神经网络与门控机制

RNN 的展开形式，以及 LSTM / GRU 的门控结构示意。

## RNN 的时间展开

<figure class="viz-figure viz-figure--wide">
  <img src="https://colah.github.io/posts/2015-08-Understanding-LSTMs/img/RNN-unrolled.png" alt="RNN 的时间展开" loading="lazy">
  <figcaption>同一个 RNN 单元在时间维度上展开，对应一个深度等于序列长度的网络。</figcaption>
  <small class="viz-figure__source">来源：Chris Olah — <a href="https://colah.github.io/posts/2015-08-Understanding-LSTMs/">Understanding LSTM Networks</a></small>
</figure>

## LSTM 单元

LSTM 引入三个门（遗忘门、输入门、输出门）和一个独立的细胞状态，缓解长依赖梯度问题。

<figure class="viz-figure viz-figure--wide">
  <img src="https://colah.github.io/posts/2015-08-Understanding-LSTMs/img/LSTM3-chain.png" alt="LSTM 链式结构" loading="lazy">
  <figcaption>LSTM 单元的整体结构：细胞状态（上方水平线）受三个门控调控。</figcaption>
  <small class="viz-figure__source">来源：Chris Olah — <a href="https://colah.github.io/posts/2015-08-Understanding-LSTMs/">Understanding LSTM Networks</a></small>
</figure>

<div class="figure-grid figure-grid--2col">
  <figure class="viz-figure">
    <img src="https://colah.github.io/posts/2015-08-Understanding-LSTMs/img/LSTM3-focus-f.png" alt="遗忘门" loading="lazy">
    <figcaption>遗忘门：决定丢弃多少旧细胞状态。</figcaption>
    <small class="viz-figure__source">来源：Chris Olah — <a href="https://colah.github.io/posts/2015-08-Understanding-LSTMs/">Understanding LSTM Networks</a></small>
  </figure>
  <figure class="viz-figure">
    <img src="https://colah.github.io/posts/2015-08-Understanding-LSTMs/img/LSTM3-focus-i.png" alt="输入门" loading="lazy">
    <figcaption>输入门：决定写入哪些新信息。</figcaption>
    <small class="viz-figure__source">来源：Chris Olah — <a href="https://colah.github.io/posts/2015-08-Understanding-LSTMs/">Understanding LSTM Networks</a></small>
  </figure>
  <figure class="viz-figure">
    <img src="https://colah.github.io/posts/2015-08-Understanding-LSTMs/img/LSTM3-focus-C.png" alt="细胞状态更新" loading="lazy">
    <figcaption>细胞状态更新：旧状态 × 遗忘门 + 新信息 × 输入门。</figcaption>
    <small class="viz-figure__source">来源：Chris Olah — <a href="https://colah.github.io/posts/2015-08-Understanding-LSTMs/">Understanding LSTM Networks</a></small>
  </figure>
  <figure class="viz-figure">
    <img src="https://colah.github.io/posts/2015-08-Understanding-LSTMs/img/LSTM3-focus-o.png" alt="输出门" loading="lazy">
    <figcaption>输出门：决定输出哪部分细胞状态。</figcaption>
    <small class="viz-figure__source">来源：Chris Olah — <a href="https://colah.github.io/posts/2015-08-Understanding-LSTMs/">Understanding LSTM Networks</a></small>
  </figure>
</div>

## GRU 单元

GRU 把 LSTM 的三个门简化为两个（更新门 + 重置门），合并细胞状态与隐藏状态。

<figure class="viz-figure viz-figure--wide">
  <img src="https://colah.github.io/posts/2015-08-Understanding-LSTMs/img/LSTM3-var-GRU.png" alt="GRU 单元" loading="lazy">
  <figcaption>GRU 单元结构。</figcaption>
  <small class="viz-figure__source">来源：Chris Olah — <a href="https://colah.github.io/posts/2015-08-Understanding-LSTMs/">Understanding LSTM Networks</a></small>
</figure>

<p class="viz-attr">
  图片来源：Chris Olah — <a href="https://colah.github.io/posts/2015-08-Understanding-LSTMs/">Understanding LSTM Networks</a>（CC-BY 许可，已注明出处）。
  <br><em>TODO：如需镜像至本站，下载至 <code>assets/v/</code> 并替换 <code>src</code>。</em>
</p>

## 字符级 RNN 生成

<figure class="viz-figure viz-figure--wide">
  <img src="https://karpathy.github.io/assets/rnn/charseq.jpeg" alt="字符级 RNN 生成示例" loading="lazy">
  <figcaption>RNN 按字符逐步生成文本：每一步的输入是上一步的输出。</figcaption>
  <small class="viz-figure__source">来源：Andrej Karpathy — <a href="https://karpathy.github.io/2015/05/21/rnn-effectiveness/">The Unreasonable Effectiveness of Recurrent Neural Networks</a></small>
</figure>

<p class="viz-attr">
  图片来源：Andrej Karpathy — <a href="https://karpathy.github.io/2015/05/21/rnn-effectiveness/">The Unreasonable Effectiveness of Recurrent Neural Networks</a>
</p>
