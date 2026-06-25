---
layout: default
title: 扩散模型：加噪与去噪
description: "把一张图的每个像素一步步掺成彩色雪花，再从噪声里去噪生成——亲手体会扩散模型画图的原理。"
permalink: /viz/diffusion-noise/
redirect_from:
  - /v/diffusion-noise/
---

{% raw %}
<style>
.dflab #plane{image-rendering:pixelated;image-rendering:crisp-edges;border:1px solid var(--color-border-strong);border-radius:var(--radius-sm);background:#e7e1d8;width:300px;max-width:84vw;aspect-ratio:1;height:auto;display:block;margin:0 auto;}
.dflab .vizui-details{margin-top:10px;}
.dflab .vizui-details summary{cursor:pointer;color:var(--color-accent);font-size:.92rem;}
.dflab .vizui-details p{margin:.5em 0 0;color:var(--color-text-muted);font-size:.9rem;line-height:1.6;}
.dflab code{background:var(--color-bg-soft,#f0ece4);padding:.05em .35em;border-radius:3px;font-size:.9em;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 扩散模型：加噪与去噪

扩散模型（像 Stable Diffusion）画图的思路出奇地巧。**前向加噪**很好懂：把一张清晰的照片，一点点给**每个像素的颜色**掺进随机噪点，加够多步，整张图就变成一团彩色“雪花”——规则固定、谁都会。**真正要学的是反过来**：训练一个模型，让它看着一团噪声，估计里面混了多少噪点、一步步减掉，把图重新“显影”出来。学会去噪后，随便丢给它一团噪声、反复去噪，就能凭空生成一张全新的图。拖滑块或点按钮，看一张猫的照片怎样被打成雪花、又怎样从雪花里被还原出来。

<section class="vizui dflab" id="dflab">
  <p class="vizui__lead">这是一张<b>照片</b>，放大看其实是一格格<b>像素</b>。<b>加噪</b>＝给每个像素的颜色掺进随机噪点（像电视雪花）——<b>像素不动，变的是颜色</b>，不是把图案的点打散到别处。<b>去噪</b>才是模型学的本事：它<b>并不知道</b>你加了什么噪声，靠学到的“图长什么样”，从一团噪声里一步步把图还原 / 生成出来。点“换图”可在猫 / 心 / 笑脸 / 星之间切换。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="t">噪声程度（时间 t）</label>
        <input type="range" id="t" min="0" max="1" step="0.01" value="0" style="width:200px">
        <output id="tVal">0%</output>
      </span>
      <span class="vizui-spacer"></span>
      <button class="vizui-btn" id="fwd" type="button">▶ 加噪</button>
      <button class="vizui-btn vizui-btn--go" id="gen" type="button">▶ 从噪声生成</button>
      <button class="vizui-btn" id="shape" type="button">↻ 换图</button>
      <span class="vizui-pill" id="stat">清晰原图</span>
    </div>
  </div>

  <div class="vizui-panel">
    <div class="vizui-bar" style="justify-content:center">
      <canvas id="plane" width="64" height="64" role="img" aria-label="扩散加噪去噪像素图"></canvas>
    </div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <details class="vizui-details">
    <summary>背后的公式（点开看）</summary>
    <p>前向加噪可以一步到位：<code>加噪图 = √保留比例 × 原图 + √(1−保留比例) × 随机噪声</code>。“保留比例”（记作 ᾱ<sub>t</sub>）随时间 t 从 1 平滑降到 0，所以任意噪声程度都能直接算出来、规则固定。模型学的是<b>反向</b>：给定一张加噪图，预测里面的噪声，减掉一点点，多步迭代就能把图还原；从纯噪声起步同样能生成全新的图。</p>
  </details>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>前向：加噪（固定）</b><p>给每个像素的颜色按固定公式掺高斯噪声，越往后越像电视雪花。规则写死，不用学。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>反向：去噪（要学）</b><p>模型预测“这张噪声图里混了多少噪点”，减掉它，一步步把图“显影”出来。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>生成新图</b><p>学会去噪后，喂一团随机噪声、反复去噪，就能“无中生有”画出一张全新的图。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var N=64, shapeId=0, seed=7, s=0, mode=null, timer=null, started=false;
var x0=null, eps=[], catX0=null, catReady=false;
var canvas=document.getElementById("plane"), ctx=canvas.getContext("2d");

function rng(sd){return function(){sd|=0;sd=sd+0x6D2B79F5|0;var x=Math.imul(sd^sd>>>15,1|sd);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
function gauss(r){var u=0,v=0;while(!u)u=r();while(!v)v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}

var PAPER=[247,242,235], HEART=[206,55,70], FACE=[246,199,66], DARK=[58,50,46], STAR=[228,168,38];
function pip(x,y,poly){var inside=false,n=poly.length;for(var a=0,b=n-1;a<n;b=a++){var xi=poly[a][0],yi=poly[a][1],xj=poly[b][0],yj=poly[b][1];if(((yi>y)!=(yj>y))&&(x<(xj-xi)*(y-yi)/(yj-yi)+xi))inside=!inside;}return inside;}
function starPoly(){var p=[];for(var k=0;k<10;k++){var ang=-Math.PI/2+k*Math.PI/5,rad=(k%2===0)?1.0:0.42;p.push([rad*Math.cos(ang),rad*Math.sin(ang)]);}return p;}
var STAR_POLY=starPoly();
function shapeColor(id,x,y){
  if(id===1){ var hx=x/0.9, hy=(y-0.12)/0.9, a=hx*hx+hy*hy-1; return (a*a*a - hx*hx*hy*hy*hy<=0)?HEART:PAPER; }
  if(id===2){ if((Math.pow(x+0.34,2)+Math.pow(y-0.30,2)<=0.020)||(Math.pow(x-0.34,2)+Math.pow(y-0.30,2)<=0.020))return DARK;
    var rr=Math.sqrt(x*x+y*y); if(rr>=0.46&&rr<=0.60&&y<=-0.06)return DARK; if(rr<=1.0)return FACE; return PAPER; }
  return pip(x,y,STAR_POLY)?STAR:PAPER;
}
function genEps(){ var r=rng(seed+shapeId*131+1); eps=[]; for(var k=0;k<N*N;k++)eps.push([gauss(r),gauss(r),gauss(r)]); }
function reseed(){ seed=(seed*1103515245+12345)&0x7fffffff; var r=rng(seed); eps=[]; for(var k=0;k<N*N;k++)eps.push([gauss(r),gauss(r),gauss(r)]); }
function build(){
  if(shapeId===0){ if(catReady){ x0=catX0.slice(); } else { shapeId=1; } }
  if(shapeId!==0){
    x0=[];
    for(var j=0;j<N;j++)for(var i=0;i<N;i++){
      var x=((i+0.5)/N*2-1)*1.3, y=(1-(j+0.5)/N*2)*1.3, c=shapeColor(shapeId,x,y);
      x0.push([c[0]/127.5-1, c[1]/127.5-1, c[2]/127.5-1]);
    }
  }
  genEps();
}
function cl(v){return v<0?0:v>255?255:v|0;}
function draw(){
  if(!x0)return;
  var a=Math.sqrt(1-s), b=Math.sqrt(s), img=ctx.createImageData(N,N), D=img.data;
  for(var k=0;k<N*N;k++){ var p=x0[k],e=eps[k],o=k*4;
    D[o]=cl((a*p[0]+b*e[0]+1)*127.5); D[o+1]=cl((a*p[1]+b*e[1]+1)*127.5); D[o+2]=cl((a*p[2]+b*e[2]+1)*127.5); D[o+3]=255; }
  ctx.putImageData(img,0,0);
}
function caption(){
  var el=document.getElementById("caption"); if(!el)return;
  if(mode==="gen") el.innerHTML="<b>从纯噪声生成：</b>模型并不知道你加了什么噪声，它从一团随机雪花出发，靠学到的“图长什么样”一步步去噪，把图慢慢“显影”出来——这就是 AI 画图的核心。";
  else if(s<0.03) el.innerHTML="<b>噪声 0%：</b>清晰的原图，每个小格子是一个像素。往右拖滑块，给每个像素的颜色掺进随机噪点。";
  else if(s>0.97) el.innerHTML="<b>噪声 100%：</b>整张图变成彩色雪花，原来是什么彻底看不见了。扩散模型训练时见过海量这样的“图 → 雪花”过程。";
  else el.innerHTML="<b>噪声 "+Math.round(s*100)+"%：</b>"+(mode==="fwd"?"每个像素掺进越来越多噪点，图案越来越模糊——这一步是固定规则，不用学。":"噪点正被一点点减掉，图案重新显现出来。");
}
function render(){
  var o=document.getElementById("tVal"); if(o)o.textContent=Math.round(s*100)+"%";
  var sl=document.getElementById("t"); if(sl)sl.value=s;
  var st=document.getElementById("stat"); if(st)st.textContent=s<0.02?"清晰原图":s>0.98?"纯噪声（雪花）":"噪声 "+Math.round(s*100)+"%";
  draw(); caption();
}
function stop(){if(timer){clearInterval(timer);timer=null;}mode=null;}
function animate(dir,m){stop();mode=m;timer=setInterval(function(){s+=dir==="fwd"?0.03:-0.03;if(s>=1){s=1;stop();}else if(s<=0){s=0;stop();}render();},55);}

document.getElementById("t").addEventListener("input",function(e){stop();s=+e.target.value;mode=null;render();});
document.getElementById("fwd").addEventListener("click",function(){if(s>=1)s=0;animate("fwd","fwd");});
document.getElementById("gen").addEventListener("click",function(){reseed();s=1;render();setTimeout(function(){animate("rev","gen");},120);});
document.getElementById("shape").addEventListener("click",function(){stop();shapeId=(shapeId+1)%4;build();s=0;mode=null;render();});

function autoDemo(){
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){s=0.6;render();return;}
  s=0;animate("fwd","fwd");
  setTimeout(function(){reseed();s=1;render();animate("rev","gen");},2400);
}
function startAll(){ if(started)return; started=true; build(); render(); setTimeout(autoDemo,900); }

var catImg=new Image();
catImg.onload=function(){
  var off=document.createElement("canvas"); off.width=N; off.height=N;
  var octx=off.getContext("2d"); octx.drawImage(catImg,0,0,N,N);
  var d=octx.getImageData(0,0,N,N).data; catX0=[];
  for(var k=0;k<N*N;k++){var o=k*4; catX0.push([d[o]/127.5-1, d[o+1]/127.5-1, d[o+2]/127.5-1]);}
  catReady=true;
  if(!started){ startAll(); } else if(shapeId===0){ x0=catX0.slice(); render(); }
};
catImg.onerror=function(){ shapeId=1; if(!started)startAll(); };
catImg.src="/assets/viz/cat.jpg?v=1";
setTimeout(function(){ if(!started){ shapeId=catReady?0:1; startAll(); } },2500);
})();
</script>
{% endraw %}
