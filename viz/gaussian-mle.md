---
layout: default
title: 高斯分布与最大似然
permalink: /viz/gaussian-mle/
redirect_from:
  - /v/gaussian-mle/
---

{% raw %}
<style>
.gmlab .axis{stroke:var(--color-border);stroke-width:1;}
.gmlab .curve{fill:var(--color-accent);opacity:.13;stroke:var(--color-accent);stroke-width:2.6;stroke-linejoin:round;}
.gmlab .stick{stroke:var(--color-gold);stroke-width:1.6;opacity:.7;}
.gmlab .pt{fill:var(--color-text);}
.gmlab .alab{font:10px var(--font-mono);fill:var(--color-text-muted);}
.gmlab .llbar{height:14px;border-radius:7px;background:var(--color-bg-section);overflow:hidden;margin-top:4px;}
.gmlab .llbar i{display:block;height:100%;border-radius:7px;background:var(--color-accent);transition:width .25s var(--ease-out);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 高斯分布与最大似然

一堆数据，假设它们来自一个高斯（正态）分布，那这个分布的中心 μ 和宽度 σ 该取多少？“最大似然”给出一个朴素的准则：**选让这批数据出现得最“顺理成章”的参数**。具体说，把每个点在曲线上的高度（概率密度）乘起来（取对数就是相加），谁让这个总和最大，谁就是最优。对高斯来说，答案漂亮得出奇——μ 就是样本均值，σ 就是样本标准差。拖动 μ、σ，看似然怎么在真值处最大。

<section class="gmlab vizui" id="gmlab">
  <p class="vizui__lead">黑点是数据（落在横轴上）。蓝钟形是你假设的高斯，金色竖线是每个点在曲线上的高度。把曲线对准数据、宽窄也合适时，这些高度乘起来（对数似然）最大。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="mu">中心 μ</label><input type="range" id="mu" min="-2" max="2" step="0.05" value="-1.2" style="width:130px"><output id="muVal">-1.2</output></span>
      <span class="vizui-field"><label for="sg">宽度 σ</label><input type="range" id="sg" min="0.25" max="2" step="0.05" value="1.6" style="width:120px"><output id="sgVal">1.6</output></span>
      <span class="vizui-spacer"></span>
      <button class="vizui-btn vizui-btn--go" id="fit" type="button">自动找最优</button>
    </div>
    <svg class="vizui-chart" id="plot" viewBox="0 0 460 250" role="img" aria-label="高斯拟合与似然"></svg>
    <div style="display:flex;justify-content:space-between;font-size:.86rem;margin-top:8px"><span>对数似然（越大越好）</span><b id="ll" style="font-family:var(--font-mono);color:var(--color-accent)">—</b></div>
    <div class="llbar"><i id="llBar"></i></div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>似然 = 数据的“顺理成章”度</b><p>每个点在曲线上的密度相乘；曲线越贴合数据，乘积越大。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>取对数好算</b><p>连乘容易下溢，取对数变成相加，最大值位置不变。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>高斯的最优解</b><p>μ* = 样本均值，σ* = 样本标准差——最大似然给了一个干净的闭式答案。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var mu=-1.2, sg=1.6, data=[];
function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
function gauss(r){var u=0,v=0;while(!u)u=r();while(!v)v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}
(function(){var r=rng(7);for(var i=0;i<16;i++)data.push(0.35+gauss(r)*0.78);})();
var mean=data.reduce(function(a,b){return a+b;},0)/data.length;
var std=Math.sqrt(data.reduce(function(a,b){return a+(b-mean)*(b-mean);},0)/data.length);
function N(x,m,s){return Math.exp(-(x-m)*(x-m)/(2*s*s))/(s*Math.sqrt(2*Math.PI));}
function LL(m,s){var l=0;data.forEach(function(x){l+=Math.log(Math.max(1e-12,N(x,m,s)));});return l;}
var LLmax=LL(mean,std), LLmin=LL(-2,2);
var SVGNS="http://www.w3.org/2000/svg",W=460,H=250,pl=24,pr=16,pt=14,pb=30,XR=3.4,YMAX=0.62;
function px(x){return pl+(x+XR)/(2*XR)*(W-pl-pr);}
function py(y){return (H-pb)-y/YMAX*(H-pt-pb);}
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function draw(){
  var svg=document.getElementById("plot");while(svg.firstChild)svg.removeChild(svg.firstChild);
  E(svg,"line",{x1:pl,y1:H-pb,x2:W-pr,y2:H-pb,"class":"axis"});
  [-3,-2,-1,0,1,2,3].forEach(function(v){E(svg,"text",{x:px(v),y:H-pb+14,"text-anchor":"middle","class":"alab"}).textContent=v;});
  // 曲线
  var cp=[];for(var i=0;i<=120;i++){var x=-XR+2*XR*i/120;cp.push(px(x)+","+py(Math.min(YMAX,N(x,mu,sg))));}
  E(svg,"polygon",{points:px(-XR)+","+(H-pb)+" "+cp.join(" ")+" "+px(XR)+","+(H-pb),"class":"curve"});
  // 竖线 + 点
  data.forEach(function(x){var h=Math.min(YMAX,N(x,mu,sg));E(svg,"line",{x1:px(x),y1:H-pb,x2:px(x),y2:py(h),"class":"stick"});});
  data.forEach(function(x){E(svg,"circle",{cx:px(x),cy:H-pb,r:4,"class":"pt"});});
}
function render(){
  document.getElementById("muVal").textContent=mu.toFixed(2);document.getElementById("sgVal").textContent=sg.toFixed(2);
  var ll=LL(mu,sg);document.getElementById("ll").textContent=ll.toFixed(1);
  document.getElementById("llBar").style.width=Math.max(0,Math.min(100,(ll-LLmin)/(LLmax-LLmin)*100))+"%";
  draw();caption(ll);
}
function caption(ll){
  var el=document.getElementById("caption"),near=Math.abs(mu-mean)<0.12&&Math.abs(sg-std)<0.15;
  if(near)el.innerHTML="<b>到最优了！</b>μ="+mu.toFixed(2)+" 几乎等于样本均值 "+mean.toFixed(2)+"，σ="+sg.toFixed(2)+" 几乎等于样本标准差 "+std.toFixed(2)+"。对数似然达到最大——这就是最大似然估计的答案。";
  else el.innerHTML="当前对数似然 "+ll.toFixed(1)+"。把 μ 往数据中心（约 "+mean.toFixed(2)+"）挪、σ 调到和数据散布（约 "+std.toFixed(2)+"）相当，似然会变大。点“自动找最优”直接跳到答案。";
}
function fitAnim(){var m0=mu,s0=sg,k=0;var iv=setInterval(function(){k++;var t=k/20;mu=m0+(mean-m0)*t;sg=s0+(std-s0)*t;document.getElementById("mu").value=mu;document.getElementById("sg").value=sg;render();if(k>=20)clearInterval(iv);},40);}
document.getElementById("mu").addEventListener("input",function(e){mu=+e.target.value;render();});
document.getElementById("sg").addEventListener("input",function(e){sg=+e.target.value;render();});
document.getElementById("fit").addEventListener("click",fitAnim);
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){mu=mean;sg=std;render();return;}fitAnim();},1100);
})();
</script>
{% endraw %}
