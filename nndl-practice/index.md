---
layout: book
title: 神经网络与深度学习：案例与实践
book_key: practice
permalink: /nndl-practice/
redirect_from:
  - /practice/
---

{%- assign book = site.data.books | where: "key", page.book_key | first -%}

## 关于本书

《神经网络与深度学习：案例与实践》是配套理论书（"蒲公英书"）的实战教程，每一类经典模型对应一个端到端案例，可运行 notebook + 实现要点 README + pytest sanity 测试。

## 代码仓库

<div class="resource-grid">
  <a class="resource-card" href="{{ book.repo }}/tree/main/pytorch">
    <h3>PyTorch 版（主推）</h3>
    <p>10 章覆盖：实践基础 / 机器学习 / 线性模型 / 前馈 / 卷积 / 循环 / 优化与正则化 / 注意力 / 图神经网络 / 大语言模型与智能体。位于 <code>nndl/nndl-practice</code> 仓库的 <code>pytorch/</code> 子目录，跟随主流框架更新。</p>
  </a>
  <a class="resource-card" href="https://github.com/nndl/practice-in-paddle">
    <h3>PaddlePaddle 版</h3>
    <p>第一版印刷书指向的官方实现，独立仓库 <code>nndl/practice-in-paddle</code>，按当时印刷版冻结。</p>
  </a>
  <a class="resource-card" href="{{ book.repo }}/tree/main/legacy">
    <h3>历史练习 <code>legacy/</code></h3>
    <p>原 <code>nndl/exercise</code> 仓库（2017–2024）的章末编程练习（numpy / 早期 PyTorch），对应<strong>理论书第 1 版</strong>。改名后整体归档到本仓库 <code>legacy/</code> 下。</p>
  </a>
</div>

## 反馈

通过 <a href="{{ book.repo }}/issues">{{ book.repo | replace: 'https://github.com/', '' }} Issues</a> 提交意见与勘误。

> 本书定位于动手实战，配合理论书一起读效果最好。系列内不同读者的搭配建议见 [**阅读路径**]({{ '/reading-path/' | relative_url }})。
