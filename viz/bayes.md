---
layout: default
title: 贝叶斯更新
permalink: /viz/bayes/
redirect_from:
  - /v/bayes/
---

{% raw %}
<style>
.bylab .axis{stroke:var(--color-border);stroke-width:1;}
.bylab .alab{font:10px var(--font-mono);fill:var(--color-text-muted);}
.bylab .dens{fill:var(--color-accent);opacity:.16;stroke:var(--color-accent);stroke-width:2.4;stroke-linejoin:round;}
.bylab .truth{stroke:#b5524a;stroke-width:2;stroke-dasharray:5 4;}
.bylab .mean{stroke:var(--color-gold);stroke-width:1.6;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 贝叶斯更新

手里一枚来路不明的硬币，正面概率 p 是多少？贝叶斯的思路很像人之常情：先有个**先验**信念（一开始啥都不知道，觉得 p 可能是任何值），每抛一次就拿结果去**更新**信念，得到**后验**。抛得越多，信念分布就越窄、越笃定，慢慢逼近硬币真实的偏向。这正是模型“从数据里学参数”的概率版本。抛几次试试。

<section class="bylab vizui" id="bylab">
  <p class="vizui__lead">曲线是当前对 p（正面概率）的信念分布：越高的地方越可能。<span style="color:#b5524a;font-weight:600">红虚线</span>是硬币真实偏向（这里藏着 0.7），<span style="color:var(--color-gold);font-weight:600">金线</span>是当前的估计均值。抛硬币，看曲线怎么往真值收窄。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <button class="vizui-btn" id="h" type="button">抛出正面 ⊕</button>
      <button class="vizui-btn" id="t" type="button">抛出反面 ⊖</button>
      <button class="vizui-btn vizui-btn--go" id="auto" type="button">▶ 自动抛 50 次</button>
      <button class="vizui-btn" id="reset" type="button">重置</button>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stat">正0 反0</span>
    </div>
    <svg class="vizui-chart" id="plot" viewBox="0 0 460 250" role="img" aria-label="p 的后验分布"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>先验：起点信念</b><p>没数据时，对 p 一无所知，分布是平的——任何值都有可能。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>更新：乘以似然</b><p>每个结果都让“与之相符的 p”更可信、不符的更不可信，分布随之移动、收窄。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>数据越多越笃定</b><p>抛得越多，后验越窄、越集中在真值附近——这就是“从经验中学习”。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var TRUE=0.7, a=1, b=1, playing=false, timer=null;
function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
var rnd=rng(9);
var SVGNS="http://www.w3.org/2000/svg",W=460,H=250,pl=30,pr=16,pt=16,pb=30;
function px(p){return pl+p*(W-pl-pr);}
function E(p,t,at){var e=document.createElementNS(SVGNS,t);for(var k in at)e.setAttribute(k,at[k]);p.appendChild(e);return e;}
function dens(){var n=120,ys=[],maxld=-1e9,lds=[];
  for(var i=0;i<=n;i++){var p=i/n,ld=(a-1)*Math.log(p||1e-9)+(b-1)*Math.log((1-p)||1e-9);lds.push(ld);if(ld>maxld)maxld=ld;}
  for(var j=0;j<=n;j++)ys.push(Math.exp(lds[j]-maxld));
  return ys;}
function draw(){
  var svg=document.getElementById("plot");while(svg.firstChild)svg.removeChild(svg.firstChild);
  E(svg,"line",{x1:pl,y1:H-pb,x2:W-pr,y2:H-pb,"class":"axis"});
  [0,0.25,0.5,0.75,1].forEach(function(v){E(svg,"text",{x:px(v),y:H-pb+14,"text-anchor":"middle","class":"alab"}).textContent=v;});
  E(svg,"text",{x:(pl+W-pr)/2,y:H-6,"text-anchor":"middle","class":"alab"}).textContent="p（正面概率）";
  var ys=dens(),n=ys.length-1,top=pt+6;
  var pts=[px(0)+","+(H-pb)];for(var i=0;i<=n;i++)pts.push(px(i/n)+","+((H-pb)-ys[i]*(H-pb-top)));pts.push(px(1)+","+(H-pb));
  E(svg,"polygon",{points:pts.join(" "),"class":"dens"});
  E(svg,"line",{x1:px(TRUE),y1:top-4,x2:px(TRUE),y2:H-pb,"class":"truth"});
  E(svg,"text",{x:px(TRUE),y:top-6,"text-anchor":"middle","class":"alab",style:"fill:#b5524a"}).textContent="真值 0.7";
  var mean=a/(a+b);E(svg,"line",{x1:px(mean),y1:top,x2:px(mean),y2:H-pb,"class":"mean"});
}
function render(){document.getElementById("stat").textContent="正"+(a-1)+" 反"+(b-1)+" · 估计 "+(a/(a+b)).toFixed(2);draw();caption();}
function caption(){
  var el=document.getElementById("caption"),N=a+b-2,sd=Math.sqrt(a*b/((a+b)*(a+b)*(a+b+1)));
  if(N===0)el.innerHTML="还没抛：曲线是平的（先验），对 p 毫无偏好。开始抛硬币吧。";
  else if(N<8)el.innerHTML="抛了 "+N+" 次：曲线开始往有结果的方向鼓起来，但还很宽——数据太少，不敢下结论。";
  else el.innerHTML="抛了 "+N+" 次：后验已经收窄并聚到 <b>"+(a/(a+b)).toFixed(2)+"</b> 附近，离真值 0.7 不远了（不确定度 ±"+(sd).toFixed(2)+"）。再抛更多会更窄、更准。";
}
function flip(head){if(head)a++;else b++;render();}
function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("auto").textContent="▶ 自动抛 50 次";}
document.getElementById("h").addEventListener("click",function(){stop();flip(true);});
document.getElementById("t").addEventListener("click",function(){stop();flip(false);});
document.getElementById("auto").addEventListener("click",function(){if(playing){stop();return;}playing=true;document.getElementById("auto").textContent="⏸ 暂停";var n=0;timer=setInterval(function(){flip(rnd()<TRUE);n++;if(n>=50)stop();},90);});
document.getElementById("reset").addEventListener("click",function(){stop();a=1;b=1;render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){for(var i=0;i<40;i++)flip(rnd()<TRUE);return;}document.getElementById("auto").click();},1000);
})();
</script>
{% endraw %}
