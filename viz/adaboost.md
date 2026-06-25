---
layout: default
title: AdaBoost 提升法
description: "弱分类器一根接一根：每轮放大上轮分错的样本、最后加权投票，看一串横竖刀拼出贴合斜线的“楼梯”。"
permalink: /viz/adaboost/
redirect_from:
  - /v/adaboost/
---

{% raw %}
<style>
.ablab .axis{stroke:var(--color-border-strong);stroke-width:1;}
.ablab .stump{stroke:var(--color-text);stroke-width:2;stroke-dasharray:6 4;}
.ablab .pt{stroke:#fff;stroke-width:1.3;}
.ablab .pt.c1{fill:var(--color-accent-light);}
.ablab .pt.c0{fill:#b5524a;}
.ablab .wrong{fill:none;stroke:var(--color-text);stroke-width:2.4;}
.ablab .glbl{font:11px var(--font-mono);fill:var(--color-text-muted);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# AdaBoost：串起一堆弱分类器

一条横平竖直的线（一个“树桩”弱分类器）只比瞎猜强一点点。**AdaBoost** 的想法是把许多这样的弱分类器**串起来纠错**：每加一个，就盯住上一轮被分错的样本、加大它们的权重，逼下一个分类器专攻这些难点；最后让所有弱分类器**加权投票**——投得准的票更重。和并联取平均的 [Bagging](/viz/bagging/) 不同，AdaBoost 是一根接一根、越接越准。这里要分的两类被一条斜线隔开，而每个弱分类器只能横切或竖切；看 AdaBoost 怎样用一串横竖刀拼出一道贴合斜线的“楼梯”。

<section class="vizui ablab" id="ablab">
  <p class="vizui__lead">蓝点（左下）、红点（右上）被一条斜线分开。每一步加一个弱分类器（虚线，只能横/竖切）。<b>点越大＝当前权重越高</b>（越受重视），<span style="color:var(--color-text)">深色圈</span>＝当前还被分错。背景是“加权投票”后的判定区域——看它怎样一步步贴近真实边界。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <button class="vizui-btn vizui-btn--go" id="step" type="button">▶ 加一个弱分类器</button>
      <button class="vizui-btn" id="auto" type="button">自动</button>
      <button class="vizui-btn" id="reset" type="button">重置</button>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stat">—</span>
    </div>
    <svg class="vizui-chart" id="plane" viewBox="0 0 320 320" style="max-width:380px;margin:0 auto" role="img" aria-label="AdaBoost 提升"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>串联纠错</b><p>每加一个弱分类器，就放大上一轮被分错样本的权重，逼下一个去专攻这些难点。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>弱分类器</b><p>单个“树桩”只切一刀、只比随机好一点；关键是它们能各管一段、互补。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>加权投票</b><p>最终预测＝所有弱分类器按权重 α 投票，错误率越低的票越重——合议出强分类器。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var pts=[],rounds=[],allW=[],step=0,playing=false,timer=null,MAXR=5;
function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
/* 数据：对角线 x+y=6 两侧，留出窄间隔，保证可被横竖刀拼出的楼梯分开 */
(function(){var r=rng(28),tries=0;
  while(pts.length<30 && tries<6000){tries++;
    var x=r()*6,y=r()*6,s=x+y;
    if(Math.abs(s-6)<0.4)continue;
    pts.push({x:x,y:y,t:(s<6)?1:-1});
  }})();
var N=pts.length;
/* 候选树桩：每轴相邻中点 × 两种极性 */
var CAND=(function(){var cs=[];["x","y"].forEach(function(key){
    var vals=pts.map(function(p){return p[key];}).sort(function(a,b){return a-b;});
    for(var i=0;i<vals.length-1;i++){if(vals[i]===vals[i+1])continue;var th=(vals[i]+vals[i+1])/2;
      cs.push({key:key,th:th,pol:1});cs.push({key:key,th:th,pol:-1});}});return cs;})();
function hOf(st,p){return (p[st.key]<st.th?st.pol:-st.pol);}
/* 预跑完整 AdaBoost */
(function(){var w=[];for(var i=0;i<N;i++)w.push(1/N);allW.push(w.slice());
  for(var t=0;t<MAXR;t++){
    var best=null;
    CAND.forEach(function(st){var err=0;for(var i=0;i<N;i++){if(hOf(st,pts[i])!==pts[i].t)err+=w[i];}
      if(!best||err<best.err)best={st:st,err:err};});
    var eps=Math.max(1e-6,Math.min(1-1e-6,best.err)),alpha=0.5*Math.log((1-eps)/eps),Z=0,nw=[];
    for(var i=0;i<N;i++){var m=(hOf(best.st,pts[i])===pts[i].t)?-1:1;var wi=w[i]*Math.exp(alpha*m);nw.push(wi);Z+=wi;}
    for(var i=0;i<N;i++)nw[i]/=Z;
    rounds.push({st:best.st,alpha:alpha,eps:eps});w=nw;allW.push(w.slice());
  }})();
function F(p,k){var s=0;for(var t=0;t<k;t++)s+=rounds[t].alpha*hOf(rounds[t].st,p);return s;}
function trainErr(k){var e=0;for(var i=0;i<N;i++){if((F(pts[i],k)>=0?1:-1)!==pts[i].t)e++;}return e;}
var SVGNS="http://www.w3.org/2000/svg",W=320,H=320,pad=16;
function wx(x){return pad+x/6*(W-2*pad);}
function wy(y){return (H-pad)-y/6*(H-2*pad);}
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function render(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  /* 判定区域（step>=1 才有分类器） */
  if(step>=1){var G=24,cw=(W-2*pad)/G,ch=(H-2*pad)/G;
    for(var gx=0;gx<G;gx++)for(var gy=0;gy<G;gy++){
      var cx=(gx+0.5)/G*6,cy=(gy+0.5)/G*6,f=F({x:cx,y:cy},step);
      E(svg,"rect",{x:pad+gx*cw,y:(H-pad)-(gy+1)*ch,width:cw+0.6,height:ch+0.6,fill:f>=0?"rgba(37,99,235,.13)":"rgba(181,82,74,.13)"});}
  }
  /* 坐标轴 */
  E(svg,"line",{x1:pad,y1:H-pad,x2:W-pad,y2:H-pad,"class":"axis"});
  E(svg,"line",{x1:pad,y1:pad,x2:pad,y2:H-pad,"class":"axis"});
  /* 最新弱分类器（虚线） */
  if(step>=1){var st=rounds[step-1].st;
    if(st.key==="x")E(svg,"line",{x1:wx(st.th),y1:pad,x2:wx(st.th),y2:H-pad,"class":"stump"});
    else E(svg,"line",{x1:pad,y1:wy(st.th),x2:W-pad,y2:wy(st.th),"class":"stump"});}
  /* 样本点：半径∝权重，深色圈=当前分错 */
  var w=allW[step];
  pts.forEach(function(p,i){var r=Math.max(4,Math.min(13,4+Math.sqrt(w[i]*N)*3.2));
    E(svg,"circle",{cx:wx(p.x),cy:wy(p.y),r:r,"class":"pt "+(p.t>0?"c1":"c0")});
    if(step>=1 && (F(p,step)>=0?1:-1)!==p.t)E(svg,"circle",{cx:wx(p.x),cy:wy(p.y),r:r+3.2,"class":"wrong"});});
  document.getElementById("stat").textContent=step===0?("未开始 · "+N+" 个样本"):("第 "+step+" 个弱分类器 · 训练错误 "+trainErr(step)+"/"+N);
  caption();
}
function caption(){
  var el=document.getElementById("caption");
  if(step===0){el.innerHTML="还没加分类器。蓝红被一条斜线分开，但每个弱分类器只能横切或竖切——单独一刀必然分错一片。点“加一个弱分类器”开始。";return;}
  var st=rounds[step-1].st,e=trainErr(step);
  var dir=st.key==="x"?"竖":"横",a=rounds[step-1].alpha.toFixed(2),eps=(rounds[step-1].eps*100).toFixed(0);
  if(step===1){el.innerHTML="<b>第 1 个：</b>一刀"+dir+"切（加权错误率 "+eps+"%，权重 α="+a+"）。一根线分不开斜边，还错 <b>"+e+"</b> 个——被分错的点权重已被放大（变大了）。";return;}
  if(e>0){el.innerHTML="<b>第 "+step+" 个：</b>又补一刀"+dir+"切（α="+a+"），专攻上一轮被放大的难点；当前还错 <b>"+e+"</b> 个，加权投票边界在逐步重塑（个别轮错误可能短暂回升，正常）。继续加。";return;}
  el.innerHTML="<b>第 "+step+" 个：</b>这串横竖刀加权投票，已经拼出一道贴合斜线的“楼梯”，<b>全分对了</b>。这就是 AdaBoost：弱分类器一根接一根、串联纠错，合成一个强分类器。";
}
function go(){if(step>=MAXR)return false;step++;render();return true;}
function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("auto").textContent="自动";}
document.getElementById("step").addEventListener("click",function(){stop();go();});
document.getElementById("auto").addEventListener("click",function(){if(playing){stop();return;}
  if(step>=MAXR){step=0;render();}playing=true;document.getElementById("auto").textContent="⏸ 暂停";
  timer=setInterval(function(){if(!go())stop();},950);});
document.getElementById("reset").addEventListener("click",function(){stop();step=0;render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){step=MAXR;render();return;}
  document.getElementById("auto").click();},1000);
})();
</script>
{% endraw %}

## 延伸阅读

<div class="resource-grid">
  <a class="resource-card" href="https://en.wikipedia.org/wiki/AdaBoost" target="_blank" rel="noopener">
    <h3>AdaBoost（维基百科）↗</h3>
    <p>提升法的标准定义、权重更新与 α 的推导，以及与指数损失的关系。</p>
  </a>
  <a class="resource-card" href="https://scikit-learn.org/stable/modules/ensemble.html#adaboost" target="_blank" rel="noopener">
    <h3>scikit-learn · AdaBoost ↗</h3>
    <p>可直接调用的实现与示例，含弱学习器、学习率等超参数说明。</p>
  </a>
</div>
