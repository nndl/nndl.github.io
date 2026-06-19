---
layout: default
title: RNN 为什么记不住：梯度消失
permalink: /viz/bptt-vanishing/
redirect_from:
  - /v/bptt-vanishing/
---

{% raw %}
<style>
.bvlab svg{max-width:100%;height:auto;}
.bvlab .axis{stroke:var(--color-border-strong);stroke-width:1;}
.bvlab .bar{fill:var(--color-accent);}
.bvlab .lbl{font:10px var(--font-sans);fill:var(--color-text-muted);}
.bvlab .big{font:22px var(--font-sans);font-weight:700;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# RNN 为什么记不住：梯度消失

普通 RNN 理论上能记住很久以前的信息，实际却常常“记不住”。问题出在训练：要让早期输入影响最终结果，误差信号得沿着时间一步步**往回传**，每回传一步就乘上一次循环权重 w。于是传回 k 步后，信号大约变成 **wᵏ**——只要 w 稍小于 1，传回几十步就衰减到几乎为 0（**梯度消失**，早期输入学不动、被“遗忘”）；稍大于 1 又会爆炸（**梯度爆炸**，训练发散）。只有 w≈1 的窄缝才稳定，却极难凑到。拖动 w，看误差信号沿时间回传时怎样消失或爆炸——这正是 LSTM 用“门控细胞”要解决的问题。

<section class="vizui bvlab" id="bvlab">
  <p class="vizui__lead">每根条是某个时间步的输入对最终结果的<b>影响强度</b>（梯度），右边是最近一步、左边是最久远一步。看 w 怎样决定久远信息是被“记住”还是“消失/爆炸”。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="w">循环权重 w</label><input type="range" id="w" min="0.5" max="1.5" step="0.02" value="0.8" style="width:200px"><output id="wVal">0.80</output></span>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stat">—</span>
    </div>
    <svg id="plane" viewBox="0 0 460 240" role="img" aria-label="梯度沿时间回传"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:#b5524a"><b>w&lt;1：消失</b><p>梯度按 wᵏ 指数衰减，回传几十步就≈0，早期输入学不到——长程记忆丢失。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>w&gt;1：爆炸</b><p>梯度指数放大，数值溢出、训练发散。需要梯度裁剪等手段救急。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>LSTM 的解法</b><p>用“细胞状态+门”让信息近乎原样直传（≈乘 1），绕开 wᵏ 衰减，记得更久。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var T=14,w=0.8;
var SVGNS="http://www.w3.org/2000/svg",W=460,H=240,pl=30,pr=14,pt=16,pb=40;
function E(p,t,a,txt){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;p.appendChild(e);return e;}
function render(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  // influence[t] = w^(distance back) ; t=0 oldest (dist T-1), t=T-1 newest (dist 0)
  var g=[];for(var t=0;t<T;t++)g.push(Math.pow(w,(T-1-t)));
  var mx=Math.max.apply(null,g);
  var bw=(W-pl-pr)/T;
  E(svg,"line",{x1:pl,y1:H-pb,x2:W-pr,y2:H-pb,"class":"axis"});
  for(var t2=0;t2<T;t2++){var hh=(g[t2]/mx)*(H-pt-pb);var x=pl+t2*bw;
    E(svg,"rect",{x:x+2,y:(H-pb)-hh,width:bw-4,height:hh,rx:1,"class":"bar",opacity:(0.35+0.6*g[t2]/mx).toFixed(2)});}
  E(svg,"text",{x:pl+bw/2,y:H-pb+14,"text-anchor":"middle","class":"lbl"},"最久远");
  E(svg,"text",{x:W-pr-bw/2,y:H-pb+14,"text-anchor":"middle","class":"lbl"},"最近");
  E(svg,"text",{x:(pl+W-pr)/2,y:H-pb+28,"text-anchor":"middle","class":"lbl"},"← 误差沿时间回传（共 "+T+" 步）");
  var oldest=Math.pow(w,T-1);
  var cc=oldest<0.1?"#b5524a":oldest>10?"#b5524a":"#206a4f";
  E(svg,"text",{x:W-pr,y:pt+18,"text-anchor":"end","class":"big",fill:cc},"w^"+(T-1)+" = "+(oldest<0.001?oldest.toExponential(1):oldest<100?oldest.toFixed(oldest<1?3:1):oldest.toExponential(1)));
  document.getElementById("wVal").textContent=w.toFixed(2);
  document.getElementById("stat").textContent=oldest<0.1?"梯度消失":oldest>10?"梯度爆炸":"较稳定";
  caption(oldest);
}
function caption(oldest){
  var el=document.getElementById("caption");
  if(oldest<0.1)el.innerHTML="<b>w="+w.toFixed(2)+"（&lt;1）：</b>回传 "+(T-1)+" 步后，最久远那步的梯度只剩 <b>"+(oldest<0.001?oldest.toExponential(1):oldest.toFixed(3))+"</b>——几乎为 0。早期输入根本学不动，RNN 因此“记不住”长程信息（梯度消失）。";
  else if(oldest>10)el.innerHTML="<b>w="+w.toFixed(2)+"（&gt;1）：</b>梯度被放大到 <b>"+(oldest>100?oldest.toExponential(1):oldest.toFixed(1))+"</b> 倍——指数爆炸，训练会数值溢出、发散（梯度爆炸）。";
  else el.innerHTML="<b>w="+w.toFixed(2)+"：</b>回传 "+(T-1)+" 步后久远梯度还剩 <b>"+oldest.toFixed(2)+"</b>，落在相对稳定的窄缝里——但训练里极难恰好维持。所以才需要 LSTM 的门控细胞，让信息近乎乘 1 地直传。";
}
document.getElementById("w").addEventListener("input",function(e){w=+e.target.value;render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  var seq=[0.7,1.3,1.0,0.8],k=0,sl=document.getElementById("w");var iv=setInterval(function(){w=seq[k];sl.value=w;render();k++;if(k>=seq.length)clearInterval(iv);},1200);},1000);
})();
</script>
{% endraw %}
