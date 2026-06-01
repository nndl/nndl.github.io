---
layout: default
title: 自适应优化器 Adam
permalink: /viz/adam/
redirect_from:
  - /v/adam/
---

{% raw %}
<style>
.adlab .contour{fill:none;stroke:var(--color-border-strong);stroke-width:1;opacity:.5;}
.adlab .minmark{fill:var(--color-gold);stroke:#fff;stroke-width:1.5;}
.adlab .p-sgd{fill:none;stroke:#b5524a;stroke-width:2;opacity:.85;}
.adlab .p-mom{fill:none;stroke:var(--color-gold);stroke-width:2;opacity:.9;}
.adlab .p-adam{fill:none;stroke:var(--color-forest);stroke-width:2.4;}
.adlab .b-sgd{fill:#b5524a;stroke:#fff;stroke-width:1.5;}
.adlab .b-mom{fill:var(--color-gold);stroke:#fff;stroke-width:1.5;}
.adlab .b-adam{fill:var(--color-forest);stroke:#fff;stroke-width:1.5;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 自适应优化器 Adam

普通梯度下降对所有参数用同一个学习率，遇到“一个方向陡、一个方向缓”的损失面就很别扭——步子大了在陡方向上乱晃，步子小了在缓方向上磨蹭。Adam 的聪明在于**给每个参数配一个自适应的学习率**：某个方向梯度一直很大，就把它的步子调小；一直很小，就调大。于是它在峡谷里既不乱晃、又能顺着谷底快速前进。看 SGD、动量、Adam 三个球同场赛跑。

<section class="adlab vizui" id="adlab">
  <p class="vizui__lead">损失面是一条又窄又长的山谷（金点是谷底）。<span style="color:#b5524a;font-weight:600">红=SGD</span>、<span style="color:var(--color-gold);font-weight:600">黄=动量</span>、<span style="color:var(--color-forest);font-weight:600">绿=Adam</span>，从同一点出发。看谁先稳稳到底。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <button class="vizui-btn vizui-btn--go" id="go" type="button">▶ 开始</button>
      <button class="vizui-btn" id="reset" type="button">重置</button>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stat">第 0 步</span>
    </div>
    <svg class="vizui-chart" id="surf" viewBox="0 0 480 240" role="img" aria-label="三种优化器轨迹"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:#b5524a"><b>SGD：一刀切</b><p>所有方向同一个学习率，在陡的方向来回横跳，在缓的方向慢慢挪。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>动量：积累惯性</b><p>抵消横跳、顺着谷底加速，比 SGD 快，但学习率仍是固定的。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>Adam：每参数自适应</b><p>按各方向的历史梯度大小自动调步长——陡方向压住、缓方向放开，又快又稳，是当下最常用的优化器。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var A=1,B=40,START={x:-2.45,y:0.95};
var sgd,mom,adam,pS,pM,pA,step,playing=false,timer=null;
function grad(p){return {x:A*p.x,y:B*p.y};}
function dist(p){return Math.hypot(p.x,p.y);}
function init(){
  sgd={x:START.x,y:START.y};
  mom={x:START.x,y:START.y,vx:0,vy:0};
  adam={x:START.x,y:START.y,mx:0,my:0,vx:0,vy:0};
  pS=[{x:sgd.x,y:sgd.y}];pM=[{x:mom.x,y:mom.y}];pA=[{x:adam.x,y:adam.y}];step=0;
}
function stepAll(){
  var lr=0.035,beta=0.85;
  var gS=grad(sgd);sgd={x:sgd.x-lr*gS.x,y:sgd.y-lr*gS.y};pS.push({x:sgd.x,y:sgd.y});
  var gM=grad(mom);mom.vx=beta*mom.vx-lr*gM.x;mom.vy=beta*mom.vy-lr*gM.y;mom.x+=mom.vx;mom.y+=mom.vy;pM.push({x:mom.x,y:mom.y});
  // Adam
  var b1=0.9,b2=0.999,eps=1e-8,alr=0.12,gA=grad(adam);step++;
  adam.mx=b1*adam.mx+(1-b1)*gA.x;adam.my=b1*adam.my+(1-b1)*gA.y;
  adam.vx=b2*adam.vx+(1-b2)*gA.x*gA.x;adam.vy=b2*adam.vy+(1-b2)*gA.y*gA.y;
  var mhx=adam.mx/(1-Math.pow(b1,step)),mhy=adam.my/(1-Math.pow(b1,step));
  var vhx=adam.vx/(1-Math.pow(b2,step)),vhy=adam.vy/(1-Math.pow(b2,step));
  adam.x-=alr*mhx/(Math.sqrt(vhx)+eps);adam.y-=alr*mhy/(Math.sqrt(vhy)+eps);pA.push({x:adam.x,y:adam.y});
}
var SVGNS="http://www.w3.org/2000/svg",W=480,H=240,pad=18;
function wx(x){return pad+(x+3)/6*(W-2*pad);}
function wy(y){return pad+(1.2-y)/2.4*(H-2*pad);}
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function poly(svg,arr,cls){if(arr.length<2)return;E(svg,"polyline",{points:arr.map(function(p){return wx(p.x)+","+wy(p.y);}).join(" "),"class":cls,"clip-path":"url(#ac)"});}
function draw(){
  var svg=document.getElementById("surf");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var clip=E(svg,"clipPath",{id:"ac"});E(clip,"rect",{x:0,y:0,width:W,height:H});
  [0.06,0.18,0.4,0.8,1.5,2.6].forEach(function(c){E(svg,"ellipse",{cx:wx(0),cy:wy(0),rx:wx(Math.sqrt(2*c/A))-wx(0),ry:wy(0)-wy(Math.sqrt(2*c/B)),"class":"contour"});});
  var g=E(svg,"g",{"clip-path":"url(#ac)"});
  poly(g,pS,"p-sgd");poly(g,pM,"p-mom");poly(g,pA,"p-adam");
  E(svg,"circle",{cx:wx(0),cy:wy(0),r:5,"class":"minmark"});
  E(svg,"circle",{cx:wx(sgd.x),cy:wy(sgd.y),r:5,"class":"b-sgd"});
  E(svg,"circle",{cx:wx(mom.x),cy:wy(mom.y),r:5,"class":"b-mom"});
  E(svg,"circle",{cx:wx(adam.x),cy:wy(adam.y),r:5.5,"class":"b-adam"});
  document.getElementById("stat").textContent="第 "+step+" 步";
}
function render(){draw();caption();}
function caption(){
  var el=document.getElementById("caption"),dS=dist(sgd),dM=dist(mom),dA=dist(adam);
  if(step===0)el.innerHTML="点“开始”。注意红球（SGD）会在山谷两壁间横跳，绿球（Adam）能压住横跳、沿谷底直奔谷底。";
  else if(dA<0.05&&dS>0.2)el.innerHTML="第 "+step+" 步：<b>Adam（绿）已经到底</b>，SGD 还在半路横跳。自适应学习率让它在窄谷里又快又稳。";
  else el.innerHTML="第 "+step+" 步：离谷底——SGD "+dS.toFixed(2)+"、动量 "+dM.toFixed(2)+"、Adam "+dA.toFixed(2)+"。绿球几乎不横跳。";
}
function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("go").textContent="▶ 开始";}
function play(){if(dist(adam)<0.03&&dist(sgd)<0.05){init();render();}stop();playing=true;document.getElementById("go").textContent="⏸ 暂停";
  timer=setInterval(function(){stepAll();render();if((dist(adam)<0.02&&dist(sgd)<0.05)||step>=120)stop();},110);}
document.getElementById("go").addEventListener("click",function(){playing?stop():play();});
document.getElementById("reset").addEventListener("click",function(){stop();init();render();});
init();render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){for(var i=0;i<80;i++)stepAll();render();return;}play();},900);
})();
</script>
{% endraw %}
