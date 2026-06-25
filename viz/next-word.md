---
layout: default
title: 下一词预测
description: "用 bigram 语言模型按概率接词成句，看“按概率接龙”为什么会跑题、重复。"
permalink: /viz/next-word/
redirect_from:
  - /v/next-word/
---

{% raw %}
<style>
.nwlab .sent{font-family:var(--font-serif);font-size:1.3rem;line-height:1.9;min-height:2.2em;padding:14px 16px;background:var(--color-bg-section);border-radius:var(--radius-md);}
.nwlab .sent .w{margin-right:2px;}
.nwlab .sent .cur{color:var(--color-accent);font-weight:700;border-bottom:2px solid var(--color-accent);}
.nwlab .cands .row{display:grid;grid-template-columns:64px 1fr 44px;align-items:center;gap:8px;margin:7px 0;cursor:pointer;}
.nwlab .cands .row:hover .nm{color:var(--color-accent);}
.nwlab .cands .nm{font-family:var(--font-serif);font-size:1.05rem;text-align:right;}
.nwlab .cands .bar{height:16px;border-radius:8px;background:var(--color-bg-section);overflow:hidden;}
.nwlab .cands .bar i{display:block;height:100%;border-radius:8px;background:var(--color-accent);transition:width .3s var(--ease-out);}
.nwlab .cands .pct{font:600 .85rem var(--font-mono);color:var(--color-text-soft);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 下一词预测

大模型写字，归根到底是在反复做一件事：**根据已经写出的词，预测下一个词最可能是什么，然后接上去**。这里用一个最简单的“二元（bigram）”语言模型演示——它只看前一个词，从读过的小语料里统计出下一个词的概率分布。点候选词手动接，或让它自动续写。你会发现：模型只是在“按概率接龙”，语料一小，就容易跑题、重复、说车轱辘话。

<section class="vizui nwlab" id="nwlab">
  <p class="vizui__lead">下面这句是模型正在写的话，最后一个高亮词是当前的“上文”。右边是模型预测的下一个词及其概率（从一小段语料里统计来的）。点候选词接上，或让它自己写。</p>

  <div class="vizui-grid2">
    <div class="vizui-panel">
      <p class="vizui-panel__title">正在生成</p>
      <div class="sent" id="sent"></div>
      <div class="vizui-bar" style="margin-top:12px">
        <button class="vizui-btn vizui-btn--go" id="auto" type="button">▶ 自动续写</button>
        <button class="vizui-btn" id="step" type="button">续写一词</button>
        <button class="vizui-btn" id="reset" type="button">重新开始</button>
      </div>
    </div>
    <div class="vizui-panel">
      <p class="vizui-panel__title">下一个词的概率（点选可接上）</p>
      <div class="cands" id="cands"></div>
    </div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>只是接龙</b><p>每一步都在“给定上文，下一个词的概率”里挑一个——没有计划，全靠统计。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>只看前一个词</b><p>bigram 的“记忆”只有一个词，所以容易跑题、绕圈。真实大模型看的上文长得多。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>语料决定一切</b><p>它只会说语料里见过的搭配；语料越大越多样，说得越通顺。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var S="⟨开始⟩", E="⟨结束⟩";
var CORPUS=[
  ["小猫","喜欢","吃","鱼"],["小猫","喜欢","睡觉"],["小狗","喜欢","吃","骨头"],
  ["小狗","喜欢","玩","球"],["今天","天气","很","好"],["今天","天气","很","冷"],
  ["我","喜欢","小猫"],["我","喜欢","今天","的","天气"],["鱼","很","好吃"],
  ["小猫","和","小狗","都","喜欢","玩"],["天气","好","我","很","开心"],["小猫","很","可爱"]
];
var BG={};
CORPUS.forEach(function(s){var seq=[S].concat(s,[E]);
  for(var i=0;i<seq.length-1;i++){var a=seq[i],b=seq[i+1];(BG[a]=BG[a]||{});BG[a][b]=(BG[a][b]||0)+1;}});
function dist(w){var m=BG[w]||{},tot=0,arr=[];for(var k in m)tot+=m[k];for(var k2 in m)arr.push([k2,m[k2]/tot]);arr.sort(function(a,b){return b[1]-a[1];});return arr;}
var sent=[], cur=S, playing=false, timer=null;

function renderSent(){
  var host=document.getElementById("sent");host.innerHTML="";
  sent.forEach(function(w,i){var sp=document.createElement("span");sp.className="w"+(i===sent.length-1?" cur":"");sp.textContent=w;host.appendChild(sp);});
  if(!sent.length){var ph=document.createElement("span");ph.style.color="var(--color-text-muted)";ph.textContent="（点“重新开始”或“自动续写”）";host.appendChild(ph);}
}
function renderCands(){
  var host=document.getElementById("cands");host.innerHTML="";
  var d=dist(cur);
  if(!d.length||cur===E){host.innerHTML='<p style="color:var(--color-text-muted);font-size:.9rem">已到句末 ⟨结束⟩。点“重新开始”。</p>';return;}
  var max=d[0][1];
  d.slice(0,7).forEach(function(it){
    var row=document.createElement("div");row.className="row";
    var label=it[0]===E?"⟨结束⟩":it[0];
    row.innerHTML='<span class="nm">'+label+'</span><div class="bar"><i style="width:'+(it[1]/max*100).toFixed(0)+'%"></i></div><span class="pct">'+(it[1]*100).toFixed(0)+'%</span>';
    row.addEventListener("click",function(){pick(it[0]);});
    host.appendChild(row);
  });
}
function pick(w){if(w===E){cur=E;}else{sent.push(w);cur=w;}render();}
function sample(){var d=dist(cur);if(!d.length)return E;var r=Math.random(),acc=0;for(var i=0;i<d.length;i++){acc+=d[i][1];if(r<=acc)return d[i][0];}return d[d.length-1][0];}
function stepGen(){if(cur===E)return;var w=sample();pick(w);}
function render(){renderSent();renderCands();caption();}
function caption(){
  var el=document.getElementById("caption");
  if(cur===E)el.innerHTML="写到了 <b>⟨结束⟩</b>。整句话每个词都只是根据前一个词的概率接出来的——读着像那么回事，其实没有任何“想法”。";
  else if(sent.length<2)el.innerHTML="从 <b>⟨开始⟩</b> 出发，模型先挑一个开头词，再一个接一个。注意每次它只盯着上一个词做决定。";
  else el.innerHTML="当前上文是 <b>"+cur+"</b>，模型据此给出下一个词的概率。挑概率高的更通顺、挑低的更出格——这正是“温度”在调的事（见 温度采样 那页）。";
}
function stop(){playing=false;if(timer){clearInterval(timer);timer=null;}document.getElementById("auto").textContent="▶ 自动续写";}
function startGen(){if(cur===E||!sent.length){sent=[];cur=S;}stop();playing=true;document.getElementById("auto").textContent="⏸ 暂停";
  timer=setInterval(function(){stepGen();render();if(cur===E||sent.length>=12)stop();},650);}
document.getElementById("auto").addEventListener("click",function(){playing?stop():startGen();});
document.getElementById("step").addEventListener("click",function(){stop();if(cur===E||!sent.length){sent=[];cur=S;}stepGen();render();});
document.getElementById("reset").addEventListener("click",function(){stop();sent=[];cur=S;render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){sent=["小猫","喜欢","吃","鱼"];cur=E;render();return;}startGen();},1000);
})();
</script>
{% endraw %}
