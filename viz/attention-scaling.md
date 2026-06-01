---
layout: default
title: 注意力为什么除以 √d
permalink: /viz/attention-scaling/
redirect_from:
  - /v/attention-scaling/
---

{% raw %}
<style>
.aslab svg{max-width:100%;height:auto;}
.aslab .bar{fill:var(--color-accent);}
.aslab .axis{stroke:var(--color-border-strong);stroke-width:1;}
.aslab .lbl{font:11px var(--font-sans);fill:var(--color-text-muted);}
.aslab .ttl{font:12px var(--font-sans);fill:#333;font-weight:600;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 注意力为什么除以 √d

自注意力靠 Query 和 Key 的**点积**算“相关分数”，再用 softmax 变成权重。但有个隐患：向量维度 d 越大，点积是 d 个乘积之和，数值会越积越大（标准差按 √d 增长）。分数一大，softmax 就会**饱和**——几乎把全部权重压给最大的那个、其余几乎为 0，变成非 0 即 1 的硬选择，梯度也随之消失，没法学。Transformer 的解法很简单：把分数**除以 √d** 再做 softmax，把它拉回稳定范围。拖动维度滑块，对比“不缩放”和“÷√d”两种 softmax。

<section class="vizui aslab" id="aslab">
  <p class="vizui__lead">同一组 Query/Key，左边是<b>不缩放</b>直接 softmax，右边是<b>÷√d</b> 后再 softmax。注意维度一大，左边就塌成“一根独大”（饱和），右边依然分布柔和。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="d">向量维度 d</label><input type="range" id="d" min="2" max="128" step="1" value="4" style="width:180px"><output id="dVal">4</output></span>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stat">—</span>
    </div>
    <svg id="plane" viewBox="0 0 460 230" role="img" aria-label="注意力缩放"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>点积随 d 变大</b><p>分数是 d 项之和，维度越高、数值波动越大（标准差∝√d）。</p></div>
    <div class="card" style="--wc:#b5524a"><b>不缩放会饱和</b><p>分数过大，softmax 变成近似 one-hot，权重几乎全给一个、梯度消失。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>÷√d 稳住</b><p>除以 √d 把分数拉回 O(1)，softmax 保持柔和、可学——这就是“缩放点积注意力”。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var K=5,d=4,base=[0.9,0.35,-0.15,0.05,-0.6];
// base 是“归一化后”的相对分数（q·k/√d，典型 spread）。原始点积 = base×√d 随维度放大；÷√d 后即 base、与 d 无关。
function scores(scale){return base.map(function(b){return scale?b:b*Math.sqrt(d);});}
function softmax(s){var m=Math.max.apply(null,s),e=s.map(function(x){return Math.exp(x-m);}),Z=e.reduce(function(a,b){return a+b;},0);return e.map(function(x){return x/Z;});}
var SVGNS="http://www.w3.org/2000/svg";
function E(p,t,a,txt){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;p.appendChild(e);return e;}
function bars(svg,x0,probs,title){
  E(svg,"text",{x:x0+95,y:24,"text-anchor":"middle","class":"ttl"},title);
  var maxP=Math.max.apply(null,probs);
  E(svg,"line",{x1:x0,y1:170,x2:x0+190,y2:170,"class":"axis"});
  for(var k=0;k<K;k++){var h=probs[k]*120,x=x0+10+k*36;
    E(svg,"rect",{x:x,y:170-h,width:26,height:h,rx:2,"class":"bar",opacity:(0.4+0.6*probs[k]).toFixed(2)});
    E(svg,"text",{x:x+13,y:184,"text-anchor":"middle","class":"lbl"},"K"+(k+1));
    E(svg,"text",{x:x+13,y:170-h-4,"text-anchor":"middle","class":"lbl"},(probs[k]*100).toFixed(0));
  }
  E(svg,"text",{x:x0+95,y:204,"text-anchor":"middle","class":"lbl"},"最大权重 "+(maxP*100).toFixed(0)+"%");
}
function render(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var pu=softmax(scores(false)),ps=softmax(scores(true));
  bars(svg,12,pu,"不缩放");
  bars(svg,250,ps,"÷ √d");
  document.getElementById("dVal").textContent=d;
  document.getElementById("stat").textContent="d = "+d+" · 不缩放最大 "+(Math.max.apply(null,pu)*100).toFixed(0)+"% / 缩放 "+(Math.max.apply(null,ps)*100).toFixed(0)+"%";
  caption(Math.max.apply(null,pu),Math.max.apply(null,ps));
}
function caption(mu,ms){
  var el=document.getElementById("caption");
  if(d<=4)el.innerHTML="维度还小（d="+d+"）：不缩放与缩放的差距还不大。把维度往大拖，看左边怎么塌。";
  else el.innerHTML="维度 d="+d+"：不缩放那边最大权重已冲到 <b>"+(mu*100).toFixed(0)+"%</b>（几乎一根独大、softmax 饱和、梯度消失）；÷√d 那边仍只有 <b>"+(ms*100).toFixed(0)+"%</b>，分布柔和、可学。这就是为什么注意力要除以 √d。";
}
document.getElementById("d").addEventListener("input",function(e){d=+e.target.value;render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){d=128;document.getElementById("d").value=128;render();return;}
  var seq=[16,48,128],k=0,sl=document.getElementById("d");var iv=setInterval(function(){d=seq[k];sl.value=d;render();k++;if(k>=seq.length)clearInterval(iv);},1100);},1000);
})();
</script>
{% endraw %}
