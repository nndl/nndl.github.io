---
layout: default
title: GAN：生成器与判别器的博弈
permalink: /viz/gan-training/
redirect_from:
  - /v/gan-training/
---

{% raw %}
<style>
.ganlab .axis{stroke:var(--color-border);stroke-width:1;}
.ganlab .alab{font:10px var(--font-mono);fill:var(--color-text-muted);}
.ganlab .barreal{fill:var(--color-text-soft);opacity:.30;}
.ganlab .barfake{fill:var(--color-gold);opacity:.72;}
.ganlab .dcurve{fill:none;stroke:var(--color-accent);stroke-width:2.6;stroke-linejoin:round;}
.ganlab .dhalf{stroke:var(--color-border-strong);stroke-width:1;stroke-dasharray:4 3;opacity:.7;}
.ganlab .mustar{stroke:#b5524a;stroke-width:1.6;stroke-dasharray:3 3;opacity:.8;}
.ganlab .dlab{font:600 10px var(--font-mono);fill:var(--color-accent);}
.ganlab .pill2{display:inline-flex;gap:6px;align-items:baseline;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# GAN：生成器与判别器的博弈

生成对抗网络（GAN）让两个网络打一场“猫鼠游戏”。**判别器** D 是警察，努力分辨哪些样本是真数据、哪些是仿造的；**生成器** G 是造假者，努力造出能骗过 D 的假样本。两边交替训练、互相施压：D 越练越会挑刺，G 就被逼着把假货做得越来越像。理论上的终点是——G 造的分布和真数据完全重合，D 再也分不出真假，只能两边都猜 50%。这里把一切压到一维：真数据是一条钟形分布，G 只能平移、缩放一个标准正态。点“自动训练”，看金色的假直方图怎么一步步贴上真分布。

<section class="vizui ganlab" id="ganlab">
  <p class="vizui__lead">淡灰直方图是<b>真数据</b>（来自 N(0.62, 0.10²)），<span style="color:var(--color-gold);font-weight:600">金色直方图是 G 造的假数据</span>，<span style="color:var(--color-accent);font-weight:600">蓝曲线是 D(x)</span>——判别器认为 x 是“真”的概率（0~1）。训练让蓝曲线先学会一高一低分辨真假，再被 G 拉平回 0.5。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <button class="vizui-btn vizui-btn--go" id="train" type="button">▶ 自动训练</button>
      <button class="vizui-btn" id="step" type="button">单步</button>
      <button class="vizui-btn" id="reset" type="button">重置</button>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="preset">真分布：单峰</span>
      <button class="vizui-btn" id="bimodal" type="button">切到双峰真实分布</button>
    </div>
    <svg class="vizui-chart" id="plot" viewBox="0 0 460 250" role="img" aria-label="GAN 真假直方图与判别器曲线"></svg>
    <div class="vizui-bar" style="justify-content:space-between;font-size:.86rem;margin-top:8px">
      <span>训练步数 <b id="stepc" style="font-family:var(--font-mono);color:var(--color-text)">0</b></span>
      <span class="pill2">G 的 μ <b id="gmu" style="font-family:var(--font-mono);color:var(--color-gold)">0.25</b> → μ*=0.62</span>
      <span class="pill2">G 的 σ <b id="gsd" style="font-family:var(--font-mono);color:var(--color-gold)">0.30</b> → σ*=0.10</span>
    </div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>D 学着分辨</b><p>判别器做梯度上升，在真数据处把 D(x) 推高、在假数据处压低——蓝曲线先拱出“真高假低”的形状。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>G 学着骗过</b><p>生成器朝“让 D 觉得是真”的方向挪动 μ、σ（非饱和损失），把假直方图往 D 评分高的地方搬。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>纳什均衡</b><p>当假分布贴上真分布，D 处处只能猜 0.5、两边谁也占不到便宜——博弈到达平衡，训练自然停下。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var MU_STAR=0.62, SD_STAR=0.10;
var MODES=[[0.30,0.07],[0.80,0.07]];
var lrD=0.08, lrG=0.005, kD=2, BATCH=64;
var bimodal=false;
var w=[0,0,0], mu=0.25, sd=0.30, steps=0, playing=false, timer=null, R=null;

function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
function gauss(r){var u=0,v=0;while(!u)u=r();while(!v)v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}
function sig(z){return 1/(1+Math.exp(-z));}
function D(x){return sig(w[0]+w[1]*x+w[2]*x*x);}
function realSample(){if(bimodal){var m=R()<0.5?MODES[0]:MODES[1];return m[0]+gauss(R)*m[1];}return MU_STAR+gauss(R)*SD_STAR;}
function fakeX(z){return mu+sd*z;}

function dStep(){
  var g0=0,g1=0,g2=0;
  for(var i=0;i<BATCH;i++){
    var xr=realSample(),dr=D(xr),c1=(1-dr);
    g0+=c1; g1+=c1*xr; g2+=c1*xr*xr;
    var z=gauss(R),xf=fakeX(z),df=D(xf),c2=-df;
    g0+=c2; g1+=c2*xf; g2+=c2*xf*xf;
  }
  w[0]+=lrD*g0/BATCH; w[1]+=lrD*g1/BATCH; w[2]+=lrD*g2/BATCH;
}
function gStep(){
  var gmu=0,gsd=0;
  for(var i=0;i<BATCH;i++){
    var z=gauss(R),x=fakeX(z),dd=D(x),dl=(1-dd)*(w[1]+2*w[2]*x);
    gmu+=dl; gsd+=dl*z;
  }
  mu+=lrG*gmu/BATCH; sd+=lrG*gsd/BATCH; if(sd<0.04)sd=0.04;
}
function tick(){for(var k=0;k<kD;k++)dStep();gStep();steps++;}
function converged(){return !bimodal && Math.abs(mu-MU_STAR)<0.09 && Math.abs(sd-SD_STAR)<0.018;}

function reset(){R=rng(7);w=[0,0,0];mu=0.25;sd=0.30;steps=0;}

// 用真分布采样一批样本，做成直方图（密度归一），返回每个 bin 的密度
var NB=34, XLO=0.0, XHI=1.2;
function histReal(n){var R2=rng(101),h=new Array(NB).fill(0);
  for(var i=0;i<n;i++){var x=bimodal?(R2()<0.5?MODES[0]:MODES[1]):[MU_STAR,SD_STAR];var v=x[0]+gauss(R2)*x[1];var b=Math.floor((v-XLO)/(XHI-XLO)*NB);if(b>=0&&b<NB)h[b]++;}
  var bw=(XHI-XLO)/NB;for(var k=0;k<NB;k++)h[k]=h[k]/(n*bw);return h;}
function histFake(n){var R3=rng(202),h=new Array(NB).fill(0);
  for(var i=0;i<n;i++){var v=fakeX(gauss(R3));var b=Math.floor((v-XLO)/(XHI-XLO)*NB);if(b>=0&&b<NB)h[b]++;}
  var bw=(XHI-XLO)/NB;for(var k=0;k<NB;k++)h[k]=h[k]/(n*bw);return h;}

var SVGNS="http://www.w3.org/2000/svg",W=460,H=250,pl=26,pr=16,ptop=16,pb=30,YMAX=4.6;
function px(x){return pl+(x-XLO)/(XHI-XLO)*(W-pl-pr);}
function pyD(d){return ptop+(1-d)*(H-ptop-pb);}        // D∈[0,1] 映射到上下
function pyH(den){return (H-pb)-Math.min(YMAX,den)/YMAX*(H-ptop-pb);}
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}

function draw(){
  var svg=document.getElementById("plot");while(svg.firstChild)svg.removeChild(svg.firstChild);
  E(svg,"line",{x1:pl,y1:H-pb,x2:W-pr,y2:H-pb,"class":"axis"});
  [0,0.2,0.4,0.6,0.8,1.0,1.2].forEach(function(v){E(svg,"text",{x:px(v),y:H-pb+14,"text-anchor":"middle","class":"alab"}).textContent=v.toFixed(1);});
  // μ* 参考线
  E(svg,"line",{x1:px(MU_STAR),y1:ptop,x2:px(MU_STAR),y2:H-pb,"class":"mustar"});
  // 真直方图（淡）
  var hr=histReal(20000),bw=(XHI-XLO)/NB;
  for(var i=0;i<NB;i++){if(hr[i]<=0)continue;var x0=XLO+i*bw;E(svg,"rect",{x:px(x0)+0.5,y:pyH(hr[i]),width:Math.max(1,px(x0+bw)-px(x0)-1),height:(H-pb)-pyH(hr[i]),"class":"barreal"});}
  // 假直方图（金）
  var hf=histFake(20000);
  for(var j=0;j<NB;j++){if(hf[j]<=0)continue;var fx0=XLO+j*bw;E(svg,"rect",{x:px(fx0)+0.5,y:pyH(hf[j]),width:Math.max(1,px(fx0+bw)-px(fx0)-1),height:(H-pb)-pyH(hf[j]),"class":"barfake"});}
  // D=0.5 参考线
  E(svg,"line",{x1:pl,y1:pyD(0.5),x2:W-pr,y2:pyD(0.5),"class":"dhalf"});
  // D(x) 曲线
  var cp=[];for(var t=0;t<=120;t++){var x=XLO+(XHI-XLO)*t/120;cp.push(px(x)+","+pyD(D(x)));}
  E(svg,"polyline",{points:cp.join(" "),"class":"dcurve"});
  E(svg,"text",{x:W-pr-2,y:pyD(0.5)-4,"text-anchor":"end","class":"dlab"}).textContent="D(x)=0.5";
}

function render(){
  document.getElementById("stepc").textContent=steps;
  document.getElementById("gmu").textContent=mu.toFixed(2);
  document.getElementById("gsd").textContent=sd.toFixed(2);
  document.getElementById("preset").textContent=bimodal?"真分布：双峰":"真分布：单峰";
  draw();caption();
}
function caption(){
  var el=document.getElementById("caption");
  if(bimodal){
    el.innerHTML="<b>模式崩溃。</b>真数据有两个峰（0.30 和 0.80），但 G(z)=μ+σ·z 只能造一个钟形——它没法同时覆盖两个峰，最后只能瘫在中间（μ≈"+mu.toFixed(2)+"），两边都顾不上。这就是 GAN 著名的“模式崩溃”：生成器太弱，干脆放弃多样性。";
    return;
  }
  if(steps===0)
    el.innerHTML="起点：G 的假分布（金）偏在左边、又太宽，和真分布（灰）对不上。点“自动训练”，先看蓝曲线 D 怎么拱起来分辨真假，再看金直方图被拉过去贴上灰直方图。";
  else if(converged())
    el.innerHTML="<b>贴上了！</b>G 的 μ 从 0.25 一路挪到 "+mu.toFixed(2)+"、σ 从 0.30 收到 "+sd.toFixed(2)+"（≈σ*=0.10），金直方图已大幅盖住灰直方图。此时 D(x) 被压平到 0.5 附近——真假难分、博弈逼近平衡（μ 还会继续慢慢爬向 0.62）。";
  else
    el.innerHTML="第 "+steps+" 步：D 学着分辨（蓝曲线在真数据处偏高、假数据处偏低），G 被逼着把 μ 从 0.25 往 0.62 挪、把 σ 从 0.30 收到 0.10。当前 μ="+mu.toFixed(2)+"、σ="+sd.toFixed(2)+"，继续训练会越来越贴。";
}

function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("train").textContent="▶ 自动训练";}
function play(){stop();playing=true;document.getElementById("train").textContent="⏸ 暂停";
  timer=setInterval(function(){tick();render();if(steps>=600||converged())stop();},70);}

document.getElementById("train").addEventListener("click",function(){playing?stop():play();});
document.getElementById("step").addEventListener("click",function(){stop();tick();render();});
document.getElementById("reset").addEventListener("click",function(){stop();bimodal=false;reset();render();});
document.getElementById("bimodal").addEventListener("click",function(){stop();bimodal=true;reset();render();});

reset();render();
setTimeout(function(){
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){
    for(var i=0;i<600&&!converged();i++)tick();render();return;
  }
  play();
},900);
})();
</script>
{% endraw %}
