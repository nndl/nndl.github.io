---
layout: default
title: 可视化资源
permalink: /viz/
redirect_from:
  - /v/
---

# 可视化资源

书中关键概念与模型的动图与交互演示，便于直观理解。条目按《神经网络与深度学习（第二版）》的章节顺序排列。

## 第 4 章 · 前馈神经网络

<div class="viz-grid">
  {% include viz-card.html
     url="https://playground.tensorflow.org/"
     title="TensorFlow Playground"
     blurb="在浏览器里直接搭一个浅层前馈网络，实时观察隐藏层学到的特征。"
     thumb="https://playground.tensorflow.org/preview.png"
     external=true %}
</div>

## 第 5 章 · 卷积神经网络

<div class="viz-grid">
  {% include viz-card.html
     url="/viz/cnn-conv-2d/"
     title="二维卷积"
     blurb="不同步长、填充下的二维卷积过程演示。"
     thumb="/viz/cnn-in_5_out_3_p_0_s_0.gif" %}
  {% include viz-card.html
     url="/viz/cnn-conv-more/"
     title="转置卷积与空洞卷积"
     blurb="对比卷积、转置卷积；不同膨胀率下的空洞卷积。"
     thumb="/viz/cnn-no_padding_no_strides_transposed.gif" %}
  {% include viz-card.html
     url="/viz/cnn-googlenet/"
     title="GoogLeNet 结构"
     blurb="GoogLeNet（Inception）网络结构示意。"
     thumb="/viz/cnn-googlenet.png" %}
  {% include viz-card.html
     url="/viz/cnn-explainer/"
     title="CNN Explainer"
     blurb="PoloClub 出品的交互式 CNN 解释器，可逐层查看激活与卷积运算。"
     thumb="https://poloclub.github.io/cnn-explainer/assets/figures/preview.png" %}
</div>

## 第 6 章 · 循环神经网络

<div class="viz-grid">
  {% include viz-card.html
     url="/viz/rnn-lstm/"
     title="RNN / LSTM / GRU"
     blurb="循环神经网络的时间展开、LSTM 三个门控、GRU 简化结构。"
     thumb="https://colah.github.io/posts/2015-08-Understanding-LSTMs/img/LSTM3-chain.png" %}
</div>

## 第 7 章 · 网络优化与正则化

<div class="viz-grid">
  {% include viz-card.html
     url="/viz/optimizers/"
     title="优化算法对比"
     blurb="SGD / Momentum / Adam 等在三维损失面上的轨迹，附交互式资源。"
     thumb="/viz/opt-3d.gif" %}
</div>

## 第 8 章 · 注意力机制与 Transformer

<div class="viz-grid">
  {% include viz-card.html
     url="/viz/attention/"
     title="注意力机制"
     blurb="编码—解码注意力、自注意力与多头注意力的可视化。"
     thumb="https://jalammar.github.io/images/t/transformer_decoding_2.gif" %}
  {% include viz-card.html
     url="/viz/positional-encoding/"
     title="位置编码"
     blurb="Transformer 中正弦/余弦位置编码的几何直观与不同位置的相似度模式。"
     thumb="https://jalammar.github.io/images/t/transformer_positional_encoding_example.png" %}
</div>

### 序列建模专题

> 跨 CNN / RNN / Transformer 的 Seq2Seq 横向对比，便于理解各架构在序列任务上的权衡。

<div class="viz-grid">
  {% include viz-card.html
     url="/viz/sgm-seq2seq-rnn/"
     title="基于 RNN"
     blurb="编码器—解码器结构的循环神经网络 Seq2Seq，常用于机器翻译。"
     thumb="/viz/sgm-seq2seq-rnn-mt.gif" %}
  {% include viz-card.html
     url="/viz/sgm-seq2seq-cnn/"
     title="基于卷积"
     blurb="WaveNet 与 fairseq 卷积 Seq2Seq：用卷积代替循环，可并行训练。"
     thumb="/viz/sgm-seq2seq-cnn-mt.gif" %}
  {% include viz-card.html
     url="/viz/sgm-seq2seq-transformer/"
     title="Transformer"
     blurb="基于自注意力机制，可并行处理整个序列，是当前大模型的基础架构。"
     thumb="/viz/sgm-seq2seq-transformer.gif" %}
</div>

## 第 9 章 · 图神经网络

<div class="viz-grid">
  {% include viz-card.html
     url="/viz/gnn/"
     title="GNN 消息传递"
     blurb="distill.pub 互动文章：节点 / 边特征如何在消息传递中聚合更新。"
     thumb="https://distill.pub/2021/gnn-intro/thumbnail.jpg" %}
</div>

## 第 10 章 · 无监督学习

<div class="viz-grid">
  {% include viz-card.html
     url="/viz/tsne/"
     title="t-SNE 与降维"
     blurb="distill.pub 经典互动：如何正确解读 t-SNE 图，以及 perplexity / 迭代步数的影响。"
     thumb="https://distill.pub/2016/misread-tsne/thumbnail.jpg" %}
</div>

## 第 12 章 · 深度强化学习

<div class="viz-grid">
  {% include viz-card.html
     url="/viz/rl-gridworld/"
     title="GridWorld 强化学习"
     blurb="Karpathy 的 REINFORCEjs：在网格世界里实时观察价值迭代、Q-Learning、Policy Gradient。"
     thumb="https://cs.stanford.edu/people/karpathy/reinforcejs/img/dpsolved.jpeg" %}
</div>

## 第 13 章 · 大语言模型与智能体

<div class="viz-grid">
  {% include viz-card.html
     url="/viz/llm-internals/"
     title="LLM 内部结构（3D）"
     blurb="bbycroft.net/llm：3D 交互式 GPT 内部张量流动演示，从 token 到 logit 的全过程。" %}
</div>

## 第 16 章 · 深度生成模型

<div class="viz-grid">
  {% include viz-card.html
     url="/viz/diffusion/"
     title="扩散模型"
     blurb="前向加噪、反向去噪过程，以及与 GAN / VAE 的对比。"
     thumb="https://lilianweng.github.io/posts/2021-07-11-diffusion-models/DDPM.png" %}
  {% include viz-card.html
     url="/viz/gan-lab/"
     title="GAN Lab"
     blurb="PoloClub 互动玩具：在浏览器中训练一个 2D GAN，逐步可视化判别器与生成器的对抗。"
     thumb="https://raw.githubusercontent.com/poloclub/ganlab/master/ganlab-teaser.png" %}
</div>

---

<p style="color: var(--color-text-muted); font-size: 0.9rem;">
  欢迎贡献新的可视化资源：fork 仓库并在 <code>v/</code> 下添加 markdown 与素材后提 PR。
</p>
