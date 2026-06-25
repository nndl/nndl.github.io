---
layout: default
title: GCN 半监督节点分类
description: "只标 2 个节点，标签沿边一层层扩散，看一张社交网络图自动分成两派——少量标签 + 图结构带动全图。"
permalink: /viz/gcn-node-classification/
redirect_from:
  - /v/gcn-node-classification/
---

{% raw %}
<style>
.gclab svg{max-width:100%;height:auto;background:var(--color-bg-soft,#f4f1ec);border-radius:var(--radius-sm);}
.gclab .edge{stroke:#b9c2c7;stroke-width:2;}
.gclab .edge.bridge{stroke:#9aa3a8;stroke-dasharray:5 4;}
.gclab .node{stroke:#fff;stroke-width:2;}
.gclab .node.seed{stroke:var(--color-text);stroke-width:3;}
.gclab .nlbl{font:12px var(--font-sans);fill:#fff;font-weight:700;}
.gclab .slbl{font:9px var(--font-sans);fill:var(--color-text-muted);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# GCN 半监督节点分类：几个标签带动全图

一张社交网络图里，只有极少数人被打了标签（属于哪一派），其余全是未知。**图卷积网络（GCN）** 怎么把标签补全？核心动作和[消息传递](/viz/gnn-message-passing/)一样：每个节点反复**聚合邻居的信息**（按边取平均）来更新自己。已知标签像染料从种子节点顺着边一层层扩散——同一社区内部连得密、相互印证，于是整张图自然被染成两派，连只有一个种子的社区也能被正确分类。这就是“半监督”：少量标签 + 图结构，带动全图。拖动传播层数，看两个种子怎样把颜色铺满全图。

<section class="vizui gclab" id="gclab">
  <p class="vizui__lead">只有 2 个节点有标签（<span style="color:var(--color-text)">深色圈</span>＝种子：<span style="color:#2563eb">A 派蓝</span>、<span style="color:#b5524a">B 派红</span>），其余初始为<span style="color:#9aa3a8">灰</span>（未知）。每传播一层，节点＝自己与邻居的平均，颜色越饱和表示越笃定。看标签怎样沿边扩散、把图分成两派。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="L">传播层数</label><input type="range" id="L" min="0" max="6" step="1" value="0" style="width:170px"><output id="lVal">0</output></span>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stat">—</span>
    </div>
    <svg id="plane" viewBox="0 0 440 240" role="img" aria-label="GCN 节点分类"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>半监督</b><p>只需极少量已标注节点，靠图结构把标签传播到大量未标注节点上。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>邻居聚合＝图卷积</b><p>每层让节点融合邻居特征（这里是标签得分），多层后“看”得更远。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>社区结构</b><p>同社区内部连得密、彼此印证，标签在社区内迅速一致，跨社区的桥几乎拦住扩散。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var pos=[[55,70],[105,45],[120,105],[60,135],[110,170],[160,80],[178,130],
         [262,110],[300,55],[335,105],[295,162],[370,60],[390,120],[360,172]];
var edges=[[0,1],[0,3],[1,2],[1,5],[2,3],[2,4],[2,5],[2,6],[3,4],[4,6],[5,6],
           [7,8],[7,9],[7,10],[8,9],[8,11],[9,10],[9,11],[9,12],[10,13],[11,12],[12,13],
           [6,7]];
var N=pos.length,bridge=[6,7];
var seeds=[{i:0,v:[1,0]},{i:13,v:[0,1]}];
var adj=[];for(var i=0;i<N;i++)adj.push([]);
edges.forEach(function(e){adj[e[0]].push(e[1]);adj[e[1]].push(e[0]);});
function isSeed(i){for(var k=0;k<seeds.length;k++)if(seeds[k].i===i)return seeds[k];return null;}
function propagate(L){
  var x=[];for(var i=0;i<N;i++){var s=isSeed(i);x.push(s?s.v.slice():[0,0]);}
  for(var t=0;t<L;t++){var nx=[];
    for(var i=0;i<N;i++){var a=x[i][0],b=x[i][1],c=1;
      adj[i].forEach(function(j){a+=x[j][0];b+=x[j][1];c++;});nx.push([a/c,b/c]);}
    seeds.forEach(function(sd){nx[sd.i]=sd.v.slice();});x=nx;}
  return x;
}
var L=0,SVGNS="http://www.w3.org/2000/svg";
function col(d){var t=(d+1)/2;t=t<0?0:t>1?1:t;var R=[181,82,74],G=[208,211,214],Bl=[37,99,235],a,c;
  if(t<0.5){a=t/0.5;c=[R[0]+(G[0]-R[0])*a,R[1]+(G[1]-R[1])*a,R[2]+(G[2]-R[2])*a];}
  else{a=(t-0.5)/0.5;c=[G[0]+(Bl[0]-G[0])*a,G[1]+(Bl[1]-G[1])*a,G[2]+(Bl[2]-G[2])*a];}
  return "rgb("+(c[0]|0)+","+(c[1]|0)+","+(c[2]|0)+")";}
function E(p,t,a,txt){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;p.appendChild(e);return e;}
function render(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var x=propagate(L);
  edges.forEach(function(e){var br=(e[0]===bridge[0]&&e[1]===bridge[1]);
    E(svg,"line",{x1:pos[e[0]][0],y1:pos[e[0]][1],x2:pos[e[1]][0],y2:pos[e[1]][1],"class":"edge"+(br?" bridge":"")});});
  var done=0;
  for(var i=0;i<N;i++){var d=x[i][0]-x[i][1],sd=isSeed(i);
    if(Math.abs(d)>0.01)done++;
    E(svg,"circle",{cx:pos[i][0],cy:pos[i][1],r:15,fill:col(d),"class":"node"+(sd?" seed":"")});
    if(sd)E(svg,"text",{x:pos[i][0],y:pos[i][1]+4,"text-anchor":"middle","class":"nlbl"},sd.v[0]>sd.v[1]?"A":"B");}
  E(svg,"text",{x:pos[0][0],y:pos[0][1]-20,"text-anchor":"middle","class":"slbl"},"种子");
  E(svg,"text",{x:pos[13][0],y:pos[13][1]+26,"text-anchor":"middle","class":"slbl"},"种子");
  document.getElementById("lVal").textContent=L;
  document.getElementById("stat").textContent="已分类 "+done+" / "+N+" 个节点";
  caption(done);
}
function caption(done){
  var el=document.getElementById("caption");
  if(L===0){el.innerHTML="<b>0 层：</b>全图只有 2 个种子有标签（A 蓝、B 红），其余都是灰色未知。拖动传播层数，看标签沿边扩散。";return;}
  if(done<N)el.innerHTML="<b>"+L+" 层：</b>标签从种子向外扩散了 "+L+" 跳，已染到 <b>"+done+"/"+N+"</b> 个节点。离种子越近、颜色越笃定，还没传到的仍是灰的。再加层。";
  else el.innerHTML="<b>"+L+" 层：</b>全部 "+N+" 个节点都被分类了——左簇归 A、右簇归 B，泾渭分明。仅靠 2 个标签加图结构就完成了全图分类，这正是 GCN 的半监督节点分类。";
}
document.getElementById("L").addEventListener("input",function(e){L=+e.target.value;render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){L=6;document.getElementById("L").value=6;render();return;}
  var seq=[1,2,3,4,6],k=0,sl=document.getElementById("L");var iv=setInterval(function(){L=seq[k];sl.value=L;render();k++;if(k>=seq.length)clearInterval(iv);},950);},1000);
})();
</script>
{% endraw %}

## 延伸阅读

<div class="resource-grid">
  <a class="resource-card" href="https://distill.pub/2021/gnn-intro/" target="_blank" rel="noopener">
    <h3>A Gentle Introduction to GNNs ↗</h3>
    <p>distill.pub 互动文章，从零讲清图神经网络与消息传递。</p>
  </a>
  <a class="resource-card" href="https://tkipf.github.io/graph-convolutional-networks/" target="_blank" rel="noopener">
    <h3>Thomas Kipf · GCN 博客 ↗</h3>
    <p>GCN 原作者讲半监督节点分类，含空手道俱乐部的经典例子。</p>
  </a>
</div>
