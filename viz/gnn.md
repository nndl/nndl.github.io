---
layout: default
title: 图神经网络
description: "distill.pub 互动文章：节点 / 边特征如何在消息传递中聚合更新。"
permalink: /viz/gnn/
redirect_from:
  - /v/gnn/
---

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 图神经网络（GNN）

图神经网络的核心运算是"消息传递"：每一层中，每个节点从其邻居收集特征，聚合后更新自己的表示。多层堆叠相当于不断扩大感受野。

## 消息传递的图示

<figure class="viz-figure viz-figure--wide">
  <img src="https://distill.pub/2021/gnn-intro/thumbnail.jpg" alt="GNN 消息传递示意" loading="lazy" onerror="this.style.display='none'">
  <figcaption>邻居节点的特征经过聚合（求和 / 平均 / 最大）后，与中心节点自身特征一起更新。点开原文可拖动节点，逐步查看消息如何在图上扩散。</figcaption>
  <small class="viz-figure__source">来源：Sanchez-Lengeling 等 — <a href="https://distill.pub/2021/gnn-intro/">A Gentle Introduction to Graph Neural Networks</a></small>
</figure>

## 看什么

- 节点 / 边 / 全局三种特征如何各自更新、相互交换
- 同一张图的不同任务（节点分类、边预测、图分类）如何复用同一份骨干
- 为什么 GNN 在分子、社交网络、推荐系统上自然适配

## 交互式资源

<div class="resource-grid">
  <a class="resource-card" href="https://distill.pub/2021/gnn-intro/" target="_blank" rel="noopener">
    <h3>A Gentle Introduction to GNNs ↗</h3>
    <p>distill.pub 互动文章，含可拖动节点查看消息传递的多个示例。</p>
  </a>
  <a class="resource-card" href="https://distill.pub/2021/understanding-gnns/" target="_blank" rel="noopener">
    <h3>Understanding Convolutions on Graphs ↗</h3>
    <p>姊妹篇：从谱方法到 GCN，再到注意力 / 消息传递的统一视角。</p>
  </a>
  <a class="resource-card" href="https://pytorch-geometric.readthedocs.io/en/latest/" target="_blank" rel="noopener">
    <h3>PyTorch Geometric ↗</h3>
    <p>主流 GNN 框架，文档自带大量可运行示例。</p>
  </a>
</div>
