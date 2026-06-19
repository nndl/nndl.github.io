---
layout: default
title: 特征向量与特征值
permalink: /viz/eigenvectors/
redirect_from:
  - /v/eigenvectors/
---

{% raw %}
<style>
.eglab .grid{stroke:var(--color-border);stroke-width:1;opacity:.45;}
.eglab .axis{stroke:var(--color-text-muted);stroke-width:1.3;opacity:.7;}
.eglab .ellipse{fill:none;stroke:var(--color-text-muted);stroke-width:1.4;stroke-dasharray:4 4;opacity:.6;}
.eglab .eigline{stroke:var(--color-forest);stroke-width:1.6;stroke-dasharray:6 5;opacity:.5;}
.eglab .vv{stroke:var(--color-accent);stroke-width:3.4;}
.eglab .av{stroke:var(--color-gold);stroke-width:3.4;}
.eglab .avlock{stroke:var(--color-gold);stroke-width:6;}
.eglab svg{touch-action:none;cursor:crosshair;}
.eglab .heads{display:flex;flex-wrap:wrap;gap:6px;}
.eglab .heads button{appearance:none;font:inherit;font-size:.82rem;cursor:pointer;padding:6px 11px;border-radius:999px;border:1px solid var(--color-border);background:var(--color-bg-section);color:var(--color-text-soft);}
.eglab .heads button:hover{border-color:var(--color-accent);color:var(--color-accent);}
.eglab .heads button.on{border-color:var(--color-accent);background:var(--color-accent);color:#fff;}
.eglab .read{display:grid;grid-template-columns:1fr auto;gap:7px 16px;font-size:.92rem;margin-top:6px;}
.eglab .read .k{color:var(--color-text-muted);}
.eglab .read .v{font:600 1rem var(--font-mono);text-align:right;}
.eglab .matgrid{display:inline-grid;grid-template-columns:repeat(2,auto);gap:4px 18px;font:600 1.05rem var(--font-mono);padding:8px 16px;border-radius:var(--radius-md);background:var(--color-bg-section);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 特征向量与特征值

矩阵会把大多数向量“转向”——方向被掰歪。但每个矩阵都藏着几条特殊方向：向量落在这些方向上时，乘以矩阵后**只被拉长或缩短，方向纹丝不动**。这些方向叫**特征向量**，拉伸的倍数就是**特征值 λ**。满足 **Av = λv** 的，正是它们。PCA 找的主轴、谱分解、PageRank，乃至神经网络里对权重矩阵的分析，都从这里出发。**在平面里拖动鼠标**设置输入向量 v，看 Av 什么时候和 v 共线。

<section class="vizui eglab" id="eglab">
  <p class="vizui__lead">拖动设置 <span style="color:var(--color-accent);font-weight:600">青向量 v</span>，<span style="color:var(--color-gold);font-weight:600">金向量 Av</span> 是它经矩阵变换后的样子。淡虚线椭圆是 v 转一圈时 Av 划出的轨迹，两条<span style="color:var(--color-forest);font-weight:600">绿色虚线</span>是特征向量方向。当 v 压到绿线上，Av 就和 v 重合——只被拉伸。</p>

  <div class="vizui-grid2">
    <div class="vizui-panel">
      <svg class="vizui-chart" id="plane" viewBox="0 0 340 340" style="max-width:380px;margin:0 auto;display:block" role="img" aria-label="向量 v 与变换后的 Av"></svg>
    </div>
    <div class="vizui-panel">
      <p class="vizui-panel__title">对称矩阵 A</p>
      <div class="matgrid"><span id="ma">2.0</span><span id="mb">0.6</span><span id="mc">0.6</span><span id="md">1.0</span></div>
      <div class="read">
        <span class="k">特征值 λ₁ / λ₂</span><span class="v" id="lams">—</span>
        <span class="k">v 的方向角</span><span class="v" id="angv">—</span>
        <span class="k">Av 的方向角</span><span class="v" id="angav">—</span>
        <span class="k">沿 v 的拉伸 λ(v)</span><span class="v" id="rq">—</span>
      </div>
      <p class="vizui-panel__title" style="margin-top:14px">换一个对称矩阵</p>
      <div class="heads" id="heads"></div>
    </div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>多数方向被转向</b><p>随便挑一个 v，矩阵几乎都会把它掰到另一个方向——Av 和 v 不共线，夹角不为零。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>特征方向只拉伸不转向</b><p>沿特征向量方向，Av = λv：方向不变，只被缩放 λ 倍。这个 λ 就是特征值。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>对称矩阵→正交两轴</b><p>对称矩阵的特征值都是实数，两条特征轴互相垂直——这正是 PCA 主成分方向的根基。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var PRESETS=[
  ["拉伸",[2.0,0.6,0.6,1.0]],
  ["对角拉伸",[1.5,-0.7,-0.7,1.5]],
  ["轴向缩放",[1.0,0,0,0.5]]
];
var pi=0, A=PRESETS[0][1].slice();           /* a b c d : [[a,b],[c,d]] */
var v=[0.4,1.5], drag=false;
var SVGNS="http://www.w3.org/2000/svg",W=340,H=340,O=170,SC=38,RV=1.6;
function sx(x){return O+x*SC;} function sy(y){return O-y*SC;}
function E(p,t,at){var e=document.createElementNS(SVGNS,t);for(var k in at)e.setAttribute(k,at[k]);p.appendChild(e);return e;}
function mul(vx,vy){return [A[0]*vx+A[1]*vy, A[2]*vx+A[3]*vy];}
function eig(){
  var a=A[0],b=A[1],c=A[2],d=A[3],tr=a+d,det=a*d-b*c,disc=Math.max(0,tr*tr-4*det),s=Math.sqrt(disc);
  var l1=(tr+s)/2,l2=(tr-s)/2;
  function vecFor(l){var vv;
    if(Math.abs(b)>1e-9)vv=[b,l-a];
    else if(Math.abs(c)>1e-9)vv=[l-d,c];
    else vv=(Math.abs(l-a)<1e-9)?[1,0]:[0,1];
    var n=Math.hypot(vv[0],vv[1]);return [vv[0]/n,vv[1]/n];}
  return {l1:l1,l2:l2,e1:vecFor(l1),e2:vecFor(l2)};
}
function arrow(svg,vx,vy,cls){var x=sx(vx),y=sy(vy),an=Math.atan2(y-O,x-O),L=12;
  E(svg,"line",{x1:O,y1:O,x2:x,y2:y,"class":cls});
  E(svg,"line",{x1:x,y1:y,x2:x-L*Math.cos(an-0.4),y2:y-L*Math.sin(an-0.4),"class":cls});
  E(svg,"line",{x1:x,y1:y,x2:x-L*Math.cos(an+0.4),y2:y-L*Math.sin(an+0.4),"class":cls});}
function draw(eg,lock){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  for(var i=-4;i<=4;i++){E(svg,"line",{x1:sx(i),y1:sy(-4),x2:sx(i),y2:sy(4),"class":i?"grid":"axis"});E(svg,"line",{x1:sx(-4),y1:sy(i),x2:sx(4),y2:sy(i),"class":i?"grid":"axis"});}
  /* 特征向量方向线（贯穿全宽） */
  [eg.e1,eg.e2].forEach(function(e){E(svg,"line",{x1:sx(-4.4*e[0]),y1:sy(-4.4*e[1]),x2:sx(4.4*e[0]),y2:sy(4.4*e[1]),"class":"eigline"});});
  /* Av 在 v 扫单位圆（半径 RV）时划出的椭圆 */
  var pts="";for(var k=0;k<=64;k++){var th=k/64*2*Math.PI,p=mul(RV*Math.cos(th),RV*Math.sin(th));pts+=(k?" ":"")+sx(p[0])+","+sy(p[1]);}
  E(svg,"polyline",{points:pts,"class":"ellipse"});
  var av=mul(v[0],v[1]);
  arrow(svg,av[0],av[1],lock?"avlock":"av");
  arrow(svg,v[0],v[1],"vv");
  E(svg,"text",{x:sx(v[0])+9,y:sy(v[1])-6,style:"font:700 14px var(--font-mono);fill:var(--color-accent)"}).textContent="v";
  E(svg,"text",{x:sx(av[0])+9,y:sy(av[1])-6,style:"font:700 14px var(--font-mono);fill:var(--color-gold)"}).textContent="Av";
  if(lock){var bx=sx(av[0])-13,by=sy(av[1])+8;E(svg,"circle",{cx:bx,cy:by,r:9,fill:"var(--color-gold)"});
    E(svg,"text",{x:bx,y:by+4,"text-anchor":"middle",style:"font:700 12px var(--font-sans);fill:#fff"}).textContent="✓";}
}
function ang(x,y){var a=Math.atan2(y,x)*180/Math.PI;return a;}
function fmtAng(a){a=((a%360)+360)%360;return a.toFixed(0)+"°";}
function render(){
  var eg=eig(),av=mul(v[0],v[1]);
  var cross=v[0]*av[1]-v[1]*av[0];                 /* v × Av */
  var lv=Math.hypot(v[0],v[1]),lav=Math.hypot(av[0],av[1]);
  var sinth=(lv*lav>1e-9)?cross/(lv*lav):0;         /* sin(angle v→Av) */
  var lock=Math.abs(sinth)<0.04;
  var vAv=v[0]*av[0]+v[1]*av[1], vv=v[0]*v[0]+v[1]*v[1], rq=vv>1e-9?vAv/vv:0;
  document.getElementById("lams").textContent=eg.l1.toFixed(2)+" / "+eg.l2.toFixed(2);
  document.getElementById("angv").textContent=fmtAng(ang(v[0],v[1]));
  document.getElementById("angav").textContent=fmtAng(ang(av[0],av[1]));
  document.getElementById("rq").textContent="×"+rq.toFixed(2);
  draw(eg,lock);
  caption(lock,rq,sinth);
}
function caption(lock,rq,sinth){
  var el=document.getElementById("caption");
  if(lock){
    el.innerHTML="v <b>落在特征向量方向</b>：Av 与 v 共线，只被拉伸 λ≈<b>"+rq.toFixed(2)+"</b> 倍，方向没变——这就是 Av = λv。";
  }else{
    var th=Math.asin(Math.max(-1,Math.min(1,Math.abs(sinth))))*180/Math.PI;
    el.innerHTML="v 被 A <b>转了向</b>（与 Av 夹角约 "+th.toFixed(0)+"°）——这不是特征方向。把 v 慢慢转到绿色虚线上，看 Av 怎么和 v 重合。";
  }
}
var svg=document.getElementById("plane");
function toW(e){var r=svg.getBoundingClientRect();return [((e.clientX-r.left)/r.width*W-O)/SC, -((e.clientY-r.top)/r.height*H-O)/SC];}
function setV(w){
  var L=Math.hypot(w[0],w[1]);
  if(L<0.25){v=[0.25*(w[0]/(L||1)),0.25*(w[1]/(L||1))];}
  else if(L>2.6){v=[2.6*w[0]/L,2.6*w[1]/L];}        /* 控住 |v|，别冲出视野 */
  else v=[w[0],w[1]];
  var av=mul(v[0],v[1]),m=Math.max(Math.abs(av[0]),Math.abs(av[1]));
  if(m>4.1){var fr=4.1/m;v=[v[0]*fr,v[1]*fr];}       /* 同时控住 Av，别让它冲出视野 */
}
svg.addEventListener("pointerdown",function(e){drag=true;svg.setPointerCapture(e.pointerId);stopDemo();setV(toW(e));render();});
svg.addEventListener("pointermove",function(e){if(!drag)return;setV(toW(e));render();});
svg.addEventListener("pointerup",function(){drag=false;});
svg.addEventListener("pointercancel",function(){drag=false;});

function setMat(){var n=["ma","mb","mc","md"];for(var i=0;i<4;i++)document.getElementById(n[i]).textContent=A[i].toFixed(A[i]%1?1:1);}
(function(){var h=document.getElementById("heads");PRESETS.forEach(function(p,i){var b=document.createElement("button");b.type="button";b.textContent=p[0];if(i===0)b.className="on";b.addEventListener("click",function(){
  stopDemo();pi=i;A=p[1].slice();setMat();
  h.querySelectorAll("button").forEach(function(x){x.classList.remove("on");});b.classList.add("on");
  render();});h.appendChild(b);});})();

var demoIv=null;
function stopDemo(){if(demoIv){clearInterval(demoIv);demoIv=null;}}

setMat();render();
setTimeout(function(){
  var eg=eig();
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){
    v=[RV*eg.e1[0],RV*eg.e1[1]];render();return;   /* 直接落到第一条特征向量上，展示对齐态 */
  }
  var n=24,k=0,a0=Math.atan2(eg.e1[1],eg.e1[0]);   /* 锚到特征向量角，扫一圈会在步 0/6/12/18/24 正好压上两条特征轴 */
  demoIv=setInterval(function(){var th=a0+k/n*2*Math.PI;v=[RV*Math.cos(th),RV*Math.sin(th)];render();k++;if(k>n){stopDemo();}},170);
},900);
})();
</script>
{% endraw %}
