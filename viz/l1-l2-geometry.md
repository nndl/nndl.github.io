---
layout: default
title: L1 与 L2 的几何（为什么 L1 稀疏）
permalink: /viz/l1-l2-geometry/
redirect_from:
  - /v/l1-l2-geometry/
---

{% raw %}
<style>
.glab .axis{stroke:var(--color-border-strong);stroke-width:1.2;}
.glab .grid{stroke:var(--color-border);stroke-width:1;opacity:.35;}
.glab .ell{fill:none;stroke:var(--color-accent);stroke-width:1.6;opacity:.32;}
.glab .ellhit{fill:none;stroke:var(--color-accent);stroke-width:2.4;opacity:.7;}
.glab .region{fill:#2563eb;fill-opacity:.10;stroke:#2563eb;stroke-width:2.4;stroke-linejoin:round;}
.glab .star{fill:var(--color-gold);stroke:#fff;stroke-width:1;}
.glab .sol{fill:#b5524a;stroke:#fff;stroke-width:1.6;}
.glab .drop{stroke:#b5524a;stroke-width:1.6;stroke-dasharray:4 3;opacity:.85;}
.glab .lbl{font:600 13px var(--font-mono);}
.glab .heads{display:inline-flex;gap:4px;padding:4px;background:var(--color-bg-section);border:1px solid var(--color-border);border-radius:999px;}
.glab .heads button{appearance:none;border:0;background:transparent;cursor:pointer;font:inherit;font-size:.88rem;color:var(--color-text-soft);padding:6px 14px;border-radius:999px;}
.glab .heads button.on{background:var(--color-bg-pure);color:var(--color-accent);font-weight:600;box-shadow:var(--shadow-sm);}
.glab svg{touch-action:none;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# L1 与 L2 的几何（为什么 L1 稀疏）

[正则化那一页](../regularization/)告诉你 L1 会把一些权重压成 0、L2 不会——那是“结果”。这一页讲“为什么”，用几何就能看明白。把两个权重 w₁、w₂ 当成平面上的坐标：损失画成一圈圈套着的**椭圆等高线**，圆心是不加约束时的最优解 w\*（一个偏离坐标轴的固定点）。正则化等价于把解**限制在一个区域里**——L2 是个**圆**，L1 是个**菱形**。带约束的解，就是这个区域上“损失最小”的那一点，也就是**最小的椭圆第一次碰到区域边界**的地方。菱形有四个**尖角**正好顶在坐标轴上，椭圆几乎总是先碰到尖角——那里有一个坐标恰好是 0，于是“稀疏”。圆没有尖角，碰到的是一段光滑弧，两个坐标都不为 0、只是一起缩小。**拖动预算 t，切换 L1 / L2**，看解落在哪。

<section class="vizui glab" id="glab">
  <p class="vizui__lead">金色五角星是不受约束的最优解 <span style="color:var(--color-gold);font-weight:600">w*</span>，蓝色区域是约束（圆=L2，菱形=L1），<span style="color:#b5524a;font-weight:600">红点</span>是受约束的解。看 L1 时红点怎么顶在菱形的尖角上、把一个权重压成 0。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="heads" id="heads"><button data-m="l1" class="on" type="button">L1（菱形）</button><button data-m="l2" type="button">L2（圆）</button></span>
      <span class="vizui-field"><label for="bud">预算 t（越小、正则越强）</label><input type="range" id="bud" min="0.40" max="1.60" step="0.01" value="0.90" style="width:170px"><output id="budVal"></output></span>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="info">—</span>
    </div>
    <svg class="vizui-chart" id="plane" viewBox="-20 -52 388 392" style="max-width:430px;margin:0 auto;display:block" role="img" aria-label="权重空间里的损失椭圆与约束区域"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>L2 = 圆</b><p>约束区域是圆，没有尖角。最小的椭圆碰到的是一段光滑圆弧，切点处两个坐标一般都不为 0——所有权重一起被缩小，但很少正好等于 0。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>L1 = 菱形</b><p>约束区域是菱形，四个尖角正好落在坐标轴上。椭圆几乎总是先顶到尖角，而尖角上有一个坐标恰好是 0——这就是某个权重被精确压成 0 的几何原因。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>所以 L1 做特征选择</b><p>解顶在尖角上 → 一批权重精确归零 → 对应特征被自动剔除。L1 因此天然产生稀疏解、自动挑特征；L2 只缩不删。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var CX=1.30, CY=0.55, A=2.2, B=0.7;        /* 损失 L(w)=A(w1-CX)^2+B(w2-CY)^2，圆心 w*=(CX,CY) */
var mode="l1", t=0.90;
function L(w1,w2){return A*(w1-CX)*(w1-CX)+B*(w2-CY)*(w2-CY);}

/* 数值求带约束最优：若 w* 已在区域内则解=w*，否则在边界上密集采样取损失最小点 */
function solve(){
  if(mode==="l2"){
    if(Math.hypot(CX,CY)<=t) return {w:[CX,CY],inside:true};
    var best=null,N=900,i,th,w1,w2,v;
    for(i=0;i<N;i++){th=2*Math.PI*i/N;w1=t*Math.cos(th);w2=t*Math.sin(th);v=L(w1,w2);
      if(!best||v<best.v)best={w:[w1,w2],v:v};}
    return {w:best.w,inside:false};
  }else{
    if(Math.abs(CX)+Math.abs(CY)<=t) return {w:[CX,CY],inside:true};
    var V=[[t,0],[0,t],[-t,0],[0,-t]],bb=null,e,k,s,a,c,p1,p2,vv;
    for(e=0;e<4;e++){a=V[e];c=V[(e+1)%4];
      for(k=0;k<=200;k++){s=k/200;p1=a[0]+(c[0]-a[0])*s;p2=a[1]+(c[1]-a[1])*s;vv=L(p1,p2);
        if(!bb||vv<bb.v)bb={w:[p1,p2],v:vv};}}
    return {w:bb.w,inside:false};
  }
}

var SVGNS="http://www.w3.org/2000/svg",W=360,H=320,O1=110,O2=160,SC=78;  /* 原点偏左下，留出 w* 与右上尖角的余量 */
function sx(x){return O1+x*SC;} function sy(y){return O2-y*SC;}
function E(p,tg,at){var e=document.createElementNS(SVGNS,tg);for(var k in at)e.setAttribute(k,at[k]);p.appendChild(e);return e;}

function ellipse(svg,Lv,cls){
  /* 等高线 A(w1-CX)^2+B(w2-CY)^2=Lv：参数方程画一圈 */
  var pts=[],i,th,w1,w2;
  for(i=0;i<=72;i++){th=2*Math.PI*i/72;
    w1=CX+Math.sqrt(Lv/A)*Math.cos(th);
    w2=CY+Math.sqrt(Lv/B)*Math.sin(th);
    pts.push(sx(w1).toFixed(1)+","+sy(w2).toFixed(1));}
  E(svg,"polyline",{points:pts.join(" "),"class":cls});
}

function draw(sol){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var g;
  for(g=-1;g<=2;g++){E(svg,"line",{x1:sx(g),y1:sy(-1.6),x2:sx(g),y2:sy(2.4),"class":g?"grid":"axis"});}
  for(g=-1;g<=2;g++){E(svg,"line",{x1:sx(-1.6),y1:sy(g),x2:sx(2.4),y2:sy(g),"class":g?"grid":"axis"});}
  /* 几圈淡椭圆 + 一圈穿过解的高亮椭圆 */
  var Lhit=L(sol.w[0],sol.w[1]);
  [Lhit*1.6,Lhit*1.3,Lhit*1.1].forEach(function(lv){if(lv>1e-4)ellipse(svg,lv,"ell");});
  if(Lhit>1e-4)ellipse(svg,Lhit,"ellhit");
  /* 约束区域 */
  if(mode==="l2"){E(svg,"circle",{cx:sx(0),cy:sy(0),r:t*SC,"class":"region"});}
  else{E(svg,"polygon",{points:[sx(t)+","+sy(0),sx(0)+","+sy(t),sx(-t)+","+sy(0),sx(0)+","+sy(-t)].join(" "),"class":"region"});}
  /* w* 五角星 */
  star(svg,sx(CX),sy(CY),7.5);
  E(svg,"text",{x:sx(CX)+11,y:sy(CY)-7,"class":"lbl",fill:"var(--color-gold-strong,#b7791f)"}).textContent="w*";
  /* 解 + 坐标轴标签 */
  var px=sx(sol.w[0]),py=sy(sol.w[1]),z1=Math.abs(sol.w[0])<0.03,z2=Math.abs(sol.w[1])<0.03;
  if(z2){E(svg,"line",{x1:px,y1:py,x2:px,y2:sy(0),"class":"drop"});}
  if(z1){E(svg,"line",{x1:px,y1:py,x2:sx(0),y2:py,"class":"drop"});}
  E(svg,"circle",{cx:px,cy:py,r:6,"class":"sol"});
  if(z2)E(svg,"text",{x:px+9,y:py-8,"class":"lbl",fill:"#b5524a"}).textContent="w₂ = 0 → 稀疏";
  else if(z1)E(svg,"text",{x:px+9,y:py-8,"class":"lbl",fill:"#b5524a"}).textContent="w₁ = 0 → 稀疏";
  else E(svg,"text",{x:px+9,y:py-8,"class":"lbl",fill:"#b5524a"}).textContent="解";
  /* 轴名 */
  E(svg,"text",{x:sx(2.4)+2,y:sy(0)+4,style:"font:600 11px var(--font-mono);fill:var(--color-text-muted)"}).textContent="w₁";
  E(svg,"text",{x:sx(0)+6,y:sy(2.4)-2,style:"font:600 11px var(--font-mono);fill:var(--color-text-muted)"}).textContent="w₂";
}
function star(svg,cx,cy,r){
  var p=[],i,a,rr;for(i=0;i<10;i++){a=-Math.PI/2+i*Math.PI/5;rr=(i%2?r*0.42:r);p.push((cx+rr*Math.cos(a)).toFixed(1)+","+(cy+rr*Math.sin(a)).toFixed(1));}
  E(svg,"polygon",{points:p.join(" "),"class":"star"});
}

function render(){
  document.getElementById("budVal").textContent=t.toFixed(2);
  var sol=solve();
  draw(sol);
  var w1=sol.w[0],w2=sol.w[1];
  var nz=(Math.abs(w1)>0.03?1:0)+(Math.abs(w2)>0.03?1:0);
  document.getElementById("info").textContent=(mode==="l1"?nz+" / 2 个权重非零":"两个权重都非零");
  caption(sol);
}

function caption(sol){
  var el=document.getElementById("caption"),w1=sol.w[0],w2=sol.w[1];
  var z1=Math.abs(w1)<0.03,z2=Math.abs(w2)<0.03;
  var c="(w₁, w₂) = ("+w1.toFixed(2)+", "+w2.toFixed(2)+")";
  if(sol.inside){
    el.innerHTML="预算 t = "+t.toFixed(2)+" 已经大到把 w* 包进了区域里，约束不起作用，解就是无约束最优 <b>"+c+"</b>。把 t 调小让约束“咬”住解。";
  }else if(mode==="l1"){
    if(z2)el.innerHTML="<b>L1（菱形）：</b>解 <b>"+c+"</b> 正好顶在菱形右边那个<b>尖角</b>上——尖角落在 w₁ 轴上，所以 <b>w₂ 被精确压成 0</b>，这就是稀疏。";
    else if(z1)el.innerHTML="<b>L1（菱形）：</b>解 <b>"+c+"</b> 顶在菱形上方的<b>尖角</b>上，尖角在 w₂ 轴上，所以 <b>w₁ 被精确压成 0</b>——稀疏。";
    else el.innerHTML="<b>L1（菱形）：</b>此时解 <b>"+c+"</b> 落在菱形的一条边上、还没顶到尖角。把 t 调小一点，看它顺着边滑下去、<b>突然吸附到尖角</b>（一个权重归 0）。";
  }else{
    el.innerHTML="<b>L2（圆）：</b>解 <b>"+c+"</b> 落在圆的一段<b>光滑弧</b>上，<b>两个权重都不为 0</b>，只是被一起缩小了。圆没有尖角，所以很难恰好把某个权重压成 0。";
  }
}

document.getElementById("heads").addEventListener("click",function(e){var b=e.target.closest("button");if(!b)return;clearAuto();mode=b.dataset.m;document.querySelectorAll("#heads button").forEach(function(x){x.classList.toggle("on",x.dataset.m===mode);});render();});
document.getElementById("bud").addEventListener("input",function(e){clearAuto();t=+e.target.value;render();});

var autoIv=null;
function clearAuto(){if(autoIv){clearInterval(autoIv);autoIv=null;}}

render();

setTimeout(function(){
  var sl=document.getElementById("bud");
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){
    mode="l1";t=0.90;sl.value="0.90";
    document.querySelectorAll("#heads button").forEach(function(x){x.classList.toggle("on",x.dataset.m==="l1");});
    render();return;
  }
  /* L1：t 从大（解在边上）扫到小（吸附到尖角 w=0） */
  mode="l1";document.querySelectorAll("#heads button").forEach(function(x){x.classList.toggle("on",x.dataset.m==="l1");});
  var seq=[1.55,1.45,1.32,1.20,1.12,1.05,0.95,0.85],n=0;
  autoIv=setInterval(function(){
    t=seq[n];sl.value=t.toFixed(2);render();n++;
    if(n>=seq.length){clearInterval(autoIv);autoIv=null;}
  },820);
},900);
})();
</script>
{% endraw %}
