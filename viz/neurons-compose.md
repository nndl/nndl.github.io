---
layout: default
title: 神经元拼曲线
permalink: /viz/neurons-compose/
redirect_from:
  - /v/neurons-compose/
---

{% raw %}
<style>
.nclab .axis{stroke:var(--color-border);stroke-width:1;}
.nclab .target{fill:none;stroke:var(--color-border-strong);stroke-width:2.5;stroke-dasharray:6 4;}
.nclab .unit{fill:none;stroke:var(--color-accent);stroke-width:1.3;opacity:.32;}
.nclab .base{fill:none;stroke:var(--color-forest);stroke-width:1.3;opacity:.4;stroke-dasharray:2 3;}
.nclab .out{fill:none;stroke:var(--color-gold);stroke-width:3;stroke-linejoin:round;}
.nclab .knee{fill:var(--color-accent);opacity:.5;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 神经元拼曲线

神经网络凭什么能拟合各种复杂的关系？秘密其实很朴素：每个神经元（配上 ReLU 这种激活函数）只会做一件最简单的事——画一条“折一下”的线。但把很多条这样的折线叠加起来，就能拼出任意复杂的曲线。拖动“神经元个数”，看金色的拟合曲线怎样一步步贴近灰色目标。

<section class="vizui nclab" id="nclab">
  <p class="vizui__lead">灰色虚线是要拟合的目标曲线。淡蓝细线是每个神经元各自贡献的“折线”,金色粗线是它们叠加出来的结果。神经元越多，金线越贴合目标。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="m">神经元个数</label>
        <input type="range" id="m" min="1" max="10" step="1" value="3" style="width:200px">
        <output id="mVal">3</output>
      </span>
      <span class="vizui-spacer"></span>
      <button class="vizui-btn vizui-btn--go" id="auto" type="button">▶ 自动演示</button>
      <span id="err" class="vizui-pill">误差 —</span>
    </div>
  </div>

  <div class="vizui-panel">
    <div class="vizui-legend">
      <span><i style="background:var(--color-gold)"></i>叠加结果</span>
      <span><i style="background:var(--color-border-strong)"></i>目标曲线</span>
      <span><i style="background:var(--color-accent);opacity:.4"></i>单个神经元</span>
    </div>
    <svg class="vizui-chart" id="plot" viewBox="0 0 480 280" role="img" aria-label="神经元叠加拟合曲线"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>一个神经元 = 一条折线</b><p>ReLU 让每个神经元在某个位置“折一下”：之前是平的，之后是一段斜线。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>叠加 = 拼形状</b><p>把许多折线加在一起，折点越多，拼出的曲线就越精细。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>万能近似</b><p>理论上，只要神经元够多，这样一层网络就能逼近几乎任意连续函数。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var NS=90, XMIN=-3, XMAX=3, YMIN=-1.5, YMAX=1.5, m=3, playing=false, timer=null, model=null;
function target(x){return 1.7/(1+Math.exp(-1.8*(x+0.4)))-0.85;}   /* 平滑非振荡的 S 形目标，避免均匀采样混叠 */

/* 折线插值：把目标在 m+1 等距点上取样、连成折线；每个“折点”就是一个 ReLU 神经元。
   神经元越多 → 折点越密 → 误差稳定下降。 */
function fit(mm){
  var n=mm+1, pts=[], j;                               /* n 段，n+1 个采样点 */
  for(j=0;j<=n;j++){var x=XMIN+(XMAX-XMIN)*j/n;pts.push([x,target(x)]);}
  var slopes=[];for(j=0;j<n;j++)slopes.push((pts[j+1][1]-pts[j][1])/(pts[j+1][0]-pts[j][0]));
  var knees=[],coefs=[];for(j=1;j<n;j++){knees.push(pts[j][0]);coefs.push(slopes[j]-slopes[j-1]);}
  return {x0:pts[0][0],y0:pts[0][1],s0:slopes[0],knees:knees,coefs:coefs};
}
function evalNet(md,x){var y=md.y0+md.s0*(x-md.x0),i;for(i=0;i<md.knees.length;i++)y+=md.coefs[i]*Math.max(0,x-md.knees[i]);return y;}
function rmse(md){var s=0;for(var i=0;i<NS;i++){var x=XMIN+(XMAX-XMIN)*i/(NS-1),e=evalNet(md,x)-target(x);s+=e*e;}return Math.sqrt(s/NS);}

var SVGNS="http://www.w3.org/2000/svg",W=480,H=280,pad=20;
function wx(x){return pad+(x-XMIN)/(XMAX-XMIN)*(W-2*pad);}
function wy(y){return (H-pad)-(y-YMIN)/(YMAX-YMIN)*(H-2*pad);}
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function curve(svg,fn,cls){var p=[];for(var i=0;i<=120;i++){var x=XMIN+(XMAX-XMIN)*i/120;p.push(wx(x)+","+wy(Math.max(YMIN-0.3,Math.min(YMAX+0.3,fn(x)))));}E(svg,"polyline",{points:p.join(" "),"class":cls,"clip-path":"url(#nclip)"});}

function draw(){
  var svg=document.getElementById("plot"); while(svg.firstChild)svg.removeChild(svg.firstChild);
  var clip=E(svg,"clipPath",{id:"nclip"});E(clip,"rect",{x:pad-2,y:2,width:W-2*pad+4,height:H-4});
  E(svg,"line",{x1:pad,y1:wy(0),x2:W-pad,y2:wy(0),"class":"axis"});
  // 目标
  curve(svg,target,"target");
  var md=model;
  // 各神经元（ReLU 折线）贡献
  for(var i=0;i<md.knees.length;i++){(function(i){curve(svg,function(x){return md.coefs[i]*Math.max(0,x-md.knees[i]);},"unit");
    E(svg,"circle",{cx:wx(md.knees[i]),cy:wy(0),r:2.6,"class":"knee"});})(i);}
  // 叠加结果
  curve(svg,function(x){return evalNet(md,x);},"out");
}
function caption(){
  var el=document.getElementById("caption"),e=rmse(model);
  document.getElementById("err").textContent="误差 "+e.toFixed(3);
  if(m<=1)el.innerHTML="<b>只有 1 个神经元</b>：整条线只能折一个弯，离弯弯绕绕的目标差得远。";
  else if(m>=8)el.innerHTML="<b>"+m+" 个神经元</b>：这么多折线叠起来，金线已经几乎贴住目标了。神经元越多，能拼出的形状越精细——这就是神经网络“万能近似”的直觉。";
  else el.innerHTML="<b>"+m+" 个神经元</b>：拟合误差 "+e.toFixed(3)+"。继续增加神经元，看金线怎样越来越贴合灰色目标。";
}
function render(){model=fit(m);document.getElementById("mVal").textContent=m;draw();caption();}

function setM(v){m=Math.max(1,Math.min(10,v));document.getElementById("m").value=m;render();}
function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("auto").textContent="▶ 自动演示";}
function auto(){stop();playing=true;document.getElementById("auto").textContent="⏸ 暂停";var v=1;setM(1);
  timer=setInterval(function(){v++;if(v>10){stop();return;}setM(v);},620);}
document.getElementById("m").addEventListener("input",function(e){stop();setM(+e.target.value);});
document.getElementById("auto").addEventListener("click",function(){playing?stop():auto();});

/* 启动 + 自动演示 */
render();
setTimeout(function(){
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){setM(10);return;}
  auto();
},900);
})();
</script>
{% endraw %}
