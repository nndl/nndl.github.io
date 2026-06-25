---
layout: default
title: 集成学习：平均的力量
description: "多个高方差弱模型一平均就变平滑、方差骤降，看一堆杂乱细线收敛成一条干净金线（随机森林核心）。"
permalink: /viz/bagging/
redirect_from:
  - /v/bagging/
---

{% raw %}
<style>
.baglab svg{max-width:100%;height:auto;}
.baglab .axis{stroke:var(--color-border-strong);stroke-width:1;}
.baglab .truth{fill:none;stroke:#9aa3a8;stroke-width:2;stroke-dasharray:5 4;}
.baglab .weak{fill:none;stroke:var(--color-accent);stroke-width:1;opacity:.18;}
.baglab .avg{fill:none;stroke:var(--color-gold);stroke-width:3;}
.baglab .pt{fill:var(--color-accent-light,#2563eb);opacity:.5;}
.baglab .alab{font:11px var(--font-sans);fill:var(--color-text-muted);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 集成学习：平均的力量

一棵深决策树很容易“想太多”——它把训练数据的噪声也学了进去，预测曲线抖来抖去（高方差）。但有个神奇的办法：**多训练几棵这样的树，每棵看数据的一个随机子集，最后把它们的预测一平均**。单棵抖得厉害，可它们的“抖”方向各不相同，一平均就互相抵消，结果又平滑又稳——这就是 Bagging（随机森林的核心）。拖动“模型个数”，看一堆杂乱的细线怎样平均出一条干净的金线。

<section class="vizui baglab" id="baglab">
  <p class="vizui__lead">蓝点是带噪声的训练数据，灰色虚线是背后的真实规律。每条<span style="color:var(--color-accent)">淡蓝细线</span>是一个高方差弱模型（看了数据的随机子集），<b>金线</b>是它们的平均。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="M">模型个数</label><input type="range" id="M" min="1" max="30" step="1" value="1" style="width:180px"><output id="mVal">1</output></span>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stat">—</span>
    </div>
    <svg id="plane" viewBox="0 0 460 300" role="img" aria-label="集成平均"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>弱模型高方差</b><p>单棵深树对数据子集很敏感，换批数据就给出很不一样的预测，曲线抖动大。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>平均抵消抖动</b><p>各模型的随机误差方向不同，平均后互相抵消，方差按约 1/M 下降。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>随机森林</b><p>就是这招：很多棵随机树投票/平均，简单却极强，是最常用的集成方法之一。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var n=46,G=90,NM=30;
function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
function gauss(r){var u=0,v=0;while(!u)u=r();while(!v)v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}
function truth(x){return 0.5+0.32*Math.sin(2*Math.PI*x*1.15);}
var dat=[],r=rng(11);
for(var i=0;i<n;i++){var x=r();dat.push({x:x,y:truth(x)+gauss(r)*0.12});}
var grid=[];for(var g=0;g<G;g++)grid.push(g/(G-1));
function fitWeak(rr){
  var idx=[];for(var k=0;k<n;k++)idx.push(Math.floor(rr()*n));
  var sp=[];for(var s2=0;s2<12;s2++)sp.push(rr());sp.sort(function(a,b){return a-b;});
  function bin(x){var b=0;for(var z=0;z<sp.length;z++)if(x>sp[z])b++;return b;}
  var sum={},cnt={};idx.forEach(function(ii){var b=bin(dat[ii].x);sum[b]=(sum[b]||0)+dat[ii].y;cnt[b]=(cnt[b]||0)+1;});
  var gm=0;idx.forEach(function(ii){gm+=dat[ii].y;});gm/=n;
  return grid.map(function(x){var b=bin(x);return cnt[b]?sum[b]/cnt[b]:gm;});
}
var models=[],rr=rng(77);for(var m=0;m<NM;m++)models.push(fitWeak(rr));
var M=1,SVGNS="http://www.w3.org/2000/svg",W=460,H=300,pl=34,pr=14,pt=12,pb=26;
function px(x){return pl+x*(W-pl-pr);}function py(y){return (H-pb)-y*(H-pt-pb);}
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function poly(svg,arr,cls){var pts=arr.map(function(y,i){return px(grid[i])+","+py(y);}).join(" ");E(svg,"polyline",{points:pts,"class":cls});}
function render(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  E(svg,"line",{x1:pl,y1:H-pb,x2:W-pr,y2:H-pb,"class":"axis"});E(svg,"line",{x1:pl,y1:pt,x2:pl,y2:H-pb,"class":"axis"});
  poly(svg,grid.map(truth),"truth");
  dat.forEach(function(d){E(svg,"circle",{cx:px(d.x),cy:py(d.y),r:3,"class":"pt"});});
  var avg=grid.map(function(_,i){var s=0;for(var m=0;m<M;m++)s+=models[m][i];return s/M;});
  for(var m=0;m<M;m++)poly(svg,models[m],"weak");
  poly(svg,avg,"avg");
  // 误差：平均模型 vs 真值
  var emse=0;avg.forEach(function(y,i){var d=y-truth(grid[i]);emse+=d*d;});emse/=G;
  document.getElementById("mVal").textContent=M;
  document.getElementById("stat").textContent="平均模型误差 "+(emse*1000).toFixed(1)+"‰";
  caption(M);
}
function caption(M){
  var el=document.getElementById("caption");
  if(M===1)el.innerHTML="<b>只有 1 个模型：</b>金线就是它本身——一条抖动的阶梯，把噪声也学了进去。多叠几个看看。";
  else if(M<8)el.innerHTML="<b>"+M+" 个模型：</b>细线各抖各的，但金线（平均）已经开始平滑、向灰色真实规律靠拢。";
  else el.innerHTML="<b>"+M+" 个模型：</b>单条细线依旧杂乱，但它们一平均，金线已经又平滑又贴近真实——随机误差被互相抵消掉了。这就是集成的威力。";
}
document.getElementById("M").addEventListener("input",function(e){M=+e.target.value;render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){M=20;document.getElementById("M").value=20;render();return;}
  var sl=document.getElementById("M");var iv=setInterval(function(){M+=2;if(M>=NM){M=NM;clearInterval(iv);}sl.value=M;render();},260);},1000);
})();
</script>
{% endraw %}
