---
layout: default
title: 自回归：一个字一个字生成
permalink: /viz/autoregressive/
redirect_from:
  - /v/autoregressive/
---

{% raw %}
<style>
.arlab svg{max-width:100%;height:auto;}
.arlab .tok{fill:#dceaf5;stroke:#9aa3a8;stroke-width:1;}
.arlab .tok.new{fill:#fbeec2;stroke:var(--color-gold);stroke-width:2;}
.arlab .ttext{font:15px var(--font-sans);fill:#1a1a1a;}
.arlab .bar{fill:#cdd6db;}
.arlab .bar.pick{fill:var(--color-accent);}
.arlab .lbl{font:12px var(--font-sans);fill:#333;}
.arlab .loop{fill:none;stroke:var(--color-forest);stroke-width:2;stroke-dasharray:4 3;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 自回归：一个字一个字生成

GPT 写文章，不是一次性吐出一整段，而是**一个字一个字往外蹦**：看着目前已经写出的内容，预测下一个最可能的字，写下它；然后把这个新字**接回输入**，再预测下一个……如此循环，直到写完。这种“拿自己刚写的当输入、继续往下写”的方式叫**自回归**。点“下一词”，看它怎样一步步把句子接出来，注意每写一个字，输入就长一点、再喂回去。

<section class="vizui arlab" id="arlab">
  <p class="vizui__lead">上面一行是已生成的内容（绿色箭头表示“接回输入”）。下面是模型对<b>下一个词</b>的概率预测，最高的那个（蓝色）被选中、添加到句尾。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <button class="vizui-btn vizui-btn--go" id="step" type="button">▶ 下一词</button>
      <button class="vizui-btn" id="auto" type="button">自动生成</button>
      <button class="vizui-btn" id="reset" type="button">重置</button>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stat">已生成 0 词</span>
    </div>
    <svg id="plane" viewBox="0 0 470 250" role="img" aria-label="自回归生成"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>预测下一词</b><p>每步只做一件事：根据已有内容，给词表里每个词打一个概率。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>接回输入</b><p>选出的词被拼到序列末尾，作为下一步的输入——“自”己的输出“回”到输入。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>逐词成文</b><p>循环几十上百次，就从一个开头“长”出整段文字。慢，但每步都可控。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var steps=[
 {cand:[["小猫",0.52],["小狗",0.24],["今天",0.16]]},
 {cand:[["趴",0.46],["躺",0.28],["跑",0.18]]},
 {cand:[["在",0.62],["到",0.2],["着",0.12]]},
 {cand:[["窗台",0.44],["沙发",0.31],["地上",0.17]]},
 {cand:[["上",0.78],["边",0.12],["里",0.07]]},
 {cand:[["晒",0.5],["睡",0.3],["发",0.13]]},
 {cand:[["太阳",0.66],["毛",0.18],["着",0.1]]},
 {cand:[["。",0.8],["，",0.13],["呢",0.05]]}
];
var gen=[],i=0,timer=null;
var SVGNS="http://www.w3.org/2000/svg",W=470;
function E(p,t,a,txt){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;p.appendChild(e);return e;}
function render(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  // 生成序列
  var bx=14,by=20,bw;
  E(svg,"text",{x:14,y:14,"class":"lbl"},"已生成：");
  for(var t=0;t<gen.length;t++){bw=Math.max(34,gen[t].length*16+12);
    var isnew=(t===gen.length-1);
    E(svg,"rect",{x:bx,y:by,width:bw,height:32,rx:5,"class":"tok"+(isnew?" new":"")});
    E(svg,"text",{x:bx+bw/2,y:by+21,"text-anchor":"middle","class":"ttext"},gen[t]);
    bx+=bw+6;
  }
  if(gen.length===0)E(svg,"text",{x:64,y:by+21,"class":"lbl"},"（点“下一词”开始）");
  // 当前预测
  if(i<steps.length){
    E(svg,"text",{x:14,y:96,"class":"lbl"},"下一词预测：");
    var c=steps[i].cand,bx2=24,bw2=120;
    for(var k=0;k<c.length;k++){
      var y=110+k*38;
      E(svg,"text",{x:bx2+30,y:y+18,"text-anchor":"end","class":"ttext"},c[k][0]);
      E(svg,"rect",{x:bx2+40,y:y,width:c[k][1]*300,height:24,rx:3,"class":"bar"+(k===0?" pick":""),opacity:(0.4+0.6*c[k][1]).toFixed(2)});
      E(svg,"text",{x:bx2+48+c[k][1]*300,y:y+17,"class":"lbl"},(c[k][1]*100).toFixed(0)+"%");
    }
    // 接回输入的环
    E(svg,"path",{d:"M 430 118 q 28 40 0 -78","class":"loop",transform:"translate(0,0)"});
    E(svg,"text",{x:404,y:104,"class":"lbl",style:"fill:var(--color-forest)"},"↻ 接回");
  } else {
    E(svg,"text",{x:14,y:120,"class":"lbl",style:"fill:var(--color-forest);font-weight:600"},"✓ 句子生成完毕。");
  }
  document.getElementById("stat").textContent="已生成 "+gen.length+" 词";
  caption();
}
function caption(){
  var el=document.getElementById("caption");
  if(gen.length===0)el.innerHTML="模型还没动笔。点“下一词”：它会先预测下一个字的概率，挑最高的写下来。";
  else if(i<steps.length)el.innerHTML="第 "+gen.length+" 步：刚写下“<b>"+gen[gen.length-1]+"</b>”。它被接回输入，模型据此再预测下一个字——这就是自回归的循环。";
  else el.innerHTML="生成结束：“<b>"+gen.join("")+"</b>”。整句话是一个字一个字、每次把已写内容喂回去接出来的。";
}
function next(){if(i>=steps.length)return;gen.push(steps[i].cand[0][0]);i++;render();}
document.getElementById("step").addEventListener("click",function(){if(timer){clearInterval(timer);timer=null;}next();});
document.getElementById("auto").addEventListener("click",function(){if(timer)return;timer=setInterval(function(){next();if(i>=steps.length){clearInterval(timer);timer=null;}},700);});
document.getElementById("reset").addEventListener("click",function(){if(timer){clearInterval(timer);timer=null;}gen=[];i=0;render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){while(i<steps.length)next();return;}
  timer=setInterval(function(){next();if(i>=steps.length){clearInterval(timer);timer=null;}},750);},1000);
})();
</script>
{% endraw %}
