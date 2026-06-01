---
layout: default
title: 中心极限定理
permalink: /viz/clt/
redirect_from:
  - /v/clt/
---

{% raw %}
<style>
.cltlab .axis{stroke:var(--color-border);stroke-width:1;}
.cltlab .bar{fill:var(--color-accent);opacity:.75;}
.cltlab .gauss{fill:none;stroke:var(--color-gold);stroke-width:2.6;}
.cltlab .src .bar{fill:var(--color-text-muted);opacity:.6;}
.cltlab .heads{display:inline-flex;gap:4px;padding:4px;background:var(--color-bg-section);border:1px solid var(--color-border);border-radius:999px;}
.cltlab .heads button{appearance:none;border:0;background:transparent;cursor:pointer;font:inherit;font-size:.86rem;color:var(--color-text-soft);padding:6px 13px;border-radius:999px;}
.cltlab .heads button.on{background:var(--color-bg-pure);color:var(--color-accent);font-weight:600;box-shadow:var(--shadow-sm);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 中心极限定理

随便挑一个分布——均匀的、偏斜的、双峰的，长得多奇怪都行。每次从它里面抽 n 个数、求个平均，把这些平均值的分布画出来。神奇的事发生了：只要 n 稍微大一点，这些**平均值的分布总会变成一个漂亮的高斯钟形**，跟原始分布长什么样几乎无关。这就是中心极限定理——它解释了为什么高斯分布在自然界和统计里无处不在。换个原始分布、拖动 n，看钟形怎么浮现。

<section class="cltlab vizui" id="cltlab">
  <p class="vizui__lead">上面小图是<b>原始分布</b>（灰）。下面大图是“每次抽 n 个求平均”得到的<b>平均值分布</b>（蓝），金线是理论高斯。n 越大，蓝色直方图越像钟形、越窄。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="heads" id="heads"><button data-s="0" class="on" type="button">均匀</button><button data-s="1" type="button">偏斜</button><button data-s="2" type="button">双峰</button></span>
      <span class="vizui-field"><label for="n">每次抽样个数 n</label><input type="range" id="n" min="1" max="30" step="1" value="1" style="width:150px"><output id="nVal">1</output></span>
      <span class="vizui-spacer"></span>
      <button class="vizui-btn" id="resample" type="button">↻ 重新抽样</button>
    </div>
    <svg class="vizui-chart src" id="src" viewBox="0 0 440 70" style="max-height:80px" role="img" aria-label="原始分布"></svg>
    <svg class="vizui-chart" id="plot" viewBox="0 0 440 210" role="img" aria-label="样本均值分布"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>平均“抹平”怪异</b><p>多个随机数相加平均，互相的高低起伏被中和，结果趋向规整的钟形。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>与原分布无关</b><p>不管原始分布多奇怪，n 够大时平均值都近似高斯，中心在原分布的均值。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>越平均越准</b><p>平均值的散布 = 原标准差 ÷ √n——样本越多，估计越集中、越可靠。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var src=0, n=1, NB=44, TRIALS=4000;
function sample(){
  if(src===0)return Math.random();
  if(src===1)return Math.pow(Math.random(),2.6);
  var u=Math.random();return u<0.5?0.13+Math.random()*0.13:0.74+Math.random()*0.13;
}
function srcStats(){var N=8000,s=0,s2=0;for(var i=0;i<N;i++){var v=sample();s+=v;s2+=v*v;}var m=s/N;return {mean:m,std:Math.sqrt(s2/N-m*m)};}
var stat=srcStats();
function hist(getter,trials){var b=new Array(NB).fill(0);for(var i=0;i<trials;i++){var v=getter();var k=Math.floor(v*NB);if(k<0)k=0;if(k>=NB)k=NB-1;b[k]++;}return b;}
var SVGNS="http://www.w3.org/2000/svg";
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function drawHist(id,bins,gauss){
  var svg=document.getElementById(id),W=440,H=svg.id==="src"?70:210,pad=svg.id==="src"?4:14,pb=svg.id==="src"?2:20;
  while(svg.firstChild)svg.removeChild(svg.firstChild);
  var max=Math.max.apply(null,bins)||1,bw=(W-2*pad)/NB;
  E(svg,"line",{x1:pad,y1:H-pb,x2:W-pad,y2:H-pb,"class":"axis"});
  bins.forEach(function(c,i){var h=c/max*(H-pb-pad);E(svg,"rect",{x:pad+i*bw,y:(H-pb)-h,width:bw-0.6,height:h,"class":"bar"});});
  if(gauss){var pts=[];for(var i=0;i<=120;i++){var x=i/120,g=Math.exp(-(x-stat.mean)*(x-stat.mean)/(2*gauss*gauss));pts.push((pad+x*(W-2*pad))+","+((H-pb)-g*(H-pb-pad)));}E(svg,"polyline",{points:pts.join(" "),"class":"gauss"});}
}
function render(){
  document.getElementById("nVal").textContent=n;
  drawHist("src",hist(sample,6000),null);
  var meanGetter=function(){var s=0;for(var i=0;i<n;i++)s+=sample();return s/n;};
  var bins=hist(meanGetter,TRIALS);
  // 理论高斯标准差 = 原std/√n，转成直方图高度比例需匹配峰值，这里只画形状（按 max 归一）
  var sd=stat.std/Math.sqrt(n);
  drawHist("plot",bins,sd>0.002?sd*Math.SQRT2*1.0:0.01);   /* 用 sd 控制钟形宽度 */
  caption(sd);
}
function caption(sd){
  var el=document.getElementById("caption");
  if(n===1)el.innerHTML="n=1：每次只抽 1 个，所谓“平均”就是它本身——所以蓝图和上面的原始分布一模一样，一点都不像钟形。把 n 拖大。";
  else if(n<8)el.innerHTML="n="+n+"：开始抽 "+n+" 个求平均，分布在往中间收、慢慢鼓成钟形了，金色高斯越来越贴合。";
  else el.innerHTML="n="+n+"：平均值的分布已经是一条漂亮的<b>高斯钟形</b>，紧紧聚在原均值 "+stat.mean.toFixed(2)+" 附近（散布≈原std/√n）。原始分布是均匀/偏斜/双峰都无所谓——这就是中心极限定理。";
}
document.getElementById("heads").addEventListener("click",function(e){var b=e.target.closest("button");if(!b)return;src=+b.dataset.s;document.querySelectorAll("#heads button").forEach(function(x){x.classList.toggle("on",+x.dataset.s===src);});stat=srcStats();render();});
document.getElementById("n").addEventListener("input",function(e){n=+e.target.value;render();});
document.getElementById("resample").addEventListener("click",render);
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){n=20;render();return;}
  var seq=[1,2,4,8,16,28],k=0,sl=document.getElementById("n");var iv=setInterval(function(){n=seq[k];sl.value=n;render();k++;if(k>=seq.length)clearInterval(iv);},850);},1000);
})();
</script>
{% endraw %}
