---
layout: default
title: 扩散模型：加噪与去噪
permalink: /viz/diffusion-noise/
redirect_from:
  - /v/diffusion-noise/
---

{% raw %}
<style>
.dflab .dot{fill:var(--color-accent);}
.dflab svg{background:#0e1b22;border-radius:var(--radius-sm);}
.dflab .tlbl{font:11px var(--font-mono);fill:#9fb6bf;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 扩散模型：加噪与去噪

扩散模型（像 Stable Diffusion）画图的思路出奇地巧。**第一步好懂**：拿一张清晰的图，一点点往上加噪声，加够多步，它就变成一团纯噪声——这叫``前向加噪''，规则固定、谁都会。**真正学的是反过来**：训练一个模型，让它看着一团噪声，一步步把噪声去掉、还原出图来。学会了``去噪'',从纯噪声出发就能生成全新的图。拖动下面的滑块，看一颗``心''怎样被打成噪声、又怎样被还原。

<section class="vizui dflab" id="dflab">
  <p class="vizui__lead">滑块从左到右 = 时间往前 = 噪声越来越多。``加噪''是固定规则；``去噪''是扩散模型真正学到的本事（这里因为知道原图所以能精确还原，真实模型则是<b>估计</b>每一步该去掉多少噪声）。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="t">噪声程度（时间 t）</label>
        <input type="range" id="t" min="0" max="1" step="0.01" value="0" style="width:220px">
        <output id="tVal">0%</output>
      </span>
      <span class="vizui-spacer"></span>
      <button class="vizui-btn" id="fwd" type="button">▶ 加噪</button>
      <button class="vizui-btn vizui-btn--go" id="rev" type="button">▶ 去噪还原</button>
      <button class="vizui-btn" id="shape" type="button">↻ 换形状</button>
    </div>
  </div>

  <div class="vizui-panel">
    <div class="vizui-bar" style="justify-content:center">
      <svg class="vizui-chart" id="plane" viewBox="0 0 320 320" style="max-width:380px;margin:0 auto" role="img" aria-label="扩散加噪去噪点云"></svg>
    </div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>前向：加噪（固定）</b><p>每步加一点高斯噪声，足够多步后图像彻底变成噪声。规则写死，不用学。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>反向：去噪（要学）</b><p>训练模型预测``这一步混进了多少噪声'',减掉它，一步步把图还原出来。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>生成新图</b><p>学会去噪后，随便给一团噪声，反复去噪，就能``无中生有''画出全新的图。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var s=0, shapeId=0, shape=[], eps=[], playing=null, timer=null;
function rng(sd){return function(){sd|=0;sd=sd+0x6D2B79F5|0;var x=Math.imul(sd^sd>>>15,1|sd);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
function gauss(r){var u=0,v=0;while(!u)u=r();while(!v)v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}

function heartPts(n){var p=[];for(var i=0;i<n;i++){var t=i/n*2*Math.PI;p.push([16*Math.pow(Math.sin(t),3),13*Math.cos(t)-5*Math.cos(2*t)-2*Math.cos(3*t)-Math.cos(4*t)]);}return p;}
function starPts(n){var p=[];for(var i=0;i<n;i++){var t=i/n*2*Math.PI,k=Math.floor(i/(n/10))%2?0.45:1;p.push([k*Math.cos(t-Math.PI/2),k*Math.sin(t-Math.PI/2)]);}return p;}
function smileyPts(){var p=[],i;for(i=0;i<70;i++){var t=i/70*2*Math.PI;p.push([Math.cos(t),Math.sin(t)]);}            /* 脸 */
  for(i=0;i<30;i++){var a=Math.PI*(0.15+0.7*i/30);p.push([0.55*Math.cos(-a),0.55*Math.sin(-a)-0.05]);}              /* 嘴 */
  p.push([-0.38,0.35]);p.push([0.38,0.35]);                                                                        /* 眼 */
  return p;}
function loadShape(){
  var raw=shapeId===0?heartPts(150):shapeId===1?starPts(150):smileyPts();
  // 归一化到 [-0.9,0.9]
  var xs=raw.map(function(p){return p[0];}),ys=raw.map(function(p){return p[1];});
  var minx=Math.min.apply(null,xs),maxx=Math.max.apply(null,xs),miny=Math.min.apply(null,ys),maxy=Math.max.apply(null,ys);
  var sc=1.8/Math.max(maxx-minx,maxy-miny), cx=(minx+maxx)/2, cy=(miny+maxy)/2;
  shape=raw.map(function(p){return [(p[0]-cx)*sc,(p[1]-cy)*sc];});
  var r=rng(99+shapeId); eps=shape.map(function(){return [gauss(r)*0.62,gauss(r)*0.62];});
}

var SVGNS="http://www.w3.org/2000/svg",W=320,H=320,pad=14;
function wx(x){return W/2+x*(W/2-pad);} function wy(y){return H/2-y*(H/2-pad);}
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function draw(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var a=Math.sqrt(1-s), b=Math.sqrt(s);
  shape.forEach(function(p,i){var x=a*p[0]+b*eps[i][0], y=a*p[1]+b*eps[i][1];
    E(svg,"circle",{cx:wx(x),cy:wy(y),r:2.6,"class":"dot",opacity:(0.5+0.5*a).toFixed(2)});});
  E(svg,"text",{x:10,y:H-10,"class":"tlbl"}).textContent="t = "+Math.round(s*100)+"%　"+(s<0.02?"原图":s>0.97?"纯噪声":"加噪中");
}
function caption(){
  var el=document.getElementById("caption");
  if(s<0.03)el.innerHTML="<b>t=0：</b>这是清晰的原图（点云）。往右拖滑块，给它一步步加噪声。";
  else if(s>0.95)el.innerHTML="<b>t=100%：</b>形状已经被噪声彻底淹没，变成一团随机点。扩散模型训练时见过无数这样的``噪声↔图''配对。";
  else el.innerHTML="<b>t="+Math.round(s*100)+"%：</b>"+(playing==="rev"?"正在去噪——噪声一步步被减掉，心形重新浮现。这就是扩散模型学到的本事。":"噪声越来越多，形状逐渐模糊。这一步规则是固定的，不用学。");
}
function render(){document.getElementById("tVal").textContent=Math.round(s*100)+"%";document.getElementById("t").value=s;draw();caption();}

function stop(){if(timer){clearInterval(timer);timer=null;}playing=null;}
function animate(dir){stop();playing=dir;
  timer=setInterval(function(){s+=dir==="fwd"?0.025:-0.025;if(s>=1){s=1;stop();}else if(s<=0){s=0;stop();}render();},60);}
document.getElementById("t").addEventListener("input",function(e){stop();s=+e.target.value;render();});
document.getElementById("fwd").addEventListener("click",function(){if(s>=1)s=0;animate("fwd");});
document.getElementById("rev").addEventListener("click",function(){if(s<=0)s=1;render();animate("rev");});
document.getElementById("shape").addEventListener("click",function(){stop();shapeId=(shapeId+1)%3;loadShape();s=0;render();});

loadShape();render();
setTimeout(function(){
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){s=0.5;render();return;}
  s=0;animate("fwd");
  setTimeout(function(){s=1;animate("rev");},3200);
},900);
})();
</script>
{% endraw %}
