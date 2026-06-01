---
layout: default
title: 激活函数与梯度消失
permalink: /viz/activations/
redirect_from:
  - /v/activations/
---

{% raw %}
<style>
.aclab .heads{display:inline-flex;gap:4px;padding:4px;background:var(--color-bg-section);border:1px solid var(--color-border);border-radius:999px;}
.aclab .heads button{appearance:none;border:0;background:transparent;cursor:pointer;font:inherit;font-size:.9rem;color:var(--color-text-soft);padding:7px 16px;border-radius:999px;}
.aclab .heads button.on{background:var(--color-bg-pure);color:var(--color-accent);font-weight:600;box-shadow:var(--shadow-sm);}
.aclab .axis{stroke:var(--color-border);stroke-width:1;}
.aclab .alab{font:11px var(--font-mono);fill:var(--color-text-muted);}
.aclab .fcurve{fill:none;stroke:var(--color-accent);stroke-width:2.6;}
.aclab .dcurve{fill:none;stroke:var(--color-gold);stroke-width:2.4;stroke-dasharray:5 4;}
.aclab .xline{stroke:var(--color-text-muted);stroke-width:1.2;stroke-dasharray:3 3;}
.aclab .fdot{fill:var(--color-accent);stroke:#fff;stroke-width:1.5;}
.aclab .ddot{fill:var(--color-gold);stroke:#fff;stroke-width:1.5;}
.aclab .layers{display:flex;gap:3px;align-items:flex-end;height:60px;margin:8px 0;}
.aclab .layers .lb{flex:1;background:var(--color-accent);border-radius:3px 3px 0 0;min-height:1px;transition:height .3s var(--ease-out),background .2s;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 激活函数与梯度消失

神经元在把信号往下传之前，会先过一道“激活函数”掰个弯。常见的有 Sigmoid、Tanh、ReLU。它们长相差不多，但有个要命的区别藏在“导数”里——而导数决定了训练时梯度能不能顺利地一层层往回传。这就是为什么深层网络早年那么难训，以及 ReLU 后来为什么一统天下。

<section class="vizui aclab" id="aclab">
  <p class="vizui__lead">蓝线是激活函数本身，金色虚线是它的导数。拖动下面的 x，看某一点的函数值和导数；再看“梯度连乘”那栏——导数小于 1，多乘几层就趋近于零。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="heads" id="heads" role="group" aria-label="激活函数">
        <button data-f="sigmoid" class="on" type="button">Sigmoid</button>
        <button data-f="tanh" type="button">Tanh</button>
        <button data-f="relu" type="button">ReLU</button>
      </span>
      <span class="vizui-spacer"></span>
      <span class="vizui-field"><label for="x0">取值点 x</label>
        <input type="range" id="x0" min="-5" max="5" step="0.1" value="2" style="width:170px">
        <output id="x0Val">2.0</output>
      </span>
    </div>
  </div>

  <div class="vizui-grid2">
    <div class="vizui-panel">
      <p class="vizui-panel__title">函数与导数</p>
      <div class="vizui-legend">
        <span><i style="background:var(--color-accent)"></i>函数 f(x)</span>
        <span><i style="background:var(--color-gold)"></i>导数 f′(x)</span>
      </div>
      <svg class="vizui-chart" id="plot" viewBox="0 0 360 240" role="img" aria-label="激活函数及其导数"></svg>
      <div id="vals" style="text-align:center;font:600 .9rem var(--font-mono);color:var(--color-text-soft)"></div>
    </div>
    <div class="vizui-panel">
      <p class="vizui-panel__title">梯度连乘 · 一层层往回传</p>
      <div class="vizui-bar" style="margin-bottom:8px">
        <span class="vizui-field"><label for="depth">网络深度</label>
          <input type="range" id="depth" min="1" max="16" step="1" value="10" style="width:150px">
          <output id="depthVal">10</output> 层</span>
      </div>
      <div class="layers" id="layers"></div>
      <div id="remain" style="font:600 .92rem var(--font-mono);color:var(--color-text);text-align:center;margin-top:4px"></div>
    </div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:#b5524a"><b>Sigmoid / Tanh 会饱和</b><p>两端又平又缓，导数趋近 0。多层连乘后梯度几乎消失，深层网络学不动。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>ReLU 不消失</b><p>正半轴导数恒为 1，梯度原样传下去——这是它成为深度网络默认激活函数的关键。</p></div>
    <div class="card" style="--wc:var(--color-text-muted)"><b>代价</b><p>ReLU 负半轴导数为 0，神经元可能“死掉”;于是有了 LeakyReLU、GELU 等改进。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var FN={
  sigmoid:{f:function(x){return 1/(1+Math.exp(-x));},d:function(x){var s=1/(1+Math.exp(-x));return s*(1-s);},nm:"Sigmoid"},
  tanh:{f:function(x){return Math.tanh(x);},d:function(x){var t=Math.tanh(x);return 1-t*t;},nm:"Tanh"},
  relu:{f:function(x){return Math.max(0,x);},d:function(x){return x>0?1:0;},nm:"ReLU"}
};
var cur="sigmoid", x0=2, depth=10;
var XMIN=-5,XMAX=5,YMIN=-1.2,YMAX=1.6;

var SVGNS="http://www.w3.org/2000/svg",W=360,H=240,pad=22;
function wx(x){return pad+(x-XMIN)/(XMAX-XMIN)*(W-2*pad);}
function wy(y){return (H-pad)-(y-YMIN)/(YMAX-YMIN)*(H-2*pad);}
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function curve(svg,fn,cls){var p=[];for(var i=0;i<=120;i++){var x=XMIN+(XMAX-XMIN)*i/120,y=Math.max(YMIN-0.3,Math.min(YMAX+0.3,fn(x)));p.push(wx(x)+","+wy(y));}E(svg,"polyline",{points:p.join(" "),"class":cls,"clip-path":"url(#aclip)"});}

function drawPlot(){
  var svg=document.getElementById("plot"); while(svg.firstChild)svg.removeChild(svg.firstChild);
  var clip=E(svg,"clipPath",{id:"aclip"});E(clip,"rect",{x:pad-2,y:2,width:W-2*pad+4,height:H-4});
  E(svg,"line",{x1:pad,y1:wy(0),x2:W-pad,y2:wy(0),"class":"axis"});
  E(svg,"line",{x1:wx(0),y1:pad-6,x2:wx(0),y2:H-pad,"class":"axis"});
  var F=FN[cur];
  curve(svg,F.f,"fcurve"); curve(svg,F.d,"dcurve");
  E(svg,"line",{x1:wx(x0),y1:pad-6,x2:wx(x0),y2:H-pad,"class":"xline"});
  E(svg,"circle",{cx:wx(x0),cy:wy(Math.min(YMAX,F.f(x0))),r:5,"class":"fdot"});
  E(svg,"circle",{cx:wx(x0),cy:wy(F.d(x0)),r:5,"class":"ddot"});
  document.getElementById("vals").innerHTML="f("+x0.toFixed(1)+") = "+F.f(x0).toFixed(3)+" 　 f′("+x0.toFixed(1)+") = <span style='color:var(--color-gold)'>"+F.d(x0).toFixed(3)+"</span>";
}
function drawLayers(){
  var host=document.getElementById("layers"); host.innerHTML="";
  var d=FN[cur].d(x0), prod=1;
  for(var i=0;i<depth;i++){
    prod*=d;
    var bar=document.createElement("div"); bar.className="lb";
    bar.style.height=Math.max(1,prod*100).toFixed(1)+"%";
    bar.style.background=prod<0.05?"#b5524a":(prod<0.4?"var(--color-gold)":"var(--color-forest)");
    bar.title="第 "+(i+1)+" 层后：×"+prod.toExponential(2);
    host.appendChild(bar);
  }
  var rem=Math.pow(d,depth);
  document.getElementById("remain").innerHTML="经过 "+depth+" 层，梯度信号约剩 <b>"+(rem<0.001?rem.toExponential(1):(rem*100).toFixed(1)+"%")+"</b>";
}
function caption(){
  var el=document.getElementById("caption"),d=FN[cur].d(x0),rem=Math.pow(d,depth);
  var msg;
  if(cur==="relu"){
    if(x0>0)msg="<b>ReLU：</b>x>0 处导数恒为 <b>1</b>，"+depth+" 层连乘还是 1——梯度原样传到底，不会消失。这就是 ReLU 的杀手锏。";
    else msg="<b>ReLU：</b>x<0 处导数为 <b>0</b>，梯度被掐断，这个神经元“死”了。把 x 拖到正半轴看对比。";
  }else if(cur==="sigmoid"){
    msg="<b>Sigmoid：</b>导数最大也只有 0.25，在 x="+x0.toFixed(1)+" 处更是只有 <b>"+d.toFixed(3)+"</b>。每层乘一次，"+depth+" 层后只剩 <b>"+(rem<0.001?rem.toExponential(1):(rem*100).toFixed(1)+"%")+"</b>——这就是梯度消失。";
  }else{
    msg="<b>Tanh：</b>导数在 0 处最大为 1，但两端同样饱和趋零（此处 "+d.toFixed(3)+"）。比 Sigmoid 好些，深层仍可能消失。";
  }
  el.innerHTML=msg;
}
function render(){document.getElementById("x0Val").textContent=x0.toFixed(1);document.getElementById("depthVal").textContent=depth;drawPlot();drawLayers();caption();}

document.getElementById("heads").addEventListener("click",function(e){var b=e.target.closest("button");if(!b)return;cur=b.dataset.f;document.querySelectorAll("#heads button").forEach(function(x){x.classList.toggle("on",x.dataset.f===cur);});render();});
document.getElementById("x0").addEventListener("input",function(e){x0=+e.target.value;render();});
document.getElementById("depth").addEventListener("input",function(e){depth=+e.target.value;render();});

/* 启动 + 自动演示：把 x 从 0 拖到饱和区，展示导数变小 */
render();
setTimeout(function(){
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  var seq=[0,1,2,3,4,2],k=0,sl=document.getElementById("x0");
  var iv=setInterval(function(){if(k>=seq.length){clearInterval(iv);return;}x0=seq[k];sl.value=x0;render();k++;},700);
},900);
})();
</script>
{% endraw %}
