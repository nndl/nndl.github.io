---
layout: default
title: 点积与余弦相似度
description: "拖两个向量，看点积=投影对齐、余弦相似度=夹角——注意力和向量检索的根基。"
permalink: /viz/dot-product/
redirect_from:
  - /v/dot-product/
---

{% raw %}
<style>
.dplab .axis{stroke:var(--color-border);stroke-width:1;}
.dplab .grid{stroke:var(--color-border);stroke-width:1;opacity:.4;}
.dplab .va{stroke:var(--color-accent);stroke-width:3.4;}
.dplab .vb{stroke:var(--color-gold);stroke-width:3.4;}
.dplab .proj{stroke:var(--color-accent);stroke-width:2;stroke-dasharray:4 3;opacity:.7;}
.dplab .projseg{stroke:var(--color-accent);stroke-width:6;opacity:.28;}
.dplab .arc{fill:none;stroke:var(--color-text-muted);stroke-width:1.6;}
.dplab .handle{fill:#fff;stroke-width:2.5;cursor:grab;}
.dplab svg{touch-action:none;}
.dplab .read{display:grid;grid-template-columns:1fr 1fr;gap:8px 18px;font-size:.92rem;}
.dplab .read .k{color:var(--color-text-muted);}
.dplab .read .v{font:600 1rem var(--font-mono);text-align:right;}
.dplab .big{font:700 1.6rem var(--font-mono);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 点积与余弦相似度

两个向量“像不像”，怎么用一个数衡量？答案是**点积**：把对应分量相乘再相加。它有个漂亮的几何含义——等于一个向量在另一个向量上的“投影”长度乘以另一个的长度。方向越一致，点积越大；垂直时为零；反向时为负。再除掉长度的影响，就得到只看夹角的**余弦相似度**。注意力分数、向量检索、推荐系统，背后都是它。**拖动两个箭头**试试。

<section class="vizui dplab" id="dplab">
  <p class="vizui__lead">拖动 <span style="color:var(--color-accent);font-weight:600">蓝向量 a</span> 和 <span style="color:var(--color-gold);font-weight:600">金向量 b</span> 的端点。淡蓝粗线是 a 在 b 上的投影。看右边的点积和余弦怎么随夹角变。</p>

  <div class="vizui-grid2">
    <div class="vizui-panel">
      <svg class="vizui-chart" id="plane" viewBox="0 0 320 320" style="max-width:360px;margin:0 auto;display:block" role="img" aria-label="两个向量与夹角"></svg>
    </div>
    <div class="vizui-panel">
      <div style="text-align:center;margin-bottom:6px">点积 a·b = <span class="big" id="dot" style="color:var(--color-accent)">—</span></div>
      <div class="read">
        <span class="k">余弦相似度 cos θ</span><span class="v" id="cos">—</span>
        <span class="k">夹角 θ</span><span class="v" id="ang">—</span>
        <span class="k">|a|（长度）</span><span class="v" id="la">—</span>
        <span class="k">|b|（长度）</span><span class="v" id="lb">—</span>
      </div>
      <div style="margin-top:14px;padding:10px 12px;border-radius:var(--radius-md);background:var(--color-bg-section);font-size:.85rem;color:var(--color-text-soft)">
        a·b = |a|·|b|·cos θ　＝　投影长度 × |b|
      </div>
    </div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-forest)"><b>同向 → 大正数</b><p>方向一致，点积最大（=两长度相乘），余弦接近 +1，最“相似”。</p></div>
    <div class="card" style="--wc:var(--color-text-muted)"><b>垂直 → 零</b><p>互相垂直时点积为 0，余弦为 0，互不相关。</p></div>
    <div class="card" style="--wc:#b5524a"><b>反向 → 负数</b><p>方向相反，点积为负，余弦接近 −1，最“不相似”。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var a=[2.0,0.9], b=[1.3,1.9], XR=3, drag=-1;
var SVGNS="http://www.w3.org/2000/svg",W=320,H=320,O=160,SC=42;
function sx(x){return O+x*SC;} function sy(y){return O-y*SC;}
function E(p,t,at){var e=document.createElementNS(SVGNS,t);for(var k in at)e.setAttribute(k,at[k]);p.appendChild(e);return e;}
function arrow(svg,v,cls){var x=sx(v[0]),y=sy(v[1]),an=Math.atan2(y-O,x-O),L=11;
  E(svg,"line",{x1:O,y1:O,x2:x,y2:y,"class":cls});
  E(svg,"line",{x1:x,y1:y,x2:x-L*Math.cos(an-0.4),y2:y-L*Math.sin(an-0.4),"class":cls});
  E(svg,"line",{x1:x,y1:y,x2:x-L*Math.cos(an+0.4),y2:y-L*Math.sin(an+0.4),"class":cls});}
function draw(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  for(var i=-3;i<=3;i++){E(svg,"line",{x1:sx(i),y1:sy(-3),x2:sx(i),y2:sy(3),"class":i?"grid":"axis"});E(svg,"line",{x1:sx(-3),y1:sy(i),x2:sx(3),y2:sy(i),"class":i?"grid":"axis"});}
  var lb=Math.hypot(b[0],b[1]), dot=a[0]*b[0]+a[1]*b[1];
  // a 在 b 上的投影
  if(lb>1e-3){var f=dot/(lb*lb),px=f*b[0],py=f*b[1];
    E(svg,"line",{x1:sx(0),y1:sy(0),x2:sx(px),y2:sy(py),"class":"projseg"});
    E(svg,"line",{x1:sx(a[0]),y1:sy(a[1]),x2:sx(px),y2:sy(py),"class":"proj"});}
  // 夹角弧
  var aa=Math.atan2(a[1],a[0]),ab=Math.atan2(b[1],b[0]),R=30;
  E(svg,"path",{d:"M"+(O+R*Math.cos(aa))+","+(O-R*Math.sin(aa))+" A"+R+","+R+" 0 0 "+(((ab-aa+2*Math.PI)%(2*Math.PI))>Math.PI?1:0)+" "+(O+R*Math.cos(ab))+","+(O-R*Math.sin(ab)),"class":"arc"});
  arrow(svg,b,"vb"); arrow(svg,a,"va");
  E(svg,"circle",{cx:sx(a[0]),cy:sy(a[1]),r:7,"class":"handle",stroke:"#155e75","data-i":0});
  E(svg,"circle",{cx:sx(b[0]),cy:sy(b[1]),r:7,"class":"handle",stroke:"#b7791f","data-i":1});
  E(svg,"text",{x:sx(a[0])+10,y:sy(a[1])-6,style:"font:700 14px var(--font-mono);fill:#155e75"}).textContent="a";
  E(svg,"text",{x:sx(b[0])+10,y:sy(b[1])-6,style:"font:700 14px var(--font-mono);fill:#b7791f"}).textContent="b";
}
function render(){
  var dot=a[0]*b[0]+a[1]*b[1], la=Math.hypot(a[0],a[1]), lb=Math.hypot(b[0],b[1]);
  var cos=(la*lb>1e-6)?dot/(la*lb):0, ang=Math.acos(Math.max(-1,Math.min(1,cos)))*180/Math.PI;
  document.getElementById("dot").textContent=dot.toFixed(2);
  document.getElementById("dot").style.color=dot>0.05?"var(--color-forest)":dot<-0.05?"#b5524a":"var(--color-text-muted)";
  document.getElementById("cos").textContent=cos.toFixed(2);
  document.getElementById("ang").textContent=ang.toFixed(0)+"°";
  document.getElementById("la").textContent=la.toFixed(2);
  document.getElementById("lb").textContent=lb.toFixed(2);
  draw();caption(dot,ang);
}
function caption(dot,ang){
  var el=document.getElementById("caption"),m;
  if(ang<35)m="两个向量<b>方向相近</b>（夹角 "+ang.toFixed(0)+"°），点积是较大的正数、余弦接近 1——很“相似”。";
  else if(ang>145)m="两个向量<b>几乎反向</b>（夹角 "+ang.toFixed(0)+"°），点积为负、余弦接近 −1——最“不相似”。";
  else if(Math.abs(ang-90)<12)m="两个向量<b>接近垂直</b>（夹角 "+ang.toFixed(0)+"°），点积接近 0——互不相关。";
  else m="夹角 "+ang.toFixed(0)+"°，点积 "+dot.toFixed(2)+"。把 a 转到和 b 同向看点积最大，转到垂直看它归零，转到反向看它变负。";
  el.innerHTML=m;
}
var svg=document.getElementById("plane");
function toW(e){var r=svg.getBoundingClientRect();return [((e.clientX-r.left)/r.width*W-O)/SC, -((e.clientY-r.top)/r.height*H-O)/SC];}
svg.addEventListener("pointerdown",function(e){var t=e.target;if(t.classList&&t.classList.contains("handle")){drag=+t.getAttribute("data-i");svg.setPointerCapture(e.pointerId);}});
svg.addEventListener("pointermove",function(e){if(drag<0)return;var w=toW(e),v=[Math.max(-XR,Math.min(XR,w[0])),Math.max(-XR,Math.min(XR,w[1]))];if(drag===0)a=v;else b=v;render();});
svg.addEventListener("pointerup",function(){drag=-1;});svg.addEventListener("pointercancel",function(){drag=-1;});
render();
setTimeout(function(){
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  var k=0;var iv=setInterval(function(){k++;var th=k*0.5;a=[2.2*Math.cos(th),2.2*Math.sin(th)];render();if(k>=13)clearInterval(iv);},420);
},1000);
})();
</script>
{% endraw %}
