---
layout: default
title: Q-learning：从试错中学策略
permalink: /viz/q-learning/
redirect_from:
  - /v/q-learning/
---

{% raw %}
<style>
.qllab .grid{display:grid;gap:3px;max-width:480px;margin:0 auto;}
.qllab .cell{aspect-ratio:1;border-radius:5px;position:relative;display:flex;align-items:center;justify-content:center;font:600 13px var(--font-mono);}
.qllab .cell .v{position:absolute;top:3px;left:0;right:0;text-align:center;font:600 11px var(--font-mono);}
.qllab .cell.wall{background:#3a4a45;}
.qllab .cell .ico{font-size:1.3rem;}
.qllab .arr{position:absolute;font-size:1rem;color:rgba(20,40,35,.55);}
.qllab .agent{position:absolute;width:46%;height:46%;border-radius:50%;background:var(--color-accent-light);box-shadow:0 0 0 2px var(--color-bg-pure),0 1px 4px rgba(0,0,0,.35);z-index:2;}
.qllab .cell.startmark{outline:2px dashed var(--color-text-muted);outline-offset:-3px;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# Q-learning：从试错中学策略

[价值迭代]({{ '/viz/value-iteration/' | relative_url }})需要先知道环境的全部规则——每个动作会去哪、能拿多少奖励——然后用 Bellman 方程一轮轮算价值。可现实里，智能体往往什么规则都不知道，只能动手试。**Q-learning** 就是这样：智能体用 ε-greedy 在格子世界里乱逛，每走一步就用刚拿到的奖励做一次小修正（TD 更新），把“在某格做某动作有多好”记进一张 Q 表。试的次数够多，Q 表慢慢收敛，一条避开陷阱、通往宝藏的策略就自己浮现出来了——全程没碰过环境模型。点“自动训练”，看箭头怎样从一片混乱里连成一条路。

<section class="qllab vizui" id="qllab">
  <p class="vizui__lead">★ 是宝藏（+1），☠ 是陷阱（−1），深色是墙，虚线框是起点。蓝点是智能体当前位置。每格按它的最大 Q 值上色，等 Q 不再全是 0，就画出从这格出发的贪心箭头。智能体不知道任何规则，只从一次次 (状态, 动作, 奖励, 新状态) 里学。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <button class="vizui-btn vizui-btn--go" id="auto" type="button">▶ 自动训练</button>
      <button class="vizui-btn" id="ep" type="button">跑一集</button>
      <button class="vizui-btn" id="step" type="button">单步</button>
      <button class="vizui-btn" id="reset" type="button">重置</button>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="epc">第 0 集</span>
    </div>
    <div class="vizui-bar" style="margin-top:10px">
      <span class="vizui-field"><label for="eps">探索率 ε</label>
        <input type="range" id="eps" min="0" max="0.5" step="0.05" value="0.2" style="width:120px">
        <output id="epsVal">0.20</output>
      </span>
      <span class="vizui-field"><label for="alp">学习率 α</label>
        <input type="range" id="alp" min="0.1" max="0.9" step="0.1" value="0.5" style="width:120px">
        <output id="alpVal">0.50</output>
      </span>
    </div>
    <div class="grid" id="grid" style="margin-top:12px"></div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>无模型</b><p>不知道转移和奖励规则，只从一次次试错的 (s, a, r, s′) 样本里学，不需要环境模型。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>TD 更新</b><p>用“即时奖励 + 打折后继的最大 Q”当作目标，自举地修正当前这一步的 Q 估计。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>ε-greedy</b><p>大多数时候走当前最优、偶尔随机探索一下，才不会一头扎进次优、永远发现不了更好的路。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
/* 地图：g=宝藏 p=陷阱 #=墙 S=起点 .=普通 */
var MAP=[".....g",".###..","....p.","S##...","......"];
var R=MAP.length, C=MAP[0].length;
var gamma=0.95, STEP=-0.02, alpha=0.5, eps=0.2;
var type=[], start=[0,0];
for(var r0=0;r0<R;r0++){type.push([]);for(var c0=0;c0<C;c0++){var ch=MAP[r0][c0];if(ch==="S"){start=[r0,c0];type[r0].push(".");}else type[r0].push(ch);}}
var DIRS=[[-1,0,"↑"],[1,0,"↓"],[0,-1,"←"],[0,1,"→"]];

/* 可复现的种子随机数（LCG），让自动演示稳定 */
var seed=12345;
function rnd(){seed=(seed*1103515245+12345)&0x7fffffff;return seed/0x7fffffff;}

var Q,epcount,agent,playing,timer;
function reset(){
  Q=[];for(var r=0;r<R;r++){Q.push([]);for(var c=0;c<C;c++)Q[r].push([0,0,0,0]);}
  seed=12345;epcount=0;agent=[start[0],start[1]];
}
function term(r,c){return type[r][c]==="g"||type[r][c]==="p";}
function wall(r,c){return r<0||c<0||r>=R||c>=C||type[r][c]==="#";}
function reward(r,c){return type[r][c]==="g"?1:type[r][c]==="p"?-1:STEP;}
function moveResult(r,c,a){var nr=r+DIRS[a][0],nc=c+DIRS[a][1];return wall(nr,nc)?[r,c]:[nr,nc];}
function argmaxQ(r,c){var bi=0;for(var a=1;a<4;a++)if(Q[r][c][a]>Q[r][c][bi])bi=a;return bi;}
function maxQ(r,c){var m=Q[r][c][0];for(var a=1;a<4;a++)if(Q[r][c][a]>m)m=Q[r][c][a];return m;}
function nonzero(r,c){for(var a=0;a<4;a++)if(Q[r][c][a]!==0)return true;return false;}

/* 单步 TD 更新：从 agent 当前格走一步 */
function stepOnce(){
  var r=agent[0],c=agent[1];
  if(term(r,c)){agent=[start[0],start[1]];return;}
  var a=rnd()<eps?Math.floor(rnd()*4):argmaxQ(r,c);
  var n=moveResult(r,c,a), rew=reward(n[0],n[1]);
  var target=term(n[0],n[1])?rew:rew+gamma*maxQ(n[0],n[1]);
  Q[r][c][a]+=alpha*(target-Q[r][c][a]);
  agent=[n[0],n[1]];
}
/* 跑完一整集：从起点出发，直到终止或 40 步 */
function runEpisode(){
  agent=[start[0],start[1]];
  for(var s=0;s<40;s++){var r=agent[0],c=agent[1];if(term(r,c))break;stepOnce();}
  epcount++;
  agent=[start[0],start[1]];
}

/* 沿贪心策略从起点走，看能否到宝藏 */
function greedyReaches(){
  var r=start[0],c=start[1],seen={};
  for(var s=0;s<60;s++){
    if(type[r][c]==="g")return true;
    if(type[r][c]==="p")return false;
    var key=r+","+c;if(seen[key])return false;seen[key]=1;
    var n=moveResult(r,c,argmaxQ(r,c));
    if(n[0]===r&&n[1]===c)return false;
    r=n[0];c=n[1];
  }
  return false;
}

function vcol(v){
  if(v>=0){var t=Math.min(1,v);return "rgb("+Math.round(238-200*t)+","+Math.round(241-135*t)+","+Math.round(238-159*t)+")";}
  var u=Math.min(1,-v);return "rgb("+Math.round(238+(181-238)*u)+","+Math.round(241+(82-241)*u)+","+Math.round(238+(74-238)*u)+")";
}
function draw(){
  var host=document.getElementById("grid");host.innerHTML="";host.style.gridTemplateColumns="repeat("+C+",1fr)";
  for(var r=0;r<R;r++)for(var c=0;c<C;c++){
    var d=document.createElement("div"),t=type[r][c];
    if(t==="#"){d.className="cell wall";host.appendChild(d);continue;}
    d.className="cell";d.style.background=vcol(maxQ(r,c));
    if(r===start[0]&&c===start[1])d.className+=" startmark";
    if(t==="g"){d.innerHTML='<span class="ico">★</span>';d.style.color="#fff";}
    else if(t==="p"){d.innerHTML='<span class="ico">☠</span>';d.style.color="#fff";}
    else{d.innerHTML='<span class="v">'+maxQ(r,c).toFixed(2)+'</span>';
      if(nonzero(r,c))d.innerHTML+='<span class="arr">'+DIRS[argmaxQ(r,c)][2]+'</span>';}
    if(r===agent[0]&&c===agent[1])d.innerHTML+='<span class="agent"></span>';
    host.appendChild(d);
  }
}
function render(){document.getElementById("epc").textContent="第 "+epcount+" 集";draw();caption();}
function caption(){
  var el=document.getElementById("caption");
  if(epcount===0){el.innerHTML="开始：Q 表全是 0，智能体还没头绪。点“跑一集”或“自动训练”，让它在格子里乱撞着学。";return;}
  if(epcount<8){el.innerHTML="第 "+epcount+" 集：还在乱撞、Q 几乎全 0，只有挨着宝藏和陷阱的格子刚被点亮一点。";return;}
  if(greedyReaches()&&epcount>=30){el.innerHTML="Q 收敛，箭头连成一条避开陷阱、通往宝藏的策略——全程没用到环境模型，纯靠试错学出来的。";return;}
  el.innerHTML="第 "+epcount+" 集：价值正从宝藏沿走过的路往回渗，靠近宝藏的格子先亮、箭头开始指向它。";
}

function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("auto").textContent="▶ 自动训练";}
function play(){stop();playing=true;document.getElementById("auto").textContent="⏸ 暂停";
  timer=setInterval(function(){runEpisode();render();if(epcount>=60&&greedyReaches())stop();else if(epcount>=200)stop();},120);}

document.getElementById("auto").addEventListener("click",function(){playing?stop():play();});
document.getElementById("ep").addEventListener("click",function(){stop();runEpisode();render();});
document.getElementById("step").addEventListener("click",function(){stop();stepOnce();render();});
document.getElementById("reset").addEventListener("click",function(){stop();reset();render();});
document.getElementById("eps").addEventListener("input",function(e){stop();eps=+e.target.value;document.getElementById("epsVal").textContent=eps.toFixed(2);});
document.getElementById("alp").addEventListener("input",function(e){stop();alpha=+e.target.value;document.getElementById("alpVal").textContent=alpha.toFixed(2);});

reset();render();
setTimeout(function(){
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){
    for(var i=0;i<300;i++)runEpisode();render();return;
  }
  play();
},900);
})();
</script>
{% endraw %}
