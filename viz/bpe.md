---
layout: default
title: BPE：合并出子词
permalink: /viz/bpe/
redirect_from:
  - /v/bpe/
---

{% raw %}
<style>
.bpelab svg{max-width:100%;height:auto;}
.bpelab .tk{fill:#dceaf5;stroke:#9aa3a8;stroke-width:1;}
.bpelab .tk.hot{fill:#fbeec2;stroke:var(--color-gold);stroke-width:2;}
.bpelab .tt{font:13px var(--font-mono);fill:#1a1a1a;}
.bpelab .lbl{font:11px var(--font-sans);fill:var(--color-text-muted);}
.bpelab .rule{font:12px var(--font-mono);fill:var(--color-forest);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# BPE：合并出子词

大模型不是按字、也不是按整词来切句子，而是切成**子词**——常见词整块、生僻词拆成小块。怎么决定切法？最常用的算法 **BPE（字节对编码）**很朴素：先把所有词拆成单个字符，然后**反复找出现最频繁的相邻字符对**，把它合并成一个新单元，再找下一个最频繁的对……合并几千上万次，高频组合（如 “ing”“est”）自然就长成了一个个子词。点“合并”，看一堆字符怎样一步步并成子词。

<section class="vizui bpelab" id="bpelab">
  <p class="vizui__lead">语料里 4 个词（右边数字是出现频次）。当前每个词的切分用方块表示；金色是这一步要合并的<b>最高频相邻对</b>。下方是已学到的合并规则。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <button class="vizui-btn vizui-btn--go" id="step" type="button">▶ 合并最高频对</button>
      <button class="vizui-btn" id="auto" type="button">自动</button>
      <button class="vizui-btn" id="reset" type="button">重置</button>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stat">0 次合并</span>
    </div>
    <svg id="plane" viewBox="0 0 470 270" role="img" aria-label="BPE 合并"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>从字符起步</b><p>初始词表就是所有单字符，任何词都能拼出来（不会有“未登录词”）。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>贪心合并高频对</b><p>每步把最常一起出现的相邻对合成新单元，高频组合逐渐变成子词。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>子词折中</b><p>常见词整块、生僻词拆小块——在“按字”和“按词”之间取得效率与覆盖的平衡。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var init=[{w:["l","o","w"],f:5},{w:["l","o","w","e","r"],f:2},{w:["n","e","w","e","s","t"],f:6},{w:["w","i","d","e","s","t"],f:3}];
var toks,merges,timer=null;
function reset(){toks=init.map(function(c){return {w:c.w.slice(),f:c.f};});merges=[];}
reset();
function bestPair(){var cnt={};toks.forEach(function(t){for(var i=0;i<t.w.length-1;i++){var p=t.w[i]+""+t.w[i+1];cnt[p]=(cnt[p]||0)+t.f;}});var best=null,bc=0;for(var p in cnt)if(cnt[p]>bc){bc=cnt[p];best=p;}return best?{a:best.split("")[0],b:best.split("")[1],c:bc}:null;}
function doMerge(){var bp=bestPair();if(!bp)return false;var m=bp.a+bp.b;merges.push({a:bp.a,b:bp.b,m:m,c:bp.c});toks.forEach(function(t){var nw=[];for(var i=0;i<t.w.length;i++){if(i<t.w.length-1&&t.w[i]===bp.a&&t.w[i+1]===bp.b){nw.push(m);i++;}else nw.push(t.w[i]);}t.w=nw;});return true;}
var SVGNS="http://www.w3.org/2000/svg";
function E(p,t,a,txt){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;p.appendChild(e);return e;}
function render(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var nb=bestPair();
  for(var r=0;r<toks.length;r++){
    var t=toks[r],y=24+r*40,x=20;
    for(var i=0;i<t.w.length;i++){
      var hot=nb&&i<t.w.length-1&&t.w[i]===nb.a&&t.w[i+1]===nb.b;
      var w=Math.max(22,t.w[i].length*9+12);
      E(svg,"rect",{x:x,y:y,width:w,height:26,rx:4,"class":"tk"+(hot?" hot":"")});
      E(svg,"text",{x:x+w/2,y:y+18,"text-anchor":"middle","class":"tt"},t.w[i]);
      x+=w+4;
    }
    E(svg,"text",{x:x+8,y:y+18,"class":"lbl"},"×"+t.f);
  }
  E(svg,"text",{x:20,y:200,"class":"lbl"},"已学合并规则：");
  var rx=20;
  for(var k=0;k<merges.length;k++){var s=merges[k].a+"+"+merges[k].b+"→"+merges[k].m;E(svg,"text",{x:rx,y:222,"class":"rule"},s);rx+=s.length*7.5+14;if(rx>430){rx=20;}}
  if(nb)E(svg,"text",{x:20,y:252,"class":"lbl"},"下一步：合并最高频对 “"+nb.a+nb.b+"”（出现 "+nb.c+" 次）");
  else E(svg,"text",{x:20,y:252,"class":"lbl",style:"fill:var(--color-forest);font-weight:600"},"没有可再合并的高频对了（每个词已基本整块）。");
  document.getElementById("stat").textContent=merges.length+" 次合并";
  caption(nb);
}
function caption(nb){
  var el=document.getElementById("caption");
  if(merges.length===0)el.innerHTML="一开始全是单字符。最频繁的相邻对是 “"+(nb?nb.a+nb.b:"")+"”——点“合并”把它并成一个子词。";
  else if(nb)el.innerHTML="已合并 "+merges.length+" 次。最近学到 “"+merges[merges.length-1].m+"”。下一个最高频对是 “"+nb.a+nb.b+"”。高频组合正一步步长成子词。";
  else el.innerHTML="合并完成：常见组合（如 “"+(merges.length?merges[merges.length-1].m:"")+"”、“est”）都成了整块子词。真实 BPE 在海量语料上合并几万次，得到大模型的词表。";
}
document.getElementById("step").addEventListener("click",function(){doMerge();render();});
document.getElementById("auto").addEventListener("click",function(){if(timer)return;timer=setInterval(function(){if(!doMerge()){clearInterval(timer);timer=null;}render();},800);});
document.getElementById("reset").addEventListener("click",function(){if(timer){clearInterval(timer);timer=null;}reset();render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){for(var k=0;k<6;k++)doMerge();render();return;}
  timer=setInterval(function(){if(!doMerge()||merges.length>=7){clearInterval(timer);timer=null;}render();},900);},1000);
})();
</script>
{% endraw %}
