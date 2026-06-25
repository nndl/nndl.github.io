---
layout: default
title: 大数定律
description: "一直抛硬币，正面频率从剧烈抖动慢慢稳稳逼近真实概率——样本越多越准。"
permalink: /viz/law-large-numbers/
redirect_from:
  - /v/law-large-numbers/
---

{% raw %}
<style>
.lllab .axis{stroke:var(--color-border);stroke-width:1;}
.lllab .alab{font:10px var(--font-mono);fill:var(--color-text-muted);}
.lllab .trueline{stroke:#b5524a;stroke-width:1.6;stroke-dasharray:5 4;}
.lllab .freq{fill:none;stroke:var(--color-accent);stroke-width:2;}
.lllab .band{fill:var(--color-accent);opacity:.06;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 大数定律

抛一枚硬币，正面概率是 0.6。只抛 5 次，可能 4 次正面（80%）也可能 1 次（20%），离 0.6 差得远。但只要一直抛下去，正面出现的比例会**越来越稳地逼近 0.6**。这就是大数定律：样本越多，频率越接近真实概率。它是“用频率估计概率”“多做实验更可靠”这些直觉的严格保证，也是为什么训练数据越多、统计越靠谱。点“开始抛”，看频率曲线怎么从剧烈抖动慢慢收敛到那条红线。

<section class="lllab vizui" id="lllab">
  <p class="vizui__lead">横轴是抛硬币的次数，纵轴是到目前为止正面出现的比例（频率）。红色虚线是真实概率。注意曲线一开始上下乱跳，越往后越贴着红线。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="p">真实概率 p</label><input type="range" id="p" min="0.1" max="0.9" step="0.05" value="0.6" style="width:130px"><output id="pVal">0.60</output></span>
      <span class="vizui-spacer"></span>
      <button class="vizui-btn vizui-btn--go" id="go" type="button">▶ 开始抛</button>
      <button class="vizui-btn" id="reset" type="button">重置</button>
      <span class="vizui-pill" id="stat">0 次</span>
    </div>
    <svg class="vizui-chart" id="plot" viewBox="0 0 460 240" role="img" aria-label="频率收敛曲线"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:#b5524a"><b>少量样本会骗人</b><p>抛几次，频率可能离真实概率很远——小样本的随机波动很大。</p></div>
    <div class="card" style="--wc:var(--color-accent)"><b>越多越准</b><p>随着次数增加，正负波动互相抵消，频率稳稳收敛到真实概率。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>为什么重要</b><p>它让“用频率估计概率”“多做实验/多取数据更可靠”有了理论保证。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var p=0.6, total=0, heads=0, hist=[], playing=false, timer=null, NMAX=700;
var SVGNS="http://www.w3.org/2000/svg",W=460,H=240,pl=34,pr=14,pt=14,pb=26;
function px(n){return pl+n/NMAX*(W-pl-pr);}
function py(f){return (H-pb)-f*(H-pt-pb);}
function E(e,t,a){var x=document.createElementNS(SVGNS,t);for(var k in a)x.setAttribute(k,a[k]);e.appendChild(x);return x;}
function draw(){
  var svg=document.getElementById("plot");while(svg.firstChild)svg.removeChild(svg.firstChild);
  [0,0.25,0.5,0.75,1].forEach(function(v){E(svg,"text",{x:pl-5,y:py(v)+3,"text-anchor":"end","class":"alab"}).textContent=v.toFixed(2);});
  E(svg,"line",{x1:pl,y1:H-pb,x2:W-pr,y2:H-pb,"class":"axis"});E(svg,"line",{x1:pl,y1:pt,x2:pl,y2:H-pb,"class":"axis"});
  [0,200,400,600].forEach(function(n){E(svg,"text",{x:px(n),y:H-pb+14,"text-anchor":"middle","class":"alab"}).textContent=n;});
  E(svg,"line",{x1:pl,y1:py(p),x2:W-pr,y2:py(p),"class":"trueline"});
  E(svg,"text",{x:W-pr,y:py(p)-5,"text-anchor":"end","class":"alab",style:"fill:#b5524a"}).textContent="真实 "+p.toFixed(2);
  if(hist.length>1){var pts=hist.map(function(h){return px(h[0])+","+py(h[1]);});E(svg,"polyline",{points:pts.join(" "),"class":"freq"});}
}
function flip(batch){for(var i=0;i<batch;i++){total++;if(Math.random()<p)heads++;if(total<=NMAX&&(total<40||total%3===0))hist.push([total,heads/total]);}}
function render(){document.getElementById("pVal").textContent=p.toFixed(2);document.getElementById("stat").textContent=total+" 次 · 频率 "+(total?(heads/total).toFixed(3):"—");draw();caption();}
function caption(){
  var el=document.getElementById("caption"),f=total?heads/total:0;
  if(total===0)el.innerHTML="点“开始抛”。一开始次数少，频率会上下乱跳、离红线很远——别被前几次骗了。";
  else if(total<50)el.innerHTML="才抛了 "+total+" 次，频率 "+f.toFixed(2)+"，还在剧烈抖动，可能和真实 "+p.toFixed(2)+" 差不少。继续抛。";
  else el.innerHTML="抛了 "+total+" 次，频率 "+f.toFixed(3)+" 已经很贴近真实概率 "+p.toFixed(2)+" 了，而且越往后越稳——这就是大数定律。";
}
function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("go").textContent="▶ 开始抛";}
function play(){if(total>=NMAX){total=0;heads=0;hist=[];}stop();playing=true;document.getElementById("go").textContent="⏸ 暂停";
  timer=setInterval(function(){flip(total<60?1:8);render();if(total>=NMAX)stop();},45);}
document.getElementById("go").addEventListener("click",function(){playing?stop():play();});
document.getElementById("reset").addEventListener("click",function(){stop();total=0;heads=0;hist=[];render();});
document.getElementById("p").addEventListener("input",function(e){p=+e.target.value;stop();total=0;heads=0;hist=[];render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){flip(700);render();return;}play();},1000);
})();
</script>
{% endraw %}
