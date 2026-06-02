---
layout: default
title: 缩放定律
permalink: /viz/scaling-laws/
redirect_from:
  - /v/scaling-laws/
---

{% raw %}
<style>
.sclab .axis{stroke:var(--color-border);stroke-width:1;}
.sclab .gridl{stroke:var(--color-border);stroke-width:1;opacity:.4;}
.sclab .alab{font:10px var(--font-mono);fill:var(--color-text-muted);}
.sclab .curve{fill:none;stroke:var(--color-accent);stroke-width:2.6;}
.sclab .extra{fill:none;stroke:var(--color-accent);stroke-width:2.6;stroke-dasharray:5 4;opacity:.7;}
.sclab .floor{stroke:var(--color-gold);stroke-width:1.6;stroke-dasharray:4 3;}
.sclab .obs{fill:var(--color-forest);stroke:#fff;stroke-width:1.5;}
.sclab .marker{fill:#b5524a;stroke:#fff;stroke-width:2;}
.sclab .vline{stroke:#b5524a;stroke-width:1.2;stroke-dasharray:3 3;opacity:.6;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 缩放定律

大模型为什么要拼命堆参数、堆数据、堆算力？因为有一条惊人稳定的规律：模型的损失（loss）会随着规模的增大**按幂律平滑下降**。把损失和规模都取对数画出来，竟是一条近乎笔直的线——这意味着，用几个小模型的结果，就能**外推预测**一个还没训练的大模型大概能到多低。拖动“模型规模”，看损失沿着这条线往下走。

<section class="sclab vizui" id="sclab">
  <p class="vizui__lead">横轴是模型规模（参数量，对数刻度），纵轴是损失（对数刻度）。<span style="color:var(--color-forest);font-weight:600">绿点</span>是几个已经训过的小模型，连成一条直线；虚线是<b>外推</b>到更大模型的预测。<span style="color:var(--color-gold);font-weight:600">金线</span>是怎么堆规模都突破不了的下限。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="n">模型规模</label><input type="range" id="n" min="0" max="6" step="0.1" value="1.4" style="width:200px"><output id="nVal"></output></span>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="pred">预测损失 —</span>
    </div>
    <svg class="vizui-chart" id="plot" viewBox="0 0 460 280" role="img" aria-label="损失随规模的幂律曲线"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>幂律 = 直线</b><p>损失 ≈ 下限 + A·规模^(−α)。取对数后是一条直线，斜率就是 −α。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>可外推预测</b><p>训几个小模型，就能预测大几个数量级的模型大概能到多低损失——省下大量试错。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>有下限</b><p>存在一个不可约的损失下限（数据本身的噪声），无论怎么堆规模都突破不了。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var E0=1.55, A=7.5, alpha=0.26;   /* loss = E0 + A * N^(-alpha)，N=参数量(百万) */
var logN=1.4;
function loss(lg){return E0+A*Math.pow(Math.pow(10,lg),-alpha);}
var SVGNS="http://www.w3.org/2000/svg",W=460,H=280,pl=44,pr=16,pt=16,pb=34;
var XLO=0,XHI=6, LYLO=Math.log10(E0)-0.015, LYHI=Math.log10(loss(0)+0.5);
function px(lg){return pl+(lg-XLO)/(XHI-XLO)*(W-pl-pr);}
function py(L){return (H-pb)-(Math.log10(L)-LYLO)/(LYHI-LYLO)*(H-pt-pb);}
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function fmtN(lg){var v=Math.pow(10,lg);return v<1000?(v.toFixed(0)+"M"):(v/1000).toFixed(v<10000?1:0)+"B";}
function draw(){
  var svg=document.getElementById("plot");while(svg.firstChild)svg.removeChild(svg.firstChild);
  for(var gx=0;gx<=6;gx++){E(svg,"line",{x1:px(gx),y1:pt,x2:px(gx),y2:H-pb,"class":"gridl"});E(svg,"text",{x:px(gx),y:H-pb+14,"text-anchor":"middle","class":"alab"}).textContent=fmtN(gx);}
  E(svg,"line",{x1:pl,y1:H-pb,x2:W-pr,y2:H-pb,"class":"axis"});E(svg,"line",{x1:pl,y1:pt,x2:pl,y2:H-pb,"class":"axis"});
  E(svg,"text",{x:pl,y:pt-4,"text-anchor":"middle","class":"alab"}).textContent="损失";
  E(svg,"text",{x:W-pr,y:H-pb+26,"text-anchor":"end","class":"alab"}).textContent="参数量（对数）";
  // 下限
  E(svg,"line",{x1:pl,y1:py(E0),x2:W-pr,y2:py(E0),"class":"floor"});
  E(svg,"text",{x:W-pr,y:py(E0)-4,"text-anchor":"end","class":"alab",style:"fill:var(--color-gold)"}).textContent="不可约下限";
  // 实测段(0~2) + 外推段(2~6)
  function seg(a,b,cls){var p=[];for(var i=0;i<=40;i++){var lg=a+(b-a)*i/40;p.push(px(lg)+","+py(loss(lg)));}E(svg,"polyline",{points:p.join(" "),"class":cls});}
  seg(0,2,"curve");seg(2,6,"extra");
  // 观测点
  [0.4,1.0,1.7].forEach(function(lg){E(svg,"circle",{cx:px(lg),cy:py(loss(lg)),r:4.5,"class":"obs"});});
  // 当前规模标记
  E(svg,"line",{x1:px(logN),y1:pt,x2:px(logN),y2:H-pb,"class":"vline"});
  E(svg,"circle",{cx:px(logN),cy:py(loss(logN)),r:6,"class":"marker"});
}
function render(){document.getElementById("nVal").textContent=fmtN(logN)+" 参数";document.getElementById("pred").textContent="预测损失 "+loss(logN).toFixed(2);draw();caption();}
function caption(){
  var el=document.getElementById("caption"),L=loss(logN);
  if(logN<=2)el.innerHTML="这是已经能训得起的规模（"+fmtN(logN)+"），损失 "+L.toFixed(2)+"。几个绿点连成一条直线——这就是幂律。";
  else el.innerHTML="把规模外推到 <b>"+fmtN(logN)+"</b>（还没训），沿着这条直线预测损失约 <b>"+L.toFixed(2)+"</b>。规模每涨 10 倍，损失稳定地降一截，但越来越贴近金色下限 "+E0.toFixed(2)+"——收益递减。";
}
document.getElementById("n").addEventListener("input",function(e){logN=+e.target.value;render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  var k=0,sl=document.getElementById("n");var iv=setInterval(function(){k++;logN=Math.min(6,0.6+k*0.45);sl.value=logN;render();if(logN>=6)clearInterval(iv);},260);},1000);
})();
</script>
{% endraw %}
