---
layout: default
title: top-k 与 top-p 采样
permalink: /viz/top-k-top-p/
redirect_from:
  - /v/top-k-top-p/
---

{% raw %}
<style>
.tklab svg{max-width:100%;height:auto;}
.tklab .bar{fill:#cdd6db;}
.tklab .bar.keep{fill:var(--color-accent);}
.tklab .wlbl{font:12px var(--font-sans);fill:#333;}
.tklab .plbl{font:10px var(--font-mono);fill:var(--color-text-muted);}
.tklab .cut{stroke:#b5524a;stroke-width:1.5;stroke-dasharray:4 3;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# top-k 与 top-p 采样

大模型每写一个字，其实是在一长串候选词上掷骰子。直接按概率随机抽，偶尔会抽到那些概率极低的“怪词”，让句子跑偏。于是要先把长尾“砍掉”再抽：**top-k** 只留概率最高的固定 k 个词；**top-p（核采样）**留下概率从高到低累加刚好够 p（比如 90%）的那一小撮——候选多少随上下文自动伸缩。砍完再重新归一化、抽样。配合“温度”，这是控制生成“稳重还是放飞”的核心旋钮。切换方式、拖动滑块，看保留了哪些词。

<section class="vizui tklab" id="tklab">
  <p class="vizui__lead">每根柱子是一个候选词的概率（已按高到低排好）。<span style="color:var(--color-accent)">蓝色</span>是保留进抽样池的词，灰色是被砍掉的长尾，红色虚线是 top-p 的累积分界。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <button class="vizui-btn vizui-btn--go" id="mk" type="button">top-k</button>
      <button class="vizui-btn" id="mp" type="button">top-p（核采样）</button>
      <span class="vizui-spacer"></span>
      <span class="vizui-field"><label id="slabel" for="s">k</label><input type="range" id="s" min="1" max="12" step="1" value="4" style="width:150px"><output id="sVal">4</output></span>
      <span class="vizui-pill" id="stat">—</span>
    </div>
    <svg id="plane" viewBox="0 0 460 250" role="img" aria-label="采样截断"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>top-k：固定个数</b><p>永远留 k 个。简单，但分布很尖时留太多、很平时留太少。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>top-p：固定概率</b><p>留到累积概率够 p 为止，候选个数随上下文自动变多变少，更自适应。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>砍掉长尾</b><p>都是为了去掉概率极低的“怪词”，让生成既不呆板也不胡来。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var words=["好","不错","晴","热","棒","凉","冷","阴","差","糟","闷","妙"];
var logit=[3.4,2.7,2.1,1.7,1.3,1.0,0.7,0.4,0.1,-0.2,-0.5,-0.9];
var mx=Math.max.apply(null,logit),ex=logit.map(function(l){return Math.exp(l-mx);}),Z=ex.reduce(function(a,b){return a+b;},0);
var prob=ex.map(function(e){return e/Z;});
var n=words.length,mode="k",val=4;
var SVGNS="http://www.w3.org/2000/svg",W=460,H=250,pl=40,pr=14,pt=16,pb=44,bw=(W-pl-pr)/n;
function py(p){return (H-pb)-p/0.5*(H-pt-pb);}
function E(p,t,a,txt){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;p.appendChild(e);return e;}
function keptSet(){
  if(mode==="k")return val;
  var c=0,i=0;for(i=0;i<n;i++){c+=prob[i];if(c>=val)return i+1;}return n;
}
function render(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  E(svg,"line",{x1:pl,y1:H-pb,x2:W-pr,y2:H-pb,stroke:"var(--color-border-strong)","stroke-width":1});
  var keep=keptSet(),cov=0;
  for(var i=0;i<n;i++){
    var x=pl+i*bw,h=(H-pb)-py(prob[i]),on=i<keep;if(on)cov+=prob[i];
    E(svg,"rect",{x:x+3,y:py(prob[i]),width:bw-6,height:h,"class":"bar"+(on?" keep":""),rx:2});
    E(svg,"text",{x:x+bw/2,y:H-pb+16,"text-anchor":"middle","class":"wlbl"},words[i]);
    E(svg,"text",{x:x+bw/2,y:H-pb+30,"text-anchor":"middle","class":"plbl"},(prob[i]*100).toFixed(0)+"%");
  }
  if(mode==="p"){var xb=pl+keep*bw;E(svg,"line",{x1:xb,y1:pt,x2:xb,y2:H-pb,"class":"cut"});}
  document.getElementById("mk").className="vizui-btn"+(mode==="k"?" vizui-btn--go":"");
  document.getElementById("mp").className="vizui-btn"+(mode==="p"?" vizui-btn--go":"");
  document.getElementById("sVal").textContent=mode==="k"?val:val.toFixed(2);
  document.getElementById("stat").textContent="保留 "+keep+" 个 · 覆盖 "+(cov*100).toFixed(0)+"%";
  caption(keep,cov);
}
function caption(keep,cov){
  var el=document.getElementById("caption");
  if(mode==="k")el.innerHTML="<b>top-k = "+val+"：</b>不管概率分布长啥样，永远保留最高的 "+keep+" 个词（覆盖 "+(cov*100).toFixed(0)+"% 概率），其余长尾全砍掉再抽样。";
  else el.innerHTML="<b>top-p = "+val.toFixed(2)+"：</b>从高到低累加，到刚够 "+(val*100).toFixed(0)+"% 时停手——这里保留了 "+keep+" 个词。分布尖就留得少、分布平就留得多，自动伸缩。";
}
function setMode(m){mode=m;var s=document.getElementById("s");if(m==="k"){s.min=1;s.max=12;s.step=1;s.value=val=4;document.getElementById("slabel").textContent="k";}else{s.min=0.3;s.max=1;s.step=0.05;s.value=val=0.85;document.getElementById("slabel").textContent="p";}render();}
document.getElementById("mk").addEventListener("click",function(){setMode("k");});
document.getElementById("mp").addEventListener("click",function(){setMode("p");});
document.getElementById("s").addEventListener("input",function(e){val=+e.target.value;render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  setTimeout(function(){setMode("p");},1400);},1000);
})();
</script>
{% endraw %}
