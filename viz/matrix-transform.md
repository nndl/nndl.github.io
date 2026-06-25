---
layout: default
title: 矩阵是空间变换
description: "拖动 2×2 矩阵的四个数，看整个平面被旋转/缩放/剪切；列是基向量去向，行列式是面积缩放。"
permalink: /viz/matrix-transform/
redirect_from:
  - /v/matrix-transform/
---

{% raw %}
<style>
.mxlab .grid0{stroke:var(--color-border);stroke-width:1;opacity:.5;}
.mxlab .gridT{stroke:#bcd3d6;stroke-width:1;}
.mxlab .axisT{stroke:var(--color-text-muted);stroke-width:1.4;}
.mxlab .shape{fill:var(--color-accent);opacity:.16;stroke:var(--color-accent);stroke-width:2;stroke-linejoin:round;}
.mxlab .mat{display:grid;grid-template-columns:repeat(2,1fr);gap:10px 16px;max-width:300px;}
.mxlab .cell{display:flex;flex-direction:column;gap:3px;}
.mxlab .cell label{font-size:.78rem;color:var(--color-text-muted);}
.mxlab .cell .v{font:600 1rem var(--font-mono);}
.mxlab .heads{display:flex;flex-wrap:wrap;gap:6px;}
.mxlab .heads button{appearance:none;font:inherit;font-size:.82rem;cursor:pointer;padding:6px 11px;border-radius:999px;border:1px solid var(--color-border);background:var(--color-bg-section);color:var(--color-text-soft);}
.mxlab .heads button:hover{border-color:var(--color-accent);color:var(--color-accent);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 矩阵是空间变换

矩阵看着像一堆数字，其实它是对整个空间的一次“拉扯”——旋转、缩放、剪切、翻转，都能用一个 2×2 矩阵表示。神经网络每一层做的“乘以权重矩阵”，本质就是把数据所在的空间变换一下。秘密很简洁：矩阵的两列，正是两个基向量 **î、ĵ** 变换后的落点；行列式则是面积被放大了多少倍。拖动四个数，看网格和图形怎么变。

<section class="vizui mxlab" id="mxlab">
  <p class="vizui__lead">浅色是原始网格，深色是被矩阵变换后的网格。<span style="color:var(--color-accent);font-weight:600">青箭头 î</span> 是 (1,0) 的去向，<span style="color:var(--color-gold);font-weight:600">金箭头 ĵ</span> 是 (0,1) 的去向——它们正好是矩阵的两列。</p>

  <div class="vizui-grid2">
    <div class="vizui-panel">
      <svg class="vizui-chart" id="plane" viewBox="0 0 320 320" style="max-width:360px;margin:0 auto;display:block" role="img" aria-label="矩阵变换后的平面"></svg>
    </div>
    <div class="vizui-panel">
      <p class="vizui-panel__title">变换矩阵</p>
      <div class="mat" id="mat"></div>
      <div style="margin:14px 0 10px;font:600 .95rem var(--font-mono);color:var(--color-text)">行列式 det = <span id="det" style="color:var(--color-accent)">1.00</span>　<span style="font-family:var(--font-sans);font-weight:400;color:var(--color-text-muted)" id="detNote">面积不变</span></div>
      <p class="vizui-panel__title" style="margin-top:8px">试试这些变换</p>
      <div class="heads" id="heads"></div>
    </div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>列 = 基向量去向</b><p>第一列是 (1,0) 变到哪、第二列是 (0,1) 变到哪。知道这两个，整个变换就定了。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>行列式 = 面积缩放</b><p>|det| 是面积放大倍数；det 为负表示空间被翻了面（镜像）；det=0 表示被压扁成一条线。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>神经网络的一层</b><p>“乘权重矩阵”就是这样变换数据空间，再配上激活函数掰弯，层层叠出复杂映射。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var M=[1,0,0,1];   /* a b c d : [[a,b],[c,d]] */
var PRESETS=[["单位",[1,0,0,1]],["旋转90°",[0,-1,1,0]],["旋转45°",[0.71,-0.71,0.71,0.71]],["放大1.5×",[1.5,0,0,1.5]],["剪切",[1,0.8,0,1]],["水平翻转",[-1,0,0,1]],["压扁",[1,0.5,0.6,0.3]]];
var SVGNS="http://www.w3.org/2000/svg",W=320,H=320,O=160,SC=40;
function tx(x,y){return [M[0]*x+M[1]*y, M[2]*x+M[3]*y];}
function sx(x){return O+x*SC;} function sy(y){return O-y*SC;}
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function arrow(svg,vx,vy,col){var x=sx(vx),y=sy(vy),a=Math.atan2(y-O,x-O),L=11;
  E(svg,"line",{x1:O,y1:O,x2:x,y2:y,stroke:col,"stroke-width":3.2,"stroke-linecap":"round"});
  E(svg,"line",{x1:x,y1:y,x2:x-L*Math.cos(a-0.4),y2:y-L*Math.sin(a-0.4),stroke:col,"stroke-width":3.2,"stroke-linecap":"round"});
  E(svg,"line",{x1:x,y1:y,x2:x-L*Math.cos(a+0.4),y2:y-L*Math.sin(a+0.4),stroke:col,"stroke-width":3.2,"stroke-linecap":"round"});}
var SHAPE=[[0,0],[1.4,0],[1.4,0.45],[0.5,0.45],[0.5,1],[1.1,1],[1.1,1.45],[0.5,1.45],[0.5,2],[0,2]]; /* 字母 F，便于看旋转/翻转 */

function draw(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  // 原始网格（浅）
  for(var i=-3;i<=3;i++){E(svg,"line",{x1:sx(i),y1:sy(-3.4),x2:sx(i),y2:sy(3.4),"class":"grid0"});E(svg,"line",{x1:sx(-3.4),y1:sy(i),x2:sx(3.4),y2:sy(i),"class":"grid0"});}
  // 变换后网格（深）
  for(var j=-3;j<=3;j++){
    var a1=tx(j,-3.4),a2=tx(j,3.4),b1=tx(-3.4,j),b2=tx(3.4,j);
    E(svg,"line",{x1:sx(a1[0]),y1:sy(a1[1]),x2:sx(a2[0]),y2:sy(a2[1]),"class":(j===0?"axisT":"gridT")});
    E(svg,"line",{x1:sx(b1[0]),y1:sy(b1[1]),x2:sx(b2[0]),y2:sy(b2[1]),"class":(j===0?"axisT":"gridT")});
  }
  // 图形
  var pts=SHAPE.map(function(p){var t=tx(p[0],p[1]);return sx(t[0])+","+sy(t[1]);});
  E(svg,"polygon",{points:pts.join(" "),"class":"shape"});
  // 基向量
  arrow(svg,M[0],M[2],"#155e75");   // î = 第一列
  arrow(svg,M[1],M[3],"#b7791f");   // ĵ = 第二列
}
function buildMat(){
  var host=document.getElementById("mat");host.innerHTML="";
  var labs=["a（î.x）","b（ĵ.x）","c（î.y）","d（ĵ.y）"];
  [0,1,2,3].forEach(function(i){
    var c=document.createElement("div");c.className="cell";
    c.innerHTML='<label>'+labs[i]+'</label><input type="range" min="-2" max="2" step="0.1" value="'+M[i]+'" data-i="'+i+'"><span class="v" id="mv'+i+'">'+M[i].toFixed(1)+'</span>';
    host.appendChild(c);
  });
  host.querySelectorAll("input").forEach(function(inp){inp.addEventListener("input",function(e){M[+e.target.dataset.i]=+e.target.value;render();});});
}
function render(){
  for(var i=0;i<4;i++){var v=document.getElementById("mv"+i);if(v)v.textContent=M[i].toFixed(1);var inp=document.querySelector('#mat input[data-i="'+i+'"]');if(inp&&+inp.value!==M[i])inp.value=M[i];}
  var det=M[0]*M[3]-M[1]*M[2];
  document.getElementById("det").textContent=det.toFixed(2);
  document.getElementById("detNote").textContent=Math.abs(det)<0.05?"压扁成一条线（不可逆）":det<0?"面积×"+Math.abs(det).toFixed(2)+"，且翻了面（镜像）":(Math.abs(det-1)<0.02?"面积不变":"面积×"+det.toFixed(2));
  draw();caption(det);
}
function caption(det){
  document.getElementById("caption").innerHTML="当前矩阵把 î 送到 ("+M[0].toFixed(1)+", "+M[2].toFixed(1)+")、把 ĵ 送到 ("+M[1].toFixed(1)+", "+M[3].toFixed(1)+")。整张网格随之"+(Math.abs(det)<0.05?"被压扁——信息丢失、不可逆":det<0?"翻了个面（镜像）":"被拉扯")+"，面积变为原来的 "+Math.abs(det).toFixed(2)+" 倍。";
}
(function(){var h=document.getElementById("heads");PRESETS.forEach(function(p){var b=document.createElement("button");b.type="button";b.textContent=p[0];b.addEventListener("click",function(){M=p[1].slice();buildMat();render();});h.appendChild(b);});})();
buildMat();render();
setTimeout(function(){
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  var seq=[1,4,2,5,3,0],k=0;var iv=setInterval(function(){M=PRESETS[seq[k]][1].slice();buildMat();render();k++;if(k>=seq.length)clearInterval(iv);},1300);
},1000);
})();
</script>
{% endraw %}
