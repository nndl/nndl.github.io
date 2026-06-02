---
layout: default
title: MCMC 采样
permalink: /viz/mcmc/
redirect_from:
  - /v/mcmc/
---

{% raw %}
<style>
.mcmclab .axis{stroke:var(--color-border);stroke-width:1;}
.mcmclab .field rect{shape-rendering:crispEdges;}
.mcmclab .samp{fill:var(--color-gold);}
.mcmclab .path{fill:none;stroke:var(--color-text);stroke-width:1;opacity:.35;}
.mcmclab .walker{fill:#b5524a;stroke:#fff;stroke-width:2;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# MCMC 采样

有时我们想从一个复杂分布里“抽样”（比如贝叶斯里的后验分布），但这个分布形状古怪、没法直接抽。MCMC（马尔可夫链蒙特卡洛）给了一个聪明的随机游走办法：从某个点出发，每步随机往旁边迈一小步——如果新位置概率更高就去，概率更低也按比例有机会去（这点很关键，让它不会卡在一个峰里）。走着走着，停留过的点就会**自动按目标分布的密度铺开**：高概率的地方点密、低概率的地方点疏。点“开始游走”，看金色样本怎么慢慢勾勒出背后的分布。

<section class="mcmclab vizui" id="mcmclab">
  <p class="vizui__lead">背景的青色浓淡是目标分布（越浓概率越高，这里有几个“山峰”）。红点是当前游走者，金点是它一路接受的样本。看金点怎么聚成和背景一样的形状。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <button class="vizui-btn vizui-btn--go" id="go" type="button">▶ 开始游走</button>
      <button class="vizui-btn" id="reset" type="button">重置</button>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stat">0 个样本</span>
    </div>
    <svg class="vizui-chart" id="plane" viewBox="0 0 320 320" style="max-width:380px;margin:0 auto" role="img" aria-label="MCMC 采样"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>随机游走</b><p>每步在附近随机提议一个新位置，不用知道分布的全貌，只要能比较两点的概率。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>概率高就多留</b><p>新点概率高就接受，低也按比例有机会接受——于是停留次数正比于概率密度。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>为什么有用</b><p>贝叶斯推断、复杂模型的后验大多没法直接算，MCMC 是从中采样的主力工具。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var XR=3, cur={x:-2,y:2}, samples=[], path=[], playing=false, timer=null;
function gpk(x,y,mx,my,s){var dx=x-mx,dy=y-my;return Math.exp(-(dx*dx+dy*dy)/(2*s*s));}
function target(x,y){return 0.65*gpk(x,y,-1,-0.6,0.62)+0.5*gpk(x,y,1.2,0.9,0.5)+0.18*gpk(x,y,0.4,-1.6,0.4);}
function randn(){var u=0,v=0;while(!u)u=Math.random();while(!v)v=Math.random();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}
function stepN(k){for(var i=0;i<k;i++){var nx=cur.x+randn()*0.45,ny=cur.y+randn()*0.45;
  var a=target(nx,ny)/(target(cur.x,cur.y)||1e-9);
  if(Math.random()<a){cur={x:Math.max(-XR,Math.min(XR,nx)),y:Math.max(-XR,Math.min(XR,ny))};}
  samples.push({x:cur.x,y:cur.y});path.push({x:cur.x,y:cur.y});if(path.length>30)path.shift();if(samples.length>1800)samples.shift();}}
var SVGNS="http://www.w3.org/2000/svg",W=320,H=320,pad=12,NG=26;
function wx(x){return pad+(x+XR)/(2*XR)*(W-2*pad);}
function wy(y){return (H-pad)-(y+XR)/(2*XR)*(H-2*pad);}
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function draw(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var fld=E(svg,"g",{"class":"field"}),cs=(W-2*pad)/NG,mx=0;
  var vals=[];for(var i=0;i<NG;i++){vals.push([]);for(var j=0;j<NG;j++){var x=-XR+2*XR*(i+0.5)/NG,y=-XR+2*XR*(j+0.5)/NG,v=target(x,y);vals[i].push(v);if(v>mx)mx=v;}}
  for(var i2=0;i2<NG;i2++)for(var j2=0;j2<NG;j2++){var x2=-XR+2*XR*(i2+0.5)/NG,y2=-XR+2*XR*(j2+0.5)/NG,t=vals[i2][j2]/mx;
    E(fld,"rect",{x:wx(x2)-cs/2,y:wy(y2)-cs/2,width:cs+0.6,height:cs+0.6,fill:"rgb("+Math.round(238-217*t)+","+Math.round(241-147*t)+","+Math.round(238-121*t)+")"});}
  samples.forEach(function(s){E(svg,"circle",{cx:wx(s.x),cy:wy(s.y),r:1.7,"class":"samp",opacity:0.5});});
  if(path.length>1)E(svg,"polyline",{points:path.map(function(p){return wx(p.x)+","+wy(p.y);}).join(" "),"class":"path"});
  E(svg,"circle",{cx:wx(cur.x),cy:wy(cur.y),r:6,"class":"walker"});
  document.getElementById("stat").textContent=samples.length+" 个样本";
}
function render(){draw();caption();}
function caption(){
  var el=document.getElementById("caption");
  if(samples.length<5)el.innerHTML="点“开始游走”。红点从角落出发随机迈步，往概率高的山峰走，金色样本会慢慢堆积。";
  else if(samples.length<300)el.innerHTML="走了 "+samples.length+" 步：金点开始往几个山峰聚拢，山谷里很稀疏——样本密度正在贴近目标分布。";
  else el.innerHTML="已有 "+samples.length+" 个样本：金点的分布几乎和背景的青色浓淡一模一样了。这堆样本就可以代替那个难算的分布拿去做统计——这就是 MCMC 的本事。";
}
function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("go").textContent="▶ 开始游走";}
function play(){stop();playing=true;document.getElementById("go").textContent="⏸ 暂停";timer=setInterval(function(){stepN(7);render();if(samples.length>=1800)stop();},60);}
document.getElementById("go").addEventListener("click",function(){playing?stop():play();});
document.getElementById("reset").addEventListener("click",function(){stop();cur={x:-2,y:2};samples=[];path=[];render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){stepN(900);render();return;}play();},1000);
})();
</script>
{% endraw %}
