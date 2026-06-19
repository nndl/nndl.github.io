---
layout: default
title: RLHF：从人类偏好到奖励模型
permalink: /viz/rlhf-reward-model/
redirect_from:
  - /v/rlhf-reward-model/
---

{% raw %}
<style>
.rmlab .axis{stroke:var(--color-border);stroke-width:1;}
.rmlab .grid{stroke:var(--color-border);stroke-width:1;opacity:.35;}
.rmlab .rcurve{fill:none;stroke:var(--color-accent);stroke-width:2.8;stroke-linejoin:round;}
.rmlab .pref{stroke:var(--color-text-muted);stroke-width:1.5;opacity:.55;}
.rmlab .win{fill:var(--color-forest);}
.rmlab .lose{fill:#b5524a;}
.rmlab .pirefc{fill:none;stroke:var(--color-text-muted);stroke-width:1.8;stroke-dasharray:5 4;opacity:.75;}
.rmlab .pifill{fill:var(--color-gold);opacity:.16;}
.rmlab .pic{fill:none;stroke:var(--color-gold);stroke-width:2.8;stroke-linejoin:round;}
.rmlab .meanline{stroke:var(--color-gold);stroke-width:1.6;stroke-dasharray:3 3;}
.rmlab .lbl{font:600 11px var(--font-mono);fill:var(--color-text-muted);}
.rmlab svg{touch-action:none;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# RLHF：从人类偏好到奖励模型

人类很难给一个回答打出“7.3 分”，但很容易说出“A 比 B 好”。RLHF 就建在这种**成对偏好**上：先从一堆“A≻B”里拟合出一条**奖励曲线** r(x)（用 Bradley-Terry 模型），再把语言模型这个“策略”往高奖励的方向推；同时拴一根 **KL 缰绳**，别让它为了刷分跑得离原模型太远。下面把一切压到一根一维“回答好坏”轴 x∈[0,1] 上——**越靠右的回答越好，但模型一开始并不知道**。拖动 β，看策略怎么从原模型滑向高分区。

<section class="vizui rmlab" id="rmlab">
  <p class="vizui__lead">上图：<span style="color:var(--color-forest);font-weight:600">绿点</span>是每对里“更好”的回答、<span style="color:#b5524a;font-weight:600">红点</span>是“更差”的，连线就是一条“≻”偏好；<span style="color:var(--color-accent);font-weight:600">蓝线</span>是拟合出的奖励 r(x)。下图：<span style="color:var(--color-text-muted);font-weight:600">灰虚线</span>是原模型 π_ref，<span style="color:#b7791f;font-weight:600">金色</span>是 RLHF 后的策略 π。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="beta">KL 强度 β（大＝贴着原模型，小＝只追高分）</label>
        <input type="range" id="beta" min="0.2" max="6" step="0.05" value="2" style="width:200px">
        <output id="betaVal">2.00</output>
      </span>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="info">—</span>
      <button class="vizui-btn vizui-btn--go" id="refit" type="button">↻ 重新拟合奖励</button>
    </div>
    <svg class="vizui-chart" id="rplot" viewBox="0 0 460 200" role="img" aria-label="偏好对与奖励曲线"></svg>
    <p class="vizui-panel__title" style="margin-top:6px">策略密度：原模型 π_ref（虚线）→ RLHF 策略 π（金色）</p>
    <svg class="vizui-chart" id="pplot" viewBox="0 0 460 150" role="img" aria-label="策略密度"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>只用成对偏好</b><p>人类不打分、只说“A 比 B 好”。Bradley-Terry 用 σ(r_W − r_L) 解释每对胜负，最大化它就拟合出奖励曲线。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>π ∝ π_ref·exp(r/β)</b><p>最优策略把奖励高的回答概率抬高。β 越小，指数项越尖，概率质量越往高分区集中。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>KL 拴住（β）</b><p>β 是缰绳：太松（β 小）会“奖励黑客”——为了刷高分跑到原模型从没见过的怪区域、开始胡说。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
/* ---------- 确定性 RNG（mulberry32） ---------- */
function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
function sig(z){return 1/(1+Math.exp(-z));}
function rstar(x){return 6*(x-0.5);}              /* 隐藏的真实质量 */

/* ---------- 偏好对：Bradley-Terry 在 r* 上采样 ---------- */
var SEED=185, NP=7, pairs=[];
function samplePairs(){
  var r=rng(SEED);pairs=[];
  for(var i=0;i<NP;i++){
    var xa=r(), xb=r();
    var winnerA = r()<sig(rstar(xa)-rstar(xb));   /* A 胜的概率 = σ(r*(xA)−r*(xB)) */
    pairs.push(winnerA?[xa,xb]:[xb,xa]);          /* [xW, xL] */
  }
}
samplePairs();

/* ---------- 奖励模型：7 个 RBF 凸包，θ 线性组合 ---------- */
var K=7, sigma=0.18, centers=[]; for(var k=0;k<K;k++)centers.push(k/(K-1));
function phi(x){return centers.map(function(c){return Math.exp(-(x-c)*(x-c)/(2*sigma*sigma));});}
var theta=new Array(K).fill(0);
function rth(x){var ph=phi(x),s=0;for(var k=0;k<K;k++)s+=theta[k]*ph[k];return s;}

/* Bradley-Terry 对数似然的梯度上升（+微小 L2 平滑） */
var LR=0.06, L2=0.01;
function btStep(){
  var g=new Array(K).fill(0);
  pairs.forEach(function(p){
    var phW=phi(p[0]), phL=phi(p[1]), d=0;
    for(var k=0;k<K;k++)d+=theta[k]*(phW[k]-phL[k]);   /* r_W − r_L */
    var s=sig(-d);                                      /* dlogσ(d)/dd = σ(−d) */
    for(var k=0;k<K;k++)g[k]+=s*(phW[k]-phL[k]);
  });
  for(var k=0;k<K;k++)theta[k]+=LR*(g[k]-L2*theta[k]);
}
function resetTheta(){theta=new Array(K).fill(0);}
function fitFull(steps){resetTheta();var n=(steps===undefined?500:steps);for(var t=0;t<n;t++)btStep();}

/* ---------- 策略：π_ref 高斯 @0.5，π ∝ π_ref·exp(r/β) ---------- */
var beta=2.0, GN=121;
function piref(x){return Math.exp(-(x-0.5)*(x-0.5)/(2*0.22*0.22));}
function policyArr(){
  var xs=[],pr=[],pi=[],Zr=0,Zp=0,i;
  for(i=0;i<GN;i++){var x=i/(GN-1);var a=piref(x),b=a*Math.exp(rth(x)/beta);xs.push(x);pr.push(a);pi.push(b);Zr+=a;Zp+=b;}
  for(i=0;i<GN;i++){pr[i]/=Zr;pi[i]/=Zp;}
  var mr=0,mp=0;for(i=0;i<GN;i++){mr+=xs[i]*pr[i];mp+=xs[i]*pi[i];}
  return {xs:xs,pr:pr,pi:pi,meanRef:mr,meanPi:mp};
}

/* ---------- SVG helpers ---------- */
var SVGNS="http://www.w3.org/2000/svg";
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
/* reward 图坐标 */
var RW=460,RH=200,rl=30,rr=12,rt=12,rb=24,RMIN=-6,RMAX=6;
function rx(x){return rl+x*(RW-rl-rr);}
function ry(v){return (RH-rb)-(v-RMIN)/(RMAX-RMIN)*(RH-rt-rb);}
/* policy 图坐标 */
var PW=460,PH=150,plL=30,plR=12,plT=10,plB=22;
function px(x){return plL+x*(PW-plL-plR);}

function drawReward(){
  var svg=document.getElementById("rplot");while(svg.firstChild)svg.removeChild(svg.firstChild);
  /* 网格 + 轴 */
  var i;
  for(i=0;i<=10;i+=2){E(svg,"line",{x1:rx(i/10),y1:rt,x2:rx(i/10),y2:RH-rb,"class":"grid"});}
  E(svg,"line",{x1:rl,y1:ry(0),x2:RW-rr,y2:ry(0),"class":"axis"});
  E(svg,"text",{x:rl-4,y:ry(0)+3,"text-anchor":"end","class":"lbl"}).textContent="0";
  E(svg,"text",{x:RW-rr,y:RH-6,"text-anchor":"end","class":"lbl"}).textContent="回答更好 →";
  /* 偏好对连线（每对 xL→xW 在轴上画一段“≻”） */
  pairs.forEach(function(p){
    E(svg,"line",{x1:rx(p[1]),y1:ry(0),x2:rx(p[0]),y2:ry(0),"class":"pref"});
  });
  /* 奖励曲线 */
  var pts=[];for(i=0;i<=100;i++){var x=i/100;pts.push(rx(x)+","+ry(Math.max(RMIN,Math.min(RMAX,rth(x)))));}
  E(svg,"polyline",{points:pts.join(" "),"class":"rcurve"});
  /* 偏好点（落在奖励曲线上更直观：r(xW) 高于 r(xL)） */
  pairs.forEach(function(p){
    E(svg,"circle",{cx:rx(p[1]),cy:ry(Math.max(RMIN,Math.min(RMAX,rth(p[1])))),r:3.6,"class":"lose"});
    E(svg,"circle",{cx:rx(p[0]),cy:ry(Math.max(RMIN,Math.min(RMAX,rth(p[0])))),r:3.6,"class":"win"});
  });
  E(svg,"text",{x:rl+2,y:rt+10,"class":"lbl",fill:"var(--color-accent)"}).textContent="r(x)";
}

function drawPolicy(P){
  var svg=document.getElementById("pplot");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var mx=0,i;for(i=0;i<GN;i++){mx=Math.max(mx,P.pr[i],P.pi[i]);}
  mx=mx*1.08||1;
  function yy(v){return (PH-plB)-(v/mx)*(PH-plT-plB);}
  E(svg,"line",{x1:plL,y1:PH-plB,x2:PW-plR,y2:PH-plB,"class":"axis"});
  /* π 填充 */
  var fill=[px(0)+","+(PH-plB)];
  for(i=0;i<GN;i++)fill.push(px(P.xs[i])+","+yy(P.pi[i]));
  fill.push(px(1)+","+(PH-plB));
  E(svg,"polygon",{points:fill.join(" "),"class":"pifill"});
  /* π_ref 虚线 */
  var pr=[];for(i=0;i<GN;i++)pr.push(px(P.xs[i])+","+yy(P.pr[i]));
  E(svg,"polyline",{points:pr.join(" "),"class":"pirefc"});
  /* π 实线 */
  var pi=[];for(i=0;i<GN;i++)pi.push(px(P.xs[i])+","+yy(P.pi[i]));
  E(svg,"polyline",{points:pi.join(" "),"class":"pic"});
  /* 两条均值竖线 */
  E(svg,"line",{x1:px(P.meanRef),y1:plT,x2:px(P.meanRef),y2:PH-plB,"class":"meanline",stroke:"var(--color-text-muted)"});
  E(svg,"line",{x1:px(P.meanPi),y1:plT,x2:px(P.meanPi),y2:PH-plB,"class":"meanline"});
  E(svg,"text",{x:px(P.meanPi),y:plT+9,"text-anchor":"middle","class":"lbl",fill:"var(--color-gold)"}).textContent="π 均值 "+P.meanPi.toFixed(2);
  E(svg,"text",{x:px(P.meanRef),y:PH-6,"text-anchor":"middle","class":"lbl"}).textContent="π_ref "+P.meanRef.toFixed(2);
}

function render(){
  document.getElementById("betaVal").textContent=beta.toFixed(2);
  drawReward();
  var P=policyArr();
  drawPolicy(P);
  document.getElementById("info").textContent=NP+" 对偏好 · π 均值 "+P.meanPi.toFixed(2);
  caption(P);
}
function caption(P){
  var el=document.getElementById("caption");
  var msg;
  if(beta>=4)msg="<b>β 很大（"+beta.toFixed(2)+"）：</b>KL 缰绳很紧，π 几乎贴着原模型 π_ref（均值仅从 0.50 挪到 "+P.meanPi.toFixed(2)+"）——奖励还没怎么发挥作用。";
  else if(beta<=0.5)msg="<b>β 很小（"+beta.toFixed(2)+"）：</b>只追高分，π 几乎全压到右端高奖励区（均值 "+P.meanPi.toFixed(2)+"）——但太贪心就会“奖励黑客”，跑到原模型没见过的地方胡说。";
  else msg="β＝"+beta.toFixed(2)+"：奖励把概率质量往右拉，π 的均值从 π_ref 的 0.50 移到了 <b>"+P.meanPi.toFixed(2)+"</b>。β 越小越往右，越大越被拴回原模型。";
  el.innerHTML="7 条“A 比 B 好”的偏好 → 拟合出一条向右上升的奖励曲线（左端 r≈"+rth(0).toFixed(1)+"，右端 r≈"+rth(1).toFixed(1)+"）。"+msg;
}

/* ---------- 交互 ---------- */
var demo=null;
function stopDemo(){if(demo){clearInterval(demo);demo=null;}}
document.getElementById("beta").addEventListener("input",function(e){stopDemo();beta=+e.target.value;render();});
document.getElementById("refit").addEventListener("click",function(){stopDemo();fitFull(500);render();});

/* ---------- 启动 ---------- */
var reduce=window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches;
if(reduce){
  /* 直接跳到拟合好的奖励 + 小 β 的右移策略 */
  fitFull(500);beta=0.5;document.getElementById("beta").value=beta;render();
}else{
  resetTheta();render();          /* θ=0：奖励是平的，等会儿看它长出来 */
  setTimeout(function(){
    var FIT_FRAMES=25, PER=20;     /* 共 25×20=500 步，落在干净的拟合曲线上 */
    var seq=[5,3.5,2.5,1.6,1.0,0.6,0.35,0.2];
    var step=0;
    demo=setInterval(function(){
      if(step<FIT_FRAMES){          /* 阶段一：θ 上升，奖励曲线向右上方长出来 */
        for(var s=0;s<PER;s++)btStep();
        render();
      }else{                        /* 阶段二：β 从大扫到小，π 从 π_ref 滑向右端高分区 */
        var j=step-FIT_FRAMES;
        if(j>=seq.length){stopDemo();return;}
        beta=seq[j];document.getElementById("beta").value=beta;render();
      }
      step++;
    },140);
  },900);
}
})();
</script>
{% endraw %}
