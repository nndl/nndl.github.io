---
layout: default
title: GridWorld 强化学习
description: "Karpathy 的 REINFORCEjs：在网格世界里实时观察价值迭代、Q-Learning、Policy Gradient。"
permalink: /viz/rl-gridworld/
redirect_from:
  - /v/rl-gridworld/
---

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# GridWorld 强化学习

Andrej Karpathy 的 REINFORCEjs：在网格世界里实时观察价值函数、策略与轨迹的演化，是理解 RL 三大主线（基于价值 / 基于策略 / Actor-Critic）最直观的小工具。

## 三个层次的同一环境

<figure class="viz-figure viz-figure--wide">
  <img src="https://cs.stanford.edu/people/karpathy/reinforcejs/img/dpsolved.jpeg" alt="REINFORCEjs GridWorld 价值函数收敛" loading="lazy" onerror="this.style.display='none'">
  <figcaption>动态规划求解后的 GridWorld：每格的数值是状态价值 V(s)，箭头指向最优动作。同一个环境也支持 TD / Q-Learning / Policy Gradient 三种解法。</figcaption>
  <small class="viz-figure__source">来源：Andrej Karpathy — <a href="https://cs.stanford.edu/people/karpathy/reinforcejs/">REINFORCEjs</a></small>
</figure>

## 推荐的看法

1. 先看 **GridWorld: DP** —— 已知转移概率，迭代 Bellman 方程
2. 再看 **GridWorld: TD** —— 无模型采样，体会 Q-Learning 的更新
3. 最后看 **PuckWorld / WaterWorld** —— 连续状态下的策略梯度

## 交互式资源

<div class="resource-grid">
  <a class="resource-card" href="https://cs.stanford.edu/people/karpathy/reinforcejs/" target="_blank" rel="noopener">
    <h3>REINFORCEjs（主页）↗</h3>
    <p>Karpathy 的 RL 演示合集，纯浏览器运行，源码可读性极高。</p>
  </a>
  <a class="resource-card" href="https://cs.stanford.edu/people/karpathy/reinforcejs/gridworld_dp.html" target="_blank" rel="noopener">
    <h3>GridWorld: DP ↗</h3>
    <p>动态规划下的价值迭代实时演示。</p>
  </a>
  <a class="resource-card" href="https://huggingface.co/learn/deep-rl-course/unit0/introduction" target="_blank" rel="noopener">
    <h3>HuggingFace Deep RL Course ↗</h3>
    <p>系统的免费深度强化学习课程，含 Colab 实验。</p>
  </a>
</div>
