---
layout: default
title: SVD 与低秩近似
permalink: /viz/svd-lowrank/
redirect_from:
  - /v/svd-lowrank/
---

{% raw %}
<style>
.svdlab .px{shape-rendering:crispEdges;}
.svdlab .frame{fill:none;stroke:var(--color-border-strong);stroke-width:1.2;}
.svdlab .svbar{fill:var(--color-accent);}
.svdlab .svbar.dim{fill:var(--color-border-strong);opacity:.55;}
.svdlab .svaxis{stroke:var(--color-border);stroke-width:1;}
.svdlab .imglabel{font:600 .8rem var(--font-sans);fill:var(--color-text-muted);text-anchor:middle;}
.svdlab .pillrow{display:flex;flex-wrap:wrap;gap:8px;margin-top:6px;}
.svdlab .pill{display:inline-flex;align-items:baseline;gap:6px;padding:6px 12px;border-radius:999px;background:var(--color-bg-section);border:1px solid var(--color-border);font-size:.85rem;color:var(--color-text-soft);}
.svdlab .pill b{font:700 1rem var(--font-mono);color:var(--color-accent);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# SVD 与低秩近似

一张图片摊开就是一个数字矩阵。奇异值分解（SVD）把这个矩阵拆成一摞“秩为 1 的薄片”，每片配一个奇异值 σ 当权重，按从大到小排好队。神奇的是：前几片就扛住了几乎全部信息，剩下一长串都是可以丢掉的细节。只留前 k 片重建出来的图，肉眼几乎看不出和原图的差别——这正是图像压缩、PCA 与大模型里 LoRA 低秩微调背后的同一个直觉。**拖动滑块**，看用几片就够了。

<section class="vizui svdlab" id="svdlab">
  <p class="vizui__lead">左边是原图，右边是只保留前 <span style="color:var(--color-accent);font-weight:600">k 个奇异值</span> 重建的结果。下方柱状图是各奇异值 <span style="color:var(--color-accent);font-weight:600">σᵢ</span> 的大小——它们陡降得很快，说明信息高度集中在头几个方向上。</p>

  <div class="vizui-grid2">
    <div class="vizui-panel">
      <svg class="vizui-chart" id="imgs" viewBox="0 0 320 180" style="max-width:380px;margin:0 auto;display:block" role="img" aria-label="原图与低秩重建对比"></svg>
    </div>
    <div class="vizui-panel">
      <p class="vizui-panel__title">控制</p>
      <div class="vizui-field"><label for="kk">保留奇异值数 k</label><input type="range" id="kk" min="1" max="12" step="1" value="6" style="width:150px"><output id="kkVal">6</output></div>
      <div class="pillrow">
        <span class="pill">压缩率 <b id="comp">—</b></span>
        <span class="pill">相对误差 <b id="err">—</b></span>
      </div>
      <p class="vizui-panel__title" style="margin-top:16px">奇异值谱 σᵢ</p>
      <svg class="vizui-chart" id="spec" viewBox="0 0 300 96" style="max-width:320px;display:block" role="img" aria-label="奇异值谱"></svg>
      <p style="font-size:.82rem;color:var(--color-text-muted);margin-top:6px">蓝色是已保留的前 k 个，灰色是被丢弃的尾巴。尾巴又长又矮，丢了也无妨。</p>
    </div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>σ 排好了队</b><p>奇异值从大到小排列，第一个就装下了大半信息；越往后越小，贡献越微弱。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>低秩 = 压缩</b><p>只存前 k 片（每片是一列 u、一行 v 加一个 σ），存储量从 m·n 降到 k·(m+n+1)。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>同一个直觉</b><p>PCA 取前几个主成分、LoRA 用低秩矩阵微调大模型——都是“少数几个方向扛住了主要信息”。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var N=28, K=6;
var SVGNS="http://www.w3.org/2000/svg";

function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}

function buildImage(){
  var M=[];for(var i=0;i<N;i++){M.push(new Array(N).fill(0));}
  var r=rng(777);
  for(var i=0;i<N;i++)for(var j=0;j<N;j++){
    var x=j/(N-1), y=i/(N-1);
    var v=0.30*(x+y)/2 + 0.16*Math.cos(2.2*x);
    if(i>=4 && i<=7) v+=0.42;            /* 横条 */
    if(j>=18 && j<=21) v+=0.38;          /* 竖条 */
    var d2=(i-19)*(i-19)+(j-9)*(j-9);
    v+=0.5*Math.exp(-d2/26);             /* 亮斑 */
    v+=0.10*Math.sin(3.1*Math.PI*x+0.7)*Math.sin(2.3*Math.PI*y);
    v+=0.07*Math.sin(5.0*Math.PI*x)*Math.cos(4.0*Math.PI*y+0.4);
    v+=0.05*Math.cos(6.5*Math.PI*x+1.1)*Math.sin(6.0*Math.PI*y);
    v+=0.035*Math.sin(8.0*Math.PI*x)*Math.sin(7.5*Math.PI*y+0.9);
    M[i][j]=v;
  }
  for(var i=0;i<N;i++)for(var j=0;j<N;j++)M[i][j]+=0.04*(r()-0.5);
  var mn=Infinity,mx=-Infinity;
  for(var i=0;i<N;i++)for(var j=0;j<N;j++){if(M[i][j]<mn)mn=M[i][j];if(M[i][j]>mx)mx=M[i][j];}
  for(var i=0;i<N;i++)for(var j=0;j<N;j++)M[i][j]=(M[i][j]-mn)/(mx-mn);
  return M;
}

function matVec(M,v){var m=M.length,n=M[0].length,out=new Array(m).fill(0);for(var i=0;i<m;i++){var s=0,row=M[i];for(var j=0;j<n;j++)s+=row[j]*v[j];out[i]=s;}return out;}
function matTVec(M,u){var m=M.length,n=M[0].length,out=new Array(n).fill(0);for(var i=0;i<m;i++){var ui=u[i],row=M[i];for(var j=0;j<n;j++)out[j]+=row[j]*ui;}return out;}
function norm(v){var s=0;for(var i=0;i<v.length;i++)s+=v[i]*v[i];return Math.sqrt(s);}

/* 幂迭代 + 收缩：每轮 v←归一化(MᵀMv)，σ=||Mv||，u=Mv/σ，再 M←M−σuvᵀ */
function svdTopK(M0,Kc,seed){
  var M=M0.map(function(r){return r.slice();}),m=M.length,n=M[0].length,r=rng(seed),res=[];
  for(var t=0;t<Kc;t++){
    var v=new Array(n);for(var j=0;j<n;j++)v[j]=r()-0.5;
    var nv=norm(v)||1;for(var j=0;j<n;j++)v[j]/=nv;
    for(var it=0;it<40;it++){
      var Mv=matVec(M,v),w=matTVec(M,Mv),nw=norm(w);
      if(nw<1e-12)break;
      for(var j=0;j<n;j++)v[j]=w[j]/nw;
    }
    var Mv2=matVec(M,v),sigma=norm(Mv2),u=new Array(m);
    if(sigma<1e-12){for(var i=0;i<m;i++)u[i]=0;}
    else{for(var i=0;i<m;i++)u[i]=Mv2[i]/sigma;}
    res.push({sigma:sigma,u:u,v:v.slice()});
    for(var i=0;i<m;i++){var us=u[i]*sigma,row=M[i];for(var j=0;j<n;j++)row[j]-=us*v[j];}
  }
  return res;
}
function reconstruct(comps,k){
  var R=[];for(var i=0;i<N;i++)R.push(new Array(N).fill(0));
  for(var t=0;t<k;t++){var c=comps[t],s=c.sigma,u=c.u,v=c.v;
    for(var i=0;i<N;i++){var su=s*u[i],row=R[i];for(var j=0;j<N;j++)row[j]+=su*v[j];}}
  return R;
}
function froDiff(A,B){var s=0;for(var i=0;i<N;i++)for(var j=0;j<N;j++){var d=A[i][j]-B[i][j];s+=d*d;}return Math.sqrt(s);}
function froNorm(A){var s=0;for(var i=0;i<N;i++)for(var j=0;j<N;j++)s+=A[i][j]*A[i][j];return Math.sqrt(s);}

var IMG=buildImage();
var COMPS=svdTopK(IMG,N,12345);
var SIG=COMPS.map(function(c){return c.sigma;});
var FRO=froNorm(IMG);
var SIGMAX=SIG[0];

function shade(v){var g=Math.round(255*(1-Math.max(0,Math.min(1,v))));return "rgb("+g+","+g+","+g+")";}

function drawGrid(svg,M,x0,y0,side){
  var c=side/N;
  for(var i=0;i<N;i++)for(var j=0;j<N;j++){
    var e=document.createElementNS(SVGNS,"rect");
    e.setAttribute("x",(x0+j*c).toFixed(2));e.setAttribute("y",(y0+i*c).toFixed(2));
    e.setAttribute("width",(c+0.5).toFixed(2));e.setAttribute("height",(c+0.5).toFixed(2));
    e.setAttribute("fill",shade(M[i][j]));e.setAttribute("class","px");
    svg.appendChild(e);
  }
  var f=document.createElementNS(SVGNS,"rect");
  f.setAttribute("x",x0);f.setAttribute("y",y0);f.setAttribute("width",side);f.setAttribute("height",side);
  f.setAttribute("class","frame");svg.appendChild(f);
}
function txt(svg,x,y,s,cls){var e=document.createElementNS(SVGNS,"text");e.setAttribute("x",x);e.setAttribute("y",y);e.setAttribute("class",cls);e.textContent=s;svg.appendChild(e);}

function drawImages(){
  var svg=document.getElementById("imgs");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var side=120,gap=40,y0=18;
  var x1=18,x2=x1+side+gap;
  drawGrid(svg,IMG,x1,y0,side);
  var Rk=reconstruct(COMPS,K);
  drawGrid(svg,Rk,x2,y0,side);
  txt(svg,x1+side/2,y0+side+22,"原图 28×28","imglabel");
  txt(svg,x2+side/2,y0+side+22,"前 "+K+" 片重建","imglabel");
}

function drawSpectrum(){
  var svg=document.getElementById("spec");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var W=300,H=96,padL=8,padB=14,padT=6,n=SIG.length;
  var bw=(W-padL-6)/n, base=H-padB, h=base-padT;
  var ax=document.createElementNS(SVGNS,"line");ax.setAttribute("x1",padL);ax.setAttribute("y1",base);ax.setAttribute("x2",W-4);ax.setAttribute("y2",base);ax.setAttribute("class","svaxis");svg.appendChild(ax);
  for(var i=0;i<n;i++){
    var bh=Math.max(1, h*(SIG[i]/SIGMAX));
    var e=document.createElementNS(SVGNS,"rect");
    e.setAttribute("x",(padL+i*bw+1).toFixed(2));e.setAttribute("y",(base-bh).toFixed(2));
    e.setAttribute("width",Math.max(1.5,bw-1.6).toFixed(2));e.setAttribute("height",bh.toFixed(2));
    e.setAttribute("class",i<K?"svbar":"svbar dim");
    svg.appendChild(e);
  }
}

function render(){
  document.getElementById("kkVal").textContent=K;
  var Rk=reconstruct(COMPS,K);
  var relerr=froDiff(IMG,Rk)/FRO;
  var comp=K*(N+N+1)/(N*N);
  document.getElementById("err").textContent=(relerr*100).toFixed(1)+"%";
  document.getElementById("comp").textContent=(comp*100).toFixed(0)+"%";
  drawImages();drawSpectrum();caption(relerr,comp);
}
function caption(relerr,comp){
  var el=document.getElementById("caption"),pct=(relerr*100).toFixed(1),cp=(comp*100).toFixed(0);
  var m;
  if(K<=2) m="只用前 "+K+" 片，重建已经抓住了大轮廓，相对误差 <b>"+pct+"%</b>。再加几片细节就回来了。";
  else if(relerr<0.03) m="只保留前 <b>"+K+"</b> 个奇异值，重建图和原图几乎分不出差别——相对误差仅 <b>"+pct+"%</b>，却只用了约 "+cp+"% 的存储量。这就是“少数几片扛住主要信息”。";
  else m="保留前 "+K+" 片，相对误差降到 <b>"+pct+"%</b>，存储量约为原图的 "+cp+"%。继续加片误差还会更小，但你会发现 5～8 片往往就够看了。";
  el.innerHTML=m;
}

var slider=document.getElementById("kk");
slider.addEventListener("input",function(e){if(demo){clearInterval(demo);demo=null;}K=+e.target.value;render();});

render();

var demo=null;
setTimeout(function(){
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){K=8;slider.value=8;render();return;}
  var seq=[1,2,3,4,5,6,7,8],k=0;
  demo=setInterval(function(){
    K=seq[k];slider.value=K;render();k++;
    if(k>=seq.length){clearInterval(demo);demo=null;}
  },720);
},900);
})();
</script>
{% endraw %}
