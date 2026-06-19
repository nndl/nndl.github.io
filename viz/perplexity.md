---
layout: default
title: 困惑度：模型有多惊讶
permalink: /viz/perplexity/
redirect_from:
  - /v/perplexity/
---

{% raw %}
<style>
.pplab svg{max-width:100%;height:auto;}
.pplab .wtok{fill:var(--color-bg-soft,#f0ece4);stroke:var(--color-border-strong);stroke-width:1;}
.pplab .pbar{fill:var(--color-accent);}
.pplab .ttext{font:14px var(--font-sans);fill:#1a1a1a;}
.pplab .lbl{font:11px var(--font-sans);fill:var(--color-text-muted);}
.pplab .big{font:30px var(--font-sans);font-weight:700;}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 困惑度：模型有多惊讶

怎么衡量一个语言模型“好不好”？看它读句子时有多**惊讶**。模型每读到一个词，都会先预测它的概率：如果它早就料到这个词（给了高概率），就不惊讶；如果完全没想到（给了低概率），就很惊讶。把整句话每个词的“惊讶程度”平均一下、再取指数，就得到**困惑度（perplexity）**。它有个直观含义：模型平均像是在**多少个词里瞎猜**——困惑度 2 表示它基本在二选一，困惑度 500 表示它几乎在五百个词里乱蒙。困惑度越低，模型越好。切换不同水平的模型，看同一句话的困惑度差多少。

<section class="vizui pplab" id="pplab">
  <p class="vizui__lead">句子：“今天 天气 真 不错”。蓝条是模型对每个词给出的概率（越高=越不惊讶）。下面是整句的困惑度。</p>

  <div class="vizui-panel">
    <div class="vizui-bar">
      <button class="vizui-btn vizui-btn--go" id="g" type="button">好模型</button>
      <button class="vizui-btn" id="m" type="button">一般模型</button>
      <button class="vizui-btn" id="r" type="button">随机模型</button>
      <span class="vizui-spacer"></span>
      <span class="vizui-pill" id="stat">—</span>
    </div>
    <svg id="plane" viewBox="0 0 460 250" role="img" aria-label="困惑度"></svg>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>预测越准越好</b><p>给真实出现的词的概率越高，惊讶越小，困惑度越低。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>≈ 有效选择数</b><p>困惑度=模型平均在“多少个词里挑”，是它不确定性的直观刻度。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>通用评测指标</b><p>语言模型最常用的评测之一，越低代表对语言建模得越好。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
var words=["今天","天气","真","不错"],n=4;
var M={g:[0.45,0.52,0.38,0.61],m:[0.18,0.22,0.15,0.25],r:[0.002,0.002,0.002,0.002]};
var mode="g";
function ppl(p){var s=0;for(var i=0;i<n;i++)s+=-Math.log(p[i]);return Math.exp(s/n);}
var SVGNS="http://www.w3.org/2000/svg",W=460,bw=80,gap=18,baseY=150;
var x0=(W-(n*(bw+gap)-gap))/2;
function E(p,t,a,txt){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;p.appendChild(e);return e;}
function render(){
  var svg=document.getElementById("plane");while(svg.firstChild)svg.removeChild(svg.firstChild);
  var p=M[mode];
  for(var i=0;i<n;i++){
    var x=x0+i*(bw+gap),h=Math.sqrt(p[i])*100;
    E(svg,"rect",{x:x+10,y:baseY-h,width:bw-20,height:h,rx:3,"class":"pbar",opacity:(0.4+0.6*p[i]).toFixed(2)});
    E(svg,"text",{x:x+bw/2,y:baseY-h-6,"text-anchor":"middle","class":"lbl"},(p[i]*100<1?(p[i]*100).toFixed(1):(p[i]*100).toFixed(0))+"%");
    E(svg,"rect",{x:x,y:baseY+6,width:bw,height:30,rx:5,"class":"wtok"});
    E(svg,"text",{x:x+bw/2,y:baseY+26,"text-anchor":"middle","class":"ttext"},words[i]);
  }
  var P=ppl(p),pc=P<5?"var(--color-forest)":P<30?"var(--color-gold)":"#b5524a";
  E(svg,"text",{x:W/2,y:baseY+78,"text-anchor":"middle","class":"big",fill:pc},"困惑度 = "+P.toFixed(1));
  document.getElementById("g").className="vizui-btn"+(mode==="g"?" vizui-btn--go":"");
  document.getElementById("m").className="vizui-btn"+(mode==="m"?" vizui-btn--go":"");
  document.getElementById("r").className="vizui-btn"+(mode==="r"?" vizui-btn--go":"");
  document.getElementById("stat").textContent="PPL "+P.toFixed(1);
  caption(P);
}
function caption(P){
  var el=document.getElementById("caption");
  if(mode==="g")el.innerHTML="<b>好模型：</b>对每个词都给了不低的概率，整句困惑度只有 <b>"+P.toFixed(1)+"</b>——它读这句话时基本不惊讶，像在两个词里挑。";
  else if(mode==="m")el.innerHTML="<b>一般模型：</b>概率给得没那么准，困惑度升到 <b>"+P.toFixed(1)+"</b>——它对这句话更没把握了。";
  else el.innerHTML="<b>随机模型：</b>对每个词都只给了 0.2% 的概率（在五百个词里瞎猜），困惑度高达 <b>"+P.toFixed(0)+"</b>——这就是完全没学会语言的样子。";
}
document.getElementById("g").addEventListener("click",function(){mode="g";render();});
document.getElementById("m").addEventListener("click",function(){mode="m";render();});
document.getElementById("r").addEventListener("click",function(){mode="r";render();});
render();
setTimeout(function(){if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  var seq=["m","r","g"],k=0;var iv=setInterval(function(){mode=seq[k];render();k++;if(k>=seq.length)clearInterval(iv);},1300);},1000);
})();
</script>
{% endraw %}
