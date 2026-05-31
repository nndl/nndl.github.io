---
layout: default
title: 可视化资源
permalink: /viz/
redirect_from:
  - /v/
---

# 可视化资源

书中关键概念与模型的动图与交互演示，便于直观理解。条目按《神经网络与深度学习（第二版）》的章节顺序排列。

## 第 2 章 · 机器学习概述

<div class="viz-grid">
  {% include viz-card.html url="/viz/overfitting/" title="过拟合实验台" blurb="拖动模型复杂度，看曲线从欠拟合到过拟合，训练/测试误差的 U 型对比。" %}
  {% include viz-card.html url="/viz/gradient-descent/" title="梯度下降下山" blurb="小球沿曲线下山找最低点；调学习率看收敛、震荡，体会局部最优陷阱。" %}
  {% include viz-card.html url="/viz/bias-variance/" title="偏差与方差" blurb="同复杂度在多份数据上学出多条曲线，看是‘齐刷刷地偏’还是‘乱七八糟地飘’。" %}
  {% include viz-card.html url="/viz/precision-recall/" title="精确率与召回率" blurb="拖判定阈值，看混淆矩阵、精确率与召回率此消彼长，以及 ROC 曲线。" %}
</div>

## 第 3 章 · 线性模型

<div class="viz-grid">
  {% include viz-card.html url="/viz/perceptron/" title="感知器画线" blurb="平面上两类点，感知器逐步把分界线转到位，还能亲手加点试试。" %}
  {% include viz-card.html url="/viz/svm-margin/" title="SVM 最大间隔" blurb="在两类点之间修一条最宽的‘马路’，分界线走正中；拖点看支持向量怎么定。" %}
</div>

## 第 4 章 · 前馈神经网络

<div class="viz-grid">
  {% include viz-card.html
     url="https://playground.tensorflow.org/"
     title="TensorFlow Playground"
     blurb="在浏览器里直接搭一个浅层前馈网络，实时观察隐藏层学到的特征。"
     thumb="https://playground.tensorflow.org/preview.png"
     external=true %}
  {% include viz-card.html url="/viz/neurons-compose/" title="神经元拼曲线" blurb="几个 ReLU 神经元各画一条折线，叠加起来逼近复杂曲线——万能近似的直觉。" %}
  {% include viz-card.html url="/viz/activations/" title="激活函数与梯度消失" blurb="Sigmoid/Tanh/ReLU 及其导数，看多层连乘后梯度怎样消失，以及 ReLU 为何取胜。" %}
  {% include viz-card.html url="/viz/backprop/" title="反向传播" blurb="迷你计算图上一步步看：正向算误差、反向用链式法则传梯度、训练让 loss 下降。" %}
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
  {% include viz-card.html url="/viz/conv-kernel/" title="卷积核手动滑动" blurb="3×3 核在图上一格格滑过，换边缘/竖线/锐化核，看同一张图被‘看’出不同特征。" %}
</div>

## 第 6 章 · 循环神经网络

<div class="viz-grid">
  {% include viz-card.html
     url="/viz/rnn-lstm/"
     title="RNN / LSTM / GRU"
     blurb="交互实验台：切换三种结构、编辑输入序列、单步观察门的开合与记忆沿时间的演化。"
     thumb="https://colah.github.io/posts/2015-08-Understanding-LSTMs/img/LSTM3-chain.png" %}
</div>

## 第 7 章 · 网络优化与正则化

<div class="viz-grid">
  {% include viz-card.html
     url="/viz/optimizers/"
     title="优化算法对比"
     blurb="SGD / Momentum / Adam 等在三维损失面上的轨迹，附交互式资源。"
     thumb="/viz/opt-3d.gif" %}
  {% include viz-card.html url="/viz/momentum/" title="学习率与动量" blurb="窄长山谷里普通梯度下降 vs 动量两球赛跑，调学习率看震荡、发散与加速。" %}
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
  {% include viz-card.html url="/viz/self-attention/" title="点词看注意力" blurb="点句子里的一个词，看自注意力把它连向相关的词（如“它”指向“小猫”）。" %}
  {% include viz-card.html url="/viz/embeddings/" title="词向量类比" blurb="二维语义空间里‘国王−男人+女人≈王后’，看词与词的关系就是向量方向。" %}
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
  {% include viz-card.html url="/viz/kmeans/" title="K-means 聚类" blurb="随机撒下中心，反复“投靠最近中心→中心移到群中央”，看点被自动分成几组。" %}
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
  {% include viz-card.html url="/viz/bandit/" title="多臂老虎机" blurb="几台隐藏中奖率的老虎机，ε-greedy 在探索与利用之间权衡，估计逐渐变准。" %}
</div>

## 第 13 章 · 大语言模型与智能体

<div class="viz-grid">
  {% include viz-card.html
     url="/viz/llm-internals/"
     title="LLM 内部结构（3D）"
     blurb="bbycroft.net/llm：3D 交互式 GPT 内部张量流动演示，从 token 到 logit 的全过程。" %}
  {% include viz-card.html url="/viz/tokenization/" title="词元化" blurb="输入文字看它被切成一个个词元；也解释了模型为什么数不清 strawberry 里有几个 r。" %}
  {% include viz-card.html url="/viz/temperature/" title="温度采样" blurb="调‘温度’看模型挑下一个词的概率条重塑：低温保守稳定、高温有创意也容易胡说。" %}
</div>

## 第 16 章 · 深度生成模型

<div class="viz-grid">
  {% include viz-card.html
     url="/viz/diffusion/"
     title="扩散模型"
     blurb="前向加噪、反向去噪过程，以及与 GAN / VAE 的对比。"
     thumb="https://lilianweng.github.io/posts/2021-07-11-diffusion-models/DDPM.png" %}
  {% include viz-card.html url="/viz/diffusion-noise/" title="扩散：加噪与去噪" blurb="看一颗‘心’被一步步打成噪声、再被去噪还原——亲手体会扩散模型生成图的原理。" %}
  {% include viz-card.html
     url="/viz/gan-lab/"
     title="GAN Lab"
     blurb="PoloClub 互动玩具：在浏览器中训练一个 2D GAN，逐步可视化判别器与生成器的对抗。"
     thumb="https://raw.githubusercontent.com/poloclub/ganlab/master/ganlab-teaser.png" %}
</div>

---

<p style="color: var(--color-text-muted); font-size: 0.9rem;">
  欢迎贡献新的可视化资源：fork 仓库并在 <code>viz/</code> 下添加 markdown 与素材后提 PR。
</p>
