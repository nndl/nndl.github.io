---
layout: default
title: Dropout
description: "训练时随机关掉一部分神经元，逼网络学冗余表示、防过拟合；测试时再全开。"
permalink: /viz/dropout/
redirect_from:
  - /v/dropout/
---

{% raw %}
<style>
.dolab .edge{stroke:var(--color-border-strong);stroke-width:1;opacity:.5;transition:opacity .25s;}
.dolab .edge.off{opacity:.06;}
.dolab .node{stroke:#fff;stroke-width:1.5;transition:fill .25s,r .25s;}
.dolab .node.on{fill:var(--color-accent);}
.dolab .node.io{fill:var(--color-forest);}
.dolab .node.off{fill:#c8d0ce;}
.dolab .llab{font:11px var(--font-sans);fill:var(--color-text-muted);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# Dropout

防过拟合有个反直觉却极有效的招：训练时**每一步都随机“关掉”一部分神经元**（让它们的输出暂时变 0）。这样网络就不能死记硬背、也不能过度依赖某几个神经元——它被迫学会用各种残缺的子网络也能把活干好，相当于同时训练了海量个略有不同的小网络。到了测试时再把所有神经元打开，效果就像这些子网络的“集体投票”，更稳、更不容易过拟合。点“换一批”，看每次关掉的是不同的神经元。

<section class="dolab vizui" id="dolab">
  <p class="vizui__lead">绿色是输入/输出层，蓝色是隐藏神经元。训练时每步随机把一些隐藏神经元变灰（关掉），它们的连线也跟着断开。每一批都是一张不同的“残缺网络”。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <span class="heads" id="mode" style="display:inline-flex;gap:4px;padding:4px;background:var(--color-bg-section);border:1px solid var(--color-border);border-radius:999px">
        <button data-m="train" class="on" type="button" style="appearance:none;border:0;background:var(--color-bg-pure);cursor:pointer;font:inherit;font-size:.86rem;padding:6px 14px;border-radius:999px;color:var(--color-accent);font-weight:600;box-shadow:var(--shadow-sm)">训练（开 Dropout）</button>
        <button data-m="test" type="button" style="appearance:none;border:0;background:transparent;cursor:pointer;font:inherit;font-size:.86rem;padding:6px 14px;border-radius:999px;color:var(--color-text-soft)">测试（全开）</button>
      </span>
      <span class="vizui-field"><label for="p">丢弃率</label><input type="range" id="p" min="0" max="0.7" step="0.05" value="0.4" style="width:120px"><output id="pVal">0.40</output></span>
      <span class="vizui-spacer"></span>
      <button class="vizui-btn vizui-btn--go" id="go" type="button">▶ 不停换</button>
      <button class="vizui-btn" id="step" type="button">换一批</button>
    </div>
    <svg class="vizui-chart" id="net" viewBox="0 0 420 260" role="img" aria-label="带 Dropout 的网络"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>逼出冗余</b><p>随时可能被关掉，神经元就不能互相过度依赖，每个都得学到有用的东西。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>像训练一群网络</b><p>每批是一张不同的子网络，等于同时训练指数级多个网络并共享参数。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>测试时全开</b><p>预测时打开全部神经元（输出按比例缩放），相当于子网络们的平均投票。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var LAYERS=[4,6,6,2], p=0.4, mode="train", playing=false, timer=null, mask=[];
function newMask(){mask=LAYERS.map(function(c,li){return Array.from({length:c},function(){return (mode==="test"||li===0||li===LAYERS.length-1)?true:Math.random()>=p;});});}
var SVGNS="http://www.w3.org/2000/svg",W=420,H=260,pad=30;
function E(p2,t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);p2.appendChild(e);return e;}
function pos(li,ni){var x=pad+li/(LAYERS.length-1)*(W-2*pad);var c=LAYERS[li];var y=H/2+(ni-(c-1)/2)*(H-2*pad)/Math.max(5,c);return [x,y];}
function draw(){
  var svg=document.getElementById("net");while(svg.firstChild)svg.removeChild(svg.firstChild);
  for(var li=0;li<LAYERS.length-1;li++)for(var a=0;a<LAYERS[li];a++)for(var b=0;b<LAYERS[li+1];b++){
    var pa=pos(li,a),pb=pos(li+1,b),on=mask[li][a]&&mask[li+1][b];
    E(svg,"line",{x1:pa[0],y1:pa[1],x2:pb[0],y2:pb[1],"class":"edge"+(on?"":" off")});}
  for(var li2=0;li2<LAYERS.length;li2++)for(var ni=0;ni<LAYERS[li2];ni++){var pp=pos(li2,ni),io=(li2===0||li2===LAYERS.length-1),on=mask[li2][ni];
    E(svg,"circle",{cx:pp[0],cy:pp[1],r:on?9:6,"class":"node "+(io?"io":(on?"on":"off"))});}
  ["输入","隐藏","隐藏","输出"].forEach(function(t,li){E(svg,"text",{x:pos(li,0)[0],y:H-6,"text-anchor":"middle","class":"llab"}).textContent=t;});
}
function dropped(){var d=0,tot=0;mask.forEach(function(row,li){if(li>0&&li<LAYERS.length-1)row.forEach(function(v){tot++;if(!v)d++;});});return {d:d,tot:tot};}
function render(){document.getElementById("pVal").textContent=p.toFixed(2);draw();caption();}
function caption(){
  var el=document.getElementById("caption"),dd=dropped();
  if(mode==="test")el.innerHTML="<b>测试模式：</b>所有神经元全部打开，不再随机丢弃——用的是训练出的“群体智慧”。这才是模型真正做预测时的样子。";
  else el.innerHTML="<b>训练模式：</b>这一批随机关掉了 <b>"+dd.d+"/"+dd.tot+"</b> 个隐藏神经元（丢弃率 "+p.toFixed(2)+"），网络只能用剩下的完成任务。点“换一批”，每次关掉的都不一样——网络因此学得更鲁棒。";
}
function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("go").textContent="▶ 不停换";}
function play(){stop();playing=true;document.getElementById("go").textContent="⏸ 暂停";timer=setInterval(function(){newMask();render();},650);}
document.getElementById("mode").addEventListener("click",function(e){var b=e.target.closest("button");if(!b)return;mode=b.dataset.m;
  document.querySelectorAll("#mode button").forEach(function(x){var on=x.dataset.m===mode;x.style.background=on?"var(--color-bg-pure)":"transparent";x.style.color=on?"var(--color-accent)":"var(--color-text-soft)";x.style.fontWeight=on?"600":"400";x.style.boxShadow=on?"var(--shadow-sm)":"none";});
  if(mode==="test")stop();newMask();render();});
document.getElementById("p").addEventListener("input",function(e){p=+e.target.value;newMask();render();});
document.getElementById("go").addEventListener("click",function(){playing?stop():play();});
document.getElementById("step").addEventListener("click",function(){stop();newMask();render();});
newMask();render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;play();},1000);
})();
</script>
{% endraw %}
