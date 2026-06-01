---
layout: default
title: 投机解码：小模型起草、大模型核验
permalink: /viz/speculative-decoding/
redirect_from:
  - /v/speculative-decoding/
---

{% raw %}
<style>
.splab svg{max-width:100%;height:auto;}
.splab .tok{stroke:#fff;stroke-width:1.5;}
.splab .ok{fill:#cfe6cf;stroke:var(--color-forest);}
.splab .rej{fill:#f3d2cf;stroke:#b5524a;}
.splab .dis{fill:#e6e6e6;stroke:#bbb;}
.splab .cor{fill:#fbeec2;stroke:var(--color-gold);stroke-width:2;}
.splab .fin{fill:#dceaf5;stroke:#9aa3a8;}
.splab .ttext{font:14px var(--font-sans);fill:#1a1a1a;}
.splab .lbl{font:12px var(--font-sans);fill:#333;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 投机解码：小模型起草、大模型核验

大模型逐词生成很慢，因为每吐一个字都要把整个大模型跑一遍。**投机解码**用一个又快又小的“草稿模型”先一口气**猜好几个字**，再让大模型**一次并行核验**这几个字：从头开始对，猜对的全部采纳，遇到第一个猜错的就在那里纠正、丢掉后面，然后继续下一轮。猜得越准，一次大模型前向就能确定越多字——**速度大涨，结果还和大模型逐字生成完全一致**。点“下一轮”，看草稿被核验、采纳或纠正。

<section class="vizui splab" id="splab">
  <p class="vizui__lead">上面是最终确定的输出。下面每一轮：草稿模型提议 4 个字，大模型核验——<span style="color:var(--color-forest)">绿=猜对采纳</span>、<span style="color:#b5524a">红=第一个猜错</span>、灰=被丢弃、<span style="color:var(--color-gold)">金=大模型纠正/补的字</span>。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <button class="vizui-btn vizui-btn--go" id="step" type="button">▶ 下一轮</button>
      <button class="vizui-btn" id="auto" type="button">自动</button>
      <button class="vizui-btn" id="reset" type="button">重置</button>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stat">—</span>
    </div>
    <svg id="plane" viewBox="0 0 470 250" role="img" aria-label="投机解码"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-forest)"><b>小模型起草</b><p>便宜的草稿模型一次猜 K 个字，速度快但不一定都对。</p></div>
    <div class="card" style="--wc:var(--color-accent)"><b>大模型并行核验</b><p>大模型一次前向就能同时检查这 K 个字，采纳猜对的前缀。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>又快又不走样</b><p>纠正机制保证最终输出和大模型逐字生成一模一样，只是用更少的前向次数。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var target=["人工","智能","正在","深刻","改变","世界","的","运行","方式","。"];
var draft =["人工","智能","正在","迅速","改变","世界","我们","运行","生活","。"];
var rounds=[],pos=0;
while(pos<target.length){
  var prop=[],p=pos,acc=0,mm=-1;
  for(var j=0;j<4&&p<target.length;j++,p++){
    if(mm<0){ if(draft[p]===target[p]){prop.push({tok:draft[p],st:"ok"});acc++;} else {prop.push({tok:draft[p],st:"rej"});mm=j;} }
    else prop.push({tok:draft[p],st:"dis"});
  }
  var corr=(pos+acc<target.length)?target[pos+acc]:null;
  rounds.push({prop:prop,acc:acc,corr:corr});
  pos=pos+acc+(corr?1:0);
}
var cur=0,timer=null,SVGNS="http://www.w3.org/2000/svg";
function E(p,t,a,txt){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;p.appendChild(e);return e;}
function assembled(upto){var out=[];for(var r=0;r<upto;r++){var R=rounds[r];for(var i=0;i<R.acc;i++)out.push(R.prop[i].tok);if(R.corr)out.push(R.corr);}return out;}
function box(svg,x,y,w,tok,cls){E(svg,"rect",{x:x,y:y,width:w,height:30,rx:5,"class":"tok "+cls});E(svg,"text",{x:x+w/2,y:y+20,"text-anchor":"middle","class":"ttext"},tok);}
function render(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var fin=assembled(cur),bx=14;
  E(svg,"text",{x:14,y:14,"class":"lbl"},"最终输出：");
  for(var i=0;i<fin.length;i++){var w=Math.max(34,fin[i].length*15+12);box(svg,bx,22,w,fin[i],"fin");bx+=w+5;}
  if(cur>0&&cur<=rounds.length){
    var R=rounds[cur-1];
    E(svg,"text",{x:14,y:96,"class":"lbl"},"第 "+cur+" 轮 · 草稿提议："); 
    var x=24;
    for(var j=0;j<R.prop.length;j++){var pj=R.prop[j],w2=Math.max(40,pj.tok.length*15+14);box(svg,x,108,w2,pj.tok,pj.st==="ok"?"ok":pj.st==="rej"?"rej":"dis");x+=w2+6;}
    E(svg,"text",{x:14,y:166,"class":"lbl"},"大模型核验 → 采纳 "+R.acc+" 个"+(R.corr?("，纠正/补：")+"":""));
    if(R.corr){box(svg,150,152,Math.max(40,R.corr.length*15+14),R.corr,"cor");}
  }
  var normal=target.length;
  document.getElementById("stat").textContent="大模型前向 "+cur+" 次（普通需 "+normal+" 次）";
  caption(fin.length,normal);
}
function caption(done,normal){
  var el=document.getElementById("caption");
  if(cur===0)el.innerHTML="点“下一轮”。草稿模型会一口气猜 4 个字，大模型一次核验。";
  else if(cur<rounds.length)el.innerHTML="第 "+cur+" 轮：这一轮一次大模型前向就敲定了好几个字。继续看，最后比一比总次数。";
  else el.innerHTML="完成！整句 "+normal+" 个字，投机解码只用了 <b>"+rounds.length+" 次</b>大模型前向（普通要 "+normal+" 次），约快 <b>"+(normal/rounds.length).toFixed(1)+"×</b>——而且输出和逐字生成完全一致。";
}
function next(){if(cur>=rounds.length)return;cur++;render();}
document.getElementById("step").addEventListener("click",next);
document.getElementById("auto").addEventListener("click",function(){if(timer)return;timer=setInterval(function(){next();if(cur>=rounds.length){clearInterval(timer);timer=null;}},900);});
document.getElementById("reset").addEventListener("click",function(){if(timer){clearInterval(timer);timer=null;}cur=0;render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){cur=rounds.length;render();return;}
  timer=setInterval(function(){next();if(cur>=rounds.length){clearInterval(timer);timer=null;}},950);},1000);
})();
</script>
{% endraw %}
