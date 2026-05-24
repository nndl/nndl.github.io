---
layout: default
title: 位置编码
permalink: /viz/positional-encoding/
---

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 位置编码

自注意力对位置不敏感，必须显式给输入序列注入位置信息。Transformer 原论文采用正弦 / 余弦位置编码——这是一种无参、可外推到任意长度的方案。

## 正弦位置编码热图

<figure class="viz-figure viz-figure--wide">
  <img src="https://jalammar.github.io/images/t/transformer_positional_encoding_example.png" alt="正弦位置编码热图" loading="lazy" onerror="this.style.display='none'">
  <figcaption>横轴为编码维度，纵轴为位置；每一行就是一个位置的编码向量。低维度变化快、高维度变化慢，类似多尺度时钟。</figcaption>
  <small class="viz-figure__source">来源：Jay Alammar — <a href="https://jalammar.github.io/illustrated-transformer/">The Illustrated Transformer</a></small>
</figure>

## 为什么用正弦 / 余弦

- **可外推**：训练时没见过的更长位置也能直接计算
- **相对位置可线性表达**：两个位置编码的差只与相对距离有关，便于注意力学相对偏移
- **无可学习参数**：不占模型容量

后续工作（RoPE、ALiBi、可学习位置嵌入等）大多在这三点上做权衡。

## 交互式资源

<div class="resource-grid">
  <a class="resource-card" href="https://kazemnejad.com/blog/transformer_architecture_positional_encoding/" target="_blank" rel="noopener">
    <h3>Transformer Positional Encoding ↗</h3>
    <p>Kazemnejad 的详细推导与图示，从向量几何解释正弦编码。</p>
  </a>
  <a class="resource-card" href="https://blog.eleuther.ai/rotary-embeddings/" target="_blank" rel="noopener">
    <h3>RoPE：旋转位置编码 ↗</h3>
    <p>EleutherAI 关于 RoPE 的可视化解读，当下大模型主流选择。</p>
  </a>
</div>
