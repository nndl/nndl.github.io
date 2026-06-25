---
layout: default
title: 因果掩码
description: "给注意力盖上因果掩码，每个词只能看自己和左边，保证自回归生成不偷看答案。"
permalink: /viz/causal-mask/
redirect_from:
  - /v/causal-mask/
---

{% raw %}
<style>
.cmlab .hm{display:grid;gap:3px;max-width:430px;margin:0 auto;}
.cmlab .hm .lab{font:12px var(--font-sans);color:var(--color-text-muted);display:flex;align-items:center;justify-content:center;}
.cmlab .hm .cell{aspect-ratio:1;border-radius:3px;display:flex;align-items:center;justify-content:center;font:600 11px var(--font-mono);transition:background .25s;}
.cmlab .hm .cell.blocked{background:repeating-linear-gradient(45deg,#eceff1,#eceff1 4px,#e0e4e6 4px,#e0e4e6 8px);color:#aab4b2;}
.cmlab .hm .row-q{box-shadow:inset 0 0 0 2px var(--color-accent);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 因果掩码

大模型是“自回归”生成的：从左往右，一个词一个词地往外蹦，每写一个都要预测“下一个最可能是什么”。但训练时整句话都摆在那儿——怎么保证模型预测某个位置时**不偷看后面的答案**？办法就是给注意力盖一张“因果掩码”：每个词只允许关注自己和它**左边**的词，右边（未来）的全部屏蔽。看看盖上和不盖的差别。

<section class="cmlab vizui" id="cmlab">
  <p class="vizui__lead"><b>行 = 哪个词在看，列 = 它能看谁。</b>打叉的斜纹格表示被掩码挡住（未来的词，不许看）。点某一行，看那个位置实际能注意到哪些词。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <label style="display:inline-flex;align-items:center;gap:8px;cursor:pointer"><input type="checkbox" id="mask" checked> 盖上因果掩码</label>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="sel">点一行试试</span>
    </div>
    <div class="hm" id="hm"></div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>只能看左边</b><p>对角线及左下方允许，右上方（未来词）全部屏蔽，保证“预测下一个”时不偷看答案。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>能并行训练</b><p>一句话所有位置可以同时算各自的预测，又互不偷看——训练飞快，这是 GPT 类模型的关键。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>编码器不掩码</b><p>像 BERT 那样要“读懂整句”的编码器则不加掩码，每个词能看到全部上下文。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var TOK=["我","喜欢","吃","苹果","和","梨"], N=TOK.length, masked=true, sel=-1;
/* 一套示意注意力打分（未归一化） */
var SCORE=[];for(var i=0;i<N;i++){var r=[];for(var j=0;j<N;j++)r.push(0.5+Math.exp(-(i-j)*(i-j)/2.2)+(j===0?0.3:0));SCORE.push(r);}
function rowWeights(i){var allow=[],sum=0;for(var j=0;j<N;j++){var ok=!masked||j<=i;allow.push(ok);if(ok)sum+=SCORE[i][j];}
  return SCORE[i].map(function(s,j){return allow[j]?s/sum:null;});}
function mix(w){var lo=[239,242,240],hi=[21,94,117];return "rgb("+Math.round(lo[0]+(hi[0]-lo[0])*w)+","+Math.round(lo[1]+(hi[1]-lo[1])*w)+","+Math.round(lo[2]+(hi[2]-lo[2])*w)+")";}
function build(){
  var hm=document.getElementById("hm");hm.innerHTML="";hm.style.gridTemplateColumns="40px repeat("+N+",1fr)";
  hm.appendChild(C("",""));TOK.forEach(function(t){hm.appendChild(C(t,"lab"));});
  for(var i=0;i<N;i++){
    hm.appendChild(C(TOK[i],"lab"));
    for(var j=0;j<N;j++){(function(i,j){
      var w=rowWeights(i)[j],c=document.createElement("div");
      if(w===null){c.className="cell blocked";c.textContent="✕";}
      else{c.className="cell";c.style.background=mix(w);c.style.color=w>0.5?"#fff":"#8a97a0";c.textContent=Math.round(w*100);}
      if(i===sel)c.classList.add("row-q");
      c.addEventListener("click",function(){sel=i;render();});
      hm.appendChild(c);
    })(i,j);}
  }
}
function render(){build();caption();document.getElementById("sel").textContent=sel<0?"点一行试试":"“"+TOK[sel]+"”能看到 "+(masked?(sel+1):N)+" 个词";}
function caption(){
  var el=document.getElementById("caption");
  if(masked)el.innerHTML="<b>盖上掩码：</b>右上方未来的词全被挡住，每个词只能注意自己和左边。"+(sel>=0?"第 "+(sel+1)+" 个词“"+TOK[sel]+"”只看得到前 "+(sel+1)+" 个词——所以它在“预测下一个”时绝不会偷看答案。":"这正是 GPT 一类模型从左到右生成的保证。");
  else el.innerHTML="<b>去掉掩码：</b>每个词都能看到整句（包括右边）。这适合“读懂整句”的任务（如 BERT），但不能用来从左往右生成——因为预测时会看到答案。";
}
document.getElementById("mask").addEventListener("change",function(e){masked=e.target.checked;render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  var k=0;var iv=setInterval(function(){sel=k;render();k++;if(k>=N)clearInterval(iv);},700);},1000);
function C(txt,cls){var d=document.createElement("div");if(cls)d.className=cls;d.textContent=txt;return d;}
})();
</script>
{% endraw %}
