---
layout: default
title: 可视化资源
permalink: /v/
---

# 可视化资源

书中关键概念与模型的动图与交互演示，便于直观理解。

## 卷积神经网络

<div class="viz-grid">
  <a class="viz-card" href="{{ '/v/cnn-conv-2d/' | relative_url }}">
    <div class="viz-card__thumb"><img src="{{ '/v/cnn-in_5_out_3_p_0_s_0.gif' | relative_url }}" alt="二维卷积演示" loading="lazy"></div>
    <div class="viz-card__body">
      <h3>二维卷积</h3>
      <p>不同步长、填充下的二维卷积过程演示。</p>
    </div>
  </a>
  <a class="viz-card" href="{{ '/v/cnn-conv-more/' | relative_url }}">
    <div class="viz-card__thumb"><img src="{{ '/v/cnn-no_padding_no_strides_transposed.gif' | relative_url }}" alt="转置卷积演示" loading="lazy"></div>
    <div class="viz-card__body">
      <h3>转置卷积与空洞卷积</h3>
      <p>对比卷积、转置卷积；不同膨胀率下的空洞卷积。</p>
    </div>
  </a>
  <a class="viz-card" href="{{ '/v/cnn-googlenet/' | relative_url }}">
    <div class="viz-card__thumb"><img src="{{ '/v/cnn-googlenet.png' | relative_url }}" alt="GoogLeNet 结构" loading="lazy"></div>
    <div class="viz-card__body">
      <h3>GoogLeNet 结构</h3>
      <p>GoogLeNet（Inception）网络结构示意。</p>
    </div>
  </a>
</div>

## 循环神经网络

<div class="viz-grid">
  <a class="viz-card" href="{{ '/v/rnn-lstm/' | relative_url }}">
    <div class="viz-card__thumb"><img src="https://colah.github.io/posts/2015-08-Understanding-LSTMs/img/LSTM3-chain.png" alt="LSTM 链式结构" loading="lazy"></div>
    <div class="viz-card__body">
      <h3>RNN / LSTM / GRU</h3>
      <p>循环神经网络的时间展开、LSTM 三个门控、GRU 简化结构。</p>
    </div>
  </a>
</div>

## 注意力机制

<div class="viz-grid">
  <a class="viz-card" href="{{ '/v/attention/' | relative_url }}">
    <div class="viz-card__thumb"><img src="https://jalammar.github.io/images/t/transformer_decoding_2.gif" alt="注意力机制" loading="lazy"></div>
    <div class="viz-card__body">
      <h3>注意力机制</h3>
      <p>编码—解码注意力、自注意力与多头注意力的可视化。</p>
    </div>
  </a>
</div>

## 序列建模

<div class="viz-grid">
  <a class="viz-card" href="{{ '/v/sgm-seq2seq-rnn/' | relative_url }}">
    <div class="viz-card__thumb"><img src="{{ '/v/sgm-seq2seq-rnn-mt.gif' | relative_url }}" alt="基于 RNN 的 Seq2Seq" loading="lazy"></div>
    <div class="viz-card__body">
      <h3>基于 RNN</h3>
      <p>编码器—解码器结构的循环神经网络 Seq2Seq，常用于机器翻译。</p>
    </div>
  </a>
  <a class="viz-card" href="{{ '/v/sgm-seq2seq-cnn/' | relative_url }}">
    <div class="viz-card__thumb"><img src="{{ '/v/sgm-seq2seq-cnn-mt.gif' | relative_url }}" alt="基于卷积的 Seq2Seq" loading="lazy"></div>
    <div class="viz-card__body">
      <h3>基于卷积</h3>
      <p>WaveNet 与 fairseq 卷积 Seq2Seq：用卷积代替循环，可并行训练。</p>
    </div>
  </a>
  <a class="viz-card" href="{{ '/v/sgm-seq2seq-transformer/' | relative_url }}">
    <div class="viz-card__thumb"><img src="{{ '/v/sgm-seq2seq-transformer.gif' | relative_url }}" alt="Transformer Seq2Seq" loading="lazy"></div>
    <div class="viz-card__body">
      <h3>Transformer</h3>
      <p>基于自注意力机制，可并行处理整个序列，是当前大模型的基础架构。</p>
    </div>
  </a>
</div>

## 生成模型

<div class="viz-grid">
  <a class="viz-card" href="{{ '/v/diffusion/' | relative_url }}">
    <div class="viz-card__thumb"><img src="https://lilianweng.github.io/posts/2021-07-11-diffusion-models/DDPM.png" alt="扩散模型" loading="lazy"></div>
    <div class="viz-card__body">
      <h3>扩散模型</h3>
      <p>前向加噪、反向去噪过程，以及与 GAN / VAE 的对比。</p>
    </div>
  </a>
</div>

## 优化

<div class="viz-grid">
  <a class="viz-card" href="{{ '/v/optimizers/' | relative_url }}">
    <div class="viz-card__thumb"><img src="{{ '/v/opt-3d.gif' | relative_url }}" alt="优化算法对比" loading="lazy"></div>
    <div class="viz-card__body">
      <h3>优化算法对比</h3>
      <p>SGD / Momentum / Adam 等在三维损失面上的轨迹，附交互式资源。</p>
    </div>
  </a>
</div>

---

<p style="color: var(--color-text-muted); font-size: 0.9rem;">
  欢迎贡献新的可视化资源：fork 仓库并在 <code>v/</code> 下添加 markdown 与素材后提 PR。
</p>
