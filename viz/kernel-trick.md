---
layout: default
title: 核技巧
permalink: /viz/kernel-trick/
redirect_from:
  - /v/kernel-trick/
---

{% raw %}
<style>
.ktlab .axis{stroke:var(--color-border);stroke-width:1;}
.ktlab .pa{fill:var(--color-accent-light);}
.ktlab .pb{fill:#b5524a;}
.ktlab .sep{stroke:var(--color-forest);stroke-width:2.4;stroke-dasharray:6 4;}
.ktlab .badline{stroke:var(--color-text-muted);stroke-width:2;stroke-dasharray:4 4;opacity:.6;}
.ktlab .lbl{font:11px var(--font-mono);fill:var(--color-text-muted);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 核技巧

有些数据天生用一条直线分不开——比如一圈套一圈：内圈一类、外圈一类，怎么画线都会有错。核技巧的妙招是：**升一个维度**。给每个点加一个新坐标 z = x² + y²（到中心的距离平方），原本平铺的点就被“抬”成一个碗形——内圈在碗底、外圈在碗壁高处，这时一个水平面（在二维里看就是一条线）轻轻松松把两类切开。支持向量机就是靠这招处理弯弯绕绕的数据。拖动“升维”看碗怎么长出来。

<section class="ktlab vizui" id="ktlab">
  <p class="vizui__lead">左边是原始二维数据：<span style="color:var(--color-accent-light);font-weight:600">蓝=内圈</span>、<span style="color:#b5524a;font-weight:600">红=外圈</span>，一条直线分不开。右边给每个点加上高度 z=x²+y²，拖动滑块把它“抬”起来——抬够了，一条水平线就能分开。</p>

  <div class="vizui-grid2">
    <div class="vizui-panel">
      <p class="vizui-panel__title">原始二维（线性不可分）</p>
      <svg class="vizui-chart" id="flat" viewBox="0 0 280 280" style="max-width:300px;margin:0 auto;display:block" role="img" aria-label="二维同心环数据"></svg>
    </div>
    <div class="vizui-panel">
      <p class="vizui-panel__title">升维后：高度 = x² + y²</p>
      <svg class="vizui-chart" id="lift" viewBox="0 0 280 280" style="max-width:300px;margin:0 auto;display:block" role="img" aria-label="升维后侧视图"></svg>
      <div class="vizui-field" style="justify-content:center;margin-top:8px"><label for="t">升维</label><input type="range" id="t" min="0" max="1" step="0.02" value="0" style="width:160px"><output id="tVal">0%</output></div>
    </div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:#b5524a"><b>低维分不开</b><p>同心环这种数据，在原始平面里没有任何直线能把两类分到两边。</p></div>
    <div class="card" style="--wc:var(--color-accent)"><b>升维变可分</b><p>加一个合适的新特征（这里是到中心的距离），数据在更高维里被一个平面切开。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>核技巧</b><p>SVM 不必真的把坐标算出来，用“核函数”就能等效地在高维里找这个分界面，又快又省。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var lift=0, A=[], B=[];
function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
(function gen(){var r=rng(6);A=[];B=[];
  for(var i=0;i<22;i++){var a=r()*2*Math.PI,rr=0.45+r()*0.5;A.push([rr*Math.cos(a),rr*Math.sin(a)]);}
  for(var j=0;j<26;j++){var a2=r()*2*Math.PI,r2=1.7+r()*0.55;B.push([r2*Math.cos(a2),r2*Math.sin(a2)]);}})();
var SVGNS="http://www.w3.org/2000/svg";
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function drawFlat(){
  var svg=document.getElementById("flat"),O=140,SC=44;while(svg.firstChild)svg.removeChild(svg.firstChild);
  E(svg,"line",{x1:O,y1:14,x2:O,y2:266,"class":"axis"});E(svg,"line",{x1:14,y1:O,x2:266,y2:O,"class":"axis"});
  // 随便一条注定失败的直线
  E(svg,"line",{x1:30,y1:90,x2:250,y2:200,"class":"badline"});
  E(svg,"text",{x:140,y:24,"text-anchor":"middle","class":"lbl"}).textContent="任何直线都会分错";
  B.forEach(function(p){E(svg,"circle",{cx:O+p[0]*SC,cy:O-p[1]*SC,r:4.5,"class":"pb"});});
  A.forEach(function(p){E(svg,"circle",{cx:O+p[0]*SC,cy:O-p[1]*SC,r:4.5,"class":"pa"});});
}
function drawLift(){
  var svg=document.getElementById("lift");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var padL=24,padB=24,Wp=280,Hp=280,zmax=6;
  function px(x){return padL+(x+2.6)/5.2*(Wp-padL-14);}
  function py(z){return (Hp-padB)-(z/zmax)*(Hp-padB-16);}
  E(svg,"line",{x1:padL,y1:Hp-padB,x2:Wp-14,y2:Hp-padB,"class":"axis"});
  E(svg,"line",{x1:padL,y1:14,x2:padL,y2:Hp-padB,"class":"axis"});
  E(svg,"text",{x:padL-4,y:20,"text-anchor":"end","class":"lbl"}).textContent="z";
  E(svg,"text",{x:Wp-14,y:Hp-padB+16,"text-anchor":"end","class":"lbl"}).textContent="x";
  // 分界水平线（升够了才显含义）
  if(lift>0.55){E(svg,"line",{x1:padL,y1:py(1.6*lift),x2:Wp-14,y2:py(1.6*lift),"class":"sep"});
    E(svg,"text",{x:Wp-16,y:py(1.6*lift)-5,"text-anchor":"end","class":"lbl",style:"fill:var(--color-forest)"}).textContent="一条线分开了";}
  function pt(p,cls){var z=(p[0]*p[0]+p[1]*p[1])*lift;E(svg,"circle",{cx:px(p[0]),cy:py(z),r:4.5,"class":cls});}
  B.forEach(function(p){pt(p,"pb");});A.forEach(function(p){pt(p,"pa");});
}
function render(){document.getElementById("tVal").textContent=Math.round(lift*100)+"%";drawFlat();drawLift();caption();}
function caption(){
  var el=document.getElementById("caption");
  if(lift<0.1)el.innerHTML="此刻两类还压在同一条线上（z=0），和左边一样分不开。往右拖“升维”。";
  else if(lift<0.9)el.innerHTML="正在升维（"+Math.round(lift*100)+"%）：每个点按 z=x²+y² 往上抬，内圈点离中心近、抬得低，外圈点抬得高，两类开始分层。";
  else el.innerHTML="升满了：内圈在碗底、外圈在碗壁，<b>一条水平线（绿色虚线）干净地把两类分开</b>。这就是核技巧——在更高维里，弯弯绕绕的数据变得线性可分。";
}
document.getElementById("t").addEventListener("input",function(e){lift=+e.target.value;render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){lift=1;render();return;}
  var k=0,sl=document.getElementById("t");var iv=setInterval(function(){k++;lift=Math.min(1,k/26);sl.value=lift;render();if(lift>=1)clearInterval(iv);},90);},1000);
})();
</script>
{% endraw %}
