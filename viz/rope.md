---
layout: default
title: RoPE 旋转位置编码
description: "位置编码成旋转角度，两词的注意力分数只取决于相对位置——更稳、还能外推到更长序列。"
permalink: /viz/rope/
redirect_from:
  - /v/rope/
---

{% raw %}
<style>
.roplab .axis{stroke:var(--color-border);stroke-width:1;}
.roplab .circ{fill:none;stroke:var(--color-border);stroke-width:1.4;}
.roplab .arc{fill:none;stroke:var(--color-text-muted);stroke-width:1.6;}
.roplab .vq{stroke:var(--color-accent);stroke-width:3.4;}
.roplab .vk{stroke:var(--color-gold);stroke-width:3.4;}
.roplab .strip{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;}
.roplab .dial{width:46px;text-align:center;}
.roplab .dial svg{display:block;margin:0 auto;}
.roplab .dial .pos{font:10px var(--font-mono);color:var(--color-text-muted);}
.roplab .dial.q .pos{color:var(--color-accent);font-weight:700;}
.roplab .dial.k .pos{color:var(--color-gold);font-weight:700;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# RoPE 旋转位置编码

Transformer 本身分不清词的先后，得额外注入“位置”。RoPE（旋转位置编码）的办法特别优雅：**不是把位置加上去，而是把每个词的向量按它的位置旋转一个角度**——位置越靠后，转得越多。妙处在于：两个词做注意力时，分数只取决于它们之间转角的差，也就是**相对位置**，跟它们在句子里的绝对位置无关。所以同样的相对距离，无论在句首还是句尾，模型看到的都一样，也因此能外推到训练时没见过的长度。拖动两个词的位置试试。

<section class="roplab vizui" id="roplab">
  <p class="vizui__lead">每个位置把向量转一个固定的角度。<span style="color:var(--color-accent);font-weight:600">蓝=查询词</span>在位置 m、<span style="color:var(--color-gold);font-weight:600">金=键词</span>在位置 n。它们的注意力分数 = 两个箭头夹角的余弦，而夹角 = (m−n)×每位转角。</p>

  <div class="vizui-grid2">
    <div class="vizui-panel">
      <svg class="vizui-chart" id="dial" viewBox="0 0 240 240" style="max-width:260px;margin:0 auto;display:block" role="img" aria-label="两个旋转向量与夹角"></svg>
      <div style="text-align:center;margin-top:6px;font:600 .92rem var(--font-mono);color:var(--color-text-soft)" id="read"></div>
    </div>
    <div class="vizui-panel">
      <p class="vizui-panel__title">控制</p>
      <div class="vizui-field"><label for="m">查询位置 m</label><input type="range" id="m" min="0" max="11" step="1" value="2" style="width:150px"><output id="mVal">2</output></div>
      <div class="vizui-field" style="margin-top:8px"><label for="n">键位置 n</label><input type="range" id="n" min="0" max="11" step="1" value="5" style="width:150px"><output id="nVal">5</output></div>
      <p class="vizui-panel__title" style="margin-top:14px">每个位置 = 一个转角</p>
      <div class="strip" id="strip"></div>
    </div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>位置 = 旋转</b><p>位置越靠后，向量转得越多——把顺序信息编进了角度里。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>只看相对位置</b><p>注意力分数只取决于两词转角之差 (m−n)，绝对位置无关——更稳、更通用。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>能外推</b><p>因为只认相对距离，模型能处理比训练时更长的序列，这是 RoPE 流行的原因。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var TH=0.52, m=2, n=5, NP=12;
var SVGNS="http://www.w3.org/2000/svg";
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function arr(svg,ox,oy,ang,len,cls){var x=ox+len*Math.cos(ang),y=oy-len*Math.sin(ang);
  E(svg,"line",{x1:ox,y1:oy,x2:x,y2:y,"class":cls});
  var a=Math.atan2(y-oy,x-ox),L=8;
  E(svg,"line",{x1:x,y1:y,x2:x-L*Math.cos(a-0.4),y2:y-L*Math.sin(a-0.4),"class":cls});
  E(svg,"line",{x1:x,y1:y,x2:x-L*Math.cos(a+0.4),y2:y-L*Math.sin(a+0.4),"class":cls});}
function drawDial(){
  var svg=document.getElementById("dial"),O=120,Rr=90;while(svg.firstChild)svg.removeChild(svg.firstChild);
  E(svg,"circle",{cx:O,cy:O,r:Rr,"class":"circ"});
  E(svg,"line",{x1:O-Rr,y1:O,x2:O+Rr,y2:O,"class":"axis"});E(svg,"line",{x1:O,y1:O-Rr,x2:O,y2:O+Rr,"class":"axis"});
  var am=m*TH, an=n*TH;
  // 夹角弧
  E(svg,"path",{d:"M"+(O+34*Math.cos(am))+","+(O-34*Math.sin(am))+" A34,34 0 0 "+(((an-am)%(2*Math.PI)+2*Math.PI)%(2*Math.PI)>Math.PI?0:1)+" "+(O+34*Math.cos(an))+","+(O-34*Math.sin(an)),"class":"arc"});
  arr(svg,O,O,an,Rr,"vk");arr(svg,O,O,am,Rr,"vq");
}
function drawStrip(){
  var host=document.getElementById("strip");host.innerHTML="";
  for(var p=0;p<NP;p++){(function(p){
    var d=document.createElement("div");d.className="dial"+(p===m?" q":"")+(p===n?" k":"");
    var s='<svg viewBox="0 0 40 40" width="40" height="40"><circle cx="20" cy="20" r="16" fill="none" stroke="#dde4e4" stroke-width="1.4"/>';
    var ang=p*TH,x=20+15*Math.cos(ang),y=20-15*Math.sin(ang),col=p===m?"#155e75":p===n?"#b7791f":"#9aa5a3";
    s+='<line x1="20" y1="20" x2="'+x.toFixed(1)+'" y2="'+y.toFixed(1)+'" stroke="'+col+'" stroke-width="'+(p===m||p===n?3:2)+'" stroke-linecap="round"/></svg>';
    d.innerHTML=s+'<div class="pos">位'+p+'</div>';
    d.addEventListener("click",function(){if(p!==n){m=p;render();}});
    host.appendChild(d);
  })(p);}
}
function render(){
  document.getElementById("mVal").textContent=m;document.getElementById("nVal").textContent=n;
  document.getElementById("m").value=m;document.getElementById("n").value=n;
  var rel=m-n, ang=rel*TH, score=Math.cos(ang);
  drawDial();drawStrip();
  document.getElementById("read").innerHTML="相对位置 m−n = <b>"+rel+"</b>　夹角 = "+(Math.abs(rel)*TH).toFixed(2)+" rad　注意力分数 cos = <b style='color:var(--color-accent)'>"+score.toFixed(2)+"</b>";
  caption(rel,score);
}
function caption(rel,score){
  document.getElementById("caption").innerHTML="查询在位置 "+m+"、键在位置 "+n+"，相对距离 "+rel+"。注意力分数 cos = <b>"+score.toFixed(2)+"</b>。<b>关键：</b>把 m、n 同时加同一个数（整体右移），相对距离不变，分数也分毫不动——RoPE 只认相对位置，所以换到句子任何地方、甚至更长的句子里都适用。";
}
document.getElementById("m").addEventListener("input",function(e){m=+e.target.value;render();});
document.getElementById("n").addEventListener("input",function(e){n=+e.target.value;render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  var seq=[[2,5],[4,7],[6,9],[1,4],[2,5]],k=0;var iv=setInterval(function(){m=seq[k][0];n=seq[k][1];render();k++;if(k>=seq.length)clearInterval(iv);},1100);},1000);
})();
</script>
{% endraw %}
