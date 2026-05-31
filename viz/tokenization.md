---
layout: default
title: 词元化
permalink: /viz/tokenization/
redirect_from:
  - /v/tokenization/
---

{% raw %}
<style>
.tklab .tkinput{width:100%;font-family:var(--font-serif);font-size:1.1rem;padding:11px 14px;border:1px solid var(--color-border-strong);border-radius:var(--radius-md);background:var(--color-bg-pure);color:var(--color-text);}
.tklab .tkinput:focus{outline:none;border-color:var(--color-accent);box-shadow:0 0 0 3px var(--color-accent-soft);}
.tklab .presets{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px;}
.tklab .preset{appearance:none;font:inherit;font-size:.86rem;cursor:pointer;padding:6px 12px;border-radius:999px;border:1px solid var(--color-border);background:var(--color-bg-section);color:var(--color-text-soft);}
.tklab .preset:hover{border-color:var(--color-accent);color:var(--color-accent);}
.tklab .toks{display:flex;flex-wrap:wrap;gap:6px;margin:4px 0 2px;min-height:44px;align-items:center;}
.tklab .tkchip{font-family:var(--font-serif);font-size:1.12rem;padding:7px 10px;border-radius:8px;border:1px solid;line-height:1.1;}
.tklab .tkchip .sp{color:var(--color-text-muted);opacity:.7;}
.tklab .tkcount{font:600 .95rem var(--font-mono);color:var(--color-accent);}
</style>
{% endraw %}

<a class="viz-back" href="{{ '/viz/' | relative_url }}">可视化资源</a>

# 词元化

大模型读不懂``字''，它读的是``词元''（token）——一段文字会先被切成一个个词元，模型再逐个处理。切法挺反直觉：常见词是一整块，生僻长词被拆成几片，每个汉字往往单独一块，连空格都算进词元里。这也解释了一个经典糗事：模型数不清``strawberry''里有几个 r——因为它压根没看见一个个字母。在下面输入文字，看它被切成什么。

<section class="vizui tklab" id="tklab">
  <p class="vizui__lead">下面是一个``示意版''分词器（非真实 GPT，但抓住了关键规律）。试试预设例子，或自己输入。</p>

  <div class="vizui-panel">
    <input class="tkinput" id="text" type="text" value="strawberry" autocomplete="off" spellcheck="false">
    <div class="presets" id="presets">
      <button class="preset" type="button" data-t="strawberry">strawberry</button>
      <button class="preset" type="button" data-t="ChatGPT is amazing!">ChatGPT is amazing!</button>
      <button class="preset" type="button" data-t="深度学习真有意思">深度学习真有意思</button>
      <button class="preset" type="button" data-t="1234567 个苹果">1234567 个苹果</button>
    </div>
  </div>

  <div class="vizui-panel">
    <p class="vizui-panel__title">切成的词元（共 <span class="tkcount" id="count">0</span> 个）</p>
    <div class="toks" id="toks"></div>
  </div>

  <div class="vizui-caption" id="caption"></div>

  <div class="vizui-why">
    <div class="card" style="--wc:var(--color-accent)"><b>常见词一整块</b><p>越常见的词越可能是单独一个词元；生僻或长的词被拆成几片（子词）。</p></div>
    <div class="card" style="--wc:var(--color-gold)"><b>汉字按字切</b><p>中文通常一个字一个词元，所以同样信息量，中文往往比英文占更多词元。</p></div>
    <div class="card" style="--wc:var(--color-forest)"><b>看不见字母</b><p>模型眼里``strawberry''是一两块词元，不是 10 个字母——所以让它数 r 常常出错。</p></div>
  </div>
</section>

{% raw %}
<script>
(function(){
"use strict";
/* 示意词表：贪心最长匹配（不区分大小写），匹配不到就退回 2 字符片段 */
var VOCAB=["straw","berry","chat","gpt","amazing","apple","apples","hello","world","deep","learning","model","tokens","token","neural","network","language","please","today","weather","good","cat","dog","is","are","the","and","to","of","in","it","you","ing","tion","ed","ly","er","un","re","pre","able","ness","ment"];
VOCAB.sort(function(a,b){return b.length-a.length;});
var COLORS=["#155e75","#b7791f","#206a4f","#2563eb","#6d5bd0","#0e7490"];

function tokWord(w){ // 纯字母词 → 子词列表
  var out=[],i=0,lw=w.toLowerCase();
  while(i<w.length){
    var hit=null;
    for(var v=0;v<VOCAB.length;v++){var p=VOCAB[v];if(lw.substr(i,p.length)===p){hit=p.length;break;}}
    if(!hit)hit=Math.min(2,w.length-i);
    out.push(w.substr(i,hit)); i+=hit;
  }
  return out;
}
function tokenize(s){
  var segs=s.match(/ ?[A-Za-z]+| ?[0-9]+| ?[一-鿿]| ?[^A-Za-z0-9一-鿿]/g)||[];
  var toks=[];
  segs.forEach(function(seg){
    var sp=seg[0]===" "; var body=sp?seg.slice(1):seg;
    var pieces;
    if(/^[A-Za-z]+$/.test(body)) pieces=tokWord(body);
    else if(/^[0-9]+$/.test(body)){pieces=[];for(var i=0;i<body.length;i+=3)pieces.push(body.substr(i,3));}
    else pieces=[body];                       /* 单个汉字 / 标点 */
    pieces.forEach(function(p,i){toks.push({t:p, sp: sp&&i===0});});
  });
  return toks;
}

function render(){
  var s=document.getElementById("text").value;
  var toks=tokenize(s), host=document.getElementById("toks"); host.innerHTML="";
  toks.forEach(function(tk,i){
    var c=COLORS[i%COLORS.length];
    var chip=document.createElement("span"); chip.className="tkchip";
    chip.style.borderColor=c; chip.style.background=c+"14"; chip.style.color=c;
    chip.innerHTML=(tk.sp?'<span class="sp">␣</span>':'')+tk.t.replace(/</g,"&lt;");
    host.appendChild(chip);
  });
  document.getElementById("count").textContent=toks.length;
  caption(s,toks);
}
function caption(s,toks){
  var el=document.getElementById("caption"), n=toks.length, chars=s.replace(/\s/g,"").length;
  var msg;
  if(/strawberry/i.test(s)) msg="``strawberry''被切成 <b>"+n+"</b> 个词元，而不是 10 个字母。模型从没单独看见过每个 r，所以一让它数 r 就容易答错。";
  else if(/[一-鿿]/.test(s)&&!/[A-Za-z]/.test(s)) msg="这串中文被切成 <b>"+n+"</b> 个词元——基本一个字一个。中文信息密度高，同样意思常比英文占更多词元。";
  else if(/[0-9]{4,}/.test(s)) msg="数字被切成一块块（每几位一个词元），而不是一位一位——这也是大模型算数容易出错的原因之一。";
  else msg="这段文字被切成 <b>"+n+"</b> 个词元。常见词是一整块，空格通常归到后一个词的前面（␣）。";
  el.innerHTML=msg;
}

document.getElementById("text").addEventListener("input",render);
document.getElementById("presets").addEventListener("click",function(e){var b=e.target.closest(".preset");if(!b)return;document.getElementById("text").value=b.dataset.t;render();});

/* 启动 + 自动演示：依次展示几个预设 */
render();
setTimeout(function(){
  if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  var seq=["ChatGPT is amazing!","深度学习真有意思","1234567 个苹果","strawberry"],k=0;
  var iv=setInterval(function(){if(k>=seq.length){clearInterval(iv);return;}document.getElementById("text").value=seq[k];render();k++;},1500);
},1000);
})();
</script>
{% endraw %}
