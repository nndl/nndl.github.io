---
layout: default
title: 反向传播
permalink: /viz/backprop/
redirect_from:
  - /v/backprop/
---

{% raw %}
<style>
.bplab .edge{stroke:var(--color-border-strong);stroke-width:1.6;fill:none;}
.bplab .edge.back{stroke:var(--color-gold);stroke-width:2.4;}
.bplab .nbox{stroke:var(--color-border-strong);stroke-width:1.2;}
.bplab .nbox.param{fill:#e8f1ec;}
.bplab .nbox.op{fill:var(--color-bg-pure);}
.bplab .nbox.inp{fill:var(--color-bg-section);}
.bplab .nbox.loss{fill:#fdeceb;stroke:#b5524a;}
.bplab .nname{font:600 12px var(--font-mono);fill:var(--color-text);}
.bplab .nval{font:600 12px var(--font-mono);fill:var(--color-accent);}
.bplab .ngrad{font:600 11px var(--font-mono);fill:var(--color-gold);}
.bplab .losschart .ll{fill:none;stroke:#b5524a;stroke-width:2;}
.bplab .losschart .axis{stroke:var(--color-border);stroke-width:1;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 反向传播

神经网络是怎么``学''的？先正向算一遍，得到一个误差（loss）；再反着走一遍，把这个误差顺着计算图一层层传回去，算出``每个权重该往哪个方向调、调多少''——这就是反向传播，深度学习的引擎。它的全部秘密就是高中学过的链式法则。下面这个只有几个节点的迷你网络，让你一步步看清楚。

<section class="vizui bplab" id="bplab">
  <p class="vizui__lead">绿框是要学的参数（w₁ w₂ b），蓝色数字是<b>正向</b>算出的值，金色数字是<b>反向</b>传回的梯度。目标是让输出 a 逼近 1。点``训练一步''反复看 loss 怎么降下来。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <button class="vizui-btn" id="fwd" type="button">① 正向传播</button>
      <button class="vizui-btn" id="bwd" type="button">② 反向传播</button>
      <button class="vizui-btn vizui-btn--go" id="train" type="button">训练一步 ▶</button>
      <button class="vizui-btn" id="reset" type="button">重置</button>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="lossLbl">loss —</span>
    </div>
  </div>

  <div class="vizui-grid2">
    <div class="vizui-panel">
      <p class="vizui-panel__title">计算图</p>
      <svg class="vizui-chart" id="graph" viewBox="0 0 520 280" role="img" aria-label="计算图与梯度"></svg>
    </div>
    <div class="vizui-panel">
      <p class="vizui-panel__title">loss 随训练下降</p>
      <svg class="vizui-chart losschart" id="loss" viewBox="0 0 300 200" role="img" aria-label="loss 曲线"></svg>
      <div id="explain" style="font-size:.86rem;color:var(--color-text-soft);line-height:1.6;margin-top:6px"></div>
    </div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>正向：算误差</b><p>输入沿计算图往前算，一路到输出 a 和误差 loss。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>反向：链式法则</b><p>从 loss 出发往回走，每个节点把``上游梯度''乘以``本地导数'',就得到自己的梯度。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>更新：沿梯度下降</b><p>每个权重朝梯度的反方向挪一小步，loss 就会下降一点；反复多步即``训练''。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var x1=1.0, x2=-1.0, target=1.0, lr=0.5;
var w1=0.6, w2=0.9, b=-0.2;
var mode="init", hist=[];
function sig(z){return 1/(1+Math.exp(-z));}
var N={
  x1:{x:46,y:40,nm:"x₁",cls:"inp"}, w1:{x:46,y:88,nm:"w₁",cls:"param"},
  x2:{x:46,y:200,nm:"x₂",cls:"inp"}, w2:{x:46,y:248,nm:"w₂",cls:"param"},
  b:{x:46,y:144,nm:"b",cls:"param"},
  m1:{x:180,y:64,nm:"×",cls:"op"}, m2:{x:180,y:224,nm:"×",cls:"op"},
  z:{x:300,y:144,nm:"+",cls:"op"}, a:{x:386,y:144,nm:"σ",cls:"op"}, loss:{x:470,y:144,nm:"loss",cls:"loss"}
};
var EDGES=[["x1","m1"],["w1","m1"],["x2","m2"],["w2","m2"],["m1","z"],["m2","z"],["b","z"],["z","a"],["a","loss"]];
function forward(){
  N.x1.v=x1;N.x2.v=x2;N.w1.v=w1;N.w2.v=w2;N.b.v=b;
  N.m1.v=w1*x1;N.m2.v=w2*x2;N.z.v=N.m1.v+N.m2.v+b;N.a.v=sig(N.z.v);N.loss.v=(N.a.v-target)*(N.a.v-target);
}
function backward(){
  N.loss.g=1; N.a.g=2*(N.a.v-target); N.z.g=N.a.g*N.a.v*(1-N.a.v);
  N.m1.g=N.z.g;N.m2.g=N.z.g;N.b.g=N.z.g; N.w1.g=N.m1.g*x1;N.w2.g=N.m2.g*x2; N.x1.g=N.m1.g*w1;N.x2.g=N.m2.g*w2;
}
function update(){w1-=lr*N.w1.g;w2-=lr*N.w2.g;b-=lr*N.b.g;}

var SVGNS="http://www.w3.org/2000/svg";
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function drawGraph(){
  var svg=document.getElementById("graph");while(svg.firstChild)svg.removeChild(svg.firstChild);
  EDGES.forEach(function(ed){var A=N[ed[0]],B=N[ed[1]];E(svg,"path",{d:"M"+(A.x+30)+","+A.y+" C"+(A.x+70)+","+A.y+" "+(B.x-40)+","+B.y+" "+(B.x-30)+","+B.y,"class":"edge"+(mode==="backward"?" back":"")});});
  Object.keys(N).forEach(function(k){var n=N[k];
    E(svg,"rect",{x:n.x-30,y:n.y-18,width:60,height:36,rx:8,"class":"nbox "+n.cls});
    E(svg,"text",{x:n.x,y:n.y-3,"text-anchor":"middle","class":"nname"}).textContent=n.nm;
    if(mode!=="init"&&n.v!==undefined)E(svg,"text",{x:n.x,y:n.y+11,"text-anchor":"middle","class":"nval"}).textContent=(Math.round(n.v*100)/100);
    if(mode==="backward"&&n.g!==undefined)E(svg,"text",{x:n.x,y:n.y+27,"text-anchor":"middle","class":"ngrad"}).textContent="∇"+(Math.round(n.g*100)/100);
  });
}
function drawLoss(){
  var svg=document.getElementById("loss");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var W=300,H=200,pad=26;
  E(svg,"line",{x1:pad,y1:H-pad,x2:W-10,y2:H-pad,"class":"axis"});
  E(svg,"line",{x1:pad,y1:10,x2:pad,y2:H-pad,"class":"axis"});
  if(hist.length){var mx=Math.max.apply(null,hist),n=Math.max(hist.length,8);
    var pts=hist.map(function(L,i){return (pad+i/(n-1)*(W-pad-10))+","+((H-pad)-L/(mx||1)*(H-pad-12));});
    E(svg,"polyline",{points:pts.join(" "),"class":"ll"});
    hist.forEach(function(L,i){E(svg,"circle",{cx:pad+i/(n-1)*(W-pad-10),cy:(H-pad)-L/(mx||1)*(H-pad-12),r:2.5,fill:"#b5524a"});});}
  E(svg,"text",{x:pad-4,y:16,"text-anchor":"end","class":"nval",style:"fill:var(--color-text-muted)"}).textContent="";
}
function explain(){
  var el=document.getElementById("explain");
  if(mode==="init"){el.innerHTML="先点``正向传播''算出 loss。";return;}
  if(mode==="forward"){el.innerHTML="正向算完：输出 a = <b>"+N.a.v.toFixed(2)+"</b>，离目标 1 还差一截，loss = <b>"+N.loss.v.toFixed(3)+"</b>。";return;}
  el.innerHTML="反向传播（链式法则）：<br>∇a = 2(a−1) = "+N.a.g.toFixed(2)+"<br>∇z = ∇a × a(1−a) = "+N.z.g.toFixed(3)+"<br>∇w₁ = ∇z × x₁ = <b>"+N.w1.g.toFixed(3)+"</b>　∇w₂ = ∇z × x₂ = <b>"+N.w2.g.toFixed(3)+"</b><br>每个权重就照这个梯度往反方向挪一步。";
}
function caption(){
  var el=document.getElementById("caption");
  if(mode==="init")el.innerHTML="这个迷你网络：z = w₁x₁ + w₂x₂ + b，再过 σ 得到输出 a，目标让 a→1。先正向、再反向，看梯度怎么算出来。";
  else if(mode==="forward")el.innerHTML="<b>正向传播完成。</b>蓝色是各节点的值。现在点``反向传播'',看误差怎样顺着金色路径传回每个参数。";
  else el.innerHTML="<b>反向传播完成。</b>金色 ∇ 是每个节点的梯度——注意它是从右边的 loss 一路乘回来的（链式法则）。点``训练一步''让参数按梯度更新、loss 下降。";
  document.getElementById("lossLbl").textContent="loss "+(N.loss.v!==undefined?N.loss.v.toFixed(3):"—");
}
function render(){drawGraph();drawLoss();explain();caption();}

document.getElementById("fwd").addEventListener("click",function(){forward();mode="forward";render();});
document.getElementById("bwd").addEventListener("click",function(){forward();backward();mode="backward";render();});
document.getElementById("train").addEventListener("click",function(){forward();backward();hist.push(N.loss.v);update();forward();mode="backward";render();});
document.getElementById("reset").addEventListener("click",function(){w1=0.6;w2=0.9;b=-0.2;hist=[];mode="init";forward();render();});

forward();render();
setTimeout(function(){
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){for(var i=0;i<20;i++){forward();backward();hist.push(N.loss.v);update();}forward();mode="backward";render();return;}
  var steps=["fwd","bwd","train","train","train","train","train","train"],k=0;
  var iv=setInterval(function(){if(k>=steps.length){clearInterval(iv);return;}document.getElementById(steps[k]).click();k++;},850);
},1000);
})();
</script>
{% endraw %}
