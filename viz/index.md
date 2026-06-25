---
layout: default
title: 可视化资源
description: "书中关键概念与模型的动图与交互演示，按《神经网络与深度学习》章节顺序排列，便于直观理解。"
permalink: /viz/
redirect_from:
  - /v/
---

# 可视化资源

书中关键概念与模型的动图与交互演示，便于直观理解。条目按《神经网络与深度学习（第二版）》的章节顺序排列。

## 数学基础

<div class="viz-grid">
  {% include viz-card.html url="/viz/matrix-transform/" title="矩阵是空间变换" blurb="拖动 2×2 矩阵的四个数，看整个平面被旋转/缩放/剪切；列是基向量去向，行列式是面积缩放。" %}
  {% include viz-card.html url="/viz/eigenvectors/" title="特征向量与特征值" blurb="拖动向量 v，看矩阵把多数方向掰歪；只有沿特征向量方向 Av=λv，只拉伸不转向——PCA / 谱分解的根基。" %}
  {% include viz-card.html url="/viz/svd-lowrank/" title="SVD 与低秩近似" blurb="一张图就是个矩阵；SVD 拆成一摞秩 1 薄片，只留前几片重建就几乎看不出差别——压缩、PCA、LoRA 的共同直觉。" %}
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
  {% include viz-card.html url="/viz/early-stopping/" title="早停：见好就收" blurb="训练误差一路降、验证误差先降后升，停在 U 形谷底——见好就收的早停。" %}
  {% include viz-card.html url="/viz/gradient-descent/" title="梯度下降下山" blurb="小球沿曲线下山找最低点；调学习率看收敛、震荡，体会局部最优陷阱。" %}
  {% include viz-card.html url="/viz/bias-variance/" title="偏差与方差" blurb="同复杂度在多份数据上学出多条曲线，看是‘齐刷刷地偏’还是‘乱七八糟地飘’。" %}
  {% include viz-card.html url="/viz/learning-curve/" title="学习曲线：该加数据还是加模型" blurb="拖数据量看训练/验证误差怎么收敛：两条都卡高处=高偏差(该换强模型)、差距大且验证还在降=高方差(该加数据)。" %}
  {% include viz-card.html url="/viz/double-descent/" title="双下降现象" blurb="测试误差降→升→再降：模型大到参数比数据还多，反而比经典最优更好（挑战偏差方差）。" %}
  {% include viz-card.html url="/viz/precision-recall/" title="精确率与召回率" blurb="拖判定阈值，看混淆矩阵、精确率与召回率此消彼长，以及 ROC 曲线。" %}
  {% include viz-card.html url="/viz/confusion-matrix/" title="混淆矩阵与多类指标" blurb="三类混淆矩阵 + 各类精确率/召回/F1：类别不平衡时一个准确率会掩盖稀有类的崩溃，宏平均与微平均就此分道扬镳。" %}
  {% include viz-card.html url="/viz/calibration/" title="概率校准" blurb="模型说“90% 把握”真有 90% 对吗？可靠性图看点落在对角线下方=过度自信，调温度把它校准回对角线、ECE 降到最低。" %}
  {% include viz-card.html url="/viz/regularization/" title="正则化 L1 / L2" blurb="调正则强度，看 L2 让权重一起缩、L1 把一些权重压到 0（稀疏 / 特征选择）。" %}
  {% include viz-card.html url="/viz/l1-l2-geometry/" title="L1 / L2 的几何（为什么 L1 稀疏）" blurb="损失椭圆碰上约束区域：L1 菱形的尖角落在坐标轴上，解顶在尖角→一个权重精确归 0；L2 的圆只能让权重一起缩。" %}
  {% include viz-card.html url="/viz/loss-functions/" title="损失函数对比" blurb="对一个正样本拖动模型打分，并排看 MSE / 交叉熵 / Hinge / Focal 的惩罚曲线——交叉熵对“自信地答错”惩罚暴涨。" %}
  {% include viz-card.html url="/viz/decision-tree/" title="决策树与信息增益" blurb="按信息增益一刀刀切分平面，看决策树怎样把交叠的两类逐步分纯。" %}
  {% include viz-card.html url="/viz/knn/" title="k 近邻 KNN" blurb="拖查询点，看最近 k 个邻居投票分类；k 小决策边界碎、k 大边界平。" %}
  {% include viz-card.html url="/viz/bagging/" title="集成学习 Bagging" blurb="多个高方差弱模型一平均就变平滑、方差骤降，看一堆杂乱细线收敛成一条干净金线（随机森林核心）。" %}
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
     thumb="/assets/viz/ext/tf-playground.png"
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
     thumb="/assets/viz/ext/cnn-explainer.png" %}
  {% include viz-card.html url="/viz/conv-kernel/" title="卷积核手动滑动" blurb="3×3 核在图上一格格滑过，换边缘/竖线/锐化核，看同一张图被‘看’出不同特征。" %}
  {% include viz-card.html url="/viz/pooling/" title="汇聚（池化）" blurb="2×2 窗口扫过特征图，最大 / 平均汇聚把它缩小、保留要点（平移不变）。" %}
  {% include viz-card.html url="/viz/receptive-field/" title="感受野" blurb="拖层数，看顶层一个神经元的感受野（蓝色锥）怎样随深度张开——深度换广度。" %}
</div>

## 第 6 章 · 循环神经网络

<div class="viz-grid">
  {% include viz-card.html url="/viz/rnn-unroll/" title="RNN 按时间展开" blurb="一个词一个词地读，隐状态像一张滚动的便签把上文压进向量；每步都用同一套权重，所以能处理任意长度。" %}
  {% include viz-card.html url="/viz/rnn-counter/" title="RNN 当计数器" blurb="喂一串括号，看某个隐状态神经元自己学成计数器——遇“(”加一、遇“)”减一，隐状态里原来存着看得懂的信息。" %}
  {% include viz-card.html url="/viz/bptt-vanishing/" title="梯度消失与爆炸" blurb="误差沿时间回传，每退一步乘一次循环权重 w；拖 w 看久远梯度按 wᵏ 消失或爆炸——RNN 记不住长程的根因。" %}
  {% include viz-card.html url="/viz/lstm-gates/" title="LSTM 门控记忆" blurb="细胞状态像一条传送带，调遗忘 / 输入 / 输出三道门：遗忘门≈1 时，存进去的值能跨越很多步几乎不衰减。" %}
  {% include viz-card.html
     url="/viz/rnn-lstm/"
     title="RNN / LSTM / GRU"
     blurb="交互实验台：切换三种结构、编辑输入序列、单步观察门的开合与记忆沿时间的演化。"
     thumb="/assets/viz/ext/lstm-colah.png" %}
  {% include viz-card.html url="/viz/bidirectional-rnn/" title="双向 RNN" blurb="“我买了苹果手机”——点词看单向只能看左边，双向再跑一个反向 RNN 补上右文，“苹果”才从水果变品牌。" %}
  {% include viz-card.html url="/viz/char-rnn/" title="字符级 RNN 生成" blurb="一个字母一个字母地写：靠隐状态记着上文，q 后面自然接 u，字符拼成合理的词——更细颗粒的自回归。" %}
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
  {% include viz-card.html url="/viz/lr-schedule/" title="学习率调度" blurb="学习率随步数的“形状”才关键：没预热的大学习率开头就把损失冲飞；预热 + 余弦退火则平稳下降、收得更低。" %}
  {% include viz-card.html url="/viz/dropout/" title="Dropout" blurb="训练时随机关掉一部分神经元，逼网络学冗余表示、防过拟合；测试时再全开。" %}
  {% include viz-card.html url="/viz/batchnorm/" title="批归一化 BatchNorm" blurb="把每批激活减均值除标准差拉回‘均值0方差1’，让深层网络训练又快又稳。" %}
  {% include viz-card.html url="/viz/layernorm/" title="层归一化 vs 批归一化" blurb="切换 BatchNorm（按列跨样本）与 LayerNorm（按行跨特征），看归一化沿哪个方向算——Transformer 为何偏爱 LayerNorm。" %}
</div>

## 第 8 章 · 注意力机制与 Transformer

### 注意力机制

<div class="viz-grid">
  {% include viz-card.html
     url="/viz/attention/"
     title="注意力机制"
     blurb="编码—解码注意力、自注意力与多头注意力的可视化。"
     thumb="/assets/viz/ext/attention-jalammar.jpg" %}
  {% include viz-card.html url="/viz/self-attention/" title="点词看注意力" blurb="点句子里的一个词，看自注意力把它连向相关的词（如“它”指向“小猫”）。" %}
  {% include viz-card.html url="/viz/embeddings/" title="词向量类比" blurb="二维语义空间里‘国王−男人+女人≈王后’，看词与词的关系就是向量方向。" %}
  {% include viz-card.html url="/viz/qkv-attention/" title="QKV 注意力计算" blurb="拆开注意力的算法：Query·Key 算分数→softmax→对 Value 加权，看“它”怎么算出指向“猫”。" %}
  {% include viz-card.html url="/viz/attention-scaling/" title="注意力为何除以 √d" blurb="拖维度看不缩放的 softmax 怎样饱和成一根独大，÷√d 后又稳住——缩放点积注意力的由来。" %}
  {% include viz-card.html url="/viz/multi-head/" title="多头注意力" blurb="三个注意力头并排，各看相邻 / 指代 / 句首一种关系——多头分工再合议。" %}
  {% include viz-card.html
     url="/viz/sgm-seq2seq-rnn/"
     title="Seq2Seq · 基于 RNN"
     blurb="编码器—解码器结构的循环神经网络 Seq2Seq，常用于机器翻译。"
     thumb="/viz/sgm-seq2seq-rnn-mt.gif" %}
  {% include viz-card.html
     url="/viz/sgm-seq2seq-cnn/"
     title="Seq2Seq · 基于卷积"
     blurb="WaveNet 与 fairseq 卷积 Seq2Seq：用卷积代替循环，可并行训练。"
     thumb="/viz/sgm-seq2seq-cnn-mt.gif" %}
</div>

### Transformer

<div class="viz-grid">
  {% include viz-card.html
     url="/viz/positional-encoding/"
     title="正弦位置编码"
     blurb="拖查询位置看位置编码热力图：不同频率的正弦给每个位置唯一编码，相近位置编码也相近。"
     thumb="/assets/viz/positional-encoding.svg" %}
  {% include viz-card.html url="/viz/causal-mask/" title="因果掩码" blurb="给注意力盖上因果掩码，每个词只能看自己和左边，保证自回归生成不偷看答案。" %}
  {% include viz-card.html url="/viz/masked-lm/" title="掩码语言模型" blurb="盖住一个词让模型双向猜（BERT），对照只看左的因果模型——双向理解为何更全面。" %}
  {% include viz-card.html url="/viz/rope/" title="RoPE 旋转位置编码" blurb="位置编码成旋转角度，两词的注意力分数只取决于相对位置——更稳、还能外推到更长序列。" %}
  {% include viz-card.html
     url="/viz/sgm-seq2seq-transformer/"
     title="Seq2Seq · 基于 Transformer"
     blurb="基于自注意力机制，可并行处理整个序列，是当前大模型的基础架构。"
     thumb="/viz/sgm-seq2seq-transformer.gif" %}
</div>

## 第 9 章 · 图神经网络

<div class="viz-grid">
  {% include viz-card.html
     url="/viz/gnn/"
     title="GNN 消息传递"
     blurb="distill.pub 互动文章：节点 / 边特征如何在消息传递中聚合更新。"
     thumb="/assets/viz/ext/gnn-distill.jpg" %}
  {% include viz-card.html url="/viz/gnn-message-passing/" title="消息传递与过平滑" blurb="节点沿边把特征传给邻居取平均，拖层数看信息扩散，以及层数太多时所有节点趋同的‘过平滑’。" %}
  {% include viz-card.html url="/viz/gcn-node-classification/" title="GCN 半监督节点分类" blurb="只标 2 个节点，标签沿边一层层扩散，看一张社交网络图自动分成两派——少量标签 + 图结构带动全图。" %}
</div>

## 第 10 章 · 无监督学习

<div class="viz-grid">
  {% include viz-card.html url="/viz/kmeans/" title="K-means 聚类" blurb="随机撒下中心，反复“投靠最近中心→中心移到群中央”，看点被自动分成几组。" %}
  {% include viz-card.html url="/viz/pca/" title="PCA 主成分分析" blurb="二维点云自动找出最铺得开的主成分方向，沿它投影把二维压成一维。" %}
  {% include viz-card.html url="/viz/gmm/" title="高斯混合与 EM" blurb="高斯混合软聚类，EM 交替算归属概率 / 更新高斯；交界处的点是‘混色’的（对比 K-means 硬分配）。" %}
  {% include viz-card.html url="/viz/sparse-autoencoder/" title="稀疏自编码器" blurb="编码器把输入压成隐层、解码器再重构；稀疏约束逼大多数隐单元为 0——拖稀疏强度，看少数几个“特征”怎样既省又干净地重建信号。" %}
  {% include viz-card.html
     url="/viz/tsne/"
     title="t-SNE 与降维"
     blurb="distill.pub 经典互动：如何正确解读 t-SNE 图，以及 perplexity / 迭代步数的影响。"
     thumb="/assets/viz/ext/tsne-distill.jpg" %}
</div>

## 第 11 章 · 模型独立的学习方式

<div class="viz-grid">
  {% include viz-card.html url="/viz/adaboost/" title="AdaBoost 提升法" blurb="弱分类器一根接一根：每轮放大上轮分错的样本、最后加权投票，看一串横竖刀拼出贴合斜线的“楼梯”。" %}
</div>

## 第 12 章 · 深度强化学习

<div class="viz-grid">
  {% include viz-card.html
     url="/viz/rl-gridworld/"
     title="GridWorld 强化学习"
     blurb="Karpathy 的 REINFORCEjs：在网格世界里实时观察价值迭代、Q-Learning、Policy Gradient。"
     thumb="/assets/viz/ext/rl-reinforcejs.jpeg" %}
  {% include viz-card.html url="/viz/bandit/" title="多臂老虎机" blurb="几台隐藏中奖率的老虎机，ε-greedy 在探索与利用之间权衡，估计逐渐变准。" %}
  {% include viz-card.html url="/viz/explore-exploit/" title="探索 vs 利用" blurb="拖探索率 ε，看总收益的倒 U 曲线：太贪会锁死次优、太浪等于乱试，中间有甜点。" %}
  {% include viz-card.html url="/viz/value-iteration/" title="价值迭代" blurb="网格世界里价值从宝藏一格格扩散，箭头连成一条避开陷阱、通往宝藏的最优路线。" %}
  {% include viz-card.html url="/viz/q-learning/" title="Q-learning：从试错学策略" blurb="不给环境模型，智能体 ε-greedy 乱走 + TD 更新，几集后 Q 表收敛、箭头连成避开陷阱通往宝藏的策略——与价值迭代正好对照。" %}
</div>

## 第 13 章 · 大语言模型与智能体

<div class="viz-grid">
  {% include viz-card.html
     url="/viz/llm-internals/"
     title="LLM 内部结构（3D）"
     blurb="bbycroft.net/llm：3D 交互式 GPT 内部张量流动演示，从 token 到 logit 的全过程。" %}
  {% include viz-card.html url="/viz/tokenization/" title="词元化" blurb="输入文字看它被切成一个个词元；也解释了模型为什么数不清 strawberry 里有几个 r。" %}
  {% include viz-card.html url="/viz/bpe/" title="BPE 子词合并" blurb="从字符起步，反复合并最高频相邻对，看“est”“low”这样的子词怎样被一步步学出来。" %}
  {% include viz-card.html url="/viz/temperature/" title="温度采样" blurb="调‘温度’看模型挑下一个词的概率条重塑：低温保守稳定、高温有创意也容易胡说。" %}
  {% include viz-card.html url="/viz/top-k-top-p/" title="top-k 与 top-p 采样" blurb="切 top-k / top-p，看截断候选词表怎么砍掉长尾、控制生成稳重还是放飞（配合温度）。" %}
  {% include viz-card.html url="/viz/next-word/" title="下一词预测" blurb="用 bigram 语言模型按概率接词成句，看“按概率接龙”为什么会跑题、重复。" %}
  {% include viz-card.html url="/viz/autoregressive/" title="自回归逐词生成" blurb="一个字一个字预测、写下、再喂回输入，动态看 GPT 怎样把句子“接”出来。" %}
  {% include viz-card.html url="/viz/perplexity/" title="困惑度" blurb="切换好/一般/随机模型，看同一句话的困惑度差多少——模型读句子时有多惊讶。" %}
  {% include viz-card.html url="/viz/beam-search/" title="束搜索与贪心" blurb="解码树上贪心 vs 束搜索：贪心掉进局部最优，束搜索留 k 条找到整体更优的句子。" %}
  {% include viz-card.html url="/viz/scaling-laws/" title="缩放定律" blurb="损失随规模按幂律下降（log-log 直线），用小模型外推预测大模型，还有不可约下限。" %}
  {% include viz-card.html url="/viz/contrastive/" title="对比学习与 CLIP" blurb="点训练，看图文相似度矩阵的对角线怎样点亮——CLIP 用配对图文拉近正样本、推远负样本。" %}
  {% include viz-card.html url="/viz/moe/" title="混合专家 MoE" blurb="路由器把每个词只派给少数几个‘专家’子网络，参数海量但每次只算一小部分。" %}
  {% include viz-card.html url="/viz/kv-cache/" title="KV 缓存与 O(n²)" blurb="自回归生成时注意力是 O(n²)，KV 缓存把历史键值存起来复用，降到线性。" %}
  {% include viz-card.html url="/viz/speculative-decoding/" title="投机解码" blurb="小模型起草几个字、大模型并行核验采纳，看它如何在不改结果的前提下加速生成。" %}
  {% include viz-card.html url="/viz/quantization/" title="量化" blurb="把连续权重吸附到离散档位，fp32→int8/int4 看体积缩小与精度损失的权衡。" %}
  {% include viz-card.html url="/viz/lora/" title="LoRA 低秩微调" blurb="冻结大权重矩阵，只训两个小矩阵 A·B，微调参数从 d² 骤降到 2dr。" %}
  {% include viz-card.html url="/viz/rlhf-reward-model/" title="RLHF：偏好 → 奖励模型" blurb="人类只说“A 比 B 好”，Bradley-Terry 拟合出奖励曲线；再把策略 π∝π_ref·exp(r/β) 推向高分区，β 是拴住别跑偏的 KL 缰绳。" %}
</div>

## 第 14 章 · 概率图模型

<div class="viz-grid">
  {% include viz-card.html url="/viz/explaining-away/" title="解释消除（贝叶斯网络）" blurb="下雨和洒水器本独立；观测“草湿”后两者都更可能，再得知“下雨”→洒水器概率反被压回——对撞结构的解释消除。" %}
  {% include viz-card.html url="/viz/hmm-viterbi/" title="HMM 维特比解码" blurb="天气看不见，只看见带没带伞——用动态规划在网格里逐列挑最优前驱，回溯出最可能的隐藏天气序列。" %}
  {% include viz-card.html url="/viz/gmm/" title="高斯混合与 EM" blurb="含隐变量 z 的概率模型：每个点先选一个高斯、再采样得到坐标；EM 反推每个点的归属概率 P(z|x) 并更新各高斯。" %}
</div>

## 第 15 章 · 深度信念网络

<div class="viz-grid">
  {% include viz-card.html url="/viz/rbm-reconstruction/" title="RBM 编码与重构" blurb="两层网络来回采样：把带噪数字编码成几个特征隐单元，再只凭它们重构回来——噪声被滤掉，叠起来就是深度信念网络。" %}
</div>

## 第 16 章 · 深度生成模型

<div class="viz-grid">
  {% include viz-card.html
     url="/viz/diffusion/"
     title="扩散模型"
     blurb="前向加噪、反向去噪过程，以及与 GAN / VAE 的对比。"
     thumb="/assets/viz/ext/diffusion-lilianweng.png" %}
  {% include viz-card.html url="/viz/diffusion-noise/" title="扩散：加噪与去噪" blurb="把一张图的每个像素一步步掺成彩色雪花，再从噪声里去噪生成——亲手体会扩散模型画图的原理。" thumb="/assets/viz/diffusion-noise.jpg" %}
  {% include viz-card.html url="/viz/vae/" title="VAE 潜空间" blurb="拖动二维潜变量，看解码出的脸连续变形——潜空间平滑、随便取一点就能采样生成。" %}
  {% include viz-card.html url="/viz/gan-training/" title="GAN：生成器与判别器的博弈" blurb="判别器当警察、生成器当造假者交替训练；看金色假直方图一步步贴上真分布，切到双峰还能演示模式崩溃。" %}
  {% include viz-card.html
     url="/viz/gan-lab/"
     title="GAN Lab"
     blurb="PoloClub 互动玩具：在浏览器中训练一个 2D GAN，逐步可视化判别器与生成器的对抗。"
     thumb="/assets/viz/ext/ganlab.png" %}
</div>

---

<p style="color: var(--color-text-muted); font-size: 0.9rem;">
  欢迎贡献新的可视化资源：fork 仓库并在 <code>viz/</code> 下添加 markdown 与素材后提 PR。
</p>
