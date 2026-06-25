---
layout: default
title: RNN 当计数器
description: "喂一串括号，看某个隐状态神经元自己学成计数器——遇“(”加一、遇“)”减一，隐状态里原来存着看得懂的信息。"
permalink: /viz/rnn-counter/
redirect_from:
  - /v/rnn-counter/
---

{% raw %}
<style>
.rclab svg{max-width:100%;height:auto;}
.rclab .axis{stroke:var(--color-border-strong);stroke-width:1;}
.rclab .br{fill:#dceaf5;stroke:#9aa3a8;stroke-width:1;}
.rclab .br.cur{fill:#fbeec2;stroke:var(--color-gold);stroke-width:2;}
.rclab .btext{font:16px var(--font-mono);fill:#1a1a1a;}
.rclab .depth{fill:none;stroke:var(--color-accent);stroke-width:2.5;}
.rclab .area{fill:var(--color-accent);opacity:.1;}
.rclab .lbl{font:11px var(--font-sans);fill:var(--color-text-muted);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# RNN 当计数器

RNN 的隐状态到底存了什么？这个例子能让你“看见”。给 RNN 喂一串括号，要它判断括号是否配对。训练之后会发现：它的某个隐状态神经元，竟然自己学成了一个**计数器**——遇到“(”就把数字加一、遇到“)”就减一，时刻记着当前的**嵌套深度**。这说明隐状态能存下有意义、可解释的信息，RNN 也能做这种“记着一个状态往前推”的任务。点“下一个”，看这个计数器神经元随括号起落。

<section class="vizui rclab" id="rclab">
  <p class="vizui__lead">上面是逐个读入的括号（金色是当前）。下面的折线是“计数器神经元”的值＝当前嵌套深度：遇 “(” 上升、遇 “)” 下降。读完若回到 0 且全程不为负，就是配对合法。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <button class="vizui-btn vizui-btn--go" id="step" type="button">▶ 下一个</button>
      <button class="vizui-btn" id="auto" type="button">自动</button>
      <button class="vizui-btn" id="seq" type="button">↻ 换序列</button>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stat">深度 0</span>
    </div>
    <svg id="plane" viewBox="0 0 470 230" role="img" aria-label="RNN 计数器"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>隐状态可解释</b><p>某个神经元的值正好等于嵌套深度——隐状态里装着看得懂的信息。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>状态机能力</b><p>“加一减一、记住当前值”就是一台计数器，RNN 天生能学这种顺序状态推进。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>读懂结构</b><p>计数、配对、匹配这类需要记着上下文的任务，正是序列模型的拿手好戏。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var SEQS=["(()(()))","((())()","(())())"],si=0,seq=SEQS[0].split(""),step=0,timer=null;
var SVGNS="http://www.w3.org/2000/svg",W=470,H=230,pl=30,pr=14,pt=80,pb=28,MAXD=4,MIND=-1;
function E(p,t,a,txt){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;p.appendChild(e);return e;}
function depths(){var d=[0],c=0,bad=false;for(var i=0;i<seq.length;i++){c+=(seq[i]==="(")?1:-1;if(c<0)bad=true;d.push(c);}return {d:d,bad:bad,end:c};}
function px(i){return pl+i*((W-pl-pr)/seq.length);}
function py(v){return (H-pb)-((v-MIND)/(MAXD-MIND))*(H-pt-pb);}
function render(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var bw=(W-pl-pr)/seq.length;
  for(var i=0;i<seq.length;i++){var cur=(i===step-1);E(svg,"rect",{x:px(i)+bw/2-15,y:24,width:30,height:34,rx:5,"class":"br"+(cur?" cur":""),opacity:(i<step?1:0.3)});E(svg,"text",{x:px(i)+bw/2,y:47,"text-anchor":"middle","class":"btext",opacity:(i<step?1:0.3)},seq[i]);}
  // 坐标
  E(svg,"line",{x1:pl,y1:py(0),x2:W-pr,y2:py(0),"class":"axis"});E(svg,"line",{x1:pl,y1:pt,x2:pl,y2:H-pb,"class":"axis"});
  for(var v=MIND;v<=MAXD;v++)E(svg,"text",{x:pl-5,y:py(v)+3,"text-anchor":"end","class":"lbl"},v);
  E(svg,"text",{x:pl-5,y:pt-4,"text-anchor":"end","class":"lbl"},"深度");
  // 深度折线（到 step）
  var dd=depths().d,pts=[];var xd=function(s){return s===0?pl:pl+(s-0.5)*bw;};for(var s=0;s<=step;s++)pts.push(xd(s)+","+py(dd[s]));
  var y0=py(0);
  if(step>=1){E(svg,"polygon",{points:(pl)+","+y0+" "+pts.join(" ")+" "+xd(step)+","+y0,"class":"area"});E(svg,"polyline",{points:pts.join(" "),"class":"depth"});}
  for(var s2=0;s2<=step;s2++)E(svg,"circle",{cx:xd(s2),cy:py(dd[s2]),r:3,fill:dd[s2]<0?"#b5524a":"var(--color-accent)"});
  var curd=dd[step];
  document.getElementById("stat").textContent="深度 "+curd;
  caption(curd);
}
function caption(curd){
  var el=document.getElementById("caption");
  var info=depths();
  if(step===0)el.innerHTML="计数器从 0 开始。点“下一个”读入括号，看深度怎样起落。";
  else if(step<seq.length)el.innerHTML="读到第 "+step+" 个是“"+seq[step-1]+"”，计数器"+(seq[step-1]==="("?"加一":"减一")+"到 <b>"+curd+"</b>。这个神经元就这样默默记着当前嵌套了多深。";
  else el.innerHTML=info.bad?("读完了：中途深度变成过负数——出现了多余的“)”，<b>括号不合法</b>。计数器一眼看穿。"):(info.end===0?("读完了：计数器回到 <b>0</b> 且全程非负——<b>括号完全配对</b>！一个神经元 + 隐状态就实现了括号匹配。"):("读完了：计数器停在 <b>"+info.end+"</b>（没回到 0）——有“(”没合上，<b>不配对</b>。"));
}
function next(){if(step>=seq.length)return;step++;render();}
document.getElementById("step").addEventListener("click",next);
document.getElementById("auto").addEventListener("click",function(){if(timer)return;timer=setInterval(function(){next();if(step>=seq.length){clearInterval(timer);timer=null;}},600);});
document.getElementById("seq").addEventListener("click",function(){if(timer){clearInterval(timer);timer=null;}si=(si+1)%SEQS.length;seq=SEQS[si].split("");step=0;render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){step=seq.length;render();return;}
  timer=setInterval(function(){next();if(step>=seq.length){clearInterval(timer);timer=null;}},650);},1000);
})();
</script>
{% endraw %}
