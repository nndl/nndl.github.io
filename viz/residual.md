---
layout: default
title: 残差连接
permalink: /viz/residual/
redirect_from:
  - /v/residual/
---

{% raw %}
<style>
.reslab .colwrap{display:grid;grid-template-columns:1fr 1fr;gap:18px;}
.reslab h4{text-align:center;margin:0 0 8px;font-size:1rem;}
.reslab .skip{stroke:var(--color-forest);stroke-width:2;fill:none;opacity:.7;}
.reslab .blk{stroke:var(--color-border-strong);stroke-width:1;}
.reslab .flow{font:10px var(--font-mono);fill:var(--color-text-muted);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 残差连接

网络越深，本该越强，但早年一深就训不动——因为反向传播时，梯度要穿过每一层、一路连乘小于 1 的数，传到底层就几乎归零（梯度消失）。残差连接（ResNet 的核心）加了一条“跳线”：每个模块的输出 = 输入 + 这个模块学到的修正。反向求导时，这条跳线给梯度留了一条**直通的高速路**（导数里多了个 +1），于是梯度怎么都不会被乘没。正因如此，几百上千层的网络才训得起来，Transformer 里也到处是它。拖动深度，对比两边梯度传到底层还剩多少。

<section class="reslab vizui" id="reslab">
  <p class="vizui__lead">每个色块是一层，颜色越深（浓）表示反向传播时梯度传到这一层还越强、越浅（发白）表示越弱。梯度从顶部（输出）往下传到底部（输入）。左边普通堆叠，右边每层带一条绿色跳线。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="n">网络深度</label><input type="range" id="n" min="4" max="40" step="1" value="24" style="width:200px"><output id="nVal">24</output> 层</span>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="info">—</span>
    </div>
    <div class="colwrap">
      <div><h4 style="color:#b5524a">普通深层网络</h4><svg id="plain" viewBox="0 0 200 360" role="img" aria-label="普通网络梯度"></svg></div>
      <div><h4 style="color:var(--color-forest)">残差网络（带跳线）</h4><svg id="res" viewBox="0 0 200 360" role="img" aria-label="残差网络梯度"></svg></div>
    </div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:#b5524a"><b>普通：梯度连乘消失</b><p>每层梯度乘一个小于 1 的数，层数一多，传到底层就趋近于 0，底层学不动。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>残差：+1 高速路</b><p>跳线让导数里多了个 +1，梯度有一条不被衰减的直通路径，再深也传得下去。</p></div>
    <div class="card" style="--wc:var(--color-accent)"><b>所以能更深</b><p>ResNet 把网络从几十层推到上百层；Transformer 每个子层也都有残差。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var N=24, decay=0.82;
var SVGNS="http://www.w3.org/2000/svg",W=200,H=360,pad=14;
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function tealOf(v){var lo=[233,238,235],hi=[21,94,117];return "rgb("+Math.round(lo[0]+(hi[0]-lo[0])*v)+","+Math.round(lo[1]+(hi[1]-lo[1])*v)+","+Math.round(lo[2]+(hi[2]-lo[2])*v)+")";}
function drawCol(id,residual){
  var svg=document.getElementById(id);while(svg.firstChild)svg.removeChild(svg.firstChild);
  var top=pad,bot=H-pad,bh=(bot-top)/N;
  for(var k=0;k<N;k++){
    var fromTop=k;                       /* 第 k 层离输出的层数（0=最顶） */
    var mag=residual?1:Math.pow(decay,fromTop);
    var y=top+k*bh;
    E(svg,"rect",{x:40,y:y+1,width:W-80,height:bh-2,rx:3,fill:tealOf(Math.max(0.04,mag)),"class":"blk"});
    if(residual&&k<N-1){E(svg,"path",{d:"M"+(W-40)+","+(y+bh/2)+" C"+(W-18)+","+(y+bh/2)+" "+(W-18)+","+(y+bh+bh/2)+" "+(W-40)+","+(y+bh+bh/2),"class":"skip"});}
  }
  E(svg,"text",{x:W/2,y:10,"text-anchor":"middle","class":"flow"}).textContent="输出 ↑ 梯度";
  E(svg,"text",{x:W/2,y:H-2,"text-anchor":"middle","class":"flow"}).textContent="输入（底层）";
}
function render(){
  document.getElementById("nVal").textContent=N;
  drawCol("plain",false);drawCol("res",true);
  var rem=Math.pow(decay,N-1);
  document.getElementById("info").textContent="传到底层：普通 "+(rem<0.001?rem.toExponential(1):(rem*100).toFixed(1)+"%")+" · 残差 ≈100%";
  caption(rem);
}
function caption(rem){
  document.getElementById("caption").innerHTML="深度 "+N+" 层时，梯度传到最底层：普通网络只剩 <b style='color:#b5524a'>"+(rem<0.001?rem.toExponential(1):(rem*100).toFixed(1)+"%")+"</b>（底部几乎褪成白色——学不动），残差网络靠跳线<b style='color:var(--color-forest)'>≈100%</b>保住（整列都是深色）。深度越大，差距越悬殊。";
}
document.getElementById("n").addEventListener("input",function(e){N=+e.target.value;render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  var seq=[8,18,30,40,24],k=0,sl=document.getElementById("n");var iv=setInterval(function(){N=seq[k];sl.value=N;render();k++;if(k>=seq.length)clearInterval(iv);},900);},1000);
})();
</script>
{% endraw %}
