---
layout: default
title: 价值迭代
permalink: /viz/value-iteration/
redirect_from:
  - /v/value-iteration/
---

{% raw %}
<style>
.vilab .grid{display:grid;gap:3px;max-width:480px;margin:0 auto;}
.vilab .cell{aspect-ratio:1;border-radius:5px;position:relative;display:flex;align-items:center;justify-content:center;font:600 13px var(--font-mono);}
.vilab .cell .v{position:absolute;top:3px;left:0;right:0;text-align:center;font:600 11px var(--font-mono);}
.vilab .cell.wall{background:#3a4a45;}
.vilab .cell .ico{font-size:1.3rem;}
.vilab .arr{position:absolute;font-size:1rem;color:rgba(20,40,35,.55);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 价值迭代

强化学习里的智能体要在一个环境里找“怎么走最划算”。价值迭代的想法是：先给每个格子算一个“价值”——从这里出发，最终能拿到多少回报。这个价值从终点（宝藏）一格格往外扩散，越靠近宝藏越值钱、越靠近陷阱越亏。算清楚每个格子的价值后，最优策略就一目了然：**每步都朝价值更高的相邻格走**。点“单步”，看价值怎样从右上角的宝藏扩散开、箭头怎样连成一条最优路线。

<section class="vilab vizui" id="vilab">
  <p class="vizui__lead">★ 是宝藏（+1），☠ 是陷阱（−1），深色是墙。每格上方小字是它的价值，箭头是从这格出发的最优走向。每走一格有一点点小代价，所以智能体会找最短的安全路线。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <button class="vizui-btn vizui-btn--go" id="auto" type="button">▶ 自动迭代</button>
      <button class="vizui-btn" id="step" type="button">单步迭代</button>
      <button class="vizui-btn" id="reset" type="button">重置</button>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="iter">第 0 轮</span>
    </div>
    <div class="grid" id="grid"></div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>价值从终点扩散</b><p>每轮：每格的价值 = 朝最好方向走一步能拿到的回报 + 打折后的下一格价值。一轮轮传开。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>最优策略 = 爬价值</b><p>价值算好后，每步朝价值最高的相邻格走，就是最优路线——箭头自动连成路。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>折扣因子 γ</b><p>远处的回报要打个折（×γ），既让价值能收敛，也体现“早拿到的回报更值钱”。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var R=5,C=6,gamma=0.92,STEP=-0.03,iter=0,playing=false,timer=null;
/* 地图：g=宝藏 p=陷阱 #=墙 .=普通 */
var MAP=[".....g",".###..","....p.",".##...","......"];
var type=[],V=[];
function reset(){type=[];V=[];for(var r=0;r<R;r++){type.push([]);V.push([]);for(var c=0;c<C;c++){var ch=MAP[r][c];type[r].push(ch);V[r].push(ch==="g"?1:ch==="p"?-1:0);}}iter=0;}
function term(r,c){return type[r][c]==="g"||type[r][c]==="p";}
function wall(r,c){return r<0||c<0||r>=R||c>=C||type[r][c]==="#";}
var DIRS=[[-1,0,"↑"],[1,0,"↓"],[0,-1,"←"],[0,1,"→"]];
function next(r,c,d){var nr=r+d[0],nc=c+d[1];return wall(nr,nc)?[r,c]:[nr,nc];}
function bestAction(r,c){var bv=-1e9,bd=null;DIRS.forEach(function(d){var n=next(r,c,d),v=STEP+gamma*V[n[0]][n[1]];if(v>bv){bv=v;bd=d;}});return {v:bv,d:bd};}
function step(){var nV=V.map(function(row){return row.slice();});var ch=0;
  for(var r=0;r<R;r++)for(var c=0;c<C;c++){if(term(r,c)||type[r][c]==="#")continue;var b=bestAction(r,c);nV[r][c]=b.v;ch+=Math.abs(b.v-V[r][c]);}
  V=nV;iter++;return ch;}

function vcol(v){if(v>=0){var t=Math.min(1,v);return "rgb("+Math.round(238-200*t)+","+Math.round(241-135*t)+","+Math.round(238-159*t)+")";}
  var u=Math.min(1,-v);return "rgb("+Math.round(238+(181-238)*u)+","+Math.round(241+(82-241)*u)+","+Math.round(238+(74-238)*u)+")";}
function draw(){
  var host=document.getElementById("grid");host.innerHTML="";host.style.gridTemplateColumns="repeat("+C+",1fr)";
  for(var r=0;r<R;r++)for(var c=0;c<C;c++){
    var d=document.createElement("div"),t=type[r][c];
    if(t==="#"){d.className="cell wall";host.appendChild(d);continue;}
    d.className="cell";d.style.background=vcol(V[r][c]);
    if(t==="g"){d.innerHTML='<span class="ico">★</span>';d.style.color="#fff";}
    else if(t==="p"){d.innerHTML='<span class="ico">☠</span>';d.style.color="#fff";}
    else{d.innerHTML='<span class="v">'+V[r][c].toFixed(2)+'</span>';
      if(iter>0){var b=bestAction(r,c);d.innerHTML+='<span class="arr">'+b.d[2]+'</span>';}}
    host.appendChild(d);
  }
}
function render(){document.getElementById("iter").textContent="第 "+iter+" 轮";draw();caption();}
function caption(){
  var el=document.getElementById("caption");
  if(iter===0)el.innerHTML="开始：只有宝藏(+1)和陷阱(−1)有价值，其余格子都是 0、还没有方向。点“单步”，看价值怎样从宝藏一圈圈扩散。";
  else if(iter<5)el.innerHTML="第 "+iter+" 轮：价值正从宝藏向外渗，靠近宝藏的格子先亮起来、箭头开始指向它。";
  else el.innerHTML="价值基本收敛了：每格都标好了价值，箭头连成一条避开陷阱、通往宝藏的最优路线。从任意格出发顺着箭头走，都是最划算的走法。";
}
function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("auto").textContent="▶ 自动迭代";}
function play(){stop();playing=true;document.getElementById("auto").textContent="⏸ 暂停";timer=setInterval(function(){var ch=step();render();if(ch<0.001||iter>40)stop();},420);}
document.getElementById("auto").addEventListener("click",function(){playing?stop():play();});
document.getElementById("step").addEventListener("click",function(){stop();step();render();});
document.getElementById("reset").addEventListener("click",function(){stop();reset();render();});
reset();render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){for(var i=0;i<30;i++)step();render();return;}play();},1000);
})();
</script>
{% endraw %}
