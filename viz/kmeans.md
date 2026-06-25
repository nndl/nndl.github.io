---
layout: default
title: K-means 聚类
description: "随机撒下中心，反复“投靠最近中心→中心移到群中央”，看点被自动分成几组。"
permalink: /viz/kmeans/
redirect_from:
  - /v/kmeans/
---

{% raw %}
<style>
.kmlab .axis{stroke:var(--color-border);stroke-width:1;}
.kmlab .pt{stroke-width:0;opacity:.9;}
.kmlab .pt.un{fill:var(--color-text-muted);opacity:.5;}
.kmlab .link{stroke-width:1;opacity:.18;}
.kmlab .ctr{stroke:#fff;stroke-width:2;}
.kmlab svg{touch-action:none;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# K-means 聚类

给一堆没有标签的点，怎么让机器自动把它们分成几组？K-means 用一个特别朴素的来回办法：先随手撒下几个“中心”，然后不停重复两步——每个点投靠离它最近的中心、每个中心挪到自己那群点的正中央。要不了几轮，中心就各自落进一团点里。看它自己把点分好组。

<section class="vizui kmlab" id="kmlab">
  <p class="vizui__lead">大菱形是“聚类中心”,小点按颜色表示当前归属。每走一步：① 每个点投靠最近的中心；② 中心移到自己那群点的平均位置。重复到不再变化。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="k">分几组（k）</label>
        <input type="range" id="k" min="2" max="5" step="1" value="4" style="width:120px">
        <output id="kVal">4</output>
      </span>
      <span class="vizui-spacer"></span>
      <button class="vizui-btn vizui-btn--go" id="go" type="button">▶ 自动聚类</button>
      <button class="vizui-btn" id="step" type="button">单步</button>
      <button class="vizui-btn" id="reset" type="button">重撒中心</button>
      <button class="vizui-btn" id="regen" type="button">↻ 换一批点</button>
    </div>
  </div>

  <div class="vizui-panel">
    <div class="vizui-bar" style="justify-content:center">
      <svg class="vizui-chart" id="plane" viewBox="0 0 360 300" style="max-width:420px;margin:0 auto" role="img" aria-label="K-means 聚类平面"></svg>
    </div>
    <div style="text-align:center;margin-top:6px"><span id="status" class="vizui-pill">第 0 步</span></div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>① 投靠最近的中心</b><p>每个点看看哪个中心离自己最近，就归到那一组、染上那个颜色。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>② 中心移到群中央</b><p>每个中心挪到自己这群点的平均位置，更贴合这团点。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>反复到稳定</b><p>两步交替几轮后，谁都不再换组，聚类就完成了。换 k、重撒中心，结果可能不同。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var COL=["#155e75","#b7791f","#206a4f","#6d5bd0","#2563eb"];
var XR=2.8, k=4, dataSeed=3, initSeed=11;
var pts=[], centers=[], assign=[], step=0, converged=false, playing=false, timer=null;

function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
function gauss(r){var u=0,v=0;while(!u)u=r();while(!v)v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}
function genPts(){
  var r=rng(dataSeed), C=[[-1.3,1.2],[1.4,1.0],[-1.2,-1.3],[1.3,-1.15]]; pts=[];
  C.forEach(function(c){for(var i=0;i<14;i++)pts.push({x:c[0]+gauss(r)*0.46,y:c[1]+gauss(r)*0.46});});
}
function initCenters(){
  var r=rng(initSeed), idx=[]; centers=[];
  while(idx.length<k){var j=Math.floor(r()*pts.length);if(idx.indexOf(j)<0)idx.push(j);}
  idx.forEach(function(j){centers.push({x:pts[j].x,y:pts[j].y});});
  assign=pts.map(function(){return -1;}); step=0; converged=false;
}
function assignAll(){
  var changed=false;
  pts.forEach(function(p,i){
    var best=0,bd=1e9;
    for(var c=0;c<centers.length;c++){var dx=p.x-centers[c].x,dy=p.y-centers[c].y,d=dx*dx+dy*dy;if(d<bd){bd=d;best=c;}}
    if(assign[i]!==best){assign[i]=best;changed=true;}
  });
  return changed;
}
function updateCenters(){
  for(var c=0;c<centers.length;c++){
    var sx=0,sy=0,n=0;
    for(var i=0;i<pts.length;i++)if(assign[i]===c){sx+=pts[i].x;sy+=pts[i].y;n++;}
    if(n>0){centers[c].x=sx/n;centers[c].y=sy/n;}
  }
}
function stepOnce(){
  if(converged)return;
  var changed=assignAll();
  updateCenters(); step++;
  if(!changed&&step>1)converged=true;
}

var SVGNS="http://www.w3.org/2000/svg",W=360,H=300,pad=16;
function wx(x){return pad+(x+XR)/(2*XR)*(W-2*pad);}
function wy(y){return (H-pad)-(y+XR)/(2*XR)*(H-2*pad);}
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k2 in a)e.setAttribute(k2,a[k2]);p.appendChild(e);return e;}
function draw(){
  var svg=document.getElementById("plane"); while(svg.firstChild)svg.removeChild(svg.firstChild);
  E(svg,"line",{x1:wx(0),y1:pad,x2:wx(0),y2:H-pad,"class":"axis"});
  E(svg,"line",{x1:pad,y1:wy(0),x2:W-pad,y2:wy(0),"class":"axis"});
  // 连线（点→所属中心）
  pts.forEach(function(p,i){if(assign[i]>=0){var c=centers[assign[i]];E(svg,"line",{x1:wx(p.x),y1:wy(p.y),x2:wx(c.x),y2:wy(c.y),stroke:COL[assign[i]],"class":"link"});}});
  // 点
  pts.forEach(function(p,i){E(svg,"circle",{cx:wx(p.x),cy:wy(p.y),r:4.5,fill:assign[i]>=0?COL[assign[i]]:"",  "class":"pt"+(assign[i]<0?" un":"")});});
  // 中心（菱形）
  centers.forEach(function(c,i){var x=wx(c.x),y=wy(c.y),s=9;
    E(svg,"polygon",{points:x+","+(y-s)+" "+(x+s)+","+y+" "+x+","+(y+s)+" "+(x-s)+","+y,fill:COL[i],"class":"ctr"});});
  document.getElementById("status").textContent=converged?("聚类完成（共 "+step+" 步）"):("第 "+step+" 步");
}
function caption(){
  var el=document.getElementById("caption");
  if(converged){el.innerHTML="<b>聚类完成！</b>"+k+" 个中心各自落进了一团点的中央，所有点被自动分成了 "+k+" 组——全程没有用到任何标签。试试换个 k，或“重撒中心”看会不会分得不一样。";return;}
  if(step===0){el.innerHTML="点“自动聚类”。"+k+" 个中心刚随机撒下，灰点还没归组。看它们怎样一步步各就各位。";return;}
  el.innerHTML="第 "+step+" 步：每个点已投靠最近的中心（同色），中心也移到了各自群点的中央。还没稳定，继续。";
}
function render(){document.getElementById("kVal").textContent=k;draw();caption();}

function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("go").textContent="▶ 自动聚类";}
function play(){if(converged)initCenters();stop();playing=true;document.getElementById("go").textContent="⏸ 暂停";
  timer=setInterval(function(){stepOnce();render();if(converged||step>=40)stop();},760);}
document.getElementById("go").addEventListener("click",function(){playing?stop():play();});
document.getElementById("step").addEventListener("click",function(){stop();stepOnce();render();});
document.getElementById("reset").addEventListener("click",function(){stop();initSeed++;initCenters();render();});
document.getElementById("regen").addEventListener("click",function(){stop();dataSeed++;genPts();initCenters();render();});
document.getElementById("k").addEventListener("input",function(e){stop();k=+e.target.value;initCenters();render();});

/* 启动 + 自动演示 */
genPts();initCenters();render();
setTimeout(function(){
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){for(var i=0;i<20&&!converged;i++)stepOnce();render();return;}
  play();
},900);
})();
</script>
{% endraw %}
