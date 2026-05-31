---
layout: default
title: 过拟合实验台
permalink: /viz/overfitting/
redirect_from:
  - /v/overfitting/
---

{% raw %}
<style>
.oflab .axis{stroke:var(--color-border);stroke-width:1;}
.oflab .alab{font:11px var(--font-mono);fill:var(--color-text-muted);}
.oflab .truecurve{fill:none;stroke:var(--color-border-strong);stroke-width:2;stroke-dasharray:5 4;}
.oflab .fitcurve{fill:none;stroke:var(--color-gold);stroke-width:2.6;stroke-linejoin:round;}
.oflab .pt{fill:var(--color-accent);}
.oflab .pt-test{fill:none;stroke:var(--color-text-muted);stroke-width:1.3;opacity:.7;}
.oflab .err-train{fill:none;stroke:var(--color-accent-light);stroke-width:2.6;stroke-linejoin:round;}
.oflab .err-test{fill:none;stroke:#b5524a;stroke-width:2.6;stroke-linejoin:round;}
.oflab .nowline{stroke:var(--color-accent);stroke-width:1.4;stroke-dasharray:4 3;opacity:.8;}
.oflab .errdot{stroke:#fff;stroke-width:1.5;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 过拟合实验台

机器学习要的是``学到规律''，而不是``背下答案''。同一批数据，模型太简单会``欠拟合''、抓不住趋势；太复杂又会``过拟合''、把噪声也当成规律背下来。拖动下面的``模型复杂度''滑块，亲眼看看这条曲线怎样从太直、到刚好、再到扭成麻花。

<section class="vizui oflab" id="oflab">
  <p class="vizui__lead">蓝点是``训练数据''（带噪声）。金色曲线是模型拟合的结果，灰色虚线是背后真正的规律。右图是``考试成绩''：训练误差 vs 没见过的测试误差。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="deg">模型复杂度（多项式次数）</label>
        <input type="range" id="deg" min="1" max="9" step="1" value="3" style="width:200px">
        <output id="degVal">3</output>
      </span>
      <span class="vizui-spacer"></span>
      <button class="vizui-btn vizui-btn--go" id="auto" type="button">▶ 自动演示</button>
      <button class="vizui-btn" id="regen" type="button">↻ 换一批数据</button>
    </div>
  </div>

  <div class="vizui-grid2">
    <div class="vizui-panel">
      <p class="vizui-panel__title">拟合情况</p>
      <div class="vizui-legend">
        <span><i class="dot" style="background:var(--color-accent)"></i>训练点</span>
        <span><i class="dot" style="background:#fff;border:1.3px solid var(--color-text-muted)"></i>测试点</span>
        <span><i style="background:var(--color-gold)"></i>模型拟合</span>
        <span><i style="background:var(--color-border-strong)"></i>真实规律</span>
      </div>
      <svg class="vizui-chart" id="chartFit" viewBox="0 0 440 260" role="img" aria-label="拟合曲线"></svg>
    </div>
    <div class="vizui-panel">
      <p class="vizui-panel__title">误差随复杂度变化</p>
      <div class="vizui-legend">
        <span><i style="background:var(--color-accent-light)"></i>训练误差</span>
        <span><i style="background:#b5524a"></i>测试误差</span>
        <span>竖线 = 当前复杂度</span>
      </div>
      <svg class="vizui-chart" id="chartErr" viewBox="0 0 440 220" role="img" aria-label="误差曲线"></svg>
    </div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-text-muted)"><b>欠拟合（太简单）</b><p>复杂度太低，曲线连训练点的大趋势都跟不上，训练和测试误差都高。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>恰到好处</b><p>曲线贴合数据又保持平滑，测试误差最低——这才是``学到规律''。</p></div>
    <div class="card" style="--wc:#b5524a"><b>过拟合（太复杂）</b><p>曲线扭来扭去穿过每个训练点，把噪声也背了下来；训练误差几乎为零，测试误差却飙升。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var NTRAIN=10, NTEST=60, MAXDEG=9, RIDGE=1e-8;
var seed=3, deg=3;
var train=[], test=[], coeffs=[], trainErr=[], testErr=[], bestDeg=3;
var playing=false, timer=null;

function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
function gauss(r){var u=0,v=0;while(!u)u=r();while(!v)v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}
function trueF(x){return Math.sin(x*2.4)*0.8;}

function genData(){
  var r=rng(seed); train=[]; test=[];
  for(var i=0;i<NTRAIN;i++){var x=-1+2*i/(NTRAIN-1)+gauss(r)*0.04;x=Math.max(-1,Math.min(1,x));train.push([x,trueF(x)+gauss(r)*0.16]);}
  for(var j=0;j<NTEST;j++){var xt=-1+2*r();test.push([xt,trueF(xt)+gauss(r)*0.16]);}
}

/* 多项式最小二乘（正规方程 + 微小岭正则 + 高斯消元） */
function polyfit(pts,d){
  var m=d+1,n=pts.length,M=[],v=[],a,b,i;
  for(a=0;a<m;a++){M.push(new Array(m).fill(0));v.push(0);}
  for(i=0;i<n;i++){
    var pw=[],p=1; for(b=0;b<m;b++){pw.push(p);p*=pts[i][0];}
    for(a=0;a<m;a++){v[a]+=pw[a]*pts[i][1];for(b=0;b<m;b++)M[a][b]+=pw[a]*pw[b];}
  }
  for(var k=0;k<m;k++)M[k][k]+=RIDGE;
  return solve(M,v);
}
function solve(M,v){
  var n=v.length,A=M.map(function(row,i){return row.concat([v[i]]);}),col,r,c;
  for(col=0;col<n;col++){
    var piv=col; for(r=col+1;r<n;r++) if(Math.abs(A[r][col])>Math.abs(A[piv][col])) piv=r;
    var tmp=A[col];A[col]=A[piv];A[piv]=tmp;
    var dd=A[col][col]||1e-12;
    for(r=0;r<n;r++){if(r===col)continue;var f=A[r][col]/dd;for(c=col;c<=n;c++)A[r][c]-=f*A[col][c];}
  }
  var x=[];for(var i2=0;i2<n;i2++)x.push(A[i2][n]/(A[i2][i2]||1e-12));return x;
}
function polyval(co,x){var y=0,p=1;for(var j=0;j<co.length;j++){y+=co[j]*p;p*=x;}return y;}
function rmse(co,pts){var s=0;for(var i=0;i<pts.length;i++){var e=polyval(co,pts[i][0])-pts[i][1];s+=e*e;}return Math.sqrt(s/pts.length);}

function recompute(){
  coeffs=[null]; trainErr=[null]; testErr=[null];
  for(var d=1;d<=MAXDEG;d++){var co=polyfit(train,d);coeffs[d]=co;trainErr[d]=rmse(co,train);testErr[d]=rmse(co,test);}
  bestDeg=1; for(var k=2;k<=MAXDEG;k++) if(testErr[k]<testErr[bestDeg]) bestDeg=k;
}

/* ---------- 绘图 ---------- */
var SVGNS="http://www.w3.org/2000/svg";
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function clear(svg){while(svg.firstChild)svg.removeChild(svg.firstChild);}

var FW=440,FH=260,Fpl=30,Fpr=14,Fpt=14,Fpb=24, YMIN=-1.6,YMAX=1.6;
function fx(x){return Fpl+(x+1)/2*(FW-Fpl-Fpr);}
function fy(y){return (FH-Fpb)-(y-YMIN)/(YMAX-YMIN)*(FH-Fpt-Fpb);}
function drawFit(){
  var svg=document.getElementById("chartFit"); clear(svg);
  E(svg,"line",{x1:Fpl,y1:fy(0),x2:FW-Fpr,y2:fy(0),"class":"axis"});
  E(svg,"line",{x1:Fpl,y1:Fpt,x2:Fpl,y2:FH-Fpb,"class":"axis"});
  /* 真实规律 */
  var tp=[]; for(var i=0;i<=80;i++){var x=-1+2*i/80;tp.push(fx(x)+","+fy(trueF(x)));}
  E(svg,"polyline",{points:tp.join(" "),"class":"truecurve"});
  /* 拟合曲线（裁剪到画布内） */
  var co=coeffs[deg],fp=[];
  for(var j=0;j<=160;j++){var xx=-1+2*j/160;var yy=Math.max(YMIN-0.4,Math.min(YMAX+0.4,polyval(co,xx)));fp.push(fx(xx)+","+fy(yy));}
  var clip=E(svg,"clipPath",{id:"fitclip"});E(clip,"rect",{x:Fpl,y:Fpt-2,width:FW-Fpl-Fpr,height:FH-Fpt-Fpb+2});
  E(svg,"polyline",{points:fp.join(" "),"class":"fitcurve","clip-path":"url(#fitclip)"});
  /* 测试点（淡） */
  for(var t=0;t<test.length;t++)E(svg,"circle",{cx:fx(test[t][0]),cy:fy(test[t][1]),r:2.4,"class":"pt-test"});
  /* 训练点 */
  for(var k=0;k<train.length;k++)E(svg,"circle",{cx:fx(train[k][0]),cy:fy(train[k][1]),r:4,"class":"pt"});
}

var EW=440,EH=220,Epl=34,Epr=14,Ept=16,Epb=30;
function ex(d){return Epl+(d-1)/(MAXDEG-1)*(EW-Epl-Epr);}
function drawErr(){
  var svg=document.getElementById("chartErr"); clear(svg);
  var ymax=0; for(var d=1;d<=MAXDEG;d++){ymax=Math.max(ymax,trainErr[d],testErr[d]);}
  ymax=Math.min(Math.max(ymax*1.1,0.4),1.3);
  function ey(v){return (EH-Epb)-Math.min(v,ymax)/ymax*(EH-Ept-Epb);}
  E(svg,"line",{x1:Epl,y1:EH-Epb,x2:EW-Epr,y2:EH-Epb,"class":"axis"});
  E(svg,"line",{x1:Epl,y1:Ept,x2:Epl,y2:EH-Epb,"class":"axis"});
  for(var dd=1;dd<=MAXDEG;dd+=2)E(svg,"text",{x:ex(dd),y:EH-Epb+15,"text-anchor":"middle","class":"alab"}).textContent=dd;
  E(svg,"text",{x:Epl-6,y:Ept+4,"text-anchor":"end","class":"alab"}).textContent="误差";
  /* 当前复杂度竖线 */
  E(svg,"line",{x1:ex(deg),y1:Ept,x2:ex(deg),y2:EH-Epb,"class":"nowline"});
  function line(arr,cls){var p=[];for(var d=1;d<=MAXDEG;d++)p.push(ex(d)+","+ey(arr[d]));E(svg,"polyline",{points:p.join(" "),"class":cls});}
  line(trainErr,"err-train"); line(testErr,"err-test");
  E(svg,"circle",{cx:ex(deg),cy:ey(trainErr[deg]),r:4,fill:"var(--color-accent-light)","class":"errdot"});
  E(svg,"circle",{cx:ex(deg),cy:ey(testErr[deg]),r:4,fill:"#b5524a","class":"errdot"});
}

function caption(){
  var el=document.getElementById("caption"),tr=trainErr[deg].toFixed(3),te=testErr[deg].toFixed(3);
  var msg;
  if(deg<=2){msg="复杂度 = "+deg+"：曲线太``直''，连训练点的趋势都跟不上——这是<b>欠拟合</b>。（测试误差 "+te+"）";}
  else if(deg>=bestDeg+3){msg="复杂度 = "+deg+"：曲线扭来扭去硬穿过每个训练点，把噪声也背了下来——这是<b>过拟合</b>。训练误差低到 "+tr+"，可测试误差却涨到 <b>"+te+"</b>。";}
  else if(Math.abs(deg-bestDeg)<=1){msg="复杂度 = "+deg+"：曲线既贴合数据、又保持平滑——<b>恰到好处</b>，测试误差最低（"+te+"）。";}
  else {msg="复杂度 = "+deg+"：训练误差 "+tr+"，测试误差 "+te+"。继续加大复杂度，留意测试误差什么时候开始反弹。";}
  el.innerHTML=msg;
}
function render(){document.getElementById("degVal").textContent=deg;drawFit();drawErr();caption();}

function setDeg(d){deg=Math.max(1,Math.min(MAXDEG,d));document.getElementById("deg").value=deg;render();}
function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("auto").textContent="▶ 自动演示";}
function auto(){
  stop();playing=true;document.getElementById("auto").textContent="⏸ 暂停";var d=1;setDeg(1);
  timer=setInterval(function(){d++;if(d>MAXDEG){stop();setDeg(bestDeg);return;}setDeg(d);},520);
}
document.getElementById("deg").addEventListener("input",function(e){stop();setDeg(+e.target.value);});
document.getElementById("auto").addEventListener("click",function(){playing?stop():auto();});
document.getElementById("regen").addEventListener("click",function(){stop();seed++;genData();recompute();render();});

/* 启动 + 自动演示一遍 */
genData();recompute();render();
setTimeout(function(){
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){setDeg(MAXDEG);return;}
  auto();
},900);
})();
</script>
{% endraw %}
