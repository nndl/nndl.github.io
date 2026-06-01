---
layout: default
title: 双下降现象
permalink: /viz/double-descent/
redirect_from:
  - /v/double-descent/
---

{% raw %}
<style>
.ddlab svg{max-width:100%;height:auto;}
.ddlab .axis{stroke:var(--color-border-strong);stroke-width:1;}
.ddlab .alab{font:11px var(--font-sans);fill:var(--color-text-muted);}
.ddlab .train{fill:none;stroke:var(--color-accent-light,#2563eb);stroke-width:2.5;}
.ddlab .test{fill:none;stroke:#b5524a;stroke-width:2.5;}
.ddlab .thr{stroke:var(--color-gold);stroke-width:2;stroke-dasharray:5 3;}
.ddlab .now{stroke:var(--color-text);stroke-width:1.5;stroke-dasharray:3 3;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 双下降现象

经典理论说：模型越复杂，测试误差先降后升（偏差-方差权衡的 U 形曲线），所以别把模型做得太大。但深度学习时代发现了一件怪事——当模型继续变大、大到**参数比数据还多**之后，测试误差竟然**第二次下降**，甚至比之前的最低点还低！整条曲线长这样：降→升→**再降**。中间那个鼓包，正好出现在“参数量≈数据量”、模型刚好能把训练数据背得一字不差的地方。这就是**双下降**，它解释了为什么如今的超大模型“越大越好”，挑战了教科书的经典直觉。拖动“模型大小”，走一遍这条反常的曲线。

<section class="vizui ddlab" id="ddlab">
  <p class="vizui__lead"><span style="color:var(--color-accent-light,#2563eb)">蓝线</span>是训练误差（越大越能背，到阈值后≈0），<span style="color:#b5524a">红线</span>是测试误差。<b>金色虚线</b>是“插值阈值”（参数≈数据量）——鼓包就在这里。注意红线最右端比中间的经典最低点还低。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="c">模型大小</label><input type="range" id="c" min="0" max="99" step="1" value="0" style="width:200px"></span>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stat">—</span>
    </div>
    <svg id="plane" viewBox="0 0 460 280" role="img" aria-label="双下降曲线"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent-light,#2563eb)"><b>经典 U（左半）</b><p>欠参数区：太小欠拟合、稍大刚好、再大方差变大——传统的偏差方差权衡。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>插值阈值（鼓包）</b><p>参数≈数据量，模型勉强背下全部数据，最不稳定，测试误差冲到峰值。</p></div>
    <div class="card" style="--wc:#b5524a"><b>第二次下降（右半）</b><p>过参数区：参数远超数据，反而找到更平滑的解，测试误差再降、常低于经典最优。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var G=100,thr=0.45;
function base(c){return 0.09+0.50*Math.exp(-c*6);}
function spike(c){return 0.42*Math.exp(-Math.pow((c-thr)/0.045,2));}
function testE(c){return base(c)+spike(c);}
function trainE(c){return c<thr?0.55*Math.pow(1-c/thr,1.5):0.012;}
var cs=[];for(var g=0;g<G;g++)cs.push(g/(G-1));
var classicMin=9,cmC=0;cs.forEach(function(c){if(c<thr-0.05){var t=testE(c);if(t<classicMin){classicMin=t;cmC=c;}}});
var finalE=testE(1),peakE=testE(thr);
var cur=0,SVGNS="http://www.w3.org/2000/svg",W=460,H=280,pl=38,pr=16,pt=14,pb=30,YMAX=0.72;
function px(c){return pl+c*(W-pl-pr);}function py(v){return (H-pb)-(v/YMAX)*(H-pt-pb);}
function E(p,t,a,txt){var x=document.createElementNS(SVGNS,t);for(var k in a)x.setAttribute(k,a[k]);if(txt!=null)x.textContent=txt;p.appendChild(x);return x;}
function poly(svg,fn,cls){var pts=cs.map(function(c){return px(c)+","+py(fn(c));});E(svg,"polyline",{points:pts.join(" "),"class":cls});}
function render(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  E(svg,"line",{x1:px(thr),y1:pt,x2:px(thr),y2:H-pb,"class":"thr"});
  E(svg,"text",{x:px(thr),y:pt-2,"text-anchor":"middle","class":"alab",style:"fill:var(--color-gold);font-weight:600"},"插值阈值");
  E(svg,"line",{x1:pl,y1:H-pb,x2:W-pr,y2:H-pb,"class":"axis"});E(svg,"line",{x1:pl,y1:pt,x2:pl,y2:H-pb,"class":"axis"});
  E(svg,"text",{x:W/2,y:H-6,"text-anchor":"middle","class":"alab"},"模型大小（参数量）→");
  E(svg,"text",{x:12,y:H/2,"text-anchor":"middle","class":"alab",transform:"rotate(-90 12 "+H/2+")"},"误差");
  poly(svg,trainE,"train");poly(svg,testE,"test");
  var c=cs[cur];
  E(svg,"line",{x1:px(c),y1:pt,x2:px(c),y2:H-pb,"class":"now"});
  E(svg,"circle",{cx:px(c),cy:py(testE(c)),r:4,fill:"#b5524a",stroke:"#fff"});
  E(svg,"circle",{cx:px(c),cy:py(trainE(c)),r:4,fill:"var(--color-accent-light,#2563eb)",stroke:"#fff"});
  document.getElementById("stat").textContent="测试误差 "+testE(c).toFixed(2);
  caption(c);
}
function caption(c){
  var el=document.getElementById("caption");
  if(c<cmC+0.02)el.innerHTML="<b>欠参数区：</b>模型还小，正走经典 U 形——测试误差先降到一个最低点（约 "+classicMin.toFixed(2)+"）。教科书说该停在这附近。";
  else if(c<thr+0.06)el.innerHTML="<b>插值阈值附近：</b>参数快≈数据量，模型勉强能背下全部训练数据，最不稳定，测试误差冲到峰值（约 "+peakE.toFixed(2)+"）。经典理论到此为止。";
  else el.innerHTML="<b>过参数区：</b>参数远超数据，测试误差<b>第二次下降</b>，最右端约 "+finalE.toFixed(2)+"——比经典最低点 "+classicMin.toFixed(2)+" 还低！这就是双下降，也是大模型“越大越好”的底气。";
}
document.getElementById("c").addEventListener("input",function(e){cur=+e.target.value;render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){cur=99;document.getElementById("c").value=99;render();return;}
  var sl=document.getElementById("c");var iv=setInterval(function(){cur+=2;if(cur>=99){cur=99;clearInterval(iv);}sl.value=cur;render();},110);},900);
})();
</script>
{% endraw %}
