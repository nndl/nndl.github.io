---
layout: book
title: 神经网络与深度学习：案例与实践
book_key: practice
permalink: /practice/
---

{%- assign book = site.data.books | where: "key", page.book_key | first -%}

## 关于本书

《神经网络与深度学习：案例与实践》是配套理论书（"蒲公英书"）的实战教程，覆盖各类经典模型与典型任务的端到端案例。提供 **PyTorch** 与 **PaddlePaddle** 两套实现。

## 代码仓库

<div class="resource-grid">
  <a class="resource-card" href="{{ book.repo }}/tree/main/pytorch">
    <h3>PyTorch 版</h3>
    <p>主推实现，跟随主流框架更新。位于 <code>nndl/nndl-practice</code> 仓库的 <code>pytorch/</code> 子目录。</p>
  </a>
  <a class="resource-card" href="https://github.com/nndl/practice-in-paddle">
    <h3>PaddlePaddle 版</h3>
    <p>第一版印刷书指向的官方实现版本。</p>
  </a>
</div>

## 章节案例

> *（待补充：按章节列出案例标题、对应理论书章节、notebook 链接、数据集说明。）*

| 章节 | 案例 | Notebook |
|------|------|----------|
| 第 2 章 | 鸢尾花分类（线性模型） | *待补充* |
| 第 4 章 | MNIST 手写数字识别（前馈网络） | *待补充* |
| 第 5 章 | CIFAR-10 图像分类（CNN） | *待补充* |
| ... | ... | ... |

## 反馈

通过 <a href="{{ book.repo }}/issues">{{ book.repo | replace: 'https://github.com/', '' }} Issues</a> 提交意见与勘误。
