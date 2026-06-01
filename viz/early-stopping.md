---
layout: default
title: 早停：见好就收
permalink: /viz/early-stopping/
redirect_from:
  - /v/early-stopping/
---

{% raw %}
<style>
.eslab svg{max-width:100%;height:auto;}
.eslab .axis{stroke:var(--color-border-strong);stroke-width:1;}
.eslab .alab{font:11px var(--font-sans);fill:var(--color-text-muted);}
.eslab .train{fill:none;stroke:var(--color-accent-light,#2563eb);stroke-width:2.5;}
.eslab .val{fill:none;stroke:#b5524a;stroke-width:2.5;}
.eslab .now{stroke:var(--color-text);stroke-width:1.5;stroke-dasharray:3 3;}
.eslab .stop{stroke:var(--color-gold);stroke-width:2;stroke-dasharray:5 3;}
.eslab .overfit{fill:#b5524a;opacity:.07;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 早停：见好就收

训练神经网络时，训练得越久，它在**训练集**上的误差几乎总在下降——看起来越来越好。但这是假象：从某一刻起，模型开始死记硬背训练数据的噪声，在**没见过的验证集**上反而越来越差。把验证误差画出来，会是一条先降后升的 U 形曲线。聪明的做法是**在 U 形谷底就停手**——这叫**早停**：不是训得越久越好，而是“见好就收”。拖动滑块推进训练轮数，看两条曲线怎么分道扬镳。

<section class="vizui eslab" id="eslab">
  <p class="vizui__lead"><span style="color:var(--color-accent-light,#2563eb)">蓝线</span>是训练误差（一路降），<span style="color:#b5524a">红线</span>是验证误差（先降后升）。<b>金色虚线</b>是验证误差最低点——就该在这里早停。再往后是<span style="color:#b5524a">过拟合区</span>。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="e">训练轮数</label><input type="range" id="e" min="0" max="59" step="1" value="0" style="width:200px"><output id="eVal">0</output></span>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stat">—</span>
    </div>
    <svg id="plane" viewBox="0 0 460 290" role="img" aria-label="早停曲线"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent-light,#2563eb)"><b>训练误差骗人</b><p>它几乎总在降，单看它你会以为越训越好——其实是开始背噪声了。</p></div>
    <div class="card" style="--wc:#b5524a"><b>验证误差是真相</b><p>用没见过的数据衡量泛化。它的 U 形谷底，就是模型最会“举一反三”的时刻。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>早停=免费正则</b><p>在谷底停手，不用改模型就避免了过拟合，还省了算力，几乎零成本。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var EP=60,cur=0;
var train=[],val=[];
for(var e=0;e<EP;e++){ train.push(0.82*Math.exp(-e/9)+0.05); val.push(0.80*Math.exp(-e/8.5)+0.13+0.00016*e*e); }
var stopE=0,best=1e9;for(var i=0;i<EP;i++)if(val[i]<best){best=val[i];stopE=i;}
var SVGNS="http://www.w3.org/2000/svg",W=460,H=290,pl=36,pr=14,pt=14,pb=28;
function px(e){return pl+e/(EP-1)*(W-pl-pr);}function py(v){return (H-pb)-(v/1.0)*(H-pt-pb);}
function E(p,t,a,txt){var x=document.createElementNS(SVGNS,t);for(var k in a)x.setAttribute(k,a[k]);if(txt!=null)x.textContent=txt;p.appendChild(x);return x;}
function poly(svg,arr,cls,upto){var pts=[];for(var i=0;i<=upto;i++)pts.push(px(i)+","+py(arr[i]));E(svg,"polyline",{points:pts.join(" "),"class":cls});}
function render(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  E(svg,"rect",{x:px(stopE),y:pt,width:(W-pr)-px(stopE),height:(H-pb)-pt,"class":"overfit"});
  E(svg,"line",{x1:pl,y1:H-pb,x2:W-pr,y2:H-pb,"class":"axis"});E(svg,"line",{x1:pl,y1:pt,x2:pl,y2:H-pb,"class":"axis"});
  E(svg,"text",{x:(W)/2,y:H-6,"text-anchor":"middle","class":"alab"},"训练轮数 →");
  E(svg,"text",{x:12,y:H/2,"text-anchor":"middle","class":"alab",transform:"rotate(-90 12 "+H/2+")"},"误差");
  poly(svg,train,"train",cur);poly(svg,val,"val",cur);
  // 早停线（仅当已训练到该点之后才显现）
  if(cur>=stopE){ E(svg,"line",{x1:px(stopE),y1:pt,x2:px(stopE),y2:H-pb,"class":"stop"}); E(svg,"text",{x:px(stopE),y:pt-3,"text-anchor":"middle","class":"alab",style:"fill:var(--color-gold);font-weight:600"},"早停点"); E(svg,"circle",{cx:px(stopE),cy:py(val[stopE]),r:4,fill:"var(--color-gold)",stroke:"#fff","stroke-width":1.5}); }
  E(svg,"line",{x1:px(cur),y1:pt,x2:px(cur),y2:H-pb,"class":"now"});
  E(svg,"circle",{cx:px(cur),cy:py(train[cur]),r:3.5,fill:"var(--color-accent-light,#2563eb)",stroke:"#fff"});
  E(svg,"circle",{cx:px(cur),cy:py(val[cur]),r:3.5,fill:"#b5524a",stroke:"#fff"});
  document.getElementById("eVal").textContent=cur;
  document.getElementById("stat").textContent="训练 "+train[cur].toFixed(2)+" · 验证 "+val[cur].toFixed(2);
  caption();
}
function caption(){
  var el=document.getElementById("caption");
  if(cur<stopE-3)el.innerHTML="<b>第 "+cur+" 轮：</b>两条线一起往下走——模型在真学规律，越训越好。";
  else if(cur<=stopE+2)el.innerHTML="<b>第 "+cur+" 轮：</b>验证误差到达谷底（第 "+stopE+" 轮）！此刻泛化最好，<b>就该早停</b>。再训下去就开始过拟合了。";
  else el.innerHTML="<b>第 "+cur+" 轮：</b>训练误差还在降，但验证误差已经掉头往上——模型在背噪声、泛化变差。早停点（第 "+stopE+" 轮）才是该停的地方。";
}
document.getElementById("e").addEventListener("input",function(ev){cur=+ev.target.value;render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){cur=stopE;document.getElementById("e").value=cur;render();return;}
  var sl=document.getElementById("e");var iv=setInterval(function(){cur++;if(cur>=EP-1){cur=EP-1;clearInterval(iv);}sl.value=cur;render();},120);},900);
})();
</script>
{% endraw %}
