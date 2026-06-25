---
layout: default
title: 逻辑回归
description: "两类点 + sigmoid 概率渐变背景，训练看决策边界和交叉熵损失怎么一步步学出来。"
permalink: /viz/logistic-regression/
redirect_from:
  - /v/logistic-regression/
---

{% raw %}
<style>
.lrlab .axis{stroke:var(--color-border);stroke-width:1;}
.lrlab .bound{stroke:var(--color-text);stroke-width:2.4;}
.lrlab .pt{stroke:#fff;stroke-width:1.5;}
.lrlab .pt.p1{fill:#2563eb;}
.lrlab .pt.p0{fill:#b5524a;}
.lrlab .field rect{shape-rendering:crispEdges;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 逻辑回归

感知器只会回答“是/否”，逻辑回归更进一步：它输出一个**概率**。办法是把“到分界线的距离”塞进一个 S 形的 sigmoid 函数，离边界越远、越确定（概率趋近 1 或 0），边界处则是模糊的 50%。训练的目标是让交叉熵损失最小——也就是让模型对每个点给出的概率，尽量贴近它真实的标签。点“训练”，看分界线和背后的概率渐变怎么一步步学出来。

<section class="vizui lrlab" id="lrlab">
  <p class="vizui__lead">背景颜色是模型预测的概率：<span style="color:#2563eb;font-weight:600">越蓝→越可能是蓝类</span>，<span style="color:#b5524a;font-weight:600">越红→越可能是红类</span>，中间白带是 50% 的决策边界。点的颜色是它的真实类别。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <button class="vizui-btn vizui-btn--go" id="train" type="button">▶ 自动训练</button>
      <button class="vizui-btn" id="step" type="button">训练一步</button>
      <button class="vizui-btn" id="reset" type="button">重置</button>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stat">损失 — · 正确率 —</span>
    </div>
  </div>

  <div class="vizui-panel">
    <div class="vizui-bar" style="justify-content:center">
      <svg class="vizui-chart" id="plane" viewBox="0 0 320 320" style="max-width:380px;margin:0 auto" role="img" aria-label="逻辑回归决策面"></svg>
    </div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>输出是概率</b><p>sigmoid 把任意分数压到 0~1，可以当作“属于蓝类的概率”，而不只是硬邦邦的是/否。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>交叉熵损失</b><p>预测概率离真实标签越远，惩罚越大；训练就是把这个损失降下去。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>线性边界</b><p>决策边界（概率 0.5 处）是一条直线；它是神经网络里一个带 sigmoid 的神经元。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var XR=3, w=[0.1,-0.1], b=0, lr=0.5, pts=[], playing=false, timer=null;
function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
function gauss(r){var u=0,v=0;while(!u)u=r();while(!v)v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}
function gen(){var r=rng(5);pts=[];
  for(var i=0;i<13;i++)pts.push({x:1.1+gauss(r)*0.72,y:1.0+gauss(r)*0.72,t:1});
  for(var j=0;j<13;j++)pts.push({x:-1.05+gauss(r)*0.72,y:-0.95+gauss(r)*0.72,t:0});}
function sig(z){return 1/(1+Math.exp(-z));}
function prob(x,y){return sig(w[0]*x+w[1]*y+b);}
function trainStep(){
  var g0=0,g1=0,gb=0;
  pts.forEach(function(p){var pr=prob(p.x,p.y),d=pr-p.t;g0+=d*p.x;g1+=d*p.y;gb+=d;});
  var n=pts.length;w[0]-=lr*g0/n;w[1]-=lr*g1/n;b-=lr*gb/n;
}
function stats(){var loss=0,corr=0;pts.forEach(function(p){var pr=Math.max(1e-6,Math.min(1-1e-6,prob(p.x,p.y)));loss+=-(p.t*Math.log(pr)+(1-p.t)*Math.log(1-pr));if((pr>=0.5?1:0)===p.t)corr++;});return {loss:loss/pts.length,acc:corr/pts.length};}

var SVGNS="http://www.w3.org/2000/svg",W=320,H=320,pad=14,NG=20;
function wx(x){return pad+(x+XR)/(2*XR)*(W-2*pad);}
function wy(y){return (H-pad)-(y+XR)/(2*XR)*(H-2*pad);}
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function pcol(p){
  if(p>=0.5){var t=(p-0.5)*2;return "rgb("+Math.round(237-200*t)+","+Math.round(240-141*t)+",247)";}
  var u=(0.5-p)*2;return "rgb(247,"+Math.round(240-110*u)+","+Math.round(240-110*u)+")";
}
function draw(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var fld=E(svg,"g",{"class":"field"}),cs=(W-2*pad)/NG;
  for(var i=0;i<NG;i++)for(var j=0;j<NG;j++){var x=-XR+2*XR*(i+0.5)/NG,y=-XR+2*XR*(j+0.5)/NG;
    E(fld,"rect",{x:wx(x)-cs/2,y:wy(y)-cs/2,width:cs+0.6,height:cs+0.6,fill:pcol(prob(x,y))});}
  // 决策边界 w0 x + w1 y + b=0
  if(Math.abs(w[1])>1e-4){var y1=-(w[0]*(-XR)+b)/w[1],y2=-(w[0]*XR+b)/w[1];E(svg,"line",{x1:wx(-XR),y1:wy(y1),x2:wx(XR),y2:wy(y2),"class":"bound"});}
  else if(Math.abs(w[0])>1e-4){var xx=-b/w[0];E(svg,"line",{x1:wx(xx),y1:pad,x2:wx(xx),y2:H-pad,"class":"bound"});}
  pts.forEach(function(p){E(svg,"circle",{cx:wx(p.x),cy:wy(p.y),r:6,"class":"pt "+(p.t?"p1":"p0")});});
}
function render(){var s=stats();document.getElementById("stat").textContent="损失 "+s.loss.toFixed(3)+" · 正确率 "+(s.acc*100).toFixed(0)+"%";draw();caption(s);}
function caption(s){document.getElementById("caption").innerHTML=s.loss>0.5?
  "还没训好：分界线没对齐，背景概率也很模糊，损失 "+s.loss.toFixed(2)+"。继续训练，看它怎么转到位。":
  "训好了：分界线把两类分开，离边界越远背景越纯（越确定），损失降到 "+s.loss.toFixed(2)+"、正确率 "+(s.acc*100).toFixed(0)+"%。靠近边界的点概率接近 50%，模型对它们没把握。";}
function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("train").textContent="▶ 自动训练";}
function play(){stop();playing=true;document.getElementById("train").textContent="⏸ 暂停";var n=0;timer=setInterval(function(){trainStep();n++;render();if(n>=60||stats().loss<0.18)stop();},120);}
document.getElementById("train").addEventListener("click",function(){playing?stop():play();});
document.getElementById("step").addEventListener("click",function(){stop();trainStep();render();});
document.getElementById("reset").addEventListener("click",function(){stop();w=[0.1,-0.1];b=0;render();});
gen();render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){for(var i=0;i<60;i++)trainStep();render();return;}play();},900);
})();
</script>
{% endraw %}
