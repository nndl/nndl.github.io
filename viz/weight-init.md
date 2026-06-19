---
layout: default
title: 权重初始化
permalink: /viz/weight-init/
redirect_from:
  - /v/weight-init/
---

{% raw %}
<style>
.wilab .axis{stroke:var(--color-border);stroke-width:1;}
.wilab .alab{font:10px var(--font-mono);fill:var(--color-text-muted);}
.wilab .stableline{stroke:var(--color-forest);stroke-width:1.4;stroke-dasharray:5 4;opacity:.7;}
.wilab .curve{fill:none;stroke-width:2.8;stroke-linejoin:round;}
.wilab .dot{stroke:#fff;stroke-width:1.2;}
.wilab .heads{display:inline-flex;gap:4px;padding:4px;background:var(--color-bg-section);border:1px solid var(--color-border);border-radius:999px;}
.wilab .heads button{appearance:none;border:0;background:transparent;cursor:pointer;font:inherit;font-size:.84rem;color:var(--color-text-soft);padding:6px 12px;border-radius:999px;}
.wilab .heads button.on{background:var(--color-bg-pure);font-weight:600;box-shadow:var(--shadow-sm);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 权重初始化

训练前，网络的权重得先随机赋个初值——这一步看似不起眼，却能决定网络“生死”。信号在前向传播时，每过一层就被权重缩放一次：如果初始权重整体偏大，信号一层层放大，到深处就**爆炸**；偏小则一层层缩小，到深处**消失**。两种都让网络没法训。Xavier / He 初始化的诀窍，是按每层的宽度把权重缩放到“不大不小”，让信号的强度（方差）逐层**保持稳定**。拖动权重尺度，看信号穿过 18 层后是爆、是没、还是稳。

<section class="wilab vizui" id="wilab">
  <p class="vizui__lead">纵轴是信号强度（标准差，对数刻度），横轴是层数。绿色虚线是“稳定”水平。看曲线穿过深层时是冲上天、跌到底、还是平稳。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="heads" id="heads"><button data-g="0.55" type="button">太小</button><button data-g="1.0" class="on" type="button">恰好（Xavier）</button><button data-g="1.7" type="button">太大</button></span>
      <span class="vizui-field"><label for="g">权重尺度</label><input type="range" id="g" min="0.5" max="1.9" step="0.05" value="1.0" style="width:140px"><output id="gVal">1.00</output></span>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="info">—</span>
    </div>
    <svg class="vizui-chart" id="plot" viewBox="0 0 460 240" role="img" aria-label="各层信号强度"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:#b5524a"><b>太大 → 爆炸</b><p>每层放大一点，深层信号指数级冲高，梯度也跟着爆，训练直接发散。</p></div>
    <div class="card" style="--wc:var(--color-text-muted)"><b>太小 → 消失</b><p>每层缩小一点，深层信号趋近 0，梯度也消失，底层学不动。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>恰好 → 稳定</b><p>Xavier/He 按层宽缩放权重，让信号方差逐层不变——深层网络才训得起来。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var D=24, L=18, gain=1.0, demoIv=null;
function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
function gauss(r){var u=0,v=0;while(!u)u=r();while(!v)v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}
function propagate(){
  var r=rng(3), a=[];for(var i=0;i<D;i++)a.push(gauss(r));
  var stds=[std(a)], sw=gain/Math.sqrt(D);
  for(var l=0;l<L;l++){var na=[];for(var i2=0;i2<D;i2++){var s=0;for(var j=0;j<D;j++)s+=gauss(r)*sw*a[j];na.push(s);}a=na;stds.push(std(a));}
  return stds;
}
function std(a){var m=0;a.forEach(function(v){m+=v;});m/=a.length;var s=0;a.forEach(function(v){s+=(v-m)*(v-m);});return Math.sqrt(s/a.length);}
var SVGNS="http://www.w3.org/2000/svg",W=460,H=240,pl=40,pr=14,pt=14,pb=26,YLO=-4,YHI=4;
function px(l){return pl+l/L*(W-pl-pr);}
function py(logv){return (H-pb)-(logv-YLO)/(YHI-YLO)*(H-pt-pb);}
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function draw(){
  var svg=document.getElementById("plot");while(svg.firstChild)svg.removeChild(svg.firstChild);
  [-4,-2,0,2,4].forEach(function(e){var y=py(e);E(svg,"line",{x1:pl,y1:y,x2:W-pr,y2:y,stroke:"#eef1ee","stroke-width":1});E(svg,"text",{x:pl-5,y:y+3,"text-anchor":"end","class":"alab"}).textContent="1e"+e;});
  E(svg,"line",{x1:pl,y1:py(0),x2:W-pr,y2:py(0),"class":"stableline"});
  E(svg,"text",{x:W-pr,y:py(0)-5,"text-anchor":"end","class":"alab",style:"fill:var(--color-forest)"}).textContent="稳定";
  E(svg,"line",{x1:pl,y1:pt,x2:pl,y2:H-pb,"class":"axis"});E(svg,"line",{x1:pl,y1:H-pb,x2:W-pr,y2:H-pb,"class":"axis"});
  E(svg,"text",{x:(pl+W-pr)/2,y:H-4,"text-anchor":"middle","class":"alab"}).textContent="层数 →";
  var stds=propagate();
  var col=gain>1.15?"#b5524a":gain<0.85?"#9aa5a3":"#206a4f";
  var pts=stds.map(function(s,l){return px(l)+","+py(Math.log10(Math.max(1e-6,s)));});
  E(svg,"polyline",{points:pts.join(" "),"class":"curve",stroke:col});
  stds.forEach(function(s,l){E(svg,"circle",{cx:px(l),cy:py(Math.log10(Math.max(1e-6,s))),r:2.6,"class":"dot",fill:col});});
  var fin=stds[stds.length-1];
  document.getElementById("info").textContent="第 "+L+" 层信号 ≈ "+(fin>1000||fin<0.001?fin.toExponential(1):fin.toFixed(2));
  caption(fin);
}
function caption(fin){
  var el=document.getElementById("caption");
  if(gain>1.15)el.innerHTML="<b>太大（尺度 "+gain.toFixed(2)+"）：</b>信号每层放大，曲线一路冲上天，到第 18 层已是 <b>"+fin.toExponential(1)+"</b>——爆炸。梯度同样会爆，训练发散。";
  else if(gain<0.85)el.innerHTML="<b>太小（尺度 "+gain.toFixed(2)+"）：</b>信号每层缩小，曲线一路跌到底，到第 18 层只剩 <b>"+fin.toExponential(1)+"</b>——消失。底层收不到信号，学不动。";
  else el.innerHTML="<b>恰好（尺度 "+gain.toFixed(2)+"≈Xavier）：</b>曲线贴着绿色稳定线，信号强度逐层基本不变（第 18 层 "+fin.toFixed(2)+"）。这正是深层网络能正常训练的前提。";
}
function render(){document.getElementById("gVal").textContent=gain.toFixed(2);document.querySelectorAll("#heads button").forEach(function(b){b.classList.toggle("on",Math.abs(+b.dataset.g-gain)<0.03);});draw();}
document.getElementById("heads").addEventListener("click",function(e){var b=e.target.closest("button");if(!b)return;if(demoIv){clearInterval(demoIv);demoIv=null;}gain=+b.dataset.g;document.getElementById("g").value=gain;render();});
document.getElementById("g").addEventListener("input",function(e){if(demoIv){clearInterval(demoIv);demoIv=null;}gain=+e.target.value;render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  var seq=[1.7,0.55,1.0],k=0,sl=document.getElementById("g");demoIv=setInterval(function(){gain=seq[k];sl.value=gain;render();k++;if(k>=seq.length){clearInterval(demoIv);demoIv=null;}},1100);},1000);
})();
</script>
{% endraw %}
