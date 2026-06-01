---
layout: default
title: 量化
permalink: /viz/quantization/
redirect_from:
  - /v/quantization/
---

{% raw %}
<style>
.qzlab .axis{stroke:var(--color-border);stroke-width:1;}
.qzlab .grid{stroke:var(--color-gold);stroke-width:1;opacity:.45;}
.qzlab .alab{font:10px var(--font-mono);fill:var(--color-text-muted);}
.qzlab .pt-raw{fill:var(--color-text-muted);opacity:.65;}
.qzlab .pt-q{fill:var(--color-accent);}
.qzlab .errln{stroke:#b5524a;stroke-width:1;opacity:.5;}
.qzlab .sizebar{height:22px;border-radius:6px;overflow:hidden;display:flex;}
.qzlab .sizebar i{height:100%;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 量化

大模型动辄几百亿参数，每个权重若用 32 位浮点数（fp32）存，光是装下就要海量内存，跑起来也慢。量化的办法是：用更少的位数来表示权重——比如只用 8 位甚至 4 位整数。代价是精度：连续的权重被“吸附”到一个个离散的档位上，多少会有误差。位数越少，档位越粗、误差越大，但体积和速度的收益也越大。这是把大模型塞进手机、消费级显卡的关键一步。拖动位数，看权重怎么被吸附到网格上、误差和体积怎么变。

<section class="qzlab vizui" id="qzlab">
  <p class="vizui__lead">灰点是原始的连续权重，金色竖线是量化档位，蓝点是被吸附到最近档位后的权重，红线是吸附产生的误差。位数越少，档位越稀疏。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="bits">位数 bits</label><input type="range" id="bits" min="1" max="8" step="1" value="8" style="width:170px"><output id="bitsVal"></output></span>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="info">—</span>
    </div>
    <svg class="vizui-chart" id="plot" viewBox="0 0 460 150" role="img" aria-label="权重量化"></svg>
    <div style="margin-top:12px">
      <div style="display:flex;justify-content:space-between;font-size:.85rem;margin-bottom:3px"><span>相对 fp32 的体积</span><b id="sizeTxt" style="font-family:var(--font-mono);color:var(--color-accent)">—</b></div>
      <div class="sizebar" style="background:var(--color-bg-section)"><i id="sizeBar" style="background:var(--color-accent)"></i></div>
    </div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>更少位数 = 更小</b><p>fp32→int8 体积缩到 1/4，int4 缩到 1/8；显存、带宽、能耗都跟着降。</p></div>
    <div class="card" style="--wc:#b5524a"><b>代价是精度</b><p>权重被吸附到离散档位，位数越少误差越大；太激进会让模型变笨。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>常用 8 / 4 位</b><p>8 位几乎无损，4 位配合一些技巧也能用——这是大模型上端侧、消费级显卡的关键。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var bits=8, weights=[];
function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
function gss(r){var u=0,v=0;while(!u)u=r();while(!v)v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}
(function(){var r=rng(5);for(var i=0;i<48;i++)weights.push(Math.max(-1,Math.min(1,gss(r)*0.42)));})();
function quant(w,levels){var t=Math.round((w+1)/2*(levels-1));return t/(levels-1)*2-1;}
var SVGNS="http://www.w3.org/2000/svg",W=460,H=150,pl=16,pr=16,yR=70,yQ=120;
function wx(x){return pl+(x+1)/2*(W-pl-pr);}
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function draw(){
  var svg=document.getElementById("plot");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var levels=Math.pow(2,bits);
  if(levels<=33){for(var i=0;i<levels;i++){var x=-1+2*i/(levels-1);E(svg,"line",{x1:wx(x),y1:14,x2:wx(x),y2:H-14,"class":"grid"});}}
  E(svg,"line",{x1:pl,y1:yR,x2:W-pr,y2:yR,"class":"axis"});E(svg,"line",{x1:pl,y1:yQ,x2:W-pr,y2:yQ,"class":"axis"});
  E(svg,"text",{x:pl,y:42,"class":"alab"}).textContent="原始权重（连续）";
  E(svg,"text",{x:pl,y:yQ-10,"class":"alab",style:"fill:var(--color-accent)"}).textContent="量化后（吸附到档位）";
  var err=0;
  weights.forEach(function(w,i){var q=quant(w,levels);err+=Math.abs(w-q);var jit=((i%7)-3)*2.2;
    E(svg,"line",{x1:wx(w),y1:yR+jit,x2:wx(q),y2:yQ,"class":"errln"});
    E(svg,"circle",{cx:wx(w),cy:yR+jit,r:3,"class":"pt-raw"});
    E(svg,"circle",{cx:wx(q),cy:yQ,r:3.2,"class":"pt-q"});});
  err/=weights.length;
  document.getElementById("info").textContent=levels+" 个档位 · 平均误差 "+err.toFixed(3);
  var frac=bits/32;
  document.getElementById("sizeTxt").textContent=(frac*100).toFixed(0)+"%（缩小 "+(32/bits).toFixed(32/bits>=10?0:1)+"×）";
  document.getElementById("sizeBar").style.width=(frac*100)+"%";
  caption(levels,err);
}
function caption(levels,err){
  var el=document.getElementById("caption");
  if(bits>=8)el.innerHTML="<b>"+bits+" 位（"+levels+" 档）：</b>档位很密，蓝点几乎和灰点重合，平均误差仅 "+err.toFixed(3)+"——几乎无损，体积却已是 fp32 的 1/4。这是最常用的量化。";
  else if(bits<=2)el.innerHTML="<b>"+bits+" 位（"+levels+" 档）：</b>只有几个档位，所有权重被硬挤到几个点上，误差高达 "+err.toFixed(3)+"——太激进，模型会明显变笨。";
  else el.innerHTML="<b>"+bits+" 位（"+levels+" 档）：</b>权重被吸附到 "+levels+" 个档位，平均误差 "+err.toFixed(3)+"。体积缩到 fp32 的 "+(bits/32*100).toFixed(0)+"%。位数和精度之间要权衡。";
}
document.getElementById("bits").addEventListener("input",function(e){bits=+e.target.value;document.getElementById("bitsVal").textContent=bits;draw();});
document.getElementById("bitsVal").textContent=bits;draw();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  var seq=[8,4,3,2,4],k=0,sl=document.getElementById("bits");var iv=setInterval(function(){bits=seq[k];sl.value=bits;document.getElementById("bitsVal").textContent=bits;draw();k++;if(k>=seq.length)clearInterval(iv);},950);},1000);
})();
</script>
{% endraw %}
