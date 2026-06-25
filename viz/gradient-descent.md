---
layout: default
title: 梯度下降下山
description: "小球沿曲线下山找最低点；调学习率看收敛、震荡，体会局部最优陷阱。"
permalink: /viz/gradient-descent/
redirect_from:
  - /v/gradient-descent/
---

{% raw %}
<style>
.gdlab .curve{fill:none;stroke:var(--color-accent);stroke-width:2.5;}
.gdlab .ground{fill:var(--color-accent-soft);stroke:none;}
.gdlab .trail{fill:none;stroke:var(--color-gold);stroke-width:1.5;stroke-dasharray:3 3;opacity:.7;}
.gdlab .trail-dot{fill:var(--color-gold);opacity:.6;}
.gdlab .ball{fill:var(--color-gold);stroke:#fff;stroke-width:2;}
.gdlab .tangent{stroke:#b5524a;stroke-width:2;stroke-linecap:round;}
.gdlab .minmark{fill:none;stroke:var(--color-forest);stroke-width:1.4;stroke-dasharray:3 2;}
.gdlab .axis{stroke:var(--color-border);stroke-width:1;}
.gdlab svg{cursor:crosshair;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 梯度下降下山

训练模型，本质上就是在一座“误差山”上找最低点。办法很朴素：站在哪儿，就看脚下哪个方向最陡、往下走一步，反复如此——这就是“梯度下降”。但步子（学习率）多大很关键：太小磨蹭，太大会一脚迈过头冲出去；有时还会卡在一个“看起来最低、其实不是”的小坑里。点曲线任意位置放小球，调步子试试。

<section class="vizui gdlab" id="gdlab">
  <p class="vizui__lead">金球沿曲线往低处滚，红色短线是它脚下的“坡度”。<b>在曲线上点一下</b>可以换个起点；调“学习率”看步子大小的影响。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="vizui-field"><label for="lr">学习率（步子）</label>
        <input type="range" id="lr" min="0.05" max="1.4" step="0.05" value="0.25" style="width:180px">
        <output id="lrVal">0.25</output>
      </span>
      <span class="vizui-spacer"></span>
      <button class="vizui-btn vizui-btn--go" id="go" type="button">▶ 开始下山</button>
      <button class="vizui-btn" id="step" type="button">单步</button>
      <button class="vizui-btn" id="reset" type="button">重置</button>
    </div>
  </div>

  <div class="vizui-panel">
    <div class="vizui-legend">
      <span><i class="dot" style="background:var(--color-gold)"></i>当前位置</span>
      <span><i style="background:#b5524a"></i>脚下坡度</span>
      <span><i style="background:var(--color-accent)"></i>误差曲线</span>
      <span class="vizui-spacer"></span><span id="stepLbl" class="vizui-pill">第 0 步</span>
    </div>
    <svg class="vizui-chart" id="surf" viewBox="0 0 480 270" role="img" aria-label="一维损失曲线与下降过程"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-text-muted)"><b>步子太小</b><p>每步只挪一点点，方向没错，但要走很多步才到底，训练很慢。</p></div>
    <div class="card" style="--wc:#b5524a"><b>步子太大</b><p>一脚跨过最低点，在谷底两侧来回弹、难以稳定落底；有时甚至直接跳进旁边的谷。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>局部最低点</b><p>球可能停在一个小坑里，四周都是上坡，却不是真正最低的谷。换起点、或把步子调大一脚跨出去，才可能到全局谷底。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
/* 误差曲线：一个不对称的“双谷”，左边是局部最低、右边是全局最低 */
function f(x){return 0.10*x*x*x*x - 0.35*x*x - 0.10*x + 0.62;}
function fp(x){return 0.40*x*x*x - 0.70*x - 0.10;}
var XMIN=-2.35, XMAX=2.35, YMIN=0, YMAX=1.7;
var lr=0.25, x=-2.0, trail=[], step=0, playing=false, timer=null, done=false, diverged=false;

function reset(x0){x=x0;trail=[x];step=0;done=false;diverged=false;}

function stepOnce(){
  if(done||diverged)return;
  var g=fp(x); x=x-lr*g; step++;
  if(x<XMIN-0.3||x>XMAX+0.3){diverged=true;return;}
  trail.push(x);
  if(Math.abs(fp(x))<0.012)done=true;
}

var SVGNS="http://www.w3.org/2000/svg", W=480,H=270,pad=24;
function wx(xx){return pad+(xx-XMIN)/(XMAX-XMIN)*(W-2*pad);}
function wy(yy){return (H-pad)-(yy-YMIN)/(YMAX-YMIN)*(H-2*pad);}
function E(p,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e;}

function draw(){
  var svg=document.getElementById("surf"); while(svg.firstChild)svg.removeChild(svg.firstChild);
  // 曲线 + 填充地面
  var cp=[],gp=[wx(XMIN)+","+wy(YMIN)];
  for(var i=0;i<=120;i++){var xx=XMIN+(XMAX-XMIN)*i/120;cp.push(wx(xx)+","+wy(f(xx)));gp.push(wx(xx)+","+wy(f(xx)));}
  gp.push(wx(XMAX)+","+wy(YMIN));
  E(svg,"polygon",{points:gp.join(" "),"class":"ground"});
  E(svg,"polyline",{points:cp.join(" "),"class":"curve"});
  // 两个最低点参考
  [-1.27,1.34].forEach(function(m){E(svg,"line",{x1:wx(m),y1:wy(f(m)),x2:wx(m),y2:wy(YMIN),"class":"minmark"});});
  // 轨迹
  if(trail.length>1){var tp=trail.map(function(t){return wx(t)+","+wy(f(t));});E(svg,"polyline",{points:tp.join(" "),"class":"trail"});
    trail.forEach(function(t){E(svg,"circle",{cx:wx(t),cy:wy(f(t)),r:2.4,"class":"trail-dot"});});}
  // 脚下坡度（切线）
  if(!diverged){var g=fp(x),dx=0.5;
    E(svg,"line",{x1:wx(x-dx),y1:wy(f(x)-g*dx),x2:wx(x+dx),y2:wy(f(x)+g*dx),"class":"tangent"});
    E(svg,"circle",{cx:wx(x),cy:wy(f(x)),r:7,"class":"ball"});}
  document.getElementById("stepLbl").textContent="第 "+step+" 步";
}
function caption(){
  var el=document.getElementById("caption");
  if(diverged){el.innerHTML="<b>球被甩出了显示范围！</b>学习率 "+lr.toFixed(2)+" 的步子实在太大了。把学习率调小再试。";return;}
  if(step===0){el.innerHTML="点“开始下山”。球会沿着脚下的坡度一步步往低处走。试试在曲线左、右不同位置放球，看它分别滚进哪个谷。";return;}
  if(done){
    if(x<0)el.innerHTML="球停在了<b>左边的小谷</b>——四周都是上坡，但右边其实还有更低的谷，这就是“局部最低点”陷阱。试试在曲线右半边点一下放球，或把学习率调大让它一脚跨过去。";
    else el.innerHTML="球滚到了<b>右边的谷</b>，这里是整条曲线的<b>全局最低点</b>。漂亮，下山成功！";
    return;
  }
  el.innerHTML="第 "+step+" 步：球在往下滚，脚下坡度 "+fp(x).toFixed(2)+"（越陡走得越快）。";
}
function render(){draw();caption();}

function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("go").textContent="▶ 开始下山";}
function play(){
  if(done||diverged){reset(x>0?1.9:-2.0);}
  stop();playing=true;document.getElementById("go").textContent="⏸ 暂停";
  timer=setInterval(function(){stepOnce();render();if(done||diverged||step>=120)stop();},260);
}
document.getElementById("lr").addEventListener("input",function(e){lr=+e.target.value;document.getElementById("lrVal").textContent=lr.toFixed(2);stop();reset(trail[0]);render();});
document.getElementById("go").addEventListener("click",function(){playing?stop():play();});
document.getElementById("step").addEventListener("click",function(){stop();stepOnce();render();});
document.getElementById("reset").addEventListener("click",function(){stop();reset(trail[0]);render();});
document.getElementById("surf").addEventListener("click",function(e){
  stop();var svg=e.currentTarget,r=svg.getBoundingClientRect();
  var sx=(e.clientX-r.left)/r.width*W;                 /* 屏幕→viewBox */
  var xx=XMIN+(sx-pad)/(W-2*pad)*(XMAX-XMIN);
  reset(Math.max(XMIN,Math.min(XMAX,xx)));render();
});

/* 启动 + 自动演示 */
reset(-2.0);render();
setTimeout(function(){
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){for(var i=0;i<40&&!done&&!diverged;i++)stepOnce();render();return;}
  play();
},900);
})();
</script>
{% endraw %}
