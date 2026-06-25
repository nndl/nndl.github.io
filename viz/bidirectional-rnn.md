---
layout: default
title: 双向 RNN
description: "“我买了苹果手机”——点词看单向只能看左边，双向再跑一个反向 RNN 补上右文，“苹果”才从水果变品牌。"
permalink: /viz/bidirectional-rnn/
redirect_from:
  - /v/bidirectional-rnn/
---

{% raw %}
<style>
.birlab svg{max-width:100%;height:auto;}
.birlab .tok{fill:var(--color-bg-soft,#f0ece4);stroke:#9aa3a8;stroke-width:1;cursor:pointer;}
.birlab .tok.sel{fill:#fbeec2;stroke:var(--color-gold);stroke-width:2.5;}
.birlab .tok.fwd{fill:#dceaf5;}
.birlab .tok.bwd{fill:#fbe6da;}
.birlab .ttext{font:14px var(--font-sans);fill:#1a1a1a;pointer-events:none;}
.birlab .lbl{font:11px var(--font-sans);fill:var(--color-text-muted);}
.birlab .pbar{fill:var(--color-accent);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 双向 RNN

普通 RNN 从左到右读，每个位置只看得到**它和它左边**的内容。可很多时候，一个词的含义要靠**右边**才能定——“我买了苹果手机”，光看“我买了苹果”还以为是水果，读到“手机”才知道是品牌。**双向 RNN** 的办法很直接：跑两个 RNN，一个从左往右、一个从右往左，再把两者在每个位置的隐状态拼起来。这样每个位置就同时拥有**左右全部上下文**，特别适合需要“读懂整句”的理解类任务。点句子里任一个词，看它在单向和双向下分别能看到哪些上下文。

<section class="vizui birlab" id="birlab">
  <p class="vizui__lead">点选一个词。<span style="color:#2563eb">蓝色</span>是前向 RNN 看到的（它+左边），<span style="color:#c06a3a">橙色</span>是后向 RNN 看到的（它+右边）。双向＝两者相加＝整句。下面是对“苹果”一词的理解。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <button class="vizui-btn" id="uni" type="button">单向（只前向）</button>
      <button class="vizui-btn vizui-btn--go" id="bi" type="button">双向</button>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stat">—</span>
    </div>
    <svg id="plane" viewBox="0 0 480 220" role="img" aria-label="双向 RNN"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent-light,#2563eb)"><b>前向看左</b><p>从句首读到当前位置，隐状态汇总了左边的上下文。</p></div>
    <div class="card" style="--wc:#c06a3a"><b>后向看右</b><p>从句尾倒着读到当前位置，补上右边的上下文。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>拼起来=全局</b><p>两个方向的隐状态一拼，每个位置都拥有整句信息——理解任务更准。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var toks=["我","买","了","苹果","手机"],N=toks.length,sel=3,mode="bi";
var SVGNS="http://www.w3.org/2000/svg",bw=66,gap=12,y=70,x0=(480-(N*(bw+gap)-gap))/2;
function tx(i){return x0+i*(bw+gap);}
function E(p,t,a,txt){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;p.appendChild(e);return e;}
function render(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  for(var i=0;i<N-1;i++){E(svg,"line",{x1:tx(i)+bw,y1:y-8,x2:tx(i+1),y2:y-8,stroke:"#2563eb","stroke-width":2,opacity:0.6});}
  if(mode==="bi")for(var i2=0;i2<N-1;i2++){E(svg,"line",{x1:tx(i2+1),y1:y+38,x2:tx(i2)+bw,y2:y+38,stroke:"#c06a3a","stroke-width":2,opacity:0.6});}
  E(svg,"text",{x:x0,y:y-16,"class":"lbl",style:"fill:#2563eb"},"前向 →");
  if(mode==="bi")E(svg,"text",{x:x0,y:y+54,"class":"lbl",style:"fill:#c06a3a"},"← 后向");
  for(var i3=0;i3<N;i3++){
    var cls="tok";
    if(i3===sel)cls="tok sel";
    else if(i3<sel)cls="tok fwd";
    else if(i3>sel&&mode==="bi")cls="tok bwd";
    E(svg,"rect",{x:tx(i3),y:y,width:bw,height:30,rx:5,"class":cls,"data-i":i3});
    E(svg,"text",{x:tx(i3)+bw/2,y:y+20,"text-anchor":"middle","class":"ttext"},toks[i3]);
  }
  var rightCnt=mode==="bi"?(N-1-sel):0, leftCnt=sel;
  if(sel===3){ var pFruit,pBrand; if(mode==="bi"){pFruit=0.15;pBrand=0.85;} else {pFruit=0.6;pBrand=0.4;}
    E(svg,"text",{x:x0,y:140,"class":"lbl"},"“苹果”被理解为：");
    E(svg,"text",{x:x0+56,y:158,"text-anchor":"end","class":"ttext"},"水果");E(svg,"rect",{x:x0+62,y:147,width:pFruit*260,height:14,rx:2,"class":"pbar",opacity:0.6});E(svg,"text",{x:x0+68+pFruit*260,y:158,"class":"lbl"},(pFruit*100).toFixed(0)+"%");
    E(svg,"text",{x:x0+56,y:180,"text-anchor":"end","class":"ttext"},"品牌");E(svg,"rect",{x:x0+62,y:169,width:pBrand*260,height:14,rx:2,"class":"pbar"});E(svg,"text",{x:x0+68+pBrand*260,y:180,"class":"lbl"},(pBrand*100).toFixed(0)+"%");
  }
  document.getElementById("uni").className="vizui-btn"+(mode==="uni"?" vizui-btn--go":"");
  document.getElementById("bi").className="vizui-btn"+(mode==="bi"?" vizui-btn--go":"");
  document.getElementById("stat").textContent=mode==="bi"?("看到左 "+leftCnt+" + 右 "+rightCnt+" = 整句"):("只看到左边 "+leftCnt+" 个");
  [].slice.call(svg.querySelectorAll(".tok")).forEach(function(rc){rc.addEventListener("click",function(){sel=+rc.getAttribute("data-i");render();});});
  caption();
}
function caption(){
  var el=document.getElementById("caption");
  if(sel===3){
    if(mode==="uni")el.innerHTML="<b>单向：</b>读到“苹果”时只看过“我买了苹果”，右边的“手机”还没读到——所以它更像在说<b>水果</b>（60%），其实判断错了。";
    else el.innerHTML="<b>双向：</b>后向 RNN 把右边的“手机”也带了进来，“苹果手机”一目了然——“苹果”被正确理解为<b>品牌</b>（85%）。这就是双向的价值。";
  } else {
    el.innerHTML="选中“"+toks[sel]+"”。"+(mode==="bi"?"双向下它同时拥有左右上下文。":"单向下它只看得到左边。")+"（点“苹果”看一个会因右文改变含义的例子）";
  }
}
document.getElementById("uni").addEventListener("click",function(){mode="uni";render();});
document.getElementById("bi").addEventListener("click",function(){mode="bi";render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  mode="uni";render();setTimeout(function(){mode="bi";render();},1700);},1000);
})();
</script>
{% endraw %}
