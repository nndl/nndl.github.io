---
layout: default
title: QKV 注意力计算
permalink: /viz/qkv-attention/
redirect_from:
  - /v/qkv-attention/
---

{% raw %}
<style>
.qklab .toks{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;}
.qklab .tok{display:flex;flex-direction:column;align-items:center;gap:5px;padding:8px 12px;border:1px solid var(--color-border);border-radius:var(--radius-md);background:var(--color-bg-pure);cursor:pointer;transition:all .15s var(--ease-out);}
.qklab .tok:hover{border-color:var(--color-accent);transform:translateY(-2px);}
.qklab .tok.q{border-color:var(--color-text);box-shadow:0 0 0 2px var(--color-accent-soft);}
.qklab .tok b{font-family:var(--font-serif);font-size:1.15rem;}
.qklab .tok .sw{width:34px;height:8px;border-radius:4px;}
.qklab .tok .role{font-size:.7rem;color:var(--color-text-muted);}
.qklab .axis{stroke:var(--color-border);stroke-width:1;}
.qklab .row{display:grid;grid-template-columns:42px 1fr 56px;align-items:center;gap:8px;margin:7px 0;font-size:.9rem;}
.qklab .row .nm{font-weight:600;}
.qklab .bar{height:14px;border-radius:7px;background:var(--color-bg-section);overflow:hidden;}
.qklab .bar i{display:block;height:100%;border-radius:7px;transition:width .3s var(--ease-out);}
.qklab .out{display:flex;align-items:center;gap:14px;margin-top:10px;padding:12px;border-radius:var(--radius-md);background:var(--color-bg-section);}
.qklab .out .swatch{width:54px;height:54px;border-radius:10px;border:2px solid #fff;box-shadow:var(--shadow-sm);transition:background .3s;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# QKV 注意力计算

“点词看注意力”那页给了直觉，这页拆开看注意力到底是怎么**算**出来的。每个词都准备了三样东西：查询 Query、键 Key、值 Value。一个词要更新自己，就拿它的 Query 去和每个词的 Key 比对齐程度（**点积**）当作分数，softmax 成权重，再按权重把大家的 Value 混合起来。**点一个词当查询方**，看它和谁最对齐、输出又像谁。

<section class="vizui qklab" id="qklab">
  <p class="vizui__lead">点下面任意词把它设为查询方（Query）。左图的黑箭头是它的 Query，彩色箭头是各词的 Key——箭头越同向，点积分数越高。右边把分数 softmax 成权重，按权重混合各词的颜色（Value）得到输出。</p>

  <div class="vizui-panel">
    <div class="toks" id="toks"></div>
  </div>

  <div class="vizui-grid2">
    <div class="vizui-panel">
      <p class="vizui-panel__title">对齐程度 = Query · Key</p>
      <svg class="vizui-chart" id="arrows" viewBox="0 0 240 240" style="max-width:280px;margin:0 auto;display:block" role="img" aria-label="Query 与 Key 向量"></svg>
    </div>
    <div class="vizui-panel">
      <p class="vizui-panel__title">分数 → softmax 权重</p>
      <div id="rows"></div>
      <div class="out">
        <div class="swatch" id="swatch"></div>
        <div style="font-size:.92rem;color:var(--color-text-soft)">输出 = Σ 权重×Value<br>最接近 <b id="nearest" style="color:var(--color-accent)">—</b> 的表示</div>
      </div>
    </div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>分数 = 点积</b><p>Query 和 Key 越“同向”，点积越大，说明这个词越值得关注。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>softmax 成权重</b><p>把一排分数压成加起来为 1 的权重，分数高的拿到更大的份额。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>输出 = 加权的 Value</b><p>按权重把各词的 Value 混合——输出主要由最受关注的词决定。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var TOK=[
  {nm:"猫",  q:[0.9,0.4],  k:[1.1,0.4],  col:[21,94,117]},
  {nm:"追",  q:[0.2,1.0],  k:[-0.2,1.0], col:[183,121,31]},
  {nm:"老鼠",q:[0.8,-0.7], k:[0.9,-0.6], col:[32,106,79]},
  {nm:"它",  q:[1.05,0.45],k:[0.2,0.15], col:[122,131,128]}
];
var qi=3, demoIv=null;
function hex(c){return "#"+c.map(function(v){v=Math.round(v);return (v<16?"0":"")+v.toString(16);}).join("");}
function softmax(z){var m=Math.max.apply(null,z),e=z.map(function(v){return Math.exp(v-m);}),s=e.reduce(function(a,b){return a+b;},0);return e.map(function(v){return v/s;});}

function buildToks(){
  var host=document.getElementById("toks");host.innerHTML="";
  TOK.forEach(function(t,i){
    var d=document.createElement("div");d.className="tok"+(i===qi?" q":"");d.dataset.i=i;
    d.innerHTML='<b>'+t.nm+'</b><span class="sw" style="background:'+hex(t.col)+'"></span><span class="role">'+(i===qi?"查询方":"点选")+'</span>';
    d.addEventListener("click",function(){if(demoIv){clearInterval(demoIv);demoIv=null;}qi=i;render();});
    host.appendChild(d);
  });
}
var SVGNS="http://www.w3.org/2000/svg";
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function arr(svg,vx,vy,col,sw){var ox=120,oy=120,sc=66,x=ox+vx*sc,y=oy-vy*sc;
  E(svg,"line",{x1:ox,y1:oy,x2:x,y2:y,stroke:col,"stroke-width":sw,"stroke-linecap":"round"});
  var a=Math.atan2(y-oy,x-ox),L=9;
  E(svg,"line",{x1:x,y1:y,x2:x-L*Math.cos(a-0.4),y2:y-L*Math.sin(a-0.4),stroke:col,"stroke-width":sw,"stroke-linecap":"round"});
  E(svg,"line",{x1:x,y1:y,x2:x-L*Math.cos(a+0.4),y2:y-L*Math.sin(a+0.4),stroke:col,"stroke-width":sw,"stroke-linecap":"round"});
}
function render(){
  buildToks();
  var Q=TOK[qi].q;
  var scores=TOK.map(function(t){return Q[0]*t.k[0]+Q[1]*t.k[1];});
  var w=softmax(scores);
  // 箭头
  var svg=document.getElementById("arrows");while(svg.firstChild)svg.removeChild(svg.firstChild);
  E(svg,"line",{x1:120,y1:14,x2:120,y2:226,"class":"axis"});E(svg,"line",{x1:14,y1:120,x2:226,y2:120,"class":"axis"});
  TOK.forEach(function(t){arr(svg,t.k[0],t.k[1],hex(t.col),2.4);});
  arr(svg,Q[0],Q[1],"#1a1a1a",3.4);
  E(svg,"text",{x:120,y:236,"text-anchor":"middle",style:"font:11px monospace;fill:#666"}).textContent="黑=Query  彩=各词Key";
  // 行
  var rows=document.getElementById("rows");rows.innerHTML="";
  TOK.forEach(function(t,i){
    var r=document.createElement("div");r.className="row";
    r.innerHTML='<span class="nm">'+t.nm+'</span><div class="bar"><i style="width:'+(w[i]*100).toFixed(1)+'%;background:'+hex(t.col)+'"></i></div><span style="font-family:var(--font-mono);color:var(--color-text-soft)">'+(w[i]*100).toFixed(0)+'%</span>';
    rows.appendChild(r);
  });
  // 输出颜色混合
  var out=[0,0,0];w.forEach(function(wi,i){out[0]+=wi*TOK[i].col[0];out[1]+=wi*TOK[i].col[1];out[2]+=wi*TOK[i].col[2];});
  document.getElementById("swatch").style.background=hex(out);
  var near=0;for(var i=1;i<TOK.length;i++)if(w[i]>w[near])near=i;
  document.getElementById("nearest").textContent=TOK[near].nm;
  caption(near,w);
}
function caption(near,w){
  document.getElementById("caption").innerHTML="查询方 <b>"+TOK[qi].nm+"</b>：它的 Query 和 <b>"+TOK[near].nm+"</b> 的 Key 最对齐，分数最高、softmax 后权重 <b>"+(w[near]*100).toFixed(0)+"%</b> 最大，于是输出主要由 "+TOK[near].nm+" 的 Value 决定。"+(TOK[qi].nm==="它"?"——这正是模型判断“它”指代“猫”的计算过程。":"");
}

render();
setTimeout(function(){
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  var seq=[0,2,1,3],k=0;demoIv=setInterval(function(){qi=seq[k];render();k++;if(k>=seq.length){clearInterval(demoIv);demoIv=null;}},1400);
},1000);
})();
</script>
{% endraw %}
