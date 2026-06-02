---
layout: default
title: 相关不等于因果
permalink: /viz/correlation-causation/
redirect_from:
  - /v/correlation-causation/
---

{% raw %}
<style>
.cclab .axis{stroke:var(--color-border-strong);stroke-width:1;}
.cclab .alab{font:11px var(--font-sans);fill:var(--color-text-muted);}
.cclab .pt{stroke:#fff;stroke-width:1;}
.cclab .pt.dim{opacity:.15;}
.cclab .trend{stroke:var(--color-text);stroke-width:2;stroke-dasharray:5 4;}
.cclab .trend.band{stroke:var(--color-forest);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 相关不等于因果

一个经典的例子：城市里**冰淇淋销量**越高，**溺水人数**也越多，两者高度相关。难道吃冰淇淋会让人溺水？当然不是——背后藏着一个共同的原因：**气温**。天一热，冰淇淋卖得多，下水游泳的人也多、溺水自然多。是气温同时推高了两者，它俩之间并没有直接的因果关系。这就是数据分析最容易踩的坑：看到相关，就以为有因果。下面把隐藏的气温“控制住”，看那条相关性怎么大幅减弱。

<section class="cclab vizui" id="cclab">
  <p class="vizui__lead">每个点是某一天：横轴冰淇淋销量、纵轴溺水人数，颜色是当天气温（<span style="color:#2563eb">蓝=凉</span> → <span style="color:#b5524a">红=热</span>）。整体看是一条明显的上升趋势（强相关）。但把气温固定在某个范围内再看……</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <label style="display:inline-flex;align-items:center;gap:8px;cursor:pointer"><input type="checkbox" id="ctrl"> 只看某个气温范围（“控制”气温）</label>
      <span class="vizui-field" id="zf" style="display:none"><label for="z">气温</label><input type="range" id="z" min="0.1" max="0.9" step="0.02" value="0.5" style="width:130px"></span>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="rinfo">—</span>
    </div>
    <svg class="vizui-chart" id="plot" viewBox="0 0 360 300" style="max-width:420px;margin:0 auto" role="img" aria-label="相关与因果散点"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>共同原因 = 混淆变量</b><p>气温同时推高冰淇淋和溺水，制造出两者的假相关——它叫“混淆变量”。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>控制变量</b><p>把气温固定在一个小范围内再看，冰淇淋和溺水的相关就大幅减弱——说明并无直接因果。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>所以要小心</b><p>看到相关别急着下因果结论；要靠对照实验或控制混淆变量才能验证因果。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var data=[], ctrl=false, z0=0.5, BW=0.1;
function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
function gss(r){var u=0,v=0;while(!u)u=r();while(!v)v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}
(function(){var r=rng(7);for(var i=0;i<90;i++){var z=r();var x=0.22+0.62*z+gss(r)*0.06,y=0.2+0.66*z+gss(r)*0.06;data.push({x:x,y:y,z:z});}})();
function corr(pts){if(pts.length<3)return 0;var n=pts.length,mx=0,my=0;pts.forEach(function(p){mx+=p.x;my+=p.y;});mx/=n;my/=n;
  var sxy=0,sx=0,sy=0;pts.forEach(function(p){sxy+=(p.x-mx)*(p.y-my);sx+=(p.x-mx)*(p.x-mx);sy+=(p.y-my)*(p.y-my);});
  return sxy/(Math.sqrt(sx*sy)||1e-9);}
var SVGNS="http://www.w3.org/2000/svg",W=360,H=300,pad=30;
function wx(x){return pad+x*(W-2*pad);}
function wy(y){return (H-pad)-y*(H-2*pad);}
function zcol(z){var b=[37,99,235],r=[181,82,74];return "rgb("+Math.round(b[0]+(r[0]-b[0])*z)+","+Math.round(b[1]+(r[1]-b[1])*z)+","+Math.round(b[2]+(r[2]-b[2])*z)+")";}
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function trendline(svg,pts,cls){if(pts.length<3)return;var n=pts.length,mx=0,my=0;pts.forEach(function(p){mx+=p.x;my+=p.y;});mx/=n;my/=n;
  var sxy=0,sx=0;pts.forEach(function(p){sxy+=(p.x-mx)*(p.y-my);sx+=(p.x-mx)*(p.x-mx);});var b=sxy/(sx||1e-9),a=my-b*mx;
  var x0=0.1,x1=0.95;E(svg,"line",{x1:wx(x0),y1:wy(a+b*x0),x2:wx(x1),y2:wy(a+b*x1),"class":"trend "+cls});}
function draw(){
  var svg=document.getElementById("plot");while(svg.firstChild)svg.removeChild(svg.firstChild);
  E(svg,"line",{x1:pad,y1:H-pad,x2:W-12,y2:H-pad,"class":"axis"});E(svg,"line",{x1:pad,y1:12,x2:pad,y2:H-pad,"class":"axis"});
  E(svg,"text",{x:(W)/2,y:H-8,"text-anchor":"middle","class":"alab"}).textContent="冰淇淋销量 →";
  E(svg,"text",{x:14,y:H/2,"text-anchor":"middle","class":"alab",transform:"rotate(-90 14 "+H/2+")"}).textContent="溺水人数 →";
  var band=ctrl?data.filter(function(p){return Math.abs(p.z-z0)<BW;}):data;
  data.forEach(function(p){var inb=!ctrl||Math.abs(p.z-z0)<BW;E(svg,"circle",{cx:wx(p.x),cy:wy(p.y),r:5,fill:zcol(p.z),"class":"pt"+(inb?"":" dim")});});
  if(!ctrl)trendline(svg,data,"");else trendline(svg,band,"band");
  var rAll=corr(data),rBand=corr(band);
  document.getElementById("rinfo").textContent=ctrl?("固定气温后相关 r = "+rBand.toFixed(2)+"（"+band.length+" 天）"):("总体相关 r = "+rAll.toFixed(2));
  caption(rAll,rBand,band.length);
}
function caption(rAll,rBand,nb){
  var el=document.getElementById("caption");
  if(!ctrl)el.innerHTML="<b>总体相关 r = "+rAll.toFixed(2)+"</b>，很强——冰淇淋越多、溺水越多，一条清晰的上升趋势。勾上方框，把气温“控制”在一个小范围内再看。";
  else el.innerHTML="只看气温相近的那 "+nb+" 天（同色点），冰淇淋和溺水的相关掉到了 <b>r = "+rBand.toFixed(2)+"</b>——大幅减弱！原来那条强相关大半是<b>气温</b>这个共同原因造出来的假象，两者之间并没有直接因果。";
}
document.getElementById("ctrl").addEventListener("change",function(e){ctrl=e.target.checked;document.getElementById("zf").style.display=ctrl?"inline-flex":"none";draw();});
document.getElementById("z").addEventListener("input",function(e){z0=+e.target.value;draw();});
draw();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  setTimeout(function(){document.getElementById("ctrl").checked=true;ctrl=true;document.getElementById("zf").style.display="inline-flex";draw();
    var zs=[0.35,0.6,0.5],k=0,sl=document.getElementById("z");var iv=setInterval(function(){z0=zs[k];sl.value=z0;draw();k++;if(k>=zs.length)clearInterval(iv);},1100);},1500);},1000);
})();
</script>
{% endraw %}
