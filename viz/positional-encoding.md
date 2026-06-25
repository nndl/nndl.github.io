---
layout: default
title: 正弦位置编码
description: "拖查询位置看位置编码热力图：不同频率的正弦给每个位置唯一编码，相近位置编码也相近。"
permalink: /viz/positional-encoding/
redirect_from:
  - /v/positional-encoding/
---

{% raw %}
<style>
.pelab svg{max-width:100%;height:auto;}
.pelab .cell{stroke:none;}
.pelab .qhi{fill:none;stroke:var(--color-gold);stroke-width:2.5;}
.pelab .simbar{fill:var(--color-accent);}
.pelab .lbl{font:10px var(--font-sans);fill:var(--color-text-muted);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 正弦位置编码

Transformer 同时看一整句话，本身分不清词的先后——“猫追狗”和“狗追猫”在它眼里一样。于是要给每个位置发一张独一无二的“身份证”，告诉模型谁在前谁在后。一个巧妙的办法：用**一组不同频率的正弦/余弦波**。低维是高频（快速摆动），高维是低频（缓慢摆动）；把每个位置在这些波上的取值拼起来，就成了它的位置编码。妙处在于：**相邻位置的编码很接近，相对距离还有稳定的规律**。下面左边是位置编码热力图，拖动“查询位置”，右边显示它和每个位置的相似度。

<section class="vizui pelab" id="pelab">
  <p class="vizui__lead">左图：每行一个位置（共 32 个），每列一个维度（共 24 个）。颜色是该维正弦/余弦的取值（<span style="color:#2563eb">蓝=−1</span>…<span style="color:#b5524a">红=+1</span>）。注意列从左到右摆动越来越慢——这就是不同频率。<b>金框</b>是当前查询位置，右边的蓝条是它与各位置编码的相似度。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="q">查询位置</label><input type="range" id="q" min="0" max="31" step="1" value="6" style="width:180px"><output id="qVal">6</output></span>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stat">—</span>
    </div>
    <svg id="plane" viewBox="0 0 410 320" role="img" aria-label="位置编码热力图"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>多频率正弦</b><p>每个维度是一条不同频率的波，组合起来给每个位置一个唯一编码。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>相近则相似</b><p>位置越近，编码越像（相似度越高）——模型因此能感知“谁挨着谁”。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>能外推</b><p>正弦是周期函数，公式直接算，遇到比训练更长的序列也能给出编码。</p></div>
  </div>
</section>

后续工作（RoPE、ALiBi、可学习位置嵌入）大多在“可外推、相对位置可线性表达、不占模型容量”这三点上做权衡。想深入可看：

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

{% raw %}
<script>
(function(){
"use strict";
var N=32,D=24,q=6;
var PE=[];for(var p=0;p<N;p++){PE.push([]);for(var d=0;d<D;d++){var i=Math.floor(d/2),fr=Math.pow(10000,-2*i/D),a=p*fr;PE[p].push(d%2===0?Math.sin(a):Math.cos(a));}}
function selfdot(p){var s=0;for(var d=0;d<D;d++)s+=PE[p][d]*PE[p][d];return s;}
function sim(p,p2){var s=0;for(var d=0;d<D;d++)s+=PE[p][d]*PE[p2][d];return s/Math.sqrt(selfdot(p)*selfdot(p2));}
var SVGNS="http://www.w3.org/2000/svg",cw=10,chh=8,hx=28,hy=16,simX=320,simW=64;
function col(v){var t=(v+1)/2,b=[37,99,235],w=[245,245,245],r=[181,82,74],a,c;if(t<0.5){a=t/0.5;c=[b[0]+(w[0]-b[0])*a,b[1]+(w[1]-b[1])*a,b[2]+(w[2]-b[2])*a];}else{a=(t-0.5)/0.5;c=[w[0]+(r[0]-w[0])*a,w[1]+(r[1]-w[1])*a,w[2]+(r[2]-w[2])*a];}return"rgb("+(c[0]|0)+","+(c[1]|0)+","+(c[2]|0)+")";}
function E(p,t,a,txt){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;p.appendChild(e);return e;}
var svg=document.getElementById("plane");
function setup(){
  var heatG=E(svg,"g",{});
  for(var p=0;p<N;p++)for(var d=0;d<D;d++)E(heatG,"rect",{x:hx+d*cw,y:hy+p*chh,width:cw,height:chh,fill:col(PE[p][d]),"class":"cell"});
  E(svg,"text",{x:hx+D*cw/2,y:hy-4,"text-anchor":"middle","class":"lbl"},"维度（频率：左快→右慢）");
  E(svg,"text",{x:10,y:hy+N*chh/2,"text-anchor":"middle","class":"lbl",transform:"rotate(-90 10 "+(hy+N*chh/2)+")"},"位置");
  E(svg,"text",{x:simX,y:hy-4,"class":"lbl"},"与查询的相似度");
}
function render(){
  var dyn=document.getElementById("dyn");if(dyn)svg.removeChild(dyn);
  var g=E(svg,"g",{id:"dyn"});
  E(g,"rect",{x:hx-1,y:hy+q*chh-1,width:D*cw+2,height:chh+2,"class":"qhi"});
  for(var p=0;p<N;p++){var s=sim(q,p);E(g,"rect",{x:simX,y:hy+p*chh,width:Math.max(0,s)*simW,height:chh-1,"class":"simbar",opacity:(0.35+0.65*Math.max(0,s)).toFixed(2)});}
  document.getElementById("qVal").textContent=q;
  document.getElementById("stat").textContent="位置 "+q+" 的编码";
  caption();
}
function caption(){
  var el=document.getElementById("caption");
  var near=q+1<N?q+1:q-1, far=(q+12)%N;
  el.innerHTML="位置 <b>"+q+"</b> 和邻近位置 "+near+" 的相似度高达 <b>"+sim(q,near).toFixed(2)+"</b>，和较远的位置 "+far+" 只有 <b>"+sim(q,far).toFixed(2)+"</b>。相似度大体随距离下降（近高远低，正弦编码会有些起伏）——这就是模型分辨先后、感知相对距离的依据。";
}
document.getElementById("q").addEventListener("input",function(e){q=+e.target.value;render();});
setup();render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  var seq=[14,22,3,6],k=0,sl=document.getElementById("q");var iv=setInterval(function(){q=seq[k];sl.value=q;render();k++;if(k>=seq.length)clearInterval(iv);},1100);},1000);
})();
</script>
{% endraw %}
