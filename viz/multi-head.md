---
layout: default
title: 多头注意力
description: "三个注意力头并排，各看相邻 / 指代 / 句首一种关系——多头分工再合议。"
permalink: /viz/multi-head/
redirect_from:
  - /v/multi-head/
---

{% raw %}
<style>
.mhlab .heads{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;}
.mhlab .head h4{margin:0 0 8px;font-size:.98rem;text-align:center;}
.mhlab .head h4 small{display:block;font-weight:400;font-size:.76rem;color:var(--color-text-muted);}
.mhlab .hm{display:grid;gap:2px;}
.mhlab .hm .lab{font:11px var(--font-sans);color:var(--color-text-muted);display:flex;align-items:center;justify-content:center;}
.mhlab .hm .cell{aspect-ratio:1;border-radius:2px;}
.mhlab .hint{font-size:.8rem;color:var(--color-text-muted);text-align:center;margin-top:6px;}
@media (max-width:680px){.mhlab .heads{grid-template-columns:1fr;max-width:320px;margin:0 auto;}}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 多头注意力

一个注意力“头”只能看一种关系；Transformer 干脆并排放好几个头，让它们各看各的——有的盯着相邻的词把短语黏起来，有的负责把代词连回它指的东西，有的让大家都参照句子开头。每个头单独看都偏科，合起来才把整句话读明白。下面三个头并排，读同一句话，看它们关注的模式有多不一样。

<section class="mhlab vizui" id="mhlab">
  <p class="vizui__lead">每个方阵是一个头的注意力：<b>行 = 哪个词在看，列 = 它看向谁</b>，格子越深表示越关注。同一句话，三个头给出完全不同的“看法”。</p>

  <div class="vizui-panel">
    <div class="heads" id="heads"></div>
    <div class="hint">把鼠标放到格子上可看具体权重。三个头都是“行内归一化”——每一行加起来是 100%。</div>
  </div>

  <div class="vizui-caption">真实模型一层有几十个头，并行算完后拼接、再融合。这种“分工 + 合议”让一层就能同时捕捉语法、指代、语序等多种关系——这是 Transformer 强大的关键之一。</div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-forest)"><b>相邻局部</b><p>主要看左右挨着的词，负责把短语、搭配黏合起来。</p></div>
    <div class="card" style="--wc:var(--color-accent)"><b>语义/指代</b><p>把含义相关的词连起来，比如“它”连回“小猫”。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>句首锚点</b><p>让大多数词都参照句子开头——真实模型里常见的一种模式。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var TOK=["小猫","追","老鼠","因为","它","饿"];
var N=TOK.length;
function norm(M){return M.map(function(row){var s=row.reduce(function(a,b){return a+b;},0)||1;return row.map(function(v){return v/s;});});}
function adj(){var M=[];for(var i=0;i<N;i++){var r=[];for(var j=0;j<N;j++)r.push(Math.exp(-(i-j)*(i-j)/1.4));M.push(r);}return norm(M);}
function sem(){var M=[];for(var i=0;i<N;i++){var r=[];for(var j=0;j<N;j++)r.push(i===j?0.4:0.05);M.push(r);}
  [[4,0,1.6],[1,0,1.0],[1,2,1.0],[5,4,1.2],[3,1,0.8]].forEach(function(l){M[l[0]][l[1]]+=l[2];});return norm(M);}
function anc(){var M=[];for(var i=0;i<N;i++){var r=[];for(var j=0;j<N;j++)r.push((j===0?1.0:0.06)+(i===j?0.3:0));M.push(r);}return norm(M);}
var HEADS=[{nm:"头 1",sub:"相邻局部",col:[32,106,79],M:adj()},{nm:"头 2",sub:"语义 / 指代",col:[21,94,117],M:sem()},{nm:"头 3",sub:"句首锚点",col:[183,121,31],M:anc()}];

function build(){
  var host=document.getElementById("heads");host.innerHTML="";
  HEADS.forEach(function(h){
    var d=document.createElement("div");d.className="head";
    d.innerHTML='<h4>'+h.nm+'<small>'+h.sub+'</small></h4>';
    var hm=document.createElement("div");hm.className="hm";hm.style.gridTemplateColumns="22px repeat("+N+",1fr)";
    hm.appendChild(cell("",""));
    TOK.forEach(function(t){hm.appendChild(cell(t,"lab"));});               // 列标题
    for(var i=0;i<N;i++){
      hm.appendChild(cell(TOK[i],"lab"));                                   // 行标题
      for(var j=0;j<N;j++){var w=h.M[i][j];var c=document.createElement("div");c.className="cell";
        c.style.background="rgb("+mix(h.col,w)+")";c.title=TOK[i]+" → "+TOK[j]+"："+(w*100).toFixed(0)+"%";hm.appendChild(c);}
    }
    d.appendChild(hm);host.appendChild(d);
  });
}
function mix(col,w){var lo=[239,242,240];return [Math.round(lo[0]+(col[0]-lo[0])*w),Math.round(lo[1]+(col[1]-lo[1])*w),Math.round(lo[2]+(col[2]-lo[2])*w)].join(",");}
function cell(txt,cls){var d=document.createElement("div");if(cls)d.className=cls;d.textContent=txt;return d;}
build();
})();
</script>
{% endraw %}
