---
layout: default
title: 对比学习与 CLIP
permalink: /viz/contrastive/
redirect_from:
  - /v/contrastive/
---

{% raw %}
<style>
.cllab svg{max-width:100%;height:auto;}
.cllab .cell{stroke:#fff;stroke-width:2;}
.cllab .diag{stroke:var(--color-gold);stroke-width:2.5;fill:none;}
.cllab .emoji{font-size:22px;}
.cllab .tlbl{font:13px var(--font-sans);fill:#333;}
.cllab .sval{font:10px var(--font-mono);fill:#444;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 对比学习与 CLIP

怎么让模型同时看懂图和文字？CLIP 的办法出奇地简单：拿一大批**配对**的“图片+对应文字”，让模型把**每张图和它自己的文字**在表示空间里**拉近**，同时把**图和别人的文字**（同一批里其它的）**推远**。不需要人工标注类别，只要“这段文字配这张图”这种现成的配对。训练到位后，正确的图文对相似度最高，整张相似度矩阵的**对角线会亮起来**。点“训练”，看一团乱糟糟的相似度怎么收敛成一条金色对角线。

<section class="vizui cllab" id="cllab">
  <p class="vizui__lead">每行一张图、每列一段文字，格子颜色是“图配文”的相似度（越蓝越像）。我们要的：<b>对角线</b>（图配自己的文字）最亮，其余（配错的）最淡。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <button class="vizui-btn vizui-btn--go" id="train" type="button">▶ 训练</button>
      <button class="vizui-btn" id="reset" type="button">重置</button>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stat">未训练</span>
    </div>
    <svg id="plane" viewBox="0 0 340 320" role="img" aria-label="对比学习相似度矩阵"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>拉近正样本</b><p>每张图和它对应的文字，在表示空间里靠得越近越好。</p></div>
    <div class="card" style="--wc:#b5524a"><b>推远负样本</b><p>同一批里其它不配对的图文，要被推开——这就是“对比”。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>免标注、可零样本</b><p>只用现成图文对训练，之后能对没见过的类别直接做“图文匹配”分类。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var imgs=["🐱","🐶","🚗","🌳","🏠"],texts=["“一只猫”","“一只狗”","“一辆车”","“一棵树”","“一座房子”"],N=5;
function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
var sim=[],r=rng(5);function reset(){sim=[];for(var i=0;i<N;i++){sim.push([]);for(var j=0;j<N;j++)sim[i].push(0.35+0.25*r());}}
reset();
var step=0,timer=null;
var SVGNS="http://www.w3.org/2000/svg",cw=44,x0=84,y0=70;
function col(v){var t=v<0?0:v>1?1:v,w=[244,241,235],a=[21,94,117];return"rgb("+((w[0]+(a[0]-w[0])*t)|0)+","+((w[1]+(a[1]-w[1])*t)|0)+","+((w[2]+(a[2]-w[2])*t)|0)+")";}
function E(p,t,a,txt){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;p.appendChild(e);return e;}
function render(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  for(var j=0;j<N;j++)E(svg,"text",{x:x0+j*cw+cw/2,y:y0-12,"text-anchor":"middle","class":"tlbl"},texts[j].slice(0,4));
  for(var i=0;i<N;i++){
    E(svg,"text",{x:x0-16,y:y0+i*cw+cw/2+8,"text-anchor":"middle","class":"emoji"},imgs[i]);
    for(var j2=0;j2<N;j2++){
      E(svg,"rect",{x:x0+j2*cw,y:y0+i*cw,width:cw,height:cw,fill:col(sim[i][j2]),"class":"cell"});
      E(svg,"text",{x:x0+j2*cw+cw/2,y:y0+i*cw+cw/2+4,"text-anchor":"middle","class":"sval",fill:sim[i][j2]>0.6?"#fff":"#444"},sim[i][j2].toFixed(2));
    }
  }
  for(var d=0;d<N;d++)E(svg,"rect",{x:x0+d*cw+1,y:y0+d*cw+1,width:cw-2,height:cw-2,"class":"diag"});
  var dm=0,om=0,oc=0;for(var a=0;a<N;a++)for(var b=0;b<N;b++){if(a===b)dm+=sim[a][b];else{om+=sim[a][b];oc++;}}
  document.getElementById("stat").textContent=step===0?"未训练":("第 "+step+" 步 · 对角 "+(dm/N).toFixed(2)+" / 其它 "+(om/oc).toFixed(2));
  caption(dm/N,om/oc);
}
function caption(diag,off){
  var el=document.getElementById("caption");
  if(step===0)el.innerHTML="一开始相似度乱糟糟，对角线（配对正确）并不比别处亮。点“训练”，让对比学习去拉近正样本、推远负样本。";
  else if(diag<0.7)el.innerHTML="训练中（第 "+step+" 步）：对角线在变蓝、其它格子在变淡——正样本被拉近、负样本被推远。";
  else el.innerHTML="训练完成：对角线平均相似度 <b>"+diag.toFixed(2)+"</b>，远高于其它 <b>"+off.toFixed(2)+"</b>。每张图都和自己的文字最配——CLIP 就这样在没有人工标类别的情况下学会了图文对应。";
}
function stepOnce(){step++;for(var i=0;i<N;i++)for(var j=0;j<N;j++){var tgt=(i===j)?1:0.06;sim[i][j]+=0.16*(tgt-sim[i][j]);}render();}
function play(){if(timer)return;timer=setInterval(function(){stepOnce();if(step>=18){clearInterval(timer);timer=null;}},180);}
document.getElementById("train").addEventListener("click",play);
document.getElementById("reset").addEventListener("click",function(){if(timer){clearInterval(timer);timer=null;}step=0;reset();render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){for(var k=0;k<18;k++)stepOnce();return;}play();},1100);
})();
</script>
{% endraw %}
