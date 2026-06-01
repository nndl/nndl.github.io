---
layout: default
title: 汇聚（池化）
permalink: /viz/pooling/
redirect_from:
  - /v/pooling/
---

{% raw %}
<style>
.pllab .conv-row{display:flex;flex-wrap:wrap;gap:20px;align-items:center;justify-content:center;}
.pllab .grid{display:grid;gap:2px;background:var(--color-border);border:1px solid var(--color-border);border-radius:4px;}
.pllab .grid .c{display:flex;align-items:center;justify-content:center;font:600 9px var(--font-mono);}
.pllab .gwrap{text-align:center;}
.pllab .gwrap .lbl{font-size:.82rem;color:var(--color-text-muted);margin-bottom:6px;}
.pllab .win{box-shadow:inset 0 0 0 2px var(--color-gold);z-index:1;}
.pllab .ocur{box-shadow:inset 0 0 0 2px var(--color-gold);}
.pllab .heads{display:inline-flex;gap:4px;padding:4px;background:var(--color-bg-section);border:1px solid var(--color-border);border-radius:999px;}
.pllab .heads button{appearance:none;border:0;background:transparent;cursor:pointer;font:inherit;font-size:.88rem;color:var(--color-text-soft);padding:7px 16px;border-radius:999px;}
.pllab .heads button.on{background:var(--color-bg-pure);color:var(--color-accent);font-weight:600;box-shadow:var(--shadow-sm);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 汇聚（池化）

卷积之后，特征图往往很大。汇聚（pooling，也叫池化）就是把它“缩小”一圈：拿一个小窗口（这里 2×2）不重叠地扫过去，每块只留一个代表值——**最大汇聚**留最强的那个响应，**平均汇聚**留平均值。这样既减少了计算量，又让网络对位置的小变动不那么敏感（平移不变）。换换两种方式，看 8×8 怎么被缩成 4×4。

<section class="vizui pllab" id="pllab">
  <p class="vizui__lead">左边 8×8 是输入特征图（越亮响应越强）。2×2 窗口不重叠地滑动，每块输出一个值，得到右边 4×4。金框是当前窗口和它对应的输出格。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="heads" id="heads"><button data-m="max" class="on" type="button">最大汇聚</button><button data-m="avg" type="button">平均汇聚</button></span>
      <span class="vizui-spacer"></span>
      <button class="vizui-btn vizui-btn--go" id="go" type="button">▶ 自动滑动</button>
      <button class="vizui-btn" id="step" type="button">单步</button>
      <button class="vizui-btn" id="reset" type="button">重置</button>
    </div>
  </div>

  <div class="vizui-panel">
    <div class="conv-row">
      <div class="gwrap"><div class="lbl">输入 8×8</div><div class="grid" id="inGrid"></div></div>
      <div style="font-size:1.4rem;color:var(--color-text-muted)">→</div>
      <div class="gwrap"><div class="lbl">汇聚后 4×4</div><div class="grid" id="outGrid"></div></div>
    </div>
    <div id="calc" style="text-align:center;margin-top:12px;font:600 .9rem var(--font-mono);color:var(--color-text-soft)"></div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>最大汇聚</b><p>只留窗口里最强的响应——“这一带有没有出现这个特征”，最常用。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>平均汇聚</b><p>取窗口平均，更平滑，保留整体强度但弱化尖峰。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>为什么有用</b><p>缩小尺寸省算力；位置略微移动结果也基本不变（平移不变），还能扩大后层的感受野。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var N=8,M=4,mode="max",wr=0,wc=0,playing=false,timer=null;
var IMG=[];for(var r=0;r<N;r++){IMG.push([]);for(var c=0;c<N;c++){
  var v=0.12+0.82*Math.exp(-((r-2)*(r-2)+(c-2)*(c-2))/3.2)+0.78*Math.exp(-((r-5)*(r-5)+(c-6)*(c-6))/3.2)+0.5*Math.exp(-((r-6)*(r-6)+(c-1)*(c-1))/2.5);
  IMG[r].push(Math.min(1,v));}}
function pool(i,j){var vs=[IMG[i*2][j*2],IMG[i*2][j*2+1],IMG[i*2+1][j*2],IMG[i*2+1][j*2+1]];
  return mode==="max"?Math.max.apply(null,vs):(vs[0]+vs[1]+vs[2]+vs[3])/4;}
function teal(v){var lo=[238,241,238],hi=[21,94,117];return "rgb("+Math.round(lo[0]+(hi[0]-lo[0])*v)+","+Math.round(lo[1]+(hi[1]-lo[1])*v)+","+Math.round(lo[2]+(hi[2]-lo[2])*v)+")";}
function build(){
  var ig=document.getElementById("inGrid");ig.style.gridTemplateColumns="repeat("+N+",1fr)";ig.innerHTML="";
  for(var r=0;r<N;r++)for(var c=0;c<N;c++){var d=document.createElement("div");d.className="c";d.style.width="26px";d.style.height="26px";d.style.background=teal(IMG[r][c]);d.style.color=IMG[r][c]>0.55?"#fff":"#789";ig.appendChild(d);}
  var og=document.getElementById("outGrid");og.style.gridTemplateColumns="repeat("+M+",1fr)";og.innerHTML="";
  for(var i=0;i<M;i++)for(var j=0;j<M;j++){var o=document.createElement("div");o.className="c";o.style.width="40px";o.style.height="40px";og.appendChild(o);}
}
function render(){
  var revealed=wr*M+wc, og=document.getElementById("outGrid").children;
  for(var i=0;i<M;i++)for(var j=0;j<M;j++){var cell=og[i*M+j],idx=i*M+j,val=pool(i,j);
    cell.style.background=idx<=revealed?teal(val):"var(--color-bg-pure)";
    cell.textContent=idx<=revealed?val.toFixed(2):"";cell.style.color=val>0.55?"#fff":"#789";
    cell.classList.toggle("ocur",i===wr&&j===wc);}
  var ig=document.getElementById("inGrid").children;
  for(var r=0;r<N;r++)for(var c=0;c<N;c++)ig[r*N+c].classList.toggle("win",r>=wr*2&&r<wr*2+2&&c>=wc*2&&c<wc*2+2);
  var vs=[IMG[wr*2][wc*2],IMG[wr*2][wc*2+1],IMG[wr*2+1][wc*2],IMG[wr*2+1][wc*2+1]];
  document.getElementById("calc").innerHTML=(mode==="max"?"max":"平均")+"("+vs.map(function(v){return v.toFixed(2);}).join(", ")+") = <b style='color:var(--color-gold)'>"+pool(wr,wc).toFixed(2)+"</b>";
  caption();
}
function caption(){document.getElementById("caption").innerHTML=mode==="max"?
  "<b>最大汇聚：</b>每个 2×2 块只保留最大值。两个亮团的峰值被原样留下，暗区被压低——特征图缩小一半，但“哪里有强响应”这件事保住了。":
  "<b>平均汇聚：</b>每个 2×2 块取平均。亮团被周围的暗格拉低，整体更平滑、尖峰被削弱。对比最大汇聚看差别。";}
function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("go").textContent="▶ 自动滑动";}
function advance(){wc++;if(wc>=M){wc=0;wr++;}if(wr>=M){wr=M-1;wc=M-1;return false;}return true;}
function play(){if(wr===M-1&&wc===M-1){wr=0;wc=0;}stop();playing=true;document.getElementById("go").textContent="⏸ 暂停";timer=setInterval(function(){if(!advance())stop();render();},170);}
document.getElementById("heads").addEventListener("click",function(e){var b=e.target.closest("button");if(!b)return;mode=b.dataset.m;document.querySelectorAll("#heads button").forEach(function(x){x.classList.toggle("on",x.dataset.m===mode);});render();});
document.getElementById("go").addEventListener("click",function(){playing?stop():play();});
document.getElementById("step").addEventListener("click",function(){stop();advance();render();});
document.getElementById("reset").addEventListener("click",function(){stop();wr=0;wc=0;render();});
build();wr=M-1;wc=M-1;render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;wr=0;wc=0;play();},900);
})();
</script>
{% endraw %}
