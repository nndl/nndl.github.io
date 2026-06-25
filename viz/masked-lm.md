---
layout: default
title: 掩码语言模型（双向）
description: "盖住一个词让模型双向猜（BERT），对照只看左的因果模型——双向理解为何更全面。"
permalink: /viz/masked-lm/
redirect_from:
  - /v/masked-lm/
---

{% raw %}
<style>
.mlmlab svg{max-width:100%;height:auto;}
.mlmlab .tok{fill:var(--color-bg-soft,#f0ece4);stroke:var(--color-border-strong);stroke-width:1;}
.mlmlab .tok.mask{fill:#fbeec2;stroke:var(--color-gold);stroke-width:2;}
.mlmlab .tok.seen{fill:#dceaf5;}
.mlmlab .ttext{font:14px var(--font-sans);fill:#1a1a1a;}
.mlmlab .arc{fill:none;stroke:var(--color-accent);stroke-width:2;opacity:.7;}
.mlmlab .pbar{fill:var(--color-accent);}
.mlmlab .lbl{font:12px var(--font-sans);fill:#333;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 掩码语言模型（双向）

GPT 这类模型从左到右写字，预测下一个词时**只能看左边**（因果）。但还有另一种训练法：把句子里的某个词盖住，让模型**同时看左右两边**来猜它——这就是 BERT 用的**掩码语言模型（MLM）**。能看双向，理解就更全面：要填“坐在 ▢ 上 晒太阳”，右边的“上 晒太阳”是关键线索，只看左边的模型用不上。切换“双向 / 只看左”，看被盖住的词能借到哪些上下文、预测有多确定。

<section class="vizui mlmlab" id="mlmlab">
  <p class="vizui__lead">金色是被盖住的词 <b>[MASK]</b>，蓝色是模型能看到的上下文，蓝色弧线表示“注意力借用”。下面是模型对被盖词的预测——看看双向比只看左，确定多少。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <button class="vizui-btn vizui-btn--go" id="bi" type="button">双向（MLM / BERT）</button>
      <button class="vizui-btn" id="ca" type="button">只看左（因果 / GPT）</button>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stat">—</span>
    </div>
    <svg id="plane" viewBox="0 0 480 280" role="img" aria-label="掩码语言模型"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-gold)"><b>盖词填空</b><p>随机盖住 15% 的词让模型猜，这是 BERT 的核心预训练任务。</p></div>
    <div class="card" style="--wc:var(--color-accent)"><b>双向理解</b><p>左右上下文一起看，对句意理解更充分，适合分类、抽取等理解类任务。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>vs 因果生成</b><p>只看左的因果模型擅长“接着写”；双向的擅长“读懂”，两条路线各有所长。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var toks=["小猫","坐在","[MASK]","上","晒太阳"],MASK=2,mode="bi";
var predBi=[["窗台",0.42],["沙发",0.31],["椅子",0.18],["地毯",0.09]];
var predCa=[["地上",0.23],["那",0.19],["它",0.16],["一",0.13],["树",0.11],["…",0.18]];
var SVGNS="http://www.w3.org/2000/svg",W=480,H=280,bw=78,bh=34,gap=12,rowY=64;
var x0=(W-(toks.length*(bw+gap)-gap))/2;
function tx(i){return x0+i*(bw+gap);}
function E(p,t,a,txt){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;p.appendChild(e);return e;}
function render(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var seen=[];for(var i=0;i<toks.length;i++){if(i===MASK)continue;if(mode==="ca"&&i>MASK)continue;seen.push(i);}
  // 弧线：从 MASK 顶部连到每个可见 token 顶部
  seen.forEach(function(j){
    var x1=tx(MASK)+bw/2,x2=tx(j)+bw/2,top=rowY,h=28+Math.abs(j-MASK)*16;
    E(svg,"path",{d:"M "+x1+" "+top+" Q "+((x1+x2)/2)+" "+(top-h)+" "+x2+" "+top,"class":"arc"});
  });
  for(var i2=0;i2<toks.length;i2++){
    var seenIt=seen.indexOf(i2)>=0,cls="tok"+(i2===MASK?" mask":(seenIt?" seen":""));
    E(svg,"rect",{x:tx(i2),y:rowY,width:bw,height:bh,rx:5,"class":cls});
    E(svg,"text",{x:tx(i2)+bw/2,y:rowY+bh/2+5,"text-anchor":"middle","class":"ttext"},toks[i2]);
  }
  // 预测条
  var pred=mode==="bi"?predBi:predCa;
  E(svg,"text",{x:x0,y:rowY+72,"class":"lbl"},"对 [MASK] 的预测：");
  for(var k=0;k<pred.length;k++){
    var py=rowY+86+k*22;
    E(svg,"text",{x:x0+54,y:py+11,"text-anchor":"end","class":"ttext"},pred[k][0]);
    E(svg,"rect",{x:x0+62,y:py,width:pred[k][1]*300,height:15,rx:2,"class":"pbar",opacity:(0.4+0.6*pred[k][1]).toFixed(2)});
    E(svg,"text",{x:x0+68+pred[k][1]*300,y:py+12,"class":"lbl"},(pred[k][1]*100).toFixed(0)+"%");
  }
  document.getElementById("bi").className="vizui-btn"+(mode==="bi"?" vizui-btn--go":"");
  document.getElementById("ca").className="vizui-btn"+(mode==="ca"?" vizui-btn--go":"");
  document.getElementById("stat").textContent=mode==="bi"?"能看到 4 个词（左+右）":"只能看到 2 个词（左）";
  caption();
}
function caption(){
  var el=document.getElementById("caption");
  if(mode==="bi")el.innerHTML="<b>双向：</b>[MASK] 借用了左右全部 4 个词，尤其右边的“上 晒太阳”几乎锁定了答案——预测高度集中在“窗台”（42%）。这就是 BERT 读得准的原因。";
  else el.innerHTML="<b>只看左：</b>[MASK] 只看得到“小猫 坐在”，没有右边的关键线索，预测分散、谁也不占绝对优势——这正是单向模型在“填空理解”上的短板。";
}
document.getElementById("bi").addEventListener("click",function(){mode="bi";render();});
document.getElementById("ca").addEventListener("click",function(){mode="ca";render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  setTimeout(function(){mode="ca";render();setTimeout(function(){mode="bi";render();},1700);},1300);},1000);
})();
</script>
{% endraw %}
