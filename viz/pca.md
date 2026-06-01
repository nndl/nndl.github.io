---
layout: default
title: PCA 主成分分析
permalink: /viz/pca/
redirect_from:
  - /v/pca/
---

{% raw %}
<style>
.pcalab .axis{stroke:var(--color-border);stroke-width:1;}
.pcalab .pt{fill:var(--color-accent-light);opacity:.85;}
.pcalab .pc1{stroke:var(--color-accent);stroke-width:3.4;stroke-linecap:round;}
.pcalab .pc2{stroke:var(--color-gold);stroke-width:3;stroke-linecap:round;}
.pcalab .projln{stroke:var(--color-text-muted);stroke-width:1;opacity:.3;}
.pcalab .projpt{fill:var(--color-accent);}
.pcalab .mbar{height:14px;border-radius:7px;background:var(--color-bg-section);overflow:hidden;margin-top:4px;}
.pcalab .mbar i{display:block;height:100%;border-radius:7px;background:var(--color-accent);transition:width .3s var(--ease-out);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# PCA 主成分分析

一堆高维数据，怎么用更少的维度概括它、又尽量不丢信息？主成分分析（PCA）的思路是：找出数据**铺得最开的方向**当作新坐标轴。第一主成分 PC1 是方差最大的方向，沿它投影就能用一个数最好地概括每个点；PC2 与它垂直，管次要的变化。拖动“数据走向”，看主成分轴怎样始终对准数据的延展方向。

<section class="pcalab vizui" id="pcalab">
  <p class="vizui__lead"><span style="color:var(--color-accent);font-weight:600">蓝轴 PC1</span> 指向数据最“长”的方向，<span style="color:var(--color-gold);font-weight:600">金轴 PC2</span> 与它垂直。蓝轴上的小点是各数据点投影下来的结果——这就是把二维“压”成一维。</p>

  <div class="vizui-grid2">
    <div class="vizui-panel">
      <svg class="vizui-chart" id="plane" viewBox="0 0 320 320" style="max-width:360px;margin:0 auto;display:block" role="img" aria-label="PCA 主成分"></svg>
    </div>
    <div class="vizui-panel">
      <p class="vizui-panel__title">控制</p>
      <div class="vizui-field"><label for="ang">数据走向</label><input type="range" id="ang" min="0" max="170" step="5" value="30" style="width:150px"><output id="angVal">30°</output></div>
      <div class="vizui-field" style="margin-top:8px"><label for="ecc">扁平程度</label><input type="range" id="ecc" min="0.12" max="0.85" step="0.03" value="0.32" style="width:150px"><output id="eccVal">0.32</output></div>
      <button class="vizui-btn" id="regen" type="button" style="margin-top:12px">↻ 换一批点</button>
      <div style="margin-top:16px;font-size:.88rem;color:var(--color-text-soft)">PC1 解释了总变化的 <b id="ev" style="color:var(--color-accent);font-family:var(--font-mono)">—</b></div>
      <div class="mbar"><i id="evBar"></i></div>
      <p style="font-size:.82rem;color:var(--color-text-muted);margin-top:8px">越接近 100%，说明数据越“扁”，用一维（沿 PC1）概括就越不丢信息。</p>
    </div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>PC1 = 最大方差方向</b><p>数据沿哪个方向铺得最开，PC1 就指向哪——它由数据的协方差矩阵算出。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>降维 = 沿主轴投影</b><p>只保留 PC1 这一维，就把二维数据压成一维，尽量少丢信息。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>用处</b><p>高维数据可视化、去冗余、压缩、去噪——抓住主要的几个方向就够了。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var XR=3, theta=30*Math.PI/180, ecc=0.32, seed=4, base=[];
function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
function gauss(r){var u=0,v=0;while(!u)u=r();while(!v)v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}
function genBase(){var r=rng(seed);base=[];for(var i=0;i<44;i++)base.push([gauss(r),gauss(r)]);}
function pts(){var c=Math.cos(theta),s=Math.sin(theta),sx_=1.7,sy_=1.7*ecc;
  return base.map(function(p){var x=p[0]*sx_,y=p[1]*sy_;return [c*x-s*y, s*x+c*y];});}
function pca(P){
  var n=P.length,mx=0,my=0;P.forEach(function(p){mx+=p[0];my+=p[1];});mx/=n;my/=n;
  var cxx=0,cyy=0,cxy=0;P.forEach(function(p){var dx=p[0]-mx,dy=p[1]-my;cxx+=dx*dx;cyy+=dy*dy;cxy+=dx*dy;});cxx/=n;cyy/=n;cxy/=n;
  var tr=(cxx+cyy)/2,d=Math.sqrt(((cxx-cyy)/2)*((cxx-cyy)/2)+cxy*cxy);
  var l1=tr+d,l2=tr-d;
  var v1=Math.abs(cxy)>1e-9?[l1-cyy,cxy]:[1,0];var nv=Math.hypot(v1[0],v1[1])||1;v1=[v1[0]/nv,v1[1]/nv];
  var v2=[-v1[1],v1[0]];
  return {mx:mx,my:my,l1:l1,l2:l2,v1:v1,v2:v2};
}
var SVGNS="http://www.w3.org/2000/svg",W=320,H=320,O=160,SC=40;
function sx(x){return O+x*SC;} function sy(y){return O-y*SC;}
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function render(){
  var P=pts(),m=pca(P);
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  for(var i=-3;i<=3;i++){E(svg,"line",{x1:sx(i),y1:sy(-3),x2:sx(i),y2:sy(3),"class":"axis",opacity:i?0.3:1});E(svg,"line",{x1:sx(-3),y1:sy(i),x2:sx(3),y2:sy(i),"class":"axis",opacity:i?0.3:1});}
  var s1=Math.sqrt(m.l1)*2, s2=Math.sqrt(m.l2)*2;
  // 投影点 + 连线
  P.forEach(function(p){var dx=p[0]-m.mx,dy=p[1]-m.my,t=dx*m.v1[0]+dy*m.v1[1],px=m.mx+t*m.v1[0],py=m.my+t*m.v1[1];
    E(svg,"line",{x1:sx(p[0]),y1:sy(p[1]),x2:sx(px),y2:sy(py),"class":"projln"});});
  // 主轴
  E(svg,"line",{x1:sx(m.mx-m.v1[0]*s1),y1:sy(m.my-m.v1[1]*s1),x2:sx(m.mx+m.v1[0]*s1),y2:sy(m.my+m.v1[1]*s1),"class":"pc1"});
  E(svg,"line",{x1:sx(m.mx-m.v2[0]*s2),y1:sy(m.my-m.v2[1]*s2),x2:sx(m.mx+m.v2[0]*s2),y2:sy(m.my+m.v2[1]*s2),"class":"pc2"});
  P.forEach(function(p){E(svg,"circle",{cx:sx(p[0]),cy:sy(p[1]),r:4,"class":"pt"});});
  P.forEach(function(p){var dx=p[0]-m.mx,dy=p[1]-m.my,t=dx*m.v1[0]+dy*m.v1[1];E(svg,"circle",{cx:sx(m.mx+t*m.v1[0]),cy:sy(m.my+t*m.v1[1]),r:2.6,"class":"projpt"});});
  var ev=m.l1/(m.l1+m.l2);
  document.getElementById("ev").textContent=(ev*100).toFixed(0)+"%";
  document.getElementById("evBar").style.width=(ev*100)+"%";
  caption(ev);
}
function caption(ev){document.getElementById("caption").innerHTML="蓝色 PC1 自动对准了数据延展的方向，它解释了 <b>"+(ev*100).toFixed(0)+"%</b> 的变化。把每个点投到蓝轴上（轴上的小点）就是降到一维的结果——数据越扁，这样做丢的信息越少。";}
function render2(){document.getElementById("angVal").textContent=Math.round(theta*180/Math.PI)+"°";document.getElementById("eccVal").textContent=ecc.toFixed(2);render();}
document.getElementById("ang").addEventListener("input",function(e){theta=+e.target.value*Math.PI/180;render2();});
document.getElementById("ecc").addEventListener("input",function(e){ecc=+e.target.value;render2();});
document.getElementById("regen").addEventListener("click",function(){seed++;genBase();render();});
genBase();render2();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  var k=0,sl=document.getElementById("ang");var iv=setInterval(function(){k++;theta=(30+k*16)*Math.PI/180;sl.value=Math.round(theta*180/Math.PI)%170;render2();if(k>=9)clearInterval(iv);},480);},1000);
})();
</script>
{% endraw %}
