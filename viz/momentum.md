---
layout: default
title: 学习率与动量
permalink: /viz/momentum/
redirect_from:
  - /v/momentum/
---

{% raw %}
<style>
.mtlab .contour{fill:none;stroke:var(--color-border-strong);stroke-width:1;opacity:.55;}
.mtlab .minmark{fill:var(--color-gold);stroke:#fff;stroke-width:1.5;}
.mtlab .path-s{fill:none;stroke:#b5524a;stroke-width:2;opacity:.85;}
.mtlab .path-m{fill:none;stroke:var(--color-forest);stroke-width:2;opacity:.9;}
.mtlab .ball-s{fill:#b5524a;stroke:#fff;stroke-width:1.5;}
.mtlab .ball-m{fill:var(--color-forest);stroke:#fff;stroke-width:1.5;}
.mtlab .valley-lbl{font:11px var(--font-mono);fill:var(--color-text-muted);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 学习率与动量

训练神经网络就是“下山”找最低点。但很多损失面像一条又窄又长的山谷：普通梯度下降会在两侧山壁之间来回横跳、磨磨蹭蹭才到底。给它加上“动量”（像下坡的小球积累惯性），横跳被抵消、顺着谷底加速——这就是 Momentum、Adam 这些优化器的核心思想。看两个小球赛跑。

<section class="vizui mtlab" id="mtlab">
  <p class="vizui__lead">红球是普通梯度下降，绿球带动量。两球从同一点出发，金点是谷底（最低点）。调节学习率和动量，看谁先到、谁会震荡甚至冲出去。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="lr">学习率</label>
        <input type="range" id="lr" min="0.02" max="0.13" step="0.005" value="0.090" style="width:150px">
        <output id="lrVal">0.090</output>
      </span>
      <span class="vizui-field"><label for="beta">动量</label>
        <input type="range" id="beta" min="0" max="0.95" step="0.05" value="0.40" style="width:150px">
        <output id="betaVal">0.40</output>
      </span>
      <span class="vizui-spacer"></span>
      <button class="vizui-btn vizui-btn--go" id="go" type="button">▶ 开始</button>
      <button class="vizui-btn" id="reset" type="button">重置</button>
    </div>
  </div>

  <div class="vizui-panel">
    <div class="vizui-legend">
      <span><i class="dot" style="background:#b5524a"></i>普通梯度下降</span>
      <span><i class="dot" style="background:var(--color-forest)"></i>带动量</span>
      <span><i class="dot" style="background:var(--color-gold)"></i>谷底</span>
      <span class="vizui-spacer"></span><span id="stepLbl" class="vizui-pill">第 0 步</span>
    </div>
    <svg class="vizui-chart" id="surf" viewBox="0 0 480 240" role="img" aria-label="损失面与下降轨迹"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:#b5524a"><b>学习率太大</b><p>步子迈太大，在陡的方向上越跳越远，直接冲出山谷——训练“发散”。</p></div>
    <div class="card" style="--wc:var(--color-text-muted)"><b>学习率太小</b><p>稳是稳，但每步挪一点点，要很多步才到底，训练很慢。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>加上动量</b><p>惯性抵消了来回横跳，又在平缓方向上越滚越快，更稳更快地到达谷底。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var A=1, B=18;                 /* 损失 f = 0.5(A x² + B y²)，窄长山谷 */
var START={x:-2.45,y:0.95};
var lr=0.090, beta=0.40;
var posS, posM, velM, pathS, pathM, step, playing=false, timer=null, divergedS=false;

function grad(p){return {x:A*p.x, y:B*p.y};}
function dist(p){return Math.hypot(p.x,p.y);}
function init(){
  posS={x:START.x,y:START.y}; posM={x:START.x,y:START.y}; velM={x:0,y:0};
  pathS=[{x:posS.x,y:posS.y}]; pathM=[{x:posM.x,y:posM.y}]; step=0; divergedS=false;
}
function stepOnce(){
  if(!divergedS){
    var gS=grad(posS); posS={x:posS.x-lr*gS.x, y:posS.y-lr*gS.y};
    if(dist(posS)>6){divergedS=true;} else pathS.push({x:posS.x,y:posS.y});
  }
  var gM=grad(posM); velM={x:beta*velM.x-lr*gM.x, y:beta*velM.y-lr*gM.y};
  posM={x:posM.x+velM.x, y:posM.y+velM.y};
  if(dist(posM)<6) pathM.push({x:posM.x,y:posM.y});
  step++;
}

/* ---------- 绘图 ---------- */
var SVGNS="http://www.w3.org/2000/svg", W=480,H=240,pad=18;
function wx(x){return pad+(x+3)/6*(W-2*pad);}
function wy(y){return pad+(1.5-y)/3.0*(H-2*pad);}
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}
function poly(svg,arr,cls){if(arr.length<2)return;var pts=arr.map(function(p){return wx(p.x)+","+wy(p.y);});E(svg,"polyline",{points:pts.join(" "),"class":cls});}
function draw(){
  var svg=document.getElementById("surf"); while(svg.firstChild)svg.removeChild(svg.firstChild);
  var clip=E(svg,"clipPath",{id:"sclip"});E(clip,"rect",{x:0,y:0,width:W,height:H});
  // 等高线椭圆（精确：二次型的等高线是椭圆）
  [0.06,0.18,0.4,0.8,1.5,2.6].forEach(function(c){
    var rx=Math.sqrt(2*c/A), ry=Math.sqrt(2*c/B);
    E(svg,"ellipse",{cx:wx(0),cy:wy(0),rx:wx(rx)-wx(0),ry:wy(0)-wy(ry),"class":"contour"});
  });
  E(svg,"text",{x:wx(0),y:wy(0)-58,"text-anchor":"middle","class":"valley-lbl"}).textContent="窄长山谷";
  var g=E(svg,"g",{"clip-path":"url(#sclip)"});
  poly(g,pathS,"path-s"); poly(g,pathM,"path-m");
  E(svg,"circle",{cx:wx(0),cy:wy(0),r:5,"class":"minmark"});
  if(!divergedS)E(svg,"circle",{cx:wx(posS.x),cy:wy(posS.y),r:5,"class":"ball-s"});
  E(svg,"circle",{cx:wx(posM.x),cy:wy(posM.y),r:5,"class":"ball-m"});
  document.getElementById("stepLbl").textContent="第 "+step+" 步";
}

function caption(){
  var el=document.getElementById("caption"), zig=lr*B>1;
  if(divergedS){
    if(dist(posM)>6)el.innerHTML="<b>两个球都发散了！</b>学习率 "+lr.toFixed(3)+" 太大——这个陡峭方向上步子过大，连动量也拉不住，双双冲出了山谷。把学习率调小些。";
    else el.innerHTML="<b>红球发散了！</b>学习率 "+lr.toFixed(3)+" 在陡峭方向上步子太大，普通梯度下降越跳越远冲出了山谷。绿球靠动量仍稳稳收敛——这正是动量的好处。";
    return;
  }
  if(step===0){el.innerHTML=zig?"点“开始”。红球（普通梯度下降）会在山谷两壁间来回横跳；绿球（带动量）在动量够大时能抵消横跳、顺谷底加速甩开红球——动量太小时它也会跟着晃。":"点“开始”。当前学习率偏小，红球只会稳稳地、慢慢地往谷底挪（步子太小、不横跳，很慢）；绿球靠动量快一点。想看“横跳”，把学习率往右调大。";return;}
  var dS=dist(posS), dM=dist(posM);
  if(dM<0.05 && dS>0.3){el.innerHTML="第 "+step+" 步：<b>绿球已经到底</b>，红球还在半路"+(zig?"横跳":"慢慢挪")+"。同样的学习率，动量明显更快。";return;}
  el.innerHTML="第 "+step+" 步：红球离谷底 "+dS.toFixed(2)+"，绿球 "+dM.toFixed(2)+"。"+(zig?(beta<0.7?"动量偏小，绿球也跟着晃——把“动量”调大些，看它抵消横跳、甩开红球。":""):"学习率偏小、收敛慢——往右调大就能看到红球横跳。");
}
function render(){draw();caption();}

function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("go").textContent="▶ 开始";}
function play(){
  if(dist(posS)<0.03&&dist(posM)<0.03||divergedS){init();render();}
  stop();playing=true;document.getElementById("go").textContent="⏸ 暂停";
  timer=setInterval(function(){
    stepOnce();render();
    if((dist(posM)<0.02&&(divergedS||dist(posS)<0.03))||step>=160){stop();}
  },110);
}
document.getElementById("lr").addEventListener("input",function(e){lr=+e.target.value;document.getElementById("lrVal").textContent=lr.toFixed(3);stop();init();render();});
document.getElementById("beta").addEventListener("input",function(e){beta=+e.target.value;document.getElementById("betaVal").textContent=beta.toFixed(2);stop();init();render();});
document.getElementById("go").addEventListener("click",function(){playing?stop():play();});
document.getElementById("reset").addEventListener("click",function(){stop();init();render();});

/* 启动 + 自动演示 */
init();render();
setTimeout(function(){
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){for(var i=0;i<60;i++)stepOnce();render();return;}
  play();
},900);
})();
</script>
{% endraw %}
