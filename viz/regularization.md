---
layout: default
title: 正则化 L1 / L2
permalink: /viz/regularization/
redirect_from:
  - /v/regularization/
---

{% raw %}
<style>
.rglab .axis{stroke:var(--color-border);stroke-width:1;}
.rglab .truec{fill:none;stroke:var(--color-border-strong);stroke-width:2;stroke-dasharray:5 4;}
.rglab .fitc{fill:none;stroke:var(--color-gold);stroke-width:2.8;stroke-linejoin:round;}
.rglab .pt{fill:var(--color-accent);}
.rglab .heads{display:inline-flex;gap:4px;padding:4px;background:var(--color-bg-section);border:1px solid var(--color-border);border-radius:999px;}
.rglab .heads button{appearance:none;border:0;background:transparent;cursor:pointer;font:inherit;font-size:.88rem;color:var(--color-text-soft);padding:6px 14px;border-radius:999px;}
.rglab .heads button.on{background:var(--color-bg-pure);color:var(--color-accent);font-weight:600;box-shadow:var(--shadow-sm);}
.rglab .wbars{display:flex;align-items:center;gap:3px;height:80px;}
.rglab .wbars .col{flex:1;display:flex;flex-direction:column;justify-content:center;height:100%;}
.rglab .wbars .bar{border-radius:2px;transition:height .25s var(--ease-out),background .2s;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 正则化 L1 / L2

模型太灵活容易过拟合——把噪声也学进去，曲线扭得乱七八糟。正则化的办法是在损失里加一项“惩罚”，专门惩罚过大的权重，逼模型用更“克制”的参数去拟合。两种常见惩罚效果不同：**L2** 让所有权重一起按比例缩小、曲线变平滑；**L1** 则会把一部分权重直接压到 0，相当于自动做“特征选择”。拖动惩罚强度 λ，看曲线和下面的权重条怎么变。

<section class="rglab vizui" id="rglab">
  <p class="vizui__lead">金色是拟合曲线，灰虚线是背后的真实规律，蓝点是带噪训练数据。下面每根条是一个特征的权重——看 λ 变大时，L2 让它们一起缩，L1 把一些直接清零。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="heads" id="heads"><button data-m="l2" class="on" type="button">L2（岭）</button><button data-m="l1" type="button">L1（套索）</button></span>
      <span class="vizui-field"><label for="lam">惩罚强度 λ</label><input type="range" id="lam" min="0" max="100" step="1" value="2" style="width:160px"><output id="lamVal"></output></span>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="info">—</span>
    </div>
    <svg class="vizui-chart" id="plot" viewBox="0 0 460 230" role="img" aria-label="正则化拟合"></svg>
    <p class="vizui-panel__title" style="margin-top:10px">各特征的权重</p>
    <div class="wbars" id="wbars"></div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>L2（岭回归）</b><p>惩罚权重的平方和，让所有权重一起平滑地变小，曲线更平缓，但很少正好为 0。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>L1（套索）</b><p>惩罚权重的绝对值，会把不重要的权重直接压到 0——产生“稀疏”解，自动挑出有用特征。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>都在防过拟合</b><p>λ 太小→过拟合（扭曲），太大→欠拟合（过平），中间有个最佳点。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var M=6, mode="l2", lamUI=2, XMIN=-2.6, XMAX=2.6, centers=[], sigma=0.72, data=[], w=[];
for(var i=0;i<M;i++)centers.push(XMIN+(XMAX-XMIN)*i/(M-1));
function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
function gauss(r){var u=0,v=0;while(!u)u=r();while(!v)v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}
function trueF(x){return Math.sin(x*1.4)*0.8;}
(function(){var r=rng(4);for(var k=0;k<16;k++){var x=XMIN+(XMAX-XMIN)*k/15;data.push([x,trueF(x)+gauss(r)*0.16]);}})();
function phi(x){return centers.map(function(c){return Math.exp(-(x-c)*(x-c)/(2*sigma*sigma));});}
var PH=data.map(function(d){return phi(d[0]);}), Y=data.map(function(d){return d[1];});
function solve(A,bb){var n=bb.length,Mx=A.map(function(r,i){return r.concat([bb[i]]);}),col,r,c;
  for(col=0;col<n;col++){var piv=col;for(r=col+1;r<n;r++)if(Math.abs(Mx[r][col])>Math.abs(Mx[piv][col]))piv=r;var tt=Mx[col];Mx[col]=Mx[piv];Mx[piv]=tt;var d=Mx[col][col]||1e-12;for(r=0;r<n;r++){if(r===col)continue;var f=Mx[r][col]/d;for(c=col;c<=n;c++)Mx[r][c]-=f*Mx[col][c];}}
  var x=[];for(var i=0;i<n;i++)x.push(Mx[i][n]/(Mx[i][i]||1e-12));return x;}
function fit(){
  var n=data.length, G=[], V=[], a, b, i;
  for(a=0;a<M;a++){G.push(new Array(M).fill(0));V.push(0);}
  for(i=0;i<n;i++)for(a=0;a<M;a++){V[a]+=PH[i][a]*Y[i];for(b=0;b<M;b++)G[a][b]+=PH[i][a]*PH[i][b];}
  if(mode==="l2"){                                  /* 岭回归闭式解 (ΦᵀΦ+λI)w=Φᵀy */
    var lamL2=lamUI/100*7, Gr=G.map(function(row,k){return row.map(function(v,l){return v+(k===l?lamL2:0);});});
    w=solve(Gr,V);
  }else{                                            /* 套索：坐标下降 + 软阈值 */
    var th=lamUI/100*4.5; w=new Array(M).fill(0);
    for(var rd=0;rd<80;rd++)for(var j=0;j<M;j++){
      var rho=V[j];for(var k=0;k<M;k++)if(k!==j)rho-=G[j][k]*w[k];
      var z=G[j][j]||1e-9; w[j]=Math.sign(rho)*Math.max(0,Math.abs(rho)-th)/z;
    }
  }
}
function predict(x){var ph=phi(x),s=0;for(var j=0;j<M;j++)s+=w[j]*ph[j];return s;}
var SVGNS="http://www.w3.org/2000/svg",W=460,H=230,pl=18,pr=14,pt=12,pb=22,YMIN=-1.4,YMAX=1.4;
function wx(x){return pl+(x-XMIN)/(XMAX-XMIN)*(W-pl-pr);}
function wy(y){return (H-pb)-(y-YMIN)/(YMAX-YMIN)*(H-pt-pb);}
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function curve(svg,fn,cls){var p=[];for(var i=0;i<=100;i++){var x=XMIN+(XMAX-XMIN)*i/100;p.push(wx(x)+","+wy(Math.max(YMIN-0.3,Math.min(YMAX+0.3,fn(x)))));}E(svg,"polyline",{points:p.join(" "),"class":cls});}
function draw(){
  var svg=document.getElementById("plot");while(svg.firstChild)svg.removeChild(svg.firstChild);
  E(svg,"line",{x1:pl,y1:wy(0),x2:W-pr,y2:wy(0),"class":"axis"});
  curve(svg,trueF,"truec");curve(svg,predict,"fitc");
  data.forEach(function(d){E(svg,"circle",{cx:wx(d[0]),cy:wy(d[1]),r:3.5,"class":"pt"});});
  // 权重条
  var host=document.getElementById("wbars");host.innerHTML="";var mx=Math.max(0.05,Math.max.apply(null,w.map(Math.abs)));
  w.forEach(function(v){var col=document.createElement("div");col.className="col";
    var h=Math.abs(v)/mx*38, up=v>=0;
    col.innerHTML='<div style="height:40px;display:flex;align-items:flex-end"><div class="bar" style="width:100%;height:'+(up?h:0)+'px;background:'+(Math.abs(v)<0.01?"#cfd8d6":"var(--color-accent)")+'"></div></div>'+
      '<div style="height:40px;display:flex;align-items:flex-start"><div class="bar" style="width:100%;height:'+(up?0:h)+'px;background:'+(Math.abs(v)<0.01?"#cfd8d6":"#b5524a")+'"></div></div>';
    host.appendChild(col);});
}
function render(){
  document.getElementById("lamVal").textContent=(lamUI/100).toFixed(2);
  fit();draw();
  var nz=w.filter(function(v){return Math.abs(v)>0.01;}).length;
  document.getElementById("info").textContent=(mode==="l1"?nz+" / "+M+" 个权重非零":"权重绝对值和 "+w.reduce(function(a,b){return a+Math.abs(b);},0).toFixed(2));
  caption(nz);
}
function caption(nz){
  var el=document.getElementById("caption"),s=lamUI/100;
  if(lamUI<4)el.innerHTML="惩罚≈0：模型尽情拟合每个点，曲线偏扭、权重偏大——容易过拟合。往右拖加大惩罚。";
  else if(mode==="l1")el.innerHTML="<b>L1（套索）：</b>惩罚强度 "+s.toFixed(2)+" 时，"+(M-nz)+" 个权重被直接压到了 <b>0</b>（灰条），只剩 "+nz+" 个起作用——这就是稀疏/特征选择。强度越大，归零的越多、曲线越简。";
  else el.innerHTML="<b>L2（岭）：</b>惩罚强度 "+s.toFixed(2)+" 时，所有权重一起按比例缩小（很少正好为 0），曲线随之变平滑。强度越大越平，太大就欠拟合了。";
}
document.getElementById("heads").addEventListener("click",function(e){var b=e.target.closest("button");if(!b)return;mode=b.dataset.m;document.querySelectorAll("#heads button").forEach(function(x){x.classList.toggle("on",x.dataset.m===mode);});render();});
document.getElementById("lam").addEventListener("input",function(e){lamUI=+e.target.value;render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  var seq=[2,30,70,2],n=0,sl=document.getElementById("lam");var iv=setInterval(function(){lamUI=seq[n];sl.value=lamUI;render();n++;if(n>=seq.length){mode="l1";document.querySelectorAll("#heads button").forEach(function(x){x.classList.toggle("on",x.dataset.m==="l1");});var s2=[2,40,80,40],m=0;var iv2=setInterval(function(){lamUI=s2[m];sl.value=lamUI;render();m++;if(m>=s2.length)clearInterval(iv2);},900);clearInterval(iv);}},900);},1100);
})();
</script>
{% endraw %}
