---
layout: default
title: 卷积核手动滑动
permalink: /viz/conv-kernel/
redirect_from:
  - /v/conv-kernel/
---

{% raw %}
<style>
.cklab .conv-row{display:flex;flex-wrap:wrap;gap:18px;align-items:center;justify-content:center;}
.cklab .grid{display:grid;gap:1px;background:var(--color-border);border:1px solid var(--color-border);border-radius:4px;}
.cklab .grid .c{width:var(--cs,20px);height:var(--cs,20px);}
.cklab .gwrap{text-align:center;}
.cklab .gwrap .lbl{font-size:.82rem;color:var(--color-text-muted);margin-bottom:6px;}
.cklab .win{box-shadow:inset 0 0 0 2px var(--color-accent);}
.cklab .ocur{box-shadow:inset 0 0 0 2px var(--color-gold);}
.cklab .kgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:2px;}
.cklab .kgrid .k{width:30px;height:30px;display:flex;align-items:center;justify-content:center;font:600 .8rem var(--font-mono);
  border-radius:4px;background:var(--color-bg-section);border:1px solid var(--color-border);color:var(--color-text-soft);}
.cklab .op{font-size:1.5rem;color:var(--color-text-muted);}
.cklab .kheads{display:flex;flex-wrap:wrap;gap:6px;}
.cklab .kheads button{appearance:none;font:inherit;font-size:.84rem;cursor:pointer;padding:6px 12px;border-radius:999px;border:1px solid var(--color-border);background:var(--color-bg-section);color:var(--color-text-soft);}
.cklab .kheads button.on{background:var(--color-bg-pure);color:var(--color-accent);font-weight:600;border-color:var(--color-accent);box-shadow:var(--shadow-sm);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 卷积核手动滑动

卷积神经网络靠“卷积核”看图——一个小小的方块（这里是 3×3）在图像上一格格滑过，每到一处就把覆盖的像素和核里的权重对应相乘再相加，得出一个数。不同的核找不同的东西：有的专挑边缘，有的专挑竖线、横线。换个核，看同一张图被“看”出完全不同的特征。

<section class="vizui cklab" id="cklab">
  <p class="vizui__lead">左边是原图（一个“十”字），中间是卷积核，右边是算出来的“特征图”：越亮表示这个核在该位置的响应越强。蓝框是当前滑动窗口，金框是它对应的输出格。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span style="font-size:.86rem;color:var(--color-text-muted)">选一个卷积核：</span>
      <span class="kheads" id="kheads"></span>
      <span class="vizui-spacer"></span>
      <button class="vizui-btn vizui-btn--go" id="go" type="button">▶ 自动滑动</button>
      <button class="vizui-btn" id="step" type="button">单步</button>
      <button class="vizui-btn" id="reset" type="button">重置</button>
    </div>
  </div>

  <div class="vizui-panel">
    <div class="conv-row">
      <div class="gwrap"><div class="lbl">原图 10×10</div><div class="grid" id="inGrid"></div></div>
      <div class="gwrap"><div class="lbl" id="kname">卷积核</div><div class="kgrid" id="kGrid"></div></div>
      <div class="op">→</div>
      <div class="gwrap"><div class="lbl">特征图 8×8</div><div class="grid" id="outGrid"></div></div>
    </div>
    <div id="calc" style="text-align:center;margin-top:12px;font:600 .9rem var(--font-mono);color:var(--color-text-soft)"></div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>核 = 一个小模式探测器</b><p>3×3 的权重决定它对什么敏感：边缘检测核在明暗交界处响应最大。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>滑动 = 处处都查一遍</b><p>同一个核滑遍全图，所以图里任何位置出现该模式都能被发现（平移不变）。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>多个核 = 多种特征</b><p>真实 CNN 一层有几十上百个核，各管一种模式；逐层叠加就能识别复杂物体。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var N=10, M=8;                       /* 原图 N×N，特征图 M×M（valid 卷积） */
var IMG=[]; for(var r=0;r<N;r++){IMG.push([]);for(var c=0;c<N;c++){var v=0.12;if(c===4||c===5)v=0.92;if(r===4||r===5)v=0.92;IMG[r].push(v);}}
var KERNELS=[
  {id:"edge",nm:"边缘检测",k:[[0,-1,0],[-1,4,-1],[0,-1,0]]},
  {id:"vert",nm:"竖线检测",k:[[1,0,-1],[2,0,-2],[1,0,-1]]},
  {id:"horiz",nm:"横线检测",k:[[1,2,1],[0,0,0],[-1,-2,-1]]},
  {id:"sharp",nm:"锐化",k:[[0,-1,0],[-1,5,-1],[0,-1,0]]},
  {id:"blur",nm:"模糊",k:[[1,1,1],[1,1,1],[1,1,1]].map(function(r){return r.map(function(v){return v/9;});})}
];
var ki=0, wr=0, wc=0, out=[], omax=1, playing=false, timer=null;

function conv(){
  var K=KERNELS[ki].k; out=[]; omax=1e-6;
  for(var i=0;i<M;i++){out.push([]);for(var j=0;j<M;j++){
    var s=0;for(var di=0;di<3;di++)for(var dj=0;dj<3;dj++)s+=IMG[i+di][j+dj]*K[di][dj];
    out[i].push(s); omax=Math.max(omax,Math.abs(s));
  }}
}
function gray(v){var g=Math.round(v*255);return "rgb("+g+","+g+","+g+")";}
function resp(v){var t=Math.min(1,Math.abs(v)/omax);var lo=[238,241,238],hi=[21,94,117];return "rgb("+Math.round(lo[0]+(hi[0]-lo[0])*t)+","+Math.round(lo[1]+(hi[1]-lo[1])*t)+","+Math.round(lo[2]+(hi[2]-lo[2])*t)+")";}

function buildGrids(){
  var ig=document.getElementById("inGrid"); ig.style.gridTemplateColumns="repeat("+N+",1fr)"; ig.style.setProperty("--cs","20px"); ig.innerHTML="";
  for(var r=0;r<N;r++)for(var c=0;c<N;c++){var d=document.createElement("div");d.className="c";d.dataset.r=r;d.dataset.c=c;d.style.background=gray(IMG[r][c]);ig.appendChild(d);}
  var og=document.getElementById("outGrid"); og.style.gridTemplateColumns="repeat("+M+",1fr)"; og.style.setProperty("--cs","23px"); og.innerHTML="";
  for(var i=0;i<M;i++)for(var j=0;j<M;j++){var o=document.createElement("div");o.className="c";o.dataset.i=i;o.dataset.j=j;og.appendChild(o);}
}
function buildKHeads(){
  var h=document.getElementById("kheads"); h.innerHTML="";
  KERNELS.forEach(function(K,idx){var b=document.createElement("button");b.type="button";b.textContent=K.nm;b.className=idx===ki?"on":"";b.dataset.i=idx;h.appendChild(b);});
}
function drawKernel(){
  var kg=document.getElementById("kGrid"); kg.innerHTML=""; var K=KERNELS[ki].k;
  for(var r=0;r<3;r++)for(var c=0;c<3;c++){var d=document.createElement("div");d.className="k";var v=K[r][c];d.textContent=(Math.round(v*100)/100);kg.appendChild(d);}
  document.getElementById("kname").textContent=KERNELS[ki].nm+" 核";
}
function render(){
  // 输出格颜色 + 揭示（已算到的位置）
  var revealed=wr*M+wc; var og=document.getElementById("outGrid").children;
  for(var i=0;i<M;i++)for(var j=0;j<M;j++){var cell=og[i*M+j];var idx=i*M+j;
    cell.style.background= idx<=revealed?resp(out[i][j]):"var(--color-bg-pure)";
    cell.classList.toggle("ocur",i===wr&&j===wc);
  }
  // 输入窗口高亮
  var ig=document.getElementById("inGrid").children;
  for(var r=0;r<N;r++)for(var c=0;c<N;c++){ig[r*N+c].classList.toggle("win",r>=wr&&r<wr+3&&c>=wc&&c<wc+3);}
  // 当前格计算
  var K=KERNELS[ki].k,s=0;for(var di=0;di<3;di++)for(var dj=0;dj<3;dj++)s+=IMG[wr+di][wc+dj]*K[di][dj];
  document.getElementById("calc").innerHTML="窗口 ("+(wr+1)+","+(wc+1)+") · Σ(像素 × 核) = <b style='color:var(--color-gold)'>"+s.toFixed(2)+"</b>";
  caption();
}
function caption(){
  var el=document.getElementById("caption"),id=KERNELS[ki].id;
  var txt={edge:"边缘检测核：在明暗交界（“十”字的边）响应最强，平坦区域几乎为零——特征图勾出了形状的轮廓。",
    vert:"竖线检测核：对竖直方向的明暗变化敏感，于是“十”字的竖杠边缘被点亮，横杠几乎没反应。",
    horiz:"横线检测核：只对水平方向的边缘敏感，点亮的是横杠的上下沿。和“竖线检测”正好互补。",
    sharp:"锐化核：放大中心、压低四周，让边缘更“跳”、细节更清楚。",
    blur:"模糊核：把每个像素换成周围 9 格的平均，图像被抹得柔和——这是去噪/降采样常用的一步。"};
  el.innerHTML="<b>"+KERNELS[ki].nm+"：</b>"+txt[id];
}

function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("go").textContent="▶ 自动滑动";}
function advance(){wc++;if(wc>=M){wc=0;wr++;}if(wr>=M){wr=M-1;wc=M-1;return false;}return true;}
function play(){if(wr===M-1&&wc===M-1){wr=0;wc=0;}stop();playing=true;document.getElementById("go").textContent="⏸ 暂停";
  timer=setInterval(function(){if(!advance()){stop();}render();},90);}
document.getElementById("go").addEventListener("click",function(){playing?stop():play();});
document.getElementById("step").addEventListener("click",function(){stop();advance();render();});
document.getElementById("reset").addEventListener("click",function(){stop();wr=0;wc=0;render();});
document.getElementById("kheads").addEventListener("click",function(e){var b=e.target.closest("button");if(!b)return;ki=+b.dataset.i;document.querySelectorAll("#kheads button").forEach(function(x,idx){x.classList.toggle("on",idx===ki);});conv();drawKernel();wr=0;wc=0;render();});

/* 启动 */
buildKHeads();buildGrids();drawKernel();conv();
wr=M-1;wc=M-1;render();        /* 初始整张特征图先显示出来 */
setTimeout(function(){
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  wr=0;wc=0;play();
},900);
})();
</script>
{% endraw %}
