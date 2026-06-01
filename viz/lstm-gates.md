---
layout: default
title: LSTM 的门控记忆
permalink: /viz/lstm-gates/
redirect_from:
  - /v/lstm-gates/
---

{% raw %}
<style>
.lglab svg{max-width:100%;height:auto;}
.lglab .axis{stroke:var(--color-border-strong);stroke-width:1;}
.lglab .lbl{font:10px var(--font-sans);fill:var(--color-text-muted);}
.lglab .cline{fill:none;stroke:var(--color-gold);stroke-width:3;}
.lglab .hline{fill:none;stroke:var(--color-accent);stroke-width:2;stroke-dasharray:4 3;}
.lglab .spike{stroke:#b5524a;stroke-width:1.5;stroke-dasharray:3 3;}
.lglab .dot{stroke:#fff;stroke-width:1.5;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# LSTM 的门控记忆

普通 RNN 的记忆会随步数指数衰减，记不住远处。LSTM 的妙招是给隐藏单元加一条专门的**细胞状态**（像一条传送带），并用三道**门**来管它：**遗忘门**决定旧记忆保留多少、**输入门**决定新信息写入多少、**输出门**决定当前露出多少给外面。关键在遗忘门——当它接近 1、输入门接近 0 时，细胞状态几乎原样往下传（≈乘 1），于是一个早早存进去的值能**跨越很多步保留不衰减**，这正是普通 RNN 做不到的。下面在第 2 步存入一个值，调三道门，看记忆能撑多久。

<section class="vizui lglab" id="lglab">
  <p class="vizui__lead">第 2 步往细胞里存入一个值（红线处）。<span style="color:var(--color-gold)">金线</span>是细胞状态 C（记忆），<span style="color:var(--color-accent)">蓝虚线</span>是输出 h。调“遗忘门”看记忆是被守住还是漏光。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="f">遗忘门</label><input type="range" id="f" min="0.5" max="1" step="0.01" value="0.98" style="width:120px"><output id="fVal">0.98</output></span>
      <span class="vizui-field"><label for="i">输入门</label><input type="range" id="i" min="0" max="1" step="0.05" value="1" style="width:90px"></span>
      <span class="vizui-field"><label for="o">输出门</label><input type="range" id="o" min="0" max="1" step="0.05" value="1" style="width:90px"></span>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stat">—</span>
    </div>
    <svg id="plane" viewBox="0 0 460 230" role="img" aria-label="LSTM 门控"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-gold)"><b>遗忘门：记多久</b><p>≈1 时细胞状态原样保留，记忆能跨越很多步不衰减；小了就漏光。</p></div>
    <div class="card" style="--wc:var(--color-accent)"><b>输入门：写多少</b><p>控制新信息写进细胞的比例，决定何时该更新记忆。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>输出门：露多少</b><p>决定当前把多少记忆透露给外部输出 h，记忆可以“留着不用”。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var T=12,f=0.98,ig=1,og=1,spikeT=2;
var SVGNS="http://www.w3.org/2000/svg",W=460,H=230,pl=34,pr=14,pt=14,pb=34;
function px(t){return pl+t/(T-1)*(W-pl-pr);}function py(v){return (H-pb)-v*(H-pt-pb);}
function E(p,t,a,txt){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;p.appendChild(e);return e;}
function compute(){var C=[],h=[],c=0;for(var t=0;t<T;t++){var g=(t===spikeT)?Math.tanh(1.2):0;c=f*c+ig*g;C.push(c);h.push(og*Math.tanh(c));}return {C:C,h:h};}
function render(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var r=compute();
  E(svg,"line",{x1:pl,y1:H-pb,x2:W-pr,y2:H-pb,"class":"axis"});E(svg,"line",{x1:pl,y1:pt,x2:pl,y2:H-pb,"class":"axis"});
  [0,0.5,1].forEach(function(v){E(svg,"text",{x:pl-5,y:py(v)+3,"text-anchor":"end","class":"lbl"},v.toFixed(1));});
  E(svg,"line",{x1:px(spikeT),y1:pt,x2:px(spikeT),y2:H-pb,"class":"spike"});
  E(svg,"text",{x:px(spikeT),y:pt+2,"text-anchor":"middle","class":"lbl",style:"fill:#b5524a"},"存入↑");
  E(svg,"polyline",{points:r.C.map(function(v,t){return px(t)+","+py(v);}).join(" "),"class":"cline"});
  E(svg,"polyline",{points:r.h.map(function(v,t){return px(t)+","+py(v);}).join(" "),"class":"hline"});
  r.C.forEach(function(v,t){E(svg,"circle",{cx:px(t),cy:py(v),r:3,fill:"var(--color-gold)","class":"dot"});});
  for(var t=0;t<T;t++)E(svg,"text",{x:px(t),y:H-pb+14,"text-anchor":"middle","class":"lbl"},t);
  E(svg,"text",{x:(pl+W-pr)/2,y:H-pb+28,"text-anchor":"middle","class":"lbl"},"时间步 →");
  // 记忆保持步数：spike 后 C 仍 > 峰值一半
  var peak=r.C[spikeT],hold=0;for(var t2=spikeT;t2<T;t2++)if(r.C[t2]>peak*0.5)hold++;
  document.getElementById("fVal").textContent=f.toFixed(2);
  document.getElementById("stat").textContent="记忆保持约 "+hold+" 步";
  caption(hold);
}
function caption(hold){
  var el=document.getElementById("caption");
  if(f>=0.97)el.innerHTML="<b>遗忘门≈1：</b>存入的值几乎原样保留，金线一路走平——记忆撑过了大约 <b>"+hold+"</b> 步、几乎不衰减。普通 RNN 这时早就忘光了，这就是 LSTM 记得久的秘密。";
  else if(f>=0.8)el.innerHTML="<b>遗忘门="+f.toFixed(2)+"：</b>记忆缓慢漏掉，金线逐步下滑，保持约 "+hold+" 步。把遗忘门再调高，记忆撑得更久。";
  else el.innerHTML="<b>遗忘门="+f.toFixed(2)+"（偏小）：</b>记忆很快漏光，只撑了约 "+hold+" 步——退化得像普通 RNN。把遗忘门调到接近 1 试试。";
}
["f","i","o"].forEach(function(id){document.getElementById(id).addEventListener("input",function(e){if(id==="f")f=+e.target.value;else if(id==="i")ig=+e.target.value;else og=+e.target.value;render();});});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  var seq=[0.7,0.88,0.98],k=0,sl=document.getElementById("f");var iv=setInterval(function(){f=seq[k];sl.value=f;render();k++;if(k>=seq.length)clearInterval(iv);},1200);},1000);
})();
</script>
{% endraw %}
