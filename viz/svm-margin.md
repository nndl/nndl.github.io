---
layout: default
title: SVM 最大间隔
permalink: /viz/svm-margin/
redirect_from:
  - /v/svm-margin/
---

{% raw %}
<style>
.svlab .axis{stroke:var(--color-border);stroke-width:1;}
.svlab .street{stroke:var(--color-accent);opacity:.12;stroke-linecap:butt;}
.svlab .decline{stroke:var(--color-text);stroke-width:2.4;}
.svlab .margin{stroke:var(--color-accent);stroke-width:1.4;stroke-dasharray:5 4;opacity:.8;}
.svlab .pt{stroke:#fff;stroke-width:1.5;cursor:grab;}
.svlab .pt.pos{fill:var(--color-accent-light);}
.svlab .pt.neg{fill:#b5524a;}
.svlab .sv{stroke:var(--color-gold);stroke-width:3;}
.svlab svg{touch-action:none;}
.svlab .pen{display:inline-flex;gap:4px;padding:4px;background:var(--color-bg-section);border:1px solid var(--color-border);border-radius:999px;}
.svlab .pen button{appearance:none;border:0;background:transparent;cursor:pointer;font:inherit;font-size:.84rem;color:var(--color-text-soft);padding:6px 12px;border-radius:999px;}
.svlab .pen button.on{background:var(--color-bg-pure);font-weight:600;box-shadow:var(--shadow-sm);}
.svlab .pen button[data-c="1"].on{color:var(--color-accent-light);}
.svlab .pen button[data-c="-1"].on{color:#b5524a;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# SVM 最大间隔

能把两类点分开的直线有无数条，哪条最好？支持向量机（SVM）的回答很有道理：选那条让两边“留白”最宽的——就像在两群点之间修一条尽量宽的马路，分界线走在马路正中央。决定这条路有多宽的，只是离得最近的那几个点，叫“支持向量”。**拖动任意一个点**，看分界线和马路怎样跟着变。

<section class="vizui svlab" id="svlab">
  <p class="vizui__lead">黑线是分界线，两条虚线之间的淡蓝“马路”就是间隔。带金圈的是支持向量——只有它们顶着马路边，其余点远离、对结果没有影响。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <button class="vizui-btn" id="regen" type="button">↻ 换一批点</button>
      <span class="vizui-spacer"></span>
      <span style="font-size:.84rem;color:var(--color-text-muted)">点空白处加点：</span>
      <span class="pen" id="pen"><button data-c="1" class="on" type="button">● 蓝点</button><button data-c="-1" type="button">● 红点</button></span>
    </div>
  </div>

  <div class="vizui-panel">
    <div class="vizui-bar" style="justify-content:center">
      <svg class="vizui-chart" id="plane" viewBox="0 0 360 320" style="max-width:420px;margin:0 auto" role="img" aria-label="SVM 最大间隔平面"></svg>
    </div>
    <div style="text-align:center;margin-top:6px"><span id="status" class="vizui-pill">间隔宽度 —</span></div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>最宽的马路</b><p>分界线放在两类之间留白最宽处，离两边都尽量远，新样本更不容易判错。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>只看支持向量</b><p>路宽只由最靠边的几个点决定；删掉远处的点，分界线纹丝不动。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>泛化更稳</b><p>最大间隔等价于一种正则化，往往比“随便分开”的线在新数据上表现更好。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var XR=3, pts=[], seed=4, pen=1, line=null, drag=-1;
function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
function gauss(r){var u=0,v=0;while(!u)u=r();while(!v)v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}
function gen(){var r=rng(seed);pts=[];
  for(var i=0;i<7;i++)pts.push({x:1.25+gauss(r)*0.5,y:1.0+gauss(r)*0.55,c:1});
  for(var j=0;j<7;j++)pts.push({x:-1.15+gauss(r)*0.5,y:-0.9+gauss(r)*0.55,c:-1});
}
/* 近似最大间隔：取异类最近点对作为支持向量，分界线=其中垂线 */
function solve(){
  var P=pts.filter(function(p){return p.c>0;}),Nn=pts.filter(function(p){return p.c<0;});
  if(!P.length||!Nn.length){line=null;return;}
  var bd=1e9,sp=null,sn=null;
  P.forEach(function(a){Nn.forEach(function(b){var d=Math.hypot(a.x-b.x,a.y-b.y);if(d<bd){bd=d;sp=a;sn=b;}});});
  var mx=(sp.x+sn.x)/2,my=(sp.y+sn.y)/2, wx_=sp.x-sn.x, wy_=sp.y-sn.y, nl=Math.hypot(wx_,wy_)||1;
  line={mx:mx,my:my,w:[wx_/nl,wy_/nl],sp:sp,sn:sn,margin:bd/2};
}
var SVGNS="http://www.w3.org/2000/svg",W=360,H=320,pad=16;
function wx(x){return pad+(x+XR)/(2*XR)*(W-2*pad);}
function wy(y){return (H-pad)-(y+XR)/(2*XR)*(H-2*pad);}
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function lineBox(px,py,dx,dy){ /* 过(px,py)方向(dx,dy)与边框交点 */
  var ts=[];if(dx!==0){ts.push((-XR-px)/dx);ts.push((XR-px)/dx);}if(dy!==0){ts.push((-XR-py)/dy);ts.push((XR-py)/dy);}
  var segs=[];ts.forEach(function(t){var x=px+t*dx,y=py+t*dy;if(x>=-XR-1e-6&&x<=XR+1e-6&&y>=-XR-1e-6&&y<=XR+1e-6)segs.push([x,y]);});
  return segs.length>=2?[segs[0],segs[1]]:null;
}
function draw(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  E(svg,"line",{x1:wx(0),y1:pad,x2:wx(0),y2:H-pad,"class":"axis"});
  E(svg,"line",{x1:pad,y1:wy(0),x2:W-pad,y2:wy(0),"class":"axis"});
  if(line){
    var dir=[-line.w[1],line.w[0]];                /* 分界线方向（垂直于 w） */
    var seg=lineBox(line.mx,line.my,dir[0],dir[1]);
    if(seg){
      // 马路（淡蓝粗线，宽=间隔*2）
      var streetW=Math.abs(wx(line.margin)-wx(0))*2;
      E(svg,"line",{x1:wx(seg[0][0]),y1:wy(seg[0][1]),x2:wx(seg[1][0]),y2:wy(seg[1][1]),"class":"street","stroke-width":streetW});
      E(svg,"line",{x1:wx(seg[0][0]),y1:wy(seg[0][1]),x2:wx(seg[1][0]),y2:wy(seg[1][1]),"class":"decline"});
    }
    // 两条间隔线（过支持向量）
    [line.sp,line.sn].forEach(function(s){var sg=lineBox(s.x,s.y,dir[0],dir[1]);if(sg)E(svg,"line",{x1:wx(sg[0][0]),y1:wy(sg[0][1]),x2:wx(sg[1][0]),y2:wy(sg[1][1]),"class":"margin"});});
  }
  pts.forEach(function(p,i){
    var isSV=line&&(p===line.sp||p===line.sn);
    E(svg,"circle",{cx:wx(p.x),cy:wy(p.y),r:7,"class":"pt "+(p.c>0?"pos":"neg")+(isSV?" sv":""),"data-i":i});
  });
  document.getElementById("status").textContent=line?("间隔宽度 "+(line.margin*2).toFixed(2)+" · 支持向量 2 个"):"需要两类点";
}
function caption(){
  document.getElementById("caption").innerHTML=line?
    "分界线落在两类之间最宽的“马路”正中。撑住马路两边的是带金圈的<b>支持向量</b>——你拖动远处的点，分界线不会动；一旦拖动支持向量、或让某个点变成最靠近对方的点，整条线立刻重算。":
    "两类都要有点才能分。用上方的笔在空白处加几个点试试。";
}
function render(){solve();draw();caption();}

var svg=document.getElementById("plane");
function toWorld(e){var r=svg.getBoundingClientRect();var sx=(e.clientX-r.left)/r.width*W,sy=(e.clientY-r.top)/r.height*H;
  return [(sx-pad)/(W-2*pad)*(2*XR)-XR, ((H-pad-sy)/(H-2*pad))*(2*XR)-XR];}
svg.addEventListener("pointerdown",function(e){
  var t=e.target;
  if(t.classList&&t.classList.contains("pt")){drag=+t.getAttribute("data-i");svg.setPointerCapture(e.pointerId);}
  else{var w=toWorld(e);if(w[0]>-XR&&w[0]<XR&&w[1]>-XR&&w[1]<XR){pts.push({x:w[0],y:w[1],c:pen});render();}}
});
svg.addEventListener("pointermove",function(e){if(drag<0)return;var w=toWorld(e);pts[drag].x=Math.max(-XR,Math.min(XR,w[0]));pts[drag].y=Math.max(-XR,Math.min(XR,w[1]));render();});
svg.addEventListener("pointerup",function(){drag=-1;});
svg.addEventListener("pointercancel",function(){drag=-1;});
document.getElementById("regen").addEventListener("click",function(){seed++;gen();render();});
document.getElementById("pen").addEventListener("click",function(e){var b=e.target.closest("button");if(!b)return;pen=+b.dataset.c;document.querySelectorAll("#pen button").forEach(function(x){x.classList.toggle("on",+x.dataset.c===pen);});});

gen();render();
})();
</script>
{% endraw %}
