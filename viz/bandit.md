---
layout: default
title: 多臂老虎机
permalink: /viz/bandit/
redirect_from:
  - /v/bandit/
---

{% raw %}
<style>
.bdlab .arms{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;}
.bdlab .arm{border:1px solid var(--color-border);border-radius:var(--radius-md);background:var(--color-bg-pure);padding:14px 12px;cursor:pointer;text-align:center;transition:transform .12s var(--ease-out),border-color .2s,box-shadow .2s;}
.bdlab .arm:hover{transform:translateY(-2px);border-color:var(--color-accent);}
.bdlab .arm.best{border-color:var(--color-gold);box-shadow:0 0 0 2px rgba(183,121,31,.18);}
.bdlab .arm.flash-win{animation:fw .5s;}
.bdlab .arm.flash-lose{animation:fl .5s;}
@keyframes fw{0%{background:rgba(32,106,79,.3)}100%{background:var(--color-bg-pure)}}
@keyframes fl{0%{background:rgba(181,82,74,.25)}100%{background:var(--color-bg-pure)}}
.bdlab .arm h4{margin:0 0 6px;font-size:1rem;}
.bdlab .arm .q{font:700 1.5rem var(--font-mono);color:var(--color-accent);}
.bdlab .arm .qbar{height:8px;border-radius:5px;background:var(--color-bg-section);overflow:hidden;margin:6px 0;position:relative;}
.bdlab .arm .qbar i{display:block;height:100%;background:var(--color-accent);border-radius:5px;transition:width .3s var(--ease-out);}
.bdlab .arm .qbar .truth{position:absolute;top:-2px;bottom:-2px;width:2px;background:var(--color-gold);}
.bdlab .arm .meta{font-size:.78rem;color:var(--color-text-muted);}
.bdlab .arm .pull{margin-top:8px;font-size:.82rem;color:var(--color-accent);font-weight:600;}
@media (max-width:560px){.bdlab .arms{grid-template-columns:repeat(2,1fr);}}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 多臂老虎机

面前四台老虎机，每台中奖率不同，但你事先不知道。想赢得最多，就得在两件事之间权衡：**利用**——一直拉目前看起来最好的那台；**探索**——偶尔试试别的，万一有更好的呢？只利用，可能一开始就押错、错过真正的好机器；只探索，又白白浪费机会。这就是强化学习里最核心的“探索 vs 利用”难题。

<section class="vizui bdlab" id="bdlab">
  <p class="vizui__lead">点任意一台老虎机拉一下（赢了变绿、输了变红）；或用下面的 ε-greedy 自动玩——它绝大多数时候拉最好的，偶尔随机探索一台。“估计胜率”会随着拉的次数越来越准。</p>

  <div class="vizui-panel">
    <div class="arms" id="arms"></div>
  </div>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="eps">探索率 ε</label>
        <input type="range" id="eps" min="0" max="0.5" step="0.05" value="0.1" style="width:140px">
        <output id="epsVal">0.10</output>
      </span>
      <span class="vizui-spacer"></span>
      <button class="vizui-btn vizui-btn--go" id="auto" type="button">▶ ε-greedy 自动玩</button>
      <button class="vizui-btn" id="reveal" type="button">揭晓真实概率</button>
      <button class="vizui-btn" id="reset" type="button">重置</button>
    </div>
    <div style="margin-top:10px;text-align:center;font:600 .95rem var(--font-mono);color:var(--color-text)" id="score">拉了 0 次 · 赢了 0 次</div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>利用 Exploit</b><p>拉目前估计最好的那台，把已知的好机会用足。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>探索 Explore</b><p>偶尔随机试别的，避免因为前几次手气而错判、错过真正最好的。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>ε-greedy</b><p>用一个小概率 ε 去探索、其余时间利用——简单却有效地平衡两者。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var NAMES=["A","B","C","D"], TRUE=[0.32,0.55,0.72,0.46];
var pulls=[0,0,0,0], wins=[0,0,0,0], eps=0.1, reveal=false, playing=false, timer=null, last=-1;
function Q(i){return pulls[i]>0?wins[i]/pulls[i]:0;}
function bestEst(){var b=0;for(var i=1;i<4;i++)if(Q(i)>Q(b))b=i;return b;}

function build(){
  var host=document.getElementById("arms");host.innerHTML="";
  for(var i=0;i<4;i++){(function(i){
    var a=document.createElement("div");a.className="arm";a.dataset.i=i;
    a.innerHTML='<h4>老虎机 '+NAMES[i]+'</h4><div class="q" id="q'+i+'">—</div>'+
      '<div class="qbar"><i id="qb'+i+'"></i><span class="truth" id="tr'+i+'" style="display:none"></span></div>'+
      '<div class="meta" id="m'+i+'">还没拉过</div><div class="pull" id="pl'+i+'">点我拉一下</div>';
    a.addEventListener("click",function(){pull(i,true);});
    host.appendChild(a);
  })(i);}
}
function pull(i,manual){
  var win=Math.random()<TRUE[i]; pulls[i]++; if(win)wins[i]++; last=i;
  var el=document.querySelector('.arm[data-i="'+i+'"]');
  el.classList.remove("flash-win","flash-lose"); void el.offsetWidth;
  el.classList.add(win?"flash-win":"flash-lose");
  if(manual)stop();
  render();
}
function autoStep(){var i=Math.random()<eps?Math.floor(Math.random()*4):bestEst();pull(i,false);}

function render(){
  var be=bestEst(), total=pulls.reduce(function(a,b){return a+b;},0), w=wins.reduce(function(a,b){return a+b;},0);
  for(var i=0;i<4;i++){
    document.getElementById("q"+i).textContent=pulls[i]>0?(Q(i)*100).toFixed(0)+"%":"—";
    document.getElementById("qb"+i).style.width=(Q(i)*100)+"%";
    document.getElementById("m"+i).textContent="拉了 "+pulls[i]+" 次，赢 "+wins[i]+" 次";
    document.getElementById("pl"+i).textContent=(i===last?"刚拉过":"点我拉一下");
    var tr=document.getElementById("tr"+i);tr.style.display=reveal?"block":"none";tr.style.left=(TRUE[i]*100)+"%";
    document.querySelector('.arm[data-i="'+i+'"]').classList.toggle("best",total>0&&i===be);
  }
  document.getElementById("score").textContent="拉了 "+total+" 次 · 赢了 "+w+" 次"+(total>0?"（胜率 "+(w/total*100).toFixed(0)+"%）":"");
  caption(total);
}
function caption(total){
  var el=document.getElementById("caption"), be=bestEst();
  if(total<4)el.innerHTML="刚开始，每台都还没怎么试过，估计很不准。多拉几次，或让 ε-greedy 自动玩。";
  else if(total<25)el.innerHTML="试探阶段：估计胜率还在抖动。注意 ε-greedy 会优先拉当前最好的“"+NAMES[be]+"”,但偶尔也去碰碰别的——别太早下结论。";
  else el.innerHTML="拉得越多估计越准。现在看起来最好的是<b>老虎机 "+NAMES[be]+"</b>（估计 "+(Q(be)*100).toFixed(0)+"%）。点“揭晓真实概率”对一下，看 ε-greedy 找对了没有。";
}

document.getElementById("eps").addEventListener("input",function(e){eps=+e.target.value;document.getElementById("epsVal").textContent=eps.toFixed(2);});
function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("auto").textContent="▶ ε-greedy 自动玩";}
document.getElementById("auto").addEventListener("click",function(){if(playing){stop();return;}playing=true;document.getElementById("auto").textContent="⏸ 暂停";timer=setInterval(autoStep,260);});
document.getElementById("reveal").addEventListener("click",function(){reveal=!reveal;document.getElementById("reveal").textContent=reveal?"隐藏真实概率":"揭晓真实概率";render();});
document.getElementById("reset").addEventListener("click",function(){stop();pulls=[0,0,0,0];wins=[0,0,0,0];last=-1;render();});

/* 启动 + 自动演示 */
build();render();
setTimeout(function(){
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){for(var i=0;i<200;i++)autoStep();return;}
  document.getElementById("auto").click();
},1000);
})();
</script>
{% endraw %}
