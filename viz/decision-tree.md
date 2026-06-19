---
layout: default
title: 决策树与信息增益
permalink: /viz/decision-tree/
redirect_from:
  - /v/decision-tree/
---

{% raw %}
<style>
.dtlab .axis{stroke:var(--color-border-strong);stroke-width:1;}
.dtlab .split{stroke:var(--color-text);stroke-width:2;}
.dtlab .pt{stroke:#fff;stroke-width:1.3;}
.dtlab .pt.c1{fill:var(--color-accent-light);}
.dtlab .pt.c0{fill:#b5524a;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 决策树与信息增益

决策树用一连串“是非问题”做判断：先问“某个特征是否大于某个值”，把数据切成两半，再在每半里继续问，直到每块里基本只剩一类。问题是——每一步该挑哪个特征、切在哪儿？答案是**让混乱程度（熵）下降得最多**的那一刀，下降的量就叫“信息增益”。拖动深度，看它一刀刀把平面切成越来越“纯”的区域。

<section class="dtlab vizui" id="dtlab">
  <p class="vizui__lead">蓝点、红点是两类数据。每加一层深度，决策树就在每个区域里选信息增益最大的一刀（横切或竖切）。背景按该区域的多数类着色——切得越深，每块越“纯”。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="depth">树的深度</label><input type="range" id="depth" min="0" max="5" step="1" value="0" style="width:170px"><output id="depthVal">0</output></span>
      <span class="vizui-spacer"></span>
      <button class="vizui-btn vizui-btn--go" id="auto" type="button">▶ 逐层生长</button>
      <span class="vizui-pill" id="info">—</span>
    </div>
    <svg class="vizui-chart" id="plane" viewBox="0 0 320 320" style="max-width:380px;margin:0 auto" role="img" aria-label="决策树切分"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>熵 = 混乱度</b><p>一块区域里两类各占一半时最“乱”（熵最大）；只剩一类时最“纯”（熵为 0）。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>信息增益 = 选刀准则</b><p>切一刀后熵下降多少，就是这刀的信息增益；每步都选增益最大的那刀。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>越切越纯</b><p>不停切分直到每块基本同类；切太深会把噪声也学进去（过拟合），需要剪枝。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var XR=2.5, maxDepth=0, pts=[], playing=false, timer=null;
function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
function gauss(r){var u=0,v=0;while(!u)u=r();while(!v)v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}
(function(){var r=rng(8),C=[[-1.5,-0.2,1],[-0.3,1.3,0],[0.6,-1.3,1],[1.6,0.4,0]];
  C.forEach(function(c){for(var i=0;i<7;i++)pts.push({x:c[0]+gauss(r)*0.4,y:c[1]+gauss(r)*0.4,t:c[2]});});})();
function entropy(P){if(!P.length)return 0;var n1=0;P.forEach(function(p){n1+=p.t;});var p1=n1/P.length,p0=1-p1;
  function h(p){return p<=0?0:-p*Math.log2(p);}return h(p0)+h(p1);}
function majority(P){var n1=0;P.forEach(function(p){n1+=p.t;});return n1>=P.length/2?1:0;}
function bestSplit(P){
  var best=null,H=entropy(P),n=P.length;
  [0,1].forEach(function(ax){
    var key=ax===0?"x":"y",vals=P.map(function(p){return p[key];}).sort(function(a,b){return a-b;});
    for(var i=0;i<vals.length-1;i++){if(vals[i]===vals[i+1])continue;var th=(vals[i]+vals[i+1])/2;
      var L=P.filter(function(p){return p[key]<th;}),R=P.filter(function(p){return p[key]>=th;});
      if(!L.length||!R.length)continue;
      var gain=H-(L.length/n*entropy(L)+R.length/n*entropy(R));
      if(!best||gain>best.gain){best={ax:ax,key:key,th:th,gain:gain,L:L,R:R};}}
  });
  return best;
}
function build(P,reg,depth){
  if(depth>=maxDepth||P.length<3||entropy(P)<0.01)return {leaf:true,cls:majority(P),reg:reg,n:P.length};
  var s=bestSplit(P);if(!s||s.gain<0.001)return {leaf:true,cls:majority(P),reg:reg,n:P.length};
  var rL=Object.assign({},reg),rR=Object.assign({},reg);
  if(s.ax===0){rL.x1=s.th;rR.x0=s.th;}else{rL.y1=s.th;rR.y0=s.th;}
  return {leaf:false,s:s,reg:reg,left:build(s.L,rL,depth+1),right:build(s.R,rR,depth+1)};
}
function leaves(node,acc){if(node.leaf)acc.push(node);else{leaves(node.left,acc);leaves(node.right,acc);}return acc;}
function splits(node,acc){if(!node.leaf){acc.push(node);splits(node.left,acc);splits(node.right,acc);}return acc;}

var SVGNS="http://www.w3.org/2000/svg",W=320,H=320,pad=14;
function wx(x){return pad+(x+XR)/(2*XR)*(W-2*pad);}
function wy(y){return (H-pad)-(y+XR)/(2*XR)*(H-2*pad);}
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function render(){
  document.getElementById("depthVal").textContent=maxDepth;
  var tree=build(pts,{x0:-XR,y0:-XR,x1:XR,y1:XR},0);
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  leaves(tree,[]).forEach(function(lf){var r=lf.reg;
    E(svg,"rect",{x:wx(r.x0),y:wy(r.y1),width:wx(r.x1)-wx(r.x0),height:wy(r.y0)-wy(r.y1),fill:lf.cls?"rgba(37,99,235,.12)":"rgba(181,82,74,.12)"});});
  splits(tree,[]).forEach(function(nd){var s=nd.s,r=nd.reg;
    if(s.ax===0)E(svg,"line",{x1:wx(s.th),y1:wy(r.y0),x2:wx(s.th),y2:wy(r.y1),"class":"split"});
    else E(svg,"line",{x1:wx(r.x0),y1:wy(s.th),x2:wx(r.x1),y2:wy(s.th),"class":"split"});});
  pts.forEach(function(p){E(svg,"circle",{cx:wx(p.x),cy:wy(p.y),r:5.5,"class":"pt "+(p.t?"c1":"c0")});});
  var lv=leaves(tree,[]),err=0;
  // 训练误差
  function predict(node,p){if(node.leaf)return node.cls;var s=node.s;return (p[s.key]<s.th?predict(node.left,p):predict(node.right,p));}
  pts.forEach(function(p){if(predict(tree,p)!==p.t)err++;});
  document.getElementById("info").textContent=lv.length+" 个区域 · 分错 "+err+"/"+pts.length;
  caption(tree,err,lv.length);
}
function caption(tree,err,nleaf){
  var el=document.getElementById("caption");
  if(maxDepth===0)el.innerHTML="深度 0：还没切，整个平面是一块，蓝红混在一起、最“乱”（熵最大）。往右拖增加深度。";
  else if(err>0)el.innerHTML="深度 "+maxDepth+"："+nleaf+" 个区域，还分错 "+err+" 个。一刀还不够——每切一刀都隔出一簇较纯的点，剩下的继续切。继续加深。";
  else el.innerHTML="深度 "+maxDepth+"："+nleaf+" 个区域，<b>全分对了</b>。树用几条横竖切线把四簇点逐一隔开——每刀都选了信息增益最大的方向。再切更深就是在抠噪声了（过拟合）。";
}
function setD(v){maxDepth=Math.max(0,Math.min(5,v));document.getElementById("depth").value=maxDepth;render();}
document.getElementById("depth").addEventListener("input",function(e){stop();setD(+e.target.value);});
function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("auto").textContent="▶ 逐层生长";}
document.getElementById("auto").addEventListener("click",function(){if(playing){stop();return;}playing=true;document.getElementById("auto").textContent="⏸ 暂停";var d=0;setD(0);timer=setInterval(function(){d++;if(d>5){stop();return;}setD(d);},850);});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){setD(4);return;}document.getElementById("auto").click();},1000);
})();
</script>
{% endraw %}
