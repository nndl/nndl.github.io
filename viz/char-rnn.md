---
layout: default
title: 字符级 RNN：一个字母一个字母地写
description: "一个字母一个字母地写：靠隐状态记着上文，q 后面自然接 u，字符拼成合理的词——更细颗粒的自回归。"
permalink: /viz/char-rnn/
redirect_from:
  - /v/char-rnn/
---

{% raw %}
<style>
.crlab svg{max-width:100%;height:auto;}
.crlab .ch{fill:#dceaf5;stroke:#9aa3a8;stroke-width:1;}
.crlab .ch.new{fill:#fbeec2;stroke:var(--color-gold);stroke-width:2;}
.crlab .ctext{font:16px var(--font-mono);fill:#1a1a1a;}
.crlab .bar{fill:#cdd6db;}
.crlab .bar.pick{fill:var(--color-accent);}
.crlab .lbl{font:11px var(--font-sans);fill:var(--color-text-muted);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 字符级 RNN：一个字母一个字母地写

语言模型不一定按词来，也可以**按字符**来：每次只预测下一个字母，写下，再喂回去。听起来很难——光靠单个字母怎么拼出像样的词？靠的正是 RNN 的**隐状态**：它一路记着“现在拼到哪、前面是什么”，于是 q 后面大概率接 u、字母们自然组装成合理的词，而不是乱码。这其实就是字符级的“自回归”，只是颗粒更细。点“下一字”，看隐状态一边更新、一边把字母拼成词。

<section class="vizui crlab" id="crlab">
  <p class="vizui__lead">上面是已写出的字符（金色是刚写的）。中间 4 根小条是隐状态（RNN 的“记忆”），下面是对下一个字符的概率预测——最高的那个被选中。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <button class="vizui-btn vizui-btn--go" id="step" type="button">▶ 下一字</button>
      <button class="vizui-btn" id="auto" type="button">自动</button>
      <button class="vizui-btn" id="nextw" type="button">↻ 换个词</button>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stat">—</span>
    </div>
    <svg id="plane" viewBox="0 0 470 240" role="img" aria-label="字符级 RNN"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>颗粒到字符</b><p>词表只有几十个字符，却能拼出任意词——连没见过的新词也拼得出。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>隐状态记上文</b><p>正因为隐状态记着已写内容，字母才会合理衔接（q→u），不是乱码。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>同样是自回归</b><p>写一个、喂回去、再写一个——和词级生成同理，只是更细。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var WORDS=[
 [["n",[["e",0.55],["a",0.25],["o",0.1]]],["e",[["u",0.5],["t",0.2],["r",0.15]]],["u",[["r",0.6],["l",0.2],["n",0.1]]],["r",[["a",0.5],["o",0.25],["e",0.15]]],["a",[["l",0.7],["r",0.15],["s",0.1]]],["l",[["·",0.9]]]],
 [["m",[["o",0.55],["a",0.2],["e",0.15]]],["o",[["d",0.5],["t",0.2],["n",0.15]]],["d",[["e",0.6],["a",0.2],["i",0.1]]],["e",[["l",0.65],["r",0.15],["s",0.1]]],["l",[["·",0.9]]]]
];
var wi=0,gen=[],step=0,timer=null,D=4;
function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var x=Math.imul(s^s>>>15,1|s);x=x+Math.imul(x^x>>>7,61|x)^x;return((x^x>>>14)>>>0)/4294967296;};}
function hstate(t){var r=rng(91+wi*13+t*7),h=[];for(var d=0;d<D;d++)h.push(Math.tanh((r()*2-1)*1.4));return h;}
var SVGNS="http://www.w3.org/2000/svg";
function E(p,t,a,txt){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;p.appendChild(e);return e;}
function render(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  E(svg,"text",{x:16,y:16,"class":"lbl"},"已生成：");
  var x=18;
  for(var i=0;i<gen.length;i++){var nw=(i===gen.length-1);E(svg,"rect",{x:x,y:24,width:30,height:34,rx:5,"class":"ch"+(nw?" new":"")});E(svg,"text",{x:x+15,y:47,"text-anchor":"middle","class":"ctext"},gen[i]);x+=34;}
  if(gen.length===0)E(svg,"text",{x:70,y:46,"class":"lbl"},"（点“下一字”开始拼）");
  var h=hstate(step);
  E(svg,"text",{x:16,y:88,"class":"lbl"},"隐状态（记忆）：");
  for(var d=0;d<D;d++){var bh=Math.abs(h[d])*30,bx=120+d*16;E(svg,"rect",{x:bx,y:108-(h[d]>0?bh:0),width:12,height:bh,fill:h[d]<0?"#2563eb":"#b5524a",rx:1});}
  if(step<WORDS[wi].length){
    E(svg,"text",{x:16,y:150,"class":"lbl"},"下一字预测：");
    var c=WORDS[wi][step][1],bx2=40;
    for(var k=0;k<c.length;k++){var y=160+k*24;
      E(svg,"text",{x:bx2,y:y+13,"text-anchor":"end","class":"ctext"},c[k][0]);
      E(svg,"rect",{x:bx2+8,y:y,width:c[k][1]*300,height:17,rx:2,"class":"bar"+(k===0?" pick":""),opacity:(0.4+0.6*c[k][1]).toFixed(2)});
      E(svg,"text",{x:bx2+14+c[k][1]*300,y:y+13,"class":"lbl"},(c[k][1]*100).toFixed(0)+"%");}
  } else E(svg,"text",{x:16,y:165,"class":"lbl",style:"fill:var(--color-forest);font-weight:600"},"✓ 拼出一个完整的词：“"+gen.join("")+"”");
  document.getElementById("stat").textContent="已写 "+gen.length+" 个字符";
  caption();
}
function caption(){
  var el=document.getElementById("caption");
  if(gen.length===0)el.innerHTML="RNN 准备一个字母一个字母地写。点“下一字”。";
  else if(step<WORDS[wi].length)el.innerHTML="刚写下“<b>"+gen[gen.length-1]+"</b>”：隐状态更新后，模型据此预测下一个最可能的字母。注意它给出的都是合理的衔接，不会乱拼。";
  else el.innerHTML="拼完啦：“<b>"+gen.join("")+"</b>”。靠隐状态记住上文，字符级 RNN 也能稳稳拼出合理的词——这就是字符级语言模型。";
}
function next(){if(step>=WORDS[wi].length)return;gen.push(WORDS[wi][step][0]);step++;render();}
document.getElementById("step").addEventListener("click",function(){if(timer){clearInterval(timer);timer=null;}next();});
document.getElementById("auto").addEventListener("click",function(){if(timer){clearInterval(timer);timer=null;return;}timer=setInterval(function(){next();if(step>=WORDS[wi].length){clearInterval(timer);timer=null;}},650);});
document.getElementById("nextw").addEventListener("click",function(){if(timer){clearInterval(timer);timer=null;}wi=(wi+1)%WORDS.length;gen=[];step=0;render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches){while(step<WORDS[wi].length)next();return;}
  timer=setInterval(function(){next();if(step>=WORDS[wi].length){clearInterval(timer);timer=null;}},700);},1000);
})();
</script>
{% endraw %}
