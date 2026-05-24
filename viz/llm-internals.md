---
layout: default
title: LLM 内部结构（3D）
permalink: /viz/llm-internals/
---

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# LLM 内部结构（3D）

Brendan Bycroft 制作的 LLM Visualization：以 3D 形式把一个真实的 GPT 内部张量逐步展开，让你"走进"模型中，看 token embedding、注意力、MLP、残差连接、归一化的每一步如何把输入转成下一个 token 的 logit。

> 这个项目以 3D 形式直接渲染了一个真实 GPT 模型的每一层张量——文字描述远不如亲自打开看一眼，建议先点底部的"LLM Visualization ↗"打开试试。

## 适合用来回答的问题

- 为什么 KV cache 是注意力层的"按位置缓存"
- 残差流（residual stream）在多层之间到底"流"了什么
- Layer Norm 在 Pre-LN / Post-LN 中位置不同会怎样影响梯度
- 一个 token 从词表 → embedding → 多层 Transformer → unembedding 的完整路径

## 交互式资源

<div class="resource-grid">
  <a class="resource-card" href="https://bbycroft.net/llm" target="_blank" rel="noopener">
    <h3>LLM Visualization ↗</h3>
    <p>3D 交互式 GPT/Transformer 可视化，按步骤展示每个张量。</p>
  </a>
  <a class="resource-card" href="https://poloclub.github.io/transformer-explainer/" target="_blank" rel="noopener">
    <h3>Transformer Explainer ↗</h3>
    <p>PoloClub 出品，可输入文本观察注意力分布与 logit 演化。</p>
  </a>
  <a class="resource-card" href="https://tiktokenizer.vercel.app/" target="_blank" rel="noopener">
    <h3>Tiktokenizer ↗</h3>
    <p>各家模型的 tokenizer 交互演示，理解 token 是怎么切分出来的。</p>
  </a>
</div>
