---
layout: default
title: 混合专家 MoE
permalink: /viz/moe/
redirect_from:
  - /v/moe/
---

{% raw %}
<style>
.moelab .toks{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-bottom:6px;}
.moelab .tok{font-family:var(--font-serif);font-size:1.1rem;padding:7px 14px;border-radius:10px;border:1px solid var(--color-border);background:var(--color-bg-pure);cursor:pointer;transition:all .15s var(--ease-out);}
.moelab .tok:hover{border-color:var(--color-accent);}
.moelab .tok.sel{border-color:var(--color-accent);box-shadow:0 0 0 2px var(--color-accent-soft);font-weight:600;}
.moelab .experts{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;}
.moelab .exp{border:1px solid var(--color-border);border-radius:var(--radius-md);background:var(--color-bg-pure);padding:10px 8px;text-align:center;position:relative;transition:all .25s var(--ease-out);opacity:.45;}
.moelab .exp.on{opacity:1;border-color:var(--color-accent);box-shadow:var(--shadow-md);}
.moelab .exp .nm{font-size:.84rem;font-weight:600;}
.moelab .exp .gbar{height:6px;border-radius:4px;background:var(--color-bg-section);overflow:hidden;margin-top:6px;}
.moelab .exp .gbar i{display:block;height:100%;background:var(--color-accent);border-radius:4px;transition:width .3s;}
.moelab .exp .g{font:600 .78rem var(--font-mono);color:var(--color-text-muted);margin-top:3px;}
.moelab .exp .badge{position:absolute;top:-8px;right:-8px;background:var(--color-gold);color:#fff;font:600 .7rem var(--font-mono);padding:2px 6px;border-radius:999px;display:none;}
.moelab .exp.on .badge{display:block;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 混合专家 MoE

大模型想变得更聪明，最直接的办法是堆更多参数——但参数一多，每次计算都很贵。混合专家（MoE）给出一个巧办法：准备一大堆“专家”子网络，但每个词进来时，由一个**路由器**只挑其中最相关的少数几个（比如 8 个里挑 2 个）来处理，其余的专家这次根本不参与计算。于是模型可以拥有海量参数（容量大），每次实际算的却只有一小部分（速度快）。DeepSeek、Mixtral 这些模型都用了它。点不同的词，看路由器把它派给谁。

<section class="moelab vizui" id="moelab">
  <p class="vizui__lead">点上面任意一个词，路由器会给 8 个专家打分（蓝条），只激活分数最高的 <b>2</b> 个（高亮+金标），其余 6 个保持休眠。不同的词通常被派给不同的专家。</p>

  <div class="vizui-panel">
    <div class="toks" id="toks"></div>
    <div style="text-align:center;color:var(--color-text-muted);font-size:.85rem;margin-bottom:12px">↓ 路由器分配 ↓</div>
    <div class="experts" id="experts"></div>
    <div style="text-align:center;margin-top:14px" id="summary"></div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>路由器分配</b><p>一个小网络给每个词算出对各专家的“匹配分”，只选 top-k 个去处理这个词。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>稀疏激活</b><p>每个词只用一小部分专家——参数总量很大，但单次计算量很小。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>容量与速度兼得</b><p>用“更多参数但每次只用一点”换来更强能力而不显著变慢，是当下大模型的常见结构。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var TOKS=["猫","追","量子","纠缠","唐诗","炒菜"];
var EXP=["日常·A","日常·B","科学·C","科学·D","文学·E","数学·F","代码·G","通用·H"];
var K=2;
/* 每个词对 8 个专家的打分（logits），设计成不同词偏好不同专家 */
var LOGITS={
  "猫":[2.4,2.0,0.2,0.1,0.6,0.0,0.0,1.0],"追":[2.2,2.3,0.1,0.2,0.4,0.3,0.1,0.9],
  "量子":[0.2,0.1,2.6,2.2,0.3,1.2,0.2,0.8],"纠缠":[0.1,0.0,2.4,2.5,0.4,0.9,0.3,0.7],
  "唐诗":[0.5,0.4,0.2,0.1,2.7,0.0,0.1,1.1],"炒菜":[1.6,1.0,0.3,0.1,0.5,0.2,0.2,2.2]
};
var sel="量子";
function softmax(z){var m=Math.max.apply(null,z),e=z.map(function(v){return Math.exp(v-m);}),s=e.reduce(function(a,b){return a+b;},0);return e.map(function(v){return v/s;});}
function build(){
  var th=document.getElementById("toks");th.innerHTML="";
  TOKS.forEach(function(t){var b=document.createElement("button");b.className="tok"+(t===sel?" sel":"");b.textContent=t;b.addEventListener("click",function(){sel=t;render();});th.appendChild(b);});
  var eh=document.getElementById("experts");eh.innerHTML="";
  EXP.forEach(function(nm,i){var d=document.createElement("div");d.className="exp";d.dataset.i=i;
    d.innerHTML='<span class="badge">激活</span><div class="nm">'+nm+'</div><div class="gbar"><i></i></div><div class="g"></div>';eh.appendChild(d);});
}
function render(){
  document.querySelectorAll("#toks .tok").forEach(function(b){b.classList.toggle("sel",b.textContent===sel);});
  var g=softmax(LOGITS[sel]);
  var order=g.map(function(v,i){return [i,v];}).sort(function(a,b){return b[1]-a[1];});
  var topSet={};for(var i=0;i<K;i++)topSet[order[i][0]]=true;
  var exps=document.querySelectorAll("#experts .exp");
  exps.forEach(function(d,i){d.classList.toggle("on",!!topSet[i]);
    d.querySelector(".gbar i").style.width=(g[i]/order[0][1]*100).toFixed(0)+"%";
    d.querySelector(".g").textContent=(g[i]*100).toFixed(0)+"%";});
  var a=order[0],b=order[1],ga=g[a[0]],gb=g[b[0]],ngab=ga+gb;
  document.getElementById("summary").innerHTML="本次只激活 <b style='color:var(--color-accent)'>"+K+" / "+EXP.length+"</b> 个专家 · 输出 ≈ "+(ga/ngab*100).toFixed(0)+"%×"+EXP[a[0]]+" + "+(gb/ngab*100).toFixed(0)+"%×"+EXP[b[0]];
  caption(order);
}
function caption(order){
  document.getElementById("caption").innerHTML="词“<b>"+sel+"</b>”被路由器派给了 <b>"+EXP[order[0][0]]+"</b> 和 <b>"+EXP[order[1][0]]+"</b> 两个专家，其余 6 个这次完全没参与计算。换个词试试——“量子/纠缠”会去找科学专家，“猫/追”会去找日常专家。容量大、算得少，这就是 MoE。";
}
build();render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  var seq=["猫","量子","唐诗","炒菜","量子"],k=0;var iv=setInterval(function(){sel=seq[k];render();k++;if(k>=seq.length)clearInterval(iv);},1200);},1000);
})();
</script>
{% endraw %}
