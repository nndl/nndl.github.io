---
layout: default
title: 稀疏自编码器
permalink: /viz/sparse-autoencoder/
redirect_from:
  - /v/sparse-autoencoder/
---

{% raw %}
<style>
.saelab svg{max-width:100%;height:auto;}
.saelab .axis{stroke:var(--color-border-strong);stroke-width:1;}
.saelab .inarea{fill:#9aa3a8;opacity:.18;}
.saelab .inline{fill:none;stroke:#9aa3a8;stroke-width:1.6;}
.saelab .recon{fill:none;stroke:var(--color-accent);stroke-width:2.6;}
.saelab .feat{fill:none;stroke:var(--color-accent);stroke-width:1;opacity:.35;}
.saelab .bar{fill:#d4dadf;}
.saelab .bar.on{fill:var(--color-accent);}
.saelab .thr{stroke:var(--color-gold);stroke-width:1.6;stroke-dasharray:5 3;}
.saelab .lbl{font:10px var(--font-sans);fill:var(--color-text-muted);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 稀疏自编码器

自编码器（autoencoder）是一种无监督模型：**编码器**把输入压成一层隐藏表示 h，**解码器**再只凭 h 把输入重构回来，训练目标就是“重构得越像越好”。**稀疏自编码器**多加一条约束——隐藏层可以很宽，但要求**任一输入只点亮其中少数几个单元**（其余压到 0，常用 L1 或 KL 惩罚实现）。这样每个常用单元会学成一个可复用的“特征”，少数特征叠加就能重建输入。下面用一组固定的“特征”（高斯基）演示：拖动稀疏强度，看活跃单元数与重构质量怎样此消彼长。

<section class="vizui saelab" id="saelab">
  <p class="vizui__lead">左图：<span style="color:#7a828a;font-weight:600">灰色</span>是输入信号，<span style="color:var(--color-accent);font-weight:600">彩色线</span>是重构（淡线是被激活的各个“特征”，相加就是重构）。右图：12 个隐单元的激活，<span style="color:var(--color-gold);font-weight:600">金色虚线</span>是稀疏阈值——只有超过它的少数单元（彩色）被保留参与重构，其余压成 0。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="lam">稀疏强度 λ</label><input type="range" id="lam" min="0" max="1.3" step="0.01" value="0.45" style="width:170px"><output id="lamVal">0.45</output></span>
      <button class="vizui-btn" id="newx" type="button">↻ 换输入</button>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stat">—</span>
    </div>
    <div class="vizui-grid2">
      <div class="vizui-panel"><p class="vizui-panel__title">输入 vs 重构（解码）</p>
        <svg id="sig" viewBox="0 0 300 190" role="img" aria-label="输入与重构信号"></svg></div>
      <div class="vizui-panel"><p class="vizui-panel__title">隐层 h（12 单元，稀疏激活）</p>
        <svg id="code" viewBox="0 0 240 190" role="img" aria-label="隐层激活"></svg></div>
    </div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>编码 → 解码</b><p>编码器把输入压成隐层激活 h，解码器只凭 h 重构输入；没有标签，靠“重构得像不像”自我监督。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>稀疏约束</b><p>隐层可以很宽，但惩罚项逼大多数单元为 0——每个输入只激活少数几个，得到一份“瘦”编码。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>学出可复用特征</b><p>真实模型会自己学出这些特征与稀疏阈值；少数特征叠加即可重建，还顺带滤掉冗余与噪声。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var L=36, K=12, sigma=1.15, lambda=0.45;
var centers=[], D=[];
for(var k=0;k<K;k++)centers.push((k+0.5)*L/K);
function bump(c){var b=[],nn=0,i;for(i=0;i<L;i++){var v=Math.exp(-(i-c)*(i-c)/(2*sigma*sigma));b.push(v);nn+=v*v;}nn=Math.sqrt(nn);for(i=0;i<L;i++)b[i]/=nn;return b;}
for(var k2=0;k2<K;k2++)D.push(bump(centers[k2]));
var PRESETS=[{u:[2,6,9],c:[1.0,0.85,1.15]},{u:[1,5,8,11],c:[0.9,1.1,0.8,1.0]},{u:[3,7],c:[1.2,0.95]}];
var pi=0, x=[];
function buildX(){x=[];for(var i=0;i<L;i++){var s=0;PRESETS[pi].u.forEach(function(u,j){s+=PRESETS[pi].c[j]*D[u][i];});x.push(s);}}
function dot(a,b){var s=0;for(var i=0;i<L;i++)s+=a[i]*b[i];return s;}
function encode(){return D.map(function(dk){return dot(x,dk);});}            // s_k = <x, D_k>
function reconstruct(s){var v=[];for(var i=0;i<L;i++){var acc=0;for(var k=0;k<K;k++)if(s[k]>lambda)acc+=s[k]*D[k][i];v.push(acc);}return v;}
function relErr(xr){var e=0,n=0;for(var i=0;i<L;i++){e+=(x[i]-xr[i])*(x[i]-xr[i]);n+=x[i]*x[i];}return n>0?Math.sqrt(e/n)*100:0;}

var SVGNS="http://www.w3.org/2000/svg";
function E(p,t,a,txt){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;p.appendChild(e);return e;}

function drawSig(s,xr){
  var svg=document.getElementById("sig");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var pl=22,pr=12,pt=14,pb=24,W=300,H=190;
  var vmax=0.55;for(var i=0;i<L;i++){vmax=Math.max(vmax,x[i],xr[i]);}
  function X(i){return pl+i/(L-1)*(W-pl-pr);}
  function Y(v){return (H-pb)-v/vmax*(H-pt-pb);}
  E(svg,"line",{x1:pl,y1:H-pb,x2:W-pr,y2:H-pb,"class":"axis"});
  // 输入区域
  var ap="M"+X(0)+","+(H-pb);for(i=0;i<L;i++)ap+=" L"+X(i).toFixed(1)+","+Y(x[i]).toFixed(1);ap+=" L"+X(L-1)+","+(H-pb)+" Z";
  E(svg,"path",{d:ap,"class":"inarea"});
  E(svg,"polyline",{points:x.map(function(v,i){return X(i).toFixed(1)+","+Y(v).toFixed(1);}).join(" "),"class":"inline"});
  // 被激活的单个特征（淡）
  for(var k=0;k<K;k++)if(s[k]>lambda){
    var pts=[];for(i=0;i<L;i++)pts.push(X(i).toFixed(1)+","+Y(s[k]*D[k][i]).toFixed(1));
    E(svg,"polyline",{points:pts.join(" "),"class":"feat"});
  }
  // 重构（彩色 = 激活特征之和）
  E(svg,"polyline",{points:xr.map(function(v,i){return X(i).toFixed(1)+","+Y(v).toFixed(1);}).join(" "),"class":"recon"});
  E(svg,"text",{x:pl,y:11,"class":"lbl"},"输入（灰）与重构（青）");
}
function drawCode(s){
  var svg=document.getElementById("code");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var pl=20,pr=12,pt=16,pb=24,W=240,H=190;
  var smax=1.2;for(var k=0;k<K;k++)smax=Math.max(smax,s[k]);smax=Math.max(smax,lambda)*1.06;
  function Y(v){return (H-pb)-v/smax*(H-pt-pb);}
  var bw=(W-pl-pr)/K;
  E(svg,"line",{x1:pl,y1:H-pb,x2:W-pr,y2:H-pb,"class":"axis"});
  for(k=0;k<K;k++){var on=s[k]>lambda,h=(H-pb)-Y(s[k]);
    E(svg,"rect",{x:(pl+k*bw+1.5).toFixed(1),y:Y(s[k]).toFixed(1),width:(bw-3).toFixed(1),height:Math.max(0,h).toFixed(1),"class":"bar"+(on?" on":"")});}
  E(svg,"line",{x1:pl,y1:Y(lambda).toFixed(1),x2:W-pr,y2:Y(lambda).toFixed(1),"class":"thr"});
  E(svg,"text",{x:W-pr,y:(Y(lambda)-4).toFixed(1),"text-anchor":"end","class":"lbl",style:"fill:var(--color-gold)"},"稀疏阈值 λ");
}
function caption(N,err){
  var el=document.getElementById("caption"),tc=PRESETS[pi].u.length;
  if(N===0)el.innerHTML="阈值太高：所有隐单元都被压成 0，什么也重构不出来（误差 100%）。把<b>稀疏强度</b>调小一点。";
  else if(N>tc+1)el.innerHTML="<b>几乎没稀疏（λ≈0）：</b>"+N+" 个单元都微微激活，相邻单元的虚假激活给重构添了毛刺——误差 <b>"+err.toFixed(0)+"%</b>。加点稀疏约束，反而更干净。";
  else if(err>15)el.innerHTML="<b>稀疏过头：</b>只剩 <b>"+N+"</b> 个单元，把真特征也砍掉了，重构开始失真——误差 <b>"+err.toFixed(0)+"%</b>。";
  else el.innerHTML="<b>甜点区：</b>只有 <b>"+N+"</b> 个隐单元被激活，却几乎完美重构（误差 <b>"+err.toFixed(0)+"%</b>）——这个信号本就由这几个“特征”叠加而成。稀疏编码既<b>省</b>又<b>干净</b>。";
}
function render(){
  var s=encode(),xr=reconstruct(s),N=s.filter(function(v){return v>lambda;}).length,err=relErr(xr);
  document.getElementById("lamVal").textContent=lambda.toFixed(2);
  document.getElementById("stat").textContent="活跃 "+N+"/"+K+" 个 · 误差 "+err.toFixed(0)+"%";
  drawSig(s,xr);drawCode(s);caption(N,err);
}
document.getElementById("lam").addEventListener("input",function(e){lambda=+e.target.value;render();});
document.getElementById("newx").addEventListener("click",function(){pi=(pi+1)%PRESETS.length;buildX();render();});
buildX();render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  var seq=[0.05,0.45,0.95,0.45],k=0,sl=document.getElementById("lam");
  var iv=setInterval(function(){lambda=seq[k];sl.value=lambda;render();k++;if(k>=seq.length)clearInterval(iv);},1200);},1000);
})();
</script>
{% endraw %}
