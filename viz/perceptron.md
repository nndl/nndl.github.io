---
layout: default
title: 感知器画线
permalink: /viz/perceptron/
redirect_from:
  - /v/perceptron/
---

{% raw %}
<style>
.pclab .axis{stroke:var(--color-border);stroke-width:1;}
.pclab .pt{stroke:#fff;stroke-width:1.5;cursor:default;}
.pclab .pt.pos{fill:var(--color-accent-light);}
.pclab .pt.neg{fill:#b5524a;}
.pclab .pt.check{stroke:var(--color-gold);stroke-width:3;}
.pclab .pt.wrong{stroke:var(--color-gold);stroke-width:3;stroke-dasharray:3 2;}
.pclab .decline{stroke:var(--color-text);stroke-width:2.5;}
.pclab .region-pos{fill:var(--color-accent-light);opacity:.06;}
.pclab .region-neg{fill:#b5524a;opacity:.06;}
.pclab svg{cursor:crosshair;touch-action:none;}
.pclab .pen{display:inline-flex;gap:4px;padding:4px;background:var(--color-bg-section);border:1px solid var(--color-border);border-radius:999px;}
.pclab .pen button{appearance:none;border:0;background:transparent;cursor:pointer;font:inherit;font-size:.85rem;color:var(--color-text-soft);padding:6px 12px;border-radius:999px;}
.pclab .pen button.on{background:var(--color-bg-pure);font-weight:600;box-shadow:var(--shadow-sm);}
.pclab .pen button[data-c="1"].on{color:var(--color-accent-light);}
.pclab .pen button[data-c="-1"].on{color:#b5524a;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 感知器画线

最早的神经元模型“感知器”要做一件简单的事：在平面上画一条线，把两类点分开。它怎么学会这条线的？办法很笨却很有效——每看到一个被分错的点，就把线朝着“纠正它”的方向挪一点，反复多遍，直到一个都不分错。看它自己把线转到位。

<section class="vizui pclab" id="pclab">
  <p class="vizui__lead">蓝点和红点是两类数据，黑线是感知器当前画的分界线。带金圈的是它正在检查的点；只要还有分错的，它就继续调整这条线。你也可以选支笔，<b>在图上点几下加自己的点</b>。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <button class="vizui-btn vizui-btn--go" id="go" type="button">▶ 开始学习</button>
      <button class="vizui-btn" id="step" type="button">单步</button>
      <button class="vizui-btn" id="reset" type="button">重置线</button>
      <button class="vizui-btn" id="regen" type="button">↻ 换一批点</button>
      <span class="vizui-spacer"></span>
      <span class="pen" id="pen"><button data-c="1" class="on" type="button">● 蓝点笔</button><button data-c="-1" type="button">● 红点笔</button></span>
    </div>
  </div>

  <div class="vizui-panel">
    <div class="vizui-bar" style="justify-content:center">
      <svg class="vizui-chart" id="plane" viewBox="0 0 360 300" style="max-width:420px;margin:0 auto" role="img" aria-label="感知器分类平面"></svg>
    </div>
    <div style="text-align:center;margin-top:6px"><span id="status" class="vizui-pill">第 0 轮 · 分错 0 个</span></div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>看一个点</b><p>感知器逐个检查数据点：分对了就跳过，分错了就动手调整。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>纠正一点点</b><p>把分界线朝着“让这个点回到正确一侧”的方向挪一小步——这就是“学习”。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>反复直到分开</b><p>只要两类点本来能用一条直线分开，这个笨办法保证最终一个都不分错。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var XR=2.3, lr=0.3, pen=1;
var pts=[], w=[0,0], b=0, idx=0, pass=0, checking=-1, wrong=-1, seed=5, playing=false, timer=null, solved=false, sinceFix=0;

function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
function gauss(r){var u=0,v=0;while(!u)u=r();while(!v)v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}
function genPts(){
  var r=rng(seed); pts=[];
  for(var i=0;i<8;i++)pts.push({x:1.05+gauss(r)*0.42,y:0.85+gauss(r)*0.42,c:1});
  for(var j=0;j<8;j++)pts.push({x:-1.0+gauss(r)*0.42,y:-0.8+gauss(r)*0.42,c:-1});
}
function resetLine(){w=[0,0];b=0;idx=0;pass=0;checking=-1;wrong=-1;solved=false;sinceFix=0;}
function pred(p){return w[0]*p.x+w[1]*p.y+b;}

function stepOnce(){
  if(solved||pts.length===0)return;
  var p=pts[idx]; checking=idx; wrong=-1;
  if(p.c*pred(p)<=0){ w[0]+=lr*p.c*p.x; w[1]+=lr*p.c*p.y; b+=lr*p.c; wrong=idx; sinceFix=0; }
  else { sinceFix++; }
  idx=(idx+1)%pts.length;
  if(idx===0)pass++;
  if(sinceFix>=pts.length)solved=true;     /* 完整一轮无错 → 收敛 */
}
function errCount(){var n=0;for(var i=0;i<pts.length;i++)if(pts[i].c*pred(pts[i])<=0)n++;return n;}

var SVGNS="http://www.w3.org/2000/svg", W=360,H=300,pad=14;
function wx(x){return pad+(x+XR)/(2*XR)*(W-2*pad);}
function wy(y){return (H-pad)-(y+XR)/(2*XR)*(H-2*pad);}
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}

function draw(){
  var svg=document.getElementById("plane"); while(svg.firstChild)svg.removeChild(svg.firstChild);
  E(svg,"line",{x1:wx(0),y1:pad,x2:wx(0),y2:H-pad,"class":"axis"});
  E(svg,"line",{x1:pad,y1:wy(0),x2:W-pad,y2:wy(0),"class":"axis"});
  // 分界线（与边框求交点连线）
  if(w[0]!==0||w[1]!==0){
    var segs=[];
    function atX(x){if(w[1]===0)return null;var y=-(w[0]*x+b)/w[1];return (y>=-XR&&y<=XR)?{x:x,y:y}:null;}
    function atY(y){if(w[0]===0)return null;var x=-(w[1]*y+b)/w[0];return (x>=-XR&&x<=XR)?{x:x,y:y}:null;}
    [atX(-XR),atX(XR),atY(-XR),atY(XR)].forEach(function(q){if(q)segs.push(q);});
    if(segs.length>=2)E(svg,"line",{x1:wx(segs[0].x),y1:wy(segs[0].y),x2:wx(segs[1].x),y2:wy(segs[1].y),"class":"decline"});
  }
  pts.forEach(function(p,i){
    var cls="pt "+(p.c>0?"pos":"neg")+(i===checking?(i===wrong?" wrong":" check"):"");
    E(svg,"circle",{cx:wx(p.x),cy:wy(p.y),r:6.5,"class":cls});
  });
  document.getElementById("status").textContent="第 "+pass+" 轮 · 当前分错 "+errCount()+" 个";
}
function caption(){
  var el=document.getElementById("caption"), e=errCount();
  if(solved||(e===0&&(w[0]||w[1]))){el.innerHTML="<b>分开了！</b>感知器找到一条线，把两类点完全分到两边，一个都不错。只要数据本来线性可分，这个笨办法一定能成功。";return;}
  if(pass===0&&checking<0){el.innerHTML="点“开始学习”。感知器会逐个检查点，发现分错的就把线挪一下。";return;}
  if(wrong>=0){el.innerHTML="发现一个<b>分错的点</b>（金色虚圈），把分界线朝着纠正它的方向挪了一步。当前还有 "+e+" 个分错。";return;}
  el.innerHTML="这个点分对了，跳过。还剩 "+e+" 个分错的点要处理。";
}
function render(){draw();caption();}

function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("go").textContent="▶ 开始学习";}
function play(){if(solved)resetLine();stop();playing=true;document.getElementById("go").textContent="⏸ 暂停";
  timer=setInterval(function(){stepOnce();render();if(solved)stop();},420);}
document.getElementById("go").addEventListener("click",function(){playing?stop():play();});
document.getElementById("step").addEventListener("click",function(){stop();stepOnce();render();});
document.getElementById("reset").addEventListener("click",function(){stop();resetLine();render();});
document.getElementById("regen").addEventListener("click",function(){stop();seed++;genPts();resetLine();render();});
document.getElementById("pen").addEventListener("click",function(e){var b2=e.target.closest("button");if(!b2)return;pen=+b2.dataset.c;
  document.querySelectorAll("#pen button").forEach(function(x){x.classList.toggle("on",+x.dataset.c===pen);});});
document.getElementById("plane").addEventListener("click",function(e){
  stop();var r=e.currentTarget.getBoundingClientRect();
  var sx=(e.clientX-r.left)/r.width*W, sy=(e.clientY-r.top)/r.height*H;
  var x=(sx-pad)/(W-2*pad)*(2*XR)-XR;                  /* 屏幕→世界坐标 */
  var y=((H-pad-sy)/(H-2*pad))*(2*XR)-XR;
  if(x>-XR&&x<XR&&y>-XR&&y<XR){pts.push({x:x,y:y,c:pen});resetLine();render();}
});

/* 启动 + 自动演示 */
genPts();resetLine();render();
setTimeout(function(){
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){for(var i=0;i<80&&!solved;i++)stepOnce();render();return;}
  play();
},900);
})();
</script>
{% endraw %}
