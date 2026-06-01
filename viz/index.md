---
layout: default
title: 可视化资源
permalink: /viz/
redirect_from:
  - /v/
---

# 可视化资源

书中关键概念与模型的动图与交互演示，便于直观理解。条目按《神经网络与深度学习（第二版）》的章节顺序排列。

## 数学基础

<div class="viz-grid">
  {% include viz-card.html url="/viz/matrix-transform/" title="矩阵是空间变换" blurb="拖动 2×2 矩阵的四个数，看整个平面被旋转/缩放/剪切；列是基向量去向，行列式是面积缩放。" %}
  {% include viz-card.html url="/viz/dot-product/" title="点积与余弦相似度" blurb="拖两个向量，看点积=投影对齐、余弦相似度=夹角——注意力和向量检索的根基。" %}
  {% include viz-card.html url="/viz/entropy/" title="熵 / 交叉熵 / KL" blurb="拖动预测分布，看熵、交叉熵、KL 散度怎么变——几乎所有分类损失函数的根基。" %}
</div>

## 概率与统计

<div class="viz-grid">
  {% include viz-card.html url="/viz/bayes/" title="贝叶斯更新" blurb="抛硬币更新对正面概率的信念：先验×数据→后验，抛得越多越笃定。" %}
  {% include viz-card.html url="/viz/gaussian-mle/" title="高斯与最大似然" blurb="拖 μ、σ 的高斯去拟合一堆点，看最大似然为什么落在样本均值和标准差上。" %}
  {% include viz-card.html url="/viz/clt/" title="中心极限定理" blurb="从任意分布反复抽 n 个求平均，n 越大，平均值的分布越收成漂亮的高斯钟形。" %}
  {% include viz-card.html url="/viz/law-large-numbers/" title="大数定律" blurb="一直抛硬币，正面频率从剧烈抖动慢慢稳稳逼近真实概率——样本越多越准。" %}
  {% include viz-card.html url="/viz/mcmc/" title="MCMC 采样" blurb="用 Metropolis 随机游走从复杂分布采样，样本逐渐铺成目标分布的形状。" %}
  {% include viz-card.html url="/viz/correlation-causation/" title="相关不等于因果" blurb="冰淇淋与溺水强相关，控制住隐藏的‘气温’后相关消失——相关未必有因果。" %}
</div>

## 第 2 章 · 机器学习概述

<div class="viz-grid">
  {% include viz-card.html url="/viz/overfitting/" title="过拟合实验台" blurb="拖动模型复杂度，看曲线从欠拟合到过拟合，训练/测试误差的 U 型对比。" %}
  {% include viz-card.html url="/viz/gradient-descent/" title="梯度下降下山" blurb="小球沿曲线下山找最低点；调学习率看收敛、震荡，体会局部最优陷阱。" %}
  {% include viz-card.html url="/viz/bias-variance/" title="偏差与方差" blurb="同复杂度在多份数据上学出多条曲线，看是‘齐刷刷地偏’还是‘乱七八糟地飘’。" %}
  {% include viz-card.html url="/viz/precision-recall/" title="精确率与召回率" blurb="拖判定阈值，看混淆矩阵、精确率与召回率此消彼长，以及 ROC 曲线。" %}
  {% include viz-card.html url="/viz/regularization/" title="正则化 L1 / L2" blurb="调正则强度，看 L2 让权重一起缩、L1 把一些权重压到 0（稀疏 / 特征选择）。" %}
  {% include viz-card.html url="/viz/decision-tree/" title="决策树与信息增益" blurb="按信息增益一刀刀切分平面，看决策树怎样把交叠的两类逐步分纯。" %}
  {% include viz-card.html url="/viz/knn/" title="k 近邻 KNN" blurb="拖查询点，看最近 k 个邻居投票分类；k 小决策边界碎、k 大边界平。" %}
</div>

## 第 3 章 · 线性模型

<div class="viz-grid">
  {% include viz-card.html url="/viz/perceptron/" title="感知器画线" blurb="平面上两类点，感知器逐步把分界线转到位，还能亲手加点试试。" %}
  {% include viz-card.html url="/viz/svm-margin/" title="SVM 最大间隔" blurb="在两类点之间修一条最宽的‘马路’，分界线走正中；拖点看支持向量怎么定。" %}
  {% include viz-card.html url="/viz/logistic-regression/" title="逻辑回归" blurb="两类点 + sigmoid 概率渐变背景，训练看决策边界和交叉熵损失怎么一步步学出来。" %}
  {% include viz-card.html url="/viz/kernel-trick/" title="核技巧" blurb="同心环线性分不开，升一维 z=x²+y² 后被一个平面切开——核技巧的直觉。" %}
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
  {% include viz-card.html url="/viz/residual/" title="残差连接" blurb="对比有无跳连的深层网络梯度，残差给梯度修一条‘+1 高速路’，于是能训得很深。" %}
  {% include viz-card.html url="/viz/weight-init/" title="权重初始化" blurb="信号穿过 18 层：初始权重太大→爆炸、太小→消失，Xavier 恰好保持稳定。" %}
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
  {% include viz-card.html url="/viz/pooling/" title="汇聚（池化）" blurb="2×2 窗口扫过特征图，最大 / 平均汇聚把它缩小、保留要点（平移不变）。" %}
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
  {% include viz-card.html url="/viz/adam/" title="自适应优化器 Adam" blurb="窄长山谷里 SGD / 动量 / Adam 三球赛跑，看 Adam 每参数自适应学习率又快又稳。" %}
  {% include viz-card.html url="/viz/dropout/" title="Dropout" blurb="训练时随机关掉一部分神经元，逼网络学冗余表示、防过拟合；测试时再全开。" %}
  {% include viz-card.html url="/viz/batchnorm/" title="批归一化 BatchNorm" blurb="把每批激活减均值除标准差拉回‘均值0方差1’，让深层网络训练又快又稳。" %}
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
  {% include viz-card.html url="/viz/qkv-attention/" title="QKV 注意力计算" blurb="拆开注意力的算法：Query·Key 算分数→softmax→对 Value 加权，看“它”怎么算出指向“猫”。" %}
  {% include viz-card.html url="/viz/multi-head/" title="多头注意力" blurb="三个注意力头并排，各看相邻 / 指代 / 句首一种关系——多头分工再合议。" %}
  {% include viz-card.html url="/viz/causal-mask/" title="因果掩码" blurb="给注意力盖上因果掩码，每个词只能看自己和左边，保证自回归生成不偷看答案。" %}
  {% include viz-card.html url="/viz/rope/" title="RoPE 旋转位置编码" blurb="位置编码成旋转角度，两词的注意力分数只取决于相对位置——更稳、还能外推到更长序列。" %}
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
  {% include viz-card.html url="/viz/pca/" title="PCA 主成分分析" blurb="二维点云自动找出最铺得开的主成分方向，沿它投影把二维压成一维。" %}
  {% include viz-card.html url="/viz/gmm/" title="高斯混合与 EM" blurb="高斯混合软聚类，EM 交替算归属概率 / 更新高斯；交界处的点是‘混色’的（对比 K-means 硬分配）。" %}
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
  {% include viz-card.html url="/viz/value-iteration/" title="价值迭代" blurb="网格世界里价值从宝藏一格格扩散，箭头连成一条避开陷阱、通往宝藏的最优路线。" %}
</div>

## 第 13 章 · 大语言模型与智能体

<div class="viz-grid">
  {% include viz-card.html
     url="/viz/llm-internals/"
     title="LLM 内部结构（3D）"
     blurb="bbycroft.net/llm：3D 交互式 GPT 内部张量流动演示，从 token 到 logit 的全过程。" %}
  {% include viz-card.html url="/viz/tokenization/" title="词元化" blurb="输入文字看它被切成一个个词元；也解释了模型为什么数不清 strawberry 里有几个 r。" %}
  {% include viz-card.html url="/viz/temperature/" title="温度采样" blurb="调‘温度’看模型挑下一个词的概率条重塑：低温保守稳定、高温有创意也容易胡说。" %}
  {% include viz-card.html url="/viz/next-word/" title="下一词预测" blurb="用 bigram 语言模型按概率接词成句，看“按概率接龙”为什么会跑题、重复。" %}
  {% include viz-card.html url="/viz/beam-search/" title="束搜索与贪心" blurb="解码树上贪心 vs 束搜索：贪心掉进局部最优，束搜索留 k 条找到整体更优的句子。" %}
  {% include viz-card.html url="/viz/scaling-laws/" title="缩放定律" blurb="损失随规模按幂律下降（log-log 直线），用小模型外推预测大模型，还有不可约下限。" %}
  {% include viz-card.html url="/viz/moe/" title="混合专家 MoE" blurb="路由器把每个词只派给少数几个‘专家’子网络，参数海量但每次只算一小部分。" %}
  {% include viz-card.html url="/viz/kv-cache/" title="KV 缓存与 O(n²)" blurb="自回归生成时注意力是 O(n²)，KV 缓存把历史键值存起来复用，降到线性。" %}
  {% include viz-card.html url="/viz/quantization/" title="量化" blurb="把连续权重吸附到离散档位，fp32→int8/int4 看体积缩小与精度损失的权衡。" %}
  {% include viz-card.html url="/viz/lora/" title="LoRA 低秩微调" blurb="冻结大权重矩阵，只训两个小矩阵 A·B，微调参数从 d² 骤降到 2dr。" %}
</div>

## 第 16 章 · 深度生成模型

<div class="viz-grid">
  {% include viz-card.html
     url="/viz/diffusion/"
     title="扩散模型"
     blurb="前向加噪、反向去噪过程，以及与 GAN / VAE 的对比。"
     thumb="https://lilianweng.github.io/posts/2021-07-11-diffusion-models/DDPM.png" %}
  {% include viz-card.html url="/viz/diffusion-noise/" title="扩散：加噪与去噪" blurb="把一张图的每个像素一步步掺成彩色雪花，再从噪声里去噪生成——亲手体会扩散模型画图的原理。" thumb="/assets/viz/diffusion-noise.jpg" %}
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
