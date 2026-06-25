---
layout: default
title: 高斯混合与 EM
description: "含隐变量 z 的概率模型：每个点先选一个高斯、再采样得到坐标；EM 反推每个点的归属概率 P(z|x) 并更新各高斯。"
permalink: /viz/gmm/
redirect_from:
  - /v/gmm/
---

{% raw %}
<style>
.gmmlab .axis{stroke:var(--color-border);stroke-width:1;}
.gmmlab .ell0{fill:rgba(181,82,74,.08);stroke:#b5524a;stroke-width:2;}
.gmmlab .ell1{fill:rgba(37,99,235,.08);stroke:#2563eb;stroke-width:2;}
.gmmlab .ctr{stroke:#fff;stroke-width:1.5;}
.gmmlab .pt{stroke:#fff;stroke-width:1;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 高斯混合与 EM

K-means 给每个点一个“硬”归属——非此即彼。但现实中两团数据常常交叠，边界上的点其实“两边都像”。高斯混合模型（GMM）用几个高斯分布来描述数据，给每个点一个**软**归属：60% 属于这簇、40% 属于那簇。怎么训练它？用 EM 算法反复两步——**E 步**：按当前的高斯算出每个点对各簇的归属概率；**M 步**：再用这些概率加权，更新每个高斯的中心和胖瘦。来回几轮，高斯就贴合了数据。点“单步”看它怎么收敛，注意交界处的点是“混色”的。

<section class="gmmlab vizui" id="gmmlab">
  <p class="vizui__lead">每个点的颜色按它的<b>软归属</b>混合：越偏红越属于红簇、越偏蓝越属于蓝簇，<span style="color:#6d5bd0;font-weight:600">交界处发紫</span>表示两边各一半。两个椭圆是当前拟合的高斯（中心 + 范围）。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <button class="vizui-btn vizui-btn--go" id="auto" type="button">▶ 自动迭代</button>
      <button class="vizui-btn" id="step" type="button">单步（E+M）</button>
      <button class="vizui-btn" id="reset" type="button">重置</button>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="iter">第 0 轮</span>
    </div>
    <svg class="vizui-chart" id="plane" viewBox="0 0 320 320" style="max-width:380px;margin:0 auto" role="img" aria-label="高斯混合软聚类"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>软归属</b><p>每个点对各簇都有一个概率，加起来为 1——比 K-means 的“非此即彼”更细腻。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>E 步 / M 步</b><p>E 步按当前高斯算归属概率，M 步用概率加权更新高斯，交替进行直到稳定。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>能拟合椭圆簇</b><p>高斯可以有不同大小和形状，比 K-means 更适合疏密不均、形状不同的簇。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var XR=2.5, pts=[], K=2, gauss2=[], iter=0, playing=false, timer=null;
function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
function gss(r){var u=0,v=0;while(!u)u=r();while(!v)v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}
function gen(){var r=rng(6);pts=[];
  for(var i=0;i<26;i++)pts.push({x:0.75+gss(r)*0.75,y:0.5+gss(r)*0.6});
  for(var j=0;j<26;j++)pts.push({x:-0.7+gss(r)*0.7,y:-0.45+gss(r)*0.8});}
function init(){gauss2=[{mx:-1.4,my:1.2,sx:1.0,sy:1.0,pi:0.5},{mx:1.4,my:-1.2,sx:1.0,sy:1.0,pi:0.5}];iter=0;resp();}
function N(p,g){var dx=p.x-g.mx,dy=p.y-g.my;return Math.exp(-(dx*dx/(2*g.sx*g.sx)+dy*dy/(2*g.sy*g.sy)))/(2*Math.PI*g.sx*g.sy);}
function resp(){pts.forEach(function(p){var a=gauss2[0].pi*N(p,gauss2[0]),b=gauss2[1].pi*N(p,gauss2[1]),s=a+b||1;p.r=a/s;});}
function step(){
  resp();                       // E 步
  for(var k=0;k<K;k++){var w=k===0?function(p){return p.r;}:function(p){return 1-p.r;};
    var sw=0,sx=0,sy=0;pts.forEach(function(p){var rk=w(p);sw+=rk;sx+=rk*p.x;sy+=rk*p.y;});
    var mx=sx/sw,my=sy/sw,svx=0,svy=0;pts.forEach(function(p){var rk=w(p);svx+=rk*(p.x-mx)*(p.x-mx);svy+=rk*(p.y-my)*(p.y-my);});
    gauss2[k].mx=mx;gauss2[k].my=my;gauss2[k].sx=Math.max(0.25,Math.sqrt(svx/sw));gauss2[k].sy=Math.max(0.25,Math.sqrt(svy/sw));gauss2[k].pi=sw/pts.length;}
  iter++;resp();
}
var SVGNS="http://www.w3.org/2000/svg",W=320,H=320,pad=14;
function wx(x){return pad+(x+XR)/(2*XR)*(W-2*pad);}
function wy(y){return (H-pad)-(y+XR)/(2*XR)*(H-2*pad);}
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function pcol(r){var red=[181,82,74],blue=[37,99,235];return "rgb("+Math.round(blue[0]+(red[0]-blue[0])*r)+","+Math.round(blue[1]+(red[1]-blue[1])*r)+","+Math.round(blue[2]+(red[2]-blue[2])*r)+")";}
function draw(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  E(svg,"line",{x1:wx(0),y1:pad,x2:wx(0),y2:H-pad,"class":"axis"});E(svg,"line",{x1:pad,y1:wy(0),x2:W-pad,y2:wy(0),"class":"axis"});
  var sc=(W-2*pad)/(2*XR);
  E(svg,"ellipse",{cx:wx(gauss2[0].mx),cy:wy(gauss2[0].my),rx:gauss2[0].sx*sc,ry:gauss2[0].sy*sc,"class":"ell0"});
  E(svg,"ellipse",{cx:wx(gauss2[1].mx),cy:wy(gauss2[1].my),rx:gauss2[1].sx*sc,ry:gauss2[1].sy*sc,"class":"ell1"});
  pts.forEach(function(p){E(svg,"circle",{cx:wx(p.x),cy:wy(p.y),r:5,fill:pcol(p.r),"class":"pt"});});
  E(svg,"circle",{cx:wx(gauss2[0].mx),cy:wy(gauss2[0].my),r:5,fill:"#b5524a","class":"ctr"});
  E(svg,"circle",{cx:wx(gauss2[1].mx),cy:wy(gauss2[1].my),r:5,fill:"#2563eb","class":"ctr"});
  document.getElementById("iter").textContent="第 "+iter+" 轮";
}
function render(){draw();caption();}
function caption(){
  var el=document.getElementById("caption"),mid=pts.filter(function(p){return p.r>0.35&&p.r<0.65;}).length;
  if(iter===0)el.innerHTML="开始：两个高斯随便放在角落，点的颜色还很模糊。点“单步”，E 步算归属、M 步挪高斯，看它们怎么找到两团数据。";
  else el.innerHTML="第 "+iter+" 轮：两个高斯椭圆已经罩住各自的点团。注意交界处还有 <b>"+mid+"</b> 个发紫的点——它们对两簇的归属都接近 50%，这正是“软聚类”与 K-means 硬分配的区别。";
}
function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("auto").textContent="▶ 自动迭代";}
function play(){stop();playing=true;document.getElementById("auto").textContent="⏸ 暂停";timer=setInterval(function(){step();render();if(iter>=20)stop();},650);}
document.getElementById("auto").addEventListener("click",function(){playing?stop():play();});
document.getElementById("step").addEventListener("click",function(){stop();step();render();});
document.getElementById("reset").addEventListener("click",function(){stop();init();render();});
gen();init();render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){for(var i=0;i<15;i++)step();render();return;}play();},1000);
})();
</script>
{% endraw %}
