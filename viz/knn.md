---
layout: default
title: k 近邻 KNN
permalink: /viz/knn/
redirect_from:
  - /v/knn/
---

{% raw %}
<style>
.knnlab .pt{stroke:#fff;stroke-width:1.3;}
.knnlab .pt.c1{fill:#2563eb;}
.knnlab .pt.c0{fill:#b5524a;}
.knnlab .pt.near{stroke:var(--color-gold);stroke-width:2.6;}
.knnlab .qline{stroke:var(--color-gold);stroke-width:1.2;opacity:.6;}
.knnlab .query{fill:var(--color-text);stroke:#fff;stroke-width:2;}
.knnlab svg{touch-action:none;cursor:crosshair;}
.knnlab .field rect{shape-rendering:crispEdges;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# k 近邻 KNN

最朴素的分类器之一：要判断一个新点是哪一类，就看离它最近的 k 个“邻居”都是什么类，谁多就归谁。它根本不“训练”，把数据记住就行。简单归简单，效果常常不差。关键的旋钮是 k：k 太小，决策边界跟着个别点抖得很碎（容易被噪声带偏）；k 太大，边界平滑但可能糊掉细节。拖动黑色查询点，调 k，看它的邻居和整片决策边界怎么变。

<section class="knnlab vizui" id="knnlab">
  <p class="vizui__lead">背景按“这个位置会被分成哪类”着色（淡蓝/淡红），交界处就是决策边界。拖动黑点，金圈是它最近的 k 个邻居，它们投票决定黑点的类别。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="k">邻居数 k</label><input type="range" id="k" min="1" max="15" step="2" value="1" style="width:180px"><output id="kVal">1</output></span>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="vote">—</span>
    </div>
    <svg class="vizui-chart" id="plane" viewBox="0 0 320 320" style="max-width:380px;margin:0 auto" role="img" aria-label="KNN 决策边界"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>邻居投票</b><p>找最近的 k 个点，多数表决——不需要训练，记住数据就能用。</p></div>
    <div class="card" style="--wc:#b5524a"><b>k 小 → 碎</b><p>k=1 只看最近一个，边界贴着每个点扭曲，容易过拟合、被噪声影响。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>k 大 → 平</b><p>k 大时多数人说了算，边界更平滑稳健，但太大就抹掉了局部细节。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var XR=2.5,k=1,pts=[],q={x:0.2,y:0.3},drag=false;
function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
function gauss(r){var u=0,v=0;while(!u)u=r();while(!v)v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}
(function(){var r=rng(11);
  for(var i=0;i<18;i++)pts.push({x:0.9+gauss(r)*0.85,y:0.6+gauss(r)*0.85,t:1});
  for(var j=0;j<18;j++)pts.push({x:-0.9+gauss(r)*0.85,y:-0.5+gauss(r)*0.85,t:0});
  // 故意放几个“噪声”点制造碎边界
  pts.push({x:-0.4,y:0.9,t:1});pts.push({x:0.6,y:-0.8,t:0});})();
function classify(x,y,kk){
  var d=pts.map(function(p){return [(p.x-x)*(p.x-x)+(p.y-y)*(p.y-y),p.t];}).sort(function(a,b){return a[0]-b[0];});
  var n1=0;for(var i=0;i<kk;i++)n1+=d[i][1];return {cls:n1>kk/2?1:0,n1:n1,near:d.slice(0,kk)};
}
var SVGNS="http://www.w3.org/2000/svg",W=320,H=320,pad=12,NG=24;
function wx(x){return pad+(x+XR)/(2*XR)*(W-2*pad);}
function wy(y){return (H-pad)-(y+XR)/(2*XR)*(H-2*pad);}
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var key in a)e.setAttribute(key,a[key]);p.appendChild(e);return e;}
function draw(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var fld=E(svg,"g",{"class":"field"}),cs=(W-2*pad)/NG;
  for(var i=0;i<NG;i++)for(var j=0;j<NG;j++){var x=-XR+2*XR*(i+0.5)/NG,y=-XR+2*XR*(j+0.5)/NG;
    var c=classify(x,y,k).cls;E(fld,"rect",{x:wx(x)-cs/2,y:wy(y)-cs/2,width:cs+0.6,height:cs+0.6,fill:c?"rgba(37,99,235,.13)":"rgba(181,82,74,.13)"});}
  var res=classify(q.x,q.y,k);
  res.near.forEach(function(d){});
  // 邻居连线 + 高亮（重新找最近 k 个对应的点）
  var dd=pts.map(function(p,idx){return [(p.x-q.x)*(p.x-q.x)+(p.y-q.y)*(p.y-q.y),idx];}).sort(function(a,b){return a[0]-b[0];});
  var nearIdx={};for(var m=0;m<k;m++)nearIdx[dd[m][1]]=true;
  pts.forEach(function(p,idx){if(nearIdx[idx])E(svg,"line",{x1:wx(q.x),y1:wy(q.y),x2:wx(p.x),y2:wy(p.y),"class":"qline"});});
  pts.forEach(function(p,idx){E(svg,"circle",{cx:wx(p.x),cy:wy(p.y),r:5.5,"class":"pt "+(p.t?"c1":"c0")+(nearIdx[idx]?" near":"")});});
  E(svg,"circle",{cx:wx(q.x),cy:wy(q.y),r:7.5,"class":"query"});
  document.getElementById("vote").textContent=k+" 个邻居：蓝 "+res.n1+" : 红 "+(k-res.n1)+" → 判为"+(res.cls?"蓝":"红");
}
function render(){document.getElementById("kVal").textContent=k;draw();caption();}
function caption(){
  document.getElementById("caption").innerHTML=k<=1?
    "k=1：只看最近的 1 个邻居，决策边界紧贴每个点、坑坑洼洼——那两个孤立点直接戳出两块小区域，这就是过拟合的样子。把 k 调大。":
    "k="+k+"：由最近 "+k+" 个邻居多数表决，决策边界明显平滑多了，孤立噪声点被周围的多数“淹没”，更稳健。但 k 太大也会抹掉真实的细节。";
}
document.getElementById("k").addEventListener("input",function(e){k=+e.target.value;render();});
var svg=document.getElementById("plane");
function toW(e){var r=svg.getBoundingClientRect();return [((e.clientX-r.left)/r.width*W-pad)/(W-2*pad)*(2*XR)-XR, ((H-pad-(e.clientY-r.top)/r.height*H)/(H-2*pad))*(2*XR)-XR];}
svg.addEventListener("pointerdown",function(e){drag=true;svg.setPointerCapture(e.pointerId);var w=toW(e);q={x:w[0],y:w[1]};render();});
svg.addEventListener("pointermove",function(e){if(!drag)return;var w=toW(e);q={x:Math.max(-XR,Math.min(XR,w[0])),y:Math.max(-XR,Math.min(XR,w[1]))};render();});
svg.addEventListener("pointerup",function(){drag=false;});svg.addEventListener("pointercancel",function(){drag=false;});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){k=9;render();return;}
  var seq=[1,3,7,13,5],i=0,sl=document.getElementById("k");var iv=setInterval(function(){k=seq[i];sl.value=k;render();i++;if(i>=seq.length)clearInterval(iv);},950);},1000);
})();
</script>
{% endraw %}
