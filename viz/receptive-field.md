---
layout: default
title: 卷积的感受野
permalink: /viz/receptive-field/
redirect_from:
  - /v/receptive-field/
---

{% raw %}
<style>
.rflab svg{max-width:100%;height:auto;background:var(--color-bg-soft,#f4f1ec);border-radius:var(--radius-sm);}
.rflab .neuron{fill:#cdd6db;stroke:#fff;stroke-width:1;}
.rflab .neuron.on{fill:var(--color-accent);}
.rflab .neuron.top{fill:var(--color-gold);stroke:#fff;stroke-width:1.5;}
.rflab .cone{fill:var(--color-accent);opacity:.12;stroke:none;}
.rflab .rlbl{font:11px var(--font-sans);fill:var(--color-text-muted);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 卷积的感受野

卷积每次只看一个小窗口（比如 3 个像素），似乎“目光短浅”。但只要一层层往上叠，高层的一个神经元，能间接“看到”输入里越来越大的一片——这片范围叫它的**感受野**。这就是为什么深层卷积网络不靠大卷积核，也能理解整张图的全局结构：**深度换来了广度**。拖动“层数”滑块，看最顶上那个金色神经元的视野（蓝色锥形）怎样随深度一层层张开。

<section class="vizui rflab" id="rflab">
  <p class="vizui__lead">最下面一行是输入像素，往上每一行是一层卷积（核大小 3）。金色是顶层那个神经元，蓝色锥形圈出它最终依赖的输入像素——就是它的感受野。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="L">卷积层数</label><input type="range" id="L" min="1" max="6" step="1" value="1" style="width:160px"><output id="lVal">1</output></span>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stat">—</span>
    </div>
    <svg id="plane" viewBox="0 0 560 320" role="img" aria-label="感受野"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-gold)"><b>小窗口</b><p>每层只看相邻 3 个，参数少、计算省。单看一层确实“目光短浅”。</p></div>
    <div class="card" style="--wc:var(--color-accent)"><b>叠出大视野</b><p>核大小 3 时，每加一层感受野就 ±1，L 层后顶层能看到 2L+1 个输入像素。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>深度换广度</b><p>不必用大卷积核，靠堆深度就能覆盖全局——这是 CNN 高效的关键之一。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var K=21, center=10, L=1;
var SVGNS="http://www.w3.org/2000/svg",W=560,H=320,padX=46,padY=26;
function nx(j){return padX+j*((W-2*padX)/(K-1));}
function ny(r){return (H-padY)-r*((H-2*padY)/6);}
function E(p,t,a,txt){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;p.appendChild(e);return e;}
function render(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  // 锥形：顶层神经元(center,row L) 向下张到输入 [center-L, center+L]
  var topx=nx(center),topy=ny(L),il=nx(Math.max(0,center-L)),ir=nx(Math.min(K-1,center+L)),iy=ny(0);
  E(svg,"polygon",{points:topx+","+topy+" "+il+","+iy+" "+ir+","+iy,"class":"cone"});
  for(var r=0;r<=L;r++){
    var rad=L-r; // 该行被覆盖的半径
    for(var j=0;j<K;j++){
      var on=Math.abs(j-center)<=rad;
      var cls="neuron"+(r===L&&j===center?" top":(on?" on":""));
      E(svg,"circle",{cx:nx(j),cy:ny(r),r:(r===L&&j===center)?8:6,"class":cls});
    }
    E(svg,"text",{x:6,y:ny(r)+4,"class":"rlbl"}, r===0?"输入":("第"+r+"层"));
  }
  var rf=2*L+1;
  document.getElementById("lVal").textContent=L;
  document.getElementById("stat").textContent="感受野 = "+rf+" 个输入像素";
  caption(rf);
}
function caption(rf){
  var el=document.getElementById("caption");
  el.innerHTML="叠 <b>"+L+"</b> 层卷积后，最顶上这一个神经元的输出，由输入里 <b>"+rf+"</b> 个像素共同决定（2×"+L+"+1）。"+(L>=5?"已经覆盖了大半个输入——靠堆深度就把视野撑开了。":"继续加层，看蓝色锥形怎样越张越宽。");
}
document.getElementById("L").addEventListener("input",function(e){L=+e.target.value;render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){L=6;document.getElementById("L").value=6;render();return;}
  var seq=[2,3,4,5,6],k=0,sl=document.getElementById("L");
  var iv=setInterval(function(){L=seq[k];sl.value=L;render();k++;if(k>=seq.length)clearInterval(iv);},900);},1000);
})();
</script>
{% endraw %}
