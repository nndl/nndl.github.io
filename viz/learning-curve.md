---
layout: default
title: 学习曲线：该加数据还是加模型
description: "拖数据量看训练/验证误差怎么收敛：两条都卡高处=高偏差(该换强模型)、差距大且验证还在降=高方差(该加数据)。"
permalink: /viz/learning-curve/
redirect_from:
  - /v/learning-curve/
---

{% raw %}
<style>
.lclab .axis{stroke:var(--color-border);stroke-width:1;}
.lclab .grid{stroke:var(--color-border);stroke-width:1;opacity:.35;}
.lclab .alab{font:11px var(--font-mono);fill:var(--color-text-muted);}
.lclab .gapfill{fill:var(--color-gold);opacity:.14;}
.lclab .curve-train{fill:none;stroke:#b5524a;stroke-width:2.8;stroke-linejoin:round;}
.lclab .curve-val{fill:none;stroke:var(--color-accent);stroke-width:2.8;stroke-linejoin:round;}
.lclab .floorline{stroke:var(--color-text-muted);stroke-width:1.3;stroke-dasharray:4 4;opacity:.7;}
.lclab .enddot{stroke:#fff;stroke-width:1.6;}
.lclab .axtitle{font:600 11px var(--font-sans);fill:var(--color-text-soft);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 学习曲线：该加数据还是加模型

模型效果不好，你的第一反应该是“再标注一万条数据”，还是“换个更大的模型”？盲目堆哪一个都可能白烧钱。**学习曲线**给了一张诊断图：固定模型，把训练集从小到大慢慢喂，画出训练误差和验证误差随数据量怎么变。两条线收成什么形状，直接告诉你病根在哪——是数据不够，还是模型太弱。拖动“模型复杂度”，看这张图的形状如何翻转。

<section class="vizui lclab" id="lclab">
  <p class="vizui__lead">横轴是<b>训练集大小 m</b>。<span style="color:#b5524a;font-weight:600">红线</span>是训练误差，<span style="color:var(--color-accent);font-weight:600">青线</span>是验证误差（在一份固定的干净数据上算）。数据越多越难“背”，训练误差升；学到的规律越靠谱，验证误差降。金色阴影是两者的<b>差距</b>。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="deg">模型复杂度（多项式次数）</label>
        <input type="range" id="deg" min="1" max="9" step="1" value="1" style="width:200px">
        <output id="degVal">1</output>
      </span>
      <span class="vizui-field"><label for="noise">数据噪声</label>
        <input type="range" id="noise" min="6" max="24" step="2" value="13" style="width:120px">
        <output id="noiseVal">0.13</output>
      </span>
      <span class="vizui-spacer"></span>
      <button class="vizui-btn vizui-btn--go" id="auto" type="button">▶ 自动演示</button>
    </div>
  </div>

  <div class="vizui-grid2">
    <div class="vizui-panel">
      <p class="vizui-panel__title">学习曲线：误差 vs 训练集大小</p>
      <svg class="vizui-chart" id="chartLc" viewBox="0 0 440 270" role="img" aria-label="训练误差与验证误差随数据量变化"></svg>
    </div>
    <div class="vizui-panel">
      <p class="vizui-panel__title">读数</p>
      <div style="display:flex;justify-content:space-between;font-size:.9rem;margin-top:8px"><span><b>验证误差地板</b>（m = 40 处）</span><b id="vaEnd" style="font-family:var(--font-mono);color:var(--color-accent)">—</b></div>
      <div style="display:flex;justify-content:space-between;font-size:.9rem;margin-top:10px"><span><b>验证误差降了多少</b>（小 m → 大 m）</span><b id="drop" style="font-family:var(--font-mono);color:var(--color-forest)">—</b></div>
      <div style="display:flex;justify-content:space-between;font-size:.9rem;margin-top:10px"><span><b>小数据时的差距</b>（验证 − 训练）</span><b id="gap0" style="font-family:var(--font-mono);color:var(--color-gold)">—</b></div>
      <div style="display:flex;justify-content:space-between;font-size:.9rem;margin-top:10px"><span><b>验证误差还在降吗</b></span><b id="slope" style="font-family:var(--font-mono);color:var(--color-text)">—</b></div>
      <div style="margin-top:16px;padding:10px 12px;border-radius:var(--radius-md);background:var(--color-bg-section);font-size:.85rem;color:var(--color-text-soft)">
        验证误差降得多 + 还在降 → <b>加数据有用</b>；<br>很快收平、卡在高处 → <b>加数据没用，要换更强的模型</b>。
      </div>
    </div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-gold)"><b>高偏差 / 欠拟合</b><p>两条线很快收到一起，却一起卡在高处下不来。模型表达力不够，再喂多少数据都没用——该换更强的模型。</p></div>
    <div class="card" style="--wc:var(--color-accent)"><b>高方差 / 过拟合</b><p>训练误差贴地、验证误差高悬，中间一道大缝。但验证误差随数据量一直在降——再加数据真能补上这道缝。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>先看形状，再花钱</b><p>同一份不满意的结果，曲线的形状决定你该往“数据”还是“模型”那边砸钱，而不是凭感觉两边都试。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var MMIN=3, MMAX=40, K=12, NVAL=80, RIDGE=1e-7, XMIN=-1, XMAX=1, JIT=0.035;
var deg=1, noise=0.13, playing=false, timer=null;

/* 确定性随机数（seeded），保证可复现 */
function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
function gauss(r){var u=0,v=0;while(!u)u=r();while(!v)v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}
/* 真实规律：一条平滑不振荡的 S 形曲线 */
function trueF(x){return 1.7/(1+Math.exp(-3.6*x))-0.85;}

/* 固定的、干净的密集验证网格 */
var VAL=[];for(var i=0;i<NVAL;i++){var vx=XMIN+(XMAX-XMIN)*i/(NVAL-1);VAL.push([vx,trueF(vx)]);}

/* 多项式最小二乘（正规方程 + 微小岭正则 + 高斯消元） */
function solve(M,v){var n=v.length,A=M.map(function(row,i){return row.concat([v[i]]);}),col,r,c;
  for(col=0;col<n;col++){var piv=col;for(r=col+1;r<n;r++)if(Math.abs(A[r][col])>Math.abs(A[piv][col]))piv=r;var tmp=A[col];A[col]=A[piv];A[piv]=tmp;var dd=A[col][col]||1e-12;for(r=0;r<n;r++){if(r===col)continue;var f=A[r][col]/dd;for(c=col;c<=n;c++)A[r][c]-=f*A[col][c];}}var x=[];for(var i2=0;i2<n;i2++)x.push(A[i2][n]/(A[i2][i2]||1e-12));return x;}
function polyfit(pts,d){var m=d+1,n=pts.length,M=[],v=[],a,b,i;for(a=0;a<m;a++){M.push(new Array(m).fill(0));v.push(0);}
  for(i=0;i<n;i++){var pw=[],p=1;for(b=0;b<m;b++){pw.push(p);p*=pts[i][0];}for(a=0;a<m;a++){v[a]+=pw[a]*pts[i][1];for(b=0;b<m;b++)M[a][b]+=pw[a]*pw[b];}}
  for(var k=0;k<m;k++)M[k][k]+=RIDGE;return solve(M,v);}
function polyval(co,x){var y=0,p=1;for(var j=0;j<co.length;j++){y+=co[j]*p;p*=x;}return y;}
function mse(co,pts){var s=0;for(var i=0;i<pts.length;i++){var e=polyval(co,pts[i][0])-pts[i][1];s+=e*e;}return s/pts.length;}

/* 对每个训练集大小 m，平均 K 份 seeded 抽样：训练误差用这 m 个点、验证误差用固定网格 */
function computeCurves(d,nz){
  var pts2=[];
  for(var m=MMIN;m<=MMAX;m++){
    var te=0,ve=0;
    for(var k=0;k<K;k++){
      var r=rng(1000+k*97+m*13), pts=[];
      for(var i=0;i<m;i++){var x=XMIN+(XMAX-XMIN)*i/(m-1)+gauss(r)*JIT;x=Math.max(-1,Math.min(1,x));pts.push([x,trueF(x)+gauss(r)*nz]);}
      var co=polyfit(pts,d);
      te+=mse(co,pts); ve+=mse(co,VAL);
    }
    pts2.push({m:m,tr:te/K,va:ve/K});
  }
  return pts2;
}

/* ---------- 绘图 ---------- */
var SVGNS="http://www.w3.org/2000/svg",W=440,H=270,pl=42,pr=14,pt=16,pb=34;
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function clear(svg){while(svg.firstChild)svg.removeChild(svg.firstChild);}
function mx(m){return pl+(m-MMIN)/(MMAX-MMIN)*(W-pl-pr);}

function render(){
  document.getElementById("degVal").textContent=deg;
  document.getElementById("noiseVal").textContent=noise.toFixed(2);
  var data=computeCurves(deg,noise);
  var last=data[data.length-1], first=data[0];
  /* y 轴随当前曲线自适应，避免低复杂度时浪费空间、高复杂度时超框 */
  var ymax=0;data.forEach(function(d){ymax=Math.max(ymax,d.tr,d.va);});
  ymax=Math.max(ymax*1.12,0.03);
  function my(v){return (H-pb)-Math.min(v,ymax)/ymax*(H-pt-pb);}

  var svg=document.getElementById("chartLc");clear(svg);
  /* 网格 + 轴 */
  for(var g=1;g<=4;g++){var yy=my(ymax*g/5);E(svg,"line",{x1:pl,y1:yy,x2:W-pr,y2:yy,"class":"grid"});}
  E(svg,"line",{x1:pl,y1:H-pb,x2:W-pr,y2:H-pb,"class":"axis"});
  E(svg,"line",{x1:pl,y1:pt,x2:pl,y2:H-pb,"class":"axis"});
  for(var mm=10;mm<=40;mm+=10)E(svg,"text",{x:mx(mm),y:H-pb+15,"text-anchor":"middle","class":"alab"}).textContent=mm;
  E(svg,"text",{x:(pl+W-pr)/2,y:H-6,"text-anchor":"middle","class":"axtitle"}).textContent="训练集大小 m →";
  E(svg,"text",{x:pl-6,y:pt+2,"text-anchor":"end","class":"alab"}).textContent="误差";

  /* 差距阴影：验证曲线与训练曲线之间 */
  var up=[],dn=[];
  data.forEach(function(d){up.push(mx(d.m)+","+my(d.va));});
  for(var i=data.length-1;i>=0;i--)dn.push(mx(data[i].m)+","+my(data[i].tr));
  E(svg,"polygon",{points:up.concat(dn).join(" "),"class":"gapfill"});

  /* 高偏差时画出验证误差的“地板线”，强调它卡住了 */
  var flat=Math.abs(last.va-data[Math.max(0,data.length-12)].va);
  if(flat<0.004){E(svg,"line",{x1:pl,y1:my(last.va),x2:W-pr,y2:my(last.va),"class":"floorline"});}

  /* 两条曲线 */
  function line(key,cls){var p=[];data.forEach(function(d){p.push(mx(d.m)+","+my(d[key]));});E(svg,"polyline",{points:p.join(" "),"class":cls});}
  line("tr","curve-train");line("va","curve-val");
  E(svg,"circle",{cx:mx(last.m),cy:my(last.tr),r:4,fill:"#b5524a","class":"enddot"});
  E(svg,"circle",{cx:mx(last.m),cy:my(last.va),r:4,fill:"var(--color-accent)","class":"enddot"});
  /* 曲线标签 */
  E(svg,"text",{x:mx(first.m)+4,y:my(first.va)-6,style:"font:600 11px var(--font-mono);fill:var(--color-accent)"}).textContent="验证";
  E(svg,"text",{x:mx(first.m)+4,y:my(first.tr)+14,style:"font:600 11px var(--font-mono);fill:#b5524a"}).textContent="训练";

  /* 读数面板：用整条曲线的形状来诊断，而不是只看 m=40 那一点 */
  var vaDrop=first.va-last.va;        /* 验证误差从小 m 到大 m 一共降了多少 */
  var earlyGap=first.va-first.tr;     /* 小数据时的差距（高方差最明显处） */
  /* 验证误差后半段还在不在降 */
  var midVa=data[Math.round(data.length*0.55)].va, stillFalling=(last.va<midVa-0.001);
  document.getElementById("vaEnd").textContent=last.va.toFixed(4);
  document.getElementById("drop").textContent="−"+vaDrop.toFixed(4);
  document.getElementById("gap0").textContent=(earlyGap>=0?"+":"")+earlyGap.toFixed(4);
  document.getElementById("slope").textContent=stillFalling?"还在降":"已收平";
  document.getElementById("slope").style.color=stillFalling?"var(--color-accent)":"var(--color-gold)";

  caption(first,last,vaDrop,earlyGap,stillFalling);
}

function caption(first,last,vaDrop,earlyGap,stillFalling){
  var el=document.getElementById("caption");
  var highBias=(last.va>0.006 && vaDrop<0.018);            /* 验证误差卡在高处、没怎么降 */
  var highVar=(earlyGap>0.02 && vaDrop>0.02 && stillFalling); /* 小数据差距大、降幅大、还在降 */
  if(highBias){
    el.innerHTML="次数 "+deg+"：两条线很快收到一起、却一起卡在高处（验证误差只从 "+first.va.toFixed(4)+" 降到 "+last.va.toFixed(4)+" 就收平了）——这是<b>高偏差 / 欠拟合</b>。再加多少数据也没用，要换<b>更强的模型</b>（把次数调大试试）。";
  }else if(highVar){
    el.innerHTML="次数 "+deg+"：小数据时训练误差贴地、验证误差高悬，中间一道大缝（差距 "+earlyGap.toFixed(4)+"）；但验证误差随数据量<b>一路从 "+first.va.toFixed(4)+" 降到 "+last.va.toFixed(4)+"、还没到底</b>——这是<b>高方差 / 过拟合</b>，<b>加数据有用</b>。";
  }else{
    el.innerHTML="次数 "+deg+"：验证误差从 "+first.va.toFixed(4)+" 降到 "+last.va.toFixed(4)+"（降了 "+vaDrop.toFixed(4)+"）。看它是“很快收平卡高处”（缺模型）还是“留着大缝还在往下掉”（缺数据）。";
  }
}

/* ---------- 交互 ---------- */
function setDeg(d){deg=Math.max(1,Math.min(9,d));document.getElementById("deg").value=deg;render();}
function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("auto").textContent="▶ 自动演示";}
document.getElementById("deg").addEventListener("input",function(e){stop();setDeg(+e.target.value);});
document.getElementById("noise").addEventListener("input",function(e){stop();noise=(+e.target.value)/100;render();});
/* 自动演示：从 d=1（高偏差）一路升到 d=8（高方差），跑一遍后停在 d=8 */
function auto(){
  stop();playing=true;document.getElementById("auto").textContent="⏸ 暂停";var d=1;setDeg(1);
  timer=setInterval(function(){d++;if(d>8){stop();setDeg(8);return;}setDeg(d);},680);
}
document.getElementById("auto").addEventListener("click",function(){if(playing){stop();return;}auto();});

/* 启动 + 自动演示一遍 */
render();
setTimeout(function(){
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){setDeg(8);return;}
  auto();
},900);
})();
</script>
{% endraw %}
