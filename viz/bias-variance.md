---
layout: default
title: 偏差与方差
permalink: /viz/bias-variance/
redirect_from:
  - /v/bias-variance/
---

{% raw %}
<style>
.bvlab .axis{stroke:var(--color-border);stroke-width:1;}
.bvlab .truec{fill:none;stroke:var(--color-gold);stroke-width:2.6;stroke-dasharray:6 4;}
.bvlab .fitc{fill:none;stroke:var(--color-accent);stroke-width:1.4;opacity:.28;}
.bvlab .meanc{fill:none;stroke:var(--color-accent);stroke-width:2.8;}
.bvlab .mbar{height:13px;border-radius:7px;background:var(--color-bg-section);overflow:hidden;margin-top:3px;}
.bvlab .mbar i{display:block;height:100%;border-radius:7px;transition:width .3s var(--ease-out);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 偏差与方差

模型的误差可以拆成两部分。**偏差**：模型太简单，根本抓不住真实规律，怎么训都偏；**方差**：模型太灵活，换一批训练数据，学出来的东西就大变样、很不稳定。理想是两者都小，但它们往往此消彼长——这正是“过拟合”的另一面。拖动复杂度，看在多份不同数据上学出的曲线，是“齐刷刷地偏”还是“乱七八糟地飘”。

<section class="vizui bvlab" id="bvlab">
  <p class="vizui__lead">金色虚线是真实规律。每条淡蓝线是用<b>一份不同的随机训练数据</b>学出来的模型，深蓝线是它们的平均。看复杂度低和高时，这些淡蓝线的“齐”与“散”。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="deg">模型复杂度（多项式次数）</label>
        <input type="range" id="deg" min="1" max="9" step="1" value="1" style="width:200px">
        <output id="degVal">1</output>
      </span>
      <span class="vizui-spacer"></span>
      <button class="vizui-btn vizui-btn--go" id="auto" type="button">▶ 自动演示</button>
    </div>
  </div>

  <div class="vizui-grid2">
    <div class="vizui-panel">
      <p class="vizui-panel__title">8 份数据各自学出的曲线</p>
      <svg class="vizui-chart" id="plot" viewBox="0 0 440 260" role="img" aria-label="多份数据的拟合曲线"></svg>
    </div>
    <div class="vizui-panel">
      <p class="vizui-panel__title">误差的两个来源</p>
      <div style="display:flex;justify-content:space-between;font-size:.88rem;margin-top:6px"><span><b>偏差²</b>（平均线离真实有多远）</span><b id="biasV" style="font-family:var(--font-mono);color:#b5524a">—</b></div>
      <div class="mbar"><i id="biasBar" style="background:#b5524a"></i></div>
      <div style="display:flex;justify-content:space-between;font-size:.88rem;margin-top:12px"><span><b>方差</b>（各条线之间有多散）</span><b id="varV" style="font-family:var(--font-mono);color:var(--color-accent)">—</b></div>
      <div class="mbar"><i id="varBar" style="background:var(--color-accent)"></i></div>
      <div style="display:flex;justify-content:space-between;font-size:.88rem;margin-top:12px"><span><b>合计</b>（偏差² + 方差）</span><b id="totV" style="font-family:var(--font-mono);color:var(--color-text)">—</b></div>
      <div class="mbar"><i id="totBar" style="background:var(--color-text-soft)"></i></div>
    </div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:#b5524a"><b>高偏差（太简单）</b><p>曲线齐刷刷地挤在一起，却整体偏离真实——模型表达力不够，欠拟合。</p></div>
    <div class="card" style="--wc:var(--color-accent)"><b>高方差（太复杂）</b><p>换份数据就学出完全不同的曲线，乱飘——模型把噪声也学了，过拟合。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>折中最好</b><p>总误差 = 偏差² + 方差，在中等复杂度处最低；这就是要“恰到好处”的原因。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var K=8, NPTS=10, NS=60, XMIN=-1, XMAX=1, deg=1, datasets=[], playing=false, timer=null;
function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
function gauss(r){var u=0,v=0;while(!u)u=r();while(!v)v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}
function trueF(x){return Math.sin(x*2.5)*0.7;}
function genAll(){datasets=[];for(var k=0;k<K;k++){var r=rng(100+k*7),d=[];for(var i=0;i<NPTS;i++){var x=-1+2*i/(NPTS-1)+gauss(r)*0.03;x=Math.max(-1,Math.min(1,x));d.push([x,trueF(x)+gauss(r)*0.18]);}datasets.push(d);}}

function solve(M,v){var n=v.length,A=M.map(function(r,i){return r.concat([v[i]]);}),col,r,c;
  for(col=0;col<n;col++){var piv=col;for(r=col+1;r<n;r++)if(Math.abs(A[r][col])>Math.abs(A[piv][col]))piv=r;var tmp=A[col];A[col]=A[piv];A[piv]=tmp;var dd=A[col][col]||1e-12;for(r=0;r<n;r++){if(r===col)continue;var f=A[r][col]/dd;for(c=col;c<=n;c++)A[r][c]-=f*A[col][c];}}var x=[];for(var i=0;i<n;i++)x.push(A[i][n]/(A[i][i]||1e-12));return x;}
function polyfit(pts,d){var m=d+1,M=[],V=[],a,b,i;for(a=0;a<m;a++){M.push(new Array(m).fill(0));V.push(0);}
  for(i=0;i<pts.length;i++){var pw=[],p=1;for(b=0;b<m;b++){pw.push(p);p*=pts[i][0];}for(a=0;a<m;a++){V[a]+=pw[a]*pts[i][1];for(b=0;b<m;b++)M[a][b]+=pw[a]*pw[b];}}
  for(var k=0;k<m;k++)M[k][k]+=1e-7;return solve(M,V);}
function polyval(co,x){var y=0,p=1;for(var j=0;j<co.length;j++){y+=co[j]*p;p*=x;}return y;}

var SVGNS="http://www.w3.org/2000/svg",W=440,H=260,pad=18,YMIN=-1.5,YMAX=1.5;
function wx(x){return pad+(x-XMIN)/(XMAX-XMIN)*(W-2*pad);}
function wy(y){return (H-pad)-(y-YMIN)/(YMAX-YMIN)*(H-2*pad);}
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function curve(svg,fn,cls){var p=[];for(var i=0;i<=100;i++){var x=XMIN+(XMAX-XMIN)*i/100,y=Math.max(YMIN-0.3,Math.min(YMAX+0.3,fn(x)));p.push(wx(x)+","+wy(y));}E(svg,"polyline",{points:p.join(" "),"class":cls,"clip-path":"url(#bvclip)"});}

function render(){
  document.getElementById("degVal").textContent=deg;
  var fits=datasets.map(function(d){return polyfit(d,deg);});
  var svg=document.getElementById("plot");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var clip=E(svg,"clipPath",{id:"bvclip"});E(clip,"rect",{x:pad-2,y:2,width:W-2*pad+4,height:H-4});
  E(svg,"line",{x1:pad,y1:wy(0),x2:W-pad,y2:wy(0),"class":"axis"});
  fits.forEach(function(co){curve(svg,function(x){return polyval(co,x);},"fitc");});
  curve(svg,function(x){return (fits.reduce(function(a,co){return a+polyval(co,x);},0))/K;},"meanc");
  curve(svg,trueF,"truec");
  // 偏差²/方差（在密集采样点上）
  var bias=0,vari=0;
  for(var i=0;i<NS;i++){var x=XMIN+(XMAX-XMIN)*i/(NS-1),mean=0,vals=[];fits.forEach(function(co){var y=polyval(co,x);vals.push(y);mean+=y;});mean/=K;
    bias+=(mean-trueF(x))*(mean-trueF(x));var vv=0;vals.forEach(function(y){vv+=(y-mean)*(y-mean);});vari+=vv/K;}
  bias/=NS;vari/=NS;var tot=bias+vari, SC=0.6;
  function setBar(id,val){document.getElementById(id+"V").textContent=val.toFixed(3);document.getElementById(id+"Bar").style.width=Math.min(100,val/SC*100)+"%";}
  setBar("bias",bias);setBar("var",vari);setBar("tot",tot);
  caption(bias,vari);
}
function caption(bias,vari){
  var el=document.getElementById("caption");
  if(deg<=2)el.innerHTML="复杂度低（次数 "+deg+"）：8 条线<b>挤在一起</b>（方差小 "+vari.toFixed(3)+"），但整体偏离金色真实曲线（偏差大 "+bias.toFixed(3)+"）——这是<b>高偏差/欠拟合</b>。";
  else if(deg>=7)el.innerHTML="复杂度高（次数 "+deg+"）：8 条线<b>乱七八糟地飘</b>（方差大 "+vari.toFixed(3)+"），换份数据就大变样——这是<b>高方差/过拟合</b>。";
  else el.innerHTML="次数 "+deg+"：偏差 "+bias.toFixed(3)+"、方差 "+vari.toFixed(3)+"。注意提高复杂度时，偏差往下走、方差往上走——总误差在中间某处最低。";
}
function setDeg(d){deg=Math.max(1,Math.min(9,d));document.getElementById("deg").value=deg;render();}
document.getElementById("deg").addEventListener("input",function(e){stop();setDeg(+e.target.value);});
function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("auto").textContent="▶ 自动演示";}
document.getElementById("auto").addEventListener("click",function(){if(playing){stop();return;}playing=true;document.getElementById("auto").textContent="⏸ 暂停";var d=1;setDeg(1);timer=setInterval(function(){d++;if(d>9){stop();return;}setDeg(d);},700);});

genAll();render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){setDeg(9);return;}document.getElementById("auto").click();},900);
})();
</script>
{% endraw %}
