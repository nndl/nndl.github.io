---
layout: default
title: 批归一化 BatchNorm
description: "把每批激活减均值除标准差拉回‘均值0方差1’，让深层网络训练又快又稳。"
permalink: /viz/batchnorm/
redirect_from:
  - /v/batchnorm/
---

{% raw %}
<style>
.bnlab .axis{stroke:var(--color-border);stroke-width:1;}
.bnlab .alab{font:10px var(--font-mono);fill:var(--color-text-muted);}
.bnlab .zone{fill:var(--color-forest);opacity:.07;}
.bnlab .pt-raw{fill:var(--color-text-muted);}
.bnlab .pt-bn{fill:var(--color-accent);}
.bnlab .gauss{fill:none;stroke-width:2.4;}
.bnlab .g-raw{stroke:var(--color-text-muted);opacity:.7;}
.bnlab .g-bn{stroke:var(--color-accent);}
.bnlab .meanline{stroke-width:1.6;stroke-dasharray:4 3;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 批归一化 BatchNorm

深层网络训练时有个麻烦：每一层的输入分布会随着前面层不断变化而漂来漂去——一会儿偏大、一会儿太散，后面的层就像在追一个移动的靶子，学得又慢又不稳。批归一化的办法很直接：在每一层，把这一批数据的激活值**减去均值、除以标准差**，强行拉回“均值 0、方差 1”的标准范围，再用两个可学习参数微调。于是每层拿到的输入都很规整，训练快得多也稳得多。拖动“原始均值”和“散布”制造糟糕的激活，看 BatchNorm 怎么把它拉回来。

<section class="bnlab vizui" id="bnlab">
  <p class="vizui__lead">灰点是进入这一层的原始激活（你可以把它调得又偏又散），蓝点是经过 BatchNorm 后的——总是乖乖落在中间、宽度归一的绿色稳定带里。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="mu">原始均值</label><input type="range" id="mu" min="-4" max="4" step="0.2" value="2.6" style="width:120px"><output id="muVal"></output></span>
      <span class="vizui-field"><label for="sg">原始散布</label><input type="range" id="sg" min="0.4" max="3" step="0.1" value="2.2" style="width:120px"><output id="sgVal"></output></span>
      <span class="vizui-spacer"></span>
      <button class="vizui-btn" id="resample" type="button">↻ 新一批</button>
    </div>
    <svg class="vizui-chart" id="plot" viewBox="0 0 460 220" role="img" aria-label="BatchNorm 前后分布"></svg>
    <div style="display:flex;justify-content:space-around;font-size:.86rem;margin-top:6px">
      <span>原始：μ=<b id="rmu" style="font-family:var(--font-mono)">—</b> σ=<b id="rsg" style="font-family:var(--font-mono)">—</b></span>
      <span style="color:var(--color-accent)">归一后：μ=<b id="bmu" style="font-family:var(--font-mono)">—</b> σ=<b id="bsg" style="font-family:var(--font-mono)">—</b></span>
    </div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>减均值除标准差</b><p>把每批激活拉到均值 0、方差 1，后面的层总能拿到分布稳定的输入。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>训练更快更稳</b><p>可以用更大的学习率，对初始化也没那么挑剔，深层网络更容易收敛。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>还能微调</b><p>归一化后再乘 γ、加 β（可学习），让网络在需要时恢复表达力。LayerNorm 是它在 Transformer 里的近亲。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var mu=2.6, sg=2.2, base=[];
function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
function gauss(r){var u=0,v=0;while(!u)u=r();while(!v)v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}
function regen(){var r=rng(13);base=[];for(var i=0;i<26;i++)base.push(gauss(r));}
regen();
function stats(a){var m=0;a.forEach(function(v){m+=v;});m/=a.length;var s=0;a.forEach(function(v){s+=(v-m)*(v-m);});return {m:m,s:Math.sqrt(s/a.length)};}
var SVGNS="http://www.w3.org/2000/svg",W=460,H=220,pl=16,pr=16,XR=14;
function wx(x){return pl+(x+XR)/(2*XR)*(W-pl-pr);}
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function gcurve(svg,m,s,yb,col){var pts=[];for(var i=0;i<=120;i++){var x=-XR+2*XR*i/120,g=Math.exp(-(x-m)*(x-m)/(2*s*s));pts.push(wx(x)+","+(yb-g*54));}E(svg,"polyline",{points:pts.join(" "),"class":"gauss "+col});}
function strip(svg,vals,y,cls){vals.forEach(function(v){E(svg,"circle",{cx:wx(v),cy:y+(Math.random()-0.5)*14,r:3.4,"class":cls});});}
function draw(){
  var svg=document.getElementById("plot");while(svg.firstChild)svg.removeChild(svg.firstChild);
  // 稳定带 [-2,2]
  E(svg,"rect",{x:wx(-2),y:8,width:wx(2)-wx(-2),height:H-26,"class":"zone"});
  E(svg,"line",{x1:pl,y1:H-18,x2:W-pr,y2:H-18,"class":"axis"});
  [-12,-8,-4,0,4,8,12].forEach(function(t){E(svg,"text",{x:wx(t),y:H-5,"text-anchor":"middle","class":"alab"}).textContent=t;});
  E(svg,"line",{x1:wx(0),y1:8,x2:wx(0),y2:H-18,"class":"axis"});
  var raw=base.map(function(z){return mu+z*sg;}), st=stats(raw);
  var bn=raw.map(function(x){return (x-st.m)/(st.s||1);});
  gcurve(svg,st.m,st.s||0.3,80,"g-raw");gcurve(svg,0,1,170,"g-bn");
  strip(svg,raw,64,"pt-raw");strip(svg,bn,154,"pt-bn");
  E(svg,"text",{x:pl+4,y:24,"class":"alab"}).textContent="原始激活（漂移/过散）";
  E(svg,"text",{x:pl+4,y:118,"class":"alab",style:"fill:var(--color-accent)"}).textContent="BatchNorm 后（μ=0, σ=1）";
  var bs=stats(bn);
  document.getElementById("rmu").textContent=st.m.toFixed(2);document.getElementById("rsg").textContent=st.s.toFixed(2);
  document.getElementById("bmu").textContent=bs.m.toFixed(2);document.getElementById("bsg").textContent=bs.s.toFixed(2);
  caption(st);
}
function caption(st){document.getElementById("caption").innerHTML="这批原始激活均值 <b>"+st.m.toFixed(1)+"</b>、标准差 <b>"+st.s.toFixed(1)+"</b>（灰点偏在一边、又宽又散）。BatchNorm 一减一除，蓝点立刻被拉回<b>均值 0、方差 1</b>的绿色稳定带——无论你把上面调得多糟，下面永远规整。";}
function render(){document.getElementById("muVal").textContent=mu.toFixed(1);document.getElementById("sgVal").textContent=sg.toFixed(1);draw();}
document.getElementById("mu").addEventListener("input",function(e){mu=+e.target.value;render();});
document.getElementById("sg").addEventListener("input",function(e){sg=+e.target.value;render();});
document.getElementById("resample").addEventListener("click",function(){regen();render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  var seq=[[2.6,2.2],[-3,1],[3.5,2.8],[0.5,0.6],[2.6,2.2]],k=0,sm=document.getElementById("mu"),ss=document.getElementById("sg");
  var iv=setInterval(function(){mu=seq[k][0];sg=seq[k][1];sm.value=mu;ss.value=sg;render();k++;if(k>=seq.length)clearInterval(iv);},950);},1000);
})();
</script>
{% endraw %}
